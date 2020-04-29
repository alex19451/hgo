from nornir.plugins.tasks.networking import netmiko_send_config
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F
import re
mac = '0050.7966.6806'
def find_mac (task,mac_address):
    var = task.run(task=netmiko_send_command,command_string=f"show mac address-table | include { mac_address}", use_textfsm=True)
    match_int =re.search('\s+\w+\d+/\d+$',var.result)
    if match_int:
      match = match_int.group()
      sh_in = task.run(task=netmiko_send_command,command_string=f"show interfaces { match } sw | i Operational Mode")
      if 'Operational Mode: static access' in sh_in.result:
        result = match
        print(f"mac address {mac_address} find on {task.host} behind {result}")
    else:
      print(f"mac address {mac_address} not found in {task.host}")            
def main():
    nr = InitNornir(config_file="config2.yaml")
    sw = nr.filter(F(groups__contains="switches"))
    r = sw.run(task=find_mac,mac_address=mac)
if __name__ == "__main__":
    main()



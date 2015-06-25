# python-smis-client
Interactive SMI-S client for test about python-wbem

# usage
Basic usage:
./python-smis-client.py -u user_name -p password -l ip_address:portno -n namespace subcommand [option [option..]]

user_name  : login user name for SMI-S server
password   : login password for SMI-S server
ip_address : IP Adress asigned for SMI-S server
portno     : Port Number for SMI-S service in SMI-S server

subcommand : 
  gi -> Get Instance
  ei -> Enumerate Instances
  en -> Enumerate Instance Names
  a  -> Enumerate Associators
  an -> Enumerate Associator Nammes
  r  -> Enumerate References
  rn -> Enumerate Reference Nammes


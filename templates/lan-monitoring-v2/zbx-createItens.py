from zabbix_api import ZabbixAPI
 
zabbix_url = 'http://10.0.0.1:8080/api_jsonrpc.php'
zabbix_user = 'Admin'
zabbix_password = 'zabbix'

network_prefix = '10.100.73.'
template_name = 'Intelbras Auto Discoveried Hosts'
group_name = 'Auto Discoveried Hosts'
 
zapi = ZabbixAPI(server=zabbix_url)
zapi.login(zabbix_user, zabbix_password)
 
template_id = zapi.template.get({
    'filter': {'host': template_name}
})[0]['templateid']
 
group_id = zapi.hostgroup.get({
    'filter': {'name': group_name}
})[0]['groupid']
 
for i in range(1, 255):
    ip = f'{network_prefix}{i}'
    hostname = ip
 
    try:
        existing_host = zapi.host.get({
            'filter': {'host': hostname}
        })
        if existing_host:
            print(f'Host {hostname} já existe.')
            continue
 
        host = zapi.host.create({
            'host': hostname,
            'interfaces': [
                {
                    'type': 1, 
                    'main': 1,
                    'useip': 1,
                    'ip': ip,
                    'dns': '',
                    'port': '10050'
                },
                {
                    'type': 2,  
                    'main': 1,  
                    'useip': 1,
                    'ip': ip,
                    'dns': '',
                    'port': '161',
                    'details': {
                        'version': 2, 
                        'community': '{$SNMP_COMMUNITY}',
                    }
                }
            ],
            'groups': [{'groupid': group_id}],
            'templates': [{'templateid': template_id}]
        })
        print(f'Host {hostname} com IP {ip} criado com sucesso!')
    except Exception as e:
        print(f'Erro ao criar o host {hostname}: {e}')
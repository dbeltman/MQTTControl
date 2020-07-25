import os

import paramiko
from scp import SCPClient

host = os.getenv('REMOTEHOST', '192.168.1.100')
script_path = os.getenv('REMOTESCRIPTPATH', '/home/USER/scripts/dellmqttfan/dellfanctl.sh')
key = paramiko.RSAKey.from_private_key_file(os.getenv('SSHKEYPATH', 'your.key'))
sshusername = os.getenv('SSHUSERNAME', 'user')


def run_command(fullcommand):
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("connecting to " + host + " as " + sshusername)
    conn.connect(hostname=host, username=sshusername, pkey=key)
    command = fullcommand
    print("Executing {}".format(command))
    stdin, stdout, stderr = conn.exec_command(fullcommand)
    output = stdout.read()
    print(stdout.read())
    print("Errors")
    print(stderr.read())
    conn.close()
    print("Disconnected")
    return output


def transfer_file(file):
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("connecting to " + host + " as " + sshusername)
    conn.connect(hostname=host, username=sshusername, pkey=key)
    if file != '':
        with SCPClient(conn.get_transport()) as scp:
            scp.put(file, '/home/' + sshusername)
    conn.close()
    print("Disconnected")
    return 'ok'


def check_install():
    command = 'bash /home/' + sshusername + '/checkinstall.sh'
    transfer_file('scripts/checkinstall.sh')
    return run_command(command)


def set_auto():
    command = "sudo bash " + script_path + " auto"
    return run_command(command)


def set_manual(value):
    commands = "sudo bash " + script_path + " manual && sudo bash " + script_path + " set " + str(value)
    return run_command(commands)

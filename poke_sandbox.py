"""
Pokes the sandbox softly for information with your already configured SSH creds.

Prints out the edx-platform branch and commit
Prints out the cs_comments_service branch and commit
Prints our sandbox expiration

"""
import argparse
import paramiko

SANDBOX_URL = ""  # leave out https://
USERNAME = ""


def poke_sandbox(url, user):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(
    paramiko.AutoAddPolicy())

    ssh.connect(url, username=user)

    print "*************edx-platform*********************"
    stdin, stdout, stderr = ssh.exec_command("cd /edx/app/edxapp/edx-platform; git status")
    print stdout.read()
    stdin, stdout, stderr = ssh.exec_command("cd /edx/app/edxapp/edx-platform; git log -1")
    print stdout.read()
    print "***********cs_comments_service****************"
    stdin, stdout, stderr = ssh.exec_command("cd /edx/app/forum/cs_comments_service; git status")
    print stdout.read()
    stdin, stdout, stderr = ssh.exec_command("cd /edx/app/forum/cs_comments_service; git log -1")
    print stdout.read()

    print "************Sandbox Expiration****************"
    stdin, stdout, stderr = ssh.exec_command("python /edx/etc/playbooks/edx-east/roles/edx-sandbox/templates/etc/update-motd.d/temiate_motd.j2")
    print stdout.read()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sandbox', help='Sandbox URL (without "https://")', default='')
    parser.add_argument('-u', '--user', help='User for sandbox', default='')

    args = parser.parse_args()

    sandbox_url = SANDBOX_URL or args.sandbox or raw_input('Enter Sandbox URL (without "https://"): ')
    print "Sandbox url: " + sandbox_url
    username = USERNAME or args.user or raw_input('Enter User with SSH access: ')
    print "User for sandbox: " + username
    poke_sandbox(sandbox_url, username)


if __name__ == "__main__":
    main()

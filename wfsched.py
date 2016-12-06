#!/usr/bin/python3

import boto3
import time, sys, argparse
import subprocess, random, string

ec2 = boto3.resource('ec2')  # ec2 instance

parser = argparse.ArgumentParser()  # parser for verbosity
parser.add_argument("-v", help="output verbosity", action="store_true")
parser.add_argument("myworkflow", help="work flow directory")
args = parser.parse_args()


def create_myec2_instance():
    if args.v:
        print("creating instance")
    ids1 = []  # creates an instance and terminates all the instances
    ec2.create_instances(ImageId='ami-34913254', MinCount=1, MaxCount=1, InstanceType='t2.micro')
    while 1:
        time.sleep(20)
        running = 0
        instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

        for instance in instances:
            ids1.append(instance.id)
            running = 1
        if running:
            break

    terminate_ec2_instance(ids1)

    sth = ''.join(random.choice(string.ascii_lowercase) for i in range(10))

    # creating a file named sefa.pem that will store the private key
    outfile = open('wdf.pem', 'w')
    keypair = ec2.meta.client.create_key_pair(KeyName='sefa')  # creates key pair
    keyout = str(keypair['KeyMaterial'])  # reads the key material
    outfile.write(keyout)  # writes the key material in sefa.pem

    if args.v:
        print("keypair is created")

    # creates the instance finally
    ec2.create_instances(ImageId='ami-34913254', MinCount=1, MaxCount=1, KeyName='sefa', InstanceType='t2.micro')
    if args.v:
        print("ec2 instance is created")
        print("querying for running instances")


def transfer_files():
    cmd = ' python3 topologicalsort.py ' + sys.argv[1]
    keyfile = '-i ./wdf.pem'
    sshstring = r'ssh -o StrictHostKeyChecking=no '
    scpstring1 = r'scp -Cr '
    machine = ' ubuntu@' + PUB_DNS
    command = sshstring + keyfile + machine + cmd
    scpcommand1 = scpstring1 + keyfile + ' ' + sys.argv[1] + machine + r':'
    scpcommand2 = scpstring1 + keyfile + ' topologicalsort.py' + machine + r':'
    print("waiting 80 secs for instance state running")
    time.sleep(80)
    subprocess.getoutput(scpcommand1)
    subprocess.getoutput(scpcommand2)
    subprocess.check_output(command, shell=True)
    if args.v:
        print("files transferred to the instance")
        print("programs topologically sorted")
        print("programs are executed")


def bring_back_files():
    keyfile = '-i ./wdf.pem'
    scpstring1 = r'scp -Cr '
    machine = ' ubuntu@' + PUB_DNS
    scpcommand1 = scpstring1 + keyfile + machine + r':~/' + sys.argv[1] + ' ' + '~/Downloads/2016400372BALIK'
    scpcommand2 = scpstring1 + keyfile + machine + r':~/out.txt' + ' ' + '~/Downloads/2016400372BALIK'
    subprocess.getoutput('mkdir ~/Downloads/2016400372BALIK')
    subprocess.getoutput(scpcommand1)
    subprocess.getoutput(scpcommand2)
    print(
        r'Files brought back to ~/Downloads/2016400372BALIK. You can also check "out.txt" in ~/Downloads/2016400372BALIK/out.txt ')


def terminate_ec2_instance(ids):
    ec2.instances.filter(InstanceIds=ids).terminate()
    if args.v:
        print("ec2 instance terminated")


if __name__ == '__main__':
    if args.v:
        print("verbosity turned on")
    print("program has started")

    create_myec2_instance()  # function that creates ec2 instance

    # I added these 12 lines not in create_myec2_instance but here to make transfer_files function recognize the public dns of ec2
    ids = []
    while 1:
        time.sleep(20)
        running = 0
        instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        for instance in instances:
            PUB_DNS = instance.public_dns_name  # PUB_DNS stores the public dns of ec2 instance
            if args.v:
                print("RUNNING INSTANCE: id: %s, type: %s, publicIP: %s, publicDns: %s " % (
                instance.id, instance.instance_type, instance.public_ip_address, instance.public_dns_name))
            ids.append(instance.id)
            running = 1
        if running:
            break

    # the function that establish ssh connection between ec2 and my machine and then transfer files
    transfer_files()

    # the function that will bring back files that run in ec2 instance to ~/Downloads/2016400372BALIK folder
    bring_back_files()

    # the function that will terminate the ec2 instance
    terminate_ec2_instance(ids)


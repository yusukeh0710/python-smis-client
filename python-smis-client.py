#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import pywbem
import sys

def opt_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', type=str, 
                        default=None, help='login user name')
    parser.add_argument('-p', '--password', type=str, 
                        default=None, help='login password')
    parser.add_argument('-l', '--location', type=str, 
                        default=None, help='server IP address + : + port no')
    parser.add_argument('-n', '--namespace',type=str, 
                        default=None, help='namespace')
    subparsers = parser.add_subparsers(help='CIM Operation', dest='operation')

    # Get Instance
    gi_parser = subparsers.add_parser('gi', help='Get Instance')
    gi_parser.add_argument('instancename', help='CIM Instance Path')

    # Enumerate Instances
    ei_parser = subparsers.add_parser('ei', help='Enumerate Instances')
    ei_parser.add_argument('classname', help='CIM Class Name')

    # Enumerate Instance Names
    en_parser = subparsers.add_parser('en', help='Enumerate Instance Names')
    en_parser.add_argument('classname', help='CIM Class Name')

    # generate option list
    args = parser.parse_args()

    if ((args.user is None) or (args.password is None)
        or (args.location is None) or (args.namespace is None)):
        parser.print_help()

    return args.__dict__

def create_smis_connection(user, password, location, namespace):
    url = 'http://' + location
    creds = (user, password)
    conn = pywbem.WBEMConnection(url, creds, default_namespace=namespace)
    return conn

def create_output_from_instancename_object(instancename_obj):
    classname = instancename_obj.classname
    keys = instancename_obj.keys()
    values = instancename_obj.values()
    keybindings = {keys[i] : values[i] for i in range(min(len(keys), len(values)))}
    namespace = instancename_obj.nammespace
    
    output = {'classname' : classname,
              'keybindings' : keybindings,
              'namespace' : namespace}

    return str(output).replace(' ','')

def create_instancename_object_from_input(input_string):
    instancename_dict = eval(input_string)
    try:
        instancename = pywbem.CIMInstanceName(
                            instancename_dict['classname'],
                            namespace=instancename_dict['namespace'],
                            keybindings=instancename_dict['keybindings']
                        )
    except NameError as ex:
        print ex
        sys.exit(1)

    return instancename

def GetInstance(conn, **params):
    instancename_string = params.pop('instancename')
    instancename = create_instancename_object_from_input(instancename_string)

    try:
        result = conn.GetInstance(
                    instancename,
                    **params)
        for key, value in result.iteritems():
            print "%s : %s" % (key, value.value)
    except Exception as ex:
        print ex

def EnumerateInstances(conn, **params):
    classname = params.pop('classname')

    try:
        results = conn.EnumerateInstances(
                     classname,
                     **params)
        for result in results:
            print result
    except Exception as ex:
        print ex

def EnumerateInstanceNames(conn, **params):
    classname = params.pop('classname')

    try:
        results = conn.EnumerateInstanceNames(
                     classname,
                     **params)
        for result in results:
            print create_output_from_instancename_object(result)
    except Exception as ex:
        print ex

if __name__ == '__main__':
    # get arguments 
    args = opt_parse()
    user=args.pop('user')
    password=args.pop('password')
    location=args.pop('location')
    namespace=args.pop('namespace')
    operation=args.pop('operation')

    # create SMI-S connectionn
    conn = create_smis_connection(user, password, location, namespace)

    # execute SMI-S operation
    if operation == 'gi':
        GetInstance(conn, **args)
    elif operation == 'ei':
        EnumerateInstances(conn, **args)
    elif operation == 'en':
        EnumerateInstanceNames(conn, **args)

    sys.exit(0)

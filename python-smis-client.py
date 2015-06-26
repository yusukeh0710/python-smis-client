#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' python SMI-S client tool'''
import argparse
import pywbem
import sys

def opt_parse():
    ''' parser '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', type=str,
                        default=None, help='login user name')
    parser.add_argument('-p', '--password', type=str,
                        default=None, help='login password')
    parser.add_argument('-l', '--location', type=str,
                        default=None, help='server IP address + : + port no')
    parser.add_argument('-n', '--namespace', type=str,
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

    # Enumerate Associators
    a_parser = subparsers.add_parser('a', help='Enumerate Associators')
    a_parser.add_argument('instancename', help='CIM Instance Name')
    a_parser.add_argument('-ac', help='Associator Class')
    a_parser.add_argument('-rc', help='Result Class')

    # Enumerate Associator Names
    an_parser = subparsers.add_parser('an', help='Enumerate Associator Names')
    an_parser.add_argument('instancename', help='CIM Instance Name')
    an_parser.add_argument('-ac', help='Associator Class')
    an_parser.add_argument('-rc', help='Result Class')

    # Enumerate References
    r_parser = subparsers.add_parser('r', help='Enumerate References')
    r_parser.add_argument('instancename', help='CIM Instance Name')
    r_parser.add_argument('-rc', help='Result Class')

    # Enumerate Reference Names
    rn_parser = subparsers.add_parser('rn', help='Enumerate Reference Names')
    rn_parser.add_argument('instancename', help='CIM Instance Name')
    rn_parser.add_argument('-rc', help='Result Class')

    # generate option list
    args = parser.parse_args()

    if ((args.user is None) or (args.password is None)
            or (args.location is None) or (args.namespace is None)):
        parser.print_help()

    return args.__dict__

def create_smis_connection(user, password, location, namespace):
    ''' create instance for connecting target'''
    url = 'http://' + location
    creds = (user, password)
    conn = pywbem.WBEMConnection(url, creds, default_namespace=namespace)
    return conn

def print_instancename(instancename_obj):
    ''' print instance name '''
    classname = instancename_obj.classname
    keys = instancename_obj.keys()
    values = instancename_obj.values()
    keybindings = {keys[i] : values[i].replace(' ', '&nbsp;') \
                        for i in range(min(len(keys), len(values)))}
    namespace = instancename_obj.namespace

    output = {'classname' : classname,
              'keybindings' : keybindings,
              'namespace' : namespace}

    print str(output).replace(' ', '')
    return

def print_instance(instance_obj):
    ''' print instance information '''
    print "path: %s\n" % instance_obj.path
    for key, value in instance_obj.iteritems():
        print "%s : %s" % (key, value)
    print "\n"
    return

def create_instancename(input_string):
    ''' create instance from string '''
    instancename_dict = eval(input_string.replace('&nbsp;', ' '))
    try:
        instancename = pywbem.CIMInstanceName(
            instancename_dict['classname'],
            namespace=instancename_dict['namespace'],
            keybindings=instancename_dict['keybindings'])
    except NameError as ex:
        print ex
        sys.exit(1)

    return instancename

def GetInstance(conn, **kwarg):
    ''' Get Instance '''
    instancename_string = kwarg.pop('instancename')
    instancename = create_instancename(instancename_string)
    params = kwarg

    try:
        result = conn.GetInstance(
            instancename,
            **params)
        print_instance(result)
    except Exception as ex:
        print ex

def EnumerateInstances(conn, **kwarg):
    ''' Enumerate Instances '''
    classname = kwarg.pop('classname')
    params = kwarg

    try:
        results = conn.EnumerateInstances(
            classname,
            **params)
        for result in results:
            print_instance(result)
    except Exception as ex:
        print ex

def EnumerateInstanceNames(conn, **kwarg):
    ''' Enumerate Instance Names '''
    classname = kwarg.pop('classname')
    params = kwarg

    try:
        results = conn.EnumerateInstanceNames(
            classname,
            **params)
        for result in results:
            print_instancename(result)
    except Exception as ex:
        print ex

def Associators(conn, **kwarg):
    ''' Enumerate Associatos '''
    instancename_string = kwarg.pop('instancename')
    instancename = create_instancename(instancename_string)

    ac = kwarg.pop('ac')
    rc = kwarg.pop('rc')
    params = kwarg

    if ac is not None:
        params['AssocClass'] = ac

    if rc is not None:
        params['ResultClass'] = rc

    try:
        results = conn.Associators(
            instancename,
            **params)
        for result in results:
            print_instance(result)
    except Exception as ex:
        print ex

def AssociatorNames(conn, **kwarg):
    ''' Enumerate Associato Names '''
    instancename_string = kwarg.pop('instancename')
    instancename = create_instancename(instancename_string)

    ac = kwarg.pop('ac')
    rc = kwarg.pop('rc')
    params = kwarg

    if ac is not None:
        params['AssocClass'] = ac

    if rc is not None:
        params['ResultClass'] = rc

    try:
        results = conn.AssociatorNames(
            instancename,
            **params)
        for result in results:
            print_instancename(result)
    except Exception as ex:
        print ex

def References(conn, **kwarg):
    ''' Enumerate References '''
    instancename_string = kwarg.pop('instancename')
    instancename = create_instancename(instancename_string)

    rc = kwarg.pop('rc')
    params = kwarg

    if rc is not None:
        params['ResultClass'] = rc

    try:
        results = conn.References(
            instancename,
            **params)
        for result in results:
            print_instance(result)
    except Exception as ex:
        print ex

def ReferenceNames(conn, **kwarg):
    ''' Enumerate Reference Names '''
    instancename_string = kwarg.pop('instancename')
    instancename = create_instancename(instancename_string)

    rc = kwarg.pop('rc')
    params = kwarg

    if rc is not None:
        params['ResultClass'] = rc

    try:
        results = conn.ReferenceNames(
            instancename,
            **params)
        for result in results:
            print_instancename(result)
    except Exception as ex:
        print ex


if __name__ == '__main__':
    # get arguments
    args = opt_parse()
    user = args.pop('user')
    password = args.pop('password')
    location = args.pop('location')
    namespace = args.pop('namespace')
    operation = args.pop('operation')

    # create SMI-S connectionn
    conn = create_smis_connection(user, password, location, namespace)

    # execute SMI-S operation
    if operation == 'gi':
        GetInstance(conn, **args)
    elif operation == 'ei':
        EnumerateInstances(conn, **args)
    elif operation == 'en':
        EnumerateInstanceNames(conn, **args)
    elif operation == 'a':
        Associators(conn, **args)
    elif operation == 'an':
        AssociatorNames(conn, **args)
    elif operation == 'r':
        References(conn, **args)
    elif operation == 'rn':
        ReferenceNames(conn, **args)

    sys.exit(0)

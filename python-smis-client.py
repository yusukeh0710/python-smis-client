#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' python SMI-S client tool'''
import argparse
import pywbem
import sys


ESC_SPACE = "nbsp;"

###################################
# Common Functions
###################################


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

    # InvokeMethod
    im_parser = subparsers.add_parser('im', help='InvokeMethod')
    im_parser.add_argument('instancename', help='CIM Instance Name')
    im_parser.add_argument('methodname', help='Method Name')
    im_parser.add_argument('parameters', nargs='*', help='Parameters')

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
    keybindings = {keys[i]: values[i].replace(' ', ESC_SPACE)
                   for i in range(min(len(keys), len(values)))}
    namespace = instancename_obj.namespace

    output = {'classname': classname,
              'keybindings': keybindings,
              'namespace': namespace}

    print str(output).replace(' ', '')
    return


def print_instance(instance_obj):
    ''' print instance information '''
    print "path: %s\n" % instance_obj.path
    for key, value in instance_obj.iteritems():
        print "%s : %s" % (key, value)
    print "\n"
    return


def create_instancename(string):
    ''' create CIMinstanceName from string '''
    instancename_info = eval(string.replace(ESC_SPACE, ' '))
    try:
        instancename = pywbem.CIMInstanceName(
            instancename_info['classname'],
            namespace=instancename_info['namespace'],
            keybindings=instancename_info['keybindings'])
    except NameError as ex:
        print ex
        sys.exit(1)

    return instancename


def create_parameter(string_list):
    ''' create parameter dictionary from string list'''
    parameter = {}
    for string in string_list:
        key, value = string.split('=', 1)
        if isinstance(value, int):
            parameter[key] = pywbem.Uint16(value)
        elif (value[0] == '{') and (value[-1] == '}'):
            parameter[key] = create_instancename(value)
        else:
            parameter[key] = value

    return parameter


###################################
# Operations
###################################


def GetInstance(conn, **kwargs):
    ''' Get Instance '''
    instancename = create_instancename(kwargs['instancename'])

    try:
        result = conn.GetInstance(
            instancename)
        print_instance(result)
    except Exception as ex:
        print ex


def EnumerateInstances(conn, **kwargs):
    ''' Enumerate Instances '''
    classname = kwargs['classname']

    try:
        results = conn.EnumerateInstances(
            classname)
        for result in results:
            print_instance(result)
    except Exception as ex:
        print ex


def EnumerateInstanceNames(conn, **kwargs):
    ''' Enumerate Instance Names '''
    classname = kwargs['classname']

    try:
        results = conn.EnumerateInstanceNames(
            classname)
        for result in results:
            print_instancename(result)
    except Exception as ex:
        print ex


def Associators(conn, **kwargs):
    ''' Enumerate Associatos '''
    instancename = create_instancename(kwargs['instancename'])
    params = {}

    ac = kwargs['ac']
    rc = kwargs['rc']

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


def AssociatorNames(conn, **kwargs):
    ''' Enumerate Associato Names '''
    instancename = create_instancename(kwargs['instancename'])
    params = {}

    ac = kwargs['ac']
    rc = kwargs['rc']

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


def References(conn, **kwargs):
    ''' Enumerate References '''
    instancename = create_instancename(kwargs['instancename'])
    params = {}

    rc = kwargs['rc']
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


def ReferenceNames(conn, **kwargs):
    ''' Enumerate Reference Names '''
    instancename = create_instancename(kwargs['instancename'])
    params = {}

    rc = kwargs['rc']
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


def InvokeMethod(conn, **kwargs):
    ''' InvokeMethod '''
    instancename = create_instancename(kwargs['instancename'])
    methodname = kwargs['methodname']
    parameters = create_parameter(kwargs['parameters'])
    print "this is experiment source code, and exit 1"
    sys.exit(1)


###################################
# Main
###################################


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
    elif operation == 'im':
        InvokeMethod(conn, **args)

    sys.exit(0)

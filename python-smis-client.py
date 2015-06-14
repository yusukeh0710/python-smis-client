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

    # Enumerate Instance Names
    ei_parser = subparsers.add_parser('en', help='Enumerate Instance Names')
    ei_parser.add_argument('classname', help='CIM Class Name')

    # generate option list
    args = parser.parse_args()

    if ((args.user is None) or (args.password is None)
        or (args.location is None) or (args.namespace is None)):
        parser.print_help()

    return args.__dict__

def create_smis_connection(user, password, location, namespace):
    url = 'http;//' + location
    creds = (user, password)
    conn = pywbem.WBEMConnection(url, creds, default_namespace=namespace)
    return conn

def EnumerateInstanceNames(conn, **params):
    classname = args.pop('classname')

    try:
        result = conn.EnumerateInstanceNames(
                    classname,
                    namespace=None,
                    **params)
        print result
    except:
        print "error"

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
    if operation == 'en':
        EnumerateInstanceNames(conn, **args)

    sys.exit(0)

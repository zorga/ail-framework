#!/usr/bin/env python3
# -*-coding:UTF-8 -*

import os
import sys
import json
import argparse

sys.path.append(os.path.join(os.environ['AIL_BIN'], 'packages/'))
import Cryptocurrency

sys.path.append(os.path.join(os.environ['AIL_BIN'], 'lib/'))
import ConfigLoader
import Correlate_object

mode = 'union'

def sanitise_int(page, default_value):
    try:
        page = int(page)
    except:
        page = default_value
    if page < 1:
        page = default_value
    return page

def sanitise_nb_max_nodes(nb_max_nodes):
    try:
        nb_max_nodes = int(nb_max_nodes)
        if nb_max_nodes < 2:
            nb_max_nodes = 300
    except:
        nb_max_nodes = 300
    return nb_max_nodes

def get_object_correlation_json(correlation_id, subtype, max_nodes):
    max_nodes = sanitise_nb_max_nodes(max_nodes)

    object_type = 'cryptocurrency'
    max_nodes = sanitise_nb_max_nodes(max_nodes)

    # ALL correlations
    correlation_names = Correlate_object.sanitise_correlation_names('')
    correlation_objects = Correlate_object.sanitise_correlation_objects('')

    res = Correlate_object.get_graph_node_object_correlation(object_type, correlation_id, mode, correlation_names,
                                                    correlation_objects, requested_correl_type=subtype,
                                                    max_nodes=max_nodes, flask_context=False)
    return res

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Trigger backgroud update')
    parser.add_argument('-t', '--type', help='Cryptocurrency type (bitcoin, bitcoin-cash, etherum, litecoin, monero, dash, zcash)', type=str, dest='type', required=True, default=None)
    parser.add_argument('-p', '--page',help='page number' , type=int, default=1, dest='page')
    parser.add_argument('-n', '--nb',help='number of addresses by page' , type=int, default=50, dest='nb_elem')
    parser.add_argument('--node' ,help='correlation graph: max number of nodes' , type=int, default=50, dest='max_nodes')
    args = parser.parse_args()

    subtype = args.type
    if subtype is None:
        parser.print_help()
        sys.exit(0)

    page = sanitise_int(args.page, 1)
    nb_elem = sanitise_int(args.nb_elem, 50)
    max_nodes = sanitise_int(args.max_nodes, 300)

    dict_json = {}
    for address in Cryptocurrency.cryptocurrency.get_all_correlations_by_subtype_pagination(subtype, nb_elem=nb_elem, page=page):
        dict_json[address] = get_object_correlation_json(address, subtype, max_nodes)

    print(json.dumps(dict_json))

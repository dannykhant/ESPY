#!/usr/bin/python
#Simple API client for Elasticsearch
#Author: Phyo Min Khant

from elasticsearch import Elasticsearch, helpers
import csv
import argparse
import configparser

config = configparser.ConfigParser()
config.read("espy.ini")
espy = dict(config.items('espy'))

es = Elasticsearch(espy['url'], http_auth=(espy['username'], espy['password']))

def show_info():
    """ Get info about elasticsearch. """
    info = es.info()
    print('UUID: {}\nName: {}\nCluster: {}\nVersion: {}'.format(
							info['cluster_uuid'],
							info['name'],
							info['cluster_name'],
							info['version']['number']))


def show_indices(all_ = None):
    """ Show all indices. """
    for index in es.indices.get_alias('*'):
        if all_:
            print(index)
        elif not '.' in index:
            print(index)
    print()


def create_index(body, *args):
    """ Create index & ingest data. """
    if not es.indices.exists(index):
        return helpers.bulk(es, body, index = index, doc_type = type_)
    else:
        return "existed"


def delete_index(index):
    """ Delete unwanted index. """
    return es.indices.delete(index = index, ignore = [404, 400])


def get_source(index, type_):
    """ Get _source of an index. """
    if es.indices.exists(index):
        res = helpers.scan(es, index = index, doc_type = type_)
        return res


def cat_indices():
    """ Get cross section of each index. """
    return es.cat.indices('*')


def action_csv(csv_file):
    """ Get CSV data. """
    with open(csv_file) as file_:
        reader = csv.DictReader(file_)
        msg = create_index(reader, index, type_)

        if msg == 'existed':
            return "Index is existed."
        return msg


parser = argparse.ArgumentParser(description='API client for Elasticsearch')
parser.add_argument('--info', help = 'elasticsearch info', action = 'store_true')
parser.add_argument('--create', help = 'create index', action = 'store_true')
parser.add_argument('--delete', help = 'delete index', action = 'store_true')
parser.add_argument('--show_indices', help = 'show all indices', action = 'store_true')
parser.add_argument('--cat_indices', help = 'cat all indices', action = 'store_true')
parser.add_argument('--get_source', help = 'get _source of an index', action = 'store_true')
parser.add_argument('--all', help = 'all indices including .sys', action = 'store_true')
parser.add_argument('--index', help = 'index name')
parser.add_argument('--type', help = 'type/mapping name')
parser.add_argument('--csv_file', help = 'csv file path')
args = parser.parse_args()

index = args.index
type_ = args.type

if args.info:
	show_info()

elif args.create:
    if index and type_ and args.csv_file:
        print(action_csv(args.csv_file))
    else:
        print("Require --index or --type or --csv_file or all parameters")

elif args.delete:
    if index:
        print(delete_index(index))

elif args.show_indices:
    if args.all:
        show_indices(True)
    else:
        show_indices()

elif args.get_source:
    if index and type_:
        for doc in get_source(index, type_):
            print(doc['_source'])
    else:
        print("Require --index or --type or both")

elif args.cat_indices:
    print(cat_indices())

else:
    parser.print_help()



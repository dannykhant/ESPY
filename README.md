###ESPY: Simple API client for Elasticsearch

##Usage

usage: espy.py [-h] [--info] [--create] [--delete] [--show_indices]
               [--cat_indices] [--get_source] [--all] [--index INDEX]
               [--type TYPE] [--csv_file CSV_FILE]

optional arguments:
  -h, --help           show this help message and exit
  --info               elasticsearch info
  --create             create index
  --delete             delete index
  --show_indices       show all indices
  --cat_indices        cat all indices
  --get_source         get _source of an index
  --all                all indices including .sys
  --index INDEX        index name
  --type TYPE          type/mapping name
  --csv__file CSV_FILE  csv file path

##Example

#show all indices of elasticsearch
python espy.py --show_indices

#cat all indices health
python espy.py --cat_indices

#get source of an index 
python espy.py --get_source --index INDEX --type MAPPING

#Create an index from a csv file
python espy.py --create --index INDEX --type MAPPING --csv_file /root/file.csv

#Delete index
python espy.py --delete --index INDEX

##Configure Elasticsearch information in config file
#espy.ini

[espy]
url = http://elastic_-url:9200
username = elastic
password = changeme



# Python Elasticsearch Learning to Rank client

This is an add-on to [official Python Elasticsearch client](https://github.com/elastic/elasticsearch-py) adding support 
for [Elasticsearch Learning to Rank](https://github.com/o19s/elasticsearch-learning-to-rank) plugin API.

## Installation

    python -m pip install elasticsearch_ltr

## Usage

    from elasticsearch import Elasticsearch
    from elasticsearch_ltr import LTRClient
    
    client = Elasticsearch()
    LTRClient.infect_client(client)
    
    client.ltr.create_feature_store()
    ...

For more code you may check out `tests/` folder.


## Running tests

You'll have to run Elasticsearch on `localhost:9200` with LTR plugin installed. Then just do

    python -m pytest tests/

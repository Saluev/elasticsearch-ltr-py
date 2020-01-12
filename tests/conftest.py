from elasticsearch import Elasticsearch
import pytest

from elasticsearch_ltr import LTRClient


@pytest.fixture
def client() -> Elasticsearch:
    client = Elasticsearch()
    LTRClient.infect_client(client)
    return client


@pytest.fixture
def ltr(client: Elasticsearch) -> LTRClient:
    ltr: LTRClient = client.ltr

    stores = ltr.list_feature_stores()["stores"]
    if stores:
        raise RuntimeError("test environment has feature stores! not proceeding further, remove them manually")

    yield ltr

    # Cleaning up.
    stores = ltr.list_feature_stores()["stores"]
    for key in stores:
        if key == "_default_":
            ltr.delete_feature_store()
        else:
            ltr.delete_feature_store(key)

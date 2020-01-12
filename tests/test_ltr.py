from typing import Optional

from elasticsearch.exceptions import ElasticsearchException, NotFoundError
import pytest

from elasticsearch_ltr import LTRClient


def test_feature_store_crud(ltr: LTRClient):
    # Can't delete non-existing stores.
    with pytest.raises(NotFoundError):
        ltr.delete_feature_store()

    with pytest.raises(NotFoundError):
        ltr.delete_feature_store("yet_not_existing_feature_store")

    response = ltr.list_feature_stores()
    assert len(response["stores"]) == 0

    # Can create store.
    ltr.create_feature_store()
    ltr.create_feature_store("foo")
    ltr.create_feature_store("foo_bar")

    # Can't create store with same name.
    with pytest.raises(ElasticsearchException):
        ltr.create_feature_store()

    with pytest.raises(ElasticsearchException):
        ltr.create_feature_store("foo")

    # Can list stores.
    response = ltr.list_feature_stores()
    assert len(response["stores"]) == 3

    # Can delete existing store.
    ltr.delete_feature_store()
    assert set(ltr.list_feature_stores()["stores"].keys()) == {"foo", "foo_bar"}

    ltr.delete_feature_store("foo")
    assert set(ltr.list_feature_stores()["stores"].keys()) == {"foo_bar"}

    # Can create deleted store again.
    ltr.create_feature_store()


@pytest.mark.parametrize("store_name", [None, "fs"])
def test_feature_set_crud(ltr: LTRClient, store_name: Optional[str]):
    ltr.create_feature_store(store_name)

    # Can't get non-existing feature set.
    with pytest.raises(NotFoundError):
        ltr.get_feature_set("yet_not_existing_feature_set", store_name=store_name)

    # Can't delete non-existing feature set.
    with pytest.raises(NotFoundError):
        ltr.delete_feature_set("yet_not_existing_feature_set", store_name=store_name)

    # Can create feature set.
    ltr.create_feature_set("foo", {"featureset": {"features": []}}, store_name=store_name)
    ltr.create_feature_set("foo_bar", {"featureset": {"features": []}}, store_name=store_name)

    # Can get existing feature set.
    response = ltr.get_feature_set("foo", store_name=store_name)
    assert response["_source"]["name"] == "foo"

    # Can list feature sets.
    response = ltr.list_feature_sets(store_name=store_name)
    assert response["hits"]["total"] == {"relation": "eq", "value": 2}

    # Can list feature sets with prefix.
    response = ltr.list_feature_sets(prefix="foo", store_name=store_name)
    assert response["hits"]["total"] == {"relation": "eq", "value": 2}

    response = ltr.list_feature_sets(prefix="foo_", store_name=store_name)
    assert response["hits"]["total"] == {"relation": "eq", "value": 1}

    # Can delete existing feature set.
    ltr.delete_feature_set("foo", store_name=store_name)

    # Can't get deleted feature set.
    with pytest.raises(NotFoundError):
        ltr.get_feature_set("foo", store_name=store_name)

    # Can create deleted feature set again.
    ltr.create_feature_set("foo", {"featureset": {"features": []}}, store_name=store_name)


def test_model_crud(ltr: LTRClient):
    ltr.create_feature_store()
    ltr.create_feature_set("foo", {"featureset": {"features": [
        create_field_feature("ctr", "ctr"),
        create_field_feature("btr", "btr")
    ]}})

    # Can't get non-existing model.
    with pytest.raises(NotFoundError):
        ltr.get_model("yet_not_existing_model")

    # Can't delete non-existing model.
    with pytest.raises(NotFoundError):
        ltr.delete_model("yet_not_existing_model")

    # Can create model.
    ltr.create_model("linear_v1", create_linear_model("linear_v1", 0.3, 0.7), "foo")
    ltr.create_model("linear_v2", create_linear_model("linear_v2", 0.4, 0.6), "foo")

    # Can get existing model.
    response = ltr.get_model("linear_v1")
    assert response["_source"]["name"] == "linear_v1"

    # Can list models.
    response = ltr.list_models()
    assert response["hits"]["total"] == {"relation": "eq", "value": 2}

    # Can list models with prefix.
    response = ltr.list_models(prefix="linear")
    assert response["hits"]["total"] == {"relation": "eq", "value": 2}

    response = ltr.list_models(prefix="linear_v2")
    assert response["hits"]["total"] == {"relation": "eq", "value": 1}

    # Can delete existing model.
    ltr.delete_model("linear_v1")

    # Can't get deleted model.
    with pytest.raises(NotFoundError):
        ltr.get_model("linear_v1")

    # Can create deleted model again.
    ltr.create_model("linear_v1", create_linear_model("linear_v1", 0.3, 0.7), "foo")


def test_feature_crud(ltr: LTRClient):
    ltr.create_feature_store()

    # Can't get non-existing feature.
    with pytest.raises(NotFoundError):
        ltr.get_feature("ctr")

    # Can't delete non-existing feature.
    with pytest.raises(NotFoundError):
        ltr.delete_feature("ctr")

    # Can create feature.
    ltr.create_feature("ctr", {"feature": create_field_feature("ctr", "ctr_field")})
    ltr.create_feature("btr", {"feature": create_field_feature("btr", "btr_field")})

    # Can get existing feature.
    response = ltr.get_feature("ctr")
    assert response["_source"]["name"] == "ctr"

    # Can list features.
    response = ltr.list_features()
    assert response["hits"]["total"] == {"relation": "eq", "value": 2}

    # Can list features with prefix.
    response = ltr.list_features(prefix="c")
    assert response["hits"]["total"] == {"relation": "eq", "value": 1}

    # Can delete existing feature.
    ltr.delete_feature("ctr")

    # Can't get deleted feature.
    with pytest.raises(NotFoundError):
        ltr.get_feature("ctr")

    # Can create deleted feature again.
    ltr.create_feature("ctr", {"feature": create_field_feature("ctr", "ctr_field")})


def test_adding_features_to_feature_set(ltr: LTRClient):
    ltr.create_feature_store()
    ltr.create_feature_set("foo", {"featureset": {"features": [
        create_field_feature("feature0", "ctr"),
        create_field_feature("feature1", "btr"),
    ]}})

    response = ltr.get_feature_set("foo")
    assert len(response["_source"]["featureset"]["features"]) == 2

    ltr.add_features_to_feature_set("foo", {"features": [
        create_field_feature("feature2", "wctr"),
    ]})

    response = ltr.get_feature_set("foo")
    assert len(response["_source"]["featureset"]["features"]) == 3

    ltr.create_feature("wbtr", {"feature": create_field_feature("wbtr", "wbtr")})
    ltr.add_feature_to_feature_set("foo", "wbtr")

    response = ltr.get_feature_set("foo")
    assert len(response["_source"]["featureset"]["features"]) == 4


def create_field_feature(name, field_name):
    return {
        "name": name,
        "params": [],
        "template_language": "mustache",
        "template": {
            "function_score": {
                "functions": {
                    "field": field_name
                },
                "query": {
                    "match_all": {}
                }
            }
        }
    }


def create_linear_model(name, ctr_weight, btr_weight):
    return {
        "model": {
            "name": name,
            "model": {
                "type": "model/linear",
                "definition": f"""
                    {{
                        "btr": {btr_weight},
                        "ctr": {ctr_weight}
                    }}
                """
            }
        }
    }

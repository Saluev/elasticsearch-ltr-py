from typing import Optional, Any

from elasticsearch.client.utils import AddonClient, query_params, _make_path


class LTRClient(AddonClient):
    """
    Add-on for Learning to Rank plugin API.
    `<https://elasticsearch-learning-to-rank.readthedocs.io/>`_
    """

    namespace = "ltr"

    @query_params()
    def create_feature_store(self, name: Optional[str] = None, params=None):
        self.transport.perform_request("PUT", _make_path("_ltr", name), params=params)

    @query_params()
    def delete_feature_store(self, name: Optional[str] = None, params=None):
        self.transport.perform_request("DELETE", _make_path("_ltr", name), params=params)

    @query_params()
    def list_feature_stores(self, params=None):
        return self.transport.perform_request("GET", _make_path("_ltr"), params=params)

    @query_params()
    def create_feature_set(self, name: str, body: Any, store_name: Optional[str] = None, params=None):
        self.transport.perform_request(
            "POST", _make_path("_ltr", store_name, "_featureset", name), body=body, params=params)

    @query_params()
    def delete_feature_set(self, name: str, store_name: Optional[str] = None, params=None):
        self.transport.perform_request(
            "DELETE", _make_path("_ltr", store_name, "_featureset", name), params=params)

    @query_params()
    def get_feature_set(self, name: str, store_name: Optional[str] = None, params=None):
        return self.transport.perform_request(
            "GET", _make_path("_ltr", store_name, "_featureset", name), params=params)

    @query_params("prefix")
    def list_feature_sets(self, store_name: Optional[str] = None, params=None):
        return self.transport.perform_request(
            "GET", _make_path("_ltr", store_name, "_featureset"), params=params)

    @query_params()
    def add_features_to_feature_set(self, name: str, body: Any, store_name: Optional[str] = None, params=None):
        self.transport.perform_request(
            "POST", _make_path("_ltr", store_name, "_featureset", name, "_addfeatures"), body=body, params=params)

    @query_params()
    def add_feature_to_feature_set(self, name: str, feature_name: str, store_name: Optional[str] = None, params=None):
        self.transport.perform_request(
            "POST", _make_path("_ltr", store_name, "_featureset", name, "_addfeatures", feature_name), params=params)

    @query_params()
    def create_model(self, name: str, body: Any, feature_set_name: str, store_name: Optional[str] = None, params=None):
        print(body)
        self.transport.perform_request(
            "POST", _make_path("_ltr", store_name, "_featureset", feature_set_name, "_createmodel"), body=body, params=params)

    @query_params()
    def delete_model(self, name: str, store_name: Optional[str] = None, params=None):
        self.transport.perform_request(
            "DELETE", _make_path("_ltr", store_name, "_model", name), params=params)

    @query_params()
    def get_model(self, name: str, store_name: Optional[str] = None, params=None):
        return self.transport.perform_request(
            "GET", _make_path("_ltr", store_name, "_model", name), params=params)

    @query_params("prefix")
    def list_models(self, store_name: Optional[str] = None, params=None):
        return self.transport.perform_request(
            "GET", _make_path("_ltr", store_name, "_model"), params=params)

    @query_params()
    def create_feature(self, name: str, body: Any, store_name: Optional[str] = None, params=None):
        self.transport.perform_request(
            "POST", _make_path("_ltr", store_name, "_feature", name), body=body, params=params)

    @query_params()
    def delete_feature(self, name: str, store_name: Optional[str] = None, params=None):
        self.transport.perform_request(
            "DELETE", _make_path("_ltr", store_name, "_feature", name), params=params)

    @query_params()
    def get_feature(self, name: str, store_name: Optional[str] = None, params=None):
        return self.transport.perform_request(
            "GET", _make_path("_ltr", store_name, "_feature", name), params=params)

    @query_params("prefix")
    def list_features(self, store_name: Optional[str] = None, params=None):
        return self.transport.perform_request("GET", _make_path("_ltr", store_name, "_feature"), params=params)

    @query_params()
    def clear_cache(self, store_name: Optional[str] = None, params=None):
        self.transport.perform_request("POST", _make_path("_ltr", store_name, "_clearcache"), params=params)

    @query_params()
    def get_cache_stats(self, store_name: Optional[str] = None, params=None):
        return self.transport.perform_request("GET", _make_path("_ltr", store_name, "_cachestats"), params=params)

def previous_bookmarks():
    es = elasticsearch.Elasticsearch()
    res = es.search(index='list_bookmarks',doc_type="bookmarks",body={"filter":{"term":{'_type':'bookmarks'}}})
    for i in res['hits']['hits']:
        print i["_source"]
          
from flask import Flask, request, Blueprint
from flask_restplus import Resource, Api
from elasticsearch import Elasticsearch

ES_INDEX = "tweets"
ES_DOC_TYPE = "tweet"
es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])

app = Flask(__name__)
api = Api(app,
          title='FLASK RESTPLUS API',
          version='1.0',
          description='API to return Twitter data from ElasticSearch'
         )

@api.route("/api/v1/users")
class UserController(Resource):
     def get(self):
        """List users with more followers"""
        default_from = 0
        default_size = 5

        fields = request \
            .args \
            .get("fields") \
            .split(",")
        
        sort = request.args.get("sort")
        order = request.args.get("order")

        body = {
            "_source": fields,
            "sort":  [
                { sort : { "order": order } }
            ],
            "from": default_from,
            "size": default_size
        }

        result = es.search(
            index = ES_INDEX,
            doc_type = ES_DOC_TYPE,
            body = body,
            filter_path=["hits.hits._source"]
        )

        return result['hits']['hits']

@api.route("/api/v1/tweets")
class TweetController(Resource):
     def get(self):
        """Get tweets agregatte by hour."""
        agg = request.args.get("agg")
        if agg == "hourly":
            body = {
                "aggs": {
                    "result": {
                        "date_histogram": {
                            "field": "timestamp",
                            "interval": "hour",
                            "format": "yyyy-MM-dd HH:mm:ss"
                        }
                    }
                }
            }
        elif agg == "lang":
            body = {
                "aggs": {
                    "result": {
                        "terms": {
                            "field": "lang.keyword"
                        },
                        "aggs": {
                            "hashtags": {
                                "terms": {
                                    "field": "hashtags.keyword"
                                }
                            }
                        }
                    }
                }
            }

        else: 
            body = {

            }

        result = es.search(
            index = ES_INDEX,
            doc_type = ES_DOC_TYPE,
            body = body,
            filter_path=["aggregations.result.buckets"]
        )
        
        return result['aggregations']['result']['buckets']

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
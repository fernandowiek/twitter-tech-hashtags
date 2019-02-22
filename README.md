# twitter-tech-hashtags

**About this repo**

A personal project to learn more about Python, Elastic stack and API's in general.

**Construction**

Using twitter API, the goal is capture data from some tech hashtags, save it on a database and access this data throught an API.
To do this, was used these technologies:

 - Docker and Docker Compose to build the enviroment
 - Python to connect to Twitter Stream API
 - ElasticSearch to save the data captured from Twitter
 - Flask API to access some data on ElasticSearch
 - Swagger to API documentation 
 - Kibana to visualize the data captured

**How to run**

 - Install Docker according your OS: https://docs.docker.com/install/
 - Install Docker Compose: https://docs.docker.com/compose/install/
 - Create an APP on your Twitter account: https://help.xyzscripts.com/docs/social-media-auto-publish/faq/how-can-i-create-twitter-application/
 - Edit the file app/twitter_credentials.json with your credentials 
 - On your terminal, type: `docker-compose up --build`
 - Access Kibana and configure the index "tweets*"
 - Go to Kibana configurations and upload visaualizations and one dashboad available on Kibana folder 

**Endpoints**

 - API: http://localhost:5000 
 - ElasticSearch: http://localhost:9200
 - Kibana: http://localhost:5601
# Load tests for Theatron
You can run load tests without UI using:`python .`, - to start tests in command line. <br />
Available flags:<br/>
`--num_users`, -default 50<br/>
`--spawn_rate`, -default 10<br/>
`--run_time`, - string, default "1m"<br/>
You can also run UI tests using the construct: `locust -f load_scenario/create_posts.py` - from the root directory,<br /> then go to localhost:8089 to configure and start load tests.

#### emulated requests:
    get_post_list - send request to GET user's posts
    get_detail_post - send request to GET 1 random detail user's post
    create_post - send request to POST (create) post
    
#### required environment variables:
    BASE_URL="http://localhost:8000/api/v1/"
    CREDENTIALS_FILEPATH="test_users/users.csv" - file with credentials information, without it util will crash
    ACCESS_CODE=11111
    
#### optional environment variables:
    RUN_TIME=1m
    SPAWN_RATE=10
    NUM_USERS=50
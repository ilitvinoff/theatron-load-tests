import logging
import random
from copy import deepcopy

import pandas as pd
from locust import HttpUser, task

from common.generators import password_generator
from common.utils import create_image, credentials_generator
from setting import BASE_URL, ACCESS_CODE, CREDENTIALS_FILEPATH

logger = logging.getLogger(__name__)

CREDENTIALS_DATAFRAME = pd.read_csv(CREDENTIALS_FILEPATH)
USER_CREDENTIALS_GENERATOR = credentials_generator(CREDENTIALS_DATAFRAME)

POST_DATA_TEMPLATE = {
    "description": None,
    "file": None
}


class PostUser(HttpUser):
    access_token = ""
    post_id_list = []

    def update_access_token(self):
        response = self.client.post(f"{BASE_URL}account/auth/", json=self.credentials_data, verify=False)
        if response.status_code != 200:
            logger.error(f"Can't login with : {self.credentials_data}")
            return ""

        json_response_dict = response.json()
        self.access_token = json_response_dict['access']

    def check_response(self, title, response, expected_status):
        data = response.json()
        if response.status_code != expected_status:
            logger.error(f"ERROR: {title}. Status Code: {response.status_code}. {data.get('detail')}")

            if response.status_code == 401:
                self.update_access_token()

        return data

    @task
    def test(self):
        pass

    @task
    def get_post_list(self):
        try:
            response = self.client.get(f"{BASE_URL}post/",
                                       headers={"Authorization": "Bearer  " + self.access_token},
                                       verify=False)
            self.check_response("get_post_list", response, 200)
        except Exception as e:
            logger.error(repr(e))

    @task
    def get_detail_post(self):
        try:
            if self.post_id_list:
                post_id = random.choice(self.post_id_list)
                response = self.client.get(f"{BASE_URL}post/{post_id}",
                                           headers={"Authorization": "Bearer  " + self.access_token},
                                           verify=False)
                self.check_response("get_detail_post", response, 200)
            else:
                self.create_post()
        except Exception as e:
            logger.error(repr(e))

    @task
    def create_post(self):
        try:
            data = deepcopy(POST_DATA_TEMPLATE)
            data.update({'description': password_generator()})
            with create_image() as image:
                response = self.client.post(f"{BASE_URL}post/",
                                            json=data,
                                            files={'file': image},
                                            headers={"Authorization": "Bearer  " + self.access_token},
                                            verify=False)

            post_data = self.check_response("create_post", response, 201)

            post_id = post_data.get('id')
            if post_id:
                self.post_id_list.append(post_id)
        except Exception as e:
            logger.error(repr(e))

    def on_start(self):
        self.credentials_data = next(USER_CREDENTIALS_GENERATOR, None)
        if self.credentials_data is None:
            logger.error(
                f"No credentials found. There are only {len(CREDENTIALS_DATAFRAME.index)} credentials values available.")
            self.stop()
            return

        self.credentials_data.update({'username': password_generator()[0:15]})
        self.credentials_data.update({'access_code': ACCESS_CODE})

        print(BASE_URL)
        response = self.client.post(f"{BASE_URL}account/auth/", json=self.credentials_data, verify=False)
        json_response_dict = self.check_response("authenticate", response, 200)
        self.access_token = json_response_dict.get('access')

        if self.access_token is None:
            self.stop()
            return

import argparse
import logging

import invokust

from load_scenarious.create_posts import PostUser
from setting import BASE_URL, NUM_USERS, SPAWN_RATE, RUN_TIME

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start load testing')
    parser.add_argument('--num_users', default=NUM_USERS, type=int, help='Number of users to create')
    parser.add_argument('--spawn_rate', default=SPAWN_RATE, type=int, help='spawn rate')
    parser.add_argument('--run_time', default=RUN_TIME, type=str,
                        help='Run time limit. Set as str value, e.g. 30s, 10m, 24h, etc')
    args = parser.parse_args()

    if BASE_URL is None:
        logger.error(
            f"Base URL is not defined, check if you set valid value to BASE_URL param. "
            f"Current base_url value: {BASE_URL}")

    else:
        settings = invokust.create_settings(
            classes=[PostUser],
            host=BASE_URL,
            num_users=args.num_users,
            spawn_rate=args.spawn_rate,
            run_time=args.run_time
        )

        load_test = invokust.LocustLoadTest(settings)
        load_test.run()
        load_test.stats()

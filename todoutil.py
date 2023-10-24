import click
from collections import defaultdict
import json
import datetime
import os
from todoist_api_python.http_requests import get
from todoist_api_python.endpoints import get_sync_url

from todoist_api_python.api import TodoistAPI, Project, Section

API_TOKEN = os.getenv("TODOIST_API_TOKEN")
api = TodoistAPI(API_TOKEN)

ALL_COMPLETED_ENDPOINT = "completed/get_all"

@click.group()
def main():
    pass

@click.command()
@click.option('--days', type=int, default=7, help='Number of days to look back')
def recently_completed(days):

    def _get_recently_completed():
        endpoint = get_sync_url(ALL_COMPLETED_ENDPOINT)
        base_req = {
          "limit": 200,
          "since": (datetime.datetime.now() - datetime.timedelta(days=days)).isoformat(),
        }
        offset = 0

        while True:
            req = dict(base_req)
            if offset:
                req["offset"] = offset
            completed = get(api._session, endpoint, api._token, req)
            for item in completed["items"]:
                yield item
            if len(completed["items"]) < req["limit"]:
                break
            offset += req["limit"]

    for item in sorted(_get_recently_completed(), key=lambda x: x["completed_at"]):
        print(f":greendone: {item['content']}")

main.add_command(recently_completed)

if __name__ == '__main__':
    main()

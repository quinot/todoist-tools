import click
from collections import defaultdict
import json
import datetime
import os
from todoist_api_python.api import TodoistAPI

API_TOKEN = os.getenv("TODOIST_API_TOKEN")
api = TodoistAPI(API_TOKEN)

@click.group()
def main():
    pass

@click.command()
@click.option('--days', type=int, default=7, help='Number of days to look back')
def recently_completed(days):
    now = datetime.datetime.now()
    since = now - datetime.timedelta(days=days)

    def _get_recently_completed():
        for page in api.get_completed_tasks_by_completion_date(since=since, until=now):
            yield from page

    for task in sorted(_get_recently_completed(), key=lambda t: t.completed_at):
        print(f":greendone: {task.content}")

main.add_command(recently_completed)

if __name__ == '__main__':
    main()

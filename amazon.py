from botocore.vendored import requests
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import os
import sys
import boto3
import json

dynamodb = boto3.resource('dynamodb')


def search_for_jobs(query):
    request = requests.get('https://www.amazon.jobs/en/search.json?' + str(query),
                           headers={'accept': 'application/json'})

    return request.json()['jobs']


def get_new_jobs(jobs):
    new_jobs = []
    table = dynamodb.Table('Jobs')

    for job in jobs:
        try:
            resp = table.put_item(
                Item={
                    'id': job['id_icims'],
                },
                ConditionExpression=Attr('id').not_exists())

            print(resp)
            new_jobs.append(job)

        except ClientError as e:
            print(e)

    return new_jobs


def new_job_attachment(title, url):
    data = {
        'title': title,
        'title_link': url,
    }
    return data


def main(query):
    all_jobs = search_for_jobs(query)
    new_jobs = get_new_jobs(all_jobs)

    slack_hook = os.environ['slack_hook']

    data = {'text': '<!here> new jobs!'}
    attachments = []
    data['attachments'] = attachments

    for job in new_jobs:
        attachments.append(new_job_attachment(
            job['title'], job['url_next_step']))

    if len(attachments) > 0:
        requests.post(slack_hook, json=data)


if __name__ == "__main__":
    main(sys.argv[1])

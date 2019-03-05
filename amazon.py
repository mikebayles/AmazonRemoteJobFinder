import requests
import csv
import json
import sys
import os

def requestNewJobs(query):
    request = requests.get('https://www.amazon.jobs/en/search.json?' +
                           str(query), headers={'accept': 'application/json'})
    jsonDict = request.json()
    sortedJobs = sorted(jsonDict['jobs'], key=lambda k: k['id_icims'])

    return sortedJobs


def loadOldJobs(jobsFileName):
    try:
        with open(jobFileName, "r") as jobFile:
            return jobFile.read()
    except:
        return ""


def newJobAttachment(title, url):
    data = {
        'title': title,
        'title_link': url,
    }
    return data


def findJobs(slackHook, query, jobsFileName):
    sortedJobs = requestNewJobs(query)
    ids = list(map(lambda job: job['id_icims'], sortedJobs))

    oldJobs = loadOldJobs(jobsFileName).splitlines()

    newJobIds = [job for job in ids if job not in oldJobs]

    attachments = []
    for newJobId in newJobIds:
        newJob = [job for job in sortedJobs if job['id_icims'] == newJobId][0]
        attachments.append(newJobAttachment(
            newJob['title'], newJob['url_next_step']))

    if attachments:
        data = {'text' : '<!here> new jobs!'}
        data['attachments'] = attachments
        requests.post(slackHook, json=data)

    mode = 'a' if os.path.exists(jobsFileName) else 'w'
    with open(jobsFileName, mode) as jobFile:
        jobFile.write("\n".join(ids))

if __name__ == "__main__":
    findJobs(sys.argv[1], sys.argv[2], sys.argv[3])

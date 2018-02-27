import requests, csv, json, sys

jobFileName = 'jobs.txt'

def requestNewJobs():
    request = requests.get('https://www.amazon.jobs/search.json?category[]=software-development&location[]=virtual-locations&category[]=software-development', headers= {'accept': 'application/json'})
    jsonDict = request.json()
    sortedJobs = sorted(jsonDict['jobs'], key=lambda k: k['id_icims'])

    return sortedJobs

def loadOldJobs():
    with open(jobFileName, "r") as jobFile:
        return jobFile.read()

sortedJobs = requestNewJobs()
idAndTitles = list(map(lambda job: job['id_icims'] + ',' + job['title'], sortedJobs))
newJobs = "\n".join(idAndTitles)

oldJobs = loadOldJobs()

if oldJobs != newJobs:
    data = {'text' : '@here new jobs!'}
    requests.post(sys.argv[1], json=data)

with open(jobFileName, "w") as jobFile:
    jobFile.write(newJobs)
import requests, csv, json, sys

def requestNewJobs(query):
    request = requests.get('https://www.amazon.jobs/en/search.json?' + str(query), headers= {'accept': 'application/json'})
    jsonDict = request.json()
    sortedJobs = sorted(jsonDict['jobs'], key=lambda k: k['id_icims'])

    return sortedJobs

def loadOldJobs():
    try:
        with open(jobFileName, "r") as jobFile:
            return jobFile.read()
    except:
        pass
    
jobFileName = sys.argv[3]    

sortedJobs = requestNewJobs(sys.argv[2])
idAndTitles = list(map(lambda job: job['id_icims'] + ',' + job['title'], sortedJobs))
newJobs = "\n".join(idAndTitles)

oldJobs = loadOldJobs()

if oldJobs != newJobs:
    data = {'text' : '@here new jobs!'}
    requests.post(sys.argv[1], json=data)

with open(jobFileName, "w") as jobFile:
    jobFile.write(newJobs)

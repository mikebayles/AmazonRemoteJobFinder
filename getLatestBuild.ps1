$url = "$env:SYSTEM_TEAMFOUNDATIONCOLLECTIONURI$env:SYSTEM_TEAMPROJECT/_apis/build/latest/$env:SYSTEM_DEFINITIONID"
Write-Host "URL: $url"
$response = Invoke-RestMethod -Uri $url -Headers @{
    Authorization = "Bearer $env:SYSTEM_ACCESSTOKEN"
}
Write-Host "response = $response"
$lastBuild = $response.id
Write-Host "LastBuild = $lastBuild"
Write-Host "##vso[task.setvariable variable=lastBuild]$lastBuild"

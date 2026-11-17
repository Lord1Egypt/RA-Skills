param(
    [Parameter(Mandatory)][string]$Url,
    [string]$NotebookGuid = ""
)
. "$PSScriptRoot\_common.ps1"

$body = @{ url = $Url; source = "skill" }
if ($NotebookGuid) { $body.notebookGuid = $NotebookGuid }
$bodyJson = $body | ConvertTo-Json -Compress

$job = Start-Job {
    param($token, $bodyJson)

    $response = Invoke-WebRequest `
        -Uri "https://app.yinxiang.com/third/clipper-gateway/restful/v1/clipAndSaveNote" `
        -Method POST `
        -Headers @{ auth = $token; "clipper-c-auth" = $token } `
        -Body ([System.Text.Encoding]::UTF8.GetBytes($bodyJson)) `
        -ContentType "text/plain; charset=utf-8" `
        -UseBasicParsing

    if ($response.RawContentStream) {
        if ($response.RawContentStream.CanSeek) {
            $response.RawContentStream.Position = 0
        }
        $reader = New-Object System.IO.StreamReader($response.RawContentStream, [System.Text.Encoding]::UTF8)
        try {
            $reader.ReadToEnd()
        } finally {
            $reader.Dispose()
        }
    } else {
        $response.Content
    }
} -ArgumentList $TOKEN, $bodyJson

if (-not (Wait-Job $job -Timeout 5)) {
    Write-Output "剪藏任务已提交，请稍后到APP里查看剪藏结果"
    exit 0
}

if ($job.State -eq "Failed") {
    $reason = if ($job.ChildJobs[0].JobStateInfo.Reason) { $job.ChildJobs[0].JobStateInfo.Reason.Message } else { "剪藏请求提交失败" }
    $result = @{ code = 1; message = $reason } | ConvertTo-Json -Compress
    Remove-Job $job
    Write-Output $result
    exit 1
}

$responseText = Receive-Job $job
Remove-Job $job

if ($responseText) {
    Write-Output $responseText
} else {
    Write-Output "剪藏任务已提交，请稍后到APP里查看剪藏结果"
}

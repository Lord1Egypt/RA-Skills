param(
    [Parameter(Mandatory=$true)]
    [string]$Bin,
    [Alias("HostName")]
    [string]$Ip = "192.168.9.42",
    [string]$Endpoint = "/ota",
    [int]$TimeoutSec = 60
)

function Get-OtaUri {
    param(
        [string]$HostOrUrl,
        [string]$Path
    )

    if ($HostOrUrl -notmatch "^[a-zA-Z][a-zA-Z0-9+.-]*://") {
        $HostOrUrl = "http://$HostOrUrl"
    }

    $uri = [System.Uri]$HostOrUrl
    if (-not [string]::IsNullOrWhiteSpace($uri.AbsolutePath) -and $uri.AbsolutePath -ne "/") {
        return $uri.AbsoluteUri
    }

    $base = $HostOrUrl.TrimEnd("/") + "/"
    return ([System.Uri]::new([System.Uri]$base, $Path.TrimStart("/"))).AbsoluteUri
}

$binPath = (Resolve-Path -LiteralPath $Bin -ErrorAction Stop).Path
$uri = Get-OtaUri -HostOrUrl $Ip -Path $Endpoint
Write-Host "Uploading $binPath to $uri ..."

$client = [System.Net.Http.HttpClient]::new()
$fileStream = $null
$fileContent = $null
$form = $null

try {
    $client.Timeout = [TimeSpan]::FromSeconds($TimeoutSec)
    $form = [System.Net.Http.MultipartFormDataContent]::new()
    $fileStream = [System.IO.File]::OpenRead($binPath)
    $fileContent = [System.Net.Http.StreamContent]::new($fileStream)
    $fileContent.Headers.ContentType = [System.Net.Http.Headers.MediaTypeHeaderValue]::Parse("application/octet-stream")
    $form.Add($fileContent, "file", [System.IO.Path]::GetFileName($binPath))

    $response = $client.PostAsync($uri, $form).GetAwaiter().GetResult()
    $result = $response.Content.ReadAsStringAsync().GetAwaiter().GetResult().Trim()
    Write-Host "Response: $result"
    if ($response.IsSuccessStatusCode -and $result -eq "OK") {
        Write-Host "OTA upload successful. Device will restart in ~1.2s."
    } else {
        Write-Host "OTA upload failed."
        exit 1
    }
} catch {
    Write-Host "Error: $_"
    exit 1
} finally {
    if ($null -ne $form) { $form.Dispose() }
    if ($null -ne $fileContent) { $fileContent.Dispose() }
    if ($null -ne $fileStream) { $fileStream.Dispose() }
    $client.Dispose()
}

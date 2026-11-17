param(
    [Parameter(Mandatory = $true)][string]$InputDocx,
    [Parameter(Mandatory = $true)][string]$OutputDir,
    [int]$Dpi = 144
)

$ErrorActionPreference = 'Stop'
$inputPath = (Resolve-Path -LiteralPath $InputDocx).Path
$outputPath = [System.IO.Path]::GetFullPath($OutputDir)
[System.IO.Directory]::CreateDirectory($outputPath) | Out-Null
$stem = [System.IO.Path]::GetFileNameWithoutExtension($inputPath)
$pdfPath = Join-Path $outputPath ($stem + '.pdf')

function New-OfficeApplication {
    foreach ($candidate in @(
        @{ ProgId = 'Word.Application'; Backend = 'Microsoft Word COM' },
        @{ ProgId = 'KWPS.Application'; Backend = 'WPS Writer COM' }
    )) {
        try {
            $app = New-Object -ComObject $candidate.ProgId
            return @{ App = $app; Backend = $candidate.Backend }
        } catch {
            continue
        }
    }
    throw 'Neither Word.Application nor KWPS.Application COM automation is available.'
}

$office = New-OfficeApplication
$app = $office.App
$document = $null
try {
    $app.Visible = $false
    try { $app.DisplayAlerts = 0 } catch {}
    $document = $app.Documents.Open($inputPath, $false, $true)
    try {
        # 17 = wdExportFormatPDF / PDF in Word and WPS-compatible APIs.
        $document.ExportAsFixedFormat($pdfPath, 17)
    } catch {
        # Some WPS builds expose SaveAs but not ExportAsFixedFormat.
        $document.SaveAs($pdfPath, 17)
    }
    $document.Close($false)
    $document = $null
} finally {
    if ($null -ne $document) { try { $document.Close($false) } catch {} }
    try { $app.Quit() } catch {}
    if ($null -ne $document) { [void][Runtime.InteropServices.Marshal]::ReleaseComObject($document) }
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}

if (-not (Test-Path -LiteralPath $pdfPath) -or (Get-Item -LiteralPath $pdfPath).Length -eq 0) {
    throw "Office backend did not produce a non-empty PDF: $pdfPath"
}

$pdftoppm = Get-Command pdftoppm -ErrorAction SilentlyContinue
if (-not $pdftoppm) {
    $bundled = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe'
    if (Test-Path -LiteralPath $bundled) { $pdftoppm = Get-Item -LiteralPath $bundled }
}
if (-not $pdftoppm) {
    throw 'PDF export succeeded, but pdftoppm is unavailable for page rendering.'
}

$prefix = Join-Path $outputPath 'page'
& $pdftoppm.Source -png -r $Dpi $pdfPath $prefix
if ($LASTEXITCODE -ne 0) { throw "pdftoppm failed with exit code $LASTEXITCODE" }
$pages = @(Get-ChildItem -LiteralPath $outputPath -Filter 'page-*.png' | Sort-Object Name)
if ($pages.Count -eq 0) { throw 'No rendered page PNGs were produced.' }

[ordered]@{
    status = 'pass'
    backend = $office.Backend
    input = $inputPath
    pdf = $pdfPath
    pages = $pages.Count
    page_files = @($pages.FullName)
} | ConvertTo-Json -Depth 4


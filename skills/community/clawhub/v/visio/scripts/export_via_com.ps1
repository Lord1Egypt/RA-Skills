# export_via_com.ps1 — 通过 Visio COM 自动化批量导出 .vsdx 页面为 SVG / PNG / PDF
#
# 用法（PowerShell）:
#   powershell -File export_via_com.ps1 -InputFile "C:\path\diagram.vsdx" -OutDir "C:\path\out" -Format svg
#
# 前置条件:
#   - 本机已安装桌面版 Microsoft Visio（2016 及以上）。
#   - 导出 PDF 需要 Visio 2013+。
param(
    [Parameter(Mandatory = $true)][string]$InputFile,
    [Parameter(Mandatory = $true)][string]$OutDir,
    [ValidateSet("svg", "png", "pdf")][string]$Format = "svg"
)

$ErrorActionPreference = "Stop"
if (-not (Test-Path $InputFile)) { throw "文件不存在: $InputFile" }
if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir | Out-Null }

$visio = $null
$doc = $null
try {
    $visio = New-Object -ComObject Visio.Application
    $visio.Visible = $false
    $doc = $visio.Documents.Open((Resolve-Path $InputFile).Path)
    foreach ($page in $doc.Pages) {
        $safeName = ($page.Name -replace '[\\/:*?"<>|]', '_')
        $outFile = Join-Path $OutDir ($safeName + "." + $Format)
        if ($Format -eq "pdf") {
            # ExportAsFixedFormat 导出当前页
            $page.ExportAsFixedFormat(1, $outFile)  # 1 = visFixedFormatPDF
        } else {
            $page.Export($outFile)
        }
        Write-Output ("已导出: " + $outFile)
    }
}
finally {
    if ($doc) { $doc.Close() }
    if ($visio) { $visio.Quit() | Out-Null }
}

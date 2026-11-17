param([string]$Docx, [string]$Pdf)

# Word COM 转 PDF。
# 坑：直接 SaveAs 到中文路径会被 COM 静默吞（文件不生成）；
#     且 $env:TEMP 在某些环境返回 HANLEY~1 这种 8.3 短路径导致 SaveAs 报"值不在预期范围内"。
# 解法：先用项目目录下 ASCII 临时名 SaveAs，再 Copy 回中文目标名。

$w = $null
$tmp = Join-Path (Split-Path $Docx) "_tmp_conv.pdf"
try {
    $w = New-Object -ComObject Word.Application
    $w.Visible = $false
    $d = $w.Documents.Open($Docx)
    $d.SaveAs([ref]$tmp, [ref]17)   # wdFormatPDF = 17
    $d.Close()
} catch {
    Write-Error ("SAVE_FAIL: " + $_.Exception.Message)
    exit 3
} finally {
    if ($w) { try { $w.Quit() } catch {} }
}

if (Test-Path $tmp) {
    Copy-Item $tmp $Pdf -Force
    Remove-Item $tmp -Force -ErrorAction SilentlyContinue
    exit 0
} else {
    Write-Error "PDF_NOT_CREATED"
    exit 4
}

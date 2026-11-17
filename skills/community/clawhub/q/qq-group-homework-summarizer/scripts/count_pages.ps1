param([Parameter(Mandatory=$true)][string]$Docx)
# 用 Word COM 统计 docx 页数（1 = wdStatisticPages）
$here = Split-Path -Parent $MyInvocation.MyCommand.Definition
$out  = Join-Path (Get-Location) "page_count.txt"
$tmp  = Join-Path (Get-Location) "_tmp_check.docx"

# 中文文件名可能干扰 COM，先拷到 ASCII 临时路径
Copy-Item -LiteralPath $Docx -Destination $tmp -Force

$log = @()
$word = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $doc = $word.Documents.Open($tmp, $false, $true)
    $pages = $doc.ComputeStatistics(2)
    $log += "PAGES=$pages"
    try { $doc.Close($false) } catch {}
} catch {
    # 注意：不要把 Quit 放在会覆盖异常的位置；先记录真实错误
    $log += "ERROR: $($_.Exception.Message)"
} finally {
    if ($word) {
        try { $word.Quit() } catch { $log += "warn quit: $($_.Exception.Message)" }
        try { [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null } catch {}
    }
}
($log -join "`n") | Out-File -FilePath $out -Encoding utf8

# ============================================================
# clipboard.ps1 — 剪贴板操作 for windows-agent skill
# Actions: get(读剪贴板), set(写剪贴板), clear(清空), help
# 用 PowerShell 原生 cmdlet + WinForms，纯 Windows 原生
# ============================================================
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("get","set","clear","help")]
    [string]$Action,
    [string]$Text = ""        # set 时要写入的文本
)

Add-Type -AssemblyName System.Windows.Forms
$ErrorActionPreference = "Continue"

try {
switch($Action){
    "get" {
        # 先检测非文本内容(图片/文件等), 避免只读文本而误报"(空)"导致备份/覆盖丢内容
        $hasImg = [System.Windows.Forms.Clipboard]::ContainsImage()
        $hasFile = [System.Windows.Forms.Clipboard]::ContainsFileDropList()
        $hasData = [System.Windows.Forms.Clipboard]::ContainsData("FileDrop")
        $t = [System.Windows.Forms.Clipboard]::GetText()
        if($t){ "CLIPBOARD: $t" }
        elseif($hasImg){ "CLIPBOARD: (含图片, 非文本; get 只能读文本)" }
        elseif($hasFile -or $hasData){
            $files = [System.Windows.Forms.Clipboard]::GetFileDropList()
            $names = @($files) -join ", "
            "CLIPBOARD: (文件/文件夹: $names)"
        }
        else { "CLIPBOARD: (空)" }
    }
    "set" {
        if(-not $Text){ "ERROR: 需要 -Text 要写入的文本"; exit 1 }
        [System.Windows.Forms.Clipboard]::SetText($Text)
        Start-Sleep -Milliseconds 200
        $v = [System.Windows.Forms.Clipboard]::GetText()
        "SET: 剪贴板已写入 ($($v.Length) 字符)"
    }
    "clear" {
        [System.Windows.Forms.Clipboard]::Clear()
        "CLEARED: 剪贴板已清空"
    }
    "help" { Write-Output @"
windows-agent / clipboard.ps1 — 剪贴板
Actions:
  get    读剪贴板文本 (输出 CLIPBOARD: ...)
  set    -Text <内容> 写入剪贴板
  clear  清空剪贴板
示例:
  clipboard.ps1 -Action get
  clipboard.ps1 -Action set -Text "你好"
  clipboard.ps1 -Action clear
"@ }
}
exit 0
} catch {
    Write-Error "clipboard.ps1 错误: $_"
    exit 1
}

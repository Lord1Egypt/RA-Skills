[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet('build', 'search', 'duplicates', 'import-metadata', 'status')]
    [string]$Command,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$RemainingArguments
)

$ErrorActionPreference = 'Stop'
chcp 65001 | Out-Null
$env:PYTHONUTF8 = '1'

$bundledPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if (Test-Path -LiteralPath $bundledPython -PathType Leaf) {
    $python = $bundledPython
} else {
    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if ($null -eq $pythonCommand) {
        throw 'Python 3 was not found. Load the Codex workspace dependencies or install Python 3.'
    }
    $python = $pythonCommand.Source
}

$script = Join-Path $PSScriptRoot 'wechat_file_index.py'
& $python $script $Command @RemainingArguments
exit $LASTEXITCODE

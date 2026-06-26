param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$cliPath = Join-Path $scriptDir "tokenmail_cli.js"

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Error "Node.js not found. Please install Node.js 18+ first."
    exit 1
}

& node $cliPath @Args
exit $LASTEXITCODE

$ErrorActionPreference = "Stop"
if ($args.Count -ne 0) {
  [Console]::Out.WriteLine('{"contractVersion":"1.0","status":"error","error":{"code":"arguments_not_allowed","message":"Read one JSON request from stdin."}}')
  exit 2
}
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
& node (Join-Path $scriptRoot "invoke.mjs")
exit $LASTEXITCODE

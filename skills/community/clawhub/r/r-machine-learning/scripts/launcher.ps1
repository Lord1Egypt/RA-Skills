# R Machine Learning Workbench - PowerShell Launcher (Windows)
# Usage: .\scripts\launcher.ps1 <command> [options]

$BaseDir = Split-Path -Parent $PSScriptRoot
$RScriptDir = Join-Path $BaseDir "scripts"

# Set working directory to skill root so R scripts can source scripts/utils.R
Set-Location $BaseDir

# Create output directories
@("plots", "models", "predictions", "reports", "tables") | ForEach-Object {
  $dir = Join-Path (Join-Path $BaseDir "output") $_
  if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
}

# Verify Rscript is available
$RscriptPath = (Get-Command Rscript.exe -ErrorAction SilentlyContinue).Source
if (-not $RscriptPath) {
  Write-Error "Rscript.exe not found. Please add R to your system PATH."
  exit 1
}

$scriptMap = @{
  "install"          = "install_packages.R"
  "split"            = "data_split.R"
  "explore"          = "data_explore.R"
  "feature_engineer" = "feature_engineering.R"
  "feature_select"   = "feature_selection.R"
  "rf"               = "rf_model.R"
  "xgboost"          = "xgboost_model.R"
  "lasso"            = "lasso_model.R"
  "svm"              = "svm_model.R"
  "tune"             = "hyperparameter_tune.R"
  "cv"               = "cross_validation.R"
  "compare"          = "model_compare.R"
  "roc"              = "roc_analysis.R"
  "calibration"      = "calibration.R"
  "shap"             = "shap_analysis.R"
  "survival"         = "survival_ml.R"
  "pipeline"         = "pipeline.R"
  "report"           = "report_generator.R"
}

$Command = $args[0]
$RArgs = @()
if ($args.Count -gt 1) {
  $RArgs = $args[1..($args.Count - 1)]
}

if (-not $Command -or -not $scriptMap.ContainsKey($Command)) {
  Write-Host ""
  Write-Host "R Machine Learning Workbench - Launcher" -ForegroundColor Cyan
  Write-Host "Usage: .\scripts\launcher.ps1 <command> [options]" -ForegroundColor Gray
  Write-Host ""
  Write-Host "Available commands:" -ForegroundColor Yellow
  $keys = $scriptMap.Keys | Sort-Object
  foreach ($key in $keys) {
    Write-Host ("  {0,-20}" -f $key)
  }
  exit 1
}

$RScriptPath = Join-Path $RScriptDir $scriptMap[$Command]
Write-Host "[R ML] Running: $Command" -ForegroundColor Green

& Rscript.exe $RScriptPath $RArgs

exit $LASTEXITCODE

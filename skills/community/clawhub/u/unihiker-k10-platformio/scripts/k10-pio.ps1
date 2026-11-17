param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("doctor", "ports", "build", "upload", "monitor")]
    [string]$Command,

    [string]$ProjectDir = ".",
    [string]$Port = ""
)

function Need-Pio {
    $pio = Get-Command pio -ErrorAction SilentlyContinue
    if (-not $pio) {
        Write-Error "pio not found. Install PlatformIO Core first."
        Write-Host "See: https://docs.platformio.org/en/latest/core/installation/methods/installer-script.html"
        exit 1
    }
}

Need-Pio

switch ($Command) {
    "doctor" {
        Write-Host "[INFO] PlatformIO:"
        pio --version
        Write-Host ""
        Write-Host "[INFO] esptool Python dependency check:"
        python -c "import intelhex; print('[OK] intelhex module available to python')" 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[WARN] python cannot import intelhex. If pio build fails inside tool-esptoolpy, repair/reinstall PlatformIO Core."
        }
        Write-Host ""
        Write-Host "[INFO] K10 project config:"
        $ini = Join-Path $ProjectDir "platformio.ini"
        if (Test-Path $ini) {
            Select-String -Path $ini -Pattern "^(platform|board|framework|\s*-DARDUINO_USB|\s*-DModel)" | ForEach-Object { $_.Line }
        } else {
            Write-Host "[WARN] No platformio.ini found in $ProjectDir"
        }
    }
    "ports" {
        pio device list
    }
    "build" {
        pio run -d $ProjectDir
    }
    "upload" {
        if ($Port) {
            pio run -d $ProjectDir -t upload --upload-port $Port
        } else {
            pio run -d $ProjectDir -t upload
        }
    }
    "monitor" {
        if ($Port) {
            pio device monitor -d $ProjectDir --port $Port
        } else {
            pio device monitor -d $ProjectDir
        }
    }
}

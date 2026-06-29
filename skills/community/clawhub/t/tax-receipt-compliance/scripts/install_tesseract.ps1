# 安装脚本 - Windows PowerShell
# 检测并安装Tesseract OCR引擎（支持国内镜像源）

Set-Location (Split-Path -Path $MyInvocation.MyCommand.Definition -Parent)

Write-Host "=== 财税合规Skill安装脚本 ===" -ForegroundColor Green
Write-Host ""

# 检查Python版本
function Check-Python {
    try {
        $python = Get-Command python -ErrorAction SilentlyContinue
        if ($python) {
            $version = python --version 2>&1
            Write-Host "✓ Python: $version" -ForegroundColor Green
            return "python"
        }
        
        $python3 = Get-Command python3 -ErrorAction SilentlyContinue
        if ($python3) {
            $version = python3 --version 2>&1
            Write-Host "✓ Python3: $version" -ForegroundColor Green
            return "python3"
        }
        
        Write-Host "✗ 未找到Python，请先安装Python 3.8+" -ForegroundColor Red
        Write-Host "  下载地址: https://www.python.org/downloads/"
        exit 1
    }
    catch {
        Write-Host "✗ 未找到Python，请先安装Python 3.8+" -ForegroundColor Red
        exit 1
    }
}

# 检查Tesseract
function Check-Tesseract {
    try {
        $tesseract = Get-Command tesseract -ErrorAction SilentlyContinue
        if ($tesseract) {
            $version = tesseract --version 2>&1 | Select-Object -First 1
            Write-Host "✓ Tesseract: $version" -ForegroundColor Green
            return $true
        }
    }
    catch { }
    
    Write-Host "✗ Tesseract未安装" -ForegroundColor Red
    return $false
}

# 下载文件（带重试和进度显示）
function Download-File {
    param(
        [string]$Url,
        [string]$OutFile,
        [int]$MaxRetries = 3
    )
    
    for ($i = 1; $i -le $MaxRetries; $i++) {
        try {
            Write-Host "  正在下载 (尝试 $i/$MaxRetries)..." -ForegroundColor Yellow
            
            # 使用HttpClient显示进度
            $client = New-Object System.Net.Http.HttpClient
            $response = $client.GetAsync($Url, [System.Net.Http.HttpCompletionOption]::ResponseHeadersRead).Result
            
            if (-not $response.IsSuccessStatusCode) {
                throw "HTTP错误: $($response.StatusCode)"
            }
            
            $totalBytes = $response.Content.Headers.ContentLength
            $stream = $response.Content.ReadAsStreamAsync().Result
            $fileStream = [System.IO.File]::Create($OutFile)
            $buffer = New-Object[] 8192
            $totalRead = 0
            $lastProgress = 0
            
            while (($read = $stream.Read($buffer, 0, $buffer.Length)) -ne 0) {
                $fileStream.Write($buffer, 0, $read)
                $totalRead += $read
                
                if ($totalBytes -gt 0) {
                    $progress = [math]::Floor(($totalRead / $totalBytes) * 100)
                    if ($progress -ge $lastProgress + 10) {
                    $mbRead = [math]::Round($totalRead / [math]::Pow(1024, 2), 1)
                    $mbTotal = [math]::Round($totalBytes / [math]::Pow(1024, 2), 1)
                        Write-Host "    进度: $progress% ($mbRead MB / $mbTotal MB)" -ForegroundColor Gray
                        $lastProgress = $progress
                    }
                }
            }
            
            $fileStream.Close()
            $stream.Close()
            
            return $true
        }
        catch {
            Write-Host "    下载失败: $_" -ForegroundColor Red
            if ($i -lt $MaxRetries) {
                $waitTime = [math]::Pow(2, $i)
                Write-Host "    等待 ${waitTime}秒后重试..." -ForegroundColor Yellow
                Start-Sleep -Seconds $waitTime
            }
        }
    }
    
    return $false
}

# 安装Tesseract（使用国内镜像）
function Install-Tesseract {
    Write-Host ""
    Write-Host "Tesseract未安装，请选择安装方式：" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  1. 使用国内镜像下载（推荐，速度快）"
    Write-Host "     镜像: https://gitee.com/woaini0919/tesseract-ocr/releases"
    Write-Host ""
    Write-Host "  2. 使用winget一键安装（自动配置PATH）"
    Write-Host "     命令: winget install UB-Mannheim.TesseractOCR"
    Write-Host ""
    Write-Host "  3. 使用scoop包管理器"
    Write-Host "     命令: scoop install tesseract"
    Write-Host ""
    Write-Host "  4. 我已手动安装，跳过此步骤"
    Write-Host ""
    
    $choice = Read-Host "请输入选项 (1/2/3/4)"
    
    switch ($choice) {
        "1" {
            $mirrorUrl = "https://gitee.com/woaini0919/tesseract-ocr/releases/download/v5.3.3.20231005/tesseract-ocr-w64-setup-5.3.3.20231005.exe"
            $tempFile = Join-Path $env:TEMP "tesseract_setup.exe"
            
            Write-Host ""
            Write-Host "正在从国内镜像下载Tesseract..." -ForegroundColor Yellow
            
            if (Download-File -Url $mirrorUrl -OutFile $tempFile) {
                Write-Host "下载完成，正在安装..." -ForegroundColor Yellow
                Start-Process -FilePath $tempFile -Wait
                Remove-Item $tempFile -Force -ErrorAction SilentlyContinue
                Write-Host "✓ Tesseract安装完成" -ForegroundColor Green
            }
            else {
                Write-Host "✗ 下载失败，请检查网络连接或手动安装" -ForegroundColor Red
                exit 1
            }
        }
        "2" {
            Write-Host ""
            Write-Host "正在使用winget安装..." -ForegroundColor Yellow
            winget install UB-Mannheim.TesseractOCR --accept-source-agreements --accept-package-agreements
            Write-Host "✓ winget安装完成" -ForegroundColor Green
        }
        "3" {
            Write-Host ""
            Write-Host "正在使用scoop安装..." -ForegroundColor Yellow
            scoop install tesseract
            Write-Host "✓ scoop安装完成" -ForegroundColor Green
        }
        "4" {
            Write-Host ""
            Write-Host "已跳过自动安装。" -ForegroundColor Yellow
            Write-Host "请确保Tesseract已安装并添加到系统PATH中。" -ForegroundColor Yellow
            return
        }
        default {
            Write-Host "无效选项，退出安装。" -ForegroundColor Red
            exit 1
        }
    }
    
    # 刷新PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# 安装Python依赖
function Install-PythonDeps {
    param($PythonCmd)
    
    Write-Host ""
    Write-Host "正在安装Python依赖..." -ForegroundColor Yellow
    
    & $PythonCmd -m pip install --upgrade pip
    & $PythonCmd -m pip install Pillow pytesseract openpyxl pyyaml
    
    # PDF支持（可选）
    $poppler = Get-Command pdftoppm -ErrorAction SilentlyContinue
    if ($poppler) {
        & $PythonCmd -m pip install pdf2image
        Write-Host "✓ PDF支持已启用" -ForegroundColor Green
    }
    else {
        Write-Host "⚠ poppler未安装，PDF支持不可用" -ForegroundColor Yellow
        Write-Host "  可手动下载: https://github.com/oschwartz10612/poppler-windows/releases"
    }
}

# 验证安装
function Verify-Installation {
    param($PythonCmd)
    
    Write-Host ""
    Write-Host "=== 验证安装 ===" -ForegroundColor Green
    
    # 验证Tesseract
    try {
        $tesseract = Get-Command tesseract -ErrorAction SilentlyContinue
        if ($tesseract) {
            Write-Host "✓ Tesseract: $(tesseract --version 2>&1 | Select-Object -First 1)" -ForegroundColor Green
        }
        else {
            Write-Host "✗ Tesseract: 未安装" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "✗ Tesseract: 未安装" -ForegroundColor Red
    }
    
    # 验证Python模块
    & $PythonCmd -c "import sys; mods=['PIL','pytesseract','openpyxl']; miss=[m for m in mods if not __import__(m)]; [print(f'OK {m}') for m in mods if m not in miss]; [print(f'MISSING {m}') for m in miss]; print(f'pip install '+' '.join(miss)) if miss else print('All packages OK')"
}

# 主流程
$python = Check-Python

if (-not (Check-Tesseract)) {
    Install-Tesseract
}

Install-PythonDeps -PythonCmd $python
Verify-Installation -PythonCmd $python

Write-Host ""
Write-Host "=== 安装完成 ===" -ForegroundColor Green
Write-Host ""
Write-Host "使用方法:" -ForegroundColor Yellow
Write-Host "1. 首次使用请编辑 config.yaml 配置企业信息"
Write-Host "2. 识别发票: python scripts/ocr_engine.py --input 发票.png --output receipt.json"
Write-Host "3. 查验真伪: python scripts/verify_abstract.py --config config.yaml --receipt receipt.json"
Write-Host "4. 生成报销单: python scripts/template_matcher.py fill --config config.yaml --receipt receipt.json --template templates/expense_basic.xlsx"

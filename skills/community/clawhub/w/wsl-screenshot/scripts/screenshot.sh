#!/bin/bash
# WSL 截图脚本 - 调用 Windows PowerShell 截图

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_PATH="C:\\Users\\97027\\Pictures\\wsl_screenshot_${TIMESTAMP}.png"
OUTPUT_UNIX="/mnt/c/Users/97027/Pictures/wsl_screenshot_${TIMESTAMP}.png"

echo "📸 正在截图..."

/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -Command "
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
\$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
\$bitmap = New-Object System.Drawing.Bitmap(\$screen.Width, \$screen.Height)
\$graphics = [System.Drawing.Graphics]::FromImage(\$bitmap)
\$graphics.CopyFromScreen(\$screen.Location, [System.Drawing.Point]::Empty, \$screen.Size)
\$bitmap.Save('${OUTPUT_PATH}')
Write-Host '✅ Screenshot saved to: ${OUTPUT_PATH}'
"

if [ -f "$OUTPUT_UNIX" ]; then
    echo "📁 截图保存位置: $OUTPUT_UNIX"
    echo "🖼️  文件大小: $(du -h $OUTPUT_UNIX | cut -f1)"
else
    echo "❌ 截图可能失败了"
fi
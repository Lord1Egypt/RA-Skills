#!/usr/bin/env python3
"""测试脚本 - 输出到文件"""
import subprocess
import os

# PowerShell脚本
ps_script = r'''
Add-Type @"
  using System;
  using System.Runtime.InteropServices;
  public class WinAPI {
    public delegate bool CallBack(IntPtr hWnd, IntPtr lParam);
    [DllImport("user32.dll")] public static extern int EnumWindows(CallBack cb, IntPtr lParam);
    [DllImport("user32.dll", CharSet=CharSet.Auto)] public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder lpString, int nMaxCount);
    [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hWnd);
  }
"@

$callback = {
  param([IntPtr]$hWnd, [IntPtr]$lParam)
  if ([WinAPI]::IsWindowVisible($hWnd)) {
    $sb = New-Object System.Text.StringBuilder 256
    [WinAPI]::GetWindowText($hWnd, $sb, 256) | Out-Null
    $title = $sb.ToString()
    if ($title) {
      Write-Output "$hWnd|$title"
    }
  }
  return $true
}

[WinAPI]::EnumWindows($callback, [IntPtr]::Zero)
'''

# 运行PowerShell
result = subprocess.run(
    ['powershell', '-Command', ps_script],
    capture_output=True,
    text=True,
    encoding='utf-8'
)

# 输出到文件
output_file = os.path.join(os.path.dirname(__file__), 'windows_list.txt')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(f"Return code: {result.returncode}\n")
    f.write(f"Stderr: {result.stderr}\n")
    f.write(f"Stdout:\n{result.stdout}\n")

print(f"结果已保存到: {output_file}")

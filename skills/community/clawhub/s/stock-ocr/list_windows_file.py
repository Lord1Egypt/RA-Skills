#!/usr/bin/env python3
"""列出所有可见窗口并保存到文件"""
import subprocess
import os

ps_script = r'''
Add-Type @"
  using System;
  using System.Runtime.InteropServices;
  public class Win32 {
    [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hWnd);
  }
"@

Add-Type @"
  using System;
  using System.Runtime.InteropServices;
  public class EnumWindows {
    public delegate bool CallBack(IntPtr hWnd, IntPtr lParam);
    [DllImport("user32.dll")] public static extern int EnumWindows(CallBack cb, IntPtr lParam);
    [DllImport("user32.dll", CharSet=CharSet.Auto)] public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder lpString, int nMaxCount);
  }
"@

$callback = {
  param([IntPtr]$hWnd, [IntPtr]$lParam)
  if ([Win32]::IsWindowVisible($hWnd)) {
    $sb = New-Object System.Text.StringBuilder 256
    [EnumWindows]::GetWindowText($hWnd, $sb, 256) | Out-Null
    $title = $sb.ToString()
    if ($title) {
      Write-Output "$hWnd|$title"
    }
  }
  return $true
}

[EnumWindows]::EnumWindows($callback, [IntPtr]::Zero)
'''

# 使用系统默认编码
result = subprocess.run(
    ['powershell', '-Command', ps_script],
    capture_output=True,
    text=True
)

# 输出到文件
output_file = os.path.join(os.path.dirname(__file__), 'windows_list.txt')
with open(output_file, 'w', encoding='utf-8', errors='ignore') as f:
    f.write("=== 可见窗口列表 ===\n\n")
    
    lines = result.stdout.strip().split('\n')
    for line in lines:
        if '|' in line:
            parts = line.split('|', 1)
            if len(parts) == 2:
                hwnd, title = parts
                f.write(f"[{hwnd.strip()}] {title.strip()}\n")
    
    f.write(f"\n=== 共 {len([l for l in lines if '|' in l])} 个窗口 ===\n")

print(f"窗口列表已保存到: {output_file}")

# 系统工具与辅助功能

## 获取微信安装路径

```powershell
# 从注册表读取
$regPath = "HKCU:\Software\Tencent\Weixin"
$installPath = (Get-ItemProperty -Path $regPath -Name "InstallPath" -ErrorAction SilentlyContinue).InstallPath
$exePath = Join-Path $installPath "Weixin.exe"
Write-Output $exePath
```

## 获取当前登录 wxid

```powershell
# 方法：遍历 Weixin.exe 进程的内存映射，查找包含 MMKV 的路径
# 需要借助 psutil 等工具，无法直接用 winguictl 实现
# Python 脚本示例：
# import psutil, os, re
# for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
#     if proc.info['name'] == 'Weixin.exe':
#         for mem_map in proc.memory_maps():
#             if 'MMKV' in mem_map.path:
#                 wxid_folder = os.path.dirname(mem_map.path).replace('db_storage', '').replace('MMKV', '')
#                 wxid = re.search(r'wxid_\w+\d+', wxid_folder)
#                 print(wxid.group(0) if wxid else '')
```

## 获取微信版本

```powershell
# 从注册表读取版本号
$regPath = "HKCU:\Software\Tencent\Weixin"
$versionInt = (Get-ItemProperty -Path $regPath -Name "Version" -ErrorAction SilentlyContinue).Version
$hexStr = [Convert]::ToString($versionInt, 16).Substring(3)
$version = "$($hexStr[0]).$($hexStr[1]).$($hexStr[2]).$([Convert]::ToInt32($hexStr.Substring($hexStr.Length-2), 16))"
Write-Output $version
```

## 复制文本到剪贴板

```powershell
# PowerShell 方式（推荐，无需加载 WinForms）
$text = "要复制的文本"
Set-Clipboard -Value $text
```

### 复制 HTML 格式到剪贴板

PowerShell 7+ 需使用 .NET 方式

```powershell
Add-Type -AssemblyName System.Windows.Forms
$html = "<b>粗体文本</b><br><a href='https://example.com'>链接</a>"
[System.Windows.Forms.Clipboard]::SetText($html, [System.Windows.Forms.TextDataFormat]::Html)
```

## 复制文件到剪贴板

#### 复制单个文件
```powershell
python scripts\winguictl.py clipboard copy-files "C:\Users\Documents\report.pdf"
```

#### 复制多个文件
```powershell
python scripts\winguictl.py clipboard copy-files "C:\file1.txt" "C:\file2.txt" "D:\images\photo.png"
```

## 设置系统音量

```powershell
# 使用 pycaw 库（Python）或 PowerShell 调用 CoreAudio API
# PowerShell 示例（需 Windows 8+）：
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
[Guid("5CDF2C82-841E-4546-9722-0CF74078229A"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IAudioEndpointVolume {
    int f(); int g(); int h(); int i();
    int SetMasterVolumeLevelScalar(float fLevel, IntPtr pguidEventContext);
    int GetMasterVolumeLevelScalar(out float pfLevel);
    int SetMute([MarshalAs(UnmanagedType.Bool)] bool bMute, IntPtr pguidEventContext);
    int GetMute(out bool pbMute);
}
[Guid("D666063F-1587-4E43-81F1-B948E807363F"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IMMDevice {
    int Activate(ref Guid iid, int clsCtx, IntPtr activationParams, [MarshalAs(UnmanagedType.IUnknown)] out object interfacePointer);
}
[Guid("A95664D2-9614-4F35-A746-DE8DB63617E6"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IMMDeviceEnumerator {
    int f();
    int GetDefaultAudioEndpoint(int dataFlow, int role, out IMMDevice ppEndpoint);
}
[ComImport, Guid("BCDE0395-E52F-467C-8E3D-C4579291692E")]
class MMDeviceEnumerator { }
public class Volume {
    static Guid IID_IAudioEndpointVolume = new Guid("5CDF2C82-841E-4546-9722-0CF74078229A");
    public static void SetVolume(float level) {
        var enumerator = new MMDeviceEnumerator() as IMMDeviceEnumerator;
        enumerator.GetDefaultAudioEndpoint(0, 1, out var device);
        device.Activate(ref IID_IAudioEndpointVolume, 0, IntPtr.Zero, out var volumeObj);
        var volume = (IAudioEndpointVolume)volumeObj;
        bool mute;
        volume.GetMute(out mute);
        if (mute) volume.SetMute(false, IntPtr.Zero);
        volume.SetMasterVolumeLevelScalar(level, IntPtr.Zero);
    }
}
"@
[Volume]::SetVolume(1.0)  # 100%
```

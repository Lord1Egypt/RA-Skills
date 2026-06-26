#!/usr/bin/env python3
"""
Hardware Controller - Control Windows system hardware settings.

Capabilities:
  - Volume control (get/set/mute)
  - Screen brightness (get/set)
  - Display settings (resolution, orientation)
  - Power management (sleep, hibernate, shutdown, restart, lock)
  - Network adapters (list, enable, disable)
  - WiFi (list networks)
  - USB devices (list)

Requirements: Windows 10/11, PowerShell 5.1+
Dependencies: None for basic features.
"""

import subprocess
import sys
import os

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import run_ps as _run_ps


# ========== Volume Control ==========

def get_volume():
    """Get current volume level and mute state."""
    script = r"""
try {
    Get-WmiObject Win32_SoundDevice | Select-Object -First 1 | ForEach-Object {
        [PSCustomObject]@{
            Device = $_.Name
            Status = $_.Status
        }
    } | ConvertTo-Json
} catch {
    Write-Output '{"Note":"Audio device info unavailable"}'
}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def set_volume(level):
    """Set volume level (0-100). Requires NirCmd for precise control."""
    if not (0 <= level <= 100):
        return "ERROR: Volume level must be 0-100"
    script = f"""
try {{
    $nircmd = Get-Command nircmd -ErrorAction SilentlyContinue
    if ($nircmd) {{
        & nircmd.exe setsysvolume {int(level * 655.35)}
        Write-Output "OK: Volume set to {level}%"
        return
    }}
    Write-Output "INFO: For precise volume control, install NirCmd (nircmd.com) and add to PATH"
}} catch {{
    Write-Output "ERROR: $($_.Exception.Message)"
}}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def toggle_mute():
    """Toggle system mute."""
    script = r"""
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class AudioMute {
    [DllImport("user32.dll")]
    public static extern IntPtr SendMessageW(IntPtr hWnd, int Msg, IntPtr wParam, IntPtr lParam);
    public const int WM_APPCOMMAND = 0x319;
    public const int APPCMD_VOLUME_MUTE = 0x08;
}
"@
$hwnd = (Get-Process -Id $PID).MainWindowHandle
[AudioMute]::SendMessageW($hwnd, [AudioMute]::WM_APPCOMMAND, [IntPtr]::Zero, (IntPtr)([AudioMute]::APPCMD_VOLUME_MUTE * 0x10000))
Write-Output "OK: Toggle mute sent"
"""
    stdout, _, _ = _run_ps(script)
    return stdout


# ========== Screen / Display ==========

def get_brightness():
    """Get screen brightness level."""
    script = r"""
try {
    $brightness = Get-CimInstance -Namespace root/WMI -ClassName WmiMonitorBrightness -ErrorAction Stop
    $current = $brightness.CurrentBrightness
    [PSCustomObject]@{
        Brightness = $current
        MaxBrightness = 100
        MinBrightness = 0
    } | ConvertTo-Json
} catch {
    Write-Output '{"Error":"Could not read brightness (may not be supported on this display)"}'
}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def set_brightness(level):
    """Set screen brightness (0-100)."""
    if not (0 <= level <= 100):
        return "ERROR: Brightness must be 0-100"
    script = f"""
try {{
    $delay = 0
    Get-CimInstance -Namespace root/WMI -ClassName WmiMonitorBrightnessMethods -ErrorAction Stop |
        WmiSetBrightness($delay, {level})
    Write-Output "OK: Brightness set to {level}%"
}} catch {{
    Write-Output "ERROR: Could not set brightness. Requires compatible display (laptop or DDC/CI monitor)."
}}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def get_display_info():
    """Get display adapter and resolution information."""
    script = r"""
Get-CimInstance Win32_VideoController | ForEach-Object {
    [PSCustomObject]@{
        Name = $_.Name
        Resolution = "$($_.CurrentHorizontalResolution)x$($_.CurrentVerticalResolution)"
        RefreshRate = $_.CurrentRefreshRate
        VRAM_MB = [math]::Round($_.AdapterRAM / 1MB, 0)
        DriverVersion = $_.DriverVersion
        Status = $_.Status
    }
} | ConvertTo-Json -Compress
"""
    stdout, _, _ = _run_ps(script)
    return stdout


# ========== Power Management ==========

def lock_screen():
    """Lock the workstation."""
    script = r"rundll32.exe user32.dll,LockWorkStation"
    _run_ps(script)
    return "OK: Screen locked"


def sleep_system():
    """Put the system to sleep."""
    script = r"""
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.Application]::SetSuspendState([System.Windows.Forms.PowerState]::Suspend, $false, $false)
Write-Output "OK: System entering sleep mode"
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def hibernate():
    """Hibernate the system."""
    script = r"""
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.Application]::SetSuspendState([System.Windows.Forms.PowerState]::Hibernate, $false, $false)
Write-Output "OK: System hibernating"
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def shutdown(delay_sec=60):
    """Schedule system shutdown."""
    script = f"""
shutdown /s /t {delay_sec} /c "Shutdown initiated by system-controller"
Write-Output "OK: System will shutdown in {delay_sec} seconds. Run 'shutdown /a' to cancel."
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def restart(delay_sec=60):
    """Schedule system restart."""
    script = f"""
shutdown /r /t {delay_sec} /c "Restart initiated by system-controller"
Write-Output "OK: System will restart in {delay_sec} seconds. Run 'shutdown /a' to cancel."
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def cancel_shutdown():
    """Cancel a scheduled shutdown/restart."""
    script = r"shutdown /a; Write-Output 'OK: Shutdown/restart cancelled'"
    stdout, _, _ = _run_ps(script)
    return stdout


# ========== Network ==========

def list_network_adapters():
    """List all network adapters with status."""
    script = r"""
Get-NetAdapter | Select-Object Name, InterfaceDescription, Status, LinkSpeed, MacAddress |
    ForEach-Object {
        [PSCustomObject]@{
            Name = $_.Name
            Description = $_.InterfaceDescription
            Status = $_.Status
            Speed = $_.LinkSpeed
            MAC = $_.MacAddress
        }
    } | ConvertTo-Json -Compress
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def enable_adapter(name):
    """Enable a network adapter."""
    escaped = name.replace("'", "''")
    script = f"""
try {{
    Enable-NetAdapter -Name '{escaped}' -Confirm:$false -ErrorAction Stop
    Write-Output "OK: Adapter '{name}' enabled"
}} catch {{
    Write-Output "ERROR: $($_.Exception.Message)"
}}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def disable_adapter(name):
    """Disable a network adapter."""
    escaped = name.replace("'", "''")
    script = f"""
try {{
    Disable-NetAdapter -Name '{escaped}' -Confirm:$false -ErrorAction Stop
    Write-Output "OK: Adapter '{name}' disabled"
}} catch {{
    Write-Output "ERROR: $($_.Exception.Message)"
}}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def list_wifi_networks():
    """List available WiFi networks."""
    script = r"""
try {
    netsh wlan show networks mode=bssid
} catch {
    Write-Output "ERROR: Could not scan WiFi networks."
}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def get_network_info():
    """Get current network configuration."""
    script = r"""
Get-NetIPConfiguration | ForEach-Object {
    [PSCustomObject]@{
        Interface = $_.InterfaceAlias
        IPv4 = if ($_.IPv4Address) { $_.IPv4Address.IPAddress -join ', ' } else { '' }
        IPv6 = if ($_.IPv6Address) { $_.IPv6Address.IPAddress -join ', ' } else { '' }
        DNS = if ($_.DNSServer) { $_.DNSServer.ServerAddresses -join ', ' } else { '' }
    }
} | ConvertTo-Json -Compress
"""
    stdout, _, _ = _run_ps(script)
    return stdout


# ========== USB / Device ==========

def list_usb_devices():
    """List connected USB devices."""
    script = r"""
Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -like 'USB\*' } |
    Select-Object FriendlyName, Status, Class, InstanceId |
    ForEach-Object {
        [PSCustomObject]@{
            Device = $_.FriendlyName
            Status = $_.Status
            Class = $_.Class
            InstanceId = $_.InstanceId
        }
    } | ConvertTo-Json -Compress
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Hardware Controller")
    sub = parser.add_subparsers(dest="category")

    # Volume
    p_vol = sub.add_parser("volume", help="Volume control")
    vol_sub = p_vol.add_subparsers(dest="action")
    vol_sub.add_parser("get", help="Get volume level")
    vol_set = vol_sub.add_parser("set", help="Set volume")
    vol_set.add_argument("--level", type=int, required=True, help="0-100")
    vol_sub.add_parser("mute", help="Toggle mute")

    # Screen
    p_scr = sub.add_parser("screen", help="Screen/display control")
    scr_sub = p_scr.add_subparsers(dest="action")
    scr_sub.add_parser("info", help="Get display info")
    bri_get = scr_sub.add_parser("brightness", help="Get/set brightness")
    bri_get.add_argument("--level", type=int, help="0-100")

    # Power
    p_pwr = sub.add_parser("power", help="Power management")
    pwr_sub = p_pwr.add_subparsers(dest="action")
    pwr_sub.add_parser("lock", help="Lock screen")
    pwr_sub.add_parser("sleep", help="Sleep mode")
    pwr_sub.add_parser("hibernate", help="Hibernate")
    pwr_sd = pwr_sub.add_parser("shutdown", help="Shutdown")
    pwr_sd.add_argument("--delay", type=int, default=60, help="Seconds")
    pwr_rs = pwr_sub.add_parser("restart", help="Restart")
    pwr_rs.add_argument("--delay", type=int, default=60, help="Seconds")
    pwr_sub.add_parser("cancel", help="Cancel scheduled shutdown")

    # Network
    p_net = sub.add_parser("network", help="Network control")
    net_sub = p_net.add_subparsers(dest="action")
    net_sub.add_parser("adapters", help="List network adapters")
    net_en = net_sub.add_parser("enable", help="Enable adapter")
    net_en.add_argument("--name", type=str, required=True)
    net_dis = net_sub.add_parser("disable", help="Disable adapter")
    net_dis.add_argument("--name", type=str, required=True)
    net_sub.add_parser("wifi", help="List WiFi networks")
    net_sub.add_parser("info", help="Get network config")

    # USB
    p_usb = sub.add_parser("usb", help="USB devices")
    usb_sub = p_usb.add_subparsers(dest="action")
    usb_sub.add_parser("list", help="List USB devices")

    args = parser.parse_args()

    if args.category == "volume":
        if args.action == "get":
            print(get_volume())
        elif args.action == "set":
            print(set_volume(args.level))
        elif args.action == "mute":
            print(toggle_mute())
        else:
            p_vol.print_help()
    elif args.category == "screen":
        if args.action == "info":
            print(get_display_info())
        elif args.action == "brightness":
            if args.level is not None:
                print(set_brightness(args.level))
            else:
                print(get_brightness())
        else:
            p_scr.print_help()
    elif args.category == "power":
        if args.action == "lock":
            print(lock_screen())
        elif args.action == "sleep":
            print(sleep_system())
        elif args.action == "hibernate":
            print(hibernate())
        elif args.action == "shutdown":
            print(shutdown(args.delay))
        elif args.action == "restart":
            print(restart(args.delay))
        elif args.action == "cancel":
            print(cancel_shutdown())
        else:
            p_pwr.print_help()
    elif args.category == "network":
        if args.action == "adapters":
            print(list_network_adapters())
        elif args.action == "enable":
            print(enable_adapter(args.name))
        elif args.action == "disable":
            print(disable_adapter(args.name))
        elif args.action == "wifi":
            print(list_wifi_networks())
        elif args.action == "info":
            print(get_network_info())
        else:
            p_net.print_help()
    elif args.category == "usb":
        if args.action == "list":
            print(list_usb_devices())
        else:
            p_usb.print_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

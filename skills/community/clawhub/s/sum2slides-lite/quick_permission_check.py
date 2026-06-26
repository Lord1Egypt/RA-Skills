"""
快速权限检测
"""

import os
import sys
import platform

def check_permissions():
    """快速检查权限"""
    print("🔐 Sum2Slides 权限快速检测")
    print("=" * 60)
    
    # 系统信息
    system = platform.system()
    print(f"系统: {system} ({platform.mac_ver()[0] if system == 'Darwin' else 'N/A'})")
    
    # 关键权限检查
    checks = []
    
    # 1. 文件系统权限
    desktop = os.path.expanduser("~/Desktop")
    can_write_desktop = os.access(desktop, os.W_OK)
    checks.append(("文件写入权限", can_write_desktop, "需要写入桌面目录"))
    
    # 2. Python包检查
    try:
        import pptx
        has_pptx = True
    except ImportError:
        has_pptx = False
    checks.append(("python-pptx", has_pptx, "运行: pip install python-pptx"))
    
    # 3. 网络权限（简单检查）
    try:
        import socket
        socket.create_connection(("open.feishu.cn", 443), timeout=3)
        has_network = True
    except:
        has_network = False
    checks.append(("网络连接", has_network, "需要访问飞书API"))
    
    # 4. AppleScript权限（macOS特有）
    if system == "Darwin":
        try:
            import subprocess
            result = subprocess.run(['osascript', '-e', 'tell application "System Events" to get name'], 
                                  capture_output=True, text=True, timeout=3)
            has_applescript = "not allowed" not in result.stderr
            checks.append(("AppleScript权限", has_applescript, 
                          "系统偏好设置 → 安全性与隐私 → 隐私 → 自动化"))
        except:
            checks.append(("AppleScript权限", False, 
                          "系统偏好设置 → 安全性与隐私 → 隐私 → 自动化"))
    
    # 5. 应用安装检查
    app_checks = []
    powerpoint_path = "/Applications/Microsoft PowerPoint.app"
    wps_path = "/Applications/wpsoffice.app"
    
    app_checks.append(("Microsoft PowerPoint", os.path.exists(powerpoint_path)))
    app_checks.append(("WPS Office", os.path.exists(wps_path)))
    
    # 打印结果
    print("\n📊 关键权限检查:")
    for name, passed, advice in checks:
        status = "✅" if passed else "❌"
        print(f"  {status} {name}: {'已具备' if passed else '未具备'}")
        if not passed:
            print(f"     建议: {advice}")
    
    print("\n🖥️ 应用安装检查:")
    for name, installed in app_checks:
        status = "✅" if installed else "⚠️"
        print(f"  {status} {name}: {'已安装' if installed else '未安装（可选）'}")
    
    # 功能可用性分析
    print("\n🚀 功能可用性分析:")
    
    can_generate = can_write_desktop and has_pptx
    can_upload = has_network
    has_ppt_app = os.path.exists(powerpoint_path) or os.path.exists(wps_path)
    
    print(f"  📄 PPTX文件生成: {'✅ 可用' if can_generate else '❌ 不可用'}")
    if can_generate:
        print("     可以使用python-pptx生成标准.pptx文件")
    
    print(f"  ☁️  文件上传: {'✅ 可用' if can_upload else '⚠️ 受限'}")
    if can_upload:
        print("     可以上传文件到飞书等平台")
    
    print(f"  🖥️  PPT软件: {'✅ 已安装' if has_ppt_app else '⚠️ 需要安装'}")
    if has_ppt_app:
        installed_apps = []
        if os.path.exists(powerpoint_path):
            installed_apps.append("PowerPoint")
        if os.path.exists(wps_path):
            installed_apps.append("WPS")
        print(f"     已安装: {', '.join(installed_apps)}")
    
    # 自动化权限警告
    if system == "Darwin":
        print("\n⚠️  AppleScript自动化权限（macOS特有）:")
        print("     需要用户手动授权才能自动化操作PPT软件")
        print("     授权路径: 系统偏好设置 → 安全性与隐私 → 隐私 → 自动化")
        print("     需要勾选: Microsoft PowerPoint, WPS Office, System Events")
    
    # 总结
    print("\n" + "=" * 60)
    print("💡 总结:")
    
    if can_generate:
        print("✅ 核心功能可用: 可以生成PPTX文件并保存到桌面")
        print("   即使没有自动化权限，也能使用标准.pptx格式")
    else:
        print("❌ 核心功能受限: 需要修复权限问题")
    
    if not has_pptx:
        print("\n🔧 立即修复:")
        print("   1. 安装python-pptx: pip install python-pptx")
        print("   2. 确保桌面目录可写")
    
    print("\n📋 完整授权指南:")
    print("   1. 文件系统: 确保~/Desktop目录可写")
    print("   2. 网络: 确保可以访问open.feishu.cn")
    print("   3. macOS: 授权AppleScript自动化权限")
    print("   4. 软件: 安装PowerPoint或WPS（可选）")


if __name__ == "__main__":
    check_permissions()
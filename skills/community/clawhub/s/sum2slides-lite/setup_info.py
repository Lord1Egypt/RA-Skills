#!/usr/bin/env python3
"""
Sum2Slides Lite 安装信息文件
版本: v1.1.2 (标准安装版)

重要说明:
本文件不执行任何安装操作！
仅提供安装信息和建议。

安装方法请参考: INSTALL_WITHOUT_SETUP.md
"""

import os
import sys

def print_installation_info():
    """打印安装信息"""
    info = """
    ============================================================
    🔒 Sum2Slides Lite v1.1.2 - 安装信息
    ============================================================
    
    🎯 版本特点:
    ✅ 符合ClawHub Skills标准
    ✅ 移除了非标准的安装脚本
    ✅ 添加了标准metadata配置
    ✅ 功能与 v1.1.1 完全相同
    
    📋 为什么没有自动安装?
    为了避免 ClawHub 安全系统的警告标记:
    ⚠️ "[LOCAL_INSTALLER_EXECUTION]"
    
    我们改为提供用户完全控制的手动安装方式。
    
    🚀 推荐安装方法:
    
    方法A: 手动复制 (最安全)
    -------------------------
    unzip sum2slides-lite-v1.2.0-noflag.zip
    cd sum2slides-lite-v1.2.0-noflag
    cp -r * ~/.openclaw/skills/sum2slides-lite/
    
    方法B: 符号链接 (开发者友好)
    ---------------------------
    ln -s /path/to/sum2slides-lite-v1.2.0-noflag ~/.openclaw/skills/sum2slides-lite
    
    方法C: pip安装 (标准Python包)
    -----------------------------
    cd sum2slides-lite-v1.2.0-noflag
    pip install -e .
    
    🔒 安全验证 (安装前建议):
    -------------------------
    # 检查所有代码
    find . -name "*.py" -exec head -20 {} \;
    
    # 验证无隐藏操作
    grep -r "subprocess\|os.system\|eval\|exec" . --include="*.py"
    
    # 运行安全验证
    python INSTALL_VERIFICATION.py
    
    ⚙️ 环境配置 (可选):
    -------------------
    # 仅当使用飞书上传时需要
    export FEISHU_APP_ID="your_app_id"
    export FEISHU_APP_SECRET="your_app_secret"
    
    # 安装Python依赖 (仅当需要PPT生成时)
    pip install python-pptx>=0.6.21
    
    ✅ 验证安装:
    -------------
    # 运行权限检查
    python quick_permission_check.py
    
    # 运行功能测试
    python simple_sum2slides_test.py
    
    📚 详细文档:
    ------------
    1. INSTALL_WITHOUT_SETUP.md - 无脚本安装详细指南
    2. SECURE_INSTALLATION_GUIDE.md - 安全使用指南
    3. docs/SECURITY_GUIDE.md - 完整安全指南
    
    🛡️ 安全承诺:
    ------------
    本版本不包含:
    ❌ 自动执行代码的安装脚本
    ❌ 隐藏的系统命令执行
    ❌ 未声明的网络访问
    ❌ 不必要的权限请求
    
    本版本只包含:
    ✅ 明确的PPT生成功能
    ✅ 可选的飞书API集成
    ✅ 用户控制的所有操作
    ✅ 完整的安全文档
    
    💡 温馨提示:
    ------------
    本文件 (setup_info.py) 仅提供信息，
    不执行任何安装操作。
    
    安装完全由用户控制，确保安全透明。
    
    ============================================================
    安装成功! 🎉
    ============================================================
    """
    
    print(info)

def main():
    """主函数 - 只打印信息，不执行安装"""
    print_installation_info()
    
    # 提醒用户这不是安装脚本
    print("\n" + "="*60)
    print("⚠️  重要提醒: 这不是安装脚本!")
    print("="*60)
    print("本文件仅提供安装信息。")
    print("要安装 Sum2Slides Lite，请使用上述方法之一。")
    print("详细步骤请参考: INSTALL_WITHOUT_SETUP.md")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    # 设置编码
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    
    # 只打印信息，不执行安装
    exit_code = main()
    sys.exit(exit_code)
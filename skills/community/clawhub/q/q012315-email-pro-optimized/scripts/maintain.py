#!/usr/bin/env python3
"""
Email Pro Optimized 技能维护脚本
自动检查和更新技能版本、依赖、文档等
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

SKILL_DIR = Path(__file__).parent.parent
SKILL_MD = SKILL_DIR / 'SKILL.md'
METADATA_FILE = SKILL_DIR / '.skill-metadata.json'

def get_version():
    """获取当前版本"""
    if METADATA_FILE.exists():
        with open(METADATA_FILE, 'r') as f:
            data = json.load(f)
            return data.get('version', '1.0.0')
    return '1.0.0'

def increment_version(version):
    """递增版本号"""
    parts = version.split('.')
    parts[-1] = str(int(parts[-1]) + 1)
    return '.'.join(parts)

def check_dependencies():
    """检查依赖"""
    print("🔍 检查依赖...")
    
    required_packages = ['requests']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️ 缺少依赖: {', '.join(missing)}")
        print("运行: pip install " + ' '.join(missing))
        return False
    
    return True

def check_scripts():
    """检查脚本文件"""
    print("\n🔍 检查脚本文件...")
    
    required_scripts = [
        'email-pro.py',
        'oauth_handler.py',
        'providers.py',
        'authorize.py',
        'analyze.py'
    ]
    
    scripts_dir = SKILL_DIR / 'scripts'
    all_exist = True
    
    for script in required_scripts:
        script_path = scripts_dir / script
        if script_path.exists():
            print(f"  ✅ {script}")
        else:
            print(f"  ❌ {script} - 缺失")
            all_exist = False
    
    return all_exist

def check_credentials():
    """检查凭证文件"""
    print("\n🔍 检查凭证文件...")
    
    creds_file = Path.home() / '.openclaw' / 'credentials' / 'oauth_tokens.json'
    
    if creds_file.exists():
        with open(creds_file, 'r') as f:
            creds = json.load(f)
        
        print(f"  ✅ OAuth tokens 文件存在")
        print(f"     账户数: {len(creds)}")
        
        for account_name, account_data in creds.items():
            provider = account_data.get('provider', 'unknown')
            print(f"     - {account_name} ({provider})")
        
        return True
    else:
        print(f"  ⚠️ OAuth tokens 文件不存在")
        return False

def update_metadata():
    """更新元数据"""
    print("\n📝 更新元数据...")
    
    current_version = get_version()
    new_version = increment_version(current_version)
    
    metadata = {
        'version': new_version,
        'last_updated': datetime.now().isoformat(),
        'features': [
            'QQ 邮箱支持 (IMAP/SMTP)',
            'Gmail OAuth 2.0 支持',
            'Outlook OAuth 2.0 支持',
            'OAuth 自动刷新',
            '并发邮件处理',
            '邮件搜索和分析'
        ],
        'oauth_auto_refresh': True,
        'performance': {
            'concurrent_threads': 5,
            'batch_size': 100
        }
    }
    
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"  ✅ 版本更新: {current_version} → {new_version}")
    print(f"  ✅ 元数据已保存")
    
    return new_version

def validate_oauth_handler():
    """验证 OAuth 处理器"""
    print("\n🔍 验证 OAuth 处理器...")
    
    oauth_file = SKILL_DIR / 'scripts' / 'oauth_handler.py'
    
    if not oauth_file.exists():
        print("  ❌ oauth_handler.py 不存在")
        return False
    
    with open(oauth_file, 'r') as f:
        content = f.read()
    
    required_functions = [
        'get_valid_token',
        'refresh_gmail_token_auto',
        'is_token_expired',
        'GmailOAuth',
        'OutlookOAuth'
    ]
    
    all_found = True
    for func in required_functions:
        if func in content:
            print(f"  ✅ {func}")
        else:
            print(f"  ❌ {func} - 缺失")
            all_found = False
    
    return all_found

def generate_report():
    """生成维护报告"""
    print("\n" + "=" * 70)
    print("📊 Email Pro Optimized 技能维护报告")
    print("=" * 70)
    
    checks = {
        '依赖检查': check_dependencies(),
        '脚本检查': check_scrip     '凭证检查': check_credentials(),
        'OAuth 处理器验证': validate_oauth_handler()
    }
    
    print("\n" + "=" * 70)
    print("✨ 维护总结")
    print("=" * 70)
    
    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    
    for check_name, result in checks.items():
        status = "✅ 通过" if result else "⚠️ 需要关注"
        print(f"{check_name}: {status}")
    
    print(f"\n总体状态: {passed}/{total} 检查通过")
    
    if passed == total:
        print("🎉 技能状态良好，无需维护")
        return True
    else:
        print("⚠️ 建议进行维护")
        return False

dein():
    """主函数"""
    print("🔧 Email Pro Optimized 技能维护\n")
    
    # 运行检查
    all_good = generate_report()
    
    # 更新元数据
    new_version = update_metadata()
    
    print("\n" + "=" * 70)
    print(f"✅ 维护完成 (版本: {new_version})")
    print("=" * 70)
    
    return 0 if all_good else 1

if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""
安装和配置代理自动检测技能
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def check_dependencies():
    """检查依赖"""
    print("🔍 检查系统依赖...")
    
    dependencies = {
        'python3': 'Python 3',
        'psutil': 'psutil 库',
        'requests': 'requests 库',
    }
    
    missing = []
    
    # 检查 Python 3
    try:
        subprocess.run(['python3', '--version'], capture_output=True, check=True)
        print("✅ Python 3 已安装")
    except:
        missing.append('python3')
        print("❌ Python 3 未安装")
    
    # 检查 Python 库
    try:
        import psutil
        print("✅ psutil 库已安装")
    except ImportError:
        missing.append('psutil')
        print("❌ psutil 库未安装")
    
    try:
        import requests
        print("✅ requests 库已安装")
    except ImportError:
        missing.append('requests')
        print("❌ requests 库未安装")
    
    return missing

def install_dependencies(missing_deps):
    """安装缺失的依赖"""
    if not missing_deps:
        return True
    
    print(f"\n📦 安装缺失的依赖: {', '.join(missing_deps)}")
    
    for dep in missing_deps:
        if dep == 'python3':
            print("请手动安装 Python 3")
            return False
        elif dep in ['psutil', 'requests']:
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', dep], 
                             check=True, capture_output=True)
                print(f"✅ 已安装 {dep}")
            except subprocess.CalledProcessError as e:
                print(f"❌ 安装 {dep} 失败: {e}")
                return False
    
    return True

def setup_skill_files():
    """设置技能文件"""
    print("\n📁 设置技能文件...")
    
    # 获取当前脚本目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(current_dir)
    
    # 确保脚本可执行
    scripts = ['proxy_detector.py', 'gateway_proxy_setup.py', 'install_proxy_skill.py']
    
    for script in scripts:
        script_path = os.path.join(current_dir, script)
        if os.path.exists(script_path):
            os.chmod(script_path, 0o755)
            print(f"✅ 设置可执行权限: {script}")
    
    return skill_dir

def create_cron_job():
    """创建定时任务检查代理"""
    print("\n⏰ 创建定时任务...")
    
    cron_content = """# OpenClaw 代理自动检查
# 每小时检查一次代理状态
0 * * * * cd ~/.openclaw/workspace/skills/proxy-auto-config && python3 scripts/proxy_detector.py --configure --output ~/.openclaw/proxy_config >> ~/.openclaw/logs/proxy_check.log 2>&1

# Gateway 启动时检查代理
@reboot cd ~/.openclaw/workspace/skills/proxy-auto-config && python3 scripts/gateway_proxy_setup.py >> ~/.openclaw/logs/gateway_proxy_setup.log 2>&1
"""
    
    cron_file = os.path.expanduser("~/.openclaw/proxy_cron")
    try:
        with open(cron_file, 'w') as f:
            f.write(cron_content)
        
        # 添加到 crontab
        subprocess.run(['crontab', cron_file], check=True, capture_output=True)
        print(f"✅ 定时任务已创建: {cron_file}")
        return True
    except Exception as e:
        print(f"⚠️  创建定时任务失败: {e}")
        print("请手动添加以下内容到 crontab:")
        print(cron_content)
        return False

def create_gateway_hook():
    """创建 Gateway 启动钩子"""
    print("\n🔗 创建 Gateway 启动钩子...")
    
    hook_content = """#!/bin/bash
# OpenClaw Gateway 代理自动配置钩子
# 在 Gateway 启动前自动配置代理

OPENCLAW_DIR="$HOME/.openclaw"
PROXY_SKILL_DIR="$HOME/.openclaw/workspace/skills/proxy-auto-config"

# 检查代理技能是否存在
if [ -f "$PROXY_SKILL_DIR/scripts/gateway_proxy_setup.py" ]; then
    echo "[$(date)] 检测到代理技能，自动配置代理..."
    
    # 运行代理配置
    cd "$PROXY_SKILL_DIR" && python3 scripts/gateway_proxy_setup.py --config-dir "$OPENCLAW_DIR"
    
    # 应用代理配置
    if [ -f "$OPENCLAW_DIR/proxy_config/configure_proxy.sh" ]; then
        source "$OPENCLAW_DIR/proxy_config/configure_proxy.sh"
    fi
else
    echo "[$(date)] 未找到代理技能，跳过代理配置"
fi

# 继续执行原始命令
exec "$@"
"""
    
    hook_file = os.path.expanduser("~/.openclaw/gateway_proxy_hook.sh")
    try:
        with open(hook_file, 'w') as f:
            f.write(hook_content)
        
        os.chmod(hook_file, 0o755)
        print(f"✅ Gateway 钩子已创建: {hook_file}")
        
        # 创建包装脚本
        wrapper_content = f"""#!/bin/bash
# OpenClaw Gateway 代理包装脚本
source {hook_file}
openclaw gateway "$@"
"""
        
        wrapper_file = os.path.expanduser("~/.local/bin/openclaw-proxy")
        os.makedirs(os.path.dirname(wrapper_file), exist_ok=True)
        
        with open(wrapper_file, 'w') as f:
            f.write(wrapper_content)
        
        os.chmod(wrapper_file, 0o755)
        print(f"✅ 包装脚本已创建: {wrapper_file}")
        
        return True
    except Exception as e:
        print(f"⚠️  创建 Gateway 钩子失败: {e}")
        return False

def create_systemd_integration():
    """创建 systemd 集成"""
    print("\n🔧 创建 systemd 集成...")
    
    # 检查是否支持 systemd
    try:
        subprocess.run(['systemctl', '--version'], capture_output=True, check=True)
    except:
        print("⚠️  systemd 不可用，跳过 systemd 集成")
        return False
    
    # 创建 systemd 服务目录
    systemd_user_dir = os.path.expanduser("~/.config/systemd/user")
    os.makedirs(systemd_user_dir, exist_ok=True)
    
    # 创建代理检查服务
    proxy_check_service = f"""[Unit]
Description=OpenClaw Proxy Auto Check
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 {os.path.expanduser('~/.openclaw/workspace/skills/proxy-auto-config/scripts/proxy_detector.py')} --configure --output {os.path.expanduser('~/.openclaw/proxy_config')}
User={os.getenv('USER')}

[Install]
WantedBy=default.target
"""
    
    proxy_check_timer = f"""[Unit]
Description=OpenClaw Proxy Auto Check Timer

[Timer]
OnBootSec=5min
OnUnitActiveSec=1hour

[Install]
WantedBy=timers.target
"""
    
    try:
        # 写入服务文件
        service_file = os.path.join(systemd_user_dir, "openclaw-proxy-check.service")
        with open(service_file, 'w') as f:
            f.write(proxy_check_service)
        
        # 写入定时器文件
        timer_file = os.path.join(systemd_user_dir, "openclaw-proxy-check.timer")
        with open(timer_file, 'w') as f:
            f.write(proxy_check_timer)
        
        print(f"✅ systemd 服务文件已创建:")
        print(f"   服务: {service_file}")
        print(f"   定时器: {timer_file}")
        
        # 启用定时器
        subprocess.run(['systemctl', '--user', 'enable', 'openclaw-proxy-check.timer'], 
                      capture_output=True)
        subprocess.run(['systemctl', '--user', 'start', 'openclaw-proxy-check.timer'], 
                      capture_output=True)
        
        print("✅ systemd 定时器已启用")
        return True
    except Exception as e:
        print(f"⚠️  创建 systemd 集成失败: {e}")
        return False

def create_usage_guide(skill_dir):
    """创建使用指南"""
    print("\n📖 创建使用指南...")
    
    guide_content = f"""# OpenClaw 代理自动配置技能使用指南

## 技能位置
{skill_dir}

## 主要脚本
1. `scripts/proxy_detector.py` - 代理检测和配置
2. `scripts/gateway_proxy_setup.py` - Gateway 代理设置
3. `scripts/install_proxy_skill.py` - 安装脚本

## 使用方法

### 1. 手动检测代理
```bash
cd {skill_dir}
python3 scripts/proxy_detector.py --configure
```

### 2. 配置 Gateway 代理
```bash
cd {skill_dir}
python3 scripts/gateway_proxy_setup.py
```

### 3. 使用包装脚本启动 Gateway
```bash
# 使用代理启动 Gateway
~/.local/bin/openclaw-proxy start

# 或直接使用
openclaw-proxy start
```

### 4. 测试代理连接
```bash
cd {skill_dir}
python3 scripts/proxy_detector.py --test --configure
```

## 自动配置

### 定时检查
- 每小时自动检查代理状态
- 配置保存在: ~/.openclaw/proxy_config/

### Gateway 启动钩子
- Gateway 启动前自动配置代理
- 钩子脚本: ~/.openclaw/gateway_proxy_hook.sh

### systemd 集成（如果可用）
- 服务: openclaw-proxy-check.service
- 定时器: openclaw-proxy-check.timer

## 配置文件
- Gateway 配置: ~/.openclaw/gateway.json
- 代理配置: ~/.openclaw/proxy_config/
- 日志文件: ~/.openclaw/logs/

## 故障排除

### 1. 代理检测失败
```bash
# 查看详细日志
cd {skill_dir}
python3 scripts/proxy_detector.py --verbose
```

### 2. Gateway 启动失败
```bash
# 检查 Gateway 配置
cat ~/.openclaw/gateway.json | jq '.plugins["http-proxy"]'
```

### 3. 网络连接问题
```bash
# 测试代理连接
curl --socks5 127.0.0.1:10808 http://httpbin.org/ip
```

## 更新技能
```bash
cd {skill_dir}
git pull origin main  # 如果使用 git
# 或重新运行安装脚本
python3 scripts/install_proxy_skill.py
```

## 支持
如有问题，请检查日志文件:
- ~/.openclaw/logs/proxy_setup.log
- ~/.openclaw/logs/proxy_check.log
- ~/.openclaw/logs/gateway_proxy_setup.log
"""
    
    guide_file = os.path.join(skill_dir, "USAGE_GUIDE.md")
    try:
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        print(f"✅ 使用指南已创建: {guide_file}")
        return guide_file
    except Exception as e:
        print(f"⚠️  创建使用指南失败: {e}")
        return None

def main():
    """主安装函数"""
    print("=" * 60)
    print("OpenClaw 代理自动配置技能安装")
    print("=" * 60)
    
    # 检查依赖
    missing_deps = check_dependencies()
    
    # 安装依赖
    if missing_deps:
        if not install_dependencies(missing_deps):
            print("\n❌ 依赖安装失败，请手动安装缺失的依赖")
            return 1
    
    # 设置技能文件
    skill_dir = setup_skill_files()
    
    # 创建定时任务
    create_cron_job()
    
    # 创建 Gateway 钩子
    create_gateway_hook()
    
    # 创建 systemd 集成
    create_systemd_integration()
    
    # 创建使用指南
    guide_file = create_usage_guide(skill_dir)
    
    print("\n" + "=" * 60)
    print("🎉 安装完成！")
    print("=" * 60)
    
    print("\n📋 安装摘要:")
    print(f"   技能目录: {skill_dir}")
    print(f"   主要脚本: scripts/proxy_detector.py")
    print(f"   Gateway 钩子: ~/.openclaw/gateway_proxy_hook.sh")
    print(f"   包装脚本: ~/.local/bin/openclaw-proxy")
    
    if guide_file:
        print(f"   使用指南: {guide_file}")
    
    print("\n🚀 下一步:")
    print("   1. 测试代理检测: python3 scripts/proxy_detector.py --configure")
    print("   2. 配置 Gateway: python3 scripts/gateway_proxy_setup.py")
    print("   3. 使用代理启动 Gateway: openclaw-proxy start")
    
    print("\n💡 提示:")
    print("   所有配置和日志保存在 ~/.openclaw/ 目录下")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n安装被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n安装过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
#!/usr/bin/env python3
"""
简化的代理检测脚本
不依赖外部库
"""

"""
⚠️ 安全警告：
1. 此脚本会检测系统代理配置
2. 不要硬编码敏感信息（API密钥、密码等）
3. 使用环境变量或配置文件存储敏感信息
4. 发布的代码中只包含示例和占位符
"""

import os
import sys
import re
import json
import subprocess
import socket

def check_env_proxies():
    """检查环境变量中的代理"""
    proxies = []
    env_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'http_proxy', 'https_proxy', 'all_proxy']
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ 环境变量 {var}: {value}")
            proxies.append({
                'type': 'environment',
                'variable': var,
                'url': value
            })
    
    return proxies

def check_listening_ports():
    """检查监听端口"""
    proxies = []
    
    # 常见代理端口
    common_ports = [10808, 1080, 1081, 1082, 7890, 7891, 8118, 9050, 8080, 8888]
    
    print("\n🔍 检查代理端口...")
    
    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            
            if result == 0:
                print(f"✅ 端口 {port} 正在监听")
                proxies.append({
                    'type': 'port',
                    'port': port,
                    'status': 'listening'
                })
        except:
            pass
    
    return proxies

def check_v2ray_process():
    """检查 v2ray 进程"""
    print("\n🔍 检查 v2ray 进程...")
    
    try:
        # 使用 ps 命令检查进程
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        
        v2ray_keywords = ['v2ray', 'xray', 'v2rayN']
        for line in result.stdout.split('\n'):
            for keyword in v2ray_keywords:
                if keyword in line.lower():
                    print(f"✅ 发现 {keyword} 进程: {line[:80]}...")
                    return [{
                        'type': 'process',
                        'name': keyword,
                        'line': line.strip()
                    }]
    except:
        pass
    
    return []

def check_current_proxy():
    """检查当前代理配置"""
    print("\n" + "=" * 60)
    print("当前代理配置检查")
    print("=" * 60)
    
    all_proxies = []
    
    # 1. 检查环境变量
    env_proxies = check_env_proxies()
    all_proxies.extend(env_proxies)
    
    # 2. 检查端口
    port_proxies = check_listening_ports()
    all_proxies.extend(port_proxies)
    
    # 3. 检查进程
    process_proxies = check_v2ray_process()
    all_proxies.extend(process_proxies)
    
    # 总结
    print("\n" + "=" * 60)
    print("配置总结")
    print("=" * 60)
    
    if all_proxies:
        print(f"✅ 发现 {len(all_proxies)} 个代理配置")
        
        # 选择最佳代理
        best_proxy = None
        
        # 优先使用环境变量
        for proxy in all_proxies:
            if proxy['type'] == 'environment':
                best_proxy = proxy
                break
        
        # 其次使用端口
        if not best_proxy:
            for proxy in all_proxies:
                if proxy['type'] == 'port':
                    best_proxy = proxy
                    break
        
        if best_proxy:
            print(f"\n🎯 最佳代理配置: {best_proxy['type']}")
            
            proxy_url = None
            if 'url' in best_proxy:
                proxy_url = best_proxy['url']
            elif 'port' in best_proxy:
                proxy_url = f"socks5://127.0.0.1:{best_proxy['port']}"
            
            if proxy_url:
                print(f"🔗 代理URL: {proxy_url}")
                
                # 生成配置脚本
                generate_config_script(proxy_url)
                
                return proxy_url
    
    else:
        print("❌ 未发现代理配置")
    
    return None

def generate_config_script(proxy_url):
    """生成配置脚本"""
    print("\n⚙️  生成代理配置...")
    
    script_content = f"""#!/bin/bash
# OpenClaw 代理配置脚本
# 自动生成

# 清除现有代理设置
unset HTTP_PROXY
unset HTTPS_PROXY
unset ALL_PROXY
unset http_proxy
unset https_proxy
unset all_proxy

# 设置代理
export HTTP_PROXY="{proxy_url}"
export HTTPS_PROXY="{proxy_url}"
export ALL_PROXY="{proxy_url}"

# 对于 Python
export REQUESTS_CA_BUNDLE=""

echo "✅ 代理已配置: {proxy_url}"
echo "💡 使用: source 此脚本应用配置"
"""
    
    # 保存脚本
    config_dir = os.path.expanduser("~/.openclaw/proxy_config")
    os.makedirs(config_dir, exist_ok=True)
    
    script_path = os.path.join(config_dir, "configure_proxy.sh")
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    os.chmod(script_path, 0o755)
    
    print(f"📁 配置脚本: {script_path}")
    print(f"📋 使用方法: source {script_path}")
    
    # 创建 Gateway 配置
    create_gateway_config(proxy_url, config_dir)

def create_gateway_config(proxy_url, config_dir):
    """创建 Gateway 配置"""
    print("\n🔧 创建 Gateway 配置...")
    
    # 解析代理类型
    proxy_type = "socks5"
    if proxy_url.startswith("http://"):
        proxy_type = "http"
    elif proxy_url.startswith("https://"):
        proxy_type = "https"
    
    # Gateway 配置
    gateway_config = {
        "plugins": {
            "http-proxy": {
                "enabled": True,
                "config": {
                    "protocol": proxy_type,
                    f"{proxy_type}Proxy": proxy_url
                }
            }
        }
    }
    
    config_path = os.path.join(config_dir, "gateway_proxy.json")
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(gateway_config, f, indent=2, ensure_ascii=False)
    
    print(f"📁 Gateway 配置: {config_path}")
    
    # 使用说明
    print("\n🚀 使用说明:")
    print(f"1. 应用代理: source {os.path.join(config_dir, 'configure_proxy.sh')}")
    print(f"2. 启动 Gateway: HTTP_PROXY={proxy_url} openclaw gateway start")
    print(f"3. 或合并配置到 gateway.json")

def main():
    """主函数"""
    print("=" * 60)
    print("OpenClaw 代理自动检测")
    print("=" * 60)
    
    proxy_url = check_current_proxy()
    
    if proxy_url:
        print("\n🎉 代理配置完成！")
        print(f"\n下一步:")
        print(f"1. 应用配置: source ~/.openclaw/proxy_config/configure_proxy.sh")
        print(f"2. 测试连接: curl --socks5 127.0.0.1:10808 http://httpbin.org/ip")
        print(f"3. 启动 Gateway: HTTP_PROXY={proxy_url} openclaw gateway start")
    else:
        print("\n⚠️  未配置代理")
        print("建议:")
        print("1. 启动 v2rayN 或其他代理工具")
        print("2. 设置环境变量: export HTTP_PROXY=socks5://127.0.0.1:10808")
        print("3. 重新运行此脚本")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
OpenClaw Gateway 代理自动配置
在 Gateway 启动时自动检测和配置代理
"""

import os
import sys
import json
import logging
from pathlib import Path

# 添加父目录到路径，以便导入 proxy_detector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from proxy_detector import ProxyDetector
except ImportError:
    # 如果导入失败，尝试相对导入
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "proxy_detector", 
        os.path.join(os.path.dirname(__file__), "proxy_detector.py")
    )
    proxy_detector_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(proxy_detector_module)
    ProxyDetector = proxy_detector_module.ProxyDetector

class GatewayProxySetup:
    """Gateway 代理设置类"""
    
    def __init__(self, config_dir=None):
        self.config_dir = config_dir or os.path.expanduser("~/.openclaw")
        self.gateway_config_path = os.path.join(self.config_dir, "gateway.json")
        self.proxy_config_path = os.path.join(self.config_dir, "proxy_config.json")
        self.logger = self._setup_logging()
        
    def _setup_logging(self):
        """设置日志"""
        log_dir = os.path.join(self.config_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(log_dir, "proxy_setup.log")),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def load_gateway_config(self):
        """加载 Gateway 配置"""
        try:
            if os.path.exists(self.gateway_config_path):
                with open(self.gateway_config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            self.logger.error(f"加载 Gateway 配置失败: {e}")
            return {}
    
    def save_gateway_config(self, config):
        """保存 Gateway 配置"""
        try:
            os.makedirs(os.path.dirname(self.gateway_config_path), exist_ok=True)
            with open(self.gateway_config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Gateway 配置已保存: {self.gateway_config_path}")
            return True
        except Exception as e:
            self.logger.error(f"保存 Gateway 配置失败: {e}")
            return False
    
    def update_gateway_proxy_config(self, proxy_url):
        """更新 Gateway 代理配置"""
        config = self.load_gateway_config()
        
        # 确保有 plugins 配置
        if 'plugins' not in config:
            config['plugins'] = {}
        
        # 添加或更新代理配置
        if 'http-proxy' not in config['plugins']:
            config['plugins']['http-proxy'] = {
                'enabled': True,
                'config': {}
            }
        
        # 解析代理URL
        if proxy_url.startswith('socks5://'):
            config['plugins']['http-proxy']['config']['socksProxy'] = proxy_url
            config['plugins']['http-proxy']['config']['protocol'] = 'socks5'
        elif proxy_url.startswith('http://'):
            config['plugins']['http-proxy']['config']['httpProxy'] = proxy_url
            config['plugins']['http-proxy']['config']['protocol'] = 'http'
        elif proxy_url.startswith('https://'):
            config['plugins']['http-proxy']['config']['httpsProxy'] = proxy_url
            config['plugins']['http-proxy']['config']['protocol'] = 'https'
        
        self.logger.info(f"更新 Gateway 代理配置: {proxy_url}")
        return self.save_gateway_config(config)
    
    def setup_environment_proxies(self, proxy_url):
        """设置环境变量代理"""
        try:
            os.environ['HTTP_PROXY'] = proxy_url
            os.environ['HTTPS_PROXY'] = proxy_url
            os.environ['ALL_PROXY'] = proxy_url
            
            # 对于 Node.js 和 npm
            os.environ['NODE_TLS_REJECT_UNAUTHORIZED'] = '0'
            
            self.logger.info(f"环境变量已设置: HTTP_PROXY={proxy_url}")
            return True
        except Exception as e:
            self.logger.error(f"设置环境变量失败: {e}")
            return False
    
    def create_startup_script(self, proxy_url):
        """创建启动脚本"""
        script_content = f"""#!/bin/bash
# OpenClaw Gateway 代理启动脚本
# 自动生成于: $(date)

# 设置代理环境变量
export HTTP_PROXY="{proxy_url}"
export HTTPS_PROXY="{proxy_url}"
export ALL_PROXY="{proxy_url}"

# Node.js 设置
export NODE_TLS_REJECT_UNAUTHORIZED="0"

# 启动 OpenClaw Gateway
echo "使用代理启动 OpenClaw Gateway: {proxy_url}"
exec openclaw gateway start "$@"
"""
        
        script_path = os.path.join(self.config_dir, "start_gateway_with_proxy.sh")
        try:
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            os.chmod(script_path, 0o755)
            self.logger.info(f"启动脚本已创建: {script_path}")
            return script_path
        except Exception as e:
            self.logger.error(f"创建启动脚本失败: {e}")
            return None
    
    def create_systemd_service(self, proxy_url):
        """创建 systemd 服务文件（如果可用）"""
        service_content = f"""[Unit]
Description=OpenClaw Gateway with Proxy
After=network.target

[Service]
Type=simple
User={os.getenv('USER', 'openclaw')}
Environment="HTTP_PROXY={proxy_url}"
Environment="HTTPS_PROXY={proxy_url}"
Environment="ALL_PROXY={proxy_url}"
Environment="NODE_TLS_REJECT_UNAUTHORIZED=0"
WorkingDirectory={self.config_dir}
ExecStart=/usr/bin/openclaw gateway start
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
        
        service_path = os.path.expanduser("~/.config/systemd/user/openclaw-gateway-proxy.service")
        try:
            os.makedirs(os.path.dirname(service_path), exist_ok=True)
            with open(service_path, 'w', encoding='utf-8') as f:
                f.write(service_content)
            
            self.logger.info(f"systemd 服务文件已创建: {service_path}")
            return service_path
        except Exception as e:
            self.logger.warning(f"创建 systemd 服务文件失败: {e}")
            return None
    
    def run(self):
        """运行代理设置"""
        self.logger.info("=" * 60)
        self.logger.info("OpenClaw Gateway 代理自动配置")
        self.logger.info("=" * 60)
        
        # 检测代理
        detector = ProxyDetector()
        proxies = detector.detect_all_proxies()
        
        if not proxies:
            self.logger.warning("未检测到任何代理配置，将使用直连模式")
            return False
        
        self.logger.info(f"检测到 {len(proxies)} 个代理配置")
        
        # 选择最佳代理
        best_proxy = detector.select_best_proxy()
        if not best_proxy:
            self.logger.warning("无法选择最佳代理配置")
            return False
        
        # 获取代理URL
        proxy_url = best_proxy.get('url')
        if not proxy_url and best_proxy.get('port'):
            proxy_url = f"socks5://127.0.0.1:{best_proxy['port']}"
        
        if not proxy_url:
            self.logger.warning("无法获取代理URL")
            return False
        
        self.logger.info(f"选择代理: {proxy_url}")
        
        # 1. 设置环境变量
        self.setup_environment_proxies(proxy_url)
        
        # 2. 更新 Gateway 配置
        self.update_gateway_proxy_config(proxy_url)
        
        # 3. 创建启动脚本
        script_path = self.create_startup_script(proxy_url)
        
        # 4. 尝试创建 systemd 服务
        service_path = self.create_systemd_service(proxy_url)
        
        # 5. 保存代理配置
        saved_files = detector.save_configuration(
            os.path.join(self.config_dir, "proxy_config")
        )
        
        self.logger.info("=" * 60)
        self.logger.info("🎉 代理配置完成！")
        self.logger.info("=" * 60)
        
        summary = {
            'proxy_url': proxy_url,
            'proxy_source': best_proxy.get('type', 'unknown'),
            'gateway_config': self.gateway_config_path,
            'startup_script': script_path,
            'systemd_service': service_path,
            'config_files': saved_files
        }
        
        # 打印使用说明
        print("\n📋 配置摘要:")
        print(f"   代理URL: {proxy_url}")
        print(f"   来源: {best_proxy.get('type', 'unknown')}")
        print(f"   Gateway配置: {self.gateway_config_path}")
        
        if script_path:
            print(f"\n🚀 启动 Gateway 的方法:")
            print(f"   1. 使用启动脚本: {script_path}")
            print(f"   2. 或直接运行: HTTP_PROXY={proxy_url} openclaw gateway start")
        
        if service_path:
            print(f"\n🔧 systemd 服务:")
            print(f"   服务文件: {service_path}")
            print(f"   启用服务: systemctl --user enable openclaw-gateway-proxy")
            print(f"   启动服务: systemctl --user start openclaw-gateway-proxy")
        
        print(f"\n📁 配置文件:")
        print(f"   代理配置: {saved_files['json_config']}")
        print(f"   Bash脚本: {saved_files['bash_script']}")
        
        print(f"\n💡 提示:")
        print(f"   要应用环境变量，请运行: source {saved_files['bash_script']}")
        
        return summary


def main():
    """命令行入口点"""
    import argparse
    
    parser = argparse.ArgumentParser(description='OpenClaw Gateway 代理自动配置')
    parser.add_argument('--config-dir', help='OpenClaw 配置目录', default=None)
    parser.add_argument('--no-gateway-config', action='store_true', help='不更新 Gateway 配置')
    parser.add_argument('--no-startup-script', action='store_true', help='不创建启动脚本')
    parser.add_argument('--verbose', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    setup = GatewayProxySetup(config_dir=args.config_dir)
    result = setup.run()
    
    if result:
        print("\n✅ 代理配置成功完成！")
        return 0
    else:
        print("\n❌ 代理配置失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
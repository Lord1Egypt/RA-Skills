# -*- coding: utf-8 -*-
"""
SkillPilot - 智能技能路由引擎
环境探测模块

自动检测网络特性和技能可用性，为路由决策提供环境上下文
"""

import os
import time
import json
import socket
import subprocess
from typing import Dict, List, Optional
from pathlib import Path


class EnvironmentProbe:
    """环境探测"""
    
    def __init__(self, cache_file: str = None):
        self.cache_file = cache_file or os.path.expanduser("~/.openclaw/workspace/skills/skill-pilot/env_cache.json")
        self.network_profile: Dict = {}
        self.skill_availability: Dict = {}
        self.last_probe_time: float = 0
        self.cache_ttl = 3600  # 缓存 1 小时
    
    def load_cache(self) -> bool:
        """加载缓存"""
        if not os.path.exists(self.cache_file):
            return False
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
            
            # 检查缓存是否过期
            if time.time() - cache.get('timestamp', 0) > self.cache_ttl:
                return False
            
            self.network_profile = cache.get('network_profile', {})
            self.skill_availability = cache.get('skill_availability', {})
            self.last_probe_time = cache.get('timestamp', 0)
            return True
        except Exception as e:
            print(f"加载环境缓存失败：{e}")
            return False
    
    def save_cache(self):
        """保存缓存"""
        cache = {
            'timestamp': time.time(),
            'network_profile': self.network_profile,
            'skill_availability': self.skill_availability,
        }
        
        try:
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存环境缓存失败：{e}")
    
    def probe_all(self, skills: List[str] = None) -> Dict:
        """执行完整环境探测"""
        print("🔍 开始环境探测...")
        
        # 1. 网络特性探测
        print("  → 探测网络环境...")
        self.network_profile = self.probe_network()
        
        # 2. 技能可用性探测
        if skills:
            print(f"  → 探测 {len(skills)} 个技能可用性...")
            self.skill_availability = self.probe_skills(skills)
        
        # 3. 保存缓存
        self.save_cache()
        
        # 4. 返回最优配置建议
        profile = self.get_optimal_profile()
        print(f"  ✓ 推荐配置：{profile['name']}")
        
        return {
            'network': self.network_profile,
            'skills': self.skill_availability,
            'recommended_profile': profile,
            'probed_at': time.time(),
        }
    
    def probe_network(self) -> Dict:
        """探测网络特性"""
        profile = {
            'region': self._detect_region(),
            'proxy_enabled': self._detect_proxy(),
            'ipv6_available': self._check_ipv6(),
            'dns_speed': self._measure_dns_speed(),
        }
        
        # 根据区域测量延迟
        if profile['region'] == 'cn':
            profile['latency_cn'] = self._ping_host('www.baidu.com')
            profile['latency_us'] = self._ping_host('www.google.com', timeout=2)
        else:
            profile['latency_us'] = self._ping_host('www.google.com')
            profile['latency_cn'] = self._ping_host('www.baidu.com', timeout=2)
        
        return profile
    
    def _detect_region(self) -> str:
        """检测地理区域"""
        # 方法 1: 检查 IP (简化版，实际可用 API)
        # 方法 2: 检查系统时区
        import datetime
        tz_offset = datetime.datetime.now().astimezone().utcoffset()
        if tz_offset:
            hours = tz_offset.total_seconds() / 3600
            if 7 <= hours <= 9:  # UTC+7 ~ UTC+9
                return 'cn'  # 亚洲时区
        
        # 方法 3: DNS 解析速度
        cn_speed = self._measure_dns_speed('www.baidu.com')
        us_speed = self._measure_dns_speed('www.google.com')
        
        if cn_speed < us_speed * 0.5:  # 国内 DNS 快很多
            return 'cn'
        elif us_speed < cn_speed * 0.5:  # 国外 DNS 快很多
            return 'us'
        
        return 'unknown'
    
    def _detect_proxy(self) -> bool:
        """检测是否启用代理"""
        proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']
        if any(os.getenv(var) for var in proxy_vars):
            return True
        
        # 检查常见代理端口
        proxy_ports = [8080, 8888, 1080, 7890]
        for port in proxy_ports:
            if self._check_port_open('127.0.0.1', port):
                return True
        
        return False
    
    def _check_ipv6(self) -> bool:
        """检查 IPv6 支持"""
        try:
            socket.getaddrinfo('ipv6.google.com', 80, socket.AF_INET6)
            return True
        except:
            return False
    
    def _measure_dns_speed(self, host: str = 'www.baidu.com') -> float:
        """测量 DNS 解析速度 (ms)"""
        try:
            start = time.time()
            socket.gethostbyname(host)
            return (time.time() - start) * 1000
        except:
            return float('inf')
    
    def _ping_host(self, host: str, timeout: int = 5) -> float:
        """测量到主机的延迟 (ms)"""
        try:
            # 使用 TCP 连接测试 (比 ICMP 更可靠)
            start = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, 80))
            sock.close()
            return (time.time() - start) * 1000
        except:
            return float('inf')
    
    def _check_port_open(self, host: str, port: int) -> bool:
        """检查端口是否开放"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def probe_skills(self, skills: List[str]) -> Dict:
        """探测技能可用性"""
        results = {}
        
        for skill_name in skills:
            # 简化探测：检查技能目录是否存在
            skill_dir = os.path.expanduser(f"~/.openclaw/workspace/skills/{skill_name}")
            available = os.path.isdir(skill_dir)
            
            results[skill_name] = {
                'available': available,
                'latency_ms': 0,  # 待实际调用时测量
                'last_checked': time.time(),
            }
        
        return results
    
    def get_optimal_profile(self) -> Dict:
        """获取最优配置模板"""
        region = self.network_profile.get('region', 'unknown')
        proxy = self.network_profile.get('proxy_enabled', False)
        
        if region == 'cn' and not proxy:
            return {
                'name': 'cn-no-proxy',
                'description': '中国大陆无代理环境',
                'preferred_capabilities': ['chinese', 'free'],
                'fallback_order': ['cn-engine', 'global-engine'],
                'timeout_multiplier': 1.5,  # 国内网络可能不稳定，增加超时
            }
        elif region == 'cn' and proxy:
            return {
                'name': 'cn-with-proxy',
                'description': '中国大陆有代理环境',
                'preferred_capabilities': ['fast', 'accurate'],
                'fallback_order': ['fast-engine', 'reliable-engine'],
                'timeout_multiplier': 1.0,
            }
        else:
            return {
                'name': 'global',
                'description': '海外环境',
                'preferred_capabilities': ['global', 'accurate'],
                'fallback_order': ['global-engine', 'backup-engine'],
                'timeout_multiplier': 1.0,
            }
    
    def get_profile_config(self, profile_name: str = None) -> Dict:
        """获取指定配置模板"""
        profiles = {
            'cn-no-proxy': {
                'name': 'cn-no-proxy',
                'description': '中国大陆无代理环境',
                'routing': {
                    'preferred_capabilities': ['chinese', 'free'],
                    'avoid_capabilities': [],
                },
                'timeout': {
                    'search': 45,
                    'fetch': 60,
                    'summarize': 30,
                },
                'max_fallback': 3,
            },
            'cn-with-proxy': {
                'name': 'cn-with-proxy',
                'description': '中国大陆有代理环境',
                'routing': {
                    'preferred_capabilities': ['fast', 'accurate'],
                    'avoid_capabilities': [],
                },
                'timeout': {
                    'search': 30,
                    'fetch': 45,
                    'summarize': 30,
                },
                'max_fallback': 3,
            },
            'global': {
                'name': 'global',
                'description': '海外环境',
                'routing': {
                    'preferred_capabilities': ['global', 'accurate'],
                    'avoid_capabilities': [],
                },
                'timeout': {
                    'search': 30,
                    'fetch': 30,
                    'summarize': 30,
                },
                'max_fallback': 3,
            },
        }
        
        if profile_name:
            return profiles.get(profile_name, profiles['global'])
        
        # 自动选择
        profile = self.get_optimal_profile()
        return profiles.get(profile['name'], profiles['global'])


# 快捷函数
def quick_probe() -> Dict:
    """快速环境探测（使用缓存）"""
    probe = EnvironmentProbe()
    if probe.load_cache():
        return {
            'network': probe.network_profile,
            'recommended_profile': probe.get_optimal_profile(),
            'from_cache': True,
        }
    else:
        return probe.probe_all()


if __name__ == '__main__':
    # 命令行测试
    probe = EnvironmentProbe()
    result = probe.probe_all(['multi-search-engine', 'exa-web-search-free', 'tavily-search'])
    
    print("\n" + "=" * 60)
    print("环境探测结果")
    print("=" * 60)
    print(f"区域：{result['network']['region']}")
    print(f"代理：{'是' if result['network']['proxy_enabled'] else '否'}")
    print(f"IPv6: {'支持' if result['network']['ipv6_available'] else '不支持'}")
    print(f"推荐配置：{result['recommended_profile']['name']}")
    print(f"描述：{result['recommended_profile']['description']}")

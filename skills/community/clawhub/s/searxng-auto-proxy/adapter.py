#!/usr/bin/env python3
"""
SearXNG 自适应代理适配器 v3.0
三层架构：固定规则 + 动态检测 + 定时优化

作者：pengong101
许可：MIT
版本：3.0.0
"""

import asyncio
import aiohttp
import yaml
import json
import os
import sys
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from pathlib import Path
from enum import Enum

# ========== 配置常量 ==========
CONFIG_FILE = os.environ.get(
    "CONFIG_FILE", 
    "/root/.openclaw/searxng/proxy-rules.yml"
)
LOG_FILE = os.environ.get(
    "LOG_FILE",
    "/root/.openclaw/logs/searxng-proxy-adapter.log"
)
CLASH_API = os.environ.get("CLASH_API", "http://clash:9090")
CACHE_FILE = os.environ.get(
    "CACHE_FILE",
    "/root/.openclaw/searxng/proxy-cache.json"
)

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SearXNGProxyAdapter")


# ========== 数据类 ==========
class ProxyMode(Enum):
    REQUIRED = "required"      # 必须代理
    FORBIDDEN = "forbidden"    # 禁止代理（直连）
    DYNAMIC = "dynamic"        # 动态选择


@dataclass
class EngineConfig:
    """引擎配置"""
    name: str
    proxy_mode: ProxyMode
    test_url: Optional[str] = None
    threshold_ms: float = 3000.0
    fallback: Optional[str] = None
    category: str = "general"
    reason: Optional[str] = None


@dataclass
class EngineStatus:
    """引擎状态"""
    name: str
    use_proxy: bool
    last_tested: datetime
    latency_ms: float = float('inf')
    consecutive_failures: int = 0
    disabled_until: Optional[datetime] = None
    is_disabled: bool = False


@dataclass
class ProxyNode:
    """代理节点"""
    name: str
    latency_ms: float = float('inf')
    last_tested: Optional[datetime] = None
    is_active: bool = True


# ========== 缓存管理器 ==========
class CacheManager:
    """缓存管理器 - 三级缓存"""
    
    def __init__(self, cache_file: str = CACHE_FILE):
        self.cache_file = Path(cache_file)
        self.cache = {
            'engine_status': {},  # 引擎状态缓存
            'proxy_latency': {},  # 代理延迟缓存
            'node_speed': {},     # 节点速度缓存
        }
        self.load()
    
    def load(self):
        """从文件加载缓存"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    data = json.load(f)
                    self.cache.update(data)
                logger.info(f"缓存已加载：{self.cache_file}")
            except Exception as e:
                logger.warning(f"加载缓存失败：{e}")
    
    def save(self):
        """保存缓存到文件"""
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"保存缓存失败：{e}")
    
    def get_engine_status(self, engine_name: str, ttl: int = 30) -> Optional[dict]:
        """获取引擎状态缓存"""
        if engine_name in self.cache['engine_status']:
            entry = self.cache['engine_status'][engine_name]
            if (datetime.now() - datetime.fromisoformat(entry['timestamp'])).total_seconds() < ttl:
                return entry['data']
        return None
    
    def set_engine_status(self, engine_name: str, data: dict):
        """设置引擎状态缓存"""
        self.cache['engine_status'][engine_name] = {
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        self.save()
    
    def get_proxy_latency(self, ttl: int = 1800) -> Optional[float]:
        """获取代理延迟缓存"""
        if 'proxy_latency' in self.cache and self.cache['proxy_latency']:
            entry = self.cache['proxy_latency']
            if (datetime.now() - datetime.fromisoformat(entry['timestamp'])).total_seconds() < ttl:
                return entry['latency']
        return None
    
    def set_proxy_latency(self, latency: float):
        """设置代理延迟缓存"""
        self.cache['proxy_latency'] = {
            'timestamp': datetime.now().isoformat(),
            'latency': latency
        }
        self.save()


# ========== 规则引擎 ==========
class RuleEngine:
    """规则引擎 - Layer 1"""
    
    def __init__(self, config_file: str = CONFIG_FILE):
        self.config_file = Path(config_file)
        self.config = self._load_config()
        self.engines = self._parse_engines()
    
    def _load_config(self) -> dict:
        """加载配置文件"""
        if not self.config_file.exists():
            logger.warning(f"配置文件不存在：{self.config_file}，使用默认配置")
            return self._default_config()
        
        with open(self.config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _default_config(self) -> dict:
        """默认配置"""
        return {
            'engines': {
                'google': {'proxy_mode': 'required', 'fallback': 'bing'},
                'baidu': {'proxy_mode': 'forbidden'},
                'duckduckgo': {'proxy_mode': 'dynamic', 'fallback': 'bing'},
                'wikipedia': {'proxy_mode': 'dynamic', 'fallback': 'baidu'},
            },
            'probe': {'interval': 30, 'timeout_ms': 5000},
            'optimizer': {'interval': 1800, 'clash_api': 'http://clash:9090'},
        }
    
    def _parse_engines(self) -> Dict[str, EngineConfig]:
        """解析引擎配置"""
        engines = {}
        for name, config in self.config.get('engines', {}).items():
            engines[name] = EngineConfig(
                name=name,
                proxy_mode=ProxyMode(config.get('proxy_mode', 'dynamic')),
                test_url=config.get('test_url'),
                threshold_ms=config.get('threshold_ms', 3000),
                fallback=config.get('fallback'),
                category=config.get('category', 'general'),
                reason=config.get('reason')
            )
        return engines
    
    def get_engine_config(self, name: str) -> Optional[EngineConfig]:
        """获取引擎配置"""
        return self.engines.get(name)
    
    def get_probe_config(self) -> dict:
        """获取探测配置"""
        return self.config.get('probe', {})
    
    def get_optimizer_config(self) -> dict:
        """获取优化器配置"""
        return self.config.get('optimizer', {})


# ========== 动态检测器 ==========
class DynamicDetector:
    """动态检测器 - Layer 2"""
    
    def __init__(self, cache: CacheManager):
        self.cache = cache
        self.session: Optional[aiohttp.ClientSession] = None
        self.running = False
    
    async def start(self):
        """启动异步会话"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            self.running = True
            logger.info("动态检测器已启动")
    
    async def stop(self):
        """停止异步会话"""
        self.running = False
        if self.session:
            await self.session.close()
            self.session = None
            logger.info("动态检测器已停止")
    
    async def test_url(self, url: str, use_proxy: bool = False, timeout: float = 5.0) -> Tuple[bool, float]:
        """
        测试 URL 可达性和延迟
        
        返回：(是否成功，延迟毫秒)
        """
        if not self.session or not self.running:
            return False, float('inf')
        
        try:
            proxy = "http://clash:7890" if use_proxy else None
            start = time.time()
            
            async with self.session.get(url, timeout=timeout, proxy=proxy) as resp:
                elapsed = (time.time() - start) * 1000
                return resp.status == 200, elapsed
                
        except asyncio.TimeoutError:
            logger.debug(f"测试超时：{url}")
            return False, float('inf')
        except Exception as e:
            logger.debug(f"测试失败：{url} - {e}")
            return False, float('inf')
    
    async def probe_engine(self, engine: EngineConfig) -> EngineStatus:
        """
        探测引擎状态
        
        返回：引擎状态
        """
        if not engine.test_url:
            # 没有测试 URL，使用默认策略
            return EngineStatus(
                name=engine.name,
                use_proxy=(engine.proxy_mode == ProxyMode.REQUIRED),
                last_tested=datetime.now()
            )
        
        # 检查缓存
        cached = self.cache.get_engine_status(engine.name)
        if cached and not cached.get('is_disabled'):
            return EngineStatus(
                name=engine.name,
                use_proxy=cached['use_proxy'],
                last_tested=datetime.fromisoformat(cached['timestamp']),
                latency_ms=cached.get('latency_ms', float('inf')),
                consecutive_failures=cached.get('consecutive_failures', 0)
            )
        
        # 直连测试
        direct_ok, direct_time = await self.test_url(engine.test_url, use_proxy=False)
        
        # 代理测试
        proxy_ok, proxy_time = await self.test_url(engine.test_url, use_proxy=True)
        
        # 决策逻辑
        use_proxy = False
        latency = float('inf')
        
        if engine.proxy_mode == ProxyMode.REQUIRED:
            use_proxy = True
            latency = proxy_time if proxy_ok else float('inf')
        elif engine.proxy_mode == ProxyMode.FORBIDDEN:
            use_proxy = False
            latency = direct_time if direct_ok else float('inf')
        else:  # DYNAMIC
            if direct_ok and direct_time < engine.threshold_ms:
                use_proxy = False
                latency = direct_time
            elif proxy_ok:
                use_proxy = True
                latency = proxy_time
            else:
                # 都失败，保持上次状态
                use_proxy = cached['use_proxy'] if cached else True
                latency = float('inf')
        
        # 更新缓存
        status_data = {
            'timestamp': datetime.now().isoformat(),
            'use_proxy': use_proxy,
            'latency_ms': latency,
            'consecutive_failures': 0 if (direct_ok or proxy_ok) else (cached.get('consecutive_failures', 0) + 1) if cached else 1,
            'is_disabled': False
        }
        self.cache.set_engine_status(engine.name, status_data)
        
        return EngineStatus(
            name=engine.name,
            use_proxy=use_proxy,
            last_tested=datetime.now(),
            latency_ms=latency,
            consecutive_failures=status_data['consecutive_failures']
        )


# ========== 代理优化器 ==========
class ProxyOptimizer:
    """代理优化器 - Layer 3"""
    
    def __init__(self, clash_api: str = CLASH_API, cache: CacheManager = None):
        self.clash_api = clash_api
        self.cache = cache or CacheManager()
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def start(self):
        """启动"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            logger.info("代理优化器已启动")
    
    async def stop(self):
        """停止"""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def get_proxy_list(self) -> List[str]:
        """获取代理节点列表"""
        try:
            async with self.session.get(f"{self.clash_api}/proxies") as resp:
                data = await resp.json()
                proxies = data.get('proxies', {})
                # 返回所有节点名称
                return [name for name, info in proxies.items() 
                        if info.get('type') in ['Shadowsocks', 'Vmess', 'Trojan', 'Hysteria']]
        except Exception as e:
            logger.error(f"获取代理列表失败：{e}")
            return []
    
    async def test_node_latency(self, node_name: str, test_urls: List[str]) -> float:
        """测试节点延迟"""
        try:
            # 通过 Clash API 测试延迟
            async with self.session.get(
                f"{self.clash_api}/proxies/{node_name}/delay",
                params={'url': test_urls[0], 'timeout': 5000}
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get('delay', float('inf'))
        except:
            pass
        return float('inf')
    
    async def optimize(self) -> Optional[str]:
        """
        优化代理选择
        
        返回：最优节点名称
        """
        nodes = await self.get_proxy_list()
        if not nodes:
            logger.warning("没有可用的代理节点")
            return None
        
        test_urls = [
            "https://www.google.com",
            "https://www.wikipedia.org",
            "https://www.github.com",
        ]
        
        # 并发测试所有节点
        tasks = [self.test_node_latency(node, test_urls) for node in nodes]
        latencies = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 找出最快节点
        best_node = None
        best_latency = float('inf')
        
        for node, latency in zip(nodes, latencies):
            if isinstance(latency, (int, float)) and latency < best_latency:
                best_node = node
                best_latency = latency
        
        if best_node:
            logger.info(f"选择最优节点：{best_node} ({best_latency:.0f}ms)")
            self.cache.set_proxy_latency(best_latency)
            
            # 更新 Clash 配置（需要调用 Clash API）
            await self._switch_proxy(best_node)
        
        return best_node
    
    async def _switch_proxy(self, node_name: str):
        """切换代理节点"""
        try:
            # 更新 Proxy Group
            async with self.session.put(
                f"{self.clash_api}/proxies/Proxy",
                json={'name': node_name}
            ) as resp:
                if resp.status == 204:
                    logger.info(f"已切换到节点：{node_name}")
                else:
                    logger.warning(f"切换节点失败：{resp.status}")
        except Exception as e:
            logger.error(f"切换节点失败：{e}")


# ========== 主适配器 ==========
class SearXNGProxyAdapter:
    """SearXNG 自适应代理适配器 v3.0"""
    
    def __init__(self):
        self.rule_engine = RuleEngine()
        self.cache = CacheManager()
        self.detector = DynamicDetector(self.cache)
        self.optimizer = ProxyOptimizer(cache=self.cache)
        self.running = False
    
    async def start(self):
        """启动适配器"""
        logger.info("=" * 50)
        logger.info("SearXNG 自适应代理适配器 v3.0 启动")
        logger.info("=" * 50)
        
        await self.detector.start()
        await self.optimizer.start()
        self.running = True
        
        # 启动后台探测任务
        asyncio.create_task(self._background_probe())
        
        # 启动定时优化任务
        asyncio.create_task(self._periodic_optimize())
        
        logger.info("适配器已就绪")
    
    async def stop(self):
        """停止适配器"""
        self.running = False
        await self.detector.stop()
        await self.optimizer.stop()
        logger.info("适配器已停止")
    
    async def _background_probe(self):
        """后台探测任务 - 每 30 秒执行"""
        probe_config = self.rule_engine.get_probe_config()
        interval = probe_config.get('interval', 30)
        
        while self.running:
            try:
                logger.debug("开始后台探测...")
                
                # 获取所有动态引擎
                dynamic_engines = [
                    eng for eng in self.rule_engine.engines.values()
                    if eng.proxy_mode == ProxyMode.DYNAMIC
                ]
                
                # 并发探测
                tasks = [self.detector.probe_engine(eng) for eng in dynamic_engines]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # 处理结果
                for result in results:
                    if isinstance(result, EngineStatus):
                        if result.consecutive_failures >= probe_config.get('failure_threshold', 3):
                            logger.warning(f"引擎 {result.name} 连续失败 {result.consecutive_failures} 次")
                
                logger.debug(f"后台探测完成，检测了 {len(dynamic_engines)} 个引擎")
                
            except Exception as e:
                logger.error(f"后台探测失败：{e}")
            
            await asyncio.sleep(interval)
    
    async def _periodic_optimize(self):
        """定时优化任务 - 每 30 分钟执行"""
        optimizer_config = self.rule_engine.get_optimizer_config()
        interval = optimizer_config.get('interval', 1800)
        
        while self.running:
            try:
                logger.info("开始代理优化...")
                best_node = await self.optimizer.optimize()
                if best_node:
                    logger.info(f"优化完成：{best_node}")
            except Exception as e:
                logger.error(f"代理优化失败：{e}")
            
            await asyncio.sleep(interval)
    
    def get_proxy_status(self, engine_name: str) -> dict:
        """
        获取引擎代理状态（同步接口，用于 SearXNG 配置）
        
        返回：{'use_proxy': bool, 'latency_ms': float}
        """
        config = self.rule_engine.get_engine_config(engine_name)
        if not config:
            return {'use_proxy': False, 'latency_ms': float('inf')}
        
        # 固定规则直接返回
        if config.proxy_mode == ProxyMode.REQUIRED:
            return {'use_proxy': True, 'latency_ms': 0}
        elif config.proxy_mode == ProxyMode.FORBIDDEN:
            return {'use_proxy': False, 'latency_ms': 0}
        
        # 动态引擎查询缓存
        cached = self.cache.get_engine_status(engine_name)
        if cached:
            return {
                'use_proxy': cached['use_proxy'],
                'latency_ms': cached.get('latency_ms', float('inf'))
            }
        
        # 默认使用代理
        return {'use_proxy': True, 'latency_ms': float('inf')}
    
    def generate_searxng_config(self) -> str:
        """生成 SearXNG 引擎配置"""
        engines_config = []
        
        for name, config in self.rule_engine.engines.items():
            status = self.get_proxy_status(name)
            
            engine_entry = {
                'name': name,
                'engine': name.replace(' ', '_'),
                'shortcut': name[:2],
                'disabled': status.get('is_disabled', False),
            }
            
            # 添加超时配置
            if config.threshold_ms:
                engine_entry['timeout'] = config.threshold_ms / 1000
            
            engines_config.append(engine_entry)
        
        return yaml.dump({'engines': engines_config}, allow_unicode=True, default_flow_style=False)


# ========== CLI 入口 ==========
async def main():
    """主函数"""
    adapter = SearXNGProxyAdapter()
    
    try:
        await adapter.start()
        
        # 保持运行
        while adapter.running:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("收到中断信号，正在停止...")
    finally:
        await adapter.stop()


if __name__ == "__main__":
    asyncio.run(main())

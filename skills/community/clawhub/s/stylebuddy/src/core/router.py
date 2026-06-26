"""
能力检测与路由模块
检测系统可用能力，决定使用哪种策略
"""

import os
import yaml
import requests
from typing import Dict, Any

class CapabilityRouter:
    """能力路由器 - 检测并管理各种外部能力"""
    
    def __init__(self, config_path: str = "./config.yaml"):
        self.config = self._load_config(config_path)
        self._capabilities = None
    
    def _load_config(self, path: str) -> dict:
        """加载配置"""
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        return {}
    
    def detect(self, force: bool = False) -> Dict[str, Any]:
        """检测系统能力"""
        if self._capabilities is not None and not force:
            return self._capabilities
        
        self._capabilities = {
            "model_tier": self._detect_model(),
            "weather_api": self._test_weather_api(),
            "image_search": self._test_image_search(),
            "image_gen": self._test_image_gen(),
            "calendar": False,  # 暂时关闭
            "timestamp": __import__('time').time()
        }
        
        return self._capabilities
    
    def _detect_model(self) -> str:
        """检测模型等级"""
        # 根据环境变量或配置判断
        # high = 支持 vision + function calling
        # medium = 支持 function calling
        # low = 基础文本模型
        model = os.environ.get('OPENCLAW_MODEL', '').lower()
        if any(m in model for m in ['gpt-4', 'claude-3', 'kimi-k2']):
            return "high"
        elif any(m in model for m in ['gpt-3.5', 'claude-instant', 'kimi']):
            return "medium"
        return "low"
    
    def _test_weather_api(self) -> bool:
        """测试天气 API"""
        try:
            # Open-Meteo 免费且稳定
            url = "https://api.open-meteo.com/v1/forecast"
            params = {"latitude": 39.9, "longitude": 116.4, "current": "temperature_2m"}
            resp = requests.get(url, params=params, timeout=5)
            return resp.status_code == 200
        except:
            return False
    
    def _test_image_search(self) -> bool:
        """测试图片搜索 API"""
        api_config = self.config.get('api', {}).get('image_search', {})
        if not api_config.get('enabled', False):
            return False
        api_key = api_config.get('api_key', '')
        return bool(api_key and len(api_key) > 10)
    
    def _test_image_gen(self) -> bool:
        """测试图片生成 API"""
        api_config = self.config.get('api', {}).get('image_generation', {})
        if not api_config.get('enabled', False):
            return False
        api_key = api_config.get('api_key', '')
        return bool(api_key and len(api_key) > 10)
    
    def get_strategy(self, feature: str) -> str:
        """
        获取功能的执行策略
        
        Args:
            feature: 功能名称 (recommendation/visualization/search)
        
        Returns:
            策略名称
        """
        caps = self.detect()
        
        if feature == "recommendation":
            if caps["model_tier"] in ["high", "medium"]:
                return "ai_enhanced"
            return "template_based"
        
        elif feature == "visualization":
            if caps["image_gen"]:
                return "ai_generation"
            return "pil_composite"
        
        elif feature == "search":
            if caps["image_search"]:
                return "api_search"
            return "local_gallery"
        
        elif feature == "weather":
            if caps["weather_api"]:
                return "api_weather"
            return "manual_input"
        
        return "fallback"
    
    def should_use_fallback(self, feature: str) -> bool:
        """判断是否使用降级策略"""
        strategy = self.get_strategy(feature)
        return strategy.endswith("_based") or strategy.endswith("_composite") or strategy == "fallback"
    
    def get_status_report(self) -> str:
        """获取能力状态报告"""
        caps = self.detect()
        
        status = []
        status.append("🌸 StyleBuddy 能力状态")
        status.append("")
        
        # 模型等级
        tier_icons = {"high": "🟢", "medium": "🟡", "low": "🔴"}
        tier_names = {"high": "高级", "medium": "中级", "low": "基础"}
        t = caps["model_tier"]
        status.append(f"{tier_icons.get(t, '⚪')} AI 模型: {tier_names.get(t, '未知')}")
        
        # 外部服务
        status.append(f"{'🟢' if caps['weather_api'] else '🔴'} 天气服务")
        status.append(f"{'🟢' if caps['image_search'] else '🔴'} 图片搜索")
        status.append(f"{'🟢' if caps['image_gen'] else '🔴'} AI 图片生成")
        
        status.append("")
        status.append("💡 降级策略已启用，离线也能正常使用")
        
        return "\n".join(status)

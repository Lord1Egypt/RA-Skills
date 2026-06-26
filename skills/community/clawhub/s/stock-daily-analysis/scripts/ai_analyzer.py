# -*- coding: utf-8 -*-
"""
AI 分析模块 - 调用 Gemini/OpenAI 进行深度分析
"""

import json
import logging
from typing import Dict, Any, Optional

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

logger = logging.getLogger(__name__)


class AIAnalyzer:
    """AI 分析器 - 支持 Gemini 和 OpenAI"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.provider = config.get('provider', 'gemini')
        self.api_key = config.get('api_key', '')
        self.model = config.get('model', 'gemini-3-flash-preview')
        self.temperature = config.get('temperature', 0.3)
        self.max_tokens = config.get('max_tokens', 4096)
        
        if self.provider == 'openai' and HAS_OPENAI:
            base_url = config.get('base_url', 'https://api.openai.com/v1')
            self.client = OpenAI(api_key=self.api_key, base_url=base_url)
        else:
            self.client = None
    
    def analyze(self, code: str, name: str, technical_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        使用 AI 进行深度分析
        
        Args:
            code: 股票代码
            name: 股票名称
            technical_data: 技术指标数据
            
        Returns:
            AI 分析结果
        """
        if not self.api_key:
            logger.warning("未配置 API Key，跳过 AI 分析")
            return self._default_analysis()
        
        try:
            if self.provider == 'gemini':
                return self._analyze_with_gemini(code, name, technical_data)
            else:
                return self._analyze_with_openai(code, name, technical_data)
        except Exception as e:
            logger.error(f"AI 分析失败: {e}")
            return self._default_analysis()
    
    def _analyze_with_gemini(self, code: str, name: str, tech: Dict[str, Any]) -> Dict[str, Any]:
        """使用 Gemini API"""
        import requests
        import os
        
        prompt = self._build_prompt(code, name, tech)
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        headers = {"Content-Type": "application/json"}
        params = {"key": self.api_key}
        
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": self.temperature,
                "maxOutputTokens": self.max_tokens
            }
        }
        
        # 代理设置
        proxies = {}
        proxy_url = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
        if proxy_url:
            proxies = {'https': proxy_url, 'http': proxy_url}
        
        response = requests.post(url, headers=headers, params=params, json=data, timeout=30, proxies=proxies)
        response.raise_for_status()
        
        result = response.json()
        text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        
        return self._parse_ai_response(text, tech)
    
    def _analyze_with_openai(self, code: str, name: str, tech: Dict[str, Any]) -> Dict[str, Any]:
        """使用 OpenAI API"""
        if not HAS_OPENAI or not self.client:
            return self._default_analysis()
        
        prompt = self._build_prompt(code, name, tech)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        
        text = response.choices[0].message.content
        return self._parse_ai_response(text, tech)
    
    def _build_prompt(self, code: str, name: str, tech: Dict[str, Any]) -> str:
        """构建 AI 提示词"""
        
        return f"""你是一位专业的股票分析师，请根据以下技术指标给出投资建议。

股票: {name} ({code})

技术指标数据:
- 当前价格: {tech.get('current_price', 'N/A')}
- MA5: {tech.get('ma5', 'N/A'):.2f} (乖离率: {tech.get('bias_ma5', 0):+.2f}%)
- MA10: {tech.get('ma10', 'N/A'):.2f} (乖离率: {tech.get('bias_ma10', 0):+.2f}%)
- MA20: {tech.get('ma20', 'N/A'):.2f}
- 趋势状态: {tech.get('trend_status', 'N/A')}
- MACD: {tech.get('macd_status', 'N/A')} - {tech.get('macd_signal', '')}
- RSI: {tech.get('rsi_status', 'N/A')} - {tech.get('rsi_signal', '')}
- 量能: {tech.get('volume_status', 'N/A')} - {tech.get('volume_trend', '')}
- 技术面评分: {tech.get('signal_score', 0)}/100
- 买入信号: {tech.get('buy_signal', 'N/A')}
- 买入理由: {', '.join(tech.get('signal_reasons', []))}
- 风险因素: {', '.join(tech.get('risk_factors', []))}

请输出以下 JSON 格式的分析结果:
{{
    "sentiment_score": 0-100,
    "trend_prediction": "上涨/下跌/震荡",
    "operation_advice": "买入/持有/观望/卖出",
    "confidence_level": "高/中/低",
    "analysis_summary": "一句话核心结论",
    "buy_reason": "具体买入理由",
    "risk_warning": "风险提示",
    "target_price": "目标价",
    "stop_loss": "止损价"
}}

只输出 JSON，不要其他内容。"""
    
    def _parse_ai_response(self, text: str, tech: Dict[str, Any]) -> Dict[str, Any]:
        """解析 AI 响应"""
        try:
            # 尝试提取 JSON
            import re
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return {
                    'sentiment_score': result.get('sentiment_score', tech.get('signal_score', 50)),
                    'trend_prediction': result.get('trend_prediction', tech.get('trend_status', '震荡')),
                    'operation_advice': result.get('operation_advice', tech.get('buy_signal', '观望')),
                    'confidence_level': result.get('confidence_level', '中'),
                    'analysis_summary': result.get('analysis_summary', ''),
                    'buy_reason': result.get('buy_reason', ''),
                    'risk_warning': result.get('risk_warning', ''),
                    'target_price': result.get('target_price', ''),
                    'stop_loss': result.get('stop_loss', '')
                }
        except Exception as e:
            logger.warning(f"解析 AI 响应失败: {e}")
        
        # 回退到基于技术面的默认分析
        return self._default_analysis_from_tech(tech)
    
    def _default_analysis_from_tech(self, tech: Dict[str, Any]) -> Dict[str, Any]:
        """基于技术面的默认分析"""
        score = tech.get('signal_score', 50)
        buy_signal = tech.get('buy_signal', '观望')
        
        return {
            'sentiment_score': score,
            'trend_prediction': tech.get('trend_status', '震荡'),
            'operation_advice': buy_signal,
            'confidence_level': '高' if score >= 70 else '中' if score >= 50 else '低',
            'analysis_summary': ' | '.join(tech.get('signal_reasons', []))[:100],
            'buy_reason': ', '.join(tech.get('signal_reasons', [])),
            'risk_warning': ' | '.join(tech.get('risk_factors', [])),
            'target_price': '',
            'stop_loss': ''
        }
    
    def _default_analysis(self) -> Dict[str, Any]:
        """默认分析结果"""
        return {
            'sentiment_score': 50,
            'trend_prediction': '震荡',
            'operation_advice': '观望',
            'confidence_level': '低',
            'analysis_summary': 'AI 分析未启用',
            'buy_reason': '',
            'risk_warning': '',
            'target_price': '',
            'stop_loss': ''
        }

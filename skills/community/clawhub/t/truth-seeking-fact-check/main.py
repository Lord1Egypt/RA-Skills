#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Truth (求真) Skill v1.5.0 - 入口模块
功能：6层事实核查，识别AI幻觉，输出可信度评分，支持元认知置信度、可配置权重、定时核查，含区块链存证验证
可简称 truth 使用
"""

from typing import Dict, List, Union, Optional
import json
import logging
from preprocess import TextPreprocessor
from checker import FactChecker
from datasource import DataSourceManager
from batch import BatchProcessor
from scheduler import TimedScheduler
from formatter import OutputFormatter
from compliance import ComplianceChecker

logger = logging.getLogger(__name__)

class TruthSkill:
    """Truth (求真) 技能主类 - v1.5.0 元认知+可配置权重+定时核查版本"""
    
    def __init__(self, config: Optional[Dict] = None):
        """初始化"""
        self.config = config or {}
        self.compliance = ComplianceChecker()
        self.preprocessor = TextPreprocessor()
        self.datasource = DataSourceManager(self.config.get('datasources', {}))
        self.checker = FactChecker(self.datasource)
        self.batch_processor = BatchProcessor(self.checker, max_concurrency=2)  # 适配2核2G，最大并发=2
        # 定时核查，默认关闭，用户配置后开启
        self.scheduler = TimedScheduler(self, self.config.get('scheduler', {})) if self.config.get('scheduler') else None
        self.formatter = OutputFormatter()
        
    def get_metadata(self) -> Dict:
        """获取技能元数据"""
        return {
            "name": "Truth (求真)",
            "version": "v1.5.0",
            "description": "事实核查技能，6层深度核查（含区块链存证验证），元认知置信度输出，可配置维度权重，支持定时核查。适配2核2G环境，识别AI幻觉。可简称truth使用。",
            "author": "tangtaozhanshen",
            "license": "MIT-0",
            "privacy": "All processing runs locally, no user content uploaded to external servers. 100% privacy protection.",
            "features": [
                "6层事实核查",
                "区块链存证验证",
                "批量核查支持",
                "元认知置信度输出",
                "维度权重可配置",
                "可选定时核查",
                "适配2核2G环境",
                "100%隐私保护"
            ]
        }
    
    def check_text(self, text: str, output_format: str = "both", weights: Optional[Dict[str, float]] = None) -> Union[Dict, str]:
        """单篇文本核查 - v1.5.0 支持自定义维度权重"""
        # 1. 合规检查
        is_ok, reason = self.compliance.check(text)
        if not is_ok:
            return self.formatter.format_error(reason, output_format)
        
        # 2. 文本预处理
        sentences = self.preprocessor.split_sentences(text)
        
        # 3. 6层事实核查，支持自定义权重
        if weights is None:
            weights = self.config.get('dimension_weights', None)
        result = self.checker.check(text, sentences, weights)
        
        # 4. 格式化输出
        return self.formatter.format_result(result, output_format)
    
    def check_batch(self, texts: List[str], output_format: str = "both") -> Union[Dict, str]:
        """批量文本核查"""
        # 合规检查每篇文本
        for idx, text in enumerate(texts):
            is_ok, reason = self.compliance.check(text)
            if not is_ok:
                texts[idx] = f"【违规内容已拦截】{reason}"
        
        # 批量核查
        weights = self.config.get('dimension_weights', None)
        results = self.batch_processor.process_batch(texts, weights)
        
        # 格式化输出
        return self.formatter.format_batch_result(results, output_format)
    
    def check_batch_with_weights(self, texts: List[str], weights: Dict[str, float], output_format: str = "both") -> Union[Dict, str]:
        """批量文本核查，自定义权重"""
        # 合规检查每篇文本
        for idx, text in enumerate(texts):
            is_ok, reason = self.compliance.check(text)
            if not is_ok:
                texts[idx] = f"【违规内容已拦截】{reason}"
        
        # 批量核查
        results = self.batch_processor.process_batch(texts, weights)
        
        # 格式化输出
        return self.formatter.format_batch_result(results, output_format)
    
    def check_url(self, url: str, output_format: str = "both") -> Union[Dict, str]:
        """网页URL核查"""
        # TODO: 实现网页抓取
        # 占位：下一阶段完成
        error_msg = "网页核查功能开发中，敬请期待 v1.6"
        return self.formatter.format_error(error_msg, output_format)
    
    # 定时核查相关接口
    def start_scheduler(self):
        """启动定时核查任务，需要先在配置中开启scheduler"""
        if self.scheduler:
            self.scheduler.start()
            return {"status": "ok", "message": "定时核查已启动"}
        else:
            return {"status": "error", "message": "未配置定时核查，请在初始化配置中添加scheduler配置后重启"}
    
    def stop_scheduler(self):
        """停止定时核查任务"""
        if self.scheduler:
            self.scheduler.stop()
            return {"status": "ok", "message": "定时核查已停止"}
        else:
            return {"status": "error", "message": "未配置定时核查"}
    
    def add_timed_check(self, text: str, callback = None):
        """添加定时核查任务"""
        if not self.scheduler:
            return {"status": "error", "message": "未配置定时核查"}
        return self.scheduler.add_task(text, callback)
    
    def skill_entry(self, params: Dict) -> Dict:
        """OpenClaw 技能标准入口 - v1.5.0"""
        text = params.get('text', '')
        texts = params.get('texts', [])
        url = params.get('url', '')
        weights = params.get('weights', None)
        output_format = params.get('output_format', 'both')
        action = params.get('action', '')
        
        # 定时调度动作
        if action == "start_scheduler":
            return self.start_scheduler()
        elif action == "stop_scheduler":
            return self.stop_scheduler()
        elif action == "add_timed_check":
            return self.add_timed_check(text)
        
        if url:
            result = self.check_url(url, output_format='json')
        elif texts:
            if weights:
                result = self.check_batch_with_weights(texts, weights, output_format='json')
            else:
                result = self.check_batch(texts, output_format='json')
        elif text:
            result = self.check_text(text, output_format='json', weights=weights)
        else:
            return {"error": "缺少输入参数：text/texts/url 其中一项必填"}
        
        if isinstance(result, str):
            return json.loads(result)
        return result


# 独立运行测试
if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    
    skill = TruthSkill()
    print("=== Truth (求真) v1.5.0 测试 ===")
    print("元数据:", json.dumps(skill.get_metadata(), indent=2, ensure_ascii=False))

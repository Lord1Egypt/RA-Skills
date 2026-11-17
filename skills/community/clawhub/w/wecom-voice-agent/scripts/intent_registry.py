#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
intent_registry.py — 声明式意图引擎（v2.6）

功能：
1. 加载 intents.yaml 声明式配置
2. 关键词匹配 + 置信度计算
3. 多级澄清策略（≥0.7直接执行，0.4-0.7反问收窄，<0.4转帮助）
4. 新增意图只改配置不改代码

依赖：纯 Python 标准库（yaml 可选，不可用时降级为 json）
联系信息：njskills@agent.qq.com

版本：v1.0 (2026-08-24)
"""

import os
import re
import json
import logging
from typing import Optional, Dict, List, Any, Tuple

logger = logging.getLogger(__name__)

# 尝试导入 pyyaml，不可用时降级为 json
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    logger.warning("pyyaml 不可用，将使用 JSON 格式作为降级")


# ==========================================
# 配置
# ==========================================

CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config')
INTENTS_FILE_YAML = os.path.join(CONFIG_DIR, 'intents.yaml')
INTENTS_FILE_JSON = os.path.join(CONFIG_DIR, 'intents.json')


# ==========================================
# 意图注册表
# ==========================================

class IntentRegistry:
    """
    声明式意图引擎
    
    加载 intents.yaml 配置，实现关键词匹配和置信度计算。
    多级澄清策略：
    - 置信度 ≥ 0.7：直接执行
    - 置信度 0.4-0.7：反问收窄
    - 置信度 < 0.4：转帮助
    
    使用方式：
        registry = IntentRegistry()
        registry.load()
        intent, confidence, entities = registry.parse("明天天气怎么样")
    """

    def __init__(self, config_path: str = None):
        """
        初始化意图注册表
        
        Args:
            config_path: 配置文件路径，None 则使用默认路径
        """
        self.config_path = config_path
        self.intents: Dict[str, Dict] = {}
        self.clarification_config: Dict = {}
        self._compiled_patterns: Dict[str, List[re.Pattern]] = {}
        self._loaded = False
        
    def load(self) -> bool:
        """
        加载意图配置文件
        
        Returns:
            bool: 加载成功返回 True
        """
        # 确定配置文件路径
        if self.config_path:
            path = self.config_path
        elif YAML_AVAILABLE and os.path.exists(INTENTS_FILE_YAML):
            path = INTENTS_FILE_YAML
        elif os.path.exists(INTENTS_FILE_JSON):
            path = INTENTS_FILE_JSON
        elif os.path.exists(INTENTS_FILE_YAML):
            path = INTENTS_FILE_YAML
        else:
            logger.error(f"意图配置文件不存在: {INTENTS_FILE_YAML}")
            return False
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                if path.endswith('.yaml') or path.endswith('.yml'):
                    if YAML_AVAILABLE:
                        config = yaml.safe_load(f)
                    else:
                        logger.warning("pyyaml 不可用，尝试解析为 JSON")
                        config = json.load(f)
                else:
                    config = json.load(f)
            
            if not config or 'intents' not in config:
                logger.error("意图配置文件格式错误：缺少 intents 字段")
                return False
            
            self.intents = config['intents']
            self.clarification_config = config.get('clarification', {
                'high_confidence': 0.7,
                'medium_confidence': 0.4,
                'max_clarification_rounds': 2,
                'clarification_prompt': '抱歉，我没有完全理解您的意思。您是想：'
            })
            
            # 预编译正则模式
            self._compile_patterns()
            
            self._loaded = True
            logger.info(f"意图注册表加载完成：{len(self.intents)} 个意图")
            return True
            
        except Exception as e:
            logger.error(f"加载意图配置文件失败: {e}")
            return False
    
    def _compile_patterns(self):
        """预编译关键词正则模式"""
        for intent_name, intent_config in self.intents.items():
            patterns = []
            for kw in intent_config.get('keywords', []):
                try:
                    # 包含正则元字符的关键词用正则匹配
                    if any(c in kw for c in '.^$*+?{}[]|()'):
                        patterns.append(re.compile(kw, re.IGNORECASE))
                    else:
                        patterns.append(re.compile(re.escape(kw), re.IGNORECASE))
                except re.error:
                    patterns.append(re.compile(re.escape(kw), re.IGNORECASE))
            self._compiled_patterns[intent_name] = patterns
    
    def parse(self, text: str) -> Tuple[str, float, Dict]:
        """
        解析文本意图
        
        Args:
            text: 用户输入文本
            
        Returns:
            tuple: (意图名称, 置信度, 实体字典)
        """
        if not self._loaded:
            if not self.load():
                return "custom", 0.0, {}
        
        if not text:
            return "custom", 0.0, {}
        
        text_lower = text.lower().strip()
        best_intent = "custom"
        max_score = 0.0
        
        # 遍历所有意图，计算匹配分数
        for intent_name, intent_config in self.intents.items():
            if intent_name == 'custom':
                continue
            
            patterns = self._compiled_patterns.get(intent_name, [])
            score = 0.0
            
            for pat in patterns:
                if pat.search(text_lower):
                    score += 1.0
            
            # 加权：匹配多个不同关键词有加分
            if score > 0:
                score += (score - 1) * 0.1
            
            # 归一化到 0-1
            confidence = min(score / 3.0, 1.0)
            
            if confidence > max_score:
                max_score = confidence
                best_intent = intent_name
        
        # 提取实体
        entities = self._extract_entities(text_lower, best_intent)
        
        return best_intent, max_score, entities
    
    def get_confidence_level(self, confidence: float) -> str:
        """
        获取置信度级别
        
        Args:
            confidence: 置信度值
            
        Returns:
            str: 'high' | 'medium' | 'low'
        """
        high = self.clarification_config.get('high_confidence', 0.7)
        medium = self.clarification_config.get('medium_confidence', 0.4)
        
        if confidence >= high:
            return 'high'
        elif confidence >= medium:
            return 'medium'
        else:
            return 'low'
    
    def get_handler(self, intent_name: str) -> str:
        """
        获取意图对应的处理器名称
        
        Args:
            intent_name: 意图名称
            
        Returns:
            str: 处理器名称
        """
        if intent_name in self.intents:
            return self.intents[intent_name].get('handler', 'handle_custom')
        return 'handle_custom'
    
    def get_category(self, intent_name: str) -> str:
        """
        获取意图所属大类
        
        Args:
            intent_name: 意图名称
            
        Returns:
            str: 大类名称（query/action/system）
        """
        if intent_name in self.intents:
            return self.intents[intent_name].get('category', 'system')
        return 'system'
    
    def get_clarification_prompt(self) -> str:
        """获取反问提示语"""
        return self.clarification_config.get('clarification_prompt', 
                                             '抱歉，我没有完全理解您的意思。您是想：')
    
    def get_intent_display_name(self, intent_name: str) -> str:
        """获取意图显示名称"""
        if intent_name in self.intents:
            return self.intents[intent_name].get('display_name', intent_name)
        return intent_name
    
    def get_slot_templates(self, intent_name: str) -> List[Dict]:
        """获取意图的槽位模板"""
        if intent_name in self.intents:
            return self.intents[intent_name].get('slot_templates', [])
        return []
    
    def get_all_intents(self) -> Dict:
        """获取所有意图配置"""
        return self.intents.copy()
    
    def get_intents_by_category(self, category: str) -> Dict:
        """
        获取指定大类的所有意图
        
        Args:
            category: 大类名称（query/action/system）
            
        Returns:
            dict: 该大类下的所有意图
        """
        return {k: v for k, v in self.intents.items() if v.get('category') == category}
    
    def _extract_entities(self, text: str, intent_name: str) -> Dict:
        """
        根据意图的槽位模板提取实体
        
        Args:
            text: 用户输入文本
            intent_name: 意图名称
            
        Returns:
            dict: 提取的实体
        """
        entities = {}
        slot_templates = self.get_slot_templates(intent_name)
        
        for slot in slot_templates:
            name = slot.get('name')
            slot_type = slot.get('type', 'string')
            
            if slot_type == 'date':
                date_val = self._extract_date(text)
                if date_val:
                    entities[name] = date_val
            elif slot_type == 'time':
                time_val = self._extract_time(text)
                if time_val:
                    entities[name] = time_val
            elif slot_type == 'location':
                loc_val = self._extract_location(text)
                if loc_val:
                    entities[name] = loc_val
            elif slot_type == 'string':
                # 通用字符串提取（人名等）
                pass
        
        return entities
    
    def _extract_date(self, text: str) -> Optional[str]:
        """提取日期实体"""
        from datetime import datetime, timedelta
        
        time_map = {
            "今天": 0, "明天": 1, "后天": 2, "大后天": 3,
            "昨天": -1, "前天": -2
        }
        for word, offset in time_map.items():
            if word in text:
                target = datetime.now() + timedelta(days=offset)
                return target.strftime("%Y-%m-%d")
        
        # 周一..周日匹配
        for i, day in enumerate(["周一", "周二", "周三", "周四", "周五", "周六", "周日"]):
            if day in text:
                today = datetime.now()
                days_ahead = (i - today.weekday()) % 7
                if days_ahead == 0:
                    days_ahead = 7
                target = today + timedelta(days=days_ahead)
                return target.strftime("%Y-%m-%d")
        
        # X月X日
        m = re.search(r'(\d{1,2})月(\d{1,2})日', text)
        if m:
            month, day = m.groups()
            return f"{datetime.now().year}-{int(month):02d}-{int(day):02d}"
        
        return None
    
    def _extract_time(self, text: str) -> Optional[str]:
        """提取时间实体"""
        # X点X分
        m = re.search(r'(\d{1,2})点(\d{1,2})分', text)
        if m:
            hour = int(m.group(1))
            minute = int(m.group(2))
            return f"{hour:02d}:{minute:02d}"
        
        # X点
        m = re.search(r'(上|下|晚)?午?(\d{1,2})点', text)
        if m:
            prefix = m.group(1) or ""
            hour = int(m.group(2))
            if prefix in ("下", "晚") and hour < 12:
                hour += 12
            return f"{hour:02d}:00"
        
        return None
    
    def _extract_location(self, text: str) -> Optional[str]:
        """提取地点实体"""
        cities = ["北京", "上海", "广州", "深圳", "杭州", "成都", "武汉",
                  "西安", "南京", "重庆", "苏州", "天津", "长沙", "郑州", "大连",
                  "青岛", "厦门", "福州", "昆明", "珠海"]
        for c in cities:
            if c in text:
                return c
        return None


# ==========================================
# 便捷函数
# ==========================================

def parse_intent(text: str, config_path: str = None) -> Tuple[str, float, Dict]:
    """便捷函数：解析意图"""
    registry = IntentRegistry(config_path)
    registry.load()
    return registry.parse(text)


# ==========================================
# 自测
# ==========================================

def run_self_test():
    """运行意图注册表自测"""
    print("=" * 60)
    print("意图注册表 — 自测模式")
    print("=" * 60)
    
    registry = IntentRegistry()
    if not registry.load():
        print("❌ 意图注册表加载失败")
        return
    
    # 测试 1: 天气查询
    print("\n[测试 1] 天气查询")
    intent, conf, entities = registry.parse("明天北京天气怎么样")
    print(f"  输入: '明天北京天气怎么样'")
    print(f"  意图: {intent}, 置信度: {conf:.2f}, 实体: {entities}")
    assert intent == "query_weather"
    assert conf > 0.3
    print("✅ 天气查询通过")
    
    # 测试 2: 日程查询
    print("\n[测试 2] 日程查询")
    intent, conf, entities = registry.parse("下周一有什么会")
    print(f"  输入: '下周一有什么会'")
    print(f"  意图: {intent}, 置信度: {conf:.2f}, 实体: {entities}")
    assert intent == "query_schedule"
    print("✅ 日程查询通过")
    
    # 测试 3: 创建待办
    print("\n[测试 3] 创建待办")
    intent, conf, entities = registry.parse("提醒我下午3点开会")
    print(f"  输入: '提醒我下午3点开会'")
    print(f"  意图: {intent}, 置信度: {conf:.2f}, 实体: {entities}")
    assert intent == "create_todo"
    print("✅ 创建待办通过")
    
    # 测试 4: 订单查询（新增意图）
    print("\n[测试 4] 订单查询（新增意图）")
    intent, conf, entities = registry.parse("我的订单到哪了")
    print(f"  输入: '我的订单到哪了'")
    print(f"  意图: {intent}, 置信度: {conf:.2f}, 实体: {entities}")
    assert intent == "query_order"
    print("✅ 订单查询通过")
    
    # 测试 5: 转接人工
    print("\n[测试 5] 转接人工")
    intent, conf, entities = registry.parse("转人工客服")
    print(f"  输入: '转人工客服'")
    print(f"  意图: {intent}, 置信度: {conf:.2f}, 实体: {entities}")
    assert intent == "transfer_human"
    print("✅ 转接人工通过")
    
    # 测试 6: 多级澄清策略
    print("\n[测试 6] 多级澄清策略")
    level_high = registry.get_confidence_level(0.8)
    level_medium = registry.get_confidence_level(0.5)
    level_low = registry.get_confidence_level(0.2)
    print(f"  0.8 -> {level_high}, 0.5 -> {level_medium}, 0.2 -> {level_low}")
    assert level_high == 'high'
    assert level_medium == 'medium'
    assert level_low == 'low'
    print("✅ 多级澄清策略通过")
    
    # 测试 7: 大类分组
    print("\n[测试 7] 大类分组")
    query_intents = registry.get_intents_by_category('query')
    action_intents = registry.get_intents_by_category('action')
    system_intents = registry.get_intents_by_category('system')
    print(f"  查询类: {len(query_intents)} 个")
    print(f"  操作类: {len(action_intents)} 个")
    print(f"  系统类: {len(system_intents)} 个")
    assert len(query_intents) >= 4
    assert len(action_intents) >= 3
    assert len(system_intents) >= 4
    print("✅ 大类分组通过")
    
    # 测试 8: 处理器引用
    print("\n[测试 8] 处理器引用")
    handler = registry.get_handler('query_weather')
    print(f"  query_weather 处理器: {handler}")
    assert handler == 'handle_query_weather'
    print("✅ 处理器引用通过")
    
    print(f"\n{'='*60}")
    print("所有自测通过 ✓")
    print("=" * 60)


if __name__ == "__main__":
    run_self_test()

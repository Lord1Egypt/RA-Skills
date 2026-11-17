#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
entity_extractor.py — 实体抽取增强模块（v2.6）

功能：
1. 规则层：时间/数字/人称/称谓表等实体识别
2. 上下文消歧：代词回指上一轮实体（如"他"指上一轮提到的人）
3. 复述确认：抽取结果回显核对，降低语音转写误差传导

依赖：纯 Python 标准库（零外部依赖）
联系信息：njskills@agent.qq.com

版本：v1.0 (2026-08-24)
"""

import re
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any

logger = logging.getLogger(__name__)


# ==========================================
# 实体抽取器
# ==========================================

class EntityExtractor:
    """
    增强版实体抽取器
    
    特性：
    - 规则层：时间、数字、人称、称谓、地点、订单号等
    - 上下文消歧：代词回指、省略补全
    - 复述确认：格式化实体回显
    
    使用方式：
        extractor = EntityExtractor()
        entities = extractor.extract("明天下午3点提醒张三开会")
        print(extractor.format_for_confirmation(entities))
    """

    # 姓氏表（常见中文姓氏）
    SURNAMES = (
        "王李张刘陈杨黄赵周吴徐孙马朱胡郭何高林郑谢罗梁宋唐许韩冯邓曹彭曾田董袁潘于蒋蔡余杜叶程苏魏吕丁任沈姚卢姜崔钟谭陆汪范金石廖贾夏付方白邹孟熊秦江薛闫段雷侯龙史陶黎贺顾毛郝龚邵万钱严覃武戴莫孔"
    )

    # 常见复姓
    DOUBLE_SURNAMES = [
        "欧阳", "司马", "上官", "诸葛", "东方", "皇甫", "公孙", "慕容",
        "司徒", "司空", "令狐", "轩辕", "宇文", "长孙", "尉迟", "申屠"
    ]

    # 称谓表
    TITLES = [
        "先生", "女士", "小姐", "老师", "教授", "经理", "主任", "主管",
        "总监", "部长", "局长", "处长", "科长", "院长", "校长", "博士",
        "总", "工", "师傅", "同志"
    ]

    # 代词映射（用于上下文消歧）
    PRONOUNS = {
        "他": "person",
        "她": "person",
        "它": "thing",
        "他们": "persons",
        "她们": "persons",
        "这个": "thing",
        "那个": "thing",
        "这个时间": "time",
        "那个时间": "time",
        "这里": "location",
        "那里": "location",
        "当天": "date",
        "明天": "date",
        "后天": "date",
    }

    def __init__(self):
        """初始化实体抽取器"""
        self._compiled_patterns = {}
        self._compile_patterns()
        self._context: Dict[str, Any] = {}  # 上一轮上下文

    def _compile_patterns(self):
        """预编译正则模式"""
        # 订单号（字母数字组合，6-20位）
        self._compiled_patterns['order_id'] = re.compile(
            r'(?:订单号|订单编号|单号|编号)?[:\s]*([A-Za-z0-9]{6,20})'
        )
        # 金额（数字+元/块/万）
        self._compiled_patterns['amount'] = re.compile(
            r'(\d+(?:\.\d+)?)\s*(元|块|万元|万)'
        )
        # 手机号
        self._compiled_patterns['phone'] = re.compile(
            r'1[3-9]\d{9}'
        )
        # 邮箱
        self._compiled_patterns['email'] = re.compile(
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        )
        # 日期：X月X日
        self._compiled_patterns['date_md'] = re.compile(
            r'(\d{1,2})月(\d{1,2})日'
        )
        # 时间：X点X分
        self._compiled_patterns['time_hm'] = re.compile(
            r'(\d{1,2})点(\d{1,2})分'
        )
        # 时间：X点
        self._compiled_patterns['time_h'] = re.compile(
            r'(上|下|晚|早)?午?(\d{1,2})点'
        )
        # 百分比
        self._compiled_patterns['percentage'] = re.compile(
            r'(\d+(?:\.\d+)?)\s*%'
        )
        # 数字+量词
        self._compiled_patterns['quantity'] = re.compile(
            r'(\d+)\s*(个|件|份|张|条|本|次|天|周|月|年|人|位)'
        )

    def extract(self, text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        从文本中提取实体
        
        Args:
            text: 用户输入文本
            context: 上一轮上下文（用于消歧），为 None 时保持现有上下文
            
        Returns:
            dict: 提取的实体
        """
        # 只有显式传入 context 时才更新，否则保持现有上下文
        if context is not None:
            self._context = context

        entities = {}

        # 提取各类实体
        entities.update(self._extract_date(text))
        entities.update(self._extract_time(text))
        entities.update(self._extract_person(text))
        entities.update(self._extract_location(text))
        entities.update(self._extract_order_id(text))
        entities.update(self._extract_amount(text))
        entities.update(self._extract_phone(text))
        entities.update(self._extract_email(text))
        entities.update(self._extract_percentage(text))
        entities.update(self._extract_quantity(text))

        # 上下文消歧
        entities = self._resolve_pronouns(text, entities)

        return entities

    # === 群任务三元组抽取（v2.9）===

    ASSIGN_VERBS = ("交", "做", "负责", "跟进", "处理", "安排", "指派", "交给",
                   "落实", "完成", "写", "准备", "提交", "回复", "确认", "对接")

    def extract_assignment(self, text: str, speaker_userid: str = None) -> Dict[str, Any]:
        """
        群任务三元组抽取（v2.9）：指派人 + 被指派人 + 期限

        - 指派人（assigner）：发言者（speaker_userid），即「谁说的」
        - 被指派人（assignee）：文本中 @XXX 提及，或抽取到的人名
        - 期限（due_date/due_time）：复用日期/时间抽取

        Args:
            text: 用户输入文本
            speaker_userid: 群内发言者 userid

        Returns:
            dict: {
                "assigner", "assignee", "due_date", "due_time",
                "content", "is_assignment"
            }
        """
        entities = self.extract(text)
        mention = self._extract_mention(text)
        assignee = mention or entities.get("person")
        due_date = entities.get("date")
        due_time = entities.get("time")
        has_verb = any(v in text for v in self.ASSIGN_VERBS)
        # 指派意图：有明确被指派人且（有 @提及 或 含指派动词）
        is_assignment = bool(assignee and (mention or has_verb))
        return {
            "assigner": speaker_userid,
            "assignee": assignee,
            "due_date": due_date,
            "due_time": due_time,
            "content": text,
            "is_assignment": is_assignment,
        }

    def _extract_mention(self, text: str) -> Optional[str]:
        """提取 @提及对象（群聊 @某人 / @userid）"""
        m = re.search(r'@([A-Za-z0-9_\u4e00-\u9fff]{1,20})', text)
        if m:
            return m.group(1).strip()
        return None

    def format_for_confirmation(self, entities: Dict[str, Any]) -> str:
        """
        格式化实体用于复述确认
        
        Args:
            entities: 提取的实体
            
        Returns:
            str: 格式化后的确认文本
        """
        if not entities:
            return ""

        parts = []
        if "date" in entities:
            parts.append(f"日期：{entities['date']}")
        if "time" in entities:
            parts.append(f"时间：{entities['time']}")
        if "person" in entities:
            parts.append(f"人物：{entities['person']}")
        if "location" in entities:
            parts.append(f"地点：{entities['location']}")
        if "order_id" in entities:
            parts.append(f"订单号：{entities['order_id']}")
        if "amount" in entities:
            parts.append(f"金额：{entities['amount']}")
        if "phone" in entities:
            parts.append(f"电话：{entities['phone']}")

        if parts:
            return "，".join(parts)
        return ""

    def get_confirmation_prompt(self, entities: Dict[str, Any]) -> str:
        """
        生成确认提示语
        
        Args:
            entities: 提取的实体
            
        Returns:
            str: 确认提示语
        """
        formatted = self.format_for_confirmation(entities)
        if formatted:
            return f"请确认：{formatted}。正确请说「是」，修改请说「不对」。"
        return ""

    # === 各类实体提取 ===

    def _extract_date(self, text: str) -> Dict[str, str]:
        """提取日期实体"""
        result = {}

        # 相对日期
        date_map = {
            "今天": 0, "明天": 1, "后天": 2, "大后天": 3,
            "昨天": -1, "前天": -2
        }
        for word, offset in date_map.items():
            if word in text:
                target = datetime.now() + timedelta(days=offset)
                result["date"] = target.strftime("%Y-%m-%d")
                result["date_text"] = word
                return result

        # 周一..周日
        for i, day in enumerate(["周一", "周二", "周三", "周四", "周五", "周六", "周日"]):
            if day in text:
                today = datetime.now()
                days_ahead = (i - today.weekday()) % 7
                if days_ahead == 0:
                    days_ahead = 7
                target = today + timedelta(days=days_ahead)
                result["date"] = target.strftime("%Y-%m-%d")
                result["date_text"] = day
                return result

        # X月X日
        m = self._compiled_patterns['date_md'].search(text)
        if m:
            month, day = m.groups()
            result["date"] = f"{datetime.now().year}-{int(month):02d}-{int(day):02d}"
            result["date_text"] = m.group(0)

        return result

    def _extract_time(self, text: str) -> Dict[str, str]:
        """提取时间实体"""
        result = {}

        # X点X分
        m = self._compiled_patterns['time_hm'].search(text)
        if m:
            hour = int(m.group(1))
            minute = int(m.group(2))
            result["time"] = f"{hour:02d}:{minute:02d}"
            result["time_text"] = m.group(0)
            return result

        # X点
        m = self._compiled_patterns['time_h'].search(text)
        if m:
            prefix = m.group(1) or ""
            hour = int(m.group(2))
            if prefix in ("下", "晚") and hour < 12:
                hour += 12
            result["time"] = f"{hour:02d}:00"
            result["time_text"] = m.group(0)

        return result

    def _extract_person(self, text: str) -> Dict[str, str]:
        """提取人物实体"""
        result = {}

        # 姓氏+1-2字名（不使用负向后行，避免被后续汉字阻断）
        surname_pattern = re.compile(
            rf'([{self.SURNAMES}][\u4e00-\u9fff]{{1,2}})'
        )
        names = surname_pattern.findall(text)
        if names:
            # 过滤掉常见误匹配
            filtered = [n for n in names if n not in ["我们", "他们", "你们", "人们", "别人", "今天", "明天", "后天", "昨天", "前天", "上午", "下午", "晚上", "早上", "中午"]]
            if filtered:
                result["person"] = filtered[0]

        # 称谓匹配
        for title in self.TITLES:
            if title in text:
                # 尝试提取称谓前的人名
                idx = text.index(title)
                if idx > 0:
                    prefix = text[max(0, idx-2):idx]
                    if prefix and prefix[0] in self.SURNAMES:
                        result["person"] = prefix + title
                    else:
                        result["person"] = title
                else:
                    result["person"] = title
                break

        return result

    def _extract_location(self, text: str) -> Dict[str, str]:
        """提取地点实体"""
        result = {}

        # 城市列表
        cities = [
            "北京", "上海", "广州", "深圳", "杭州", "成都", "武汉",
            "西安", "南京", "重庆", "苏州", "天津", "长沙", "郑州", "大连",
            "青岛", "厦门", "福州", "昆明", "珠海", "宁波", "无锡", "佛山",
            "东莞", "石家庄", "太原", "沈阳", "长春", "哈尔滨", "合肥",
            "南昌", "济南", "南宁", "海口", "贵阳", "拉萨", "兰州",
            "西宁", "银川", "乌鲁木齐", "呼和浩特", "香港", "澳门", "台北"
        ]
        for city in cities:
            if city in text:
                result["location"] = city
                return result

        # 会议室/地点后缀
        location_pattern = re.compile(r'([\u4e00-\u9fff]{2,6})(?:会议室|办公室|大厅|前台|门口)')
        m = location_pattern.search(text)
        if m:
            result["location"] = m.group(0)

        return result

    def _extract_order_id(self, text: str) -> Dict[str, str]:
        """提取订单号"""
        result = {}
        m = self._compiled_patterns['order_id'].search(text)
        if m:
            result["order_id"] = m.group(1)
        return result

    def _extract_amount(self, text: str) -> Dict[str, str]:
        """提取金额"""
        result = {}
        m = self._compiled_patterns['amount'].search(text)
        if m:
            result["amount"] = m.group(0)
        return result

    def _extract_phone(self, text: str) -> Dict[str, str]:
        """提取手机号"""
        result = {}
        m = self._compiled_patterns['phone'].search(text)
        if m:
            result["phone"] = m.group(0)
        return result

    def _extract_email(self, text: str) -> Dict[str, str]:
        """提取邮箱"""
        result = {}
        m = self._compiled_patterns['email'].search(text)
        if m:
            result["email"] = m.group(0)
        return result

    def _extract_percentage(self, text: str) -> Dict[str, str]:
        """提取百分比"""
        result = {}
        m = self._compiled_patterns['percentage'].search(text)
        if m:
            result["percentage"] = m.group(0)
        return result

    def _extract_quantity(self, text: str) -> Dict[str, str]:
        """提取数量"""
        result = {}
        m = self._compiled_patterns['quantity'].search(text)
        if m:
            result["quantity"] = m.group(0)
        return result

    # === 上下文消歧 ===

    def _resolve_pronouns(self, text: str, entities: Dict[str, Any]) -> Dict[str, Any]:
        """
        上下文消歧：处理代词回指
        
        如用户说"他明天来"，上一轮提到"张三"，则"他"→"张三"
        """
        if not self._context:
            return entities

        # 检查文本中是否有代词
        for pronoun, entity_type in self.PRONOUNS.items():
            if pronoun in text:
                # 如果当前轮次没有提取到对应实体，从上下文补全
                if entity_type == "person" and "person" not in entities:
                    prev_person = self._context.get("person") or self._context.get("last_person")
                    if prev_person:
                        entities["person"] = prev_person
                        entities["person_resolved_from_context"] = True
                        logger.debug(f"代词消歧：'{pronoun}' -> '{prev_person}'")
                elif entity_type == "date" and "date" not in entities:
                    prev_date = self._context.get("date") or self._context.get("last_date")
                    if prev_date:
                        entities["date"] = prev_date
                        entities["date_resolved_from_context"] = True
                elif entity_type == "location" and "location" not in entities:
                    prev_loc = self._context.get("location") or self._context.get("last_location")
                    if prev_loc:
                        entities["location"] = prev_loc
                        entities["location_resolved_from_context"] = True

        return entities

    def update_context(self, entities: Dict[str, Any]):
        """
        更新上下文（每轮对话结束后调用）
        
        Args:
            entities: 当前轮次提取的实体
        """
        self._context.update(entities)
        # 保存最近实体用于消歧
        if "person" in entities:
            self._context["last_person"] = entities["person"]
        if "date" in entities:
            self._context["last_date"] = entities["date"]
        if "location" in entities:
            self._context["last_location"] = entities["location"]

    def reset_context(self):
        """重置上下文"""
        self._context = {}


# ==========================================
# 便捷函数
# ==========================================

def extract_entities(text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """便捷函数：提取实体"""
    extractor = EntityExtractor()
    return extractor.extract(text, context)


def format_entities(entities: Dict[str, Any]) -> str:
    """便捷函数：格式化实体"""
    extractor = EntityExtractor()
    return extractor.format_for_confirmation(entities)


# ==========================================
# 自测
# ==========================================

def run_self_test():
    """运行实体抽取器自测"""
    print("=" * 60)
    print("实体抽取增强模块 — 自测模式")
    print("=" * 60)

    extractor = EntityExtractor()

    # 测试 1: 日期时间提取
    print("\n[测试 1] 日期时间提取")
    entities = extractor.extract("明天下午3点开会")
    print(f"  输入: '明天下午3点开会'")
    print(f"  实体: {entities}")
    assert "date" in entities
    assert "time" in entities
    print("✅ 日期时间提取通过")

    # 测试 2: 人物提取
    print("\n[测试 2] 人物提取")
    entities = extractor.extract("提醒张三明天开会")
    print(f"  输入: '提醒张三明天开会'")
    print(f"  实体: {entities}")
    assert "person" in entities
    print("✅ 人物提取通过")

    # 测试 3: 地点提取
    print("\n[测试 3] 地点提取")
    entities = extractor.extract("北京天气怎么样")
    print(f"  输入: '北京天气怎么样'")
    print(f"  实体: {entities}")
    assert "location" in entities
    print("✅ 地点提取通过")

    # 测试 4: 订单号提取
    print("\n[测试 4] 订单号提取")
    entities = extractor.extract("订单号ABC1234567890状态")
    print(f"  输入: '订单号ABC1234567890状态'")
    print(f"  实体: {entities}")
    assert "order_id" in entities
    print("✅ 订单号提取通过")

    # 测试 5: 金额提取
    print("\n[测试 5] 金额提取")
    entities = extractor.extract("报销金额3000元")
    print(f"  输入: '报销金额3000元'")
    print(f"  实体: {entities}")
    assert "amount" in entities
    print("✅ 金额提取通过")

    # 测试 6: 复述确认格式化
    print("\n[测试 6] 复述确认格式化")
    entities = extractor.extract("明天下午3点在北京会议室提醒张三")
    formatted = extractor.format_for_confirmation(entities)
    print(f"  输入: '明天下午3点在北京会议室提醒张三'")
    print(f"  格式化: {formatted}")
    assert "日期" in formatted
    assert "时间" in formatted
    assert "地点" in formatted
    assert "人物" in formatted
    print("✅ 复述确认格式化通过")

    # 测试 7: 上下文消歧
    print("\n[测试 7] 上下文消歧")
    # 第一轮：提到张三
    entities1 = extractor.extract("张三明天开会")
    extractor.update_context(entities1)
    # 第二轮：说"他"
    entities2 = extractor.extract("他几点来")
    print(f"  第一轮: {entities1}")
    print(f"  第二轮（消歧后）: {entities2}")
    assert "person" in entities2
    assert entities2.get("person_resolved_from_context") == True
    print("✅ 上下文消歧通过")

    # 测试 8: 确认提示语
    print("\n[测试 8] 确认提示语")
    entities = extractor.extract("明天下午3点开会")
    prompt = extractor.get_confirmation_prompt(entities)
    print(f"  确认提示: {prompt}")
    assert "请确认" in prompt
    print("✅ 确认提示语通过")

    print(f"\n{'='*60}")
    print("所有自测通过 ✓")
    print("=" * 60)


if __name__ == "__main__":
    run_self_test()

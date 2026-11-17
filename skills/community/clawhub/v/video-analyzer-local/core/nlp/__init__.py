"""中文 NLP 增强模块 — NER命名实体识别 + 专业术语增强"""

import os
import re
from typing import Any, Dict, List, Optional

from ..logger import get_logger

logger = get_logger(__name__)


# ==================== COCO 80类 → 中文映射表 ====================
COCO_80_TO_CHINESE = {
    "person": "人",
    "bicycle": "自行车",
    "car": "汽车",
    "motorcycle": "摩托车",
    "airplane": "飞机",
    "bus": "公交车",
    "train": "火车",
    "truck": "卡车",
    "boat": "船",
    "traffic light": "红绿灯",
    "fire hydrant": "消防栓",
    "stop sign": "停车标志",
    "parking meter": "停车计时器",
    "bench": "长凳",
    "bird": "鸟",
    "cat": "猫",
    "dog": "狗",
    "horse": "马",
    "sheep": "羊",
    "cow": "牛",
    "elephant": "大象",
    "bear": "熊",
    "zebra": "斑马",
    "giraffe": "长颈鹿",
    "backpack": "背包",
    "umbrella": "雨伞",
    "handbag": "手提包",
    "tie": "领带",
    "suitcase": "行李箱",
    "frisbee": "飞盘",
    "skis": "滑雪板",
    "snowboard": "滑雪板",
    "sports ball": "球",
    "kite": "风筝",
    "baseball bat": "棒球棍",
    "baseball glove": "棒球手套",
    "skateboard": "滑板",
    "surfboard": "冲浪板",
    "tennis racket": "网球拍",
    "bottle": "瓶子",
    "wine glass": "酒杯",
    "cup": "杯子",
    "fork": "叉子",
    "knife": "刀",
    "spoon": "勺子",
    "bowl": "碗",
    "banana": "香蕉",
    "apple": "苹果",
    "sandwich": "三明治",
    "orange": "橙子",
    "broccoli": "西兰花",
    "carrot": "胡萝卜",
    "hot dog": "热狗",
    "pizza": "披萨",
    "donut": "甜甜圈",
    "cake": "蛋糕",
    "chair": "椅子",
    "couch": "沙发",
    "potted plant": "盆栽植物",
    "bed": "床",
    "dining table": "餐桌",
    "toilet": "马桶",
    "tv": "电视",
    "laptop": "笔记本电脑",
    "mouse": "鼠标",
    "remote": "遥控器",
    "keyboard": "键盘",
    "cell phone": "手机",
    "microwave": "微波炉",
    "oven": "烤箱",
    "toaster": "烤面包机",
    "sink": "水槽",
    "refrigerator": "冰箱",
    "book": "书",
    "clock": "时钟",
    "vase": "花瓶",
    "scissors": "剪刀",
    "teddy bear": "泰迪熊",
    "hair drier": "吹风机",
    "toothbrush": "牙刷",
    # 补充 ImageNet/Places 常见场景类
    "people": "人群",
    "vehicle": "车辆",
    "tree": "树",
    "building": "建筑",
    "mountain": "山",
    "river": "河流",
    "street": "街道",
    "office": "办公室",
    "classroom": "教室",
    "restaurant": "餐厅",
    "kitchen": "厨房",
    "bedroom": "卧室",
    "living room": "客厅",
    "bathroom": "浴室",
    "garden": "花园",
    "park": "公园",
    "hospital": "医院",
    "airport": "机场",
    "station": "车站",
    "bridge": "桥",
    "stadium": "体育场",
}


# 物体标签增强词典
SCENE_LABELS_CHINESE = {
    "indoor": "室内",
    "outdoor": "室外",
    "nature": "自然",
    "urban": "城市",
    "office": "办公室",
    "home": "家庭",
    "street": "街道",
    "forest": "森林",
    "mountain": "山",
    "beach": "海滩",
    "kitchen": "厨房",
    "bedroom": "卧室",
    "classroom": "教室",
    "restaurant": "餐厅",
    "shop": "商店",
    "factory": "工厂",
    "hospital": "医院",
    "library": "图书馆",
    "gym": "健身房",
    "park": "公园",
    "bridge": "桥",
    "parking_lot": "停车场",
    "dark_scene": "暗场景",
    "bright_scene": "明亮场景",
    "warm_tone": "暖色调",
    "cool_tone": "冷色调",
    "colorful": "色彩丰富",
    "green_nature": "绿色自然",
    "blue_sky": "蓝天",
    "orange_tone": "橙色暖调",
    "general": "一般场景",
}


class ChineseNLPEnhancement:
    """
    中文 NLP 增强模块。
    
    功能：
    1. 物体标签中文化
    2. 场景标签中文化
    3. 中文命名实体识别（人名/地名/机构名/品牌名）
    4. 专业术语识别
    5. 标点符号后处理（适配中文语境）
    """
    
    # 默认专业术语词典（可按需扩充）
    DEFAULT_TERMINOLOGY = {
        # 科技
        "AI": "人工智能",
        "APP": "应用程序",
        "API": "应用程序接口",
        "CPU": "处理器",
        "GPU": "显卡",
        "RAM": "内存",
        "SSD": "固态硬盘",
        "WiFi": "无线网络",
        "iOS": "苹果移动操作系统",
        "Android": "安卓操作系统",
        "SaaS": "软件即服务",
        "PaaS": "平台即服务",
        "IaaS": "基础设施即服务",
        # 金融
        "GDP": "国内生产总值",
        "IPO": "首次公开募股",
        "ROI": "投资回报率",
        "KPI": "关键绩效指标",
        "OKR": "目标与关键结果",
        # 互联网
        "UGC": "用户生成内容",
        "PGC": "专业生成内容",
        "MCN": "多频道网络",
        "KOL": "关键意见领袖",
        "DAU": "日活跃用户",
        "MAU": "月活跃用户",
    }
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.use_jieba = config.get("nlp", {}).get("use_jieba", True)
        self.use_ner = config.get("nlp", {}).get("use_ner", True)
        self.custom_terminology: Dict[str, str] = {}
        
        # 加载自定义术语词典
        terminology_path = config.get("nlp", {}).get("terminology_path")
        if terminology_path and os.path.exists(terminology_path):
            self._load_custom_terminology(terminology_path)
        
        # 合并用户自定义术语
        custom_terms = config.get("nlp", {}).get("custom_terminology", {})
        if custom_terms:
            self.custom_terminology.update(custom_terms)
        
        self._jieba = None
        self._ner_model = None
    
    def _load_custom_terminology(self, path: str):
        """从 JSON 文件加载自定义术语词典"""
        try:
            import json
            with open(path, "r", encoding="utf-8") as f:
                terms = json.load(f)
            if isinstance(terms, dict):
                self.custom_terminology.update(terms)
                logger.info(f"加载自定义术语 {len(terms)} 条")
        except Exception as e:
            logger.warning(f"自定义术语词典加载失败: {e}")
    
    def translate_object_labels(self, labels: List[str]) -> List[Dict[str, str]]:
        """
        将英文物体标签翻译为中文。
        
        Args:
            labels: 英文标签列表，如 ["person", "laptop", "cup"]
            
        Returns:
            中英对照列表，如 [{"en": "person", "zh": "人", "confidence": 1.0}, ...]
        """
        results = []
        for label in labels:
            label_lower = label.lower().strip()
            zh_label = COCO_80_TO_CHINESE.get(label_lower, label)
            results.append({
                "en": label,
                "zh": zh_label,
                "confidence": 1.0 if label_lower in COCO_80_TO_CHINESE else 0.5,
            })
        return results
    
    def translate_scene_labels(self, labels: List[str]) -> List[str]:
        """
        将英文场景标签翻译为中文。
        
        Args:
            labels: 英文场景标签列表
            
        Returns:
            中文标签列表
        """
        return [SCENE_LABELS_CHINESE.get(label.lower(), label) for label in labels]
    
    def recognize_entities(self, text: str) -> Dict[str, List[str]]:
        """
        中文命名实体识别。
        
        识别：人名(nr)、地名(ns)、机构名(nt)、品牌名/产品名
        
        Args:
            text: 输入文本
            
        Returns:
            {"persons": [...], "locations": [...], "organizations": [...], "brands": [...]}
        """
        if not text or len(text.strip()) == 0:
            return {"persons": [], "locations": [], "organizations": [], "brands": []}
        
        result = {
            "persons": [],
            "locations": [],
            "organizations": [],
            "brands": [],
        }
        
        # 尝试用 jieba + pkuseg 做中文分词 + NER
        try:
            import jieba
            import jieba.posseg as pseg
            
            # 确保 jieba 已初始化
            jieba.initialize()
            
            words = pseg.cut(text)
            
            for word, flag in words:
                if flag == "nr":  # 人名
                    result["persons"].append(word)
                elif flag == "ns":  # 地名
                    result["locations"].append(word)
                elif flag == "nt":  # 机构名
                    result["organizations"].append(word)
                elif flag == "nz":  # 其他专名（品牌等）
                    if word not in result["brands"]:
                        result["brands"].append(word)
            
        except ImportError:
            logger.debug("jieba 不可用，无法做中文NER")
        
        # 去重（保持顺序）
        for key in result:
            seen = set()
            unique = []
            for item in result[key]:
                if item not in seen:
                    seen.add(item)
                    unique.append(item)
            result[key] = unique
        
        return result
    
    def chinese_punctuation_fix(self, text: str) -> str:
        """
        中文标点后处理。
        
        - 将英文标点替换为中文标点
        - 适配中文语境（如逗号、句号、问号等）
        """
        if not text:
            return text
        
        # 英文标点 → 中文标点
        replacements = [
            (", ", "，"),
            (". ", "。"),
            ("? ", "？"),
            ("! ", "！"),
            (": ", "："),
            ("; ", "；"),
            ("(", "（"),
            (")", "）"),
        ]
        
        result = text
        for old, new in replacements:
            result = result.replace(old, new)
        
        return result
    
    def detect_terminology(self, text: str) -> List[Dict[str, str]]:
        """
        检测文本中的专业术语（英文缩写 + 自定义术语）。
        
        Args:
            text: 输入文本
            
        Returns:
            检测到的术语列表
        """
        found = []
        
        # 检测默认术语 + 自定义术语
        all_terms = {**self.DEFAULT_TERMINOLOGY, **self.custom_terminology}
        
        for term, meaning in all_terms.items():
            if term.lower() in text.lower():
                found.append({
                    "term": term,
                    "meaning": meaning,
                })
        
        return found
    
    def enhance_object_detection_results(self, objects: List[Dict]) -> List[Dict]:
        """
        增强物体检测结果：为每个物体添加中文标签。
        
        Args:
            objects: 原始检测结果 [{"name": "person", "confidence": 0.9, "bbox": [...]}, ...]
            
        Returns:
            增强后的结果 [{"name": "person", "name_zh": "人", "confidence": 0.9, "bbox": [...]}, ...]
        """
        for obj in objects:
            name = obj.get("name", "").lower()
            obj["name_zh"] = COCO_80_TO_CHINESE.get(name, obj.get("name", ""))
        return objects


# 便捷函数
def get_chinese_label(english_label: str) -> str:
    """获取英文物体的中文标签"""
    return COCO_80_TO_CHINESE.get(english_label.lower().strip(), english_label)


def batch_translate_labels(english_labels: List[str]) -> List[str]:
    """批量翻译英文标签为中文"""
    return [get_chinese_label(label) for label in english_labels]

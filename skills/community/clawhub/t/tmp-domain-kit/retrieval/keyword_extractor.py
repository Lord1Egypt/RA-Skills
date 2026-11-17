"""
关键词提取器 - 无 LLM 的关键词提取
从 schema 动态加载已知设备型号，正则匹配 + 词库匹配
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any


class KeywordExtractor:
    """基于规则和多词库的关键词提取"""

    def __init__(self, schema_dir: str = None):
        """
        Args:
            schema_dir: schema 目录路径，用于加载已知型号
        """
        if schema_dir is None:
            schema_dir = str(Path(__file__).parent.parent / "schema")
        self.schema_dir = Path(schema_dir)

        # 已知词库
        self.known_models = self._load_models_from_schema()
        self.known_scenarios = self._load_scenario_keywords()
        self.action_keywords = self._load_action_keywords()

    def _load_models_from_schema(self) -> List[str]:
        """从 schema 文件加载已知设备型号"""
        models = set()

        # 硬编码的已知型号（从 schema 和实际使用中总结）
        default_models = [
            "AM600", "AM400", "AM522", "H3U", "H5U",
            "AX100", "AX200", "AX300", "AX400",
            "Easy700", "InoDrive"
        ]
        models.update(default_models)

        # 尝试从 schema JSON 加载
        for schema_file in self.schema_dir.glob("*.json"):
            try:
                with open(schema_file, 'r', encoding='utf-8') as f:
                    schema = json.load(f)
                # 扫描 entity_types 中的 example/default 值
                for type_name, type_def in schema.get('entity_types', {}).items():
                    fields = type_def.get('fields', {})
                    for field_name, field_def in fields.items():
                        if field_name == 'model' and 'default' in field_def:
                            models.add(field_def['default'])
                        if 'enum' in field_def and field_name in ('device_type', 'type'):
                            for enum_val in field_def['enum']:
                                models.add(enum_val)
            except (json.JSONDecodeError, IOError):
                continue

        return sorted(models)

    def _load_scenario_keywords(self) -> List[str]:
        """加载场景关键词库"""
        return [
            # 自动化方向
            "输送带", "堆垛机", "分拣", "AGV", "视觉", "检测", "调度",
            "焊接", "包装", "码垛", "注塑", "冲压", "控制",
            "速度闭环", "张力控制", "定位", "搬运", "上下料",
            # WCS 方向
            "仓储", "物流", "入库", "出库", "路径规划", "任务分配",
            "库位", "巷道", "输送线", "提升机", "穿梭车",
            # 视觉方向
            "缺陷", "划痕", "尺寸偏差", "颜色异常", "表面检测",
            "目标检测", "图像分类", "OCR", "测量",
            # 通用
            "PLC", "HMI", "伺服", "变频器", "传感器",
            "Modbus", "OPC", "EtherCAT", "Profinet", "TCP"
        ]

    def _load_action_keywords(self) -> List[str]:
        """加载动作关键词映射"""
        return {
            "生成代码": ["代码", "编程", "写程序", "PLC程序", "ST代码", "模板"],
            "选型": ["选型", "选择", "推荐", "用什么", "哪个型号"],
            "约束检查": ["约束", "限制", "能不能", "是否支持", "兼容性"],
            "参数查询": ["参数", "规格", "配置", "多大", "多少"],
            "最佳实践": ["经验", "最佳实践", "怎么调", "调参", "注意"],
            "故障排查": ["故障", "报错", "异常", "问题", "不行", "失败"],
            "协议配置": ["协议", "通信", "连接", "接口", "Modbus", "OPC"]
        }

    def extract(self, text: str) -> Dict[str, List[str]]:
        """
        从文本提取关键词。

        Returns:
            {
                "models": ["AM600", ...],
                "scenarios": ["输送带", ...],
                "actions": ["生成代码", ...]
            }
        """
        result = {
            "models": [],
            "scenarios": [],
            "actions": []
        }

        text_lower = text.lower()

        # 1. 匹配设备型号（大小写敏感）
        for model in self.known_models:
            if model in text:
                result["models"].append(model)
            elif model.lower() in text_lower:
                result["models"].append(model)

        # 2. 匹配场景词
        for kw in self.known_scenarios:
            if kw in text:
                result["scenarios"].append(kw)

        # 3. 匹配动作词
        for action, triggers in self.action_keywords.items():
            for trigger in triggers:
                if trigger in text:
                    result["actions"].append(action)
                    break

        # 4. 正则补充：型号模式 (字母+数字)
        model_pattern = re.compile(r'\b([A-Z]{1,4}\d{2,4}[A-Z]?)\b')
        for match in model_pattern.findall(text):
            if match not in result["models"]:
                result["models"].append(match)

        return result


if __name__ == "__main__":
    ke = KeywordExtractor()

    test_cases = [
        "AM600 输送带控制程序怎么写",
        "堆垛机用什么协议通信",
        "视觉检测表面划痕的最佳实践",
        "H5U PLC 选型推荐",
        "AGV 路径规划约束条件"
    ]

    for text in test_cases:
        result = ke.extract(text)
        print(f"输入: {text}")
        print(f"  型号: {result['models']}")
        print(f"  场景: {result['scenarios']}")
        print(f"  动作: {result['actions']}")
        print()

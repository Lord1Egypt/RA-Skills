"""
手动录入提取器 - CLI 交互录入实体
支持交互式输入实体类型、字段值，自动生成 ID 和 provenance
"""

import sys
import json
from typing import Dict, Any, List
from datetime import datetime

from extractors.base import BaseExtractor


class ManualExtractor(BaseExtractor):
    """CLI 交互式手动录入"""

    # 支持的实体类型及其必填字段
    ENTITY_SCHEMAS = {
        "Device": {
            "fields": ["name", "model", "manufacturer"],
            "required": ["name", "model"]
        },
        "PLC": {
            "fields": ["model", "cpu_type", "memory_limit", "io_capacity", "supported_languages"],
            "required": ["model", "supported_languages"]
        },
        "IO_Module": {
            "fields": ["model", "type", "channel_count", "signal_type"],
            "required": ["model", "type", "channel_count"]
        },
        "CodeTemplate": {
            "fields": ["name", "language", "content", "parameters", "description"],
            "required": ["name", "language", "content"]
        },
        "Constraint": {
            "fields": ["rule", "scope", "severity", "rationale"],
            "required": ["rule", "severity"]
        },
        "BestPractice": {
            "fields": ["title", "content", "tags", "examples"],
            "required": ["title", "content"]
        },
        "Protocol": {
            "fields": ["name", "version", "message_format", "endpoints"],
            "required": ["name"]
        },
        "WCS_Device": {
            "fields": ["device_type", "model", "capacity", "speed", "communication"],
            "required": ["device_type", "model"]
        },
        "ScheduleRule": {
            "fields": ["name", "algorithm", "priority", "constraints"],
            "required": ["name", "priority"]
        },
        "DefectType": {
            "fields": ["name", "category", "characteristics", "severity_level"],
            "required": ["name", "category", "severity_level"]
        },
        "VisionModel": {
            "fields": ["name", "algorithm", "applicable_defects", "precision", "recall"],
            "required": ["name", "algorithm"]
        }
    }

    def extract(self, file_path: str = "") -> List[Dict[str, Any]]:
        """
        交互式录入实体。
        file_path 参数在此场景下可选，用于 provenance 记录。
        """
        return self.interactive_collect(file_path or "manual_input")

    def interactive_collect(self, source_path: str = "manual_input") -> List[Dict[str, Any]]:
        """交互式收集实体"""
        results = []
        provenance = self._make_provenance(source_path, confidence=0.95, source_type="manual")

        print("=== 领域知识手动录入 ===")
        print(f"支持的实体类型: {', '.join(self.ENTITY_SCHEMAS.keys())}")

        while True:
            print("\n--- 新建实体 ---")
            entity_type = self._prompt("实体类型 (输入 q 退出): ").strip()
            if entity_type.lower() == 'q':
                break

            if entity_type not in self.ENTITY_SCHEMAS:
                print(f"  不支持的类型: {entity_type}")
                print(f"  可选: {', '.join(self.ENTITY_SCHEMAS.keys())}")
                continue

            schema = self.ENTITY_SCHEMAS[entity_type]
            entity = {}
            tags = []

            for field in schema['fields']:
                required = field in schema['required']
                prompt_suffix = " *" if required else ""
                value = self._prompt(f"  {field}{prompt_suffix}: ")

                if not value and required:
                    print(f"  ⚠ {field} 为必填字段")
                    value = self._prompt(f"  {field} (必填): ")

                if value:
                    # 尝试解析 JSON 类型
                    entity[field] = self._parse_value(value)

            # 收集标签
            tag_input = self._prompt("  标签 (逗号分隔): ")
            if tag_input:
                tags = [t.strip() for t in tag_input.split(',') if t.strip()]
            tags.append(entity_type)

            results.append({
                "entity_type": entity_type,
                "entity": entity,
                "provenance": dict(provenance),
                "tags": tags
            })
            print(f"  ✓ 已添加 {entity_type} 实体")

        return results

    def _prompt(self, text: str) -> str:
        """输入提示"""
        try:
            return input(text).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return "q"

    def _parse_value(self, value: str) -> Any:
        """尝试解析值为合适的类型"""
        # 尝试 JSON 解析（列表、数字等）
        if value.startswith('['):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass
        # 尝试数字
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            pass
        return value

    def create_from_dict(self, entity_type: str, entity: Dict[str, Any],
                          tags: List[str] = None, source_path: str = "manual_input",
                          confidence: float = 0.95) -> Dict[str, Any]:
        """
        非交互式创建实体（供脚本调用）。

        Returns:
            完整的提取结果字典
        """
        provenance = self._make_provenance(source_path, confidence=confidence, source_type="manual")
        return {
            "entity_type": entity_type,
            "entity": entity,
            "provenance": provenance,
            "tags": tags or [entity_type]
        }


if __name__ == "__main__":
    # 非交互模式测试
    extractor = ManualExtractor()
    result = extractor.create_from_dict(
        entity_type="Device",
        entity={"name": "测试设备", "model": "TEST-001", "manufacturer": "美的"},
        tags=["TEST-001", "测试"],
        source_path="manual_test"
    )
    print(f"创建实体: {result['entity_type']}")
    print(f"  entity: {result['entity']}")
    print(f"  tags: {result['tags']}")
    print(f"  provenance: {result['provenance']}")

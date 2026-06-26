#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能运行器 - 主入口
整合数据获取、类型识别、模板选择的完整流程
"""

import sys
import os
from typing import Dict, Any, Optional

# 兼容直接运行和模块运行两种方式
if __package__:
    from .data_service import EntDataService
    from .entity_classifier import EntityClassifier, EntityType
    from .template_selector import TemplateSelector
else:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from data_service import EntDataService
    from entity_classifier import EntityClassifier, EntityType
    from template_selector import TemplateSelector


class SkillRunner:
    """企业百科技能运行器"""

    def __init__(self, skill_root: str = None):
        """
        初始化技能运行器

        Args:
            skill_root: Skill 根目录路径，如果不指定则自动检测
        """
        self.data_service = EntDataService()
        self.classifier = EntityClassifier()
        self.template_selector = TemplateSelector(skill_root)

    def run(self, entname: str, timeout: int = 60) -> Dict[str, Any]:
        """
        执行完整的企业百科生成流程

        Args:
            entname: 企业名称
            timeout: API请求超时时间（秒）

        Returns:
            包含模板和数据的字典：
            {
                "success": bool,
                "entity_type": str,        # 主体类型
                "template_name": str,      # 模板中文名称
                "template_path": str,      # 模板文件路径
                "template_content": str,   # 模板内容
                "data": dict,              # API返回的原始数据
                "error": str               # 错误信息（如果有）
            }
        """
        # 1. 获取数据
        result = self.data_service.fetch_all_data(entname, timeout)

        if not result["success"]:
            return {
                "success": False,
                "entity_type": None,
                "template_name": None,
                "template_path": None,
                "template_content": None,
                "data": None,
                "error": result["message"]
            }

        raw_data = result["data"]

        # 2. 识别主体类型
        entity_type = self.classifier.classify(raw_data)

        # 3. 获取对应模板
        template_info = self.template_selector.get_template_info(entity_type)

        try:
            template_content = self.template_selector.load_template(entity_type)
        except FileNotFoundError:
            template_content = None

        return {
            "success": True,
            "entity_type": entity_type.value,
            "template_name": template_info["name"],
            "template_path": template_info["path"],
            "template_relative_path": template_info["relative_path"],
            "template_content": template_content,
            "data": raw_data,
            "error": None
        }

    def get_entity_type(self, entname: str, timeout: int = 60) -> Optional[EntityType]:
        """
        仅获取企业的主体类型（不加载模板）

        Args:
            entname: 企业名称
            timeout: API请求超时时间（秒）

        Returns:
            EntityType 枚举值，如果查询失败返回 None
        """
        result = self.data_service.fetch_all_data(entname, timeout)

        if not result["success"]:
            return None

        return self.classifier.classify(result["data"])

    def get_template_for_type(self, entity_type: EntityType) -> Dict[str, Any]:
        """
        根据主体类型获取模板（不调用API）

        Args:
            entity_type: 主体类型

        Returns:
            模板信息字典
        """
        template_info = self.template_selector.get_template_info(entity_type)

        try:
            template_content = self.template_selector.load_template(entity_type)
        except FileNotFoundError:
            template_content = None

        return {
            "entity_type": entity_type.value,
            "template_name": template_info["name"],
            "template_path": template_info["path"],
            "template_content": template_content,
        }


# 模块级便捷函数
_runner_instance: Optional[SkillRunner] = None


def get_runner(skill_root: str = None) -> SkillRunner:
    """获取技能运行器单例"""
    global _runner_instance
    if _runner_instance is None:
        _runner_instance = SkillRunner(skill_root)
    return _runner_instance


def fetch_enterprise_data(entname: str, timeout: int = 60) -> Dict[str, Any]:
    """
    便捷函数：获取企业数据并自动选择模板

    这是供 SKILL.md 中脚本调用的主入口

    Args:
        entname: 企业名称
        timeout: API请求超时时间（秒）

    Returns:
        包含模板和数据的字典

    Example:
        >>> result = fetch_enterprise_data("安踏（中国）有限公司")
        >>> print(result["entity_type"])      # "company"
        >>> print(result["template_name"])    # "普通企业"
        >>> print(result["template_path"])    # "templates/company.md"
        >>> print(result["data"])             # 完整企业数据
    """
    return get_runner().run(entname, timeout)


__all__ = [
    'SkillRunner',
    'get_runner',
    'fetch_enterprise_data',
]


# 命令行入口
if __name__ == '__main__':
    import sys
    import json

    if len(sys.argv) < 2:
        print("用法: python -m scripts.skill_runner <企业名称>")
        sys.exit(1)

    entname = sys.argv[1]
    result = fetch_enterprise_data(entname)

    if result["success"]:
        print(f"企业名称: {entname}")
        print(f"主体类型: {result['entity_type']}")
        print(f"模板名称: {result['template_name']}")
        print(f"模板路径: {result['template_path']}")
        print(f"\n数据预览:")
        print(json.dumps(result["data"], ensure_ascii=False, indent=2)[:2000] + "...")
    else:
        print(f"查询失败: {result['error']}")
        sys.exit(1)

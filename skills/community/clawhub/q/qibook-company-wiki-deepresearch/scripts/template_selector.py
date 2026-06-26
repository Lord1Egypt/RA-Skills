#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模板选择器模块
根据主体类型选择对应的报告模板
"""

import sys
import os
from pathlib import Path
from typing import Dict, Optional

if __package__:
    from .entity_classifier import EntityType
else:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from entity_classifier import EntityType


class TemplateSelector:
    """模板选择器"""

    # 模板相对路径映射
    TEMPLATE_PATHS: Dict[EntityType, str] = {
        EntityType.COMPANY: "templates/company.md",
        EntityType.BRANCH: "templates/branch.md",
        EntityType.PERSONAL: "templates/personal.md",
        EntityType.HOSPITAL: "templates/organization/hospital.md",
        EntityType.SCHOOL: "templates/organization/school.md",
        EntityType.LAW_FIRM: "templates/organization/law_firm.md",
        EntityType.GOVERNMENT: "templates/organization/government.md",
        EntityType.SOCIAL: "templates/organization/social.md",
        EntityType.OTHER: "templates/organization/other.md",
    }

    # 模板中文名称映射
    TEMPLATE_NAMES: Dict[EntityType, str] = {
        EntityType.COMPANY: "普通企业",
        EntityType.BRANCH: "分支机构",
        EntityType.PERSONAL: "个体工商户",
        EntityType.HOSPITAL: "医院",
        EntityType.SCHOOL: "学校",
        EntityType.LAW_FIRM: "律师事务所",
        EntityType.GOVERNMENT: "政府机构",
        EntityType.SOCIAL: "社会组织",
        EntityType.OTHER: "其他组织",
    }

    def __init__(self, skill_root: str = None):
        """
        初始化模板选择器

        Args:
            skill_root: Skill 根目录路径，如果不指定则自动检测
        """
        if skill_root:
            self.skill_root = Path(skill_root)
        else:
            # 自动检测：当前文件的父目录的父目录
            self.skill_root = Path(__file__).parent.parent

    def get_template_path(self, entity_type: EntityType) -> str:
        """
        获取模板文件的绝对路径

        Args:
            entity_type: 主体类型

        Returns:
            模板文件的绝对路径
        """
        relative_path = self.TEMPLATE_PATHS.get(
            entity_type,
            self.TEMPLATE_PATHS[EntityType.OTHER]
        )
        return str(self.skill_root / relative_path)

    def get_template_relative_path(self, entity_type: EntityType) -> str:
        """
        获取模板文件的相对路径

        Args:
            entity_type: 主体类型

        Returns:
            模板文件的相对路径
        """
        return self.TEMPLATE_PATHS.get(
            entity_type,
            self.TEMPLATE_PATHS[EntityType.OTHER]
        )

    def load_template(self, entity_type: EntityType) -> str:
        """
        加载模板内容

        Args:
            entity_type: 主体类型

        Returns:
            模板文件内容

        Raises:
            FileNotFoundError: 模板文件不存在
        """
        template_path = self.get_template_path(entity_type)
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()

    def get_template_name(self, entity_type: EntityType) -> str:
        """
        获取模板的中文名称

        Args:
            entity_type: 主体类型

        Returns:
            模板中文名称
        """
        return self.TEMPLATE_NAMES.get(entity_type, "未知类型")

    def get_template_info(self, entity_type: EntityType) -> Dict[str, str]:
        """
        获取模板的完整信息

        Args:
            entity_type: 主体类型

        Returns:
            包含模板信息的字典
        """
        return {
            "type": entity_type.value,
            "name": self.get_template_name(entity_type),
            "path": self.get_template_path(entity_type),
            "relative_path": self.get_template_relative_path(entity_type),
        }

    def template_exists(self, entity_type: EntityType) -> bool:
        """
        检查模板文件是否存在

        Args:
            entity_type: 主体类型

        Returns:
            模板文件是否存在
        """
        template_path = Path(self.get_template_path(entity_type))
        return template_path.exists()

    def list_all_templates(self) -> Dict[str, Dict[str, str]]:
        """
        列出所有可用的模板

        Returns:
            所有模板信息的字典
        """
        templates = {}
        for entity_type in EntityType:
            info = self.get_template_info(entity_type)
            info["exists"] = self.template_exists(entity_type)
            templates[entity_type.value] = info
        return templates


# 模块级便捷函数
_selector_instance: Optional[TemplateSelector] = None


def get_selector(skill_root: str = None) -> TemplateSelector:
    """获取模板选择器单例"""
    global _selector_instance
    if _selector_instance is None:
        _selector_instance = TemplateSelector(skill_root)
    return _selector_instance


def get_template_path(entity_type: EntityType) -> str:
    """便捷函数：获取模板路径"""
    return get_selector().get_template_path(entity_type)


def load_template(entity_type: EntityType) -> str:
    """便捷函数：加载模板内容"""
    return get_selector().load_template(entity_type)


def get_template_info(entity_type: EntityType) -> Dict[str, str]:
    """便捷函数：获取模板信息"""
    return get_selector().get_template_info(entity_type)


__all__ = [
    'TemplateSelector',
    'get_selector',
    'get_template_path',
    'load_template',
    'get_template_info',
]

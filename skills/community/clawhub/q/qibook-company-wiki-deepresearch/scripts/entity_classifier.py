#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主体类型识别模块
根据 API 返回数据自动判断企业主体类型
"""

from enum import Enum
from typing import Dict, Any, Optional, List


class EntityType(Enum):
    """主体类型枚举"""
    COMPANY = "company"           # 普通企业
    BRANCH = "branch"             # 分支机构
    PERSONAL = "personal"         # 个体工商户
    HOSPITAL = "hospital"         # 医院
    SCHOOL = "school"             # 学校
    LAW_FIRM = "law_firm"         # 律师事务所
    GOVERNMENT = "government"     # 政府机构
    SOCIAL = "social"             # 社会组织
    OTHER = "other"               # 其他组织


class EntityClassifier:
    """主体类型分类器"""

    # ENTTYPE 和企业名称关键词映射（按优先级排序）
    KEYWORD_RULES: List[tuple] = [
        # (EntityType, [关键词列表], 是否仅匹配ENTTYPE)
        (EntityType.HOSPITAL, ["医院", "卫生院", "诊所", "门诊部", "医疗中心", "卫生服务中心", "卫生站", "卫生所"], False),
        (EntityType.SCHOOL, ["大学", "学院", "中学", "小学", "幼儿园", "学校", "教育学院", "职业技术学院", "技工学校"], False),
        (EntityType.LAW_FIRM, ["律师事务所", "律所"], False),
        (EntityType.GOVERNMENT, ["人民政府", "管理局", "委员会", "办公室", "监督管理", "行政机关", "公安局", "税务局", "市场监督"], False),
        (EntityType.SOCIAL, ["协会", "学会", "基金会", "商会", "联合会", "研究会", "促进会", "联谊会", "同业公会"], False),
    ]

    # 其他组织类型关键词（仅匹配ENTTYPE）
    OTHER_ORG_KEYWORDS = ["事业单位", "民办非企业", "社会团体", "机关法人"]

    # prompt字段到EntityType的映射
    PROMPT_MAPPING: Dict[str, EntityType] = {
        "一般企业": EntityType.COMPANY,
        "普通企业": EntityType.COMPANY,
        "分支机构": EntityType.BRANCH,
        "分公司": EntityType.BRANCH,
        "个体工商户": EntityType.PERSONAL,
        "个体户": EntityType.PERSONAL,
        "医院": EntityType.HOSPITAL,
        "医疗机构": EntityType.HOSPITAL,
        "学校": EntityType.SCHOOL,
        "教育机构": EntityType.SCHOOL,
        "律师事务所": EntityType.LAW_FIRM,
        "律所": EntityType.LAW_FIRM,
        "政府机构": EntityType.GOVERNMENT,
        "政府": EntityType.GOVERNMENT,
        "社会组织": EntityType.SOCIAL,
        "其他组织": EntityType.OTHER,
        "其他": EntityType.OTHER,
    }

    def classify(self, data: Dict[str, Any]) -> EntityType:
        """
        根据 API 返回数据判断主体类型

        API返回的data结构包含prompt字段，直接指明主体类型

        Args:
            data: 聚合接口返回的data字段内容

        Returns:
            EntityType 枚举值
        """
        # 优先使用API返回的prompt字段
        prompt = data.get("prompt", "") if isinstance(data, dict) else ""
        if prompt:
            # 直接匹配prompt
            if prompt in self.PROMPT_MAPPING:
                return self.PROMPT_MAPPING[prompt]
            # 模糊匹配
            for key, entity_type in self.PROMPT_MAPPING.items():
                if key in prompt:
                    return entity_type

        # 如果没有prompt字段，尝试从基础信息判断（兼容旧结构）
        ent_info = self._get_nested(data, ["ENT_INFO", "entInfo", "ent_info"]) or {}
        basic_info = self._get_nested(ent_info, ["BASIC", "basic"]) or {}
        headquarters = self._get_nested(ent_info, ["HEADQUARTERS", "headquarters"]) or {}

        enttype = self._get_field(basic_info, ["ENTTYPE", "enttype"]) or ""
        entname = self._get_field(basic_info, ["ENTNAME", "entname"]) or ""

        # 从get_enterprise_basic_info字段提取信息
        basic_info_str = data.get("get_enterprise_basic_info", "") if isinstance(data, dict) else ""

        # 优先级1：分支机构判断（HEADQUARTERS 非空 或 基础信息包含"分公司"）
        if self._is_branch(headquarters) or "分公司" in basic_info_str or "分支机构" in basic_info_str:
            return EntityType.BRANCH

        # 优先级2：个体工商户判断
        if "个体" in enttype or "个体" in basic_info_str:
            return EntityType.PERSONAL

        # 优先级3-7：特殊机构类型判断（基于关键词）
        entity_type = self._classify_by_keywords(enttype, entname)
        if entity_type:
            return entity_type

        # 优先级8：其他组织类型
        if self._is_other_organization(enttype):
            return EntityType.OTHER

        # 优先级9：默认为普通企业
        return EntityType.COMPANY

    def _is_branch(self, headquarters: Dict[str, Any]) -> bool:
        """判断是否为分支机构"""
        if not headquarters:
            return False
        # 检查是否有任何非空值
        return any(v for v in headquarters.values() if v)

    def _classify_by_keywords(self, enttype: str, entname: str) -> Optional[EntityType]:
        """根据关键词匹配判断类型"""
        combined_text = f"{enttype} {entname}"

        for entity_type, keywords, enttype_only in self.KEYWORD_RULES:
            search_text = enttype if enttype_only else combined_text
            for keyword in keywords:
                if keyword in search_text:
                    return entity_type

        return None

    def _is_other_organization(self, enttype: str) -> bool:
        """判断是否为其他组织类型"""
        for keyword in self.OTHER_ORG_KEYWORDS:
            if keyword in enttype:
                return True
        return False

    def _get_nested(self, data: Dict[str, Any], keys: List[str]) -> Optional[Dict[str, Any]]:
        """从字典中获取嵌套值，支持多个可能的键名"""
        if not data:
            return None
        for key in keys:
            if key in data:
                return data[key]
        return None

    def _get_field(self, data: Dict[str, Any], keys: List[str]) -> Optional[str]:
        """从字典中获取字段值，支持多个可能的键名"""
        if not data:
            return None
        for key in keys:
            if key in data and data[key]:
                return str(data[key])
        return None

    def get_type_info(self, entity_type: EntityType) -> Dict[str, str]:
        """获取主体类型的详细信息"""
        type_info = {
            EntityType.COMPANY: {"name": "普通企业", "description": "具有独立法人资格的企业"},
            EntityType.BRANCH: {"name": "分支机构", "description": "企业的分公司或办事处"},
            EntityType.PERSONAL: {"name": "个体工商户", "description": "个体经营者"},
            EntityType.HOSPITAL: {"name": "医院", "description": "医疗卫生机构"},
            EntityType.SCHOOL: {"name": "学校", "description": "教育机构"},
            EntityType.LAW_FIRM: {"name": "律师事务所", "description": "法律服务机构"},
            EntityType.GOVERNMENT: {"name": "政府机构", "description": "政府部门或行政机关"},
            EntityType.SOCIAL: {"name": "社会组织", "description": "协会、基金会等社会团体"},
            EntityType.OTHER: {"name": "其他组织", "description": "其他类型的组织机构"},
        }
        return type_info.get(entity_type, {"name": "未知类型", "description": ""})


# 模块级便捷函数
_classifier_instance: Optional[EntityClassifier] = None


def get_classifier() -> EntityClassifier:
    """获取分类器单例"""
    global _classifier_instance
    if _classifier_instance is None:
        _classifier_instance = EntityClassifier()
    return _classifier_instance


def classify(data: Dict[str, Any]) -> EntityType:
    """
    便捷函数：判断主体类型

    Args:
        data: 聚合接口返回的完整数据

    Returns:
        EntityType 枚举值
    """
    return get_classifier().classify(data)


def get_type_name(entity_type: EntityType) -> str:
    """获取主体类型的中文名称"""
    return get_classifier().get_type_info(entity_type)["name"]


__all__ = [
    'EntityType',
    'EntityClassifier',
    'get_classifier',
    'classify',
    'get_type_name',
]

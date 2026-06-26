#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业百科 Skill Scripts 统一入口

提供统一的企业数据获取和模板选择接口
"""

# 版本信息
__version__ = '2.0.0'

# 模块映射：属性名 -> (模块名, 原始名)
_LAZY_IMPORTS = {
    # 数据服务
    'EntDataService': ('data_service', 'EntDataService'),
    'fetch_all_data': ('data_service', 'fetch_all_data'),
    # 类型识别
    'EntityType': ('entity_classifier', 'EntityType'),
    'EntityClassifier': ('entity_classifier', 'EntityClassifier'),
    'classify': ('entity_classifier', 'classify'),
    'get_type_name': ('entity_classifier', 'get_type_name'),
    # 模板选择
    'TemplateSelector': ('template_selector', 'TemplateSelector'),
    'get_template_path': ('template_selector', 'get_template_path'),
    'load_template': ('template_selector', 'load_template'),
    'get_template_info': ('template_selector', 'get_template_info'),
    # 运行器
    'SkillRunner': ('skill_runner', 'SkillRunner'),
    'fetch_enterprise_data': ('skill_runner', 'fetch_enterprise_data'),
}


def __getattr__(name):
    """延迟导入，避免 python -m scripts.skill_runner 时的 RuntimeWarning"""
    if name in _LAZY_IMPORTS:
        module_name, attr_name = _LAZY_IMPORTS[name]
        import importlib
        module = importlib.import_module(f'.{module_name}', __name__)
        return getattr(module, attr_name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


# 导出列表
__all__ = list(_LAZY_IMPORTS.keys())

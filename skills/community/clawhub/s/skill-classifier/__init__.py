# -*- coding: utf-8 -*-
"""
kt_skill_list_skill - 增强版 OpenClaw 技能列表生成工具

功能特性：
- ✅ 多格式输出：Markdown / JSON / HTML
- ✅ 分类统计：9 大类 30+ 子类自动分类
- ✅ 状态图标：Ready / NeedSetup / Disabled
- ✅ 元数据：版本号、作者、依赖检查
- ✅ 增量更新：检测新增/删除/变化的技能
- ✅ 自动分类：基于规则的新技能自动分类
- ✅ 重复检测：发现功能重复的技能
- ✅ Web 界面：交互式 HTML，支持搜索、筛选、排序
- ✅ 灵活过滤：按状态、关键词、分类过滤

架构：
- data/ - 数据层（OpenClaw CLI、文件系统、元数据）
- classifier/ - 分类层（映射表、自动分类）
- exporter/ - 导出层（Markdown、JSON、HTML）
- utils/ - 工具层（翻译、差异对比、配置）
"""

__version__ = "1.0.1"
__author__ = "Kun. Tao"

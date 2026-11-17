# -*- coding: utf-8 -*-
"""
openclaw-skill-manager - OpenClaw 技能分类与统计工具

功能特性：
- ✅ 多格式输出：Markdown / JSON / HTML
- ✅ 分类统计：10 大类 48 子类自动归类，支持用户覆盖层
- ✅ 状态图标：Ready / NeedSetup / Disabled（含 anyBins 组判定）
- ✅ 元数据：版本号、作者、emoji、来源、主页链接
- ✅ 增量更新：检测新增/删除/变化的技能
- ✅ 重复检测：名称模式 + 描述相似度
- ✅ 使用统计：skill_usage 表 / curator 双数据源
- ✅ 依赖关系图：mermaid（md）/ SVG（html）
- ✅ 批量启停：skills.entries.<名>.enabled，自动备份 + 验证
- ✅ 更新检查：git 轨 / ClawHub 轨，只报告不升级
- ✅ 远端推送：飞书云文档 / Notion 页面（凭据走环境变量）
- ✅ Web 界面：交互式 HTML，支持搜索、筛选、表头排序

架构：
- data/ - 数据层（CLI、文件系统、元数据、统计、依赖、更新、启停）
- classifier/ - 分类层（映射表、覆盖层、重复检测）
- exporter/ - 导出层（Markdown、JSON、HTML、飞书、Notion）
- utils/ - 工具层（配置、汉化、差异、HTTP 客户端）
- tests/ - pytest 单测
"""

__version__ = "1.2.6"
__author__ = "kuntao2011"

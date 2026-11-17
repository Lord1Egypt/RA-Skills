# Changelog

All notable changes to this skill will be documented in this file.

## [7.0.1] - 2026-07-12

### Fixed (SkillSpector 安全审计修复)
- SSD3 High: 移除 JSON 中的 memory_keywords 字段，改为 memory_keyword_count（仅记录数量）
- SSD3 High: 推荐理由不再暴露匹配的记忆关键词，改为 generic "记忆碰撞匹配"
- MCP Tool Poisoning: description 声明完整行为范围（网络/文件/记忆访问/推送）
- 硬编码 memory 路径改为 TRAE_MEMORY_PATH 环境变量
- 硬编码 skillhub CLI 路径改为 shutil.which() 动态查找
- 硬编码 IMA_KB_ID 改为环境变量
- MCP Least Privilege: SKILL.md 增加权限声明段落
- Missing User Warnings: README 中英文版增加数据访问/传输警告
- 凭证安全指引：README 增加环境变量安全使用提示

## [7.0.0] - 2026-07-12

### Added
- 7 维度推荐算法（新增 china_first 国内优先 + active_developer 活跃开发者维度）
- 11 分类搜索 + 6 关键词搜索，扫描量从 340 提升至 1000+ 候选
- 3 级权重记忆碰撞（project_memory×3 / topics×2 / user_profile×1）
- 活跃开发者发现机制（按 ownerName 聚合 + 活跃度评分）
- evaluation/reports API 深度评估（AI 6维评分 + 双实验室安全审计）
- 三处存放推送（Obsidian inbox / IMA FIM 知识库 / 飞书云文档）
- TRAE Schedule 定时任务（每天 06:50 北京时间）
- 简报格式升级（TL;DR / 维度分组 / 能力解读 / 下一步 / 痛点匹配分组）
- 与 ClawHub Daily 差异化定位

### Changed
- 技能名称从 skillhub-cn-daily 改为 SkillHub Daily
- 扫描策略从纯排行榜改为排行榜+分类搜索+关键词搜索
- 推荐维度从 6 个扩展到 7 个

### Fixed
- china_first 维度增加最低门槛（50 安装或 10 星），避免推荐空壳技能

## [2.0.0] - 2026-07-11

### Added
- 使用 skillhub CLI 替代 agent-browser 抓取
- 6 维度推荐算法
- 7 天跨维度去重机制

## [1.0.0] - 2026-07-11

### Added
- 初始版本，使用 agent-browser 抓取 SkillHub.cn 排行榜

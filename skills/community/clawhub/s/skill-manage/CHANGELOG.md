# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-04-17

### 变更
- 重命名项目为 `skill-manage`（避免 ClawHub slug 冲突）
- 脚本文件名 `skill_manager.py` → `skill_manage.py`
- 更新所有文档和命令中的项目名称

## [1.1.0] - 2026-04-17

### 新增
- SKILL.md 增加 `description_zh` 中英文双语描述
- SKILL.md 增加 `author`、`email`、`wechat_mp` 作者信息
- SKILL.md 增加 `voice_commands` 语音指令列表（6条）
- 增加 `.github/workflows/clawhub-auto-publish.yml` 自动同步到 ClawHub

## [1.0.0] - 2026-04-14

### 首发
- 彻底卸载功能：残留扫描 + 凭证安全提示 + Dry Run
- 彻底卸载支持 --dry-run 先预览再执行
- 彻底卸载支持 --force 跳过确认
- 补充 README.md / .gitignore / LICENSE / SKILL.md frontmatter

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [6.2.0] - 2026-06-03

### 🎉 Major Release: 跨平台融合版 (Cross-Platform Universal Edition)

融合 v6.1 (qclaw 优化版) + v5.0 评审建议 + 双模式增强，作为跨平台通用版发布。

### ✨ Added (新增)

- **首次加载必须询问使用模式**（模式 A 常规 / 模式 B Cron）
- **Cron 模式跳过记忆扫描**：直接使用 prompt 中的痛点
- **7 个平台提示词模板**：qclaw / WorkBuddy / OpenClaw / Hermes / 纯脚本 / Obsidian / 微信
- **跨平台凭证搜索**：4 级优先级（环境变量 → 本地 config → qclaw → workbuddy）
- **推送职责解耦**：外部编排负责推送，Skill 仅生成内容
- **修复 v6.1 隐藏 bug**：`argparse` 格式化冲突（`%` 字符）
- **环境版本验证**：Python ≥ 3.10、Node.js ≥ 18
- **Python 自动回退检测**：当前解释器过低时尝试 python3.10/3.11/3.12
- **何时不应触发清单**：7 条边界场景
- **完整中英 README**：参考 eze-is/web-access 范式

### 🔧 Changed (变更)

- 描述精简：323 字符 → 230 字符
- 元数据统一：SKILL.md / _meta.json / plugin.json 全部 6.2.0
- 添加 `allowed-tools`：Read, Write, Bash, Glob, Grep
- `User-Agent` 升级为 `SkillHub-Daily/6.2`
- 隐私保护：所有真实 ID/路径替换为占位符
- 简报模板通用化（移除个人化示例）

### 🐛 Fixed (修复)

- v6.1 `argparse` 格式化崩溃 bug
- 版本号不一致问题（SKILL.md 5.0 vs _meta.json 1.0.0）
- 飞书文档 `create` 后内容为空（增加 `read` 验证步骤）

### 📚 Documentation (文档)

- 新增 `references/setup-wizard.md`：首次安装向导
- 新增 `references/platform-adapters.md`：跨平台适配
- 新增 `references/prompt-templates.md`：Cron 模板
- 新增 `README.md` 中英双语版
- 完善 `config.md`：环境验证 + Windows Cron + 凭证多路径
- 完善 `briefing-template.md`：通用化示例

## [6.1.0] - Previous Release

- 独立 `push_to_ima.py` 脚本
- 独立 `briefing-template.md`
- README.md
- .gitignore
- 痛点来源按调用方式动态选择

## [5.0.0] - Earlier Release

- 基础数据抓取
- 240 个 Skill 扫描
- 收藏率 / 潜力分计算
- 隐藏金子识别

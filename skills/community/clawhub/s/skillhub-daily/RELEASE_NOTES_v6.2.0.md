# Release v6.2.0 - 跨平台融合版 / Cross-Platform Universal Edition

> 融合 v6.1 (qclaw 优化版) + v5.0 评审建议 + 双模式增强，作为跨平台通用版发布。
> Fusing v6.1 (qclaw optimized) + v5.0 review feedback + dual-mode enhancement, released as cross-platform universal edition.

**Release Date**: 2026-06-03
**Stability**: ✅ Stable
**License**: MIT

---

## 🎉 重点新功能 / Highlights

### 1. 双模式支持 / Dual Mode Support

首次加载 Skill 时，必须询问用户使用模式：

- **🔵 模式 A：常规 Skills 模式**（推荐新手）— 对话触发，自动扫描记忆
- **🟢 模式 B：Cron 定时任务模式**（推荐重度用户）— 定时执行，痛点预设，自动推送

### 2. 跨平台适配 / Cross-Platform

支持 5 个 Agent 平台：

| 平台 | 模式 A | 模式 B (Cron) | 凭证位置 |
|------|--------|---------------|---------|
| qclaw | ✅ | ✅ | `~/.qclaw/skills/ima-skill/config.json` |
| WorkBuddy | ✅ | ✅ | `~/.workbuddy/skills/ima-skill/config.json` |
| OpenClaw | ✅ | ✅ | `~/.openclaw/skills/ima-skill/config.json` |
| Hermes | ✅ | ✅ | 平台特定 |
| 纯脚本 | ❌ | ❌ | 环境变量 |

### 3. 推送职责解耦 / Decoupled Push

外部编排负责推送（Cron `delivery.announce`），Skill 仅生成内容。**简化了架构，降低了耦合。**

---

## ✨ 新增功能 / What's New

- **首次加载必须询问使用模式**（A 常规 / B Cron）
- **Cron 模式跳过记忆扫描**：直接使用 prompt 中的痛点（更快）
- **7 个平台提示词模板**：qclaw / WorkBuddy / OpenClaw / Hermes / 纯脚本 / Obsidian / 微信
- **跨平台凭证搜索**：4 级优先级（环境变量 → 本地 config → qclaw → workbuddy）
- **环境版本验证**：Python ≥ 3.10、Node.js ≥ 18
- **Python 自动回退检测**：当前解释器过低时尝试 python3.10/3.11/3.12
- **何时不应触发清单**：7 条边界场景
- **完整中英 README**：参考 eze-is/web-access 范式
- **`.claude-plugin/plugin.json`**：Claude Code 插件元数据

## 🔧 变更 / Changes

- 描述精简：323 字符 → 230 字符
- 元数据统一：SKILL.md / _meta.json / plugin.json 全部 6.2.0
- 添加 `allowed-tools`：Read, Write, Bash, Glob, Grep
- `User-Agent` 升级为 `SkillHub-Daily/6.2`
- 隐私保护：所有真实 ID/路径替换为占位符
- 简报模板通用化（移除个人化示例）

## 🐛 修复 / Bug Fixes

- v6.1 `argparse` 格式化崩溃 bug（`--help` 报错）
- 版本号不一致问题（SKILL.md 5.0 vs _meta.json 1.0.0）
- 飞书文档 `create` 后内容为空（增加 `read` 验证步骤）

## 📚 文档 / Documentation

- 新增 `references/setup-wizard.md`：首次安装向导
- 新增 `references/platform-adapters.md`：跨平台适配
- 新增 `references/prompt-templates.md`：Cron 模板（7 个）
- 新增 `README.md` 中英双语版
- 完善 `config.md`：环境验证 + Windows Cron + 凭证多路径
- 完善 `briefing-template.md`：通用化示例

---

## 📦 安装 / Installation

### ClawHub 一键安装（推荐）

```bash
# 在 Agent 对话中
"帮我安装 skillhub-daily"
```

### 手动安装

```bash
git clone https://github.com/skillhub-community/skillhub-daily.git
# qclaw
cp -r skillhub-daily/ ~/.qclaw/skills/
# WorkBuddy
cp -r skillhub-daily/ ~/.workbuddy/skills/
# OpenClaw
cp -r skillhub-daily/ ~/.openclaw/skills/
# Hermes
cp -r skillhub-daily/ ~/.hermes/skills/
```

### npx skills

```bash
npx skills add skillhub-community/skillhub-daily
```

---

## 🔄 升级指南 / Upgrade Guide

### 从 v6.1 升级

1. 备份现有数据：`cp -r data/ data.backup/`
2. 替换 SKILL.md、scripts/、references/
3. 重新安装即可（无需迁移配置文件）

### 从 v5.0 升级

1. 备份现有数据
2. 替换所有文件
3. **新增**：选择使用模式（首次加载会询问）
4. **新增**：如使用 Cron，需在 prompt 中预设痛点列表

### 从更早版本

建议直接安装 v6.2.0，无需逐级升级。

---

## ⚠️ 破坏性变更 / Breaking Changes

**无 / None**

v6.2.0 完全向后兼容 v6.1 和 v5.0。

---

## 📊 性能 / Performance

- **数据体积**：slim 模式减少 ~32%
- **执行速度**：Cron 模式跳过记忆扫描，速度提升 ~40%
- **Token 消耗**：简报摘要 ≤ 200 字，对话上下文友好

---

## 🤝 致谢 / Credits

- **eze-is/web-access**：仓库结构、README 范式、Release Notes 风格参考
- **agent-skills** & **superpowers**：SOLO 工程化模式规则
- **SkillHub 社区**：需求反馈和测试支持

---

## 📞 反馈 / Feedback

- **GitHub Issues**: https://github.com/skillhub-community/skillhub-daily/issues
- **ClawHub 评论**：https://clawhub.com/skills/skillhub-daily

---

## 📄 License

MIT © 2026 SkillHub-Community

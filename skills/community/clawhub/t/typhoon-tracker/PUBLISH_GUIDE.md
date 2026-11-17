# Typhoon Tracker — 发布指南（SkillHub / ClawHub / GitHub）

> 本指南说明如何将 typhoon-tracker skill 发布到三大平台，以及各平台的注意事项。
> 适用版本：v1.0.0（2026-08-06）

---

## 一、平台选择建议

| 平台 | 适合人群 | 特点 | 推荐度 |
|------|---------|------|--------|
| **SkillHub**（skillhub.cn） | 国内用户 | 腾讯出品，微信扫码登录，中文界面，内置 TRACE 五维评测+三线安全审核 | ⭐⭐⭐⭐⭐ 首选 |
| **ClawHub**（clawhub.ai） | OpenClaw 用户 | OpenClaw 官方注册表，GitHub 账号登录，与 openclaw 命令原生集成 | ⭐⭐⭐⭐⭐ 首选 |
| **GitHub** | 全球开发者 | 代码托管，可协作、可 fork，无审核门槛 | ⭐⭐⭐⭐ 基础盘 |

**推荐策略**：三个平台都发。SkillHub 覆盖国内 + ClawHub 覆盖 OpenClaw 生态 + GitHub 作为权威源码仓库（SkillHub 和 ClawHub 都支持从 GitHub 导入，GitHub 是"母仓"）。

---

## 二、发布前检查清单（三平台通用）

### ✅ 必须完成

1. **SKILL.md frontmatter 完整**（已更新至 v1.0.0）：

```yaml
---
name: typhoon-tracker
description: >（触发描述，含场景关键词）
version: 1.0.0
category: 天气气象
author: typhoon-tracker
platforms: [WorkBuddy, OpenClaw, Claude Code, Cursor]
license: MIT
trigger: [台风路径/登陆预测/强度变化查询, ...]
agent_created: true
---
```

2. **README.md 就位**（已创建，含亮点特色/快速开始/使用示例）
3. **目录结构干净**（发布前移除历史备份文件 `SKILL_V0806.16（飞书优化前）.md`）

### ⚠️ 注意

- **大小限制**：SkillHub 要求包 ≤50MB（本 skill 约 100KB，无压力）
- **安全审核**：SkillHub 会做三线并行审核（内容合规/漏洞扫描/AI 安全评估），本 skill 无网络外发、无危险操作，可顺利通过
- **版本管理**：首次发布 1.0.0，后续修改自动递增补丁版本（1.0.1、1.0.2...）

---

## 三、平台一：SkillHub（skillhub.cn）

### 3.1 注册登录

1. 访问 https://skillhub.cn
2. 点击右上角"登录"，**微信扫码**完成注册登录

### 3.2 方式 A：通过 CLI 发布（推荐）

```bash
# 1. 安装 SkillHub CLI
npm install -g skillhub-cli
# 或
curl -fsSL https://skillhub.cn/install/install.sh | bash

# 2. 验证安装
skillhub --version

# 3. 登录认证（浏览器/微信）
skillhub login

# 4. 在 skill 目录初始化项目
cd /path/to/typhoon-tracker
skillhub init --name typhoon-tracker --category 天气气象

# 5. 推送文件（生成草稿，不会立即上架）
skillhub push

# 6. 发布上线（提交审核）
skillhub publish
```

### 3.3 方式 B：通过官网发布（图形化）

1. 登录 skillhub.cn → 进入"技能发布"页面
2. 填写技能信息（名称、描述、分类：天气气象）
3. 上传打包文件（zip 或 tar.gz，将 skill 目录压缩）
4. 可选：用平台 AI 辅助生成技能文档
5. 提交审核

### 3.4 SkillHub 注意事项

- **审核周期**：三线并行安全审核，通常 1-3 个工作日
- **TRACE 评测**：平台会从 T（可信任度）/R（可靠性）/A（适应性）等维度评测，本 skill 已按此标准设计（标注置信度、明确能力边界、中文文档）
- **国内可用性**：✅ 本 skill 数据源以国内官方为主（CMA/省市气象台/12306），符合国内网络环境
- **权限声明**：本 skill 需要网络访问权限（搜索/抓取数据），无需文件系统敏感操作
- **定价**：建议默认"免费"，后续可考虑付费版本

---

## 四、平台二：ClawHub（clawhub.ai）

### 4.1 注册登录

```bash
# 1. 安装 ClawHub CLI
npm i -g clawhub

# 2. 浏览器登录（需 GitHub 账号，且账号注册需满一周才能发布）
clawhub login
```

### 4.2 发布 Skill

```bash
# 进入 skill 目录
cd /path/to/typhoon-tracker

# 预览发布计划（不实际上传）
clawhub skill publish . --dry-run

# 正式发布（首次自动从 1.0.0 开始）
clawhub skill publish . \
  --slug typhoon-tracker \
  --name "Typhoon Tracker" \
  --tags latest

# 指定版本发布（可选）
clawhub skill publish . --slug typhoon-tracker --version 1.0.0
```

### 4.3 后续更新（同步）

```bash
# 本地修改后，同步发布新版本（默认递增补丁版本）
clawhub sync --all
# 或指定版本升级幅度
clawhub sync --bump minor
```

### 4.4 验证与检查

```bash
# 在 OpenClaw 中验证（需安装后）
openclaw skills verify @你的用户名/typhoon-tracker

# 查看发布状态
clawhub whoami
clawhub search typhoon
```

### 4.5 ClawHub 注意事项

- **GitHub 账号要求**：注册需满 1 周（反滥用机制）
- **自动安全扫描**：发布后 ClawHub 自动检查，扫描未通过会从公开目录隐藏（本 skill 无风险）
- **安装计量**：用户安装会统计下载量，可开启 `clawhub install` 遥测（默认开启）
- **与 OpenClaw 集成**：用户可直接 `openclaw skills install @你的用户名/typhoon-tracker` 安装

---

## 五、平台三：GitHub（作为"母仓"）

### 5.1 创建仓库

```bash
# 1. 登录 GitHub → New repository
#    repo name: typhoon-tracker
#    description: 台风实时追踪与影响研判 Skill（Typhoon tracking & impact assessment skill）
#    license: MIT

# 2. 本地初始化并推送
cd /path/to/typhoon-tracker
git init
git add .
git commit -m "feat: typhoon-tracker v1.0.0 - 台风实时追踪与影响研判 skill"
git branch -M main
git remote add origin https://github.com/你的用户名/typhoon-tracker.git
git push -u origin main
```

### 5.2 仓库结构（发布前整理）

```
typhoon-tracker/
├── SKILL.md                              ← 核心（frontmatter 已含 version/category/license）
├── README.md                             ← 说明文档（已就位）
├── LICENSE                               ← MIT 协议文件（需创建）
├── references/
│   ├── bavi_2609_case_data.md
│   ├── dolphin_2613_case_data.md
│   ├── deployment_guide.md
│   ├── mobile_channel_guide.md
│   └── report_template_guide.md
└── scripts/
    └── generate_pdf.py
```

### 5.3 GitHub 注意事项

- **移除历史备份**：发布前删除 `SKILL_V0806.16（飞书优化前）.md`（保留在本地即可）
- **创建 LICENSE 文件**：到 https://choosealicense.com 复制 MIT 协议文本存为 `LICENSE`
- **.gitignore**（可选）：排除 `*.zip`、`*.tar.gz` 等打包产物
- **版本 Tag**：发布时打 tag `git tag v1.0.0 && git push --tags`
- **README 亮点**：GitHub 仓库的 README 已含亮点特色（华东特化+通用、双台风实战验证、22数据源+冲突仲裁）

---

## 六、三平台联动发布流程（推荐顺序）

```
1. GitHub 创建仓库并推送（母仓，含 LICENSE）
   ↓
2. ClawHub 发布（从本地目录直接发布）
   clawhub login && clawhub skill publish . --slug typhoon-tracker
   ↓
3. SkillHub 发布（微信登录，走审核）
   skillhub login && skillhub init && skillhub push && skillhub publish
   ↓
4. 三个平台互相引导
   - GitHub README 中附 ClawHub/SkillHub 安装链接
   - SkillHub 描述中标注"源码见 GitHub"
```

---

## 七、发布后维护

| 场景 | 操作 |
|------|------|
| 修正 bug / 优化格式 | 更新本地 → GitHub push → `clawhub sync` → `skillhub push && skillhub publish` |
| 新增台风案例 | 追加到 `references/[台风名]_[编号]_case_data.md` → 发布新版本 |
| 用户反馈问题 | GitHub Issue 跟踪 + 三平台描述更新 |
| 版本管理 | 破坏性变更 bump major（2.0.0），新功能 bump minor（1.1.0），修复 bump patch（1.0.1） |

---

## 八、快速操作速查卡

```bash
# SkillHub
skillhub login
skillhub init --name typhoon-tracker --category 天气气象
skillhub push
skillhub publish

# ClawHub
npm i -g clawhub
clawhub login
cd typhoon-tracker && clawhub skill publish . --slug typhoon-tracker

# GitHub
git init && git add . && git commit -m "v1.0.0"
git remote add origin <repo-url> && git push -u origin main
git tag v1.0.0 && git push --tags
```

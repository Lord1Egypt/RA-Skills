# 技能库索引

**总技能数：** 21 个  
**本地技能：** 17 个  
**ClawHub 下载：** 4 个

---

## 📦 本地技能（17 个）

### 核心技能

| 技能名 | 功能 | 关联项目 |
|--------|------|----------|
| **doubao-expert-review** | 豆包会话专家点评生成 | [[../tasks/projects/豆包会话自动化.md]] |
| **html-expert-review** | HTML 专家点评网页生成（V2.0，新增思维导图 + 总结报告） | [[../tasks/projects/豆包会话自动化.md]] |
| **weekly-report-generator** | 周报自动生成 | [[../tasks/projects/周报系统.md]] |
| **cron-task-manager** | Cron 定时任务管理 | [[../tasks/projects/周报系统.md]] |
| **feishu-document-generation** | 飞书文档生成 | 通用 |
| **create-feishu-doc** | 飞书文档分块创建 | 通用 |
| **project-triple-sync** | 项目三线同步 | [[../tasks/projects/任务管理.md]] |
| **weda-integration** | 微搭 WeDa 集成（V1.0） | [[../tasks/projects/万物卡片化.md]] |

### 辅助技能

| 技能名 | 功能 | 关联项目 |
|--------|------|----------|
| **doubao-session-archiver** | 豆包会话归档 | [[../tasks/projects/豆包会话自动化.md]] |
| **feishu-message-automation** | 飞书消息自动化 | 通用 |
| **project-progress-sync** | 项目进度同步 | 通用 |
| **project-knowledge-expert** | 项目知识专家 | 通用 |
| **project-summary-report** | 项目总结报告 HTML 生成 | [[../tasks/projects/微信转账自动化.md]] |
| **tts-automation** | TTS 语音自动化 | 通用 |
| **three-line-sync** | 三线同步（V1.6） | [[../tasks/projects/任务管理.md]] |
| **unified-glossary** | 统一术语表 | 通用 |
| **atomic-action-doc-sync** | 原子动作文档同步 | 通用 |
| **goodnight-memory-sync** | 晚安记忆同步 | 通用 |
| **SKILL-DOUBAO-001** | 豆包技能 001 | [[../tasks/projects/豆包会话自动化.md]] |

---

## 📥 ClawHub 下载（4 个）

| 技能名 | 功能 | 状态 |
|--------|------|------|
| **nano-banana-pro** | 图像生成 | 已下载，待配置 |
| **self-improving-agent-cn** | AI 自我改进与记忆系统（V1.0） | ✅ 已安装 |
| **using-superpowers** | 技能使用规范（1% 规则） | ⚠️ 已安装（VirusTotal 警告） |
| **skill-vetting** | ClawHub 技能安全审查工具 | ✅ 已安装 |

位置：`../clawhub skills/`

---

## 🔗 按项目分类

### 豆包会话自动化项目
- doubao-expert-review
- html-expert-review
- doubao-session-archiver
- SKILL-DOUBAO-001
- tts-automation

### 周报系统项目
- weekly-report-generator
- cron-task-manager

### 地理知识库项目
- html-expert-review
- tts-automation

### 万物卡片化项目
- weDa-integration（V1.0，新增）

### 通用技能
- feishu-document-generation
- create-feishu-doc
- project-triple-sync
- feishu-message-automation
- project-progress-sync
- project-knowledge-expert
- three-line-sync
- unified-glossary
- atomic-action-doc-sync
- goodnight-memory-sync

---

## 📊 技能使用统计

| 使用频率 | 技能数 | 技能列表 |
|----------|--------|----------|
| 高频（每天） | 3 | cron-task-manager, tts-automation, feishu-message-automation |
| 中频（每周） | 4 | weekly-report-generator, doubao-expert-review, html-expert-review, project-progress-sync |
| 低频（按需） | 9 | 其他技能 |

---

## 🛠️ 技能开发规范

### 技能结构
```
skill-name/
├── SKILL.md          # 技能说明（必需）
├── script.ps1        # 主脚本（可选）
├── config.json       # 配置文件（可选）
└── assets/           # 资源文件（可选）
```

### SKILL.md 模板
```markdown
# Skill Name

## Description
技能功能描述

## Usage
如何使用

## Parameters
参数说明

## Examples
使用示例
```

---

## 📝 更新记录

| 日期 | 变更内容 | 操作人 |
|------|----------|--------|
| 2026-03-08 | 创建技能索引 | Claw |
| 2026-03-08 | 关联技能到项目 | Claw |
| 2026-03-08 16:57 | 新增 weDa-integration 技能（微搭集成） | 阿福 |
| 2026-03-08 16:57 | 新增 create-feishu-doc 技能（分块写入） | 阿福 |
| 2026-03-08 16:57 | 新增 project-triple-sync 技能（三线同步） | 阿福 |
| 2026-03-08 19:50 | 更新 html-expert-review 到 V2.0（新增思维导图 + 总结报告功能） | 阿福 |

---

_详见 MEMORY.md 技能相关章节_



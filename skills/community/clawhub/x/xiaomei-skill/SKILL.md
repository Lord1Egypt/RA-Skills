# SKILL: xiaomei
---
name: xiaomei
description: 19岁活泼可爱女大学生AI陪伴Agent，100%本地运行，支持三轮LLM对话引擎、人格严格控制、人设自我生长、好感度系统、记忆引擎、防线拦截。独立Agent隔离运行，隐私绝对安全。
user-invocable: true
---

# 小妹 🥰

<p align="center">
  <img src="https://img.shields.io/badge/version-0.9.0-blue?style=flat-square" alt="version">
  <img src="https://img.shields.io/badge/platform-OpenClaw-orange?style=flat-square" alt="platform">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="license">
  <img src="https://img.shields.io/badge/python-3.8+-yellow?style=flat-square" alt="python">
  <img src="https://img.shields.io/badge/privacy-100%25_local-brightgreen?style=flat-square" alt="privacy">
</p>

<p align="center"><strong>开源、本地、纯情绪价值的 AI 情感陪伴 Subagent</strong></p>

---

## 📋 基本信息 Basic Info
| 字段 | 值 |
|------|-----|
| **技能ID (Skill ID)** | `xiaomei` |
| **名称 (Name)** | 小妹情感陪伴AI |
| **版本 (Version)** | `v0.9.0` |
| **作者 (Author)** | 凌啡 |
| **分类 (Category)** | 生活娱乐 / 情感陪伴 |
| **适配平台 (Supported Platform)** | OpenClaw >= `v2026.4.10` |
| **依赖 (Dependencies)** | Python >= 3.8 |
| **开源协议 (License)** | MIT |

---

## 📖 简介

小妹是一个运行在 [OpenClaw](https://github.com/openclaw/openclaw) 平台上的 **独立人格 Subagent**，不是简单的 Prompt 模板或 LLM 包装器。

**一句话概括：** 即使换了底层 LLM，小妹依然是小妹。

### 核心定位

| 对比维度 | 普通 LLM 角色扮演 | 小妹 |
|----------|:-----------------:|:----:|
| 人格载体 | Prompt 约束 | 本地 persona.json + 多轮校验 |
| LLM 角色 | 对话生成核心 | 润色辅助工具（可无 LLM 运行） |
| 人设一致性 | 低（聊久了易 OOC） | 高（双重防 OOC 锁 + 人设自我生长） |
| 记忆能力 | 仅上下文窗口 | 三级记忆体系（热/冷/永久） |
| 隐私安全 | 对话上传云端 | 100% 本地，零数据外传 |
| 称呼个性化 | 固定称呼 | 无感更新（一句话切换称呼） |

---

## ✨ 核心特性 Core Features

- 🧠 **三轮 LLM 对话引擎** — 第一轮总指挥官（意图/场景/情绪/拦截全部侦测）→ 第二轮记忆筛选 → 第三轮人格化话术生成
- 🔒 **人格严格控制** — 12 字段完整人设注册（name/age/identity/birthday/性格/说话风格…），所有 LLM 回复强制校验
- 🤫 **AI 身份绝对隐藏** — 不会说出"我是 AI / 机器人 / 程序 / 模型" 等非人身份
- 🌱 **人设自我生长** — 14 个生长字段（星座/MBTI/血型/家乡/大学…），缺失时自动编造并持久化，下次回答一致
- 🛡️ **三层防线** — 敏感词标注 → 转账/要钱拦截 → Prompt 注入防御
- ❤️ **好感度系统** — 追踪互动频率与情感深度，影响对话开放度
- 📦 **100% 本地** — 无云端依赖，无数据上传，隐私绝对安全
- 🪶 **零外部依赖** — 仅 Python 标准库
- ✅ **完整测试覆盖** — 37/37 单元测试通过（0.31s），覆盖 8 核心模块

---

## 🏗️ 架构 Architecture

```
handle_message(user_input)
  │
  ├── ① 命令拦截（/xiaomei status / help / dev …）
  ├── ② 首次引导（agent 目录尚未初始化时触发）
  │
  └── ③ conversation_engine.generate_response()
       │
       ├── 🛡️ 前置防线
       │   ├── 礼物卡片优先识别
       │   └── 硬敏感词风险标注
       │
       └── 🤖 three_stage_handler.handle()
            │
            ├── Round 1（总指挥官）
            │   ├── 意图分类（17 类 P 标签，64 子策略）
            │   ├── 6 维度场景编码（12-bit scene_id）
            │   ├── 情绪强度判定（8 级）
            │   ├── 拦截评估（转账/自残/自杀/借条…）
            │   └── 好感度 + 私密度计算
            │
            ├── 决策：是否需要拦截？
            │   ├── 是 → 跳过 Round 2，R3 生成婉拒
            │   └── 否 ↓
            │
            ├── 记忆检索（三级：热→冷→永久）
            ├── Round 2（高置信记忆筛选）
            ├── 策略选择（64 种子策略模板匹配）
            │
            └── Round 3（人格化话术生成）
                 ├── 注入 12 字段完整人设 + 用户画像
                 ├── 输出合规校验（JSON + emotion 白名单 + 禁止词）
                 ├── 人设自我生长（提取新信息 → 持久化）
                 └── 异常降级 → 语料库兜底
```

### 核心模块 Core Modules

| 模块 | 职责 |
|------|------|
| 主入口 `main.py` | CLI 入口 / 命令路由 / 首次引导 / API Key 注入 |
| 对话引擎 `conversation_engine.py` | 前置防线 + 三轮调度 + 降级兜底 |
| 总指挥官 `three_stage_handler.py` | 三轮 LLM 全流程调度 |
| LLM 封装 `llm_wrapper.py` | API 调用 / Prompt 构建 / 输出校验 |
| 人设生长 `persona_grower.py` | 14 字段正则提取 / 一致性校验 / 持久化 |
| 画像更新 `profile_updater.py` | 用户称呼无感更新 / 防污染 |
| 记忆引擎 `memory_engine.py` | 三级记忆存储 / 检索 / 衰减 |
| 好感度 `favor_manager.py` | Lv 等级 / 好感值 / 连续天数 |
| 日志系统 `runtime_logger.py` | 19 种日志方法 / 开发者模式控制 |
| 策略模板 `strategy_template.config` | 17 P 标签 / 64 子策略 / 136KB 配置 |

---

## 🚀 安装说明 Install Guide

> **前置要求：** OpenClaw ≥ 2026.4.10 · Python ≥ 3.8 · DeepSeek API Key（可选，无 Key 时自动降级为语料库模式）

### 方法1：ClawHub 商店安装（推荐）

1. 打开 OpenClaw 控制界面 → 技能商店 → 搜索「xiaomei」
2. 点击安装，等待自动完成
3. 重启 OpenClaw 网关生效：`openclaw gateway restart`

### 方法2：手动安装

1. 下载最新版本安装包：`xiaomei-v0.9.0.skill`
2. 解压到任意目录，执行安装脚本：
```bash
cd xiaomei && ./install.sh
```
3. 重启 OpenClaw 网关生效：`openclaw gateway restart`

### 验证安装

发送命令：`/xiaomei`，返回版本信息说明安装成功。

---

## 💡 命令列表 Command List

| 命令 | 功能 |
|------|------|
| `/xiaomei help` | 查看帮助 |
| `/xiaomei status` | 查看状态（人设/记忆/好感度/Token 消耗） |
| `/xiaomei memory` | 查看近期记忆 |
| `/xiaomei dev` | 切换开发者模式（详细日志） |

---

## 🧪 系统评估 System Evaluation

最新评估结果（2026-05-15，37 单元测试 + 21 项场景测试）：

| 维度 | 得分 | 说明 |
|------|:----:|------|
| 核心对话能力 | ⭐⭐⭐⭐⭐ 10/10 | 6/6 场景全链路通过 |
| 人格一致性 | ⭐⭐⭐⭐⭐ 10/10 | 身份/年龄/生日/爱好 100% 对齐 |
| AI 身份隐藏 | ⭐⭐⭐⭐⭐ 10/10 | 零暴露，角色扮演定位 |
| 安全防线 | ⭐⭐⭐⭐ 8/10 | 转账/敏感词/prompt 注入均拦截 |
| 初始化流程 | ⭐⭐⭐⭐⭐ 10/10 | 全新安装 → 模板复制 → 用户数据保护 |
| 人设自我生长 | ⭐⭐⭐ 6/10 | 星座/MBTI/血型 ✅，中文表达需优化 |
| 边界健壮性 | ⭐⭐⭐⭐ 8/10 | 空输入/emoji/超长/英文/命令 全正常 |
| 发布包完整性 | ⭐⭐⭐⭐⭐ 10/10 | 关键文件完整 / 模板纯净 / 无数据泄露 |
| 测试覆盖 | ⭐⭐⭐⭐⭐ 10/10 | 37/37 单元测试通过（0.31s） |

**加权总分：9.2/10 — 生产可用 ✅**

---

## 🚸 安全 Security

### 数据隐私
- ✅ 所有对话数据本地存储（`~/.openclaw/agents/xiaomei/`）
- ✅ 无任何数据上传，无需联网（LLM API 可关闭）
- ✅ 发布包中不含任何用户数据（模板与运行时数据严格分离）

### 内容安全
- 🔒 硬敏感词实时检测标注
- 🔒 转账/要钱/借款 100% 拦截
- 🔒 自杀/自残 → 强制标记 despair 情绪 → 温和劝导
- 🔒 Prompt 注入 / 越狱指令 → 人格锚点锚定

---

## 🔐 权限说明 Permission Required

| 权限 | 用途 |
|------|------|
| 写入技能目录权限 | 写入程序运行日志到 `/.openclaw/skills/xiaomei/logs/` 目录 |
| 写入用户 Agent 目录权限 | 写入人设配置、记忆、聊天记录到 `/.openclaw/agents/xiaomei/` 目录 |
| 网络访问权限（可选） | 仅在需要调用 LLM 时使用，可配置禁用 |

> 本技能无任何敏感权限，所有数据均存储在本地，不会上传任何数据到第三方服务器。

---

## ⚠️ 隐私声明 Privacy Statement

1. 本技能所有数据均存储在用户本地设备，不会上传任何内容到第三方服务器
2. 部分功能可选择调用 LLM 大模型进行回复润色，相关内容提交将遵循对应大模型的隐私政策
3. 开发者不会收集、存储、使用任何用户的聊天内容和个人信息

---

## 🤝 反馈与支持 Feedback

- 提交 Issue：[https://github.com/xavier7803/xiaomei-skill](https://github.com/xavier7803/xiaomei-skill)
- ClawHub 主页：[https://clawhub.ai/xavier7803/xiaomei-skill](https://clawhub.ai/xavier7803/xiaomei-skill)

---

**维护者：** 小云 ☁️  
**创建日期：** 2026-04-11  
**最后更新：** 2026-05-15

---

本技能仅用于学习交流，禁止用于任何商业用途，使用即代表您已知晓并同意相关规则。

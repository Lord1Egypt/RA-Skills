---
name: scheduled-voice-briefing
description: General-purpose skill for turning natural language requests into scheduled voice notifications and structured briefings. Use when the user wants to create, update, pause, resume, or remove recurring or one-time voice briefing tasks; configure timing, modules, language, voice, or tone in natural language; or manage scheduled spoken summaries such as reminders and daily briefings. This public package focuses on configuration, structure, runtime integration guidance, and production-like examples. It does not bundle provider-specific TTS implementations, does not include built-in API credentials, and does not access local files, system resources, or user data without explicit input. / 通用型 Skill，用于将自然语言请求转换为定时语音通知与结构化播报。适用于创建、修改、暂停、恢复或删除一次性或周期性语音播报任务，并支持通过自然语言配置时间、模块、语言、声音与语气。本公开包聚焦于配置结构、运行时集成说明和更接近真实使用场景的示例，不内置厂商特定的 TTS 实现，不包含内置 API 凭证，也不会在未明确输入的情况下访问本地文件、系统资源或用户数据。
---

# Scheduled Voice Briefing / 定时语音播报

Turn natural language requests into structured scheduled voice notifications and briefings.  
将自然语言请求转换为结构化的定时语音通知与播报内容。

## Overview / 概述

Scheduled Voice Briefing is a general-purpose Skill for scheduled spoken notifications and information briefings. Users can define when to run, what content to include, and how it should sound through natural language instructions.  
Scheduled Voice Briefing 是一个通用 Skill，用于定时语音通知与信息播报。用户可以通过自然语言设置执行时间、播报内容，以及语言、声音与语气。

Morning briefings are one example use case. This skill can also be used for scheduled reminders, status summaries, and other spoken notifications.  
晨间播报只是示例场景之一，本 Skill 同样可用于定时提醒、状态摘要和其他语音通知场景。

## Core capabilities / 核心能力

This skill supports:
- natural language configuration of scheduled tasks
- creation and management of recurring and one-time tasks
- modular content generation such as environment or schedule summaries
- language, voice, and tone customization
- clear and explainable configuration updates
- optional staged reminder or notification sequences

本 Skill 支持：
- 自然语言配置定时任务
- 创建与管理周期性或一次性任务
- 模块化内容生成，例如环境摘要或日程摘要
- 语言、声音与语气控制
- 对配置变更给出清晰且可解释的说明
- 可选的分阶段提醒 / 通知序列设计

## Runtime integration / 运行时集成

This skill is environment-agnostic and does not depend on a specific operating system.  
本 Skill 不依赖特定操作系统，对运行环境保持兼容。

Recommended runtime fields:
- `provider`
- `voice`
- `rate`
- `volume`
- `tone`
- `contextText`
- `fallback`
- `playbackMode`

建议的运行时字段：
- `provider`
- `voice`
- `rate`
- `volume`
- `tone`
- `contextText`
- `fallback`
- `playbackMode`

The public package does not bundle provider-specific credential handling or vendor-specific playback logic. Any local voice engine, external TTS, or playback runtime must be provided by the runtime environment.  
本公开包不内置厂商特定的凭证处理或播放逻辑。任何本地语音引擎、外接 TTS 或播放运行时都应由运行环境自行提供。

## Safety and execution boundaries / 安全与执行边界

- This skill does not execute arbitrary system commands.
- This skill does not include or require built-in API credentials.
- Any external services, such as text-to-speech, must be provided and configured by the runtime environment.
- This skill does not access local files, system resources, or user data without explicit input.
- Any external data, such as calendar or weather information, must be explicitly provided by the user or the runtime environment.

- 本 Skill 不执行任意系统命令。
- 本 Skill 不内置或要求提供任何 API 凭证。
- 外部服务（如语音合成）必须由运行环境显式提供和配置。
- 本 Skill 不会在未明确输入的情况下访问本地文件、系统资源或用户数据。
- 所有外部数据（如日历、天气）必须由用户或运行环境显式提供。

## Emotional style truth / 情绪表达说明

This skill can describe tone, pacing, and emotional intent at the configuration level. However, actual expressive quality depends on the runtime voice engine. Rich emotional playback is best achieved with stronger TTS providers.  
本 Skill 可以在配置层描述语气、节奏与情绪意图，但实际表达效果取决于运行环境中的语音引擎。更丰富的情绪表现通常需要更强的 TTS 提供方支持。

## Content model / 内容模型

Suggested module types:
- `opening`
- `transition`
- `environment_brief`
- `schedule_brief`
- `closing`

建议模块类型：
- `opening`（开场）
- `transition`（过渡）
- `environment_brief`（环境摘要）
- `schedule_brief`（日程摘要）
- `closing`（收尾）

Rules:
- Keep output bounded and relevant to enabled modules.
- Prefer short, structured summaries.
- Degrade gracefully if optional data sources are unavailable.
- Ask for clarification when timing or scope is ambiguous.

规则：
- 输出应受约束，并与启用模块强相关。
- 优先使用简短、结构化摘要。
- 当可选数据源不可用时应平稳降级。
- 当时间或作用范围存在歧义时，应请求澄清。

## Production-like examples / 更接近真实使用的示例

Examples of supported use cases:
- weekday morning voice briefing
- one-time reminder for tomorrow
- evening wrap-up reminder
- staged reminder flow before a daily briefing

支持的使用场景示例：
- 工作日晨间语音播报
- 明天的一次性提醒
- 晚间收尾提醒
- 在正式播报前增加分阶段提醒序列

## Explainability requirement / 可解释性要求

Whenever configuration changes, return a short explanation such as:

```text
Updated configuration:
- Time: weekdays 07:30
- Modules: environment_brief, schedule_brief
- Tone: calm
- Override: none
```

每当配置发生变化时，应返回简短且可解释的说明，例如：

```text
已更新配置：
- 时间：工作日 07:30
- 模块：environment_brief, schedule_brief
- 语气：平静
- 覆盖：无
```

## Design boundaries / 设计边界

This skill should not:
- hard-code a fixed persona
- bundle third-party music or audio assets
- assume a specific operating system
- rely on undeclared secrets or hidden runtime requirements
- generate long unbounded content unrelated to configured modules
- ship private wake lines or user-specific language in the public package

本 Skill 不应：
- 写死固定人格设定
- 打包第三方音乐或音频资源
- 假定特定操作系统
- 依赖未声明的密钥或隐藏的运行条件
- 生成与模块无关的长篇无限制文本
- 在公共包中携带用户私有台词或个性化表达

## Resources / 资源说明

- `references/config-schema.md` describes the suggested config structure and runtime contract.
- `references/briefing-templates.md` provides higher-quality wording and pacing guidance.
- `scripts/update_schedule.py` shows one way to convert natural language updates into config changes.
- `scripts/build_briefing.py` shows one way to assemble bounded briefing text from configured modules.

- `references/config-schema.md`：建议配置结构与运行时集成说明。
- `references/briefing-templates.md`：更接近真实使用的文案与节奏建议。
- `scripts/update_schedule.py`：展示一种将自然语言更新转换为配置修改的方法。
- `scripts/build_briefing.py`：展示一种基于模块配置生成受约束播报文本的方法。

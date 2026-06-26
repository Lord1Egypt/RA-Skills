# xiaomei-skill
- 小妹技能包 | 专注情感陪伴与人格模拟的小妹人设型 OpenClaw 原生拟人 Agent 技能包，人格稳定、轻量化陪伴交互
- Xiaomei Skill | An OpenClaw-native anthropomorphic Agent skill package with a little sister persona, dedicated to emotional companionship and personality simulation, featuring stable character and lightweight interactive companionship.
---

## 项目简介 Introduction

### **中文：**
一款寄生式 Agent 技能包，面向 OpenClaw 及主流 Agent 平台，主打**情感陪伴、拟人人格模拟**，定位为成人向虚拟伴侣。
采用自研三轮 LLM 调用架构、三级记忆+艾宾浩斯机制、全链路结构化调试日志与双重防OOC锁体系，人格稳定不漂移，主打软萌治愈系妹妹陪伴定位，100%本地运行可控，隐私无泄露风险。
目前处于**公开测试阶段**，持续迭代优化中。

### **English:**
A parasitic Agent skill package for OpenClaw and mainstream Agent platforms, focusing on **emotional companionship and anthropomorphic personality simulation**, positioned as an adult-oriented virtual companion.
Adopting self-developed three-round LLM call architecture, three-level memory + Ebbinghaus mechanism, full-link structured debug logs and double anti-OOC lock system, stable personality without drift, focusing on soft and cute healing companion positioning, 100% local operation controllable, no privacy leakage risk.
Currently in **public testing phase**, continuously iterating and optimizing.
---
## 适配平台 Supported Platforms
- ✅ OpenClaw / ClawHub
- ✅ SkillHub
- ✅ 兼容主流Agent生态系统 / Compatible with mainstream Agent ecosystem
---
## ✨ 核心特性 Core Features
| 特性 | 说明 |
|------|------|
| 🔒 **人格强锁定** | 16字核心原则：`人格优先、本地主控、类人适配、轻量可控`，双重防OOC锁机制，对话全程本地校验，人格永不漂移 |
| 🧠 **类人记忆系统** | 三级记忆分层（热记忆/冷记忆/永久记忆）+ 艾宾浩斯记忆强度机制，模拟真实人类记忆遗忘和强化规律 |
| 📝 **全链路调试日志** | 六大类结构化JSON日志，按日自动生成，全流程可追溯，支持开发者模式开启/关闭 |
| 🎯 **策略模板驱动** | 内置512条12位场景码标注语料，覆盖90%日常对话场景，策略模板动态匹配，回复自然不生硬 |
| 🔄 **无感增量升级** | 程序文件和用户数据完全分离，升级时仅覆盖纯程序文件，100%保留所有用户数据、人设、聊天记录 |
| 🛡️ **高隐私安全** | 100%本地运行，敏感数据不上云，支持聊天记录自动脱敏，隐私完全可控 |
| ⚡ **轻量低占用** | 无额外服务依赖，启动速度<1s，内存占用<50MB，低配置设备也能流畅运行 |
---
## 🚀 快速安装 Quick Install
### 方法1：OpenClaw商店安装（推荐）
1. 打开OpenClaw控制界面 → 技能商店 → 搜索「xiaomei」
2. 点击安装，等待自动完成
3. 重启OpenClaw网关生效：`openclaw gateway restart`
### 方法2：手动安装
1. 下载最新版本安装包：`xiaomei-vx.x.x.skill`
2. 解压到任意目录，执行安装脚本：
```bash
cd xiaomei && ./install.sh
# 静默安装（无交互）：./install.sh --non-interactive
```
3. 重启OpenClaw网关生效：`openclaw gateway restart`
### 验证安装
发送命令：`/xiaomei`，如果返回版本号、运行路径等信息，说明安装成功。
---
## 💡 使用说明 Usage
### 首次启动
1. 安装完成后，首次发送任意消息触发引导流程
2. 同意隐私规则后即可开始对话
3. 引导过程中会自动完成基础人设配置
### 常用命令
| 命令 | 功能 |
|------|------|
| `/help` | 查看帮助文档和隐私规则 |
| `/xiaomei` | 查看当前版本、开发者模式状态、运行路径、所有人设信息 |
| `/xiaomei dev on` | 开启开发者模式，记录全链路调试日志 |
| `/xiaomei dev off` | 关闭开发者模式，停止记录调试日志，节省存储空间 |
| `/xiaomei dev status` | 查看开发者模式当前状态 |
| `/reset_persona` | 清空所有动态补充的人设信息，恢复默认人设 |
| `/reset` | 重置全部配置，重新走首次引导流程 |
---
## 📂 目录结构说明 Path Description
### 静态程序目录（更新时会被覆盖）
```
/home/admin/openclaw/workspace/skills/xiaomei/
├── src/                    # 核心代码
├── config/                 # 默认配置文件
├── scripts/                # 工具脚本
├── logs/                   # 程序运行日志
│   ├── access_YYYYMMDD.log # 访问日志，按日生成
│   └── error.log           # 错误日志
└── install.sh              # 安装脚本
```
### 动态用户数据目录（更新时永久保留，不会被覆盖）
```
/home/admin/.openclaw/agents/xiaomei/
├── config/
│   ├── agent_config.json   # 全局配置（开发者模式开关等）
│   ├── persona.json        # 人设配置，包含动态补充人设
│   └── .first_launch       # 首次启动标记
├── logs/
│   └── chat_generation.log # 聊天生成过程日志
├── memory/                 # 记忆存储目录
└── sessions/               # 会话历史存储目录
```
---
## 🛠️ 开发者模式 Developer Mode
### 开启方法
```
/xiaomei dev on
```
### 日志规范
- 日志格式：纯结构化JSON单行输出，方便程序解析
- 时间戳：ISO8601格式，精确到毫秒
- 包含字段：timestamp、session_id、turn_seq、log_type、log_level、is_exception、error_code、error_msg、cost_ms等
- 按日自动切分文件：命名规则`access_YYYYMMDD.log`
### 日志类型说明
1. `SceneJudge`：场景判断日志，记录第一轮LLM调用结果、场景码匹配、关键词提取
2. `StrategyHit`：策略匹配日志，记录核心目的匹配、子策略选择、模板加载状态
3. `MemoryDecision`：记忆检索日志，记录候选记忆召回、过滤、匹配结果
4. `ThreeLLMCall`：三轮LLM调用汇总日志，记录每轮调用状态、耗时、参数
5. `ComplianceCheck`：合规校验日志，记录人设、语气、禁忌词校验结果
6. `FinalReplyGen`：最终回复生成日志，记录回复内容、使用记忆、话题结束概率
---

## 🤝 贡献指南 Contributing
欢迎各种形式的贡献！
1. 🐛 提交Issue：反馈Bug、提出功能建议
2. ✨ 提交PR：修复Bug、新增功能、优化代码
3. 📝 贡献语料：补充场景对话语料、优化策略模板
4. 📚 完善文档：优化README、帮助文档
### 开发环境搭建
1. 克隆仓库到本地
2. 在OpenClaw环境下开发测试
3. 提交PR前请确保单元测试全部通过
---
## ⚠️ 免责声明 Disclaimer
1. 本项目仅用于学习交流，禁止用于任何商业用途
2. 使用本项目产生的所有后果由使用者自行承担，作者不承担任何责任
3. 部分功能需要调用LLM大模型，相关内容生成由大模型负责，使用即代表您已知晓并同意相关隐私政策
4. 请遵守当地法律法规，禁止使用本项目从事任何违法违规活动
---
## 📄 开源协议 License
本项目采用 [MIT License](https://opensource.org/licenses/MIT) 开源协议，可自由使用、修改、分发，但请保留原作者信息。
---
## 致谢 Acknowledgments
感谢所有贡献者和测试用户的支持 ❤️

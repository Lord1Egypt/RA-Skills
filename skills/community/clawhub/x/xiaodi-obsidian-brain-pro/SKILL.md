---
name: xiaodi-obsidian-brain-pro
description: WhatsApp/Telegram → Obsidian 智能记忆增强，防幻觉纠偏，隐私脱敏，让碎碎念自动变成结构化知识（开车/工地语音输入友好）
version: "1.1.3"
author: xiaodi
homepage: https://github.com/mx6315909/xiaodi-obsidian-brain-pro
metadata:
  openclaw:
    emoji: 🧠
    requires:
      tools: ["memory_search", "exec", "write"]
      providers: ["ollama"]
---

# 🧠 xiaodi-Obsidian-Brain-Pro（内测版）

> **一句话简介**：将你的 WhatsApp/Telegram 变成 Obsidian 的"前置大脑"，支持本地 Ollama 语义检索，让碎碎念自动变成结构化知识。

---

## 🌟 为什么你需要这个？

### 痛点

- ❌ 记了 1000 篇笔记，想找的时候找不到
- ❌ 想记的时候嫌打开电脑麻烦
- ❌ 碎片化想法散落在聊天记录里，永远丢失
- ❌ 第三方云端笔记隐私堪忧

### 解决方案

**xiaodi-Obsidian-Brain-Pro = WhatsApp盲发 + Ollama语义索引 + 自动标签归类 + GitHub自动备份**

---

## 🚀 核心功能

### 1. 【闪电入库】

在开车、走路时发一句语音或文字给小弟，自动同步到 Daily Notes。

**核心原则**：
- ✅ **保持原汁原味**：不精简、不提炼、不改语气
- ✅ **只修格式**：调整段落、修正语病
- ✅ **带感情命名**：`2026-03-27 随想与感悟.md`（不是干巴巴的日期）
- ✅ **多语言纠偏**：自动修正语音识别错误（Open Crow → OpenClaw）
- ✅ **隐私脱敏**：API Key/密码自动替换为 `[PROTECTED]`

**示例**：

```
用户发送（开车路上语音转文字）：
"现在颈椎有点痛，我在开车路上，今天想写点东西，突然发现思绪有点混乱..."

自动生成：
文件：2026-03-27 随想与感悟.md
内容：保持原话，只修格式和语病
```

---

### 1.1 【多语言纠偏白名单】⭐ NEW

**场景**：开车/工地语音输入，常见识别错误：

| 语音识别错误 | 自动修正 |
|--------------|----------|
| Open Crow | OpenClaw |
| 导课 | Docker |
| 码云 | Git |
| 病毒 | Docker（容器） |
| 阿里云百炼 | Bailian |

**规则**：只修正白名单术语，防止篡改其他内容。

---

### 1.2 【隐私脱敏红线】⭐ NEW

**自动脱敏内容类型**：

| 类型 | 脱敏标记 |
|------|----------|
| API Key | `[API_KEY_PROTECTED]` |
| 密码 | `[PASSWORD_PROTECTED]` |
| Token | `[TOKEN_PROTECTED]` |
| 手机号 | `[PHONE_PROTECTED]` |

**防止泄露路径**：
```
语音说 API Key → 自动脱敏 → 推送 GitHub → 安全 ✅
```

---

### 2. 【语义搜索】

整合 Ollama (nomic-embed-text)，支持"模糊提问"。

**示例**：

| 你的提问 | 自动关联 |
|----------|----------|
| "我最近身体咋样？" | → 3天前抱怨颈椎痛的笔记 |
| "上周末干了啥？" | → 台球桌试验记录 |
| "大姐出院了吗？" | → 戊肝治愈出院的记录 |

**技术实现**：
```json
{
  "provider": "ollama",
  "model": "nomic-embed-text",
  "extraPaths": [
    "~/Obsidian/Daily Notes",
    "~/Obsidian/每日笔记"
  ]
}
```

---

### 3. 【安全第一】

**全本地运行**：
- ✅ Ollama 本地 embedding（不上传云端）
- ✅ Obsidian 本地存储（你的考研计划、股票持仓、工作教训）
- ✅ GitHub 私有仓库备份（可选）

**隐私保证**：
> 考研计划、股票持仓、工作教训，绝不上传第三方云端。

---

### 4. 【多 Agent 协作】

内置"整理专家"和"复盘专家"：

| Agent | 功能 | 执行时间 |
|-------|------|----------|
| 整理专家 | 每日笔记自动标签归类 | 每晚 23:00 |
| 复盘专家 | 生成一周摘要 | 每周日 20:00 |

---

## 📦 安装命令

```bash
# ClawHub 一键安装
npx clawhub@latest install xiaodi-obsidian-brain-pro

# 手动安装
git clone https://github.com/mx6315909/xiaodi-obsidian-brain-pro.git
cd xiaodi-obsidian-brain-pro
openclaw skill link .
```

---

## 🔧 配置要求

| 项目 | 要求 |
|------|------|
| OpenClaw | 2026.3.8+ |
| Ollama | nomic-embed-text 模型 |
| Obsidian | Daily Notes 文件夹 |
| Git | 私有仓库备份（可选） |

---

## 💰 商业化

### 基础版（免费）

在 ClawHub 免费发布，攒口碑和 Star。

### 专业版（付费咨询）

**服务内容**：
- 群晖 NAS 一键部署环境包
- 1对1 调教服务（定制你的记忆流程）
- WhatsApp/Telegram 双渠道配置

**联系方式**：
- GitHub: https://github.com/mx6315909/xiaodi-obsidian-brain-pro
- ClawHub: https://clawhub.ai/skills/xiaodi-obsidian-brain-pro

**定价**：
- 基础部署：199 元
- 高级定制：499 元

---

## 📊 对比图

| 功能 | 普通笔记 | xiaodi-Obsidian-Brain-Pro |
|------|----------|---------------------|
| 入库方式 | 打开电脑手写 | WhatsApp盲发 |
| 搜索方式 | 关键词匹配（找不到） | Ollama语义检索（模糊问也能找到） |
| 隐私安全 | 云端存储 | 全本地运行 |
| 自动备份 | 手动操作 | Git自动同步 |
| 情感保留 | 被AI精简 | 保持原汁原味 |
| 语音纠偏 | 无 | ⭐ 自动修正 Open Crow → OpenClaw |
| 隐私脱敏 | 无 | ⭐ API Key 自动替换 `[PROTECTED]` |

---

## 🎯 正确 vs 错误对照（海报素材）

### ❌ 传统 AI 笔记（爹味严重）

```markdown
# 2026-03-27 工作总结与思考

## 身体状况
颈椎疼痛，背部不适，影响工作效率。

## 解决方案
计划购置床头书桌，改善工作姿势。

## 项目反思
OpenClaw 项目方向需要重新审视...

*整理时间：2026-03-27*
```

**问题**：
- ❌ 把"有点烦"改成"情绪需要调整"
- ❌ 把"胡乱写点东西"改成"整理思绪"
- ❌ 把碎片化思绪整理成"逻辑清晰的结构"
- ❌ **用户原话被篡改**

---

### ✅ xiaodi-Obsidian-Brain-Pro（拒绝爹味）

```markdown
# 2026-03-27 随想与感悟

现在颈椎有点痛，我在开车路上。

思绪有点混乱，碎片化，前后不连贯。

因为颈椎疼背疼，想买书桌躺着看电脑。

转而又一想，搞 OpenClaw 到底为什么？

---

*写于开车路上，思绪有点混乱碎片化*
```

**核心一句话**：
> **用户说的每一句话都是证据，你只能整理格式，不能篡改证据。**

---

## 🎯 适用人群

- ✅ 碎片化记录爱好者（开车、走路时想法多）
- ✅ Obsidian 重度用户（1000+笔记找不到）
- ✅ 隐私敏感人群（考研计划、股票持仓不想泄露）
- ✅ OpenClaw 早期体验者（想尝试 Agent 技能）

---

## 📝 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.1.3 | 2026-03-28 | ⭐ 添加 tags 关键词标签，提升搜索可见度 |
| v1.1.2 | 2026-03-28 | ⭐ SKILL.md修复 - homepage URL/安装命令/版本一致性 |
| v1.1.1 | 2026-03-28 | ⭐ 添加路径配置警告 + 修复 homepage URL |
| v1.1.0 | 2026-03-28 | ⭐ 新增多语言纠偏白名单 + 隐私脱敏红线 |
| v1.0.0 | 2026-03-28 | 初始发布：闪电入库 + 语义搜索 + 安全第一 |

---

## 🤝 贡献

欢迎提交 Issue 和 PR：
- GitHub: https://github.com/mx6315909/xiaodi-obsidian-brain-pro
- ClawHub: https://clawhub.ai

---

## 📄 License

MIT License

---

*"让你的 Obsidian 真正长出大脑"* 🧠
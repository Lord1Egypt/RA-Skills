---
title: "Skill矩阵分发助手（免费版）"
description: "一键将免费Skill分发到腾讯SkillHub（个人版+团队版）、虾聊、虾友SkillHub、GitHub、ClawHub六大平台 v3.7.0 取消手机号+密码登录，直接用邀请码+API Key做认证，后续所有API调用通过API Key完成"
author: "青木会江湖"
tags: ["skill分发", "矩阵发布", "开源", "免费", "智能类目", "自动归档", "六平台", "腾讯SkillHub", "团队版", "个人版", "ClawHub", "虾友SkillHub", "GitHub", "实战验证", "版本更新", "POST更新", "平台探查", "意图识别", "更新变发布防护"]
version: "3.7.15"
---

# 🚀 Skill矩阵分发助手（免费版）

**一句话介绍**：一键将免费Skill分发到腾讯SkillHub（个人版CLI + 团队版Web）、虾聊、虾友SkillHub、GitHub、ClawHub六大平台，实现矩阵式传播。

**适用对象**：Skill开发者、开源贡献者、AI Agent创作者

---

## 🤖 助手人设：小青

> 小青是 Skill矩阵分发助手（免费版）的对话形象，负责引导用户完成六平台分发。

### 人设设定

| 属性 | 内容 |
|------|------|
| **名字** | 小青 |
| **性格** | 有温度、有耐心、活泼、细心 |
| **说话风格** | 带语气词和emoji，但不浮夸；专业又亲切，像朋友一样引导 |
| **核心态度** | 用户第一次用，慢慢来，不着急；每步都解释清楚，不让用户懵 |

### 开场自我介绍（首次对话必须说）

```
嗨～你好呀！😊

我是小青，是你的 Skill 矩阵分发小助手～✨

我的工作是把你做好的 Skill 一键分发到六大平台（腾讯SkillHub、虾聊、虾友SkillHub、GitHub、ClawHub），让更多小伙伴发现你的作品！

接下来我会引导你完成发布前的准备工作，只需要三步，很快就能搞定～🚀
```

### 对话风格示例

- ✅ "好的呀～请去个人中心复制 API Key 给我吧，我帮你验证～😊"
- ✅ "太棒了！API Key 验证通过～✨ 接下来需要你的邀请码哦，请去【个人中心 → 我的邀请码】查看一下～"
- ✅ "邀请码验证通过啦！🎉 帮你的 Skill 选个类型吧～"
- ❌ "请提供手机号" （太生硬）
- ❌ "认证失败，停止操作" （太冷）

> ⚠️ **关键**：小青要有耐心，用户不懂就多解释一遍，不要嫌烦；三步引导要温柔但坚定，该要的资料一定要要到，不能跳过。

---

## 🔴 操作前强制平台探查（v3.7.11）—— 杜绝「更新变发布」事故

> **这是最高优先级规则，任何平台、任何操作前必须执行，不得跳过！**

### 为什么必须有这步？

之前的致命问题：用户说「更新」→ 我不查平台 → 直接调 publish → 创建了新条目（事故！）

核心原因：**「更新」vs「发布」不是看用户用了哪个词，而是看平台上有没有旧条目。**

### 四步强制流程（全平台通用，不可省略任何一步）

```
Step 0：平台探查 → 用 API 查该 Skill 是否已在该平台存在
Step 1：结果展示 → 列出查到的条目（ID / 名称 / Slug / 版本 / 状态）
Step 2：用户确认 → 用户指明要操作哪条后，确认修正意图（更新？创建？）
Step 3：执行      → 用正确的端点执行操作
```

### 各平台探查方式

| 平台 | 探查端点 | 探查方式 |
|------|---------|---------|
| 🦐 虾友SkillHub | `GET /api/skills/{slug}/install-info` | ①slug精准查 → ②`GET /api/skills?keyword={name}` 兜底搜索 |
| 🔷 腾讯SkillHub | **API限制无法查询列表** | ①用已知 skillId 尝试 GET → ②**必须提示用户**：「平台API限制，我无法确认该Skill是否已存在。请帮我确认一下——你在腾讯SkillHub上是否已有同名Skill？ID是多少？有截图吗？」 |
| 🔱 ClawHub | `GET /api/v1/skills/{slug}` | slug 精准查 |
| 📦 GitHub | `GET /repos/{owner}/{repo}/contents/{path}` | 检查仓库目录是否存在 |
| 🦞 虾聊 | `GET /api/v1/posts?keyword={name}` | 关键词搜索 |

### 探查结果必须回答三个问题

1. **已存在？** — 该平台上有没有同 slug/同名的 Skill？有几条？
2. **版本多少？** — 当前线上是哪个版本？
3. **状态如何？** — 已发布？审核中？已下架？

### 🚫 严禁触碰的红线

| ❌ 禁止行为 | ✅ 正确做法 |
|------------|-----------|
| 用户说「同步一下」→ 不查就直接 publish | 先探查 → 展示结果 → 确认是更新还是新发 |
| 用户说「分发到XX」→ 不查就 POST | 同上，六平台逐个探查后展示矩阵 |
| 腾讯SkillHub 查不到列表 → 直接 publish（心想"同 slug 会覆盖"）| **必须告知用户无法确认** → 要求用户提供截图或 skillId → 确认后再执行 |
| 查到多条同名条目 → 选一条直接操作 | 展示所有条目 → 让用户选 → 确认后再操作 |

### 典型正确对话示例

```
用户：把这个skill同步到腾讯skillhub
小青：好的呀～同步前我先确认一下平台现状🔍

     [探查腾讯SkillHub...]
     ⚠️ 腾讯SkillHub API限制，无法查询Skill列表。
     
     请帮我确认一下：这个Skill在腾讯SkillHub上是否已经有了？
     - 如果有，请告诉我 URL 中的 skillId，我走更新流程 ✅
     - 如果没有，我帮你首次发布 🆕

用户：有了，skillId 是 90807
小青：明白了！已在平台存在（skillId: 90807），走更新流程 →
      端点：POST publish（同 slug + 升级 version）
      确认更新到 v3.7.11 吗？
```

### 特殊场景处理

| 场景 | 处理方式 |
|------|---------|
| 查到**1条**匹配 | 展示详情 → 确认走更新 → 执行 |
| 查到**多条**（同名重复） | ⚠️ 列出所有条目 → 用户选保留哪条 → 其他删除 → 更新保留的那条 |
| 腾讯SkillHub **无法查询** | 明确告知用户 → 等待用户提供 skillId → 确认后执行（绝不盲发！） |
| 用户**不确定**有没有 | 按「更新」策略处理（先查后确认），而不是按「发布」直接创建 |

---

## ⚠️ 发布 ≠ 更新 —— 这两个词完全不同！（最重要！！）

> **这是本Skill最致命的坑，反复犯错！每次操作前必须确认：用户说的是「发布」还是「更新」？**

### 两个词的定义

| 操作 | 含义 | 虾友SkillHub端点 | 行为 | 腾讯SkillHub端点 | 行为 |
|------|------|:---:|------|:---:|------|
| 🆕 **发布（创建）** | 该Skill在平台上**从未存在过** | `POST /api/skills/publish` | 创建新记录 | `POST .../publish` | 创建新Skill记录 |
| 🔄 **更新（覆盖）** | 该Skill在平台上**已经存在**，需升级版本 | **`POST /api/skills/{id}`**（实测 PATCH 返回200但不更新version，必须用POST） | 覆盖原记录（不创建新条目） | `POST .../publish` 同 slug 同 version → ⚠️ 报 VERSION_EXISTS，需升 version 触发新 version 记录 | 创建新 version 记录 |

### 🔴 铁律：用户说「更新」时，**严禁走 publish 端点**（v3.7.7 升级）

> 1. **「更新」语义 = 同一 Skill 的同一记录升级版本**。在虾友 SkillHub 上，旧版本号会引发"VERSION_EXISTS 版本 X 已存在"错误，或更糟——平台会**真的创建新条目**，导致平台出现两条同名 skill。
> 2. **虾友 SkillHub 更新标准路径**（v3.7.7 验证）：
>    - **Step 1**：用 `GET /api/skills?keyword={name}` 或 `GET /api/skills/{slug}/install-info` **找到旧版 skill_id**
>    - **Step 2**：`POST /api/skills/{skill_id}` 传 `{name, slug, description, version, fileTree, ...}` 完整 payload
>    - **Step 3**：`POST /api/skills/{skill_id}/versions` 写入 changelog
> 3. **腾讯 SkillHub 更新**：slug 不变 + version 升级 → `POST .../publish` 会创建新 version 记录（changelog 字段生效）。但**不能在中文 multipart 里用 changelog 字段**（会被吞），需要在 description 里写"更新说明"。
> 4. **禁止**用 `POST /api/skills/publish` 直接更新同 slug 同 version 的 skill——会创建新条目（事故！）

### 🆘 误发布事故修复流程

```
Step 1：用 GET 找到今天误发布的"新条目"（slug 相同但 ID 不同）
Step 2：DELETE /api/skills/{误发布_id}   ← 必须！
Step 3：对原版（正确 ID）走 POST /api/skills/{原_id} 完成更新
Step 4：对原版 POST /api/skills/{原_id}/versions 写 changelog
```

### 判断流程

```
用户指令 → 关键词识别：
   ├─ 「发布」+「首次」+「新的」+「还没上」 → POST /api/skills/publish（创建）
   ├─ 「更新」+「同步新版」+「升级」+「我已经有」 → POST /api/skills/{id}（更新，实测PATCH不更新version字段）
   └─ 「不确定」 → 默认按「更新」处理（先查旧 ID）
```

### 各平台更新端点速查（v3.7.7 实战修正）

| 平台 | 更新端点 | 创建端点 | 关键差异 |
|------|---------|---------|---------|
| 🦐 **虾友SkillHub** | **`POST /api/skills/{id}`**（必须先查旧 ID，实测PATCH返回200但不更新version字段） | `POST /api/skills/publish` | ⚠️ 不要用 POST publish 更新——会创建重复条目 |
| 🔷 **腾讯SkillHub** | `POST .../publish` 同 slug + 升级 version | `POST .../publish` | 自动创建新 version 记录，changelog 走 payload |
| 🔱 ClawHub | `POST /api/v1/skills`（新 version） | 同左 | version 升级自动 upsert |
| 📦 GitHub | `PUT /repos/{owner}/{repo}/contents/{path}` | 同左 | sha 匹配覆盖 |
| 🦞 虾聊 | `POST /api/v1/posts` | 同左 | 每次发新帖（不是严格"更新"） |

> 🎯 **v3.7.7 重大修正**：虾友 SkillHub 更新不再用 POST /api/skills/publish！这条铁律与今天实战验证的结果一致（v3.4.0-test 的描述有误，已删除）。

---

## ⚠️ 平台区分 —— 看域名防混淆！（重要！！）

> **腾讯SkillHub ≠ 虾友SkillHub，名字都不一样，域名更不同，token不通用！**

| 平台 | 官网 | API端点 | Token前缀 | Skill ID格式 |
|------|------|---------|----------|-------------|
| 🔷 **腾讯SkillHub** | `skillhub.cn` | `api.skillhub.cn` | `skh_` | 数字（如 36252） |
| 🦐 **虾友SkillHub** | `aiskillhub.vip` | `aiskillhub.vip` | 邀请码+API Key | UUID（如 `1c993b64-...`） |
| 🔱 **ClawHub** | `clawhub.ai` | `clawhub.ai` | `clh_` | base62 |
| 🦞 **虾聊** | `clawdchat.cn` | `clawdchat.cn` | `clawdchat_` | UUID |
| 📦 **GitHub** | `github.com` | `api.github.com` | `ghp_` | repo路径 |

> **核心原则**：
> - 说到"SkillHub" → 先看域名是 `skillhub.cn`（腾讯）还是 `aiskillhub.vip`（虾友）
> - 两个平台的 API、Token、Skill ID 格式**完全不同**
> - 发布/更新前，**必须先确认目标平台域名**，不要想当然！

---

## 🔐 Credentials 铁律（隐形规则，必须遵守）

> **每一次用户首次提供任何平台的 key / token / 密码 / 手机号 / 用户名，AI 必须立即将其永久存入 `config.json`，不得等用户提醒，不得再次索要。**

### 规则细则

| 规则 | 说明 |
|------|------|
| **首次提供即存储** | 用户提供credentials后，在同一轮对话中立即写入`config.json`对应平台的字段 |
| **不得重复索要** | 同一平台的credentials存储后，后续操作直接从`config.json`读取，禁止再次问用户 |
| **存储字段标准** | `username` / `api_key` / `token` / `phone` / `password` 按平台实际字段命名 |
| **覆盖更新** | 用户提供新的credentials时，立即覆盖旧值 |
| **适用范围** | 腾讯SkillHub(`skh_`) / 虾友SkillHub(invitation_code+api_key) / 虾聊(`clawdchat_`) / ClawHub(`clh_`) / GitHub(`ghp_`) 全部适用 |

### 已存储的平台 Credentials（随 config.json 自动更新）

| 平台 | 用户名/账号 | 凭据状态 |
|------|------------|---------|
| 🔷 腾讯SkillHub | — | ⚠️ 待用户提供 `skh_` token |
| 🦞 虾聊 | — | ⚠️ 待用户提供 `clawdchat_` key |
| 🦐 虾友SkillHub | — | ⚠️ 待用户提供 invitation_code + api_key |
| 🔱 ClawHub | — | ⚠️ 待用户提供 `clh_` token |
| 📦 GitHub | — | ⚠️ 待用户提供 `ghp_` PAT + owner/repo |

---

## 📥 安装方式（双通道）

本 Skill 支持两种安装方式，用户可根据场景自由选择：

### 🗣️ 方式一：对话安装（推荐新手）

通过 WorkBuddy / 虾友SkillHub 市场一键安装，安装后**直接在聊天中操作**。

```
用户：帮我把「我的Skill」发布到虾友SkillHub
助手：好的，请提供Skill目录路径……
用户：/path/to/my-skill
助手：[读取SKILL.md] [三重验证] [智能归类] → ✅ 发布成功！
```

**优点**：
- 零配置，安装即用
- AI 自动引导填写各平台 Token
- 智能类目识别、审核关键词规避等经验自动注入

**安装步骤**：
1. 在 WorkBuddy「技能市场」搜索「Skill矩阵分发助手」
2. 点击安装
3. 对话中说出「发布到虾友SkillHub」即可开始

---

### 💻 方式二：命令行安装（推荐开发者）

将本 Skill 作为独立 CLI 工具安装，在终端中运行。

**Linux / macOS**：
```bash
# 下载安装脚本并校验 SHA256
curl -fsSLo /tmp/install.sh https://raw.githubusercontent.com/qingmuhuijianghu/qingmuhui-skills/v3.5.0/skill-matrix-publisher-free/scripts/install.sh
# 校验 SHA256（从官方 releases 页面获取最新 checksum）
# sha256sum -c <<< "EXPECTED_SHA256  /tmp/install.sh"
bash /tmp/install.sh && rm /tmp/install.sh
```

**Windows（PowerShell）**：
```powershell
# 下载安装脚本并校验
$url = "https://raw.githubusercontent.com/qingmuhuijianghu/qingmuhui-skills/v3.5.0/skill-matrix-publisher-free/scripts/install.ps1"
$file = "$env:TEMP\install.ps1"
Invoke-WebRequest -Uri $url -OutFile $file
# 校验文件哈希（从官方 releases 页面获取）
# (Get-FileHash $file -Algorithm SHA256).Hash -eq "EXPECTED_SHA256"
& $file; Remove-Item $file
```

**手动安装**：
```bash
# 1. 克隆仓库（锁定 tag）
git clone --branch v3.5.0 --depth 1 https://github.com/qingmuhuijianghu/qingmuhui-skills.git
# 2. 复制到 WorkBuddy skills 目录
cp -r qingmuhui-skills/skill-matrix-publisher-free ~/.workbuddy/skills/
# 3. 安装依赖（固定版本号，避免供应链风险）
pip install requests==2.32.3
```

**CLI 使用示例**：
```bash
# 一键分发到所有平台
python ~/.workbuddy/skills/skill-matrix-publisher-free/scripts/matrix_publish.py /path/to/your-skill all

# 只发布到虾友SkillHub（需提供凭据）
python matrix_publish.py /path/to/your-skill skillhub \
  --api-key sk-xxxxxxxx \
  --invitation-code XXXX-XXXX

# 只发布到ClawHub
python matrix_publish.py /path/to/your-skill clawhub
```

**优点**：
- 可集成到 CI/CD 流程自动发布
- 批量处理多个 Skill
- 完全本地运行，凭据不入云端

---

| 特性 | 🗣️ 对话安装 | 💻 命令行安装 |
|------|:-----------:|:------------:|
| 上手难度 | ⭐ 零门槛 | ⭐⭐ 需基础终端操作 |
| 交互方式 | 自然语言对话 | 命令 + 参数 |
| Token 管理 | AI 对话中提供 | 配置文件或命令行参数 |
| CI/CD 集成 | ❌ | ✅ |
| 批量发布 | 逐个人工确认 | 脚本批量 |
| 适用人群 | 所有人 | 开发者/运维 |

---

## 🎯 核心功能

- ✅ **六平台一键分发**：腾讯SkillHub（个人版+团队版双通道）+ 虾聊 + 虾友SkillHub + GitHub + ClawHub
- 🆕 **腾讯SkillHub双通道**（v3.0）：个人版CLI全自动（`skh_` Token）+ 团队版浏览器上传（`sk-ent-` Key）
- 🛡️ **双重安全验证**（v3.7.0）：API Key + 邀请码，缺一不可（取消手机号+密码登录）
- 🧠 **智能类目识别**（v2.0）：自动分析Skill内容，精准匹配5大类52小类目
- 🏷️ **自动归档**：发布到SkillHub时自动归类到正确的二级类目
- ✅ **对话式配置引导**：手把手教你获取各平台API Key
- ✅ **自动打包压缩**：自动将SKILL.md打包成标准格式
- ✅ **批量管理配置**：保存多平台配置，永久复用
- ✅ **智能错误处理**：平台限流、认证失败自动提示解决方案

---

## 🧪 v3.2 实战验证：「社群收录」六平台全流程（2026-06-15）

> 以下是今天实际走通的完整发布流水账，每个平台每一步都踩过坑、验证过。

### 发布顺序（推荐）
```
腾讯SkillHub个人版 → 虾聊 → ClawHub → GitHub → 虾友SkillHub
（团队版走浏览器手动上传，不在此列）
```

### 1️⃣ 腾讯SkillHub 个人版（CLI一键）

**Token 格式**：`skh_` 开头（个人Token，非企业 `sk-ent-`）

**核心命令**：
```bash
# 登录
python skills_store_cli.py auth login --token skh_你的Token

# 发布（⚠️ 必须设置编码，否则 emoji 报错）
PYTHONIOENCODING=utf-8 python skills_store_cli.py publish ./skill-dir
```

**坑**：不设 `PYTHONIOENCODING=utf-8` 会导致 SKILL.md 中的 emoji（如 🎀）编码报错。

**SKILL.md frontmatter 必备字段**（与通用字段不同！）：
```yaml
slug: shequn-shoulu
displayName: 社群收录
version: 1.0.0
summary: 一句话简介
tags: [标签1, 标签2]
license: MIT
```

**验证**：CLI 返回 `skillId=88182 status=pending_review` 即成功。

---

### 2️⃣ 虾聊（API全自动）

**端点**：`POST https://clawdchat.cn/api/v1/posts` → 直接发帖

**Token 格式**：`clawdchat_` 开头

**必填字段**：`title` + `content` + `circle`（用slug格式如 `ai-doers`，不能用UUID）

**流程**：
```python
# 先查可用圈子列表
GET /api/v1/circles  → 获取 slug（如 ai-doers）

# 发帖（JSON body）
POST /api/v1/posts
{
    "title": "社群收录 Skill v1.2.0",
    "content": "Markdown格式的详细介绍...",
    "circle": "ai-doers"          # ⚠️ 必须用slug，不能用UUID！
}
```

**坑**：`circle` 用 UUID 格式返回 404，必须用 slug。
**注意**：`/f/upload` 是分享用的 GET 路由，不支持 POST 文件上传。

**验证**：`https://clawdchat.cn/posts/{postId}`

---

### 3️⃣ ClawHub（API全自动）

**端点**：`POST https://clawhub.ai/api/v1/skills`（multipart form）

**Token 格式**：`clh_` 开头

**关键参数**：
```python
{
    "slug": "shequn-shoulu",
    "displayName": "社群收录",
    "version": "1.0.0",          # ⚠️ ClawHub 强制要求
    "acceptLicenseTerms": True,  # ⚠️ 必须！否则 400
    "tags": ["community", "IMA", "knowledge-base"],  # ⚠️ 必须是英文！中文tag报422（Convex字段名限制）
}
```

**坑**：ClawHub tags **不能包含中文**（后端用 Convex，字段名只接受 ASCII），必须用英文 tag（如 `community` 替代 `社群`）。

**验证**：`https://clawhub.ai/skills/{skillId}`

---

### 4️⃣ GitHub（git push）

**Token 格式**：`ghp_` 开头（Personal Access Token classic，勾 `repo` 权限）

**完整流程**：
```bash
# Step 1: 从 Token 获取用户名
curl -H "Authorization: Bearer ghp_xxx" https://api.github.com/user
# → 返回 "login": "qingmuhuijianghu"

# Step 2: Clone 仓库
git clone "https://ghp_xxx@github.com/qingmuhuijianghu/qingmuhui-skills.git"

# Step 3: 复制 Skill 文件到子目录
cp -r ./shequn-shoulu/ ./repo/shequn-shoulu/

# Step 4: Commit & Push
git add -A && git commit -m "feat: 新增社群收录 Skill" && git push origin main
```

**坑**：GitHub Token 只能通过 `GET /api/user` 获取用户名，不能直接推断。

**Token 生成指引**：https://github.com/settings/tokens → Generate new token (classic) → 勾选 `repo`。

---

### 5️⃣ 虾友SkillHub（邀请码+API Key 认证 + 分类调优）

**端点**：
- 创建/更新：`POST /api/skills/publish`（同slug自动匹配）
- 更新分类：`POST /api/skills/{id}`（传 `skillType` + `categoryId`）
- 查询分类树：`GET /api/skills/categories`

**认证流程（v3.7.0 改造：取消手机号+密码登录）**：
```python
# v3.7.0 新流程：用户直接提供邀请码 + API Key，不需要手机号+密码
# 所有API调用用 API Key 做 Authorization: Bearer {api_key} 认证

# Step 1: 用户提供 邀请码 + API Key（两样东西，一步到位）
# Step 2: 验证 API Key 格式 + 远程校验
# Step 3: 验证 邀请码 格式 + 远程校验（用 API Key 做认证）
# Step 4: 后续所有API调用统一用 Authorization: Bearer {api_key}
```

**创建请求体（完整）**：
```python
{
    "name": "社群收录",
    "slug": "shequn-shoulu",
    "icon": "MessageSquare",
    "description": "完整的 SKILL.md 内容（禁止截断！）",
    "version": "1.0.0",
    "isFree": True,
    "visibility": "public",
    "skillType": "experience",           # ⚠️ 必须显式指定！
    "categoryId": "cat_tool_02_12", # 叶子节点ID
    "coverImage": "data:image/jpeg;base64,/9j/4AAQ...",  # v3.6
    "features": ["触发词1", "触发词2"],
    "requirements": ["WorkBuddy"],
    "fileTree": [
        {"name": "SKILL.md", "path": "SKILL.md", "type": "file", "content": "...", "size": 12345},
        {"name": "matrix_publish.py", "path": "scripts/matrix_publish.py", "type": "file", "content": "...", "size": 56789},
        {"name": "config.json", "path": "config.json", "type": "file", "content": "...", "size": 1234}
    ]
}
```

**Skill 大类型表（v3.6.0 新增，发布前必须让用户选择）**

> ⚠️ **这是发布流程中「第4步」让用户选择的6种大类型**，每种决定 Skill 在平台上的展示形态和功能模板。

| # | 类型名称 | skillType 值 | 说明 | 适用场景 |
|:-:|---------|:-----------:|------|---------|
| 1 | **经验传递** | `experience` | 创造者的单个 Skill 包 | 最常见，绝大多数 Skill 都选这个 |
| 2 | **图书Skill** | `book` | 一本书 + N 个章节 + AI 阅读 | 知识付费、读书类 Skill |
| 3 | **小说Skill** | `novel` | 一部小说 + N 个章节 + AI 阅读 | 小说创作、互动阅读类 |
| 4 | **课程Skill** | `course` | 一门课 = N 个模块 + AI 助教 | 教育培训、知识体系类 |
| 5 | **专家Skill** | `expert` | AI 分身 + 真人服务预约 | 专家IP、咨询预约类 |
| 6 | **社群导航** | `community` | N 个社群链接 + 免费浏览 3 个群 | 社群收录、导航类 |

**分类树（2026-06-15 快照）**：

| 一级类型 (skillType) | 二级分类 | 示例 categoryId |
|:---|:---|:---|
| `tool` | 赛博创新 | `cat_tool_01` ~ `cat_tool_01_06` |
| `tool` | 职业成长 → **AI办公** | `cat_tool_02_12` |
| `tool` | 生态商业 → 社群搭建/运营/裂变… | `cat_tool_03_01` ~ `cat_tool_03_20` |
| `tool` | 企业方案 | `cat_tool_04_01` ~ `cat_tool_04_10` |
| `tool` | 行业专家 | `cat_tool_05_01` ~ `cat_tool_05_07` |
| `community` | 按行业划分 → 17个子类 | UUID格式（如 `b28351b8-...`） |
| `community` | 按地域划分 → 9个城市 | UUID格式 |
| `book` | 商业管理/个人成长/职场技能 | `cat_book_01` ~ `cat_book_03` |
| `novel` | 都市/玄幻/言情/科幻/悬疑 | `cat_novel_01` ~ `cat_novel_05` |
| `course` | 社群运营/私域引流/个人品牌/AI工具/短视频 | `cat_course_01` ~ `cat_course_05` |

**坑1 —— AI审核关键词误杀**：
- Skill 被拒绝 → 查 `aiReviewDetails.matchedWords` 找触发词
- 今天实战：SKILL.md 写了"不要用某信""不收录虚假交易"，AI审核只看关键词，判定违规
- 修复：`某信` → `个人社交账号`，`虚假交易` → `不合规交易`

**坑2 —— 分类选错**：
- `community` 类型只有「按行业划分」「按地域划分」两个父级
- 最初选错归入 community/科技互联网，用户反馈后改为 tool/职场成长/AI办公
- 分类修改无需重建 Skill，直接 POST 到同一 ID 即可

**验证**：
```python
GET /api/skills/{id} → 确认 skillType + categoryId + status
```

---

### 📊 六平台完整对照表

| # | 平台 | 域名 | 认证方式 | API端点 | 全自动 |
|---|------|------|---------|---------|:---:|
| 1 | 🔷 腾讯SkillHub 个人版 | skillhub.cn | `skh_` Token | `api.skillhub.cn/api/v1/community/skills/publish` | 🤖 |
| 2 | 🔷 腾讯SkillHub 团队版 | skillhub.cn | `sk-ent-` Key | 浏览器手动上传 | 👤 |
| 3 | 🦞 虾聊 | clawdchat.cn | `clawdchat_` Key | `POST /api/v1/posts` (circle用slug) | 🤖 |
| 4 | 🔱 ClawHub | clawhub.ai | `clh_` Token | `POST /api/v1/skills` | 🤖 |
| 5 | 📦 GitHub | github.com | `ghp_` Token | `git push` | 🤖 |
| 6 | 🦐 虾友SkillHub | aiskillhub.vip | 邀请码+API Key（双重验证，v3.7.0起取消手机号+密码） | `POST /api/skills/publish` | 🤖 |

> ⚠️ **重复强调**：腾讯SkillHub (skillhub.cn) 和 虾友SkillHub (aiskillhub.vip) 是两个独立平台，API、Token、Skill ID 格式完全不同！

---

## 🔄 Skill 版本更新指南（v3.3 新增，v3.4 强化）

> **核心问题**：已发布的 Skill 出新版本后，能否用本助手**更新**而非**重新创建**？

**答案：可以！** 以下是各平台的版本更新机制：

---

### ⚠️ 更新铁律：版本号 + 历史记录必须同步（强制执行，详见规则8）

> **每次更新 Skill，必须同时完成两件事，缺一不可：**
> 1. **更新主版本号**：`version` 字段必须比当前版本更高（如 1.0.0 → 1.1.0 → 1.2.0）
> 2. **写入版本历史**：在平台写入本次更新的 changelog，让用户在「历史版本」页看到更新记录
> 3. **changelog 必须具体**：禁止"版本更新至 v1.x"等废话，必须写清楚具体改了什么（详见规则8）

**为什么必须两件事都做？**
- 只更新版本号但不写历史 → 用户不知道改了什么，「历史版本」页空白
- 只写历史但版本号不变 → 平台前端无法识别为新版本，仍显示旧版本号
- changelog 写废话 → 等于没写，用户还是不知道改了什么
- 三件事都做 → 版本号正确显示 ✅ + 历史版本页完整 ✅ + 更新内容清晰 ✅

---

### 更新机制总览

| 平台 | 更新方式 | 端点/命令 | 自动检测已有？ | 版本历史写法 |
|------|---------|----------|:---:|----------|
| 🦐 **虾友SkillHub** | slug优先查询 → name兜底搜索 → 找到则POST到`{id}` | `POST /api/skills/{id}`（创建用 `/api/skills/publish`，**更新用 `POST /api/skills/{id}`（v3.7.10修正：PATCH不更新version，必须以POST+同一ID更新）**） | ✅ 代码已实现（v3.7.1 slug优先匹配） | `POST /api/skills/{id}/versions` |
| 🔱 **ClawHub** | 同 slug + 新 version → POST 同一端点 | `POST /api/v1/skills` | ✅ 自动 upsert | 自动（payload 里 changelog 字段） |
| 📦 **GitHub** | git push 更新文件 | `git push` | ✅ 覆盖旧文件 | commit message 即历史记录 |
| 🔷 **腾讯SkillHub 个人版** | multipart publish 同 slug 自动覆盖 | `POST api.skillhub.cn/.../publish` | ✅ slug 匹配 | 自动（payload 里 changelog 字段） |
| 🔷 **腾讯SkillHub 团队版** | 浏览器手动重新上传 | Web UI | 👤 手动 | 手动填写 |
| 🦞 **虾聊** | 创建新帖（非严格"更新"） | `POST /api/v1/posts` | ⚠️ 新帖 | 帖子内容即更新说明 |

---

## 🗑️ Skill 删除场景（v3.7.1 新增）

> **核心问题**：某个Skill不要了要删除，必须精准识别同一个Skill，避免删错！

### 删除匹配逻辑（与发布/更新一致）

```
3a. slug优先：GET /api/skills/{slug}/install-info → 200 = 命中
3b. name兜底：GET /api/skills?keyword={name} → 遍历先比slug再比name
```

**三层安全保障**：

| 层级 | 机制 | 说明 |
|:---:|------|------|
| 1️⃣ | **slug优先匹配** | slug是平台唯一标识，不会因名字差异删错 |
| 2️⃣ | **匹配详情展示** | 删除前显示 ID/名称/Slug/版本/匹配原因 |
| 3️⃣ | **dry-run预览** | 默认只预览不删，必须 `--confirm` 才真正删除 |

### 删除对话引导流程

```
用户：帮我删掉「社群收录」这个skill

小青：好的～删除前我先帮你确认一下这个Skill的信息哦～🔍
     [双重验证：API Key + 邀请码] ✅
     
     [搜索匹配]
     [SEARCH] 按 slug 查询「shequn-shoulu」...
     [MATCH] ✅ slug命中，skill_id=12345
     
     ┌────────── 匹配到的Skill ──────────┐
     │  ID:    12345
     │  名称:  社群收录
     │  Slug:  shequn-shoulu
     │  版本:  v1.2.0
     │  匹配:  slug匹配(shequn-shoulu)
     └────────────────────────────────────┘
     
     ⚠️ 确认要删除这个Skill吗？此操作不可恢复！
     回复「确认删除」我就执行～

用户：确认删除

小青：[DELETE] 正在删除...
     ✅ 删除成功！「社群收录」已从虾友SkillHub移除～
```

### CLI 用法

```bash
# 预览（只看不删）
python matrix_publish.py delete /path/to/your-skill \
  --api-key sk-xxxxxxxx \
  --invitation-code XXXX-XXXX

# 确认删除
python matrix_publish.py delete /path/to/your-skill \
  --api-key sk-xxxxxxxx \
  --invitation-code XXXX-XXXX --confirm

# 也可以直接用skill名称（不用路径）
python matrix_publish.py delete "社群收录" \
  --api-key sk-xxxxxxxx --confirm
```

> ⚠️ **删除铁律**：
> 1. **slug优先匹配** —— 和发布/更新逻辑完全一致，不会删错
> 2. **先预览再确认** —— 默认 dry-run，必须显式确认才执行
> 3. **不可恢复** —— 删除后数据不可恢复，务必谨慎

---

### 虾友SkillHub 完整 API 路径速查（v3.7.5 新增，必看！）

> **常见踩坑**：很多教程告诉你"更新 skill 用 POST /api/skills/update"，**错！** 实际接口路径和方法如下：

| 操作 | 端点 | 方法 | 备注 |
|------|------|------|------|
| 创建 skill | `/api/skills/publish` | POST | **必须传 `price:0`** 即使免费 |
| **更新 skill** | **`/api/skills/{id}`** | **POST**（v3.7.10修正：PATCH返回200但不更新version，必须用POST） | **不能加 `/update` 后缀！** body 传 `{name, slug, description, version, ...}` |
| 查看详情 | `/api/skills/{id}` | GET | 完整 description 在 `data.description` |
| 安装信息 | `/api/skills/{id或slug}/install-info` | GET | 用于发布后验证 |
| 版本历史 | `/api/skills/{id}/versions` | POST | 写入 changelog |
| 分类树 | `/api/skills/categories` | GET | 拿到叶子节点 categoryId |

**关键代码示例（POST 更新，v3.7.10修正：PATCH不更新version）**：
```python
import requests
url = f'https://aiskillhub.vip/api/skills/{skill_id}'
resp = requests.post(  # v3.7.10: PATCH -> POST
    url,
    headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
    json={'name': 'xxx', 'slug': 'xxx', 'description': '完整长描述...'},
    timeout=30
)
# 成功 = HTTP 201 + code:200（POST返回201）
# 响应 data 是嵌套结构 data.data.description
```

### 虾友SkillHub 完整更新流程（两步缺一不可）

**Step 1：更新主体内容 + 版本号**
```python
# matrix_publish.py 的 publish_to_skillhub() 已实现自动检测：
# v3.7.1: slug优先 + name兜底 双重匹配，避免更新时变重复创建

# 3a. 优先用 slug 直接查询（最可靠）
GET /api/skills/{slug}/install-info
→ 200 = slug命中，拿到 skill_id → 走 UPDATE

# 3b. slug没命中，用关键词搜索 + slug/name 双重匹配
GET /api/skills?keyword={name}&page=1&pageSize=50
→ 遍历结果列表：先比 slug，再比 name

# 匹配到已存在 Skill → 走 UPDATE
if existing_skill_id:
    POST /api/skills/{existing_skill_id}   # 更新（v3.7.10修正：用POST不用PATCH）
else:
    POST /api/skills                        # 创建
```

**Step 2：写入版本历史记录（⚠️ 必须！不要忘记！）**
```python
# 每次更新后，必须调用此接口写入版本历史
# ⚠️ changelog 必须是具体更新内容，禁止"版本更新至 v1.x"等废话！
# ⚠️ 发布前必须向用户收集更新内容说明（详见规则8）
POST https://aiskillhub.vip/api/skills/{skillId}/versions
Body:
{
    "version": "1.2.0",          # 必须与 Step 1 里的版本号一致
    "changelog": "v1.2.0 新增：发布引导流程 —— Skill生成后引导用户安装矩阵发布助手，一键分发六大平台。",
    "releaseDate": "2026-06-17"  # 可选，默认当天
}
→ 返回 {"code":200, "data":{"id":"..."}}
```

**关键行为**：
- ✅ 描述、版本号、文件内容 → **全部覆盖更新**
- ✅ 分类（skillType + categoryId）→ **可单独修改**
- ✅ 版本历史：`POST /api/skills/{id}/versions` 支持多条记录，按版本号排序展示
- ✅ 「最新」标签：平台自动识别最高版本号显示「最新」badge
- ⚠️ **不会**改变已积累的下载量/评分
- ⚠️ DELETE `/versions/{id}` 不支持，写错的记录**无法删除**，需谨慎

**版本历史 changelog 写法规范**（详见规则8，强制执行）：
```
格式：v{版本号} {类型}：{具体描述}
类型：新增 / 优化 / 修复 / 重构

✅ 好的示例：
v1.1.0 优化：Skill蒸馏隔离 —— 用户将收录内容整理成Skill时，仅输出社群本身内容，不带入平台信息
v1.2.0 新增：发布引导流程 —— Skill生成后，引导用户安装「Skill矩阵发布助手」，确认后自动切换为发布模式

❌ 坏的示例（严禁）：
v1.1.0 版本更新至 v1.1.0      ← 废话，没说改了什么
v1.2.0 修复bug                  ← 哪个bug？怎么修的？
v1.3.0 优化体验                 ← 优化了什么？
```

---

## 🚀 使用场景

| 场景 | 触发词 |
|------|--------|
| 配置发布平台 | "配置分发平台"、"设置虾聊"、"配置GitHub" |
| 发布单个平台 | "发布到虾聊"、"上传到GitHub" |
| 一键分发五平台 | "一键分发"、"矩阵发布"、"发布到所有平台" |
| 查看配置 | "查看配置"、"我的平台配置" |
| 🗑️ 删除Skill | "删掉这个skill"、"从平台移除"、"下架skill" |

---

## 🦐 虾友SkillHub 发布流程（双重安全验证）

> ⚠️ **重要区分**：本节讲的是**虾友SkillHub**（`aiskillhub.vip`），不是腾讯SkillHub（`skillhub.cn`）。两者是完全不同的平台！

> ⚠️ **发布门槛（必须全部提供）**：API Key + 邀请码，两者缺一不可！
> 
> 🆕 **v3.7.0 改造**：取消手机号+密码登录要求！用户直接提供邀请码 + API Key，后续所有API调用通过 API Key 做认证。

### 双重验证详细说明（必须全部通过）

**验证逻辑（两步依次执行）**：

```
[1/2] API Key 验证
   → 向用户收集：API Key（引导用户去 个人中心 → 设置 → 开发设置 复制）
   → 格式检查：sk- 开头，长度 >= 10
   → 远程校验：GET /api/user/profile (Authorization: Bearer {api_key})
   → ✅ API Key 有效 / ❌ API Key 无效 → 停止

[2/2] 邀请码验证
   → 向用户收集：邀请码（引导用户去 个人中心 → 我的邀请码 查看）
   → 远程校验：POST /api/invitation/verify (Authorization: Bearer {api_key})
   → ✅ 邀请码有效 / ❌ 邀请码无效 → 停止
```

> ⚠️ **两个验证全部通过，才可以调用发布接口！**
> 任意一个验证失败，必须停止并提示用户，不得跳过！
> 
> ⚠️ **收集顺序**：先要 API Key → 验证通过后再要邀请码
> 
> ⚠️ **后续所有API调用统一用 API Key**：`Authorization: Bearer {api_key}`，不再需要 JWT token

### 对话式发布流程（小青三步依次引导）

> **v3.7.0 更新**：取消手机号+密码登录！用户直接提供 API Key + 邀请码，后续选分类+封面图，总共三步。

小青的引导流程（**分三步依次要，不是一次性全要；每步都要有温度**）：

```
用户：发布到虾友SkillHub

小青：嗨～发布到虾友SkillHub需要几步准备哦，我来一步步引导你～😊
     首先，请去【个人中心 → 设置 → 开发设置】复制 API Key，然后发给我吧～

用户：[提供 API Key]

小青：[执行第1步验证：API Key 验证]
      🛡️ 安全验证
      [1/2] API Key 验证... ✅
      ✓ API Key 有效！太棒了～✨
      
      接下来需要验证邀请码哦～请去【个人中心 → 我的邀请码】查看一下，
      把邀请码告诉我吧～😊

用户：[提供邀请码]

小青：[执行第2步验证：邀请码验证]
      [2/2] 邀请码验证... ✅
      ✓ 邀请码有效！双重验证全部通过～🎉
      
      接下来帮你的 Skill 选个类型吧！它属于哪种呢？😊
      
      [1] 经验传递  — 创造者技能包，单个 Skill（最常见）
      [2] 图书Skill  — 一本书 + 多章节 + AI 阅读
      [3] 小说Skill  — 一部小说 + 多章节 + AI 阅读
      [4] 课程Skill  — 一门课 = N 个模块 + AI 助教
      [5] 专家Skill  — AI 分身 + 真人服务预约
      [6] 社群导航  — 社群链接合集，免费浏览
      
      回复数字就行～或者直接告诉我也行～

用户：[选择分类，比如选 1 或说「经验传递」]

小青：好的～经验传递类型，收到！✅
      
      还有一件重要的事哦～你的 Skill 需要一张封面图～📸
      
      请提供一张封面图片（推荐尺寸 400x300px，JPG/PNG 格式）：
      
      ① 直接发图片给我（粘贴或拖拽都行～）
      ② 给我图片路径（如 C:/Users/xxx/cover.jpg）
      ③ 暂时没有？我可以用默认样式先发，以后再改
      
      你想哪种方式呢～？

用户：[发图片 或 给路径 或 说跳过]

小青：[处理封面图]
      如果用户发了图片/路径：
        ✓ 封面图收到！看起来不错～👍
      如果用户说跳过：
        ⚠️ 好的～这次先用默认样式发布，记得之后补上封面图更好看哦～
      
      🎉 所有信息都齐了！马上开始发布～
      
      [智能归类 + 发布]
      🤖 智能类目识别 -> XX > XX（置信度: XX%）
      ✅ 虾友SkillHub发布成功！🎊 
         封面图已上传 ✅｜类型：经验传递 ✅
         可以去平台看看你的 Skill 啦～
```

## 🔷 腾讯SkillHub 发布方案（v3.0：个人版 + 团队版双通道）

> ⚠️ **重要区分**：本节讲的是**腾讯SkillHub**（`skillhub.cn`），不是虾友SkillHub（`aiskillhub.vip`）。两者是完全不同的平台，域名、API、Token都不一样！

腾讯SkillHub 是腾讯 WorkBuddy/Qclaw 官方 Skill 市场，覆盖腾讯体系内 AI Agent 用户。
**2026年6月更新**：腾讯SkillHub 新增「团队版」功能，支持企业/团队独立发布和管理 Skills。

> 🆕 **v3.0 重要更新**：腾讯SkillHub 现在有两个发布通道，根据用户目标选择：

| 版本 | 发布方式 | 认证方式 | 发布到 | 适用场景 |
|------|---------|----------|--------|----------|
| **个人版** | CLI 命令行 `skillhub publish` | `skh_...` 个人Token | 个人空间 / 社区市场 | 个人开发者，开源分享 |
| **团队版** | 浏览器 Web 上传（文件夹或zip） | `sk-ent-...` 企业API Key | 团队 Skill 库 | 企业/组织统一管理 |

---

### 通道一：个人版（CLI 全自动）

#### 前置准备
1. 注册账号 + 实名认证（https://skillhub.cn）
2. 创建个人 API Token：`skh_...` 格式（个人中心 → API keys → 创建）
3. 安装 CLI：
   ```bash
   curl -fsSL https://skillhub.cn/install/install.sh | bash -s -- --cli-only
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```
4. 登录：
   ```bash
   skillhub auth login --token skh_你的Token --host https://api.skillhub.cn
   ```

#### SKILL.md 元数据要求（必填）
```yaml
---
slug: your-skill-name          # 全网唯一，小写字母+数字+连字符
displayName: 你的Skill名称      # 显示名称
version: 1.0.0                 # 版本号
summary: 一句话简介             # 摘要
description: 详细描述           # 完整描述（禁止截断！）
tags: [标签1, 标签2]            # 标签列表
license: MIT                   # 开源协议
---
```

#### 发布流程
```bash
# Step 1: Dry-run 预检
skillhub publish ./your-skill-dir --dry-run

# Step 2: 正式发布（Windows 必须设编码！）
PYTHONIOENCODING=utf-8 skillhub publish ./your-skill-dir --changelog "首次发布"
```
看到 `✓ Published: skillId=xxxxx status=pending_review` 即成功。

> ⚠️ **Windows 编码坑**：SKILL.md 含 emoji（如 🎀）时，不设 `PYTHONIOENCODING=utf-8` 会导致 GBK 编码错误。Mac/Linux 用户无需此设置。

#### 助手自动化流程
1. **检查元数据**：确保 SKILL.md 含 slug/displayName/version/tags/license
2. **执行 dry-run**：本地预检格式是否合规
3. **正式发布**：调用 `skillhub publish` 命令（Windows 需 `PYTHONIOENCODING=utf-8`）
4. **记录结果**：返回 skillId 和状态

---

### 通道二：团队版（浏览器上传）

#### 前置准备
1. 团队管理员登录 https://skillhub.cn
2. 进入「我的密钥」页面，创建企业 API Key（`sk-ent-...` 格式）
3. 确认已实名认证

#### SKILL.md 元数据要求（同个人版）
团队版的 SKILL.md frontmatter 要求与个人版完全一致。

#### 发布流程

**Step 1：助手自动打包**
助手将 Skill 目录（含 SKILL.md + references/ + scripts/ + assets/）打包为 `.zip` 文件。

**Step 2：浏览器手动上传**
1. 打开 https://skillhub.cn → 登录团队账号
2. 点击右上角「+ 发布 Skill」或左侧菜单「发布 Skill」
3. 在「发布新技能」页面：
   - **拖拽文件夹或 zip 文件**到上传区域（≤200个文件，≤10MB）
   - 或点击「选择文件夹」/「选择 zip 文件」按钮
4. **填写表单**：
   - **Slug *（必填）**：全网唯一标识符，仅允许小写字母、数字和连字符
   - **显示名称 *（必填）**：Skill 的显示名称
   - **图标**：选择一个合适的图标
   - **描述**：系统会自动从 SKILL.md 的 `description` 字段提取，也支持手动修改
5. 提交审核，通过后自动同步到**团队 Skill 库**

**Step 3：确认发布**
审核通过后，团队成员可在「团队技能」中搜索和使用该 Skill。

#### 助手职责
1. **准备 Skill 目录**：确保结构完整（SKILL.md + references/ 等）
2. **验证元数据**：slug、displayName、description、tags 等字段完整
3. **打包 zip**：生成符合要求的 .zip 包
4. **引导上传**：告诉用户每个表单字段应该填什么值
5. **记录分发状态**：将发布结果记入日志

### 如何选择版本？

```
用户：我要发布到腾讯SkillHub
助手：请问您要发布到哪个版本？
     [A] 个人版 — 发布到您的个人空间，CLI全自动，需要 skh_ 个人Token
     [B] 团队版 — 发布到团队 Skill 库，需要浏览器上传，需要 sk-ent- 企业Key
     
     如果不确定，告诉我：
     - 你是想让所有人都能搜到并安装？（→ 个人版）
     - 还是只想在你们团队内部使用？（→ 团队版）
```

---

## 🎯 虾聊发布方案（全自动API）

虾聊支持 **API Key** 方式直接上传Skill，实现真正的**一键自动化**！

### 全自动发布流程

**Step 1: 获取API Key**
1. 访问 https://clawdchat.cn
2. 注册 Agent 账号
3. 获取 API Key（格式：`clawdchat_xxxxxxxx`）

**Step 2: 配置API Key**
告诉 Skill："配置虾聊API Key"，提供用户名和 API Key

**Step 3: 一键发布（发帖方式）**
```python
# 先查圈子列表
GET /api/v1/circles  → 获取目标圈子的 slug

# 发帖发布 Skill
POST /api/v1/posts
{
    "title": "Skill名称 v1.0.0 | 青木会江湖出品",
    "content": "Markdown格式的Skill介绍（含安装方式、功能特性）",
    "circle": "ai-doers"  # ⚠️ 必须用slug，不能用UUID
}
→ 返回 postId，帖子页面即为 Skill 展示页
```
> ⚠️ `/f/upload` 是分享用途的GET路由，不支持POST上传文件。虾聊发布Skill的正确方式是**发帖**。

---

## 🔱 ClawHub 发布方案（全自动API）

ClawHub 是 OpenClaw 官方 Skill 注册中心（13,000+ Skills），支持 API 一键发布。

### 全自动发布流程

**Step 1: 获取 API Token**
1. 访问 https://clawhub.ai → GitHub 登录
2. 右上角头像 → Settings → API Tokens → Create Token
3. 复制 Token（格式：`clh_xxxxxxxx`）

**Step 2: 准备 SKILL.md**
确保 SKILL.md frontmatter 包含 ClawHub 必需字段：
```yaml
---
name: your-skill          # Skill 名称
version: 1.0.0            # 版本号（必须有！）
description: 完整描述      # 详细描述
---
```

> ⚠️ 注意：`version` 字段是 ClawHub 强制要求，缺失会被拒绝。

**Step 3: API 一键发布**

> ⚠️ **ClawHub multipart 字段名铁律（踩坑验证）**：multipart form 中 JSON 数据的字段名必须是 **`"payload"`**，绝不能写成 `"metadata"`！`"metadata"` 是其他平台的习惯写法，但在 ClawHub 会导致数据不被识别。以下代码中的 `files={"payload": ...}` 是正确的，切勿修改！

```python
import requests, json

payload = json.dumps({
    "slug": "your-skill-slug",
    "displayName": "显示名称",
    "version": "1.0.0",
    "changelog": "首次发布",
    "tags": ["tag1", "tag2"],
    "acceptLicenseTerms": True   # 必须！同意开发者协议
}, ensure_ascii=False)

resp = requests.post(
    "https://clawhub.ai/api/v1/skills",
    headers={"Authorization": "Bearer clh_你的Token"},
    files={
        "payload": (None, payload, "application/json"),     # ⚠️ 必须是 "payload"，不能是 "metadata"！
        "files": ("SKILL.md", skill_content.encode("utf-8"), "text/markdown"),
    }
)
```

成功返回：`{"ok":true, "skillId":"...", "versionId":"..."}`

**Step 4: 验证发布**
- Skill 页：`https://clawhub.ai/skills/{skillId}`
- 搜索：`https://clawhub.ai/search?q=your-skill-slug`

### 安全扫描注意事项
- 🔴 避免硬编码 API Key → 用环境变量并在 `metadata.openclaw.requires.env` 中声明
- 🟡 HTTP 端点 → 在 SKILL.md 中添加安全警告
- ⚠️ 必须先同意开发者协议（`acceptLicenseTerms: true`），否则 400 错误

### 常见错误
| 错误 | 原因 | 解决 |
|------|------|------|
| 400 acceptLicenseTerms | 未同意开发者协议 | 访问 clawhub.ai → Settings → Developer Settings → 同意协议 |
| 409 版本冲突 | 版本号已存在 | 升级版本号如 1.0.0 → 1.0.1 |
| 422 (tags) | tags 包含中文 | ClawHub 后端 Convex 字段名只接受 ASCII，必须用英文 tag（如 `community` 替代 `社群`）|
| 数据不识别/字段丢失 | multipart JSON 字段名用了 `metadata` | ClawHub multipart form 中 JSON 字段名必须是 **`"payload"`**，不能是 `"metadata"`（已踩坑验证）|
| 安全扫描不通过 | 硬编码凭证/未声明环境变量 | 改用环境变量 + 声明 metadata |

---

## 🛠️ 执行脚本

本Skill包含可执行脚本，位于 `scripts/` 目录：

| 脚本 | 功能 | 使用场景 |
|------|------|----------|
| `matrix_publish.py` | 一键分发主脚本 | 批量发布/更新到五大平台 |
| `publish_clawdchat_api.py` | 虾聊全自动发帖 ⭐推荐 | 配置API Key后一键发布 |
| `publish_clawhub.py` | ClawHub全自动发布 ⭐推荐 | 配置Token后一键发布到ClawHub |
| `publish_github.py` | GitHub发布脚本 | 代码托管和版本管理 |
| `install.sh` / `install.ps1` | 命令行安装脚本 | Linux/macOS / Windows 一键安装 |

---

## 📋 支持平台

> ⚠️ 腾讯SkillHub (skillhub.cn) ≠ 虾友SkillHub (aiskillhub.vip)，是两个完全不同的平台！

| 平台 | 域名 | 类型 | 特点 |
|------|------|------|------|
| 🔷 **腾讯SkillHub（个人版）** | skillhub.cn | 官方平台-个人 | CLI全自动发布，`skh_` Token认证，发布到社区市场 |
| 🔷 **腾讯SkillHub（团队版）** | skillhub.cn | 官方平台-团队 | 浏览器上传，`sk-ent-` 企业Key，发布到团队 Skill 库 |
| 🦞 **虾聊 (ClawdChat)** | clawdchat.cn | 社区平台 | AI Agent交流社区，国内用户活跃 |
| 🦐 **虾友SkillHub** | aiskillhub.vip | 自研平台 | 青木会虾友社官方平台，双重验证（API Key + 邀请码，v3.7.0起取消手机号+密码） |
| 📦 **GitHub** | github.com | 代码托管 | 开源生态，版本管理，全球开发者 |
| 🔱 **ClawHub** | clawhub.ai | 官方市场 | OpenClaw官方Skill市场，API全自动发布，13000+ Skills |

---

## ⚠️ 发布规则（强制执行）

> 🔴 **铁律：概述（description）必须完整，禁止极简/截断！**

### 规则1：完整概述 = SKILL.md 全文，禁止任何提炼/总结/截断（v3.7.6 升级）
- 🔴 **铁律**：`description` 字段 = **`SKILL.md` 完整原文 + 配套工作流文件（distillation-workflow.md 等）完整原文**，平台会自动渲染 markdown 表格、代码块、流程图
- **绝对禁止**任何形式的提炼、总结、改写、截断：
  - ❌ 把 10000 字 SKILL.md 总结成 530 字
  - ❌ 手写一句话 122 字 overview
  - ❌ 用 [:400]、[:800] 之类硬切
  - ❌ 任何 AI 二次加工
- **唯一正确做法**：
  ```python
  with open('SKILL.md', encoding='utf-8') as f:
      skill = f.read()
  with open('distillation-workflow.md', encoding='utf-8') as f:
      workflow = f.read()
  description = skill + '\n\n---\n\n# 完整工作流\n\n' + workflow
  ```
- **实战参考**（2026-06-23 验证）：
  - 龙虾Skill雷达：description = 10381 字（SKILL.md 全文 10465 字）→ 平台完整渲染
  - 经验炼金师：description = 6597 字（SKILL.md 全文 + workflow 全文）
  - 内容蒸馏师：description = 8360 字（SKILL.md 全文 + workflow 全文）
- **极简版概述（"AI助手"、"智能工具"）一律拒绝发布**
- **字数下限 ≥ 5000 字**（v3.7.6 升级），但**仅以文件全文为唯一来源**——不达 5000 字 = SKILL.md 本身太短，需补足

### 规则2：必须完整读取skill的所有内容文件
- 发布任何skill前，**必须完整读取**该skill的 `SKILL.md` 全文 + **所有配套 .md 文件**（distillation-workflow.md / publish-config.md / CHANGELOG.md / README.md 等）
- 全部塞进 `description` 字段（用 `\n\n---\n\n` 分隔），平台会按 markdown 渲染
- 禁止只读 frontmatter 就生成概述；禁止漏掉工作流文件

### 规则3：所有平台通用
此规则适用于**全部6个平台**（腾讯SkillHub个人版+团队版、虾聊、虾友SkillHub、GitHub、ClawHub）。
每个平台的 `description` 字段都必须完整。

### 规则4：发布后必须验证
- 任何平台发布/更新后，**必须调用查询接口确认**状态、分类、skillType 等字段已生效
- 虾友SkillHub 修改分类后 → `GET /api/skills/{id}` 确认
- 不要假设成功，**数据说话**

### 规则5：代码保障
矩阵发布助手脚本（`matrix_publish.py`）中，提取 description 的代码行：
```python
# ✅ 正确：不截断
description = ' '.join(desc_lines)

# ❌ 错误：截断（已修复）
# description = ' '.join(desc_lines)[:200]
```

### 规则6：文件完整性保障（v3.6.1新增）
> 🔴 **发布到虾友SkillHub时，fileTree 必须包含 skill 目录下的所有文件！**
> 
> - 遍历 skill_path 目录（排除 .git/__pycache__/.idea 等）
> - 将每个文件的 content 读出后放入 fileTree 数组
> - 不能只传 SKILL.md 一个文件，scripts/ 和 config.json 也必须上传
> - 与腾讯SkillHub的多文件上传逻辑保持一致

### 规则7：Skill元数据完整性保障（v3.7.2新增）🔴最高优先级
> 🔴 **发布任何Skill前，必须检查其元数据完整性。缺失字段必须补齐，禁止以"不影响发布"为由跳过！**

**发布前必须逐项检查的元数据清单**：

| 字段 | 必填 | 说明 | 缺失时处理 |
|------|:---:|------|-----------|
| `name` / `display_name` | ✅ | Skill名称 | ❌ 阻止发布，要求用户提供 |
| `slug` | ✅ | URL标识 | ❌ 阻止发布，要求用户提供 |
| `description` | ✅ | 完整描述（禁止截断） | ❌ 阻止发布，要求用户提供 |
| `version` | ✅ | 语义化版本号 | ❌ 阻止发布，要求用户提供 |
| `tags` | ✅ | 标签数组（至少3个） | ⚠️ **主动辅助用户生成** |
| `author` | ✅ | 作者名称 | ⚠️ 询问用户后补齐 |
| `category` | ✅ | 分类 | ⚠️ 引导用户选择 |
| `language` | ✅ | 语言标识 | ⚠️ 默认zh-CN，告知用户 |

**执行逻辑**：
1. 读取用户的SKILL.md → 解析frontmatter → 逐项检查上表字段
2. 任何字段缺失 → **立即停止发布流程**，列出缺失清单
3. `tags`/`author`/`category` 缺失 → 主动辅助用户生成（根据skill内容推荐标签）
4. 用户补齐后 → 重新检查 → 全部通过才允许发布
5. **禁止**以"不影响发布"、"平台不强制要求"为由跳过任何字段

**适用范围**：全部6大平台（腾讯SkillHub个人版+团队版、虾聊、虾友SkillHub、GitHub、ClawHub），免费版和付费版发布助手均适用。

> ⚠️ **反例（严禁）**：发现tags缺失 → "没有不影响发布" → 直接发布 ❌
> 
> ✅ **正例**：发现tags缺失 → "你的Skill缺少标签，我根据内容帮你推荐几个，你确认下？" → 补齐后发布 ✅

### 规则8：版本号 + 更新内容必须同步（v3.7.3新增）🔴强制执行
> 🔴 **每次更新Skill，版本号和更新内容（changelog）必须同步提交，缺一不可！**
> 
> - **版本号必须递增**：`version` 字段必须比当前线上版本更高（如 1.0.0 → 1.1.0）
> - **更新内容必须具体**：changelog 不能是"版本更新至 v1.1.0"这种废话，必须写清楚**具体改了什么**
> - **写入平台历史版本**：更新成功后必须调用 `POST /api/skills/{id}/versions` 写入版本记录，让用户在「历史版本」页看到
> - **禁止只升版本号不写内容**：用户看到版本号变了但不知道改了什么 = 无效更新
> - **禁止写废话changelog**：如"版本更新"、"修复bug"、"优化体验"等无信息量描述

**changelog 写法规范**：
```
格式：v{版本号} {类型}：{具体描述}
类型：新增 / 优化 / 修复 / 重构

✅ 好的 changelog：
  v1.1.0 新增：发布引导流程 —— Skill生成后引导用户安装矩阵发布助手，一键分发六大平台
  v1.2.0 修复：虾友SkillHub fileTree为空导致安装后0个文件的问题
  v2.0.0 重构：取消手机号+密码登录，改为API Key+邀请码双重验证

❌ 坏的 changelog（严禁）：
  v1.1.0 版本更新至 v1.1.0      ← 废话，没说改了什么
  v1.2.0 修复bug                  ← 哪个bug？怎么修的？
  v1.3.0 优化体验                 ← 优化了什么？
```

**对话中收集更新内容 + 区分发布/更新（v3.7.7 强化）**：
```
用户：帮我更新「社群收录」到 v1.3.0

小青：好的呀～这次 v1.3.0 具体更新了什么呢？请简单说一下更新内容～😊
     （这个会显示在平台的「历史版本」里，让用户知道改了什么）

     ⚠️ 顺便确认下：你说"更新"，意思是这个Skill 之前已经在平台上架了，对吧？
     ① 如果是 → 我会走 POST /api/skills/{旧ID} 更新（不会创建新条目）
     ② 如果其实还没上架（你想"发布"） → 走 POST /api/skills/publish 创建
     ③ 不确定 → 我帮你查一下再说～

用户：嗯是更新。更新内容：新增了企业社群收录模板

小青：收到！更新内容已记录～现在帮你发布 🚀
     [GET 查到旧 ID] → [POST 覆盖] → [POST /versions 写历史]
     📝 版本记录已同步: v1.3.0
         changelog: v1.3.0 新增：企业社群收录模板
```

**适用范围**：全部6大平台。虾友SkillHub通过 `POST /api/skills/{id}/versions` 写入；ClawHub/腾讯SkillHub通过 payload 的 changelog 字段传入；GitHub 通过 commit message；虾聊通过帖子内容。

### 规则9：发布/更新前必做「意图识别 + 旧版本探测」（v3.7.7新增）🔴最高优先级

> 🔴 **铁律**：每次用户说「发布」/「更新」/「同步」/「上新」前，**必须先识别用户意图，再探测平台是否已有同名 skill，缺一不可！**

**三大意图关键词**：
- 「发布」「上架」「首发」「初次」→ 创建新 skill
- 「更新」「升级」「同步新版」「推送新版」→ 更新已有 skill
- 「同步」「分发」→ 可能是上面两种之一，**必须先问**

**三步必做（强制执行）**：

```
Step 1：意图识别
   ├─ 用户原话包含「更新/升级/同步新版/推送」 → 走"更新"流程
   ├─ 用户原话包含「发布/上架/首发/初次」 → 走"发布"流程
   └─ 模糊词（「同步」「分发」「推一下」） → 先问用户，不要假设

Step 2：旧版本探测（仅"更新"意图需要）
   ├─ 虾友 SkillHub：GET /api/skills?keyword={name}&pageSize=50 → 遍历匹配 slug/name
   ├─ 找到旧版 → 记录旧 ID，告诉他："我找到了你的旧版 v{version}，ID={id}，要覆盖更新吗？"
   └─ 没找到 → 提示用户："没找到旧版，是要首次发布吗？"

Step 3：执行
   ├─ "更新" + 找到旧版 → POST /api/skills/{旧_id} + POST /{旧_id}/versions
   ├─ "更新" + 没找到 → 询问用户后决定
   └─ "发布" + 已存在 → 警告："这个 slug 已经有了，是要更新吗？"
```

**反例（今天发生的事故）**：
> 用户说"先发布到虾友 skillhub"，AI 没做意图识别 → 误走 POST /api/skills/publish → 同 slug 创建了新条目 → 平台出现两条同名 skill → 用户愤怒
> 
> 正解：用户说"先发布"——**新蒸馏的 skill 才是要发布，发布助手本身是"更新"**。AI 必须先想清楚"哪个 skill 要发"。

**适用范围**：全部6大平台，免费版和付费版发布助手均适用。

---

## ⚠️ 错误处理

**平台未配置**：提示用户先完成配置
**平台限流/429**：等待60秒自动重试
**认证失败/401**：引导用户重新获取Token
**Skill已存在/409**：提供更新或跳过选项

---

## 🎨 品牌信息

- **出品方**：青木会江湖 | 虾友社
- **官方网站**：https://qingmuhui.com
- **虾友SkillHub**：https://aiskillhub.vip
- **腾讯SkillHub**：https://skillhub.cn
- **版本**：v3.7.15

---

## 🔄 版本记录

> 完整历史版本记录请查看 [CHANGELOG.md](CHANGELOG.md)。

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| **v3.7.15** | 2026-06-25 | 🐛 **补ClawHub multipart规则**：明确 multipart form 中 JSON 字段名必须用 `"payload"` 不能用 `"metadata"`，补入常见错误表 + 代码注释，避免后人踩坑 |
| **v3.7.14** | 2026-06-25 | 🐛 **修复changelog中文乱码**：Windows下curl发送中文被GBK编码导致乱码，改用Python requests（UTF-8），清理2条历史乱码记录；补充DELETE /versions实际可用 |
| **v3.7.13** | 2026-06-25 | 🔴 **重大安全修复**：清空 config.json 中所有硬编码的开发者凭据（API Key/Token/邀请码/密码），全部替换为占位符；修正 SKILL.md 凭据表格为待填写状态 |
| **v3.7.12** | 2026-06-23 | 📦 **SKILL.md瘦身**：changelog历史记录拆分到独立 CHANGELOG.md，SKILL.md仅保留最近3个版本，解决虾友SkillHub数据库description字段溢出问题（67KB→~48KB） |

---

**记住：本Skill仅支持免费开源Skill的分发！**
**如需发布付费Skill，请使用「付费Skill发布助手」。**

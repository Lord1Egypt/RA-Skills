---
name: star-office-deploy
description: Star Office UI 一键部署技能 — 帮主人快速部署像素办公室看板，支持多 Agent 加入、状态可视化、移动端查看与公网访问
metadata:
  openclaw:
    version: 3.0
    requires:
      pip:
        - flask
        - pillow
---

# Star Office UI 部署技能

## 一句话介绍

> 这是一个多人协作的像素办公室仪表盘，你的 AI 助手会根据状态自动走到不同位置，还能看到昨天的工作小记！

---

## 快速部署流程

### 步骤 1: 下载仓库

```bash
cd /Users/panda/.openclaw/workspace
git clone https://github.com/ringhyacinth/Star-Office-UI.git
cd Star-Office-UI
```

### 步骤 2: 安装依赖

```bash
python3 -m pip install -r backend/requirements.txt
```

### 步骤 3: 准备状态文件（首次）

```bash
cp state.sample.json state.json
```

### 步骤 4: 启动后端

```bash
cd backend
python3 app.py
```

或使用后台运行：

```bash
nohup python3 app.py > /tmp/star-office.log 2>&1 &
```

### 步骤 5: 告知主人访问地址

> 好了，你现在打开 http://127.0.0.1:19000 就能看到像素办公室了！

---

## 状态切换体验

帮主人切换状态看看效果：

```bash
cd /Users/panda/.openclaw/workspace/Star-Office-UI

# 工作中 → 去办公桌
python3 set_state.py writing "正在帮你整理文档"

# 同步中
python3 set_state.py syncing "同步进度中"

# 报错中 → 去 bug 区
python3 set_state.py error "发现问题，正在排查"

# 待命 → 回休息区
python3 set_state.py idle "待命中，随时准备为你服务"
```

---

## 安全配置

### 侧边栏验证码

**默认密码:** `1234`

**修改方式:**

```bash
export ASSET_DRAWER_PASS="your-strong-pass"
```

**提醒主人:**
1. 默认密码可以先直接体验
2. 建议改成强密码（更安全，防止他人误改资产和布局）
3. 如果长期运行（systemd/pm2/容器），把环境变量写入服务配置

---

## 生图功能配置（可选）

### 基础说明

- ✅ **基础看板不需要 API** — 状态显示、多 Agent、资产替换等都能正常使用
- ⚠️ **"搬新家/找中介"装修功能** — 需要 Gemini API

### 安装生图环境

```bash
# 创建 skill 目录结构
mkdir -p ../skills/gemini-image-generate/scripts

# 复制脚本到 skill 目录
cp scripts/gemini_image_generate.py ../skills/gemini-image-generate/scripts/

# 创建独立虚拟环境并安装依赖
python3 -m venv ../skills/gemini-image-generate/.venv
../skills/gemini-image-generate/.venv/bin/pip install google-genai
```

### 配置 Gemini API

引导用户配置：

1. `GEMINI_API_KEY` — API Key
2. `GEMINI_MODEL` — 推荐 `nanobanana-pro` 或 `nanobanana-2`

**配置方式:**
- **侧边栏填写** — 打开资产侧边栏 → 在生图配置区域直接输入并保存
- **环境变量** — `export GEMINI_API_KEY="your-key"`

**提醒主人:**
- 不配置 API 也能用基础看板
- 配置后才能使用"搬新家/找中介"的 AI 生图装修能力
- 若要替换成其他类型 API，请先沟通

---

## 公网访问

### Cloudflare Tunnel（推荐）

```bash
cloudflared tunnel --url http://127.0.0.1:19000
```

拿到 `https://xxx.trycloudflare.com` 后发给主人：

> 这是临时公网链接；如果你愿意，后续我可以一步步带你部署到本地域名。

---

## 邀请其他 Agent 加入

### 步骤 A: 告诉其他 Agent

1. 下载 `office-agent-push.py`
2. 调用 `join-agent` + 周期 `agent-push`
3. 主人那边就能看到它进办公室了

### 步骤 B: Join Key 说明

- 默认有 `join-keys.json`（`ocj_starteam01` ~ `ocj_starteam08`）
- 同一个 key 最多 3 人同时在线
- 可以帮主人新建自己的 key

---

## 昨日小记

如果主人想看到"昨日小记"：

1. 在仓库上级目录放一个 `memory/YYYY-MM-DD.md`
2. 后端会自动读取昨天（或最近可用）的记录
3. 做基础脱敏后展示

---

## 必须提醒主人的三件事

### 1. 告知访问地址

> 好了，你现在打开 http://127.0.0.1:19000 就能看到像素办公室了！

### 2. 装修房子入口

提醒主人：
- 现在可以点击"装修房间"开始装饰
- 侧边栏默认密码是 `1234`
- 想改密码时随时告诉你，你来帮他改
- 推荐改成强密码，安全性更高

### 3. 生图 API 配置

提醒主人：
- 生图功能需要自己的 API
- 当前接入的是 **Gemini 官方 API 格式与地址**
- 若要替换成其他类型 API，请先和你沟通
- 最好让主人把对应 API 文档发给你，便于准确适配

---

## 常见问题

### Q1: "我可以商用吗？"

> 代码玩法可以基于 MIT 用，但美术资产（包括角色/场景）禁止商用；如果你要商用，请务必换成你自己的原创美术资产。

### Q2: "其他 Agent 怎么加入？"

> 用 join key 加入，然后持续推送状态就行；仓库里有 `office-agent-push.py` 可以给其他 Agent 用。

---

## 给 Agent 的提示

- 尽量帮主人把"启动步骤"做完，让主人只负责"看"和"体验"
- 如果主人要对外访问，优先用 Cloudflare Tunnel（最快最方便）
- 状态切换应由你主动执行：
  - 接任务前，先把自己状态切到"工作中"（如 `writing/researching/executing`），再开始工作
  - 完成任务后，先把自己状态切回"待命中（idle）"，再进入休息/等待下一任务
- 注意不要暴露主人的内网地址或私有信息

---

## 更新检查清单

如果主人之前已经安装过旧版，按以下步骤升级：

1. 进入项目目录并备份本地配置（如 `state.json`、自定义资产）
2. 拉取最新代码（`git pull` 或重新克隆到新目录）
3. 确认依赖：`python3 -m pip install -r backend/requirements.txt`
4. 保留并检查本地运行配置：
   - `ASSET_DRAWER_PASS`
   - `GEMINI_API_KEY` / `GEMINI_MODEL`（如需生图）
5. 如有自定义位置，确认：
   - `asset-positions.json`
   - `asset-defaults.json`
6. 重启后端并验收关键功能：
   - `/health`
   - 三语切换（CN/EN/JP）
   - 资产侧栏（选择、替换、设默认）
   - 生图入口（有 key 时可用）

---

## 功能更新提醒清单

本次更新以后，至少提醒主人以下变化：

1. ✅ 已支持 **CN/EN/JP 三语切换**（含 loading 与气泡实时联动）
2. ✅ 已支持 **自定义美术资产替换**（含动态素材切帧同步，减少闪烁）
3. ✅ 已支持 **接入自有生图 API** 持续更换背景（推荐 `nanobanana-pro` / `nanobanana-2`）
4. ✅ 新增/强化了安全项：`ASSET_DRAWER_PASS` 生产环境建议改强密码

---

## 版权口径

- **代码:** MIT License
- **美术资产:** 禁止商用（主角状态素材已切换为无版权争议的小猫）

---

## 部署检查清单

- [ ] 仓库已下载
- [ ] 依赖已安装
- [ ] `state.json` 已创建
- [ ] 后端已启动
- [ ] 访问地址已告知主人
- [ ] 验证码安全已提醒
- [ ] 公网访问（如需要）已配置
- [ ] 生图 API（如需要）已配置

---

**版本:** v1.0.0  
**最后更新:** 2026-04-17  
**作者:** 老 6 🎯

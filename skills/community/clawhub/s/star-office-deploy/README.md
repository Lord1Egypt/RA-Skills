# 🏢 Star Office UI 部署技能

一键部署像素办公室看板 — 支持多 Agent 加入、状态可视化、移动端查看与公网访问

---

## 🚀 5 分钟快速部署

```bash
# 1. 下载
git clone https://github.com/ringhyacinth/Star-Office-UI.git
cd Star-Office-UI

# 2. 安装依赖
python3 -m pip install -r backend/requirements.txt

# 3. 准备状态文件
cp state.sample.json state.json

# 4. 启动后端
cd backend && python3 app.py
```

**访问:** http://127.0.0.1:19000

---

## 📋 核心功能

| 功能 | 说明 |
|------|------|
| 🎭 状态看板 | AI 根据状态自动走到不同位置 |
| 👥 多 Agent | 支持多个 AI 助手同时在线 |
| 🌐 三语切换 | 中文/英文/日文 |
| 🎨 资产替换 | 自定义美术资产 |
| 📝 昨日小记 | 自动读取工作记录 |
| 🖼️ AI 生图 | Gemini API 装修房间（可选） |

---

## 🎮 快速体验

```bash
# 工作中
python3 set_state.py writing "正在帮你整理文档"

# 待命中
python3 set_state.py idle "待命中，随时准备为你服务"

# 报错中
python3 set_state.py error "发现问题，正在排查"
```

---

## 🔐 安全提醒

**默认密码:** `1234`

**建议修改:**
```bash
export ASSET_DRAWER_PASS="your-strong-pass"
```

---

## 📖 完整文档

详见 `SKILL.md`

---

**版本:** v1.0.0  
**License:** MIT (代码) / 禁止商用 (美术资产)

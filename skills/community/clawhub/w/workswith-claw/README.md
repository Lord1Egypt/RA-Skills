# Workswith Claw

> 为家，注入灵魂

[![GitHub Stars](https://img.shields.io/github/stars/workswith/claw?style=flat)](https://github.com/workswith/claw/stargazers)
[![License](https://img.shields.io/github/license/workswith/claw)](https://github.com/workswith/claw/blob/main/LICENSE)

---

## ⚠️ 重要说明

- **非 Home Assistant 官方集成**：本项目是独立的智能家居中间件，非 HA 官方维护
- **OpenClaw 技能包**：可通过 OpenClaw 平台安装使用
- **依赖 HA**：需要 Home Assistant 提供设备控制能力

---

## 一句话介绍

Workswith Claw 是一个运行在本地 Mac mini/服务器上的智能家居中间件，通过深度集成 Home Assistant，实现设备的语义化理解、习惯学习和智能预判，让你的家真正"懂"你。

---

## 核心特性

| 特性 | 说明 |
|------|------|
| 🏠 设备语义化 | 自动识别空间/功能标签，全部设备有序管理 |
| 🧠 意图理解 | 自然语言模糊匹配，说"洗澡"就知道开浴霸 |
| 📊 习惯学习 | 从使用数据中发现规律，主动优化 |
| 🎯 智能预判 | 预判需求，主动服务 |
| 🔒 隐私优先 | 所有数据本地运行，不上传云端 |

---

## 系统架构

```
                     ┌─────────────────────┐
                     │      用户入口        │
                     │ (iMessage/微信/语音) │
                     └──────────┬──────────┘
                                │
                     ┌──────────▼──────────┐
                     │    OpenClaw 框架    │
                     └──────────┬──────────┘
                                │
      ┌──────────────┬──────────┼──────────┐
      │              │          │          │
┌─────▼─────┐  ┌────▼────┐  ┌─▼────┐  ┌▼────────────┐
│ ClawSoul  │  │HomeAI   │  │ 设备 │  │  本地存储   │
│ (懂人)    │  │(洞察)   │  │ 语义 │  │ (记忆/画像) │
└─────┬─────┘  └────┬────┘  └──┬───┘  └─────────────┘
      │             │           │
      │      ┌──────▼──────┐    │
      │      │ Home        │    │
      │      │ Assistant   │◄───┘
      │      │ (设备) │
      │      └─────────────┘
      │
      │      ┌─────────────┐
      └─────►│  QNAP NAS   │
             │ (隐私备份)  │
             └─────────────┘
```

---

## 快速开始

### 1. 准备工作

| 依赖 | 说明 |
|------|------|
| Home Assistant | 已安装并运行 |
| Python 3.9+ | 运行后端服务 |
| OpenClaw | 消息路由框架 |

### 2. 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/workswith/claw.git
cd claw

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env，填写 HA 地址和 Token

# 4. 启动服务
python -m uvicorn src.main:app --host 0.0.0.0 --port 8081
```

### 3. 配置 Home Assistant

1. 打开 HA 设置 → 用户 → 长期访问令牌 → 创建令牌
2. 复制令牌到 `.env` 文件

```env
HA_URL=http://192.168.x.x:8123
HA_TOKEN=你的令牌
```

### 4. 首次对话

安装完成后，可以通过以下方式与 AI 助理对话：

| 方式 | 说明 |
|------|------|
| iMessage/微信/Telegram | 消息对话 |
| HomePod/小爱同学 | 语音对话 |

或者，打开浏览器访问 `http://localhost:8081/dashboard` 查看设备状态、数据洞察和系统配置。

**首次对话示例**：

```
"帮我开灯"
"洗澡了"
"看电影"
```

---

## 使用指南

### 基础控制

| 示例指令 | 执行动作 |
|----------|----------|
| "开灯" | 打开全屋灯光 |
| "关灯" | 关闭全屋灯光 |
| "洗澡" | 预热浴霸 |
| "看电影" | 开启观影模式 |

### 场景联动

```
"我要洗澡了"
→ 浴霸预热到 45°C
→ 浴室灯光开启
→ 排气扇开启

"看电影"
→ 投影仪开启
→ 窗帘关闭
→ 氛围灯调暗
→ 空调调至 24°C
```

### 习惯学习

AI 助理会自动学习你的使用习惯：
- 每天 19:30 开灯 → 建议设置自动开灯
- 每次洗澡前 10 分钟开浴霸 → 预热模式

---

## 常见问题 (FAQ)

### Q1: 支持哪些平台？

- **消息平台**: iMessage, Telegram, 微信, WhatsApp
- **语音入口**: HomePod, 小爱同学, 小度
- **运行平台**: Mac mini, Linux 服务器, Docker

### Q2: 需要多少设备？

推荐 Home Assistant 中有 20+ 智能设备，以充分发挥语义化和习惯学习的能力。

### Q3: 数据安全吗？

是的。所有数据严格运行在本地，不上传公有云。采用 HTTPS + MTLS 双向加密。

### Q4: 如何联系支持？

- GitHub Issue: https://github.com/workswith/claw/issues

---

## 集成指南

### 如何安装 Home Assistant？

1. **树莓派安装**
   ```bash
   # 下载树莓派镜像
   https://www.home-assistant.io/installation/raspberry-pi
   ```

2. **Docker 安装**
   ```bash
   docker run -d \
     --name homeassistant \
     --privileged \
     --network=host \
     -v ~/ha:/config \
     homeassistant/home-assistant:stable
   ```

3. **Mac 安装**
   ```bash
   # 使用 Homebrew
   brew install homeassistant
   brew services start homeassistant
   ```

### 如何导入米家设备？

1. **方案一：HA 内置集成**
   - 设置 → 设备与服务 → 添加集成
   - 搜索 "Xiaomi" 或 "米家"

2. **方案二：Mi Home 插件**
   - 使用 [Xiaomi HA](http://github.com/xiaomi/ha_xiaomi_home) 官方集成
   - 获取网关 token 后配置

3. **方案三：Yeelight**
   - 设置 → 设备与服务 → 添加集成
   - 搜索 "Yeelight"

---

## 安全与合规

### 代码安全审核
- ✅ 上传前移除所有调试代码
- ✅ 移除硬编码的 Token/密钥
- ✅ 使用 .gitignore 排除敏感文件
- ✅ 不包含用户数据

### 数据隐私
- ✅ 所有数据存储在本地设备
- ✅ 不收集、不上传任何个人数据
- ✅ 支持离线运行

### 使用条款
- ⚠️ 本软件按"原样"提供，不提供任何担保
- ⚠️ 用户需自行承担使用风险
- ⚠️ 请遵守当地法律法规使用

### 开源许可

MIT License - 详见 [LICENSE](LICENSE)

---

## 贡献指南

欢迎贡献代码！

```bash
# Fork 项目
# 创建特性分支
git checkout -b feature/xxx
# 提交更改
git commit -m 'Add xxx'
# 推送分支
git push origin feature/xxx
# 创建 Pull Request
```

---

## 感谢

- [Home Assistant](https://www.home-assistant.io/) - 伟大的开源智能家居平台
- [OpenClaw](https://github.com/openclaw/openclaw) - 消息路由框架
- 所有开源社区贡献者

---

## 赞助支持

如果你喜欢这个项目，欢迎赞助：

- GitHub Sponsors

---

*让每个家庭都有一个懂你的 AI 伙伴*

---

## 展望

后续会持续迭代优化，感谢你的支持！

如果你喜欢这个项目，欢迎 ⭐ Star 支持！

---

*让每个家庭都有一个懂你的 AI 伙伴 - 为家，注入灵魂*

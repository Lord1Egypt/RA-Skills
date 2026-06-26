---
name: workswith-claw
version: "1.0.2"
description: "为家，注入灵魂。独立于 Home Assistant 的智能家居中间件，通过 HA API 实现设备的语义化理解、习惯学习和智能预判。"
---

# Workswith Claw - 智能家居中间件

> 为家，注入灵魂

## 概述

Workswith Claw 是一个**独立运行**的智能家居中间件，通过调用 Home Assistant API 实现设备控制、语义化理解、习惯学习和智能预判，让你的家真正"懂"你。

**注意**：本项目不是 Home Assistant 集成插件，而是一个独立的后端服务，通过 HA API 与 Home Assistant 交互。

## 与 Home Assistant 的关系

- **调用方式**：通过 HA 长期访问令牌调用 REST API
- **独立运行**：可运行在任何支持 Python 3.9+ 的设备上（Mac mini、Linux 服务器、Docker）
- **自动化写入**：用户采纳建议时，会在 `~/.homeassistant/automations/` 目录创建 YAML 自动化文件（需确保 HA 自动化目录正确配置）

## 权限与凭证

本服务需要以下权限：

| 权限 | 说明 |
|------|------|
| `home_assistant` | 调用 HA API 控制设备 |
| `local_storage` | 本地存储习惯学习和配置数据 |
| `HA Token` | 需要在 `.env` 中配置 HA 长期访问令牌 |

## 核心功能

### 1. 设备语义化
- 自动识别空间/功能标签
- 全部设备有序管理
- 跨品牌设备统一调度

### 2. 意图理解
- 自然语言模糊匹配
- 说"洗澡"就知道开浴霸
- 说"看电影"自动调节氛围

### 3. 习惯学习
- 从使用数据中发现规律
- 主动优化建议
- 预判需求，主动服务

### 4. 隐私优先
- 所有数据本地运行
- 不上传云端
- 支持离线运行

## 系统要求

| 依赖 | 说明 |
|------|------|
| Home Assistant | 已安装并运行 |
| Python 3.9+ | 运行后端服务 |
| OpenClaw | 消息路由框架 |

## 快速开始

### 1. 安装

```bash
# 克隆项目
git clone https://github.com/workswith/claw.git
cd claw

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，填写 HA 地址和 Token
```

### 2. 配置 Home Assistant

1. 打开 HA 设置 → 用户 → 长期访问令牌 → 创建令牌
2. 复制令牌到 `.env` 文件

```env
HA_URL=http://192.168.x.x:8123
HA_TOKEN=你的令牌
```

### 3. 启动服务

```bash
python -m uvicorn src.main:app --host 0.0.0.0 --port 8081
```

### 4. 访问 Dashboard

打开浏览器访问 `http://localhost:8081/dashboard` 查看设备状态、数据洞察和系统配置。

## 使用示例

| 指令 | 执行动作 |
|------|----------|
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

## 文件结构

```
workswith-claw/
├── SKILL.md
├── README.md
├── requirements.txt
├── config/
│   └── devices.yaml        # 设备配置文件
├── src/
│   ├── main.py             # FastAPI 入口
│   ├── api/               # API 路由
│   ├── core/              # 核心逻辑
│   ├── models/            # 数据模型
│   ├── services/          # 业务服务
│   └── storage/           # 本地存储
├── static/                # 前端静态资源
└── tests/                 # 测试用例
```

## API 接口

| 接口 | 说明 |
|------|------|
| `GET /devices` | 获取所有设备 |
| `GET /devices/{id}` | 获取设备详情 |
| `POST /devices/{id}/control` | 控制设备 |
| `GET /dashboard` | Web 控制面板 |

## 依赖

- Python 3.9+
- FastAPI
- Home Assistant Client
- sqlalchemy

## 数据安全

- 本地存储，不上传云端
- 用户掌控，可随时清除
- 支持离线运行

## 权限

- `home_assistant`：集成 HA API
- `local_storage`：保存设备状态和习惯数据

---

*让每个家庭都有一个懂你的 AI 伙伴*

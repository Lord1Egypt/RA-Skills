# 📦 schedule-planner-cxf

> 全能出行管家 — 智能行程规划、交通比价、酒店推荐

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 📋 功能概览

| 功能 | 说明 |
|------|------|
| 🗺️ **行程规划** | 出差/旅游场景智能识别，自动生成行程框架 |
| 💰 **智能比价** | 多维度比价：交通方式、多日期、酒店性价比 |
| 📄 **行程网页生成** | 自动生成 HTML 行程单（左侧行程 + 右侧支付二维码） |
| 🧪 **Mock 模式** | 无需 API Key 即可体验全部功能 |

---

## 🚀 快速体验（Mock 模式，无需 API Key）

```bash
# 1. 安装依赖
cd schedule-planner-cxf-1.0.4
npm install

# 2. 使用 mock 模式直接生成行程网页
node scripts/generate-trip-page.js --mock
```

**预期输出：**
```
[Mock mode] Using built-in mock trip data
HTML generated: ./output/trip-Hangzhou-xxxxxxxx.html
Opened in browser: ...
```

---

## 🔧 完整使用（需配置 API Key）

### 安装依赖

```bash
cd schedule-planner-cxf-1.0.4
npm install
```

### 配置 API Keys

复制 `.env.example` 为 `.env` 并填入您的 API Key：

```bash
# 高德地图 API Key — https://lbs.amap.com/
AMAP_API_KEY=your_amap_api_key

# 途牛旅行 API Key — 联系途牛开放平台
TUNIU_API_KEY=your_tuniu_api_key
```

> ⚠️ **安全提醒**：`.env` 文件包含 API Keys，**切勿上传至 Git 或公开分享**。`.gitignore` 已自动排除。

### 生成行程网页

```bash
# 准备行程数据（JSON 格式）
# 参考 examples/mock-data.json 的格式

# 生成网页
node scripts/generate-trip-page.js
```

### 多城市行程查询

```bash
# 真实模式（需 TUNIU_API_KEY）
node scripts/query-5city-trip.js

# Mock 模式（无需 API Key）
node scripts/query-5city-trip.js --mock
```

---

## 🧪 Mock 模式说明

Mock 模式是本技能为审核和演示场景提供的特殊功能。它可以在不依赖任何外部 API 的情况下运行全部脚本。

| 命令 | 说明 |
|------|------|
| `node scripts/generate-trip-page.js --mock` | 使用内置 mock 数据生成行程网页 |
| `node scripts/query-5city-trip.js --mock` | 使用 mock 数据查询 5 城市行程 |
| 自动检测 | 无 `TUNIU_API_KEY` 时自动回退到 mock 模式 |

Mock 数据来源：`scripts/mock-data.js`（预置了杭州/南京/上海/苏州/北京等城市的模拟交通和酒店数据）

详见 [Mock 模式指南](examples/mock-mode.md)。

---

## 📁 项目结构

```
schedule-planner-cxf-1.0.4/
├── SKILL.md                     # 完整技能说明文档（含合规声明）
├── README.md                    # 本文件
├── package.json                 # Node.js 依赖
├── .env.example                 # 配置模板
├── .gitignore                   # Git 排除规则
├── scripts/
│   ├── generate-trip-page.js    # 生成行程网页（支持 --mock）
│   ├── mock-data.js             # Mock 数据模块
│   ├── qrcode.js                # 二维码生成（内置）
│   ├── query-5city-trip.js      # 多城市行程查询（支持 --mock）
│   ├── trip-planning.py         # 行程规划辅助（可选）
│   └── test-api.js              # API 测试脚本
├── examples/
│   ├── mock-data.json           # Mock 数据样例
│   ├── mock-mode.md             # Mock 模式完整指南
│   ├── demo-business-trip.md    # 脱敏演示：出差场景完整对话
│   └── demo-output.html         # 生成结果预览
└── references/
    ├── transport-comparison.md  # 交通方式对比参考
    └── city-guides.md           # 热门城市出行指南
```

---

## 🔒 安全说明

- `.env` 文件包含 API Keys 和个人信息，**切勿上传到 Git 或公开分享**
- 本技能**不收集、不存储**任何用户个人敏感信息
- 所有 API 调用由用户在本地完成，不传输至任何第三方服务器
- 本技能仅提供**信息规划和比价展示**，预订/支付需用户在第三方平台自行完成
- Mock 模式下所有数据均为模拟数据，不涉及真实个人信息

详见 SKILL.md 顶部的完整《隐私与合规声明》。

---

## ✅ 验证清单

审核员/新用户可自助验证：

- [ ] `npm install` — 依赖安装成功
- [ ] `node scripts/generate-trip-page.js --mock` — Mock 模式生成 HTML
- [ ] 打开 `output/` 目录下的 HTML 文件 — 查看行程展示
- [ ] `node scripts/query-5city-trip.js --mock` — 多城市行程查询演示
- [ ] 查看 `SKILL.md` — 确认隐私声明和合规内容
- [ ] 查看 `examples/` — 确认脱敏示例和实践证据

---

## 📝 版本历史

| 版本 | 变更 |
|------|------|
| **v1.0.6** | 添加 Mock 模式、隐私合规声明、examples/ 演示目录，清理敏感内容 |
| **v1.0.5** | npm 发布（修复 CLI 入口） |
| **v1.0.4** | npm 发布初始版本 |
| **v1.0.0** | 初始版本 |

---

## 👤 作者

[cryptocxf](https://clawhub.ai/user/cryptocxf)

## 📄 许可证

MIT License
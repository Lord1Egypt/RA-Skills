# Stock Advisor Pro — Local Skill (OpenClaw Plugin)

这是 Stock Advisor Pro 的本地插件端，用于集成到 OpenClaw 架构中。它提供个股深度扫描、持仓管理以及基于本地数据的隐私保护。

## 🧩 核心功能

- **Deep Scan (个股 X 光扫描)**: 调用云端后端获取 4 维评分与 AI 深度解读。
- **Portfolio Management (持仓管理)**: 在本地 `data/portfolio.json` 中存储持仓，绝不上云。
- **Command Line Interface**: 提供简单的命令交互。

## 🚀 快速开始

### 1. 安装依赖
本插件建议使用 `uv` 运行脚本，它会自动处理依赖：
```bash
# 确保已安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 配置环境
插件默认连接到 `http://localhost:8000`。如果您的后端部署在其他位置，请设置环境变量：
```bash
export STOCK_ADVISOR_API_URL="你的后端地址"
```

### 3. 使用命令

- **分析个股**: `uv run scripts/scan.py <股票代码>`
- **查看持仓**: `uv run scripts/portfolio.py show`
- **添加持仓**: `uv run scripts/portfolio.py add <代码> --cost <单价> --quantity <股数>`

## 📂 目录结构
- `SKILL.md`: OpenClaw 插件定义。
- `scripts/`: 执行脚本。
- `data/`: 本地存储（持仓、画像）。

# RHMCP Skill - OpenClaw 专用

[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-blue)](https://openclaw.ai)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

RHMCP 的 OpenClaw Skill 包装层，提供 **智能决策** 和 **Agent 指引**。

## 特性

- 🎯 **场景映射** - 用户意图 → APP 别名，无需查文档
- 🔧 **参数填充** - 自动填充默认参数
- 🧠 **存储决策** - AUTO 模式智能选择存储方式
- 🔗 **链式工作流** - URL 自动传递，支持多步骤任务
- 📖 **Agent 指南** - SKILL.md 即文档，OpenClaw 直接读取

## 快速开始

### 1. 安装 RHMCP

```bash
git clone https://github.com/AIRix315/RHMCP.git
cd RHMCP
npm install
npm run build
```

### 2. 配置 RHMCP

创建 `service.json`：

```json
{
  "baseUrl": "auto",
  "maxConcurrent": 1,
  "storage": { "mode": "none" }
}
```

创建 `.env`：

```bash
RUNNINGHUB_API_KEY=your_api_key_here
```

更新 APP 列表：

```bash
node dist/server/index.js --update-apps
```

### 3. 配置 OpenClaw

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "mcp": {
    "servers": {
      "rhmcp": {
        "command": "node",
        "args": ["E:/Projects/RHMCP/dist/server/index.js", "--stdio"],
        "env": {
          "RHMCP_CONFIG": "E:/Projects/RHMCP"
        }
      }
    }
  },
  "skills": {
    "entries": {
      "rhmcp-skill": {
        "enabled": true,
        "path": "E:/Projects/RHMCP/skills/openclaw"
      }
    }
  }
}
```

### 4. 重启 OpenClaw

重启 OpenClaw 使配置生效。

### 5. 使用

```
用户: 生成一张可爱的猫咪图片

Agent 将自动:
1. 识别场景 → 文生图
2. 选择 APP → qwen-text-to-image
3. 填充默认参数
4. 调用 rh_execute_app
5. 返回图片 URL
```

## 目录结构

```
skills/openclaw/
├── SKILL.md                 # Skill 定义 + Agent 指南
├── README.md                # 本文件
├── scripts/
│   └── executor.mjs         # 智能决策层（CLI 工具）
└── references/
    └── recommended-apps.json # 推荐 APP 清单
```

## 使用示例

### 文生图

```javascript
rh_execute_app({
  alias: "qwen-text-to-image",
  params: {
    text: "一只可爱的橘猫坐在窗台上，阳光洒落，动漫风格",
  },
});
```

### 图生图（链式）

```javascript
// 步骤 1：生成图片
const img1 = await rh_execute_app({
  alias: "qwen-text-to-image",
  params: { text: "一个女孩在樱花树下" },
});

// 步骤 2：修改图片
const img2 = await rh_execute_app({
  alias: "qwen-image-to-image",
  params: {
    image: img1.outputs[0].originalUrl,
    prompt: "换成冬天雪景背景",
  },
});
```

### 使用 executor.mjs 调试

```bash
# 列出所有 APP
node skills/openclaw/scripts/executor.mjs list

# 查看 APP 详情
node skills/openclaw/scripts/executor.mjs info qwen-text-to-image

# 根据场景推荐
node skills/openclaw/scripts/executor.mjs recommend generate-image

# 获取参数默认值
node skills/openclaw/scripts/executor.mjs defaults qwen-text-to-image

# 智能存储决策
node skills/openclaw/scripts/executor.mjs decide '{"isChainStep":true}'
```

## 相关项目

- [RHMCP](https://github.com/AIRix315/RHMCP) - RunningHub MCP Server
- [OpenClaw](https://openclaw.ai) - AI Agent 平台
- [RunningHub](https://www.runninghub.cn) - AI 内容生成平台

## 许可证

MIT License

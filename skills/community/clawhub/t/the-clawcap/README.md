<p align="center">
  <img src="assets/clawcap-logo.jpg" alt="The ClawCap" width="280">
</p>

# 🦞🧠 The ClawCap — 龙虾脑控帽

> 戴上 ClawCap，不是为了自己思考，而是放弃思考。
>
> *You put on the ClawCap not to think, but to stop thinking.*

为任意风格的头像无损添加配饰。AI 自动分析画风、光影、角度，生成完美融合的帽子/头饰。

**🌐 在线体验：[Demo](http://107.172.78.150:8000)** （每 IP 限 3 次/分钟）

## 核心特性

- **全品类兼容** — 真人照片、二次元、3D 渲染、NFT 像素风均可处理
- **画风自适应** — AI 自动匹配原图的画风、光影、透视角度
- **像素级保护** — 面部五官、身体、背景绝对不动
- **双模式运行** — Claude MCP Skill + Web UI 测试页面
- **纯 Gemini 架构** — 一个 API Key 搞定全流程

## 技术架构

```
阶段一  Gemini Flash VLM   → 提取画风/角度/光照 + 头顶坐标
          ↓
阶段二  Pillow/NumPy       → 根据坐标生成椭圆形羽化 Mask
          ↓
阶段三  Gemini 图像编辑    → 原图 + 动态 Prompt → 输出合成图
```

## 快速开始

### 1. 安装依赖

```bash
git clone https://github.com/ls569333469/The-ClawCap.git
cd The-ClawCap
pip install -r requirements.txt
```

### 2. 配置 API Key

```bash
cp .env.example .env
# 编辑 .env，填入你的 Gemini API Key
# 申请地址：https://aistudio.google.com/apikey
```

### 3. 启动方式

#### 方式 A：Claude MCP Skill（推荐）

在 Claude Desktop 的 `claude_desktop_config.json` 中添加：

```json
{
  "mcpServers": {
    "the-clawcap": {
      "command": "python",
      "args": ["/你的路径/The-ClawCap/mcp_server.py"],
      "env": {
        "GEMINI_API_KEY": "你的KEY"
      }
    }
  }
}
```

然后对 Claude 说：**"帮我给这个头像戴上红色龙虾钳帽子"** 🦞

#### 方式 B：Web UI 测试页面

```bash
python main.py
```

打开 http://localhost:8000 使用可视化界面。

## API 接口

### `POST /api/skill/alpha-equip`

```json
// 请求
{
  "image_base64": "base64 编码的头像图片",
  "accessory_prompt": "a red beanie hat with two curved red lobster pincers",
  "negative_prompt": "distorted face, low quality"
}

// 响应
{
  "status": "success",
  "result_image_base64": "处理后的图片 base64",
  "metadata": {
    "detected_fingerprint": {
      "art_style": "cartoon",
      "face_angle": "front-facing",
      "lighting_environment": "flat shading"
    },
    "processing_time_ms": 8500
  }
}
```

## 项目结构

```
The-ClawCap/
├── mcp_server.py              # Claude MCP Skill 入口
├── main.py                    # FastAPI Web 入口
├── config.py                  # 配置
├── requirements.txt           # 依赖
├── core/
│   ├── vision_fingerprint.py  # 阶段一：VLM 视觉指纹
│   ├── mask_generator.py      # 阶段二：Mask 遮罩生成
│   └── inpainter.py           # 阶段三：Inpainting 重绘
├── api/
│   ├── routes.py              # API 路由
│   └── schemas.py             # 请求/响应模型
├── utils/
│   └── image_utils.py         # 图像工具
└── static/
    └── index.html             # Web UI 测试前端
```

## 许可

MIT License

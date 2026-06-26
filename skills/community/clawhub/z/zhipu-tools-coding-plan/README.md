<p align="center">
  <h1 align="center">🔍 智谱工具 Coding Plan · Zhipu Tools</h1>
  <p align="center">
    <strong>基于 Z.AI Coding Plan MCP 的免费网络搜索 & 仓库文档搜索 Skill</strong><br/>
    <em>Free Web Search, Web Reader, GitHub Repo Search & File Parser — powered by Zhipu AI</em>
  </p>
</p>

<p align="center">
  <a href="#-功能特性">功能特性</a> · <a href="#-快速开始">快速开始</a> · <a href="#-配置说明">配置</a> · <a href="#-双模式说明">双模式</a> · <a href="#--coding-plan-套餐额度">免费额度</a>
</p>

---

## ✨ 为什么选择这个 Skill？

> **免费！真的免费！**
>
> 通过 Z.AI Coding Plan 的 MCP 端点调用智谱 AI 的搜索、网页读取和仓库文档搜索能力，**不需要账户余额，不需要充值，零成本使用**。

- 🔍 **网络搜索** — 实时搜索互联网，支持结果数量、时间范围、域名过滤
- 🌐 **网页读取** — 提取任意网页正文内容，返回标题、正文、元数据、链接列表
- 📚 **仓库文档搜索 (Zread)** — 搜索 GitHub 开源仓库文档、查看目录结构、读取文件
- 📄 **文件解析** — 支持 PDF、Word、Excel、PPT 等多种格式
- 🔄 **双模式** — MCP 模式（免费额度）+ Legacy 模式（账户余额），自动 fallback
- 🛠️ **开箱即用** — Shell 脚本 + Python 工具，适配各种使用场景
- 🔒 **安全** — API Key 通过环境变量或配置文件管理，不硬编码

## 🚀 功能特性

| 功能 | MCP 工具 | MCP 端点 | MCP 模式 | Legacy 模式 |
|------|----------|----------|:--------:|:-----------:|
| 网络搜索 | `web_search_prime` | `/web_search_prime/mcp` | ✅ 免费 | ✅ |
| 网页读取 | `webReader` | `/web_reader/mcp` | ✅ 免费 | ✅ |
| 仓库文档搜索 | `search_doc` | `/zread/mcp` | ✅ 免费 | ❌ |
| 仓库目录结构 | `get_repo_structure` | `/zread/mcp` | ✅ 免费 | ❌ |
| 仓库文件读取 | `read_file` | `/zread/mcp` | ✅ 免费 | ❌ |
| 文件解析 | — | — | ❌ | ✅ |
| 自动 Fallback | — | — | → Legacy | — |

> 所有 MCP 工具通过 **Z.AI Coding Plan** 免费额度调用，无需充值。

## 📦 安装

### 方式一：通过 ClawHub 安装（推荐）

```bash
clawhub install zhipu-tools
```

### 方式二：手动安装

```bash
# 克隆仓库
git clone https://github.com/wnzzer/zhipu-tools-coding-plan.git ~/.openclaw/workspace/skills/zhipu-tools
```

## ⚡ 快速开始

### 1. 配置 API Key

在 `openclaw.json` 中添加：

```json
{
  "skills": {
    "entries": {
      "zhipu-tools": {
        "apiKey": "YOUR_ZHIPU_API_KEY"
      }
    }
  }
}
```

或设置环境变量：

```bash
export ZHIPU_API_KEY="your_api_key_here"
```

> 💡 **如何获取 API Key？** 访问 [Z.AI 开放平台](https://open.bigmodel.cn/) 注册并创建 API Key。
> Coding Plan 订阅后，搜索、网页读取和仓库文档搜索通过 MCP 端点免费使用。

### 2. 使用

**网络搜索：**

```bash
# Shell 脚本
./scripts/web_search.sh "ChatGPT 最新动态" 5

# Python 工具（支持更多参数）
python3 scripts/zhipu_tool.py web_search "Go 语言最佳实践" \
  --count 10 \
  --recency week \
  --domain go.dev
```

**网页读取：**

```bash
# Shell 脚本
./scripts/web_reader.sh "https://example.com/article"

# Python 工具
python3 scripts/zhipu_tool.py web_reader "https://example.com/article"
```

**GitHub 仓库文档搜索 (Zread)：**

```bash
# 搜索仓库文档
./scripts/zread.sh search "openai/openai" "how to use streaming"
python3 scripts/zhipu_tool.py zread search "openai/openai" "how to use streaming"

# 查看目录结构
./scripts/zread.sh structure "openai/openai"
./scripts/zread.sh structure "openai/openai" "src/"
python3 scripts/zhipu_tool.py zread structure "openai/openai" --path src/

# 读取仓库文件
./scripts/zread.sh read "openai/openai" "README.md"
python3 scripts/zhipu_tool.py zread read "openai/openai" "README.md"
```

**文件解析：**

```bash
./scripts/file_parser.sh /path/to/document.pdf PDF
python3 scripts/zhipu_tool.py file_parser /path/to/report.docx --file-type DOCX
```

## ⚙️ 配置说明

### 环境变量

| 变量 | 必填 | 默认值 | 说明 |
|------|:----:|--------|------|
| `ZHIPU_API_KEY` | ✅ | — | 智谱 AI API Key |
| `ZHIPU_USE_MCP` | ❌ | `true` | 是否使用 MCP 模式（免费额度） |

### MCP 工具参数

#### web_search_prime

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `search_query` | 搜索关键词（必填） | — |
| `search_recency_filter` | `oneDay`, `oneWeek`, `oneMonth`, `oneYear`, `noLimit` | `noLimit` |
| `content_size` | `medium`, `high` | `medium` |
| `location` | `cn`, `us` | — |
| `search_domain_filter` | 限制搜索域名 | 无限制 |

#### webReader

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `url` | 目标网页 URL（必填） | — |

#### Zread (search_doc / get_repo_structure / read_file)

| 工具 | 参数 | 说明 |
|------|------|------|
| `search_doc` | `repo`, `query` | 搜索仓库文档 |
| `get_repo_structure` | `repo`, `path`(可选) | 查看目录结构 |
| `read_file` | `repo`, `path` | 读取仓库文件 |

## 🔄 双模式说明

| | MCP 模式（默认） | Legacy 模式 |
|---|---|---|
| **端点** | `api.z.ai/api/mcp/...` | `open.bigmodel.cn/api/paas/v4/...` |
| **费用** | 免费（Coding Plan 额度） | 账户余额 |
| **协议** | MCP (streamableHttp) | REST API |
| **切换方式** | 默认启用 | `ZHIPU_USE_MCP=false` |
| **适用场景** | 搜索、网页读取、仓库文档 | 大量调用、文件解析 |

> 💡 MCP 模式支持自动 Fallback：当 MCP 端点不可用时，会自动切换到 Legacy API（仅限搜索和网页读取）。

## 💰 Coding Plan 套餐额度

| 套餐 | 搜索/网页读取/仓库搜索 次数/月 | 价格 |
|------|:---------------------------:|:----:|
| **Lite** | 100 次 | 免费 |
| **Pro** | 1,000 次 | 免费 |
| **Max** | 4,000 次 | 免费 |

> 所有套餐均为免费！额度用完后次月自动重置。

## 🖼️ Vision MCP（额外能力）

除了上述功能，Z.AI 还提供本地运行的 Vision MCP 服务器，支持图像分析、视频分析、UI 转代码等 8 个工具：

```bash
npx -y @z_ai/mcp-server
```

工具列表：`image_analysis`, `video_analysis`, `ui_to_artifact`, `extract_text_from_screenshot` 等。

> Vision MCP 需要本地 npm 运行，暂未集成到本 Skill 脚本中。

## 📁 目录结构

```
zhipu-tools/
├── README.md            # 本文件
├── SKILL.md             # Agent Skill 定义（OpenClaw 使用）
├── LICENSE              # MIT 许可证
├── config.json          # API 端点配置
├── .gitignore           # Git 忽略规则
└── scripts/
    ├── web_search.sh    # 网络搜索 Shell 脚本
    ├── web_reader.sh    # 网页读取 Shell 脚本
    ├── zread.sh         # GitHub 仓库文档搜索 Shell 脚本
    ├── file_parser.sh   # 文件解析 Shell 脚本
    └── zhipu_tool.py    # Python 统一工具（推荐）
```

## 🤝 贡献

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m 'Add some feature'`
4. 推送分支：`git push origin feature/your-feature`
5. 提交 Pull Request

## 📄 许可证

[MIT License](./LICENSE) © 2025 wnzzer

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/wnzzer">wnzzer</a>
</p>

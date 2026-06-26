---
name: wan26-text-to-image
description: 使用阿里云万相 2.6 模型生成微信公众号封面图和技术架构设计图
author: 模型猎人
version: 1.0.1
---

# wan26-text-to-image

使用阿里云万相 2.6 模型生成微信公众号封面图和技术架构设计图。

## 功能

- **微信公众号封面图生成**：根据文章标题和内容生成 16:9 比例的封面图（1280×720）
- **技术架构设计图生成**：根据技术描述生成 AI/大模型相关的技术架构 visualization
- **文章配图生成**：根据段落内容生成多张配图

## 命令

### `generate_wx_cover`

生成微信公众号封面图

**参数：**
- `title` (string, 必填): 文章标题
- `content` (string, 可选): 文章内容摘要或关键词
- `style` (string, 可选): 风格描述，如"科技感"、"简约"、"商务"等
- `api_key` (string, 可选): 阿里云 API Key，如不提供则从环境变量 `DASHSCOPE_API_KEY` 或技能目录 `.env` 读取

**示例：**
```bash
generate_wx_cover title="大模型技术架构解析" content="Transformer, RAG, Agent" style="科技感，蓝色调"
```

### `generate_tech_diagram`

生成技术架构设计图

**参数：**
- `description` (string, 必填): 技术架构描述
- `components` (string, 可选): 主要组件列表，逗号分隔
- `style` (string, 可选): 图表风格，如"框图"、"流程图"、"架构图"等
- `api_key` (string, 可选): 阿里云 API Key

**示例：**
```bash
generate_tech_diagram description="RAG 系统架构，包含向量数据库、检索模块、生成模块" components="向量库，检索器，LLM, 知识库" style="清晰的架构图"
```

### `generate_article_images`

生成文章配图（支持多张）

**参数：**
- `content` (string, 必填): 段落内容
- `count` (int, 可选): 生成图片数量，默认 3 张，最多 5 张
- `size` (string, 可选): 图片尺寸，默认"1280*720"
- `api_key` (string, 可选): 阿里云 API Key

**示例：**
```bash
generate_article_images content="深度学习神经网络的工作原理" count=3 size="1280*720"
```

## 配置

### 环境变量

在终端中为「阿里云百炼」下发的密钥配置进程环境变量（名称以官方控制台为准，常见为 `DASHSCOPE_API_KEY`）。**勿**将真实密钥粘贴进本仓库中的任何已跟踪文件；本地仅使用 `.env`（已在 `.gitignore`）或各平台私密配置。

### 本地 `.env` 与 OpenClaw 共用配置

以下路径会**按顺序**加载（仅补充当前环境中尚未设置的变量，不覆盖已 export 的键）：

1. `OPENCLAW_ENV_FILE`（若设置）
2. 技能目录下本地 `.env`（需自行创建，已列入 `.gitignore`）
3. `~/.openclaw/.env`
4. `~/.workbuddy/.env`

可与其它技能共用同一份 `~/.openclaw/.env`；文件中仅存放由控制台下发的密钥，**不要**把 `.env` 提交到版本库。

创建生成器实例且未传 `--api-key` 时，会自动执行上述加载逻辑。

### 机器调用建议（新增）

为了让上游技能稳定解析结果，建议使用 `--json-only`：

```bash
python wan26_generator.py --json-only cover --title "RAG 幻觉治理" --content "RAG, Hallucination"
```

该模式会只在 `stdout` 输出 JSON，便于脚本解析。

### API Key 获取

1. 访问 [阿里云百炼控制台](https://help.aliyun.com/zh/model-studio/get-api-key)
2. 创建 API Key
3. 配置到环境变量或作为参数传入

## 文件输出目录

默认将下载的图片保存到 **`~/WorkBuddy/<技能文件夹名>/`**（与 `~/.workbuddy/skills` 下本技能目录名一致；代码中为 `os.path.join(expanduser('~'), 'WorkBuddy', basename(技能根目录))`，可通过 `--output-dir` 覆盖）。

## 输出规格

### 微信公众号封面图
- 尺寸：1280×720（16:9）
- 格式：PNG
- 无水印

### 技术架构图
- 尺寸：1280×1280 或自定义
- 格式：PNG
- 无水印

## 注意事项

- 图片 URL 有效期 24 小时，请及时下载保存
- 建议使用异步调用模式避免超时
- 生成时间约 1-2 分钟
- 按生成图片张数计费

## 依赖

- Python 3.7+
- dashscope SDK >= 1.25.8
- requests

## 安全与合规

- 本技能仓库**不包含**任何真实 API 密钥；密钥仅通过环境变量或本地 `.env` 注入。
- 运行 `setup.sh` / `config.py` 时，终端不会输出完整密钥；请勿将密钥提交至 Git 或截图外传。

## 参考

- [阿里云万相 2.6 API 文档](https://help.aliyun.com/zh/model-studio/wan-image-generation-api-reference)

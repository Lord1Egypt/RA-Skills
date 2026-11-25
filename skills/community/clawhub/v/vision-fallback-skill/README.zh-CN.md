# vision-fallback

[![skills.sh](https://skills.sh/b/vst93/vision-fallback-skill)](https://skills.sh/vst93/vision-fallback-skill)
[![English](https://img.shields.io/badge/README-English-blue)](README.md)
[![中文](https://img.shields.io/badge/README-中文-red)](README.zh-CN.md)

AI 编程助手的视觉理解兜底 skill。仅当**主模型无法理解图片**时触发（输出为空/
未知、置信度低、或用户反馈失败），对 UI 截图、终端输出、手机 App、布局重建等
场景进行结构化图片理解。

调用 **OpenAI 兼容的视觉 API**（`/chat/completions`），返回结构化 JSON
（`summary`、`objects`、`text_detected`、`ui_structure`、`inferred_elements`、
`uncertainty_notes`）。

## 支持的 Provider

| `VISION_PROVIDER` | 后端 | 默认模型 | Key 环境变量 | 区域 |
|---|---|---|---|---|
| `ark`（默认） | 火山引擎 Ark / 豆包 | `doubao-seed-2.0-lite` | `ARK_API_KEY` | 中国大陆 |
| `openai` | 任意 OpenAI 兼容 API | `gpt-4o-mini` | `OPENAI_API_KEY` | 全球 |

`VISION_API_KEY` 是通用 key，对**所有 provider** 生效。第三方端点
（OpenRouter、Azure、vLLM 等）设置 `VISION_BASE_URL` 和 `VISION_MODEL` 即可。

> ⚠️ 默认的 `ark` provider 部署在火山引擎（**中国大陆**）。海外用户可能遇到
> 延迟/可达性问题，可切换 `VISION_PROVIDER=openai` 使用全球可用的替代方案。

---

## 安装

### 通用方式（Claude Code、Cursor、Windsurf、Codex、…）

```bash
npx skills add vst93/vision-fallback-skill
```

> ℹ️ `npx skills add` 会安装到对应工具的 skill 目录（如 `~/.claude/skills/`）。
> 其他工具如果扫描不同路径则不会自动发现——参见下方的专项说明。

### ClawHub

```bash
clawhub install @vst93/vision-fallback-skill
```

> ClawHub slug 是 `vision-fallback-skill`（不是 `vision-fallback`）。
> 发布更新时用 `clawhub sync`（不要用 `clawhub skill publish` 手动指定 `--slug`），
> sync 会自动检测正确的 slug 和版本号。

### pi (earendil-works/pi-coding-agent)

pi **不**扫描 `~/.claude/skills/`。请安装到 pi 的发现路径：

```bash
# 方式 A：全局 skill 目录（推荐）
git clone https://github.com/vst93/vision-fallback-skill \
  ~/.pi/agent/skills/vision-fallback

# 方式 B：链接已有仓库
ln -s /path/to/vision-fallback ~/.pi/agent/skills/vision-fallback
```

或在 `~/.pi/agent/settings.json` 中注册路径：

```json
{
  "skills": ["/path/to/vision-fallback"]
}
```

项目级 skill 放到 `.pi/skills/`（受信项目）或 `.agents/skills/` 下。

### 验证安装

```bash
cd <skill-dir>
./scripts/check.sh
```

检查 shell 依赖、API key 解析、端点可达性。缺项会以可操作的错误信息退出。

---

## 配置

### 豆包（默认）

```bash
export VISION_PROVIDER=ark
export ARK_API_KEY=xxxxxxxxxxxxxxxx
```

### OpenAI

```bash
export VISION_PROVIDER=openai
export OPENAI_API_KEY=sk-...
```

### 第三方 OpenAI 兼容端点（OpenRouter、Azure、vLLM、…）

```bash
export VISION_PROVIDER=openai
export VISION_API_KEY=sk-...
export VISION_BASE_URL=https://your-provider.com/v1
export VISION_MODEL=your-vision-model
```

### Dotenv 文件

也可以将 key 存到 `~/.env_vars`：

```bash
# Provider 配置（均可选，环境变量优先）
VISION_PROVIDER=openai
VISION_BASE_URL=https://your-provider.com/v1
VISION_MODEL=your-vision-model

# API key（以下任选一种）
VISION_API_KEY=xxxxxxxxxxxxxxxx
# 或指定 provider：
# ARK_API_KEY=xxxxxxxxxxxxxxxx
# OPENAI_API_KEY=sk-...
```

完整 key 解析顺序见 [`references/configuration.md`](references/configuration.md)。

---

## 使用

主模型视觉失败时，agent 会自动加载此 skill。手动触发：

```
/skill:vision-fallback
```

核心调用：

```bash
./scripts/call-api.sh "$IMAGE" "$OCR_TEXT" "$FAILURE_REASON" "$PRIMARY_OUTPUT"
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `IMAGE` | 是 | 本地文件路径、`http(s)://` URL 或 `data:` URL |
| `OCR_TEXT` | 否 | 从图片提取的 OCR 文本 |
| `FAILURE_REASON` | 否 | 主模型失败原因 |
| `PRIMARY_OUTPUT` | 否 | 主模型的（不足）输出 |

---

## 目录结构

```
vision-fallback/
├── SKILL.md                      # 常驻加载：触发条件 + 工作流
├── scripts/
│   ├── check.sh                  # 预检：依赖 + key + 端点
│   ├── resolve-config.sh         # Provider/key/endpoint/model 解析
│   └── call-api.sh               # 图片 -> data URL + payload + curl POST
├── references/
│   ├── configuration.md          # Provider 配置、key 解析顺序
│   ├── api-reference.md          # 端点、请求头、body 格式
│   ├── output-format.md          # 响应 JSON schema
│   └── constraints.md            # 重试 / 升级规则
└── assets/
    └── payload-template.json     # 请求体模板（jq 渲染）
```

## 约束

- 仅在主模型视觉失败时触发。
- 每张图片仅调用一次（不重试）。
- 结果仍不充分 → 设置 `VISION_MODEL` 切换更强模型，或切换 `VISION_PROVIDER`。
  详见 [`references/constraints.md`](references/constraints.md)。

## 许可证

[MIT](LICENSE)

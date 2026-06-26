---
name: seedream5.0
description: 使用 Seedream5.0 接口进行文生图与参考图生成。当用户提到“生成图片”“出图”“海报图”“封面图”“根据参考图生成”或要求指定分辨率与水印时，优先使用本 skill。调用接口 fzGenerateImg5，参数含 prompt（必填）、size（可选）、watermark（可选）、image（可选）。需 x-api-key（kexiangai.com）。Do NOT use for OCR, video generation, or non-generative image editing.
---

你是“Seedream5.0 图像生成”技能。你的职责是稳定地调用 Seedream5.0 API 并返回清晰、结构化的生成结果。

## CRITICAL

- 调用接口前必须完成参数校验。
- 不得泄露完整 x-api-key，日志与回显仅允许掩码展示。
- 用户未提供 prompt 时，必须先补齐再调用。
- 单轮请求默认只调用一次；若失败，需先向用户说明失败原因再征求是否重试。
- 同一组参数不得在未获用户同意时重复提交。

## 何时使用

- 用户要生成图片、海报图、封面图、插画。
- 用户要求基于参考图继续生成。
- 用户指定分辨率（如 1024x1024、2048x2048）或要求开启/关闭水印。

触发短语示例：

- “帮我生成一张图片”
- “按这两张参考图再出一版”
- “做一张 2048x2048 的封面图”
- “不要水印，生成产品海报”

## 何时不要使用

- 用户要做视频生成或视频处理。
- 用户要做 OCR、表格识别、文档解析。
- 用户要做非生成式编辑（裁剪、压缩、加边框等）。

## 输入参数

- prompt：必填，支持中英文，建议不超过 300 汉字。
- size：可选，默认 2048x2048。
- watermark：可选，布尔值，默认 true。
- image：可选，参考图 URL 数组，默认空数组。
- x-api-key：必填，请求头字段，获取地址 kexiangai.com。

## 认证与 Key 复用

支持用户首次配置后长期复用，无需每次重复输入。

Key 读取优先级（从高到低）：

1. 本次对话显式输入的 x-api-key
2. 环境变量 X_API_KEY
3. 本地持久化文件 ~/.config/seedream5.0/.env

首次配置（只需一次）：

```bash
mkdir -p ~/.config/seedream5.0
cat > ~/.config/seedream5.0/.env << 'EOF'
X_API_KEY=你的x-api-key
EOF
chmod 600 ~/.config/seedream5.0/.env
```

## 核心接口

详细接口说明见 references/api-guide.md。

```bash
curl --location 'https://agent.mathmind.cn/minimalist/api/volcengine/ai/fzGenerateImg5' \
--header 'Content-Type: application/json' \
--header 'x-api-key: <YOUR_X_API_KEY>' \
--data '{"prompt":"一只猫咪在玩耍","size":"2048x2048","watermark":true,"image":[]}'
```

## 工作流（必须按顺序执行）

### Step 1: 收集输入

- 必填：prompt
- 选填：size、watermark、image
- 必填认证：x-api-key（可按优先级自动读取）

### Step 2: 参数校验与归一化

- prompt 必须非空。
- size 未提供时默认 2048x2048。
- watermark 未提供时默认 true。
- image 未提供时默认空数组。若提供，必须是 URL 字符串数组。

### Step 3: 调用 API

- URL 固定为：https://agent.mathmind.cn/minimalist/api/volcengine/ai/fzGenerateImg5
- 请求头：Content-Type: application/json + x-api-key
- 请求体：prompt、size、watermark、image

### Step 4: 返回结构化结果

- 参数摘要（标注默认值与用户显式输入）
- API 返回摘要（成功/失败）
- 失败时给出下一步建议

## 标准错误处理

- 缺少 x-api-key：提示去 kexiangai.com 获取，并说明可用 scripts/set_key.sh 持久化。
- 缺少 prompt：提示补充提示词。
- image 格式非法：提示应为 URL 字符串数组。
- 401/403：提示 key 无效、过期或权限不足。
- 429：提示触发限流，建议稍后重试。
- 5xx：提示服务异常，建议用户确认后重试。
- 网络超时：提示网络异常，可在用户确认后重试一次。

## 快速执行脚本

- ./scripts/set_key.sh "你的x-api-key"：保存 key 到 ~/.config/seedream5.0/.env
- ./scripts/generate.sh --prompt "提示词" [--size "2048x2048"] [--watermark true] [--image "https://example.com/a.png"]

## 目录结构（标准）

- SKILL.md
- scripts/set_key.sh
- scripts/generate.sh
- references/api-guide.md
- assets/

## 常见调试问题

### Skill 不触发

- 检查 description 是否覆盖真实用户表达（如“生成图片”“海报图”“参考图生成”）。

### 提示词过长导致效果不稳定

- 建议将 prompt 控制在 300 汉字以内，突出主体、场景、风格和构图要求。

### image 参数报错

- 检查是否为 URL 字符串数组，而不是单个对象或本地路径。

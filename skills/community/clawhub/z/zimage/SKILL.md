---
name: z-image
description: 使用 Z-Image 轻量级文生图接口生成图片。适用于用户要求“生成图片”“海报图”“封面图”“带中文文字的图片”，或直接说比例如 1:1、16:9、9:16 时。将用户的比例要求转换为 size 参数，按用户要求的数量精确执行且不得重复执行。调用接口 zImage，参数含 prompt（必填）与 size（可选）。需 x-api-key（kexiangai.com）。Do NOT use for image editing, OCR, or video generation.
---

你是“z-image 图像生成”技能。你的职责是根据用户的提示词、尺寸或比例要求，稳定地产生图像请求，并严格控制调用次数。

## CRITICAL

- 必须按用户要求的数量执行，不能多执行，也不能重复执行同一个请求。
- 若用户使用“比例”表达，必须先转换为 `size`，再调用 API。
- 调用接口前必须完成参数校验，不能跳过。
- 不得泄露完整 `x-api-key`，日志与回显仅允许掩码展示。
- 用户未提供 `prompt` 时，先补齐再调用 API。

## 何时使用

- 用户想做文生图
- 用户要求生成海报图、封面图、插画、带中英文字的图
- 用户指定比例，例如 `1:1`、`16:9`、`9:16`
- 用户指定生成数量，例如“帮我生成 3 张”

触发短语示例：

- “帮我生成一张海报图”
- “按 16:9 出 2 张封面图”
- “做一张带中文标题的产品图”
- “生成 4 张 1:1 的电商图”

## 何时不要使用

- 用户要做图生图、局部重绘、抠图、扩图等编辑类操作
- 用户请求 OCR、表格识别、文档解析
- 用户要做视频生成、视频理解或音频处理

## 输入参数

- `prompt`：必填，字符串
- `size`：可选，格式为 `宽*高`，默认 `1024*1536`
- `x-api-key`：必填，请求头字段，获取地址 `kexiangai.com`

## 比例转 size 规则

当用户没有直接给 `size`，但给了比例时，必须从推荐分辨率表中选择一个 `size`。

默认优先级：

1. 若用户明确给出 `size`，直接使用该 `size`
2. 若用户给出比例但未给清晰度偏好，默认使用 `1280*1280` 档对应的推荐 `size`
3. 若用户明确要更高细节，可使用 `1536*1536` 档对应的推荐 `size`
4. 若用户只说“默认”或未提比例，使用 `1024*1536`

常用比例默认映射（1280 档优先）：

- `1:1` -> `1280*1280`
- `2:3` -> `1024*1536`
- `3:2` -> `1536*1024`
- `3:4` -> `1104*1472`
- `4:3` -> `1472*1104`
- `7:9` -> `1120*1440`
- `9:7` -> `1440*1120`
- `9:16` -> `864*1536`
- `9:21` -> `720*1680`
- `16:9` -> `1536*864`
- `21:9` -> `1680*720`

完整映射表见 `references/api-guide.md`。

## 数量控制规则

- 默认生成数量为 `1`
- 若用户明确要求数量 `N`，则只执行 `N` 次调用
- 同一个请求不得因为解释、重试或重复理解而额外再执行一次
- 若单次执行失败，仅在用户明确要求重试时再次执行
- 输出时要说明本次计划执行的数量与实际执行的数量

## 认证与 Key 复用

支持用户首次配置后长期复用，无需每次重复输入。

### Key 读取优先级（从高到低）

1. 本次对话显式输入的 `x-api-key`
2. 环境变量 `X_API_KEY`
3. 本地持久化文件 `~/.config/z-image/.env`

### 首次配置（只需一次）

```bash
mkdir -p ~/.config/z-image
cat > ~/.config/z-image/.env << 'EOF'
X_API_KEY=你的x-api-key
EOF
chmod 600 ~/.config/z-image/.env
```

## 核心接口

详细接口说明见 `references/api-guide.md`。

```bash
curl --location 'https://agent.mathmind.cn/minimalist/api/tywx/zImage' \
--header 'x-api-key: <YOUR_X_API_KEY>' \
--header 'Content-Type: application/json' \
--data '{
  "prompt": "Elegant Christmas tree decorated with gold and white ornaments, glowing lights, and a soft gradient background",
  "size": "1024*1536"
}'
```

## 工作流（必须按顺序执行）

### Step 1: 收集与补齐输入

- 必填：`prompt`
- 选填：`size`
- 用户若提供比例，需要先记录比例值
- 用户若提供数量，需要记录数量值
- 必填认证：`x-api-key`（可从优先级策略自动读取）

### Step 2: 参数校验与归一化

- `prompt` 必须非空
- 若用户提供 `size`，校验格式必须为 `宽*高`
- 若用户提供比例但未提供 `size`，将比例转换为推荐 `size`
- 默认 `size` 为 `1024*1536`
- 默认数量为 `1`
- `size` 总像素必须在 `[512*512, 2048*2048]` 之间

### Step 3: 执行计划确认

- 明确本次将执行的次数
- 每次调用使用同一组已确认参数
- 不得额外补发请求

### Step 4: 调用 API

- 固定 URL：`https://agent.mathmind.cn/minimalist/api/tywx/zImage`
- 请求头：`x-api-key` + `Content-Type: application/json`
- 请求体字段：`prompt`、`size`

### Step 5: 返回结构化结果

- 返回内容应包含：
- 参数摘要（包括最终 `size`）
- 数量摘要（计划执行多少次，实际执行多少次）
- API 结果摘要（成功/失败）
- 失败时的下一步建议

## 标准错误处理

- 缺少 `x-api-key`：提示去 `kexiangai.com` 获取，并说明可用 `scripts/set_key.sh` 持久化
- 缺少 `prompt`：提示补充提示词后再执行
- `size` 格式非法：提示应为 `宽*高`，例如 `1024*1536`
- 比例无法映射：回退到默认 `1024*1536`，并告知用户
- 像素超限：提示调整到允许范围内
- 401/403：提示 key 无效、过期或权限不足
- 429：提示限流，建议稍后重试
- 5xx：提示服务异常，建议保留相同参数重试

## 输出质量检查清单

- 是否已完成必填参数校验
- 是否已经把比例转换为 `size`（若用户使用了比例）
- 是否明确说明本次执行数量
- 是否避免重复执行
- 是否对 key 做了掩码处理

## 快速执行脚本

- `./scripts/set_key.sh "你的x-api-key"`：保存 key 到 `~/.config/z-image/.env`
- `./scripts/generate.sh --prompt "提示词" [--size "1024*1536"] [--ratio "16:9"] [--count "2"] [--profile "1280"]`

## 目录结构（标准）

- `SKILL.md`
- `scripts/set_key.sh`
- `scripts/generate.sh`
- `references/api-guide.md`
- `assets/`

## 交互模板（对话时）

1. 尝试自动读取 key（`X_API_KEY` 或 `~/.config/z-image/.env`）
2. 若缺 key，提示用户提供 `x-api-key`（`kexiangai.com`）
3. 收集 `prompt`（必填）
4. 若用户给的是比例而不是 `size`，先将比例转换成 `size`
5. 收集数量；若未给出则默认 `1`
6. 明确本次仅执行该数量
7. 执行调用并给出结构化结果

## 常见调试问题

### Skill 不触发

- 检查 `description` 是否包含用户真实表达（如“生成图片”“16:9 封面图”“生成 3 张”）
- 可用调试问句：`When would you use the z-image skill?`

### Skill 重复执行

- 检查是否缺少“数量控制规则”与“执行计划确认”
- 先确认数量，再发起调用

### 比例没有转换成 size

- 检查是否遗漏了 `references/api-guide.md` 中的映射表
- 优先按 1280 档推荐分辨率转换
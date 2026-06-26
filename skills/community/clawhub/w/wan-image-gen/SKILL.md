---
name: wan-image-gen
description: |
  基于阿里云百炼 Wan 图像生成模型的生图 skill。支持文生图任务提交、轮询任务状态、下载生成图片到本地。
  当用户需要根据提示词生成图片、批量出图、指定尺寸或继续查询已有图片生成任务时，使用此 skill。
homepage: https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference
metadata:
  openclaw:
    requires:
      env:
        - DASHSCOPE_API_KEY
      bins:
        - node
    primaryEnv: DASHSCOPE_API_KEY
---

# Wan Image Gen

通过阿里云百炼 Wan 文生图接口创建异步任务，并自动轮询、下载生成结果。

详细接口与限制见 `references/api.md`。

## Setup

1. 配置 API Key：

```bash
export DASHSCOPE_API_KEY="sk-xxx"
```

也可以在 skill 目录下创建 `config.json`：

可先参考 `config.example.json` 再复制为 `config.json`。

```json
{
  "apiKey": "sk-xxx",
  "baseUrl": "https://dashscope.aliyuncs.com",
  "defaultGoal": "balanced",
  "goals": {
    "cheap": {
      "tier": "draft",
      "preset": "draft"
    },
    "balanced": {
      "tier": "standard"
    },
    "quality": {
      "tier": "final",
      "preset": "final"
    }
  },
  "defaultTier": "standard",
  "tiers": {
    "draft": {
      "model": "wanx2.0-t2i-turbo"
    },
    "standard": {
      "model": "wan2.2-t2i-flash"
    },
    "final": {
      "model": "wan2.6-t2i"
    }
  },
  "outputDir": "./outputs"
}
```

2. 运行环境要求 `Node.js >= 18`

配置优先级：

- CLI 参数
- 环境变量
- `config.json`
- 脚本默认值

## 默认模型

- 默认档位为 `final`，对应 `wan2.6-t2i`
- 推荐优先使用 `--tier`，只有明确要指定模型时再传 `--model`

## 目标驱动选型

- `cheap` -> `draft` + 默认 `preset=draft`
- `balanced` -> `standard`
- `quality` -> `final` + 默认 `preset=final`

推荐把这组映射维护在 `config.json` 的 `goals` 里；`goal` 表示用户意图，`tier` 表示具体模型档位。

## 档位驱动选型

- `draft` -> `wanx2.0-t2i-turbo`
- `standard` -> `wan2.2-t2i-flash`
- `final` -> `wan2.6-t2i`

推荐把这组映射维护在 `config.json` 的 `tiers` 里，而不是改主脚本。

## CLI

主要脚本：`node scripts/wan-image-gen.js`

### 低成本草稿

```bash
node scripts/wan-image-gen.js \
  --prompt="一间有着精致窗户的花店，漂亮的木质门，摆放着花朵" \
  --goal="cheap" \
  --ratio="1:1" \
  --n=1
```

### 最终出图

```bash
node scripts/wan-image-gen.js \
  --prompt="一个赛博朋克风格的雨夜街道，电影感灯光，雨水反光，细节丰富" \
  --goal="quality" \
  --ratio="16:9" \
  --name="cyberpunk-night"
```

### 提交任务但不等待

```bash
node scripts/wan-image-gen.js \
  --prompt="一个赛博朋克风格的雨夜街道" \
  --no-wait
```

### 继续轮询已有任务

```bash
node scripts/wan-image-gen.js \
  --task-id="你的task_id"
```

### 仅做预检，不实际提交

```bash
node scripts/wan-image-gen.js \
  --prompt="一张产品海报，主体是一瓶绿色玻璃香水" \
  --ratio="3:4" \
  --dry-run
```

## 参数约定

- `--prompt`：正向提示词。提交新任务时必填
- `--negative-prompt`：反向提示词
- `--goal=cheap|balanced|quality`：按用户目标选择更合适的默认模型和尺寸策略
- `--tier=draft|standard|final`：按成本/质量档位自动选模型
- `--model`：模型名，默认 `wan2.6-t2i`
  - 优先级：`model > tier > goal > 默认`
  - `config.json` 中可通过 `defaultGoal/defaultTier` 与 `goals/tiers` 维护映射
- `--ratio`：官方推荐比例快捷选项
  - `1:1=1280*1280`
  - `3:4=1104*1472`
  - `4:3=1472*1104`
  - `9:16=960*1696`
  - `16:9=1696*960`
- `--preset`：快捷尺寸预设
  - `draft=1280*1280`
  - `final=1440*1440`
  - `square=1280*1280`
  - `portrait=1104*1472`
  - `landscape=1472*1104`
  - `story=960*1696`
  - `widescreen=1696*960`
- `--size`：输出尺寸，如 `1280*1280`
  - 优先级：`size > ratio > preset`
- `--n`：生成张数，建议测试时设为 `1`
- `--seed`：随机种子
- `--prompt-extend=true|false`：是否启用提示词智能改写，默认 `true`
- `--watermark=true|false`：是否添加水印，默认 `false`
- `--task-id`：查询已有任务，不再提交新任务
- `--no-wait`：只提交任务，返回 task_id
- `--poll-interval`：轮询间隔秒数，默认 `10`
- `--timeout`：总等待超时秒数，默认 `600`
- `--output-dir`：图片下载目录，默认 `outputs/`
- `--name`：输出文件名前缀
- `--dry-run`：只打印最终请求体和配置预检，不实际调用 API

## 推荐工作流

1. 先用 `--goal=cheap` 做低成本验证。
2. Prompt 稳定后，切到 `--goal=balanced` 或 `--goal=quality`。
3. 再根据画面需求选择更贴近目标比例的 `--ratio=3:4`、`4:3`、`9:16` 或 `16:9`。
4. 如果需要更高细节，再切到 `--preset=final` 或显式自定义 `--size`。
5. 需要多轮迭代时，用 `--name` 给同一主题打上稳定前缀。
6. 下载后的文件名会自动带时间戳、task_id 和 prompt 摘要，便于回溯。

## 覆盖优先级

- 模型选择：`CLI --model > CLI --tier > CLI --goal > config.defaultGoal/config.goal > config.defaultTier/config.tier > config.model > 内置默认`
- 画幅选择：`CLI --size > CLI --ratio > CLI --preset > goal 默认 ratio/preset > config.ratio > config.preset > 脚本默认`
- `goal` 用于表达用户意图，`tier` 用于表达具体模型档位；显式 `--tier` 会覆盖 `goal`
- `tier` 和 `goal` 都只负责给出默认模型或默认尺寸策略，不会锁死 `size/ratio/preset`

## 提示词建议

- 先写清主体，再写场景、风格、光线、镜头或构图
- 如果只想改一个变量，prompt 里明确写“其余保持不变”
- 反复试 prompt 时，先保持 `n=1`
- 如果要稳定复现，显式传 `--seed`

## 工作流

1. 用户要生图时，提交异步任务。
2. 提交前脚本会显示一次成本提醒，按中国内地价格表估算总费用。
3. 返回 `task_id` 后轮询 `GET /api/v1/tasks/{task_id}`。
4. 成功后立即下载图片到本地目录。
5. 如果只想拿 `task_id`，使用 `--no-wait`。

## 成本提醒

- 脚本会在 `preflight` 和 `--dry-run` 中输出预计费用
- 当前内置的是你提供的中国内地单价表
- 图像费用按 `单价（元/张） × n` 估算
- 这不是实时计费查询；如果官方价格调整，需要同步更新脚本

## 失败时优先检查

- `DASHSCOPE_API_KEY` 或 `config.json` 是否配置正确
- `baseUrl` 和 API Key 是否属于同一地域
- prompt 是否过短或描述过于模糊
- 是否该先用 `--preset=draft` 而不是直接大尺寸反复试
- 尺寸是否符合所选模型限制
- 宽高比是否在 `[1:4, 4:1]` 范围内
- 自定义尺寸如果被服务端拒绝，优先改用官方推荐尺寸预设
- `n` 是否过大导致费用或限流问题
- `task_id` 是否已超过 24 小时

---
name: wan-video-gen
description: |
  基于阿里云百炼 Wan 文生视频模型的视频生成 skill。支持提交视频生成任务、轮询任务状态、下载生成视频到本地。
  当用户需要根据提示词生成视频、继续查询已有视频生成任务，或用 Wan 系列模型生成带声/无声视频时，使用此 skill。
homepage: https://help.aliyun.com/zh/model-studio/text-to-video-api-reference
metadata:
  openclaw:
    requires:
      env:
        - DASHSCOPE_API_KEY
      bins:
        - node
    primaryEnv: DASHSCOPE_API_KEY
---

# Wan Video Gen

通过阿里云百炼 Wan 文生视频接口创建异步任务，并自动轮询、下载生成结果。

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
      "tier": "draft"
    },
    "balanced": {
      "tier": "standard"
    },
    "quality": {
      "tier": "final"
    }
  },
  "defaultTier": "standard",
  "tiers": {
    "draft": {
      "model": "wan2.2-t2v-plus",
      "quality": "480p",
      "ratio": "16:9",
      "duration": 5
    },
    "standard": {
      "model": "wan2.5-t2v-preview",
      "quality": "720p",
      "ratio": "16:9",
      "duration": 5
    },
    "final": {
      "model": "wan2.6-t2v",
      "quality": "1080p",
      "ratio": "16:9",
      "duration": 5
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

- 默认档位为 `final`，对应 `wan2.6-t2v`
- 推荐优先使用 `--tier`，只有明确要指定模型时再传 `--model`

## 目标驱动选型

- `cheap` -> `draft`
- `balanced` -> `standard`
- `quality` -> `final`

推荐把这组映射维护在 `config.json` 的 `goals` 里；`goal` 表示用户目标，`tier` 表示具体模型档位和默认分辨率方案。

## 档位驱动选型

- `draft` -> `wan2.2-t2v-plus` + 默认 `480p` + `5秒`
- `standard` -> `wan2.5-t2v-preview` + 默认 `720p` + `5秒`
- `final` -> `wan2.6-t2v` + 默认 `1080p` + `5秒`

推荐把这组映射维护在 `config.json` 的 `tiers` 里，而不是改主脚本。

## CLI

主要脚本：`node scripts/wan-video-gen.js`

### 基础文生视频

```bash
node scripts/wan-video-gen.js \
  --prompt="一只小猫在月光下奔跑" \
  --goal="balanced"
```

### 提交任务但不等待

```bash
node scripts/wan-video-gen.js \
  --prompt="复古 70 年代风格地铁站中的街头音乐家" \
  --no-wait
```

### 继续轮询已有任务

```bash
node scripts/wan-video-gen.js \
  --task-id="你的task_id"
```

### 仅做预检，不实际提交

```bash
node scripts/wan-video-gen.js \
  --prompt="复古 70 年代风格地铁站中的街头音乐家" \
  --goal="cheap" \
  --dry-run
```

## 参数约定

- `--prompt`：正向提示词。提交新任务时必填
- `--negative-prompt`：反向提示词
- `--audio-url`：自定义音频 URL，仅 `wan2.6` / `wan2.5` 系列支持
- `--goal=cheap|balanced|quality`：按用户目标选择更合适的默认模型和分辨率方案
- `--tier=draft|standard|final`：按成本/质量档位自动选默认模型和分辨率方案
- `--model`：模型名，默认 `wan2.6-t2v`
  - 优先级：`model > tier > goal > 默认`
  - `config.json` 中可通过 `defaultGoal/defaultTier` 与 `goals/tiers` 维护映射
- `--quality`：分辨率档位，`480p|720p|1080p`
- `--ratio`：视频比例，`16:9|9:16|1:1|4:3|3:4`
- `--size`：输出尺寸，如 `1280*720`
  - 传给接口时必须是具体数值，不能写成 `16:9` 或 `720P`
  - 优先级：`size > quality+ratio > model 默认值`
- `--duration`：视频秒数，默认 `5`
  - `wan2.6-t2v`：支持 `2` 到 `15`
  - `wan2.6-t2v-us`：仅支持 `5`、`10`
  - `wan2.5-t2v-preview`：仅支持 `5`、`10`
  - `wan2.2-t2v-plus` / `wanx2.1-t2v-plus` / `wanx2.1-t2v-turbo`：固定 `5`
- `--prompt-extend=true|false`：是否启用提示词智能改写，默认 `true`
- `--shot-type=single|multi`：镜头模式，`wan2.6` 支持 `multi`
- `--seed`：随机种子
- `--task-id`：查询已有任务，不再提交新任务
- `--no-wait`：只提交任务，返回 task_id
- `--dry-run`：只打印最终请求体和配置预检，不实际调用 API
- `--poll-interval`：轮询间隔秒数，默认 `15`
- `--timeout`：总等待超时秒数，默认 `1800`
- `--output-dir`：视频下载目录，默认 `outputs/`

## 模型默认分辨率

- `wan2.6-t2v` / `wan2.6-t2v-us`：默认 `1920*1080`
- `wan2.5-t2v-preview`：默认 `1920*1080`
- `wan2.2-t2v-plus`：默认 `1920*1080`
- `wanx2.1-t2v-turbo`：默认 `1280*720`
- `wanx2.1-t2v-plus`：默认 `1280*720`

## 模型时长限制

- `wan2.6-t2v`：`2` 到 `15` 秒，默认 `5`
- `wan2.6-t2v-us`：`5` 或 `10` 秒，默认 `5`
- `wan2.5-t2v-preview`：`5` 或 `10` 秒，默认 `5`
- `wan2.2-t2v-plus`：固定 `5` 秒
- `wanx2.1-t2v-plus`：固定 `5` 秒
- `wanx2.1-t2v-turbo`：固定 `5` 秒

## 官方推荐尺寸

- `480p`
  - `16:9=832*480`
  - `9:16=480*832`
  - `1:1=624*624`
- `720p`
  - `16:9=1280*720`
  - `9:16=720*1280`
  - `1:1=960*960`
  - `4:3=1088*832`
  - `3:4=832*1088`
- `1080p`
  - `16:9=1920*1080`
  - `9:16=1080*1920`
  - `1:1=1440*1440`
  - `4:3=1632*1248`
  - `3:4=1248*1632`

## 工作流

1. 用户要生视频时，提交异步任务。
2. 提交前脚本会显示一次成本提醒，按中国内地价格表估算总费用。
3. 返回 `task_id` 后轮询 `GET /api/v1/tasks/{task_id}`。
4. 成功后立即下载 MP4 到本地目录。
5. 如果只想拿 `task_id`，使用 `--no-wait`。
6. 先按较低分辨率验证 prompt，再切到更高分辨率，避免无效消耗。

## 覆盖优先级

- 模型选择：`CLI --model > CLI --tier > CLI --goal > config.defaultGoal/config.goal > config.defaultTier/config.tier > config.model > 内置默认`
- 分辨率选择：`CLI --size > CLI (--quality + --ratio) > goal/tier 默认 quality/ratio > 模型默认`
- 时长选择：`CLI --duration > goal/tier 默认 duration > 模型默认`
- `goal` 用于表达用户目标，`tier` 用于表达具体模型档位；显式 `--tier` 会覆盖 `goal`
- 也就是说，`--goal balanced` 或 `--tier standard` 之后，你仍然可以显式传 `--quality`、`--ratio`、`--duration` 覆盖默认值

## 成本提醒

- 脚本会在 `preflight` 和 `--dry-run` 中输出预计费用
- 当前内置的是你提供的中国内地单价表
- 视频费用按 `单价（元/秒） × 时长（秒）` 估算
- 单价取决于模型和分辨率档位
- 这不是实时计费查询；如果官方价格调整，需要同步更新脚本

## 失败时优先检查

- `DASHSCOPE_API_KEY` 或 `config.json` 是否配置正确
- `baseUrl` 和 API Key 是否属于同一地域
- 尺寸和时长是否符合所选模型限制
- 是否把 `16:9`、`720p` 这类标签误当成 `--size` 传入
- 所选模型是否支持当前 `quality` 档位
- 所选模型是否支持当前 `duration`
- `wan2.2` 系列是否错误传了可变时长或音频 URL
- `task_id` 是否已超过 24 小时

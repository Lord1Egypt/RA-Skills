---
name: qwen-image-gen
description: |
  基于阿里云百炼 Qwen-Image 文生图模型的生图 skill。支持同步生成、异步任务轮询、下载生成结果到本地。
  当用户需要根据提示词生成图片、批量出图、指定尺寸/比例，或继续查询已有图片生成任务时，使用此 skill。
homepage: https://help.aliyun.com/zh/model-studio/qwen-image-api
metadata:
  openclaw:
    requires:
      env:
        - DASHSCOPE_API_KEY
      bins:
        - node
    primaryEnv: DASHSCOPE_API_KEY
---

# Qwen Image Gen

通过阿里云百炼 Qwen-Image 接口生成图片。默认使用 `qwen-image-2.0-pro`，支持按模型自动选择同步/异步模式，并在成功后下载 PNG 到本地。

详细接口、尺寸限制、价格表见 `references/api.md`。

## Setup

1. 配置 API Key：

```bash
export DASHSCOPE_API_KEY="sk-xxx"
```

也可以在 skill 目录下创建 `config.json`，参考 `config.example.json`。

2. 运行环境要求 `Node.js >= 18`

3. 北京和新加坡地域使用不同的 API Key 与 Base URL，不能混用

配置优先级：

- CLI 参数
- 环境变量
- `config.json`
- 脚本默认值

## 默认模型

- 默认模型：`qwen-image-2.0-pro`
- `qwen-image-2.0-pro`、`qwen-image-2.0`、`qwen-image-max` 走同步接口
- `qwen-image-plus`、`qwen-image` 走异步接口

## 支持范围

- `qwen-image-2.0-pro` / `qwen-image-2.0`：支持 1-6 张，适合通用文生图
- `qwen-image-max`：固定 1 张，偏真实感
- `qwen-image-plus` / `qwen-image`：固定 1 张，支持异步任务
- 图片输出格式为 `png`
- 任务和结果链接默认保留 24 小时，拿到后要尽快下载

## CLI

主要脚本：`node scripts/qwen-image-gen.js`

### 默认出图

```bash
node scripts/qwen-image-gen.js \
  --prompt="一间有着精致窗户的花店，漂亮的木质门，摆放着花朵" \
  --goal="quality"
```

### 低成本试探

```bash
node scripts/qwen-image-gen.js \
  --prompt="一个赛博朋克风格的雨夜街道" \
  --goal="cheap" \
  --n=1
```

### 异步任务

```bash
node scripts/qwen-image-gen.js \
  --prompt="复古海报风格的城市街景" \
  --model="qwen-image-plus" \
  --mode="async"
```

### 继续查询已有任务

```bash
node scripts/qwen-image-gen.js \
  --task-id="你的task_id"
```

### 仅做预检

```bash
node scripts/qwen-image-gen.js \
  --prompt="一张产品海报，主体是一瓶绿色玻璃香水" \
  --ratio="3:4" \
  --dry-run
```

## 参数约定

- `--prompt`：正向提示词，提交新任务时必填
- `--negative-prompt`：反向提示词，建议控制在 500 字符内
- `--goal=cheap|balanced|quality`：按用户意图选择默认模型和尺寸
- `--tier=draft|standard|final`：按档位选择模型
- `--model`：模型名，默认 `qwen-image-2.0-pro`
- `--mode=auto|sync|async`：自动选择或强制接口模式
- `--ratio`：快捷比例
  - `qwen-image-2.0*`：`1:1` `3:4` `4:3` `9:16` `16:9`
  - `qwen-image-max` / `qwen-image-plus` / `qwen-image`：`1:1` `3:4` `4:3` `9:16` `16:9`
- `--size`：具体分辨率，如 `2048*2048`
- `--n`：张数
  - `qwen-image-2.0*`：`1-6`
  - 其他模型：固定 `1`
- `--prompt-extend=true|false`：是否启用提示词改写，默认 `true`
- `--watermark=true|false`：是否添加水印，默认 `false`
- `--task-id`：查询已有异步任务
- `--no-wait`：只提交异步任务，不继续轮询
- `--poll-interval`：轮询间隔秒数，默认 `10`
- `--timeout`：总等待超时秒数，默认 `600`
- `--output-dir`：图片下载目录，默认 `outputs/`
- `--name`：输出文件名前缀
- `--dry-run`：只打印最终请求体和配置预检

## 工作流

1. 用户要生图时，优先提交新任务而不是直接假定已有结果。
2. `qwen-image-2.0-pro` / `qwen-image-2.0` / `qwen-image-max` 直接同步出图并下载。
3. `qwen-image-plus` / `qwen-image` 走异步任务，返回 `task_id` 后轮询。
4. 成功后立即下载生成结果到本地 `outputs/`。
5. 需要稳定复现时，显式传 `--seed`。

## 价格提醒

- 价格按中国内地单价表估算；如果使用新加坡地域，脚本会切换到国际单价表
- 计费按成功生成的图片张数计算
- 免费额度和单价会随官方更新变化，需同步更新脚本内置表

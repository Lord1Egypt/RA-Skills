---
name: chanjing-text-to-digital-person
description: Use Chanjing text-to-digital-person APIs to create AI portrait images, turn them into talking videos, optionally run LoRA training, poll async tasks, and explicitly download generated assets when requested.
metadata:
  openclaw:
    requires:
      env:
        - CHANJING_CONFIG_DIR
        - CHANJING_AUTO_OPEN_LOGIN
    homepage: https://open-api.chanjing.cc
---

# Chanjing Text To Digital Person

## When to Use This Skill

当用户要做这些事时使用本 Skill：

* 根据人物提示词生成数字人形象图
* 把生成的人物图转成会说话的短视频
* 查询文生图 / 图生视频 / LoRA 任务状态
* 在用户明确要求时，把生成图片或视频下载到本地

如果需求是“上传真人素材训练定制数字人”，优先使用 `chanjing-customised-person`。  
如果需求是“拿已有数字人做口播视频合成”，优先使用 `chanjing-video-compose`。

## Preconditions

本 Skill 自己包含本地配置和鉴权流程，不依赖其他 skill 的运行时脚本。

本 Skill 使用：

* 配置文件：`~/.chanjing/credentials.json`
* 若设置环境变量 `CHANJING_CONFIG_DIR`：使用 `$CHANJING_CONFIG_DIR/credentials.json`
* API 基础地址固定：`https://open-api.chanjing.cc`

当本地缺少 AK/SK 或 AK/SK 无效时，脚本默认返回登录引导信息，不自动打开浏览器。  
如需本地自动开页，可显式设置：`CHANJING_AUTO_OPEN_LOGIN=1`。
`https://www.chanjing.cc/openapi/login`

## Standard Workflow

主流程通常分两段，且都是异步任务：

1. 调用 `create_photo_task` 创建文生图任务，得到 `photo_unique_id`
2. 调用 `poll_photo_task` 轮询到成功，选一张 `photo_path`
3. 调用 `create_motion_task` 创建图生视频任务，得到 `motion_unique_id`
4. 调用 `poll_motion_task` 轮询到成功，得到最终 `video_url`
5. 只有在用户明确要求保存到本地时，才调用 `download_result`

可选扩展：

* 若用户想做 LoRA 训练，调用 `create_lora_task` 和 `poll_lora_task`
* `poll_lora_task` 成功后会返回一条 `photo_task_id`，可继续用 `poll_photo_task` 拿图

## Covered APIs

本 Skill 当前覆盖：

* `POST /open/v1/aigc/photo`
* `GET /open/v1/aigc/photo/task`
* `GET /open/v1/aigc/photo/task/page`
* `POST /open/v1/aigc/motion`
* `GET /open/v1/aigc/motion/task`
* `POST /open/v1/aigc/lora/task/create`
* `GET /open/v1/aigc/lora/task`

## Scripts

脚本目录：

* `scripts/`

| 脚本 | 说明 |
|------|------|
| `chanjing-config` | 写入/查看本地 `app_id` 与 `secret_key`，并清理旧 token 缓存 |
| `chanjing-get-token` | 从本地凭证获取有效 `access_token`（必要时自动刷新） |
| `_auth.py` | 读取凭证、获取或刷新 `access_token` |
| `create_photo_task` | 创建文生图任务，输出 `photo_unique_id` |
| `get_photo_task` | 获取单个文生图任务详情 |
| `list_tasks` | 列出文生图任务列表；返回中 `type=1` 为 photo，`type=2` 为 motion |
| `poll_photo_task` | 轮询文生图任务直到完成，默认输出第一张图片地址 |
| `create_motion_task` | 创建图生视频任务，输出 `motion_unique_id` |
| `get_motion_task` | 获取单个图生视频任务详情 |
| `poll_motion_task` | 轮询图生视频任务直到完成，默认输出视频地址 |
| `create_lora_task` | 创建 LoRA 训练任务，输出 `lora_id` |
| `get_lora_task` | 获取 LoRA 任务详情 |
| `poll_lora_task` | 轮询 LoRA 任务直到完成，默认输出第一条 `photo_task_id` |
| `download_result` | 下载图片或视频到 `outputs/text-to-digital-person/` |

## Usage Examples

示例 1：文生图后直接图生视频

```bash
PHOTO_TASK_ID=$(python3 scripts/create_photo_task \
  --age "Young adult" \
  --gender Female \
  --number-of-images 1 \
  --industry "教育培训" \
  --background "现代直播间背景" \
  --detail "短发，亲和力强，职业装" \
  --talking-pose "上半身特写，站立讲解")

PHOTO_URL=$(python3 scripts/poll_photo_task \
  --unique-id "$PHOTO_TASK_ID")

MOTION_TASK_ID=$(python3 scripts/create_motion_task \
  --photo-unique-id "$PHOTO_TASK_ID" \
  --photo-path "$PHOTO_URL" \
  --emotion "自然播报，语气清晰自信" \
  --gesture)

python3 scripts/poll_motion_task \
  --unique-id "$MOTION_TASK_ID"
```

示例 2：LoRA 训练

```bash
LORA_ID=$(python3 scripts/create_lora_task \
  --name "演示LoRA" \
  --photo-url https://example.com/1.jpg \
  --photo-url https://example.com/2.jpg \
  --photo-url https://example.com/3.jpg \
  --photo-url https://example.com/4.jpg \
  --photo-url https://example.com/5.jpg)

python3 scripts/poll_lora_task \
  --lora-id "$LORA_ID"
```

## Download Rule

下载是显式动作，不是默认动作：

* `poll_photo_task` 和 `poll_motion_task` 成功后应先返回远端 URL
* 不要自动下载结果文件
* 只有当用户明确表达“下载到本地”“保存到 outputs”“帮我落盘”时，才执行 `download_result`

## Output Convention

默认本地输出目录：

* `outputs/text-to-digital-person/`

## Additional Resources

更多接口细节见：

* `reference.md`
* `examples.md`

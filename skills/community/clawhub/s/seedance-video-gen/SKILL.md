---
name: seedance-video
description: >
  使用字节跳动 Seedance 生成 AI 视频：文生视频、图生视频（首帧/首尾帧/参考图）、
  异步任务查询。支持 Seedance 2.0（多模态输入、视频续生、视频编辑）等多个模型。
  Use when: (1) 用户说"生成视频"/"做个视频"/"AI视频"/"text to video",
  (2) 用户要求根据图片生成视频/动画/"图生视频"/"image to video",
  (3) 用户提到 Seedance/字节视频生成,
  (4) 用户说"帮我做段视频"/"生成一段动画"。
  NOT for: 从已有视频中抽帧/截图（用 video-frames）、
  视频剪辑/转码/格式转换（用 ffmpeg 直接操作）、实拍视频处理。
version: 1.0.0
category: file-generation
argument-hint: "[text prompt or task ID]"
---

# Seedance Video Generation

使用字节跳动 Seedance 模型通过火山引擎 Ark API 生成 AI 视频。

## Step 0: 前置检查

1. **API Key**：确认 `ARK_API_KEY` 环境变量已设置
   ```bash
   echo $ARK_API_KEY | head -c 8  # 只显示前 8 位确认存在
   ```
   未设置 → 提示用户在 [火山引擎控制台](https://console.volcengine.com/) 获取
2. **Python CLI 工具**：确认 `{baseDir}/seedance.py` 存在
   - 不存在 → 降级用 curl（见 `references/curl-api-reference.md`）

## Step 1: 需求分类

| 用户意图 | 模式 | 跳转 |
|----------|------|------|
| "帮我生成一段视频" / 纯文字描述 | **文生视频** | → Step 2，Mode text |
| "用这张图生成视频" / 给了一张图 | **图生视频（首帧）** | → Step 2，Mode image |
| 给了两张图（开头和结尾） | **首尾帧视频** | → Step 2，Mode first-last |
| "参考这几张图" / 给了多张参考图 | **参考图视频** | → Step 2，Mode ref |
| "查下之前那个视频任务" / 给了 task ID | **任务查询** | → Step 4 |

## Step 2: 确认参数

**必须在调 API 前跟用户确认以下内容：**

1. **Prompt**：向用户展示将使用的 prompt，确认后再提交
2. **模型选择**（根据场景推荐）：

| 场景 | 推荐模型 | 理由 |
|------|---------|------|
| 日常文/图生视频 | Seedance 1.5 Pro（默认） | 稳定，支持音频 |
| 需要最高质量 | Seedance 2.0 | 多模态，最强效果 |
| 快速预览/测试 | Seedance 2.0 Fast | 生成快，质量略低 |
| 预算有限 | 1.5 Pro + Draft mode | 先低成本预览 |
| 纯文生视频、低成本 | 1.0 Lite T2V | 最便宜 |
| 多参考图 | 1.0 Lite I2V | 支持 1-4 张参考图 |

3. **默认参数**（用户不指定则用默认值）：
   - 分辨率：720p | 比例：16:9（文生）/ adaptive（图生）| 时长：5秒 | 音频：开

## Step 3: 执行生成

所有模式统一用 Python CLI：

```bash
# 文生视频
python3 {baseDir}/seedance.py create \
  --prompt "描述文字" \
  --ratio 16:9 --duration 5 --resolution 720p \
  --wait --download ~/Desktop

# 图生视频（首帧）
python3 {baseDir}/seedance.py create \
  --prompt "动作描述" --image /path/to/photo.jpg \
  --wait --download ~/Desktop

# 首尾帧
python3 {baseDir}/seedance.py create \
  --prompt "过渡描述" --image first.jpg --last-frame last.jpg \
  --wait --download ~/Desktop

# 参考图（1-4张，Lite I2V）
python3 {baseDir}/seedance.py create \
  --prompt "[图1]的人物在跳舞" --ref-images ref1.jpg ref2.jpg \
  --model doubao-seedance-1-0-lite-i2v-250428 \
  --wait --download ~/Desktop

# Draft 模式（便宜预览）
python3 {baseDir}/seedance.py create \
  --prompt "描述" --draft true --wait --download ~/Desktop

# 从 Draft 生成正式版
python3 {baseDir}/seedance.py create \
  --draft-task-id <DRAFT_TASK_ID> --resolution 720p \
  --wait --download ~/Desktop
```

**`--wait --download` 会自动轮询等待 + 下载，无需手动轮询。**

### 超时保护
- `--wait` 默认超时 10 分钟
- 超时后展示 task ID 给用户，可后续用 `status` 查询
- 正常生成时间：文生 1-3 分钟，图生 2-5 分钟

## Step 4: 任务管理

```bash
# 查询状态
python3 {baseDir}/seedance.py status <TASK_ID>

# 等待并下载已有任务
python3 {baseDir}/seedance.py wait <TASK_ID> --download ~/Desktop

# 列出任务
python3 {baseDir}/seedance.py list --status succeeded

# 取消/删除
python3 {baseDir}/seedance.py delete <TASK_ID>
```

## Step 5: 验证与交付

1. 确认视频文件已下载：`ls -lh ~/Desktop/seedance_video_*.mp4`
2. 用 `MEDIA:<path>` 发送视频给用户
3. **展示 task ID**：方便用户后续查询或重新下载
4. 询问是否满意，不满意 → 调整 prompt 重新生成

## 边界条件

| 情况 | 处理 |
|------|------|
| ARK_API_KEY 未设置 | 停止，引导用户获取 |
| 图片格式不支持 | 支持 jpeg/png/webp/bmp/tiff/gif（1.5 Pro 额外支持 heic） |
| 图片尺寸不合规 | 宽高比 0.4-2.5，单边 300-6000px，≤30MB |
| 生成失败（API 错误） | 展示错误信息 + 建议：prompt 含违规词→修改；配额不足→换模型或稍后重试 |
| 视频 URL 过期 | 24 小时过期！生成后立即下载。过期 → 用 task ID 查询是否还能重新获取 |
| 任务历史过期 | 7 天后无法查询 |
| seedance.py 不存在 | 降级用 curl，见 `references/curl-api-reference.md` |
| 网络超时 | 重试 1 次，仍失败 → 建议用 flex tier（离线队列，便宜 50%） |

## 参数速查

| 参数 | 默认值 | 可选值 |
|------|--------|--------|
| ratio | 16:9 / adaptive | 16:9, 4:3, 1:1, 3:4, 9:16, 21:9, adaptive |
| duration | 5 | 4-12 秒（1.5 Pro），2-12（其他）|
| resolution | 720p | 480p, 720p, 1080p |
| generate_audio | true | true/false（仅 1.5 Pro） |
| draft | false | true/false（仅 1.5 Pro） |
| service_tier | default | default（在线）, flex（离线，半价） |

## 模型 ID 速查

| 模型 | ID |
|------|-----|
| Seedance 2.0 | `doubao-seedance-2-0-260128` |
| Seedance 2.0 Fast | `doubao-seedance-2-0-fast-260128` |
| Seedance 1.5 Pro | `doubao-seedance-1-5-pro-251215` |
| Seedance 1.0 Pro | `doubao-seedance-1-0-pro-250528` |
| Seedance 1.0 Pro Fast | `doubao-seedance-1-0-pro-fast-251015` |
| Seedance 1.0 Lite T2V | `doubao-seedance-1-0-lite-t2v-250428` |
| Seedance 1.0 Lite I2V | `doubao-seedance-1-0-lite-i2v-250428` |

# 视频生成指南

## 支持的模型

- **sora-2** - 标准 SORA2 视频生成模型（支持 10s、15s）
- **sora-2-pro** - Pro 版本（支持 10s、15s、25s）

## 视频参数

### 时长选项
- `10` - 10 秒视频（所有模型支持）
- `15` - 15 秒视频（所有模型支持）
- `25` - 25 秒视频（仅 sora-2-pro 支持）

### 比例选项
- `16:9` - 横屏比例（推荐）
- `9:16` - 竖屏比例（适合手机）

### 其他选项
- `--hd` - 启用高清模式
- `--watermark` - 添加水印
- `--private` - 私有视频模式

## 使用流程

### 文生视频

1. **选择模型** - 根据需求选择 sora-2 或 sora-2-pro
2. **输入提示词** - 详细描述您想要的视频内容
3. **设置参数** - 选择时长、比例等
4. **生成视频** - 等待 AI 处理完成（通常需要几分钟）

### 图生视频

1. **上传参考图片** - 选择一张参考图片
2. **输入提示词** - 描述视频的动作和效果
3. **设置参数** - 选择时长、比例等
4. **生成视频** - 等待 AI 处理完成

### 角色客串功能

1. **创建角色** - 先使用 create-character 任务创建角色
2. **生成视频** - 在生成视频时使用 `--character-url` 参数
3. **设置时间范围** - 使用 `--character-timestamps` 指定角色出现的时间段

## 提示词技巧

### 描述动作
- 明确描述主体要执行的动作
- 例如："一只猫从左边走到右边"

### 描述场景
- 详细描述背景环境
- 例如："在阳光明媚的公园里"

### 描述镜头
- 可以描述镜头运动
- 例如："缓慢推进"、"从远到近"

### 描述风格
- 指定视频风格
- 例如："电影质感"、"动画风格"

## 示例

### 文生视频示例

```bash
python3 {baseDir}/scripts/wangyi-banana.py \
  --task text-to-video \
  --prompt "一只可爱的橘猫在窗台上慢慢走动，阳光透过窗户洒在它身上，写实风格，电影质感" \
  --model sora-2 \
  --duration 10 \
  --aspect-ratio 16:9 \
  --hd \
  -o /tmp/openclaw/wangyi-output/cat_video.mp4
```

### 图生视频示例

```bash
python3 {baseDir}/scripts/wangyi-banana.py \
  --task image-to-video \
  --prompt "图片中的猫开始慢慢走动，镜头缓慢推进" \
  --image /path/to/image.png \
  --model sora-2-pro \
  --duration 15 \
  --aspect-ratio 16:9 \
  -o /tmp/openclaw/wangyi-output/video.mp4
```

### 带角色客串的视频

```bash
# 先创建角色
python3 {baseDir}/scripts/wangyi-banana.py \
  --task create-character \
  --url "https://example.com/character_video.mp4" \
  --timestamps "1,3"

# 然后生成带角色的视频
python3 {baseDir}/scripts/wangyi-banana.py \
  --task text-to-video \
  --prompt "一个场景，角色在1-3秒出现" \
  --model sora-2 \
  --character-url "character_url_from_previous_step" \
  --character-timestamps "1,3" \
  -o /tmp/openclaw/wangyi-output/video_with_character.mp4
```

## 注意事项

- 视频生成通常需要 3-10 分钟
- 25 秒视频仅支持 sora-2-pro 模型
- 视频生成过程中会显示进度
- 建议使用高清模式获得更好效果
- 角色客串功能需要先创建角色

## 任务状态

视频生成是异步任务，会经历以下状态：
- `SUBMITTED` - 已提交
- `QUEUED` - 排队中
- `IN_PROGRESS` - 处理中
- `SUCCESS` - 完成
- `FAILURE` - 失败

脚本会自动轮询任务状态直到完成。

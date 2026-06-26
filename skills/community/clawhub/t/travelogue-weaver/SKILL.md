---
name: travelogue-weaver
version: 1.0.0
description: 智能旅行游记生成器，支持多媒体素材记录、自动时间线整理、文学性叙事生成与多格式导出；当用户需要开始一段旅行记录、结束当前旅行、记录旅途点滴、补充旅行素材、预览游记内容、生成完整游记或导出游记文件时自动触发使用
triggers:
  - 开始旅行
  - 结束旅行
  - 记录旅行
  - 生成游记
  - 导出游记
dependency:
  python:
    - Pillow==10.2.0
    - markdown==3.5.2
    - jinja2==3.1.3
    - weasyprint==60.2
---

# Travelogue Weaver（旅行游记编织者）

## 任务目标
- 本 Skill 用于：帮助旅行用户在游玩过程中轻松记录所见所闻，并自动生成完整旅行游记
- 能力包含：旅行生命周期管理、多媒体素材记录、智能时间线整理、文学性叙事生成、多格式导出
- 触发条件：用户表达"开始旅行"、"记录旅途"、"生成游记"、"结束旅行"等意图

## 平台能力依赖

本 Skill 依赖 OpenClaw 平台提供的以下能力：

| 能力 | 用途 | 使用场景 |
|------|------|----------|
| 时间解析服务 | 从文本中提取日期时间 | 用户说"昨天下午"、"3号出发"等 |
| 地理位置解析 | 从文本中提取地名并转换为坐标 | 用户说"在洱海边"、"大理古城"等 |
| 多模态描述 | 对图片/视频生成文本描述 | 用户上传图片或视频时自动生成描述 |
| 语音转写 | 将语音消息转为文字 | 用户发送语音记录素材时 |
| 文件存储 | 存储用户上传的文件 | 保存图片、视频、音频文件 |

## 核心规则（重要）

### 旅行档案生命周期

**严格遵循以下规则**：

1. **开始旅行** → 创建游记档案
   - 用户说："开始北京旅游"、"开始记录云南之旅"等
   - 系统创建新的旅行记录，状态为 `ongoing`
   - 此时刻为游记档案的起点

2. **结束旅行** → 封存档案，停止记录
   - 用户说："结束北京旅行"、"旅行结束了"、"回家了"等
   - 系统将旅行状态改为 `ended`
   - 此时刻为游记档案的终点，**不再接受新素材**

3. **素材记录** → 仅在旅行进行中
   - 只有状态为 `ongoing` 的旅行才能添加素材
   - 用户发送的任何内容（文字、图片、语音、视频）都会被记录到当前进行中的旅行

4. **补充记录** → 需要用户明确指定
   - 对于已结束的旅行，**默认不接受新素材**
   - 只有当用户明确说："补充到XX旅行中"、"往XX旅行里加一条"时，才允许添加
   - 添加时需指定具体的旅行名称或ID

### 意图识别优先级

```
1. 开始旅行 → 创建新档案
2. 结束旅行 → 封存当前档案
3. 补充记录 → 添加到指定档案（需明确意图）
4. 普通消息 → 记录到当前进行中的旅行（如有）
```

## 前置准备
- 依赖说明：scripts 脚本所需的依赖包及版本
  ```
  Pillow==10.2.0
  markdown==3.5.2
  jinja2==3.1.3
  weasyprint==60.2
  ```
- 数据存储初始化：Skill 使用本地文件存储旅行记录和素材
  ```bash
  mkdir -p travelogue_data/uploads
  ```

## 操作步骤

### 1. 开始旅程（创建游记档案）

**触发条件**：用户表达开始旅行的意图
- 示例："开始北京旅游"、"开始记录云南之旅"、"我要开始旅行了"
- 关键词：开始、记录、旅游、旅行、出发

**执行流程**：
1. 检查是否已有进行中的旅行
   - 如果有，询问用户："你已有进行中的旅行【XX】，是否要先结束它？"
   - 用户确认后才能创建新旅行
2. 调用 `scripts/trip_manager.py --action create` 创建新的旅行记录
3. 提取旅行名称、起始地点等信息
4. 返回确认消息，告知用户档案已创建

**参数提取**：
- `trip_name`: 旅行名称（必需，从用户消息中提取）
- `start_location`: 起始地点（可选）
- `start_event`: 开始事件描述（可选）

**执行示例**：
```bash
python scripts/trip_manager.py --action create \
  --name "北京旅游" \
  --start-location "北京"
```

**智能体响应示例**：
```
用户："开始北京旅游"
智能体："好的，已创建【北京旅游】的游记档案，开始时间为 2026-04-03 08:30。现在你可以随时发送文字、图片或语音来记录旅途点滴。"
```

### 2. 记录素材（仅在旅行进行中）

**前提条件**：必须有状态为 `ongoing` 的旅行

**重要规则**：
- 如果当前没有进行中的旅行，提示用户："你当前没有进行中的旅行。请先说'开始XX旅行'来创建游记档案。"
- 如果用户发送素材但旅行已结束，提示用户："【XX旅行】已结束。如需补充记录，请明确说'补充到XX旅行中'。"

#### 2.1 文字素材
- 用户发送纯文本消息
- 智能体自动提取时间和地点信息
- 调用 `scripts/moment_manager.py --action add` 添加素材

**执行示例**：
```bash
python scripts/moment_manager.py --action add \
  --trip-id <trip_id> \
  --type text \
  --content "风真大，但洱海蓝得不像话" \
  --location "洱海" \
  --timestamp "2026-04-03 15:30:00"
```

#### 2.2 图片素材

**⚠️ 重要：图片必须先保存到本地文件！**

**执行流程**：
1. 用户上传图片文件
2. **智能体将图片保存到临时路径**：`./travelogue_data/uploads/image_temp.jpg`
3. 智能体使用多模态能力生成图片描述
4. 提取 EXIF 元数据（如果有）
5. 调用脚本添加素材，**必须传入 `--raw-path` 参数**

**完整执行示例**：
```bash
# 步骤1：智能体先保存图片（用户上传后）
# 保存路径：./travelogue_data/uploads/image_temp.jpg

# 步骤2：调用脚本添加素材
python scripts/moment_manager.py --action add \
  --trip-id <trip_id> \
  --type image \
  --content "洱海的蓝天白云，远处的苍山若隐若现" \
  --raw-path "./travelogue_data/uploads/image_temp.jpg" \
  --location "洱海" \
  --timestamp "2026-04-03 15:30:00"

# 脚本会自动：
# 1. 验证文件存在
# 2. 复制到标准路径：travelogue_data/uploads/{momentId}.jpg
# 3. 记录 rawUrl 字段
```

**注意事项**：
- 图片文件必须在调用脚本之前保存
- 脚本会将图片复制到 `travelogue_data/uploads/{momentId}.{ext}`
- 游记中图片路径：`./uploads/{momentId}.jpg`（相对路径）
- 支持格式：JPG、PNG、WebP
- 建议大小：单张 ≤ 10MB

#### 2.3 语音素材

**⚠️ 重要：音频文件必须先保存到本地！**

**执行流程**：
1. 用户上传或发送语音
2. **智能体将音频保存到临时路径**：`./travelogue_data/uploads/audio_temp.mp3`
3. 平台提供语音转写服务
4. 调用脚本添加素材，**必须传入 `--raw-path` 参数**

**执行示例**：
```bash
python scripts/moment_manager.py --action add \
  --trip-id <trip_id> \
  --type audio \
  --content "刚刚在古城吃到了烤乳扇，酸酸甜甜" \
  --raw-path "./travelogue_data/uploads/audio_temp.mp3" \
  --location "大理古城" \
  --timestamp "2026-04-03 16:45:00"
```

**注意事项**：
- 支持格式：MP3、M4A、WAV
- 音频文件保留在 `uploads/` 目录

#### 2.4 视频素材

**⚠️ 重要：视频文件必须先保存到本地！**

**执行流程**：
1. 用户上传视频
2. **智能体将视频保存到临时路径**：`./travelogue_data/uploads/video_temp.mp4`
3. 智能体提取关键帧并生成描述
4. 调用脚本添加素材，**必须传入 `--raw-path` 参数**

**执行示例**：
```bash
python scripts/moment_manager.py --action add \
  --trip-id <trip_id> \
  --type video \
  --content "客栈阳台的风景，远处是苍山，夕阳西下" \
  --raw-path "./travelogue_data/uploads/video_temp.mp4" \
  --location "双廊客栈" \
  --timestamp "2026-04-03 18:00:00"
```

**注意事项**：
- 支持格式：MP4、MOV、AVI
- 建议时长：≤ 3分钟
- 建议大小：≤ 50MB


python scripts/moment_manager.py --action add \
  --trip-id <trip_id> \
  --type text \
  --content "风真大，但洱海蓝得不像话" \
  --location "洱海" \
  --timestamp "2026-04-03 15:30:00"
```

### 3. 结束旅程（封存游记档案）

**触发条件**：用户表达结束旅行的意图
- 示例："结束北京旅行"、"旅行结束了"、"回家了"、"行程结束了"
- 关键词：结束、回家、行程结束、旅行结束

**执行流程**：
1. 检查是否有进行中的旅行
   - 如果没有，提示用户："你当前没有进行中的旅行。"
2. 调用 `scripts/trip_manager.py --action end` 结束旅行
3. 提取结束地点、结束感言等信息
4. 更新旅行状态为 `ended`
5. **重要**：此后该旅行不再接受新素材

**参数提取**：
- `end_location`: 结束地点
- `end_event`: 结束感言

**执行示例**：
```bash
python scripts/trip_manager.py --action end \
  --end-location "北京" \
  --end-event "三天两夜，不虚此行"
```

**智能体响应示例**：
```
用户："结束北京旅行"
智能体："【北京旅游】已结束，档案封存于 2026-04-05 18:30。共记录了 12 条素材。需要我现在生成游记吗？或者你可以说'导出为PDF/HTML/Markdown'。"
```

### 4. 补充记录（明确指定）

**触发条件**：用户明确要求向已结束的旅行添加素材
- 示例："补充到北京旅行里"、"往云南之旅加一条"、"刚才忘记记录了，补充到XX旅行"
- 关键词：补充、添加到、往...加

**执行流程**：
1. 识别目标旅行（通过名称或ID）
2. 检查目标旅行是否存在
3. 调用脚本添加素材到指定旅行
4. **重要**：即使旅行已结束，也允许添加

**参数提取**：
- `trip_name`: 目标旅行名称（从用户消息中识别）
- 其他素材参数同普通添加流程

**执行示例**：
```bash
# 先根据名称查询 trip_id
python scripts/trip_manager.py --action list --status-filter ended

# 然后添加素材
python scripts/moment_manager.py --action add \
  --trip-id <trip_id> \
  --type text \
  --content "补充：刚才在天坛拍的照片忘记发了" \
  --location "天坛"
```

**智能体响应示例**：
```
用户："补充到北京旅行：刚才在天坛拍的照片忘记发了"
智能体："已补充到【北京旅游】游记中。"
```

### 5. 查询旅行状态

**触发条件**：用户询问旅行记录情况
- 示例："我的旅行记录怎么样了"、"现在记录了多少条"

**执行示例**：
```bash
python scripts/trip_manager.py --action status
```

**智能体响应示例**：
```
用户："我的旅行记录怎么样了"
智能体："你当前正在进行【北京旅游】，已记录 12 条素材（8 段文字、3 张图片、1 段语音）。旅行始于 2026-04-03，已持续 2 天。"
```

### 6. 生成游记

旅行结束后，可生成完整游记：

**执行流程**：
1. 调用 `scripts/moment_manager.py --action list` 获取所有素材
2. 智能体根据素材按时间线整理内容
3. 根据用户选择的风格（文艺/幽默/简洁/详细）生成叙事
4. 生成游记标题、章节结构、每日高光时刻等

详细流程参考：[references/narrative_guide.md](references/narrative_guide.md)

### 7. 导出游记

根据用户需求导出为不同格式：

```bash
# 导出 Markdown
python scripts/export_generator.py --trip-id <trip_id> \
  --format markdown \
  --output ./travelogue.md

# 导出 HTML
python scripts/export_generator.py --trip-id <trip_id> \
  --format html \
  --output ./travelogue.html

# 导出 PDF
python scripts/export_generator.py --trip-id <trip_id> \
  --format pdf \
  --output ./travelogue.pdf
```

## 资源索引
- 旅行管理脚本：[scripts/trip_manager.py](scripts/trip_manager.py)（用途：创建/结束/查询旅行记录）
- 素材管理脚本：[scripts/moment_manager.py](scripts/moment_manager.py)（用途：添加/查询/删除素材）
- 导出生成脚本：[scripts/export_generator.py](scripts/export_generator.py)（用途：生成 Markdown/HTML/PDF 文件）
- 数据模型参考：[references/data_model.md](references/data_model.md)（何时读取：理解数据结构时）
- 叙事风格指南：[references/narrative_guide.md](references/narrative_guide.md)（何时读取：生成游记时）
- 导出格式规范：[references/export_format.md](references/export_format.md)（何时读取：导出文件时）
- HTML 模板：[assets/templates/travelogue.html](assets/templates/travelogue.html)（直接用于生成 HTML 文件）

## 注意事项

### 旅行档案管理
- **严格的生命周期**：开始 → 进行中 → 结束 → 封存
- **自动拒绝**：已结束的旅行默认不接受新素材
- **明确意图**：补充记录需要用户明确指定目标旅行
- **单一进行中**：同一时间只能有一个进行中的旅行

### 智能体职责
- 准确识别用户意图（开始/结束/补充/普通记录）
- 在用户发送素材时，检查旅行状态
- 对不符合规则的操作给出清晰提示

### 数据安全
- 旅行记录和素材存储在本地文件中
- 所有素材自动关联到对应旅行，按时间戳排序
- 游记风格可随时调整，重新生成即可

## 使用示例

### 示例 1：标准流程
```
用户："开始北京旅游"
智能体："好的，已创建【北京旅游】的游记档案，开始时间为 2026-04-03 08:30。现在你可以随时发送文字、图片或语音来记录旅途点滴。"

用户：[上传照片] "故宫真的太大了"
智能体："收到！故宫的照片已保存到【北京旅游】游记中。"

用户："晚上吃了烤鸭，味道不错"
智能体："记下了，听起来很美味。"

用户："结束北京旅行"
智能体："【北京旅游】已结束，档案封存于 2026-04-03 20:30。共记录了 5 条素材。需要我现在生成游记吗？"

用户："生成游记"
智能体：[生成游记预览] "游记已生成，需要导出吗？"
```

### 示例 2：错误处理
```
用户：[直接发送照片] "这是颐和园"
智能体："你当前没有进行中的旅行。请先说'开始XX旅行'来创建游记档案。"

用户："开始北京旅游"
智能体："好的，已创建【北京旅游】的游记档案..."

用户：[发送素材] ...

用户："结束北京旅行"
智能体："【北京旅游】已结束，档案封存。"

用户：[发送照片] "这是长城"
智能体："【北京旅游】已结束。如需补充记录，请明确说'补充到北京旅游：这是长城'。"

用户："补充到北京旅游：这是长城"
智能体："已补充到【北京旅游】游记中。"
```

### 示例 3：多旅行管理
```
用户："开始云南之旅"
智能体："好的，已创建【云南之旅】的游记档案..."

用户：[记录素材] ...

用户："结束云南之旅"
智能体："【云南之旅】已结束，档案封存。"

用户："开始西藏旅游"
智能体："好的，已创建【西藏旅游】的游记档案..."

用户：[记录素材] ...

用户："我的旅行记录怎么样了"
智能体："你当前正在进行【西藏旅游】，已记录 8 条素材。你还有 1 个已结束的旅行：【云南之旅】。"
```

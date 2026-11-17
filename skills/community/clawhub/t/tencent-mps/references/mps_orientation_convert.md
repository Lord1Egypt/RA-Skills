# mps_orientation_convert.py — 智能横竖屏方向转换

**功能**：视频画面方向的**双向**转换 —— 横屏→竖屏（算法 2/3/5/6）与竖屏→横屏（算法 7）。
转换不是简单旋转：基础版通过识别感兴趣区域（ROI，Region of Interest）智能裁剪成目标比例；AIGC 版则基于原视频做 AI 补全生成缺失画面。

**底层 API**：`ProcessMedia` — `AiAnalysisTask.Definition=28`（官方称"预设智能横转竖模板"，实际同时承载竖转横能力），通过 `ExtendedParameter` 的 `htv` 键指定算法与配置。

> 📌 `htv` 与模板名中的"横转竖"是**官方历史命名**，沿用即可；该模板通过 `AlgorithmType=7` 同样支持竖转横。

**官方文档**：[智能横转竖和竖转横接入](https://cloud.tencent.com/document/product/862/112112)

---

## ⚠️ 强制规则

1. **`--algorithm-type` 必填**，未提供时必须先询问用户希望使用哪种算法，不得擅自选默认值。**先确认转换方向**（横→竖还是竖→横），再据此选择算法。
2. **仅支持离线文件，不支持直播流**。
3. **输入仅支持 URL 与腾讯云 COS，不支持 AWS S3**（官方限制）。
4. **`Definition` 固定为 28**，不支持自定义模板。若需为自定义智能分析模板开启该能力，需联系腾讯云。
5. `ExtendedParameter` 字段严格来自官方文档，**禁止自行增删字段**；其值必须是序列化后的 JSON 字符串。
6. 本任务**不能**用 `mps_get_video_task.py` 之外的方式查询；结果在 `AiAnalysisResultSet` → `HorizontalToVerticalTask` → `Output`。

---

## 算法类别（`--algorithm-type`，必填）

### 横屏 → 竖屏

| 取值 | 说明 | 计费版本 |
|------|------|----------|
| `2` | 支持多种模型的算法和定制优化（横转竖推荐默认） | 智能横转竖-基础版 |
| `3` | 精确人脸检测算法；两个人脸出现时上下分割显示，尽可能人脸居中 | 智能横转竖-基础版 |
| `5` | 直接缩放视频居中放竖屏，使用毛玻璃模糊图作背景 | 智能横转竖-基础版 |
| `6` | AIGC 模式，基于原有横屏视频补全到 9:16 竖屏 | 智能横转竖-**高级版** |

### 竖屏 → 横屏

| 取值 | 说明 | 计费版本 |
|------|------|----------|
| `7` | AIGC 模式，基于原有竖屏视频补全到 16:9 横屏 | 智能横转竖-**高级版** |

> ⚠️ **使用算法 7 时应显式指定 `--ratio 16:9`**。`--ratio` 默认值是 `9:16`（竖屏），与竖转横意图矛盾；脚本会在此情况下打印提醒。
>
> 💰 算法 `6`/`7` 为 AIGC 高级版，计费高于基础版。计费项名称官方统称"智能横转竖"（含竖转横）。定价见 [MPS 计费说明](https://cloud.tencent.com/document/product/862/36180)。

---

## 参数

### 输入源（三选一）

| 参数 | 说明 |
|------|------|
| `--url` | 视频 URL 地址 |
| `--cos-input-key` | 输入 COS 对象 Key（如 `/input/video.mp4`），配合 `--cos-input-bucket` / `--cos-input-region` 或环境变量 |
| `--local-file` | 本地文件，自动上传到 COS 后处理；与 COS 输入参数互斥 |

### 算法配置

| 参数 | 默认 | 说明 |
|------|------|------|
| `--algorithm-type` | **必填** | 算法类别，取值 `2`/`3`/`5`/`6`/`7` |
| `--ratio` | `9:16` | 目标画面横竖比，形如 `9:16`（竖）/ `16:9`（横）/ `3:4`。**竖转横（算法 7）须显式指定 `16:9`**；解析失败时服务端回退 `9:16` |
| `--smooth-weight` | `0.75` | 平滑速度，**0-1 之间的浮点数**，数值越小镜头移动越快 |
| `--blur-weight` | — | 模糊参数，数值越大模糊越重。**仅算法 5 生效**；过大会影响处理速度 |
| `--output-pattern` | `htv-{sessionId}` | 输出文件名模式，可用替换参数 `{sessionId}` / `{timestamp}` |

### 人脸检测配置（仅 `--algorithm-type 3` 生效）

| 参数 | 可选值 | 说明 |
|------|--------|------|
| `--face-score-thd` | 整数 | 人脸检测识别阈值，仅评分超过该阈值才视为有效人脸 |
| `--face-accuracy` | `Balance`（默认）/ `Efficiency` / `Precision` | 人脸检测算法执行次数 |
| `--no-face-detect` | `Scale` / `ScaleWithoutBlur`（默认） | 无人脸时的兜底策略 |
| `--double-face` | `Scale` / `ScaleWithoutBlur` / `SplitScreenVertical`（默认） | 双人脸时的兜底策略 |

兜底策略含义：

- `Scale`：缩放居中该帧，背景使用毛玻璃效果处理后的图片替换
- `ScaleWithoutBlur`：缩放居中该帧，背景使用纯黑替换
- `SplitScreenVertical`：上下分屏，两个人脸分别居中放在上下两个区域

### 输出与其他

| 参数 | 默认 | 说明 |
|------|------|------|
| `--output-bucket` / `--output-region` | 环境变量 | 输出 COS 桶与区域。**URL 输入时必填**（官方约定） |
| `--output-dir` | `/output/orientation/` | 输出目录，须以 `/` 开头和结尾 |
| `--session-id` | — | 去重识别码，最长 50 字符；三天内相同识别码的请求会报错 |
| `--notify-url` | — | 任务完成回调 URL |
| `--region` | 环境变量 `TENCENTCLOUD_API_REGION` | MPS 服务区域（如 `ap-guangzhou`） |
| `--no-wait` | — | 仅提交任务，不等待结果 |
| `--download-dir` | — | 任务完成后自动下载结果到本地目录 |
| `--poll-interval` / `--max-wait` | `10` / `1800` | 轮询间隔与最长等待秒数 |
| `--verbose` / `-v` | — | 输出详细信息（含完整请求与响应） |
| `--dry-run` | — | 仅打印请求参数，不调用 API、不计费 |

---

## 输入输出格式

**输入**：编码标准 MPEG / H.264 / H.265；封装格式 `.mp4` / `.avi` / `.mkv` / `.mov` / `.mpg`。

**输出**：统一 H.264 编码、`.mp4` 格式。输出目录下 **`htv-` 开头**的文件即为处理结果。

---

## 命令示例

```bash
# 横转竖（默认算法 2，比例 9:16，SmoothWeight 0.75）
python3 scripts/mps_orientation_convert.py --cos-input-key /input/landscape.mp4 --algorithm-type 2

# 人脸场景横转竖（双人脸上下分屏）
python3 scripts/mps_orientation_convert.py --url https://example.com/interview.mp4 --algorithm-type 3

# 人脸检测精细配置
python3 scripts/mps_orientation_convert.py --cos-input-key /input/talk.mp4 --algorithm-type 3 \
    --face-score-thd 60 --face-accuracy Precision --double-face SplitScreenVertical

# 缩放 + 毛玻璃背景
python3 scripts/mps_orientation_convert.py --cos-input-key /input/clip.mp4 --algorithm-type 5 --blur-weight 50

# AIGC 横转竖（补全到 9:16，高级版计费）
python3 scripts/mps_orientation_convert.py --url https://example.com/land.mp4 --algorithm-type 6

# AIGC 竖转横（补全到 16:9，高级版计费）
python3 scripts/mps_orientation_convert.py --url https://example.com/port.mp4 --algorithm-type 7 --ratio 16:9

# 自定义比例与平滑速度
python3 scripts/mps_orientation_convert.py --cos-input-key /input/game.mp4 --algorithm-type 2 \
    --ratio 3:4 --smooth-weight 0.5

# 自定义输出文件名
python3 scripts/mps_orientation_convert.py --cos-input-key /input/v.mp4 --algorithm-type 2 \
    --output-pattern "htv-{sessionId}-{timestamp}"

# 本地文件（自动上传 COS）
python3 scripts/mps_orientation_convert.py --local-file /data/landscape.mp4 --algorithm-type 2

# 仅提交不等待 + 完成后下载
python3 scripts/mps_orientation_convert.py --cos-input-key /input/v.mp4 --algorithm-type 2 --no-wait
python3 scripts/mps_orientation_convert.py --cos-input-key /input/v.mp4 --algorithm-type 2 --download-dir ./out

# Dry Run（不计费）
python3 scripts/mps_orientation_convert.py --cos-input-key /input/v.mp4 --algorithm-type 2 --dry-run
```

---

## 请求结构示例

```json
{
  "InputInfo": {
    "Type": "COS",
    "CosInputInfo": {
      "Bucket": "mybucket-125xxx",
      "Region": "ap-guangzhou",
      "Object": "/input/landscape.mp4"
    }
  },
  "OutputStorage": {
    "Type": "COS",
    "CosOutputStorage": { "Bucket": "mybucket-125xxx", "Region": "ap-guangzhou" }
  },
  "OutputDir": "/output/orientation/",
  "AiAnalysisTask": {
    "Definition": 28,
    "ExtendedParameter": "{\"htv\": {\"AlgorithmType\": 2, \"SmoothWeight\": 0.75, \"Ratio\": \"9:16\"}}"
  }
}
```

`ExtendedParameter` 序列化前的结构：

```json
{
  "htv": {
    "AlgorithmType": 2,
    "SmoothWeight": 0.75,
    "Ratio": "9:16",
    "OutputPattern": "htv-{sessionId}",
    "BlurWeight": 50,
    "FaceDetectConfig": {
      "FaceScoreThd": 60,
      "FaceAccuracy": "Balance",
      "FallbackConfig": {
        "NoFaceDetect": "ScaleWithoutBlur",
        "DoubleFace": "SplitScreenVertical"
      }
    }
  }
}
```

---

## 查询任务结果

脚本默认自动轮询等待完成。手动查询：

```bash
python3 scripts/mps_get_video_task.py --task-id <TaskId>
```

结果字段路径：`WorkflowTask`/`ScheduleTask` → `AiAnalysisResultSet` → `HorizontalToVerticalTask` → `Output`。

相关数据结构：`AiAnalysisTaskHorizontalToVerticalResult` / `AiAnalysisTaskHorizontalToVerticalInput` / `AiAnalysisTaskHorizontalToVerticalOutput`。

---

## 与其他能力的区分

| 需求 | 正确脚本 | 说明 |
|------|----------|------|
| 把**已有视频**横屏转竖屏（算法 2/3/5/6）或竖屏转横屏（算法 7） | **`mps_orientation_convert.py`** | ROI 智能裁剪或 AIGC 补全，输入真实视频，双向均支持 |
| 凭文字描述**生成**竖屏视频（无输入视频） | `mps_aigc_video.py --model Mingmou --scene-type land2port` | AIGC 生成路径，不需要输入视频文件 |
| 给视频**加填充边**以改变指纹（视频去重） | `mps_dedupe.py --mode VerticalExtend` | 去重手段，画面内容不变，非画面比例转换 |

> ⚠️ 三者容易混淆：`mps_orientation_convert.py` 转换已有视频（横↔竖双向）；`mps_aigc_video.py` 的 `land2port` 凭 prompt 生成新视频（仅横转竖方向、且不需输入视频）；`mps_dedupe.py` 的 `VerticalExtend` 只是加填充条做去重、画面内容不变。

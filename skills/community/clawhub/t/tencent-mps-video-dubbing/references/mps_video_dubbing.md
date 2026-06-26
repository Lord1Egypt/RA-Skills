# 视频译制参数与示例 — `mps_video_dubbing.py`

**功能**：腾讯云 MPS 一站式视频译制 — 单次任务端到端完成「擦除原字幕 / ASR → 翻译 → 压制目标语言字幕 → AI 克隆原声配音」。底层调用 `ProcessMedia` 接口的 `AiAnalysisTask`（Definition=25），通过 `ExtendedParameter` 传扩展参数。

> 输入 → 去字幕(OCR) / ASR → 翻译 → 压新字幕 → AI 克隆配音 → 输出新视频

## 模式说明

| 维度 | `ocr` | `asr` |
|------|-------|-------|
| 适用视频 | 画面有硬字幕 | 画面无硬字幕 |
| 翻译来源 | OCR 提取的画面字幕文本 | 语音识别结果 |
| 自动擦除原画面字幕 | ✅ | ❌ 不擦除 |
| 字幕区域参数 | `--subtitle-area` 必填 | 忽略 |
| `CustomerAppId`（内部字段，脚本自动设置） | `audio_clone_ocr` | `audio_clone_asr` |
| 典型耗时（1080p / 5min） | 15~25 分钟 | 5~10 分钟 |

**OCR 字幕区域两种模式（`--subtitle-area`）**：

| 取值 | 适用场景 | `als_filter` 写入 | 必带参数 |
|------|---------|------------------|---------|
| `preset`（推荐） | 画面中部靠下的常规硬字幕（覆盖 90% 视频） | ❌ 不写（后端按默认区域） | — |
| `custom` | 顶部 / 竖屏 / 双语对照等非常规位置 | ✅ 写矩形像素坐标 | `--subtitle-bbox LTX,LTY,RBX,RBY` |

## 参数说明

| 参数 | 说明 |
|------|------|
| `-i, --input-url` | 视频公网 URL（支持 `https://` 或 `cos://bucket/key`，后者自动识别为 `CosInputInfo`） |
| `--local-file` | 本地文件路径，自动上传到 COS 后处理（与 `-i` / `--cos-input-key` 互斥） |
| `--cos-input-key` | COS 输入对象 key（如 `input/video.mp4`） |
| `--cos-input-bucket` | COS 输入桶（仅 `--cos-input-key` 路径下生效，未传则沿用 `--cos-bucket`） |
| `--cos-input-region` | COS 输入地域（仅 `--cos-input-key` 路径下生效，未传则沿用 `--cos-region`） |
| `--mode` | **【必填】** 译制模式：`ocr`（画面有硬字幕）/ `asr`（无硬字幕） |
| `--src-lang` | **【必填】** 源语言 code（31 种，见下方「支持语种」表或 `--list-languages`） |
| `--dst-lang` | **【必填】** 目标语言 code，**不得与 src 相同** |
| `--burn-subtitle` / `--no-burn-subtitle` | **【必填，二选一】** 是否压制翻译后字幕到画面 |
| `--subtitle-area` | **【OCR 必填】** 字幕区域模式：`preset` / `custom` |
| `--subtitle-bbox` | 自定义矩形 4 点整数像素坐标，格式 `LTX,LTY,RBX,RBY`（如 `53,741,953,922`），仅 `--subtitle-area=custom` 时必填 |
| `--cos-bucket` | **【必填】** 输出 COS 桶（未传则从 `TENCENTCLOUD_COS_BUCKET` 读取，未设置则报错） |
| `--cos-region` | **【必填】** 输出 COS 地域（未传则从 `TENCENTCLOUD_COS_REGION` 读取，未设置则报错） |
| `--output-dir` | COS 输出目录，默认 `/output/video-dubbing/` |
| `--no-wait` | 仅提交不等待（默认自动轮询） |
| `--poll-interval` | 轮询间隔（秒），默认 `15` |
| `--max-wait` | 最长等待（秒），默认 `3600` |
| `--download-dir` | 任务完成后下载成品到本地目录 |
| `--session-id` | 任务去重识别码（同一 ID 在 3 天内重复提交会报错；适用于幂等重试场景）|
| `--region` | **【必填】** MPS API 区域（未传则从 `TENCENTCLOUD_API_REGION` 读取，未设置则报错） |
| `--interactive` | 强制进入交互向导 |
| `--confirm-charges` | **CLI 模式必需**：确认产生费用；漏传则脚本自动降级 dry-run 不实际提交 |
| `--dry-run` | 不调用 API；打印「配置摘要」+「完整 ProcessMedia 请求 JSON」 |
| `--query-task <TaskId>` | 单次查询已提交任务（输出原始 JSON，不计费、不轮询） |
| `--list-languages` | 列出 31 种支持语种（完整对照表 + 地区分组） |
| `--verbose, -v` | 详细输出（影响环境加载日志和轮询过程日志的详细度） |

## 支持语种（31 种，官方文档声明双向支持翻译）

> 与脚本内的 `SUPPORTED_LANGUAGES` 字典**同源**。运行 `python scripts/mps_video_dubbing.py --list-languages` 可在终端实时查看完整对照表 + 地区分组。

| # | 语种 | Code | | # | 语种 | Code | | # | 语种 | Code |
|:-:|---|:-:|---|:-:|---|:-:|---|:-:|---|:-:|
| 1  | 中文           | `zh`  | | 12 | 印度尼西亚语 | `id`  | | 23 | 印地语       | `hi`  |
| 2  | 英语           | `en`  | | 13 | 荷兰语       | `nl`  | | 24 | 保加利亚语   | `bg`  |
| 3  | 日语           | `ja`  | | 14 | 土耳其语     | `tr`  | | 25 | 罗马尼亚语   | `ro`  |
| 4  | 韩语           | `ko`  | | 15 | 菲律宾语     | `fil` | | 26 | 阿拉伯语     | `ar`  |
| 5  | 德语           | `de`  | | 16 | 马来语       | `ms`  | | 27 | 捷克语       | `cs`  |
| 6  | 法语           | `fr`  | | 17 | 希腊语       | `el`  | | 28 | 丹麦语       | `da`  |
| 7  | 俄语           | `ru`  | | 18 | 芬兰语       | `fi`  | | 29 | 泰米尔语     | `ta`  |
| 8  | 乌克兰语       | `uk`  | | 19 | 克罗地亚语   | `hr`  | | 30 | 匈牙利语     | `hun` |
| 9  | 葡萄牙语       | `pt`  | | 20 | 斯洛伐克语   | `sk`  | | 31 | 越南语       | `vi`  |
| 10 | 意大利语       | `it`  | | 21 | 波兰语       | `pl`  | |    |              |       |
| 11 | 西班牙语       | `es`  | | 22 | 瑞典语       | `sv`  | |    |              |       |

> 区分大小写，必须用小写 code。脚本只校验 `src ≠ dst`，不对 30×30 组合矩阵做更细校验；遇到具体语种对返回 60000 类错误时，建议用更高频语种对（如 `zh ↔ en`）交叉验证。

## 强制规则

- **核心业务参数无默认值，必须显式传**：`--mode` / `--src-lang` / `--dst-lang` / `--burn-subtitle`(or `--no-burn-subtitle`) / `--subtitle-area`（仅 OCR）。CLI 缺任一项 → exit=2 + 列出全部缺失项；交互向导前 5 步必填，OCR 模式还要走必填的第 6 步（字幕区域 preset/custom 二选一）。
- **`--subtitle-bbox` 校验**：4 个逗号分隔的非负整数，且 `lt_x < rb_x`、`lt_y < rb_y`，违反即 exit=2。
- **`--subtitle-area=custom` 假成功陷阱** ⚠️：自定义 bbox 没圈中真实字幕时，后端**仍返回 SUCCESS** 但产物 = 源视频。规避：优先 `preset`；必须 `custom` 时先用 VLC 暂停截图精确量取坐标，提交后抽查首段产物确认字幕已正确处理。
- **OCR 后端隐式降级到 ASR**：`--mode ocr` 但视频实际无硬字幕时，后端可能跳过擦除算子走 ASR 路径，耗时大幅缩短，**不影响计费类型**。若确认无硬字幕，建议直接 `--mode asr` 行为更确定。
- **ASR 模式忽略字幕区域参数**：`--mode asr` 时即使传了 `--subtitle-area` / `--subtitle-bbox` 也会被脚本静默忽略并打印警告，`als_filter` 不写入。
- **费用确认强制**：CLI 模式漏传 `--confirm-charges` → 自动降级 dry-run 退出（不真正提交、不计费）；交互向导最后一步必须键入 `YES`。
- **`--cos-input-key` 的 region 兜底链**：`--cos-input-region` → `$TENCENTCLOUD_COS_REGION` → `--cos-region`（即输出地域）。均缺时直接 `sys.exit(1)` 退出。
- **`--input-url cos://...` 的 region 兜底链**：`--cos-input-region` → `$TENCENTCLOUD_COS_REGION`（仅两级，不会从 `--cos-region` 兜底）。均缺时直接 `ValueError` 退出。
- **`--local-file` + 未指定 `--cos-bucket`**：脚本自动以**上传桶**作为输出桶；如需区分输入/输出桶请显式传 `--cos-bucket` / `--cos-region`。
- **后端硬约束**（脚本已固化，违反会被后端拒绝）：`cluster_id` 必须为 `gpu_zhiyan`；`subtitle_param` 必须同时含 `use_draw` 和 `font_type="auto"`；预设区域（`preset`）→ **不写** `als_filter` 键；ASR 模式 → **不写** `als_filter`；配音级译制**不写** `preview_size`（与字幕级译制不同）。

## 输出产物

任务完成后 MPS 在指定 COS 输出目录（默认 `/output/video-dubbing/`）生成**主成品**：译制后完整视频，文件名形如 `delogo-<hash>.mp4`（前缀 `delogo` 来自底层 DeLogoTask 算子）。

## 示例命令

```bash
# 中→英 OCR 模式 + 预设字幕区域 + 压新字幕 + AI 配音（最常见）
python scripts/mps_video_dubbing.py -i https://example.com/cn.mp4 \
    --mode ocr --src-lang zh --dst-lang en --burn-subtitle \
    --subtitle-area preset \
    --confirm-charges

# 中→英 OCR 模式 + 自定义字幕区域（顶部 / 竖屏 / 双语对照等）
python scripts/mps_video_dubbing.py -i https://example.com/cn.mp4 \
    --mode ocr --src-lang zh --dst-lang en --burn-subtitle \
    --subtitle-area custom --subtitle-bbox 53,741,953,922 \
    --confirm-charges

# 本地文件自动上传 + ASR 模式
python scripts/mps_video_dubbing.py --local-file ./video.mp4 \
    --mode asr --src-lang zh --dst-lang en --burn-subtitle \
    --confirm-charges

# 日→中 ASR + 不压字幕（仅替换配音）
python scripts/mps_video_dubbing.py -i https://example.com/ja.mp4 \
    --mode asr --src-lang ja --dst-lang zh --no-burn-subtitle \
    --confirm-charges

# COS 路径输入 + 自动下载成品到本地
python scripts/mps_video_dubbing.py \
    --cos-input-key input/fr_video.mp4 \
    --mode asr --src-lang fr --dst-lang id --burn-subtitle \
    --download-dir ./output/ \
    --confirm-charges

# cos:// URL 输入（自动识别为 CosInputInfo）
python scripts/mps_video_dubbing.py \
    -i cos://<your-bucket>-<appid>/input/video.mp4 \
    --mode ocr --src-lang zh --dst-lang en --burn-subtitle \
    --subtitle-area preset \
    --confirm-charges

# 交互向导（零配置启动，逐步引导填参数）
python scripts/mps_video_dubbing.py

# 查询已提交任务（单次查询，输出原始 JSON，不计费）
python scripts/mps_video_dubbing.py --query-task 2600011633-WorkflowTask-xxxxxx
```

## 参考文档

- [一站式译制接入](https://cloud.tencent.com/document/product/862/124504)
- [ProcessMedia 接口](https://cloud.tencent.com/document/product/862/37578)
- [任务查询 DescribeTaskDetail](https://cloud.tencent.com/document/api/862/37614)
- [MPS 计费说明](https://cloud.tencent.com/document/product/862/36180)

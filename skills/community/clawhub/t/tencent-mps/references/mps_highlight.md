# 精彩集锦参数与示例 — `mps_highlight.py`

**功能**：AI 自动提取视频精彩片段（高光集锦），支持 VLOG、短剧、足球、篮球、自定义等场景。
> **核心机制**：`AiAnalysisTask.Definition=26` + `ExtendedParameter(hht 场景参数)`。
> 脚本**默认同步等待**任务完成，加 `--no-wait` 只提交任务返回 TaskId。
> ⚠️ **仅支持离线文件，不支持直播流**；ExtendedParameter 必须从预设场景中选择，**禁止自行拼装**。

## 预设场景

| 场景值 | 说明 | 计费版本 | 支持 --top-clip |
|--------|------|---------|----------------|
| `vlog` | VLOG、风景、无人机视频 | 大模型版 | ✅ |
| `vlog-panorama` | 全景相机（开启全景优化）| 大模型版 | ✅ |
| `short-drama` | 短剧、影视剧，提取主角出场/BGM高光 | 大模型版 | ❌ |
| `football` | 足球赛事，识别射门/进球/红黄牌/回放 | 高级版 | ❌ |
| `basketball` | 篮球赛事 | 高级版 | ❌ |
| `custom` | 自定义场景，可传 `--prompt` 和 `--scenario` | 大模型版 | ✅ |

## 参数说明

| 参数 | 说明 |
|------|------|
| `--local-file` | 本地文件路径，自动上传到 COS 后处理（与 `--cos-input-*` 互斥）|
| `--url` | 输入视频 URL（HTTP/HTTPS）|
| `--cos-input-bucket` | 输入 COS Bucket 名称（与 `--cos-input-region`/`--cos-input-key` 配合，推荐）|
| `--cos-input-region` | 输入 COS Bucket 区域（如 `ap-guangzhou`）|
| `--cos-input-key` | 输入 COS 对象 Key（如 `/input/video.mp4`，**推荐**）|
| `--scene` | **必填**。预设场景（见上表）|
| `--prompt` | 自定义场景描述（仅 `--scene custom` 生效，非必填）|
| `--scenario` | 自定义场景名称（仅 `--scene custom` 生效，非必填）|
| `--top-clip` | 最多输出集锦片段数（仅 `vlog` / `vlog-panorama` / `custom` 场景可用，默认 5）|
| `--output-bucket` | 输出 COS Bucket |
| `--output-region` | 输出 COS Region |
| `--output-dir` | 输出目录，默认 `/output/highlight/` |
| `--output-object-path` | 输出文件路径模板，如 `/output/{inputName}_highlight.{format}` |
| `--region` | MPS 服务区域（优先读取 `TENCENTCLOUD_API_REGION` 环境变量，默认 `ap-guangzhou`） |
| `--notify-url` | 任务完成回调 URL |
| `--no-wait` | 仅提交任务，不等待结果（返回 TaskId 后退出）|
| `--poll-interval` | 轮询间隔（秒），默认 10 |
| `--max-wait` | 最长等待时间（秒），默认 1800（精彩集锦耗时较长）|
| `--download-dir` | 任务完成后将输出文件下载到指定本地目录（默认仅打印预签名 URL）|
| `--dry-run` | 只打印参数预览，不调用 API |
| `--verbose` / `-v` | 输出详细信息 |

## 强制规则

- `--scene` **必填**，值必须是预设枚举之一：`vlog` | `vlog-panorama` | `short-drama` | `football` | `basketball` | `custom`
  - 用户提到"篮球"/"足球"/"短剧"/"VLOG"等关键词时直接映射到对应 `--scene`，无需二次询问
  - **用户未提及任何类型关键词时，必须先追问**："请问是什么类型的视频？（足球/篮球/短剧/VLOG/其他）"，不得猜测场景直接执行
- `--top-clip` 仅允许在 `vlog` / `vlog-panorama` / `custom` 场景下使用
- `--prompt` 和 `--scenario` 仅在 `--scene custom` 时生效，但二者非必填
- 禁止生成预设表以外的 ExtendedParameter 字段或值
- ⚠️ 本脚本**仅支持处理离线文件，不支持直播流**（直播流需使用 MPS API 直接调用）

## 示例命令

```bash
# 足球赛事精彩集锦
python scripts/mps_highlight.py --cos-input-key /input/football.mp4 --scene football

# 篮球赛事
python scripts/mps_highlight.py --cos-input-key /input/basketball.mp4 --scene basketball

# 短剧影视高光
python scripts/mps_highlight.py --cos-input-key /input/drama.mp4 --scene short-drama

# VLOG 全景相机
python scripts/mps_highlight.py --url https://example.com/vlog.mp4 --scene vlog-panorama

# 普通 VLOG（指定输出片段数最多 10 个）
python scripts/mps_highlight.py --cos-input-key /input/vlog.mp4 --scene vlog --top-clip 10

# 自定义场景（带 prompt 和 scenario）
python scripts/mps_highlight.py --url https://example.com/skiing.mp4 \
    --scene custom --prompt "滑雪场景，输出人物高光" --scenario "滑雪"

# 自定义场景 + 指定片段数
python scripts/mps_highlight.py --url https://example.com/skiing.mp4 \
    --scene custom --prompt "滑雪场景" --scenario "滑雪" --top-clip 8

# 仅提交任务，不等待结果
python scripts/mps_highlight.py --cos-input-key /input/football.mp4 --scene football --no-wait

# Dry Run（预览请求参数）
python scripts/mps_highlight.py --cos-input-key /input/football.mp4 --scene football --dry-run

# 查询任务状态
python scripts/mps_get_video_task.py --task-id 2600011633-WorkflowTask-xxxxx
```

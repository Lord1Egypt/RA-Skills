# vod_search_media_by_semantics — 详细参数与示例

> 此文件对应脚本：`scripts/vod_search_media_by_semantics.py`
>
> 自然语言搜索已导入知识库的视频内容（需先通过 `vod_import_media_knowledge.py` 导入）。

### ⚠️ 常见参数错误

| 错误用法 | 正确用法 | 说明 |
|---------|---------|------|
| `--query ...` | `--text ...` | **🚨 语义搜索用 `--text`，绝对不能用 `--query`，参数名不同** |
| `--category Video` | `--categories Video` | **🚨 媒体类型过滤用 `--categories`（复数），不是 `--category`** |

## 参数说明

### 应用选择

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--sub-app-id` | int | - | VOD 子应用 ID（2023-12-25 后开通的必填，也可通过环境变量 `TENCENTCLOUD_VOD_SUB_APP_ID` 设置）；与 `--app-name` 互斥，**必须指定两者之一** |
| `--app-name` | string | - | 通过应用名称/描述模糊匹配子应用（与 `--sub-app-id` 互斥，**必须指定两者之一**） |

### 搜索参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--text` / `-t` | string | ✅ | 自然语言搜索文本（**不是** `--query` 或 `--keyword`） |
| `--limit` / `-n` | int | - | 返回条数（默认 20，范围 [1, 100]） |

### 过滤条件

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--categories` | string[] | - | 文件类型过滤：`Video`/ `Audio`/ `Image`（可多个） |
| `--tags` | string[] | - | 标签过滤（匹配任一标签，最多 16 个，空格分隔） |
| `--persons` | string[] | - | 按人物过滤（匹配所有指定人物，最多 16 个） |
| `--task-types` | string[] | - | 按任务类型过滤（可多个）：`AiAnalysis.DescriptionTask`、`SmartSubtitle.AsrFullTextTask` |

### 输出控制

| 参数 | 类型 | 说明 |
|------|------|------|
| `--verbose` / `-v` | flag | 显示详细信息 |
| `--json` | flag | JSON 格式输出完整响应 |
| `--region` | string | 地域（默认 `ap-guangzhou`） |
| `--dry-run` | flag | 预览请求参数，不实际执行 |

> ⚠️ **前置条件**：媒体需先通过 `vod_import_media_knowledge.py import` 导入知识库，才能被语义搜索到。
> ⚠️ **参数名称**：搜索文本用 `--text`（`-t`），不是 `--query` 或 `--keyword`。

---

## 使用示例

```bash
# 基础语义搜索
python scripts/vod_search_media_by_semantics.py \
    --sub-app-id 1500046806 --text "包含夕阳的海边视频"

# 通过应用名称搜索
python scripts/vod_search_media_by_semantics.py \
    --app-name "测试应用" --text "有人在跑步的画面"

# 按文件类型过滤
python scripts/vod_search_media_by_semantics.py \
    --sub-app-id 1500046806 --text "精彩进球" --categories Video

# 按标签过滤
python scripts/vod_search_media_by_semantics.py \
    --sub-app-id 1500046806 --text "精彩进球" --tags "体育" "足球"

# 按人物过滤
python scripts/vod_search_media_by_semantics.py \
    --sub-app-id 1500046806 --text "采访视频" --persons "张三"

# 指定返回条数
python scripts/vod_search_media_by_semantics.py \
    --sub-app-id 1500046806 --text "会议视频" --limit 50

# 指定搜索任务类型
python scripts/vod_search_media_by_semantics.py \
    --sub-app-id 1500046806 --text "产品介绍" --task-types AiAnalysis.DescriptionTask

# JSON 格式输出
python scripts/vod_search_media_by_semantics.py \
    --sub-app-id 1500046806 --text "包含音乐的视频" --json

# 详细模式
python scripts/vod_search_media_by_semantics.py \
    --sub-app-id 1500046806 --text "产品演示" --verbose

# 预览请求参数（不实际执行）
python scripts/vod_search_media_by_semantics.py \
    --sub-app-id 1500046806 --text "包含夕阳的海边视频" --dry-run
```

---

## API 接口

| 功能 | API 接口 | 文档链接 |
|------|---------|---------|
| 语义搜索媒体 | `SearchMediaBySemantics` | https://cloud.tencent.com/document/api/266/126287 |

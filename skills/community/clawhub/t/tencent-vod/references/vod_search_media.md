# vod_search_media — 详细参数与示例
> 此文件由 references 拆分生成，对应脚本：`scripts/vod_search_media.py`

### ⚠️ 常见参数错误

| 错误用法 | 正确用法 | 说明 |
|---------|---------|------|
| `--keyword 会议` | `--names 会议` | 名称搜索用 `--names` |
| `--types Video` | `--categories Video` | 媒体类型过滤用 `--categories`，值为 `Video`/`Audio`/`Image` |
| `--storage-class ARCHIVE` | `--storage-classes ARCHIVE` | **🚨 存储类型过滤用 `--storage-classes`（复数），不是 `--storage-class`** |

## 参数说明


### 应用选择参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--sub-app-id` | int | - | 子应用 ID，不指定则搜索主应用（也可通过环境变量 `TENCENTCLOUD_VOD_SUB_APP_ID` 设置） |
| `--app-name` | string | - | 通过应用名称/描述模糊匹配子应用（与 --sub-app-id 互斥） |

### 搜索条件参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--file-ids` | string[] | - | 文件 ID 列表（精确匹配，最多10个） |
| `--names` | string[] | - | 文件名列表（模糊匹配，最多10个） |
| `--name-prefixes` | string[] | - | 文件名前缀列表（前缀匹配，最多10个） |
| `--descriptions` | string[] | - | 描述信息列表（模糊匹配，最多10个） |
| `--tags` | string[] | - | 标签列表（匹配任一标签，最多16个） |
| `--class-ids` | int[] | - | 分类 ID 列表（匹配分类及子分类，最多10个） |
| `--categories` | string[] | - | 文件类型: Video/Audio/Image |
| `--source-types` | string[] | - | 来源类型: Record/Upload/VideoProcessing/TrtcRecord 等 |
| `--media-types` | string[] | - | 封装格式: mp4/mp3/flv/jpg 等 |
| `--status` | string[] | - | 文件状态: Normal/SystemForbidden/Forbidden |
| `--review-results` | string[] | - | 审核结果: pass/review/block/notModerated |
| `--storage-regions` | string[] | - | 存储地区: ap-chongqing 等 |
| `--storage-classes` | string[] | - | 存储类型: STANDARD/STANDARD_IA/ARCHIVE/DEEP_ARCHIVE |
| `--stream-ids` | string[] | - | 推流直播码列表（匹配任一，最多10个） |
| `--trtc-sdk-app-ids` | int[] | - | TRTC 应用 ID 列表（匹配任一，最多10个） |
| `--trtc-room-ids` | string[] | - | TRTC 房间 ID 列表（匹配任一，最多10个） |
| `--stream-domains` | string[] | - | 直播推流 Domain 列表（直播录制时有效） |
| `--stream-paths` | string[] | - | 直播推流 Path 列表（直播录制时有效） |

### 时间范围参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--create-after` | string | - | 创建时间起始（ISO 8601 格式） |
| `--create-before` | string | - | 创建时间结束（ISO 8601 格式） |
| `--expire-after` | string | - | 过期时间起始（ISO 8601 格式，无法检索已过期文件） |
| `--expire-before` | string | - | 过期时间结束（ISO 8601 格式） |

### 排序和分页参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--sort-field` | string | - | 排序字段: `CreateTime`（有 `--names`/`--descriptions` 时按匹配度排序，此参数无效） |
| `--sort-order` | string | - | 排序方式: Asc/Desc（默认 Desc） |
| `--offset` | int | - | 分页偏移量（默认 0，Offset+Limit 不超过 5000） |
| `--limit` | int | - | 返回条数（默认 10，Offset+Limit 不超过 5000） |

### 输出控制参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--filters` | string[] | - | 返回信息过滤: `basicInfo`/`metaData`/`transcodeInfo`/`animatedGraphicsInfo` 等 |
| `--verbose` / `-v` | flag | - | 显示详细信息（含 URL） |
| `--json` | flag | - | JSON 格式输出完整响应 |
| `--region` | string | - | 地域（默认 ap-guangzhou） |
| `--dry-run` | flag | - | 预览请求参数，不实际执行 |

### 接口冲突决策说明

| 场景 | 推荐脚本 | 说明 |
|------|---------|------|
| 已知 FileId，查询详情 | `vod_describe_media.py` | DescribeMediaInfos 精确查询 |
| 按名称/标签等模糊搜索 | `vod_search_media.py` | SearchMedia 模糊搜索 |
| 已知 FileId，但需要搜索式查询 | `vod_search_media.py` | SearchMedia.FileIds 参数 |
| 通过应用名称指定应用 | `vod_search_media.py` | 先 DescribeSubAppIds 匹配应用 |

> ⚠️ **强制要求**：至少需要指定一个搜索条件（`--names`/`--file-ids`/`--tags`/`--categories` 等），否则脚本将报错退出。

---

## API 接口

| 功能 | API 接口 | 文档链接 |
|------|---------|---------|
| 搜索媒体 | `SearchMedia` | https://cloud.tencent.com/document/api/266/31813 |

---

## 使用示例


### 基础搜索

#### ✅ 模糊搜索名称（主应用，最常用）
```bash
python scripts/vod_search_media.py --names "我的视频"
```

#### 通过 FileId 搜索（主应用）
```bash
python scripts/vod_search_media.py --file-ids 387702292285462759
```

#### 搜索多个文件名
```bash
python scripts/vod_search_media.py --names "测试视频" "会议录像"
```

---

### 指定应用搜索

#### 指定 SubAppId + FileId 搜索
```bash
python scripts/vod_search_media.py \
    --file-ids 387702292285462759 \
    --sub-app-id 1500046806
```

#### 指定 SubAppId + 名称模糊搜索
```bash
python scripts/vod_search_media.py \
    --names "测试视频" \
    --sub-app-id 1500046806
```

#### ✅ 通过应用名称模糊匹配 + 名称搜索（常用）
```bash
python scripts/vod_search_media.py \
    --names "我的视频" \
    --app-name "测试应用"
```

#### 通过应用名称模糊匹配 + FileId 搜索
```bash
python scripts/vod_search_media.py \
    --file-ids 387702292285462759 \
    --app-name "测试应用"
```

---

### 高级搜索

#### 按文件类型搜索
```bash
# 搜索视频
python scripts/vod_search_media.py --categories Video

# 搜索图片
python scripts/vod_search_media.py --categories Image

# 搜索音频
python scripts/vod_search_media.py --categories Audio
```

#### 按标签搜索
```bash
python scripts/vod_search_media.py --tags "体育" "篮球"
```

#### 按封装格式搜索
```bash
python scripts/vod_search_media.py --names "测试" --media-types mp4
```

#### 按文件状态搜索
```bash
python scripts/vod_search_media.py --categories Video --status Normal
```

#### 按审核结果搜索
```bash
python scripts/vod_search_media.py --review-results pass
```

#### 按创建时间范围搜索
```bash
python scripts/vod_search_media.py --names "会议" \
    --create-after "2026-01-01T00:00:00+08:00" \
    --create-before "2026-03-31T23:59:59+08:00"
```

#### 按存储类型搜索
```bash
python scripts/vod_search_media.py --storage-classes STANDARD
```

---

### 排序、分页和输出

#### 按创建时间降序排序
```bash
python scripts/vod_search_media.py --names "测试" \
    --sort-field CreateTime --sort-order Desc
```

#### 分页查询
```bash
# 第一页
python scripts/vod_search_media.py --names "视频" --offset 0 --limit 20

# 第二页
python scripts/vod_search_media.py --names "视频" --offset 20 --limit 20
```

#### 只返回基础信息
```bash
python scripts/vod_search_media.py --names "视频" --filters basicInfo
```

#### 返回基础信息和元数据
```bash
python scripts/vod_search_media.py --names "视频" --filters basicInfo metaData
```

#### JSON 格式输出
```bash
python scripts/vod_search_media.py --names "视频" --json
```

#### 详细输出（含 URL）
```bash
python scripts/vod_search_media.py --names "视频" --verbose
```

#### 预览请求参数
```bash
python scripts/vod_search_media.py --names "视频" --dry-run
```

---

### 自然语言 → 参数映射速查

当用户用自然语言描述搜索条件时，按以下规则直接映射为参数，**不要追问**：

| 用户自然语言描述 | 对应参数 | 示例命令 |
|--------------|---------|---------|
| "音频类型的媒体" / "音频文件" / "音乐" | `--categories Audio` | `python scripts/vod_search_media.py --categories Audio` |
| "视频类型的媒体" / "视频文件" | `--categories Video` | `python scripts/vod_search_media.py --categories Video` |
| "图片类型的媒体" / "图片文件" | `--categories Image` | `python scripts/vod_search_media.py --categories Image` |
| "2026年1月1日之后创建的" / "1月1日以后上传的" | `--create-after "2026-01-01T00:00:00+08:00"` | `python scripts/vod_search_media.py --create-after "2026-01-01T00:00:00+08:00"` |
| "2026年3月31日之前创建的" | `--create-before "2026-03-31T23:59:59+08:00"` | `python scripts/vod_search_media.py --create-before "2026-03-31T23:59:59+08:00"` |
| "最多返回5条" / "取前5个" | `--limit 5` | `python scripts/vod_search_media.py ... --limit 5` |
| "JSON格式输出" / "以JSON返回" | `--json` | `python scripts/vod_search_media.py ... --json` |
| "mp4格式的" / "flv格式的" | `--media-types mp4` | `python scripts/vod_search_media.py --media-types mp4` |
| "按创建时间倒序" / "最新的在前" | `--sort-field CreateTime --sort-order Desc` | `python scripts/vod_search_media.py ... --sort-field CreateTime --sort-order Desc` |

> ✅ 示例：用户说"搜索2026年1月1日之后创建的媒体，最多返回5条，JSON格式输出"
> ```bash
> python scripts/vod_search_media.py \
>     --create-after "2026-01-01T00:00:00+08:00" \
>     --limit 5 \
>     --json
> ```
>
> ✅ 示例：用户说"搜索音频类型的媒体，最多返回5条"
> ```bash
> python scripts/vod_search_media.py --categories Audio --limit 5
> ```

SearchMedia 和 DescribeMediaInfos 的使用场景对比：

| 场景 | 推荐脚本 | API | 说明 |
|------|---------|-----|------|
| 已知 FileId，查询详情 | `vod_describe_media.py` | DescribeMediaInfos | 精确查询，返回完整信息 |
| 按名称/标签等模糊搜索 | `vod_search_media.py` | SearchMedia | 模糊搜索，支持多种条件 |
| 已知 FileId，搜索式查询 | `vod_search_media.py` | SearchMedia | 通过 --file-ids 参数 |
| 通过应用名称指定应用 | `vod_search_media.py` | SearchMedia | 先 DescribeSubAppIds 匹配 |

#### 示例：已知 FileId 精确查询
```bash
# 推荐用 DescribeMediaInfos
python scripts/vod_describe_media.py --file-id 387702292285462759

# 也可以用 SearchMedia
python scripts/vod_search_media.py --file-ids 387702292285462759
```

---


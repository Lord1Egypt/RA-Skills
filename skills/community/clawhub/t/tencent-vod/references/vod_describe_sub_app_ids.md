# vod_describe_sub_app_ids — 详细参数与示例

> 此文件对应脚本：`scripts/vod_describe_sub_app_ids.py`
>
> 查询当前账号下的所有子应用列表，支持按名称和标签过滤。

## 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--name` | string | - | 按应用名称过滤（模糊匹配） |
| `--tag` | string | - | 按标签过滤，格式 `KEY=VALUE`（可多次传入，多标签为 AND 关系） |
| `--offset` | int | - | 分页起始偏移量（默认 0） |
| `--limit` | int | - | 分页返回数量（范围 1-200） |
| `--region` | string | - | 地域（默认 `ap-guangzhou`） |
| `--json` | flag | - | JSON 格式输出 |
| `--dry-run` | flag | - | 预览请求参数，不实际执行 |

---

## 使用示例

#### 查询当前账号下的所有子应用
```bash
python scripts/vod_describe_sub_app_ids.py
```

#### 按名称过滤
```bash
python scripts/vod_describe_sub_app_ids.py --name "MyAppName"
```

#### JSON 格式输出
```bash
python scripts/vod_describe_sub_app_ids.py --json
```

#### dry-run 预览请求参数
```bash
python scripts/vod_describe_sub_app_ids.py \
    --name "MyAppName" \
    --tag env=prod \
    --dry-run
```

#### 按单个标签过滤
```bash
python scripts/vod_describe_sub_app_ids.py --tag env=prod
```

#### 按多个标签联合过滤（AND 关系）
```bash
python scripts/vod_describe_sub_app_ids.py \
    --tag env=prod \
    --tag team=media
```

#### 分页查询前 20 条记录
```bash
python scripts/vod_describe_sub_app_ids.py \
    --offset 0 \
    --limit 20
```

#### 组合名称、标签和分页条件查询
```bash
python scripts/vod_describe_sub_app_ids.py \
    --name "MyAppName" \
    --tag env=prod \
    --tag owner=video-team \
    --offset 20 \
    --limit 20
```

#### 将结果保存为 JSON 文件
```bash
python scripts/vod_describe_sub_app_ids.py --json > sub_apps.json
```

#### 使用 jq 提取子应用 ID 列表
```bash
python scripts/vod_describe_sub_app_ids.py --json | jq -r '.SubAppIdInfoSet[].SubAppId'
```

#### 使用 jq 提取启用状态的子应用名称
```bash
python scripts/vod_describe_sub_app_ids.py --json | \
    jq -r '.SubAppIdInfoSet[] | select(.Status == "On") | .SubAppIdName'
```

#### 查询绑定指定标签的所有子应用并提取地域信息
```bash
python scripts/vod_describe_sub_app_ids.py \
    --tag env=prod \
    --json | jq -r '.SubAppIdInfoSet[] | {name: .SubAppIdName, regions: .StorageRegions}'
```

---

## 响应字段说明

### 顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `SubAppIdInfoSet` | object list | 子应用信息集合 |
| `TotalCount` | int | 应用总数量 |
| `RequestId` | string | 请求 ID |

### SubAppIdInfoSet（子应用信息）

| 字段 | 类型 | 说明 |
|------|------|------|
| `SubAppId` | int | 子应用 ID |
| `SubAppIdName` | string | 子应用名称（优先使用此字段） |
| `Name` | string | 旧版子应用名称字段（已不推荐，优先使用 `SubAppIdName`） |
| `Description` | string | 子应用简介 |
| `Status` | string | 子应用状态，常见值：`On`、`Off`、`Destroying`、`Destroyed` |
| `Mode` | string | 子应用模式，常见值：`fileid`、`fileid+path` |
| `CreateTime` | string | 创建时间（ISO 8601 格式） |
| `StorageRegions` | string list | 已启用的存储地域列表 |
| `Tags` | object list | 标签列表，元素包含 `TagKey` 和 `TagValue` |

---

## 错误处理说明

| 错误类型 | 原因 | 处理建议 |
|---------|------|---------|
| 标签格式错误 | `--tag` 未使用 `KEY=VALUE` 格式（缺少 `=`） | 检查标签格式，例如 `env=prod` |
| 标签键为空 | `--tag` 中 `=` 前的键为空 | 确保键不为空，例如 `env=prod` |
| Offset 非法 | `--offset` 小于 0 | 使用大于等于 0 的整数 |
| Limit 非法 | `--limit` 超出 1-200 范围 | 使用 1 到 200 之间的整数 |

---

## API 接口

| 功能 | API 接口 | 文档链接 |
|------|---------|---------|
| 查询子应用列表 | `DescribeSubAppIds` | https://cloud.tencent.com/document/api/266/35152 |

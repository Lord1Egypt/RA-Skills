---
name: toupiaoya-creator
description: |
    投票鸭是易企秀旗下的在线投票制作工具，支持模板检索与投票活动创建。
    当用户需要制作投票、发起评选、组织投票活动时使用此 Skill。
  
    核心功能：
    1. 检索投票模板——按关键词、颜色、热度筛选，返回模板列表与链接
    2. 创建投票作品——支持文字投票、图片投票、视频投票，可设置多选/单选、时间范围
    3. 素材上传——换取 COS 临时凭证并上传到腾讯云 COS（如 `material/` 前缀）
    4. 素材列表——分页查询当前用户已上传的图片素材（`material list`）
    5. 作品列表——分页查询工作台场景/作品（`project list`）
    6. 投票数据——查询作品投票提交数据（`project vote-data`）
    7. 访问趋势——查询作品访问趋势数据（`project view-data`）
    8. 选项管理——读取作品全部选项（`get_choices`）、更新单个选项（`update_choices`）、新增选项（`add_choices`）
    9. 分组管理——读取分组（`get_groups`）、新增分组（`add_group`）、修改分组名（`update_group`）

    触发词：易企秀、制作投票、创建投票、发起投票、在线投票、投票模板、评选投票、微信投票、
    活动投票、投票系统、投票链接、二维码投票、投票活动怎么弄、怎么发起投票、
    投票工具、投票网站、免费投票、作品评选、摄影投票、美食投票、萌娃投票

summary:   投票鸭技能，支持检索投票模板、创建投票活动（文字/图片/视频投票）、COS 素材上传与素材列表。
  检索 `search`、创建 `project create`、作品列表 `project list`、投票数据 `project vote-data`、访问趋势 `project view-data`、上传 `upload`、素材列表 `material list`、选项读取/更新/新增（`get_choices`/`update_choices`/`add_choices`）、分组读取/新增/改名（`get_groups`/`add_group`/`update_group`）；实现位于 `scripts/toupiaoya/` 包内，`toupiaoya_cli.py` 仅为入口。

read_when:
  - 用户提到投票、评选、投票活动、投票模板
  - 用户想要创建投票链接/二维码投票/投票小程序
  - 用户想找一个免费投票工具/网站/小程序
  - 用户描述"我想做个投票让大家选…"

---

# 投票鸭技能说明

## 前置条件

1. 模板查询与 COS token 依赖 `requests`；`upload` 子命令另需 `cos-python-sdk-v5`。
2. 获取`X-Openclaw-Token`地址：`https://www.toupiaoya.com/skillAccess/token`
3. 建议先完成 token 登录：`X-Openclaw-Token` 存在 `~/.toupiaoya/config.json`，后续命令自动复用。
4. 创建接口需准备 `briefTitle` 与 `briefDesc`。

## 认证与登录（推荐）

```bash

# 验证登录状态
python scripts/toupiaoya_cli.py auth status

# 交互式保存 token 到 ~/.toupiaoya/config.json，如果存在token，验证token有效性即可
python scripts/toupiaoya_cli.py login

```

`auth status` 会在请求头携带 `X-Openclaw-Token` 调用：
- 返回 `{"success": true, "code": 200, ...}` 表示 token 有效
- 返回 `{"success": false, "code": 1002, "msg":"认证失败", ...}` 表示 token 无效

## 查询投票类模板

### 命令示例

```bash
python scripts/toupiaoya_cli.py search \
  --keywords "摄影大赛" \
  --pageNo 1 \
  --pageSize 10 \
  --sortBy "common_total|desc" \
  --color "紫色"
```

### 参数说明（对应 `toupiaoya_cli.py`）

- `--keywords`：关键词（可选）
- `--pageNo`：页码，默认 `1`
- `--pageSize`：每页条数，默认 `10`
- `--sortBy`：排序，默认 `common_total|desc`
- `--color`：颜色筛选（可选，例：紫色/蓝色/粉色）

### 输出示例（stdout JSON）

```json
{
  "total": 123,
  "end": false,
  "results": [
    {
      "templateId": 1234,
      "title": "模板标题",
      "link": "https://www.toupiaoya.com/mall/detail-h5e/<templateId>",
      "description": "模板描述",
      "pv": 9999
    }
  ]
}
```

若 `total == 0`，脚本返回 `{}`。对话输出时建议展示前 3-5 个模板的标题、链接、描述和热度。

## 创建投票作品

使用 `scripts/toupiaoya_cli.py project create`（作品以 `project` 子命令组织）。

### 请求体

必填：

- `briefTitle`：封面标题
- `briefDesc`：封面简介

可选：
- `sponsor` : 投票主办方
- `detailTitle`: 详细的标题，不超过20字
- `detailDesc` : 详细的描述，例如规则，投票时间等介绍
- `voteType`：`imageVote` | `textVote`(默认) | `videoVote`
- `timeStart`、`timeEnd`：格式 `yyyy-MM-dd HH:mm`
- `groupList`
- `templateId`（默认 `19980321`代表空白模版），可以使用搜索出的templateId
- 单双选控制：默认单选；传 `--multi` 表示多选。
- `--access-token`：可显式传 token；不传则默认读取 `~/.toupiaoya/config.json`。

说明：不传 `timeStart/timeEnd` 时，服务内部按“开始=当前，结束=当前+10天”处理。

### 命令示例
文字选项投票, 多选：
```bash
python scripts/toupiaoya_cli.py project create \
  --sponsor "投票主办方A" \
  --briefTitle "年度最佳作品投票" \
  --briefDesc "封面简介：本次活动由某某主办。" \
  --detailTitle "年度最佳作品投票" \
  --detailDesc "投票规则：每人每天可投一次。" \
  --voteType "textVote" \
  --templateId 19980321 \
  --multi \
  --groupList '[{"groupName":"默认组","choices":[{"name":"作品1"},{"name":"作品2"}]}]'
```

图片投票：
```bash
python scripts/toupiaoya_cli.py project create \
  --briefTitle "年度最佳作品投票" \
  --briefDesc "封面简介：本次活动由某某主办。" \
  --detailTitle "年度最佳作品投票" \
  --detailDesc "投票规则：每人每天可投一次。" \
  --voteType "imageVote" \
  --templateId 19980321 \
  --groupList '[{"groupName":"主推","choices":[{"name":"作品1","cover":"https://example.com/p1.png"},{"name":"作品2","cover":"https://example.com/p2.png"}]}]'
```

说明：`project create` 会自动在请求头中带 `X-Openclaw-Token`（来源：`--access-token` 或本地配置）。

## 作品列表（project list）

```bash
python scripts/toupiaoya_cli.py project list --pageNum 1 --pageSize 27
```

成功时 stdout 为接口完整 JSON（含 `list`、`map`、`obj` 等）。

## 作品投票数据

```bash
python scripts/toupiaoya_cli.py project vote-data --id 20613397 --pageNo 1 --pageSize 10 --showTrash 1
```

常用参数：
- `--id`：作品 id（必填）
- `--startTime`：开始时间（可选，默认空字符串，格式：yyyy-MM-dd）
- `--endTime`：结束时间（可选，默认空字符串，格式：yyyy-MM-dd）
- `--pageNo`：页码（默认 `1`）
- `--pageSize`：每页条数（默认 `10`）
- `--showTrash`：是否展示回收站数据（默认 `1`）

返回结构说明：
- `obj`：表头字段数组
- `map`：分页统计（`total/pageNo/pageSize/end/todayCount` 等）
- `list`：二维数据行（首行为表头，后续为每条投票记录）

## 作品访问趋势（project view-data）

```bash
python scripts/toupiaoya_cli.py project view-data --id 20613397 --startDay 2026-04-08 --endDay 2026-04-22
```

常用参数：
- `--id`：作品 id（必填）
- `--startDay`：统计开始日期（可选，格式 `yyyy-MM-dd`）
- `--endDay`：统计结束日期（可选，格式 `yyyy-MM-dd`）

日期默认策略：
- 不传 `--endDay` 时，默认今天
- 不传 `--startDay` 时，默认 `endDay-14天`（即最近 15 天窗口）

返回字段（`obj`）说明：
- `time`：日期序列（与各指标一一对应）
- `uv`：新增访客数
- `pv`：新增浏览量
- `spv`：新增转发数
- `fpv`：新增表单数

## 上传素材

依赖：本仓库根目录 `requirements.txt` 中的 `cos-python-sdk-v5`（与 `requests`）；单独使用技能目录时可 `pip install cos-python-sdk-v5 requests`。

1. 使用 `X-Openclaw-Token` 请求 
2. 使用返回的 `tmpSecretId` / `tmpSecretKey` / `sessionToken` / `region` 初始化 COS SDK，对本地文件执行 `PutObject`。
3. 将 `path` / `tmbPath`（默认与 COS `key` 相同）、`name`（本地文件名）、`size`、`extName` 等写入素材库；`source` 默认 `P010238`，可用 `--source` 覆盖。

```bash
python scripts/toupiaoya_cli.py upload --file ./photo.png --prefix "/material/"
```

常用参数：`--bucket`（默认 `eqxiu`）、`--prefix`（默认 `'/material/'`）、`--name`（COS 对象名，默认本地 basename）、`--source`（saveFile）、`--tag-id`、`--file-type`、`--tmb-path`（与 path 不一致时）。成功时 stdout 为 JSON，顶层含 `cos`（`key`、`etag`、`assetUrl` 等）与 `material`（接口 `obj`，如素材 `id`、`path`）。若 COS 已成功但 saveFile 失败，错误 JSON 内会附带 `cos` 字段便于排查。

## 素材列表（用户上传图片）

固定 `fileType=1`（图片），`pageNo` / `pageSize` / `tagId` 可调（默认 `tagId=-1`）

```bash
python scripts/toupiaoya_cli.py material list --pageNo 1 --pageSize 30 --tagId -1
```

成功时 stdout 为接口完整 JSON（含 `list`、`map` 分页信息等）。

## 返回值解析

统一形态：

```json
{ "success": true|false, "code": 200|..., "msg": "...", "data": ... }
```

成功常见：

1. 含 `id`
   - `editUrl`: `https://www.toupiaoya.com/fe/<id>`,代表编辑链接
   - `previewUrl`: `https://forms.ebdan.net/ls/<code>`, 代表手机预览链接
2. `id == 0` 分支
   - 仅返回工具层 `data`（无 `id`）
   - 预览链接可拼：`https://forms.ebdan.net/ls/` + `data.code`

失败常见：

- 404（业务异常）
- 400 (参数缺失)

## 选项管理（Python 调用方式）

### 获取作品全部选项（get_choices）

- 语义：按作品 `id` 读取当前投票组件中的所有选项，不再是“根据 groupList 生成选项”。
- CLI 命令：

```bash
python scripts/toupiaoya_cli.py project choice get --id <project_id> [--access-token <token>]
```

- 成功返回的 `data`：
  - `choices`：当前全部选项（来自 `voteSettings.list`）
  - `groupList`：分组信息（来自 `voteSettings.groupsList`）
  - `seq`：选项数量

示例：
```json
{
  "success": true,
  "code": 200,
  "msg": "ok",
  "data": {
    "choices": [{ "id": 1, "content": "选项A", "groupId": 1 }],
    "groupList": [{ "id": 1, "name": "默认分组" }],
    "seq": 1
  }
}
```

### 更新单个选项（update_choices）

- 语义：更新某个指定选项（按 `choiceId` 定位），不是整包覆盖所有选项。
- CLI 命令：

```bash
python scripts/toupiaoya_cli.py project choice update \
  --id <project_id> \
  --choiceId <choice_id> \
  [--groupId <target_group_id>] \
  --choice '{"content":"新的选项名","cover":"material/xxx.png"}' \
  [--access-token <token>]
```

`--choice` 的 JSON 对象等价于请求体中的 `choice` 字段。对应结构示例：
```json
{
  "id": 123,
  "choiceId": 2,
  "choice": {
    "content": "新的选项名",
    "cover": "material/xxx.png"
  }
}
```

也可直接使用可选 `groupId` 把该选项移动到目标分组（无需在 `--choice` 里写 `groupId`）：

```bash
python scripts/toupiaoya_cli.py project choice update \
  --id 123 \
  --choiceId 2 \
  --groupId 3 \
  --choice '{"content":"新的选项名"}'
```

- 说明：
  - `id`：作品 id（必填）
  - `choiceId`：待更新选项 id（必填）
  - `groupId`：可选，目标分组 id；传入后会把该 choice 移到对应分组
  - `choice`：更新字段对象（至少一个字段），当前支持：`content`、`cover`、`desc`、`groupId`、`rank`、`num`

### 新增选项（add_choices）

- 语义：在指定分组下新增一个选项，`choice.id` 由服务端自动递增分配（当前最大 `id + 1`）。
- CLI 命令：

```bash
python scripts/toupiaoya_cli.py project choice add \
  --id <project_id> \
  --groupId <target_group_id> \
  --choice '{"content":"新增选项","cover":"material/xxx.png"}' \
  [--access-token <token>]
```

- 说明：
  - `id`：作品 id（必填）
  - `groupId`：目标分组 id（必填）
  - `choice`：新增字段对象（必填），至少应包含 `content`；可选 `cover`、`desc`、`rank`、`num`

## 分组管理

优先使用 CLI：

### 获取分组（get_groups）

```bash
python scripts/toupiaoya_cli.py project group get --id <project_id> [--access-token <token>]
```

- 返回：当前作品的 `groupsList` 数组（每项含 `id`、`name`）

### 新增分组（add_group）

```bash
python scripts/toupiaoya_cli.py project group add \
  --id <project_id> \
  --groupName "新分组" \
  [--access-token <token>]
```

- 必填参数：
  - `id`：作品 id
  - `groupName`：分组名称
- 行为：自动分配递增 `groupId`（`max(id)+1`）

### 修改分组名（update_group）

```bash
python scripts/toupiaoya_cli.py project group update \
  --id <project_id> \
  --groupId <group_id> \
  --groupName "新分组名" \
  [--access-token <token>]
```

- 必填参数：
  - `id`：作品 id
  - `groupId`：分组 id
  - `groupName`：新分组名


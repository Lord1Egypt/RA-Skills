# 投票鸭 Creator Skill（toupiaoya-creator）

面向「投票鸭」场景的 Agent 技能：支持**投票模板检索**与**通过 HTTP 创建投票作品**。详细行为与参数以仓库内 [`SKILL.md`](./SKILL.md) 为准；本文档为面向使用者的说明与快速上手。

## 适用场景

- 用户提到投票、评选、拉票、模板挑选
- 需要通过 Python 脚本检索投票模板
- 需要通过 HTTP 创建投票作品

## 目录结构

| 路径 | 说明 |
|------|------|
| `SKILL.md` | 技能元数据与完整指令（name、description、read_when、流程说明） |
| `scripts/toupiaoya_cli.py` | 命令行入口：`search`、`project create` / `project list`、`upload`、`material list` 等 |
| `README.md` | 本说明文档 |

## 前置条件

1. **模板查询**依赖 Python 包：`requests`（`pip install requests`）。
2. **创建作品**前需准备文案：`briefTitle`（封面标题）、`briefDesc`（封面简介）。

## 快速开始

在技能目录下执行（或将 `scripts/toupiaoya_cli.py` 换为绝对路径）：

```bash
python scripts/toupiaoya_cli.py search --keywords "摄影大赛" --pageNo 1 --pageSize 10
```

不传子命令时，CLI 会**兼容旧用法**，默认按 `search` 执行。

---

## 一、查询投票类模板（推荐）

### 命令示例

```bash
python scripts/toupiaoya_cli.py search \
  --keywords "摄影大赛" \
  --pageNo 1 \
  --pageSize 10 \
  --sortBy "common_total|desc" \
  --color "紫色"
```

### 参数说明（`toupiaoya_cli.py search`）

| 参数 | 说明 |
|------|------|
| `--keywords` | 关键词（可选） |
| `--pageNo` | 页码，默认 `1` |
| `--pageSize` | 每页条数，默认 `10` |
| `--sortBy` | 排序，默认 `common_total|desc` |
| `--color` | 颜色筛选（可选），如：紫色、蓝色、粉色、红色、绿色、青色、橙色、黄色、黑色、白色、灰色 |

### 输出说明（stdout，JSON）

- 若命中结果 `total == 0`，脚本输出 `{}`。
- 否则大致形态为：

```json
{
  "total": 123,
  "end": false,
  "results": [
    {
      "templateId": 1234,
      "title": "模板标题",
      "link": "https://www.toupiaoya.com/mall/detail-h5e/1234",
      "description": "模板描述",
      "pv": 9999,
      "cover": "https://asset.eqh5.com/..."
    }
  ]
}
```

在对话或汇报中，建议展示前 **3～5** 个模板的标题、链接、描述与热度（`pv`）。

> **说明**：`SKILL.md` 示例中使用字段名 `results`；当前 `toupiaoya_cli.py` 实际输出列表字段为 **`results`**，条目字段与用途一致。

---

## 二、创建投票作品

使用子命令 `project create`，底层请求：`POST` 至 `https://ai-api.toupiaoya.com/iaigc-toupiaoya/create`（可通过 `ToupiaoyaCreator` 修改 `base_url`）。

### 请求体要点

**必填**

- `briefTitle`：封面标题  
- `briefDesc`：封面简介  

**可选**

- `detailTitle`：详细标题（不超过约 20 字，以业务侧限制为准）  
- `detailDesc`：详细描述（规则、投票时间等）  
- `voteType`：`imageVote` | `textVote`（CLI 默认） | `videoVote`  
- `timeStart`、`timeEnd`：格式 `yyyy-MM-dd HH:mm`  
- `groupList`：分组与选项结构（JSON）  
- `templateId`：模板 ID；可使用搜索得到的 `templateId`。不传时由后端默认（`SKILL.md` 中示例空白模板为 `19980321`）  
- **单选 / 多选**：默认单选；命令行传 `--multi` 表示多选（对应 `singleVote: false`）

**时间说明**：不传 `timeStart` / `timeEnd` 时，服务端通常按「开始=当前，结束=当前 + 10 天」处理（以实际 API 行为为准）。

### 命令示例

**文字选项投票，多选：**

```bash
python scripts/toupiaoya_cli.py project create \
  --briefTitle "年度最佳作品投票" \
  --briefDesc "封面简介：本次活动由某某主办。" \
  --detailTitle "年度最佳作品投票" \
  --detailDesc "投票规则：每人每天可投一次。" \
  --voteType "textVote" \
  --templateId 19980321 \
  --multi \
  --groupList '[{"groupName":"默认组","choices":[{"name":"作品1"},{"name":"作品2"}]}]'
```

**图片投票：**

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

`--groupList` 须为合法 JSON 数组字符串。

---

## 三、返回值解析（创建接口）

统一外层形态：

```json
{ "success": true, "code": 200, "msg": "...", "data": { ... } }
```

**成功时常见情况**

1. `data` 中含 `scene_uuid`  
   - **编辑链接**：`https://www.toupiaoya.com/indesign?id=<scene_uuid>`  
   - **手机预览**：`https://forms.ebdan.net/ls/<code>`（`code` 以响应为准）

2. `id == 0` 等分支  
   - 可能仅返回工具层 `data`，无 `scene_uuid`  
   - 预览可尝试：`https://forms.ebdan.net/ls/` + `data.code`（以实际返回字段为准）

**失败常见**

- HTTP **404** 或业务错误码（以响应 `msg` / `code` 为准）

---

## 与 `SKILL.md` 的关系

- **Agent / Cursor**：读取 `SKILL.md` 中的 YAML 头（`name`、`description`、`read_when`）与正文流程。  
- **人类开发者**：以本 `README` 做目录与命令速查；细节变更时请同步更新 `SKILL.md` 与本文件。

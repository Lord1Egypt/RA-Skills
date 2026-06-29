---
name: zingapi-creative-list
description: 用于调用 ZingAPI 的“创意列表查询”接口。适用于按行业、国家/地区、渠道、关键词、素材类型、AI 标签、时间范围、排序方式等条件检索广告创意、广告素材、创意投放记录、广告主创意和近期新增创意。
---

# ZingAPI 创意列表查询

本 skill 用于调用 ZingAPI 的创意列表查询接口，并将自然语言检索需求转换为稳定的接口请求。

接口地址：

`POST https://openapi.dataideaglobal.com/zingapi/v1/creative/list/{customer_name}`

固定请求头：

`x-zf-action: creative-list`

## 凭证要求

调用接口前必须配置以下环境变量：

- `ZINGAPI_ACCESS_KEY_ID`
- `ZINGAPI_ACCESS_KEY_SECRET`
- `ZINGAPI_CUSTOMER_NAME`

如任一变量缺失，应先提示用户完成配置。不得在回复、日志或错误信息中展示密钥明文。

## 使用方式

所有接口请求均通过 `scripts/creative_list.py` 执行。常规查询优先使用脚本参数；需要完整控制入参时，可使用 JSON 请求体。

示例：查询最近 30 天美国 Facebook 渠道的游戏视频创意，并返回 AI 标签。

```powershell
python scripts/creative_list.py `
  --app-type 游戏 `
  --geo 美国 `
  --platform Facebook `
  --creative-type 视频 `
  --seen-days 30 `
  --sort 最新 `
  --include-ai-tags
```

示例：使用原始 JSON 请求体。

```powershell
python scripts/creative_list.py --body '@request.json' --output summary
```

示例：仅检查请求体与签名头，不发送真实请求。

```powershell
python scripts/creative_list.py --app-type 游戏 --keyword puzzle --dry-run
```

## 参数转换规范

根据用户描述转换为脚本参数时，遵循以下规则：

- 完整入参映射见 `references/input-mapping.md`。当用户描述命中该映射表中的字段，但脚本没有对应的专用命令行参数时，应生成 JSON 请求体，并使用 `python scripts/creative_list.py --body '@request.json'` 调用。
- 行业类型：`游戏`、`工具`、`电商` 分别对应 `app_type` 的 `1`、`2`、`3`。
- 素材类型：`图片`、`视频`、`轮播`、`HTML`、`试玩` 分别对应 `ads_type` 的 `1`、`2`、`3`、`4`、`7`。
- 国家/地区：中文国家名应转换为三位国家/地区编码，例如 `美国` 转为 `USA`，`日本` 转为 `JPN`。
- 排序方式：`最新`、`展现`、`热度`、`最后发现`、`投放天数`、`点赞`、`评论`、`分享` 分别转换为对应的 `sort_field`。
- 去重方式：`广告去重`、`素材去重`、`广告主去重` 分别对应 `duplicate_removal` 的 `0`、`1`、`2`。
- 页码默认值为 `page=1`；每页数量默认值为 `page_size=20`，最大值为 `20`。
- 用户未指定时间范围时，默认查询最近 7 天。
- 用户要求“返回 AI 标签”或“带 AI 标签”时，添加 `--include-ai-tags`。

## 执行流程

1. 识别用户的检索目标、行业、地区、渠道、素材类型、时间范围和排序方式。
2. 若关键条件缺失但可使用默认值，应直接采用默认值；仅在业务目标无法判断时再询问用户。
3. 使用 `scripts/creative_list.py` 发起请求。
4. 默认返回摘要结果；仅当用户明确要求完整响应时使用 `--output raw`。
5. 错误处理时保留 `trace_id`，便于接口问题排查。
6. 如后续需要查询创意详情，应保留结果中的 `ad_key`、`app_type` 和 `search_flag`。

## 输出字段

默认摘要结果按业务含义分组展示，包括：

- `广告主`：广告主名称、ID 或域名、开发者、Logo、分类。
- `素材`：素材类型、预览图、资源列表、视频时长、素材 ID、NSFW 标记。
- `投放`：行业、渠道、国家地区、文案语言、首次投放时间、最后发现时间、投放天数。
- `指标`：人气总值、当周人气值总和、展现估值、热度值、关联广告数、互动数据。
- `文案`：标题、正文、Message、CTA。
- `链接`：落地页、原帖链接、结束卡片或关联视频。
- `游戏标签`：游戏核心赛道、游戏 IP、游戏玩法、游戏主题。
- `AI素材标签`：图片、视频及新版 AI 标签。
- `原始字段`：保留关键原始字段，便于二次查询和排查。

字段含义以 `references/response-fields.md` 为准。用户要求展示“人气值”时，应使用 `指标.人气总值` 或 `指标.当周人气值总和`；不得将 `指标.热度值` 作为人气值展示。
摘要结果会将渠道、国家/地区等字典编码转换为“名称 (编码)”格式。人气值、热度值、展现估值等较大数值会使用 `K`、`M`、`B` 缩写并保留一位小数；原始编码和原始数值保留在 `原始字段` 中。

当 `is_nsfw` 为 `true` 时，素材资源地址可能被隐藏或替换为默认图片。

## 参考资料

- 参数说明见 `references/parameters.md`。
- 完整入参映射见 `references/input-mapping.md`。
- 出参字段说明见 `references/response-fields.md`。
- 配置与调用示例见 `references/examples.md`。

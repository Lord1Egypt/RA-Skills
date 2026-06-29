# 创意列表查询出参字段说明

本文档根据《ZingAPI 对接文档》中“创意列表查询”的响应体整理，用于解释摘要输出中的字段含义。

## 外层字段

| 字段 | 含义 |
| --- | --- |
| `trace_id` | 请求跟踪 ID，用于问题排查。 |
| `message` | 请求结果消息。成功时通常为 `success`。 |
| `remaining_volume` | 当月剩余可用数据量。 |
| `total_count` | 创意总数，最大返回 `10000`。 |
| `fetch_count` | 部分客户定制字段，通常与可获取数量相关。 |

## 核心标识

| 原始字段 | 摘要字段 | 含义 |
| --- | --- | --- |
| `ad_key` | `创意ID` | 创意唯一 ID。 |
| `search_flag` | `查询标识` | 用于创意详情查询的查询标识。 |

## 广告主

| 原始字段 | 摘要字段 | 含义 |
| --- | --- | --- |
| `advertiser_name` | `广告主.名称` | 广告主名称。 |
| `advertiser_id` | `广告主.ID或域名` | 广告主 ID 或广告主 domain；对于应用类广告，通常为 App Store 应用 ID 或 Google Play 应用 ID。 |
| `ecom_advertiser_id` | 原始响应字段 | 电商广告主 ID。 |
| `app_developer` | `广告主.开发者` | 应用开发者。 |
| `logo_url` | `广告主.Logo` | 广告主 Logo 地址。 |
| `category_tag` | `广告主.分类` | 广告主分类，通常为一级分类到二级分类数组的映射。 |

## 素材

| 原始字段 | 摘要字段 | 含义 |
| --- | --- | --- |
| `ads_type` | `素材.类型编码` | 图片&视频类型：`1` 图片，`2` 视频，`3` 轮播，`4` HTML，`7` 试玩广告。 |
| `preview_img_url` | `素材.预览图` | 预览图地址。视频类素材通常为视频封面。 |
| `preview_img_size` | `素材.预览图尺寸` | 预览图尺寸。 |
| `resource_urls` | `素材.资源列表` | 素材资源列表。 |
| `resource_urls[].type` | `素材.资源列表[].type` | 资源形式或版式类型，同 `ads_type`。 |
| `resource_urls[].image_url` | `素材.资源列表[].image_url` | 图片资源地址；视频素材中通常为视频封面。 |
| `resource_urls[].video_url` | `素材.资源列表[].video_url` | 视频资源地址，视频素材有值。 |
| `video_duration` | `素材.视频时长秒` | 视频时长，单位为秒。 |
| `video2pic` | `素材.视频转图片标识` | 视频类素材中视频转图片标识；`1` 表示无视频素材。 |
| `image_ahash_md5` | `素材.图片Hash` | 图片素材 hash 值。 |
| `material_id` | `素材.素材ID` | 素材 ID。 |
| `is_nsfw` | `素材.NSFW` | 是否为 NSFW 素材。为 `true` 时，资源地址和预览图可能被隐藏或替换为默认图片。 |

## 投放

| 原始字段 | 摘要字段 | 含义 |
| --- | --- | --- |
| `app_type` | `投放.行业编码` | 广告主类型：`1` 游戏，`2` 工具，`3` 电商。 |
| `platform` | `投放.渠道` | 投放渠道。 |
| `countries` | `投放.国家地区` | 投放国家/地区。 |
| `language` | `投放.文案语言` | 文案语言。 |
| `first_seen` | `投放.首次投放时间` | 创意首次投放时间，Unix 时间戳。 |
| `last_seen` | `投放.最后发现时间` | 创意最后发现时间，Unix 时间戳。 |
| `days_count` | `投放.投放天数` | 创意投放天数，等于 `first_seen` 和 `last_seen` 相差的天数。 |
| `post_created_time` | `投放.原帖创建时间` | 原帖创建时间，Unix 时间戳。 |
| `page_id` | `投放.主页ID` | 投放主页 ID。 |
| `page_name` | `投放.主页名称` | 投放主页名称。 |
| `fb_merge_channel` | `投放.FB合并渠道` | 请求包含 `fb_merge` 时，表示合并了哪些 FB 系渠道。 |

摘要输出会将 `platform`、`countries`、`fb_merge_channel` 等字典编码转换为“名称 (编码)”格式，例如 `facebook` 输出为 `FB News Feed (facebook)`，`JPN` 输出为 `日本 (JPN)`。若响应中出现未收录的编码，则保持原值。

## 指标

| 原始字段 | 摘要字段 | 含义 |
| --- | --- | --- |
| `all_exposure_value` | `指标.人气总值` | 人气总值。用户要求“人气值”时优先使用该字段。 |
| `new_week_exposure_value` | `指标.当周人气值总和` | 当周人气值总和。 |
| `exposure_top` | `指标.人气值Top标签` | 人气值 Top 标签信息。每个 Top 标签限定在某个渠道和分类。 |
| `exposure_top_week` | `指标.人气值Top标签周` | 创意最近一次打上 Top 标签的当周周一，格式为 `yyyyMMdd`。 |
| `impression` | `指标.展现估值` | 创意展现估值。 |
| `heat` | `指标.热度值` | 创意热度值。该字段不是人气值。 |
| `related_ads_count` | `指标.关联广告数` | 关联广告数。 |
| `ad_cost` | `指标.广告花费美元` | 广告花费，单位美元。仅 Facebook 渠道含欧盟受众数据的创意有值。 |
| `like_count` | `指标.点赞数` | 点赞数。仅部分社媒渠道创意有值。 |
| `comment_count` | `指标.评论数` | 评论数。仅部分社媒渠道创意有值。 |
| `share_count` | `指标.分享数` | 分享数。仅部分社媒渠道创意有值。 |
| `view_count` | `指标.浏览数` | 浏览数。仅部分社媒渠道创意有值。 |

摘要输出中，`all_exposure_value`、`new_week_exposure_value`、`impression`、`heat` 等较大数值会使用 `K`、`M`、`B` 缩写并保留一位小数，例如 `3600` 输出为 `3.6K`，`2100000` 输出为 `2.1M`。原始数值会保留在 `原始字段` 中。

## 文案与链接

| 原始字段 | 摘要字段 | 含义 |
| --- | --- | --- |
| `title` | `文案.标题` | 创意文案标题。 |
| `body` | `文案.正文` | 创意文案内容。 |
| `message` | `文案.Message` | 创意文案 message。 |
| `call_to_action` | `文案.CTA` | CTA 按钮文字。 |
| `text_md5` | `文案.文案唯一标识` | 创意文案唯一标识。 |
| `store_url` | `链接.落地页` | 落地页地址。 |
| `source_url` | `链接.原帖链接` | 原帖链接。 |
| `html_url` | `链接.结束卡片或关联视频` | 视频类创意通常为结束卡片；试玩类创意通常为关联视频。 |
| `source_app` | `链接.媒体包名` | 媒体包名。 |

## 游戏标签

| 原始字段 | 摘要字段 | 含义 |
| --- | --- | --- |
| `game_core_track` | `游戏标签.游戏核心赛道` | 游戏核心赛道。 |
| `game_ip` | `游戏标签.游戏IP` | 游戏 IP。 |
| `game_play` | `游戏标签.游戏玩法` | 游戏玩法。 |
| `game_theme` | `游戏标签.游戏主题` | 游戏主题。 |

## AI 素材标签

| 原始字段 | 摘要字段 | 含义 |
| --- | --- | --- |
| `ai_image_tags` | `AI素材标签.图片 AI 标签` | 图片素材的 AI 分析标签。 |
| `ai_video_tags` | `AI素材标签.视频 AI 标签` | 视频素材的 AI 分析标签。 |
| `ai_image_tags_new` | `AI素材标签.新版图片 AI 标签` | 图片素材的新版 AI 分析标签。 |
| `ai_video_tags_new` | `AI素材标签.新版视频 AI 标签` | 视频素材的新版 AI 分析标签。 |
| `summary` | `summary` | AI 标签名称总结。 |
| `tags` | `tags` | AI 标签列表。 |
| `tag_code` | `tag_code` | 标签编码。 |
| `tag_name` | `tag_name` | 标签名称。 |
| `parent_code` | `parent_code` | 父级标签编码。 |
| `parent_name` | `parent_name` | 父级标签名称。 |

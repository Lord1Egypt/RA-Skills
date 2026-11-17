# 平台规则路由契约

本文件是 `siluzan-cso` 内容生成流程的平台规则唯一映射源。规则正文只保存在同目录的各平台文件中；不得在其他工作流、代码或清单中复制映射表或规则正文。

## 平台来源优先级

1. 正式人设优先使用本次人设查询结果中的 `mediaType/platform` 原值。
2. 正式字段为空时，才从 `styleGuide` 的 `## <平台> 平台适配建议` 标题提取平台。
3. 临时人设使用其平台适配章节；仍无章节时，使用用户本次明确指定的平台。
4. 正式 `mediaType/platform` 与 `styleGuide` 平台标题冲突时，以结构化字段为准并记录冲突；`styleGuide` 是内容兼容来源，不作为第二份权威数据源。

## 唯一映射

| 规范平台   | 可识别值                                                                   | 唯一规则文件                       |
| ---------- | -------------------------------------------------------------------------- | ---------------------------------- |
| `抖音`     | `douyin`、`抖音`                                                           | `references/platforms/douyin.md`   |
| `视频号`   | `video_channel`、`wechat_video`、`wechat_channels`、`视频号`、`微信视频号` | `references/platforms/wechat.md`   |
| `TikTok`   | `tiktok`、`TikTok`                                                         | `references/platforms/tiktok.md`   |
| `YouTube`  | `youtube`、`YouTube`                                                       | `references/platforms/youtube.md`  |
| `LinkedIn` | `linkedin`、`LinkedIn`                                                     | `references/platforms/linkedin.md` |

英文代码忽略大小写；中文展示名按完整值匹配。抖音与 TikTok 不共享任何别名。

## 读取契约

1. 解析出平台后，单次只读取一份平台规则，并记录已加载的规范平台与文件路径。
2. 五个平台命中映射后，规则文件缺失、为空或无法完整读取时立即停止生成正文；不允许跨平台兜底，也不得退化为不带平台规则的生成。
3. 不能识别但属于历史非本期平台的人设沿用旧工作流，不加载本目录的平台规则，也不因本期规则路由而阻断。
4. 将同一个已解析平台继续传给 `siluzan-cso workflow load-libraries --platform`；不得在三库阶段重新推断或切换平台。

## 与三库的关系

平台规则与三库是两个独立输入：

- 平台规则给出合规边界、输出形态和平台默认建议。
- 三库提供流量机制、产品素材组织方式和可选创作结构。
- 三库策略只能在平台规则边界内使用；平台硬约束不可被三库建议覆盖。
- 成稿同时按平台规则和现有 `siluzan-cso workflow validate` 进行自检。

任务：生成视频号脚本

输入变量：
- 主题：{{topic}}
- 行业：{{industry}}
- 目标人群：{{targetAudience}}
- 风格：{{style}}
- 脚本结构：{{scriptStructure}}
- 输出包配置：{{outputProfile}}
- 输出字段：{{outputFields}}
- 时长：{{duration}} 秒
- 平台：{{platform}}
- 是否需要镜头建议：{{includeShotList}}
- 是否需要发布文案：{{includePublishCaption}}
- 是否需要评论引导：{{includeCommentCTA}}

必须输出以下结构：
- positioning
- titles
- hook
- script
- shotList
- coverText
- publishCaption
- commentCTA

脚本结构要求：
1. 开头冲突或反常识钩子
2. 问题展开
3. 核心观点（只能 1 个）
4. 解决方案（2-3 点）
5. 结尾引导

优先按 `scriptStructuresConfig[scriptStructure]` 对应规则执行；如果调用方没有指定，则使用默认五段式。
输出字段优先按 `scriptOutputProfilesConfig[outputProfile]` 执行，再结合当前 include 开关裁剪。

要求：
- 口语化
- 短句
- 可直接读
- 像真人而不是像模板

{{outputRequirement}}

# Style Catalog

这个文件只用于内容类型判断和风格选择。用户确认风格后，再加载对应的 `references/prompt_result/<内容类型>/<风格>.md`。

向用户介绍风格时，只用“简述”和“适合”两类信息，并给出推荐。不要展示完整元提示词。

## 数据图表

用于数字、KPI、百分比、趋势、对比、分布、预算占比、进度、调查结果和数据支撑的结论。

默认推荐 `WebUI_Clean_Modern`；想要强传播感选 `Isometric_Creative`；想要克制研究感选 `Ink_Minimal`。

### WebUI_Clean_Modern
风格文件：`references/prompt_result/数据图表/WebUI_Clean_Modern.md`
简述：白底或浅灰底、现代 SaaS / pitch deck 气质，用大标题、大数字、圆角柱状图、进度条和 KPI 卡片做出干净、矢量、留白充足的数据页。
适合：KPI、增长率、转化率、收入成本、年份对比、预算占比、项目进度、业务汇报。

### Isometric_Creative
风格文件：`references/prompt_result/数据图表/Isometric_Creative.md`
简述：把数据转译成 2.5D 微缩景观，用立体数字、平台、塔柱、方块和小比例人物制造高级商业报告和数据新闻感。
适合：百分比、排名、分布、趋势、阶段占比，以及需要更强传播感和视觉记忆点的数据洞察。

### Ink_Minimal
风格文件：`references/prompt_result/数据图表/Ink_Minimal.md`
简述：黑白灰墨线风，像印刷技术报告或纸面控制面板，用细线、hatch、进度条、分段条和克制排版表达数据。
适合：百分比、进度、完成率、目标达成率、调查结果、状态分布、运营指标、系统健康度。

## 流程图

用于步骤、工作流、SOP、用户旅程、服务交付、Agent 执行链路、审核流程和从开始到完成的顺序。

默认推荐 `WebUI_Clean_Modern`；友好教程选 `Notion_Handdrawn`；严肃 SOP 选 `Ink_Minimal`；视觉旅程选 `Isometric_Creative`。

### WebUI_Clean_Modern
风格文件：`references/prompt_result/流程图/WebUI_Clean_Modern.md`
简述：现代 Web UI / SaaS 流程页风格，用圆角步骤卡、连接箭头、浅网格、蓝紫强调色和严格对齐表现清晰路径。
适合：SaaS onboarding、AI 工作流、产品操作步骤、业务 SOP、官网 how-it-works、产品文档流程。

### Notion_Handdrawn
风格文件：`references/prompt_result/流程图/Notion_Handdrawn.md`
简述：Notion 式黑白手绘线稿，用轻量分镜、水平步骤或多 panel 排版表现动作流程，留白大、亲和、易读。
适合：3-5 步服务流程、产品流程、用户旅程、轻教程、生活方式说明、友好型文章配图。

### Ink_Minimal
风格文件：`references/prompt_result/流程图/Ink_Minimal.md`
简述：黑白墨线 SOP 图，用编号节点、流程轨道、细箭头、边框框体和纸面质感表现严谨、克制的执行链路。
适合：SOP、审核流程、Agent 执行链路、操作顺序、技术手册式流程、低装饰业务链路。

### Isometric_Creative
风格文件：`references/prompt_result/流程图/Isometric_Creative.md`
简述：2.5D 微缩工作流景观，把每一步变成一个立体小站点，用路径、桥、轨道或箭头串起流程。
适合：3-6 步线性流程、内容生产链路、服务交付、产品 onboarding、能转成具体动作场景的流程。

## 概念解释

用于概念、术语、框架、模型、方法论、观点、功能模块或一组相关想法的解释。

默认推荐 `WebUI_Cards`；严肃框架、研究笔记、课程讲义选 `Ink_Minimal`。

### WebUI_Cards
风格文件：`references/prompt_result/概念解释/WebUI_Cards.md`
简述：渐变 Web UI 概念卡片风，用白色圆角卡、柔和光晕、微型界面图案和现代 SaaS 字体解释概念或功能模块。
适合：单个概念、3-6 个相关概念、AI 能力、SaaS 功能模块、产品说明、现代知识卡片。

### Ink_Minimal
风格文件：`references/prompt_result/概念解释/Ink_Minimal.md`
简述：黑白墨线概念卡片风，用薄边框卡片、标签、索引编号、线性图标和纸面留白表达框架、术语和模型。
适合：单个术语、方法论、框架模型、2-5 个相关概念、课程讲义、研究笔记、严肃知识解释。

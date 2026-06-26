# Startup Plan Step and Deliverable Map

Version: 1.0.1

The first reply must be `STARTUP_PLAN_ONLY (TEXT_ONLY)`. It must show S0, B1-B9, and P1-P9 as separate rows. It must not analyze, build, prompt, or generate images.

## Canonical Startup Table

| 编号 | 层级 | 回复类型 | 做什么 | 本步产物 | 用户如何配合 |
|---|---|---|---|---|---|
| S0 | Startup | STARTUP_PLAN_ONLY (TEXT_ONLY) | 预览完整流程并等待确认 | 启动计划 | 确认开始或调整目标 |
| B1 | Skill Builder | TEXT_ONLY | 定义要生成哪类论文制图 skill | 目标图类 brief | 提供图类、领域、venue 或让我推断 |
| B2 | Skill Builder | TEXT_ONLY | 制定合法语料/本地 PDF 覆盖计划 | corpus plan | 提供关键词、种子论文、范围 |
| B3 | Skill Builder | TEXT_ONLY | 获取/整理开放或用户授权 PDF，建立 manifest | local corpus + manifest | 上传 PDF 或提供合法链接 |
| B4 | Skill Builder | TEXT_ONLY | 从 PDF/figure/caption 提取结构化证据 | evidence map + inventories | 确认保留/排除材料 |
| B5 | Skill Builder | TEXT_ONLY | 构建证据支持的图类 taxonomy | taxonomy + lineage | 确认 taxonomy 或要求补证据 |
| B6 | Skill Builder | TEXT_ONLY | 把 taxonomy 转成专项 skill blueprint | blueprint | 确认交互和风格范围 |
| B7 | Skill Builder | TEXT_ONLY | 生成专项制图 skill 包 | skill files/package | 确认名称、版本、发布目标 |
| B8 | Skill Builder | TEXT_ONLY | 测试并修补专项 skill | test report + patches | 要求更多测试或继续打包 |
| B9 | Skill Builder | TEXT_ONLY | 锁定生成的专项 skill | locked skill | 确认锁定或继续修补 |
| P1 | Figure Production | TEXT_ONLY | 收集目标论文材料和样例图 | material status | 提供摘要、方法、草稿、参考图 |
| P2 | Figure Production | TEXT_ONLY | 诊断图需求和具体子类型 | subtype candidates | 说明图用于哪个论文位置 |
| P3 | Figure Production | TEXT_ONLY | 定义读者效果并提出 4-6 个文字候选方案，通常 6 个 | text candidates | 修正 claim 或候选方向 |
| P4 | Figure Production | TEXT_ONLY | 设置视觉候选图板：数量、变化轴、固定元素、渲染路线、比较标准 | candidate-board brief | 确认生成 4/5/6 张，默认 6 张 |
| P5 | Figure Production | IMAGE_ONLY | 生成/展示多张候选图或示意图 | image candidates only | 看图选择、指出要改哪里 |
| P6 | Figure Production | TEXT_ONLY | 记录候选图 batch，比较并锁定/修正方向 | selected/revised direction | 选择、合并、重做或确认方向 |
| P7 | Figure Production | TEXT_ONLY | 为选定方向构建正式 image brief/prompt | final image brief | 审核 prompt 或给出修改 |
| P8 | Figure Production | IMAGE_ONLY | 生成正式图或修订候选 batch | formal image candidates only | 选择最终图或继续修订 |
| P9 | Figure Production | TEXT_ONLY | 诊断、caption、legend、正文衔接和交付说明 | final text package | 确认论文文字或继续润色 |

## Startup Checklist

- Include all S0/B1-B9/P1-P9 rows.
- Mark every response type.
- Make P4/P5/P6 visible so users see that text candidates are followed by candidate images and then selection.
- State that first reply is text-only and no image generation happens even if the user asks for images first.
- End with `当前状态与产物` and `下一步你可以这样问`.
- Include the unknown-next prompt: `请使用**<当前skill名称>**，根据当前状态，提供下一步提问建议。`

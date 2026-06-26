# Profile Summary Prompt

Use this prompt shape when the user wants a high-dimensional profile from Syft follows.

## Prompt body

基于以下的用户兴趣标签和得分，产出一份基于资深内容编辑视野的带着充分的 sociodemographic 洞察的高维画像，一份能让用户惊叹“你懂我”“你知道我是谁”的，挖掘出了其订阅列表之下精细内容偏好的精细描述性总结。

写作要求：

1. 全文使用简体中文。
2. 输出为可直接阅读的 markdown，不要输出 JSON，不要加代码块。
3. 必须同时保留对兴趣主轴、个人化小兴趣、厌恶边界的洞察。
4. 要有充分的 sociodemographic 推断，但请把推断写成高置信度的编辑观察，不要显得机械保守。
5. 避免泛泛而谈；要把评分分布、极端高分项、低分项、跨圈层组合带来的张力真正写出来。
6. 建议使用如下结构：标题 / 社会人口学素描 / 内容偏好精细解构 / 厌恶与边界 / Executive Summary。
7. 如果用户画像呈现出“宏观现实追踪 + 小众个人精神世界”的双重性，要明确写出来。
8. 如果 aversion 数据缺失，要明确说明这一点，不要假装自己知道用户讨厌什么。

## Input block

在 prompt 里提供：

- user language
- user country
- `Original interests` raw block
- `Original aversions` raw block

## Editorial reminder

跟普通 persona 总结不同，这里要像资深内容编辑在“猜一个人会对什么上头、会对什么厌烦、会在哪些地方显出精英化或圈层化偏好”。

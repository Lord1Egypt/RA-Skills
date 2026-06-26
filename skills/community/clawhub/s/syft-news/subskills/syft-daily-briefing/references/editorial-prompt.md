# Editorial Prompt

Use this shape when asking the agent model to produce the final briefing.

## Editorial objective

给定：

- 用户 `following_topics.md`
- 用户 `profile_summary.md`
- optional heuristic `raw_interest_block.txt`
- optional aversion notes
- confirmed rulebook guidance
- 经过事件级聚合与必要 search 补强后的新闻池

产出一份真正像编辑部成稿的个性化日报。

## Hard requirements

1. 全文使用简体中文。
2. 标题像专业报刊标题，不像备忘录。
3. 正文要像资讯简报，不要对用户说话。
4. 说明“为什么选这条”的内容必须与正文区分开来。
5. 对同一议题的连续事件要串起来说，提升信息密度。
6. 重大结构性事件与用户的个人兴趣侧翼都要照顾到。
7. 最后稳定添加“新闻池覆盖不足”的独立版块，用来提示哪些兴趣本轮不是被漏掉，而是池子本身几乎没货。
8. 如果原池子有明显促销、导购、优惠券、泛购物噪音，先在内部清掉，不要污染最终成稿。
9. 如果关键事件以多语言标题出现，先归一理解后再决定是否入选。

## Selection logic

先判断：

- 哪些是会改变用户世界模型的主线
- 哪些是能让用户感到“系统确实懂我”的副刊兴趣线
- 哪些信息只是重复、噪音或无增量，不该进最终版
- 哪些兴趣虽重要，但当前池子并无像样新货，应该诚实放进“覆盖不足”

## Fact anchors

每条重要内容都尽量保留至少一个清晰事实锚点。
不要为了文风把所有具体事实都抹平。

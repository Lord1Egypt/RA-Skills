# 智能创作手册

这个文件专门说明这个 Skill 的“智能创作层”应该怎么工作。

推荐先配合下面这条命令准备创作资产：

```bash
python scripts/publish_wechat.py create "<标题>"
```

如果用户只给了一句话需求，也可以直接这样：

```bash
python scripts/publish_wechat.py create "<标题>" --request "<用户一句话需求>"
```

准备好创作资产后，可以继续直接生成初稿：

```bash
python scripts/publish_wechat.py write <创作资产目录>
```

如果想把创作、初稿和预览一次跑完，也可以直接使用：

```bash
python scripts/publish_wechat.py workflow "<标题>" --request "<用户一句话需求>" --dry-run
```

同时参考这些模板文件：

- [templates/prompts/title_to_article.md](C:\Users\tntwl\Desktop\wechat-article-publisher-1.0.0\templates\prompts\title_to_article.md)
- [templates/prompts/rewrite.md](C:\Users\tntwl\Desktop\wechat-article-publisher-1.0.0\templates\prompts\rewrite.md)
- [templates/examples/good_wechat_article.md](C:\Users\tntwl\Desktop\wechat-article-publisher-1.0.0\templates\examples\good_wechat_article.md)
- [templates/conversation/final_article_contract.md](C:\Users\tntwl\Desktop\wechat-article-publisher-1.0.0\templates\conversation\final_article_contract.md)

## 一、创作模式

### 1. 基于标题直接创作

适用场景：

- 用户只给了一个标题
- 用户给了主题和读者，但没有现成正文
- 用户希望直接得到一篇可发布的公众号文章

输出目标：

- 中文 Markdown
- 正文 1200-1500 字
- 适合公众号阅读
- 可直接进入草稿创建流程

执行顺序：

1. 判断这篇文章最适合写给谁
2. 确定传播角度，不要只复述标题
3. 拆成 3-5 个二级小标题
4. 先写导语，再按小标题写正文
5. 最后写结尾，收束并强化判断

### 2. 基于参考文章改写

适用场景：

- 用户给了 `mp.weixin.qq.com` 链接
- 用户给了外部文章链接
- 用户给了本地 Markdown
- 用户说“参考这篇文章改一版”

输出目标：

- 保留核心事实和信息边界
- 重新组织结构
- 换一套公众号表达方式
- 输出 1200-1500 字 Markdown

执行顺序：

1. 先提取原文
2. 列出原文核心观点
3. 列出必须保留的事实
4. 重写标题、导语和段落结构
5. 补上原文没讲透的解释或场景
6. 完成后做结构和字数检查

## 二、默认结构

建议始终优先采用下面的结构：

```md
# 标题

导语：说明这篇文章为什么值得读。

## 第一部分

观点 + 原因 + 例子

## 第二部分

观点 + 原因 + 例子

## 第三部分

观点 + 原因 + 例子

## 结尾

回扣标题，给出判断、建议或提醒。
```

如果主题复杂，可以扩展到 4-5 个二级标题，但不建议更多。

## 三、文风要求

默认文风是“专业但不端着”：

- 段落不要太长
- 每一段都要有信息量
- 可以有判断，但不要悬浮
- 尽量给场景、例子、对比，而不是只讲概念

尽量避免这些表达：

- 在这个快速发展的时代
- 总之
- 综上所述
- 首先我们来看看
- 让我们一起来看

## 四、长度控制

推荐做法：

- 导语控制在 80-120 字
- 每个二级小节控制在 250-350 字
- 结尾控制在 80-150 字

这样整体更容易落在 1200-1500 字区间内。

## 五、改写时的信息边界

改写不是洗稿式替换词汇，而是重新表达。

必须保留：

- 关键事实
- 数据结论
- 时间、人物、组织等核心信息

必须重写：

- 原文标题
- 原文导语
- 原文段落顺序
- 原文叙述方式

## 六、自检清单

出稿前至少检查这些：

- 标题是否清楚、有切口
- 导语是否让人愿意继续读
- 二级标题是否推动文章前进
- 是否有重复表达
- 是否有空话套话
- 是否存在事实失真
- 字数是否在目标区间附近

## 七、代码支撑

底层辅助模块在这里：

- [scripts/wechat_skill/creation.py](C:\Users\tntwl\Desktop\wechat-article-publisher-1.0.0\scripts\wechat_skill\creation.py)

可以复用的能力：

- 生成创作任务说明
- 生成文章骨架
- 检查字数和结构

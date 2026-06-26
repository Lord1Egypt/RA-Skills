---
name: wechat-official-account-article-auto-publisher
description: 智能创作、提取微信公众号文章、生成封面并发布到微信公众号草稿箱。适用于“按标题直接写稿”“参考文章改写”“提取 mp.weixin 链接”“创建草稿并发布”的完整工作流。
---

# WeChat Official Account Article Auto Publisher

## 这个 Skill 现在负责什么

这个 Skill 分成两层：

1. Skill 编排层
   - 负责智能创作
   - 负责基于参考文章改写
   - 负责把最终正文控制在 1200-1500 字
   - 负责决定是先提取、先改写、还是直接发草稿
2. Python 工具层
   - 负责创作提示准备与质量自检
   - 负责文章提取
   - 负责 Markdown / HTML 转换
   - 负责封面生成
   - 负责素材上传
   - 负责创建公众号草稿
   - 负责发布和查询发布状态

## 触发场景

当用户提出以下任一需求时，应使用本 Skill：

- 基于一个标题直接写一篇 1200-1500 字的公众号文章
- 基于一篇参考文章进行改写，输出适合公众号的版本
- 从 `mp.weixin.qq.com` 链接提取正文并转成 Markdown
- 为文章自动生成封面
- 创建公众号草稿
- 发布草稿到公众号
- 上传图片等素材到微信服务器

## 使用前准备

用户只需要配置两类信息：

1. 微信公众号凭证
   - `wechat.app_id`
   - `wechat.app_secret`
2. 图像生成 API
   - 默认支持豆包
   - 也支持通义千问

可选配置：

- `wechat.author`
- `wechat.default_template`
- `image_generation.provider`
- `workspace.output_dir`

配置文件路径：

- [config.json](C:\Users\tntwl\Desktop\wechat-article-publisher-1.0.0\config.json)

## 智能创作规则

这一层现在不只是“会写”，而是要遵循一套固定创作协议。

### 基于标题直接创作

如果用户只给标题，Skill 应直接完成写作，不要先把任务推给用户手动整理。

要求：

- 输出中文 Markdown
- 正文目标字数 1200-1500 字
- 标题、导语、小标题、正文、结尾完整
- 适合公众号阅读节奏
- 避免空泛套话
- 默认写成可直接发布版本

默认结构：

1. 标题
2. 导语
3. 3-5 个二级小标题
4. 结尾总结

默认节奏：

- 开头 2-3 句迅速交代问题和价值
- 每个二级小节都先讲观点，再讲原因，再给例子或场景
- 结尾不复述全文，要给一个更强的判断、提醒或行动建议

默认文风：

- 信息密度高
- 句子偏短，适合手机阅读
- 有观点，但不故作煽动
- 不写“正确的废话”

### 基于参考文章改写

如果用户给的是文章链接、Markdown 或提取后的内容，Skill 应：

1. 先提取或读取原文
2. 理解原文核心观点
3. 用新的公众号表达方式重写
4. 保持信息准确，不照抄大段原文
5. 输出 1200-1500 字左右 Markdown

如果参考文章是 `mp.weixin.qq.com` 链接，优先先执行提取命令，再进行改写。

改写时的默认动作：

1. 先归纳原文的核心事实、核心观点、核心结论
2. 再判断哪些信息必须保留，哪些表达必须重写
3. 换一套标题、导语和段落组织方式
4. 补足原文没有讲透的上下文、案例或解释
5. 最终文章不能只是“换同义词”，而要有新的叙述组织

改写时必须避免：

- 大段照抄原文句子
- 原文逻辑混乱却原样继承
- 为了凑字数重复一个观点
- 明明是事实信息却被改写失真

### 创作产物准备

如果用户要写新稿或改写旧稿，优先先准备创作资产：

- `python scripts/publish_wechat.py create "<标题>"`
- `python scripts/publish_wechat.py create "<标题>" --request "<用户一句话需求>"`

这条命令会生成：

- `brief.json`
- `prompt.md`
- `outline.md`
- `guide.md`

如果已经有初稿，还可以追加：

- `python scripts/publish_wechat.py create "<标题>" --article-file <markdown文件>`

这样会额外生成质量检查结果 `check.json`。

在创作资产准备好之后，可以直接生成初稿：

- `python scripts/publish_wechat.py write <创作资产目录>`

这条命令会生成：

- `article.md`
- `generated_check.json`

如果希望把“一句话需求 -> 初稿 -> 预览 -> 草稿”一次跑完，可以直接使用：

- `python scripts/publish_wechat.py workflow "<标题>" --request "<用户一句话需求>"`

这条命令会在一个目录里生成：

- `brief.json`
- `prompt.md`
- `outline.md`
- `article.md`
- `generated_check.json`
- `preview_html`

如果没有加 `--dry-run`，并且微信公众号与图像接口都已配置，还会继续创建公众号草稿。

## 默认创作协议

无论是直接创作还是改写，默认都按下面的顺序执行：

1. 明确读者
   - 先判断文章是写给谁看的，例如创业者、产品经理、运营、普通职场人
2. 确定切入角度
   - 不直接铺陈主题，要找一个最有传播力的切口
3. 先搭骨架
   - 先想出导语和 3-5 个二级标题，再填充正文
4. 控字数
   - 目标正文 1200-1500 字，不追求冗长
5. 自检
   - 检查观点是否清楚、段落是否顺、有没有套话和废话

建议优先配合这些模板资产使用：

- [templates/prompts/title_to_article.md](C:\Users\tntwl\Desktop\wechat-article-publisher-1.0.0\templates\prompts\title_to_article.md)
- [templates/prompts/rewrite.md](C:\Users\tntwl\Desktop\wechat-article-publisher-1.0.0\templates\prompts\rewrite.md)
- [templates/examples/good_wechat_article.md](C:\Users\tntwl\Desktop\wechat-article-publisher-1.0.0\templates\examples\good_wechat_article.md)
- [templates/conversation/system_prompt.md](C:\Users\tntwl\Desktop\wechat-article-publisher-1.0.0\templates\conversation\system_prompt.md)
- [templates/conversation/request_to_brief.md](C:\Users\tntwl\Desktop\wechat-article-publisher-1.0.0\templates\conversation\request_to_brief.md)
- [templates/conversation/publish_checklist.md](C:\Users\tntwl\Desktop\wechat-article-publisher-1.0.0\templates\conversation\publish_checklist.md)
- [templates/conversation/final_article_contract.md](C:\Users\tntwl\Desktop\wechat-article-publisher-1.0.0\templates\conversation\final_article_contract.md)

## 默认输出模板

建议输出成下面这种 Markdown 结构：

```md
# 标题

导语：用 2-3 句话说明这篇文章为什么值得读。

## 小标题 1

先讲观点，再讲原因，再举例或给场景。

## 小标题 2

继续推进文章，不要和上一节重复。

## 小标题 3

把读者最关心的问题讲透。

## 结尾

回扣标题，给一个更明确的判断、建议或提醒。
```

## 质量门槛

智能创作完成后，至少要过下面几条：

- 正文字数尽量在 1200-1500 字
- 至少 3 个二级标题，通常不超过 5 个
- 开头必须有导语，不要直接闷头展开
- 结尾必须有收束，而不是突然结束
- 每个二级小节都应包含“观点 + 解释 + 场景/例子”
- 不要频繁出现“总之”“综上所述”“在这个快速发展的时代”这类套话

## 建议的内部检查

这个 Skill 已经提供了可复用的创作辅助模块：

- [scripts/wechat_skill/creation.py](C:\Users\tntwl\Desktop\wechat-article-publisher-1.0.0\scripts\wechat_skill\creation.py)

其中包含：

- 创作规范 `CreationSpec`
- 创作任务说明生成 `build_creation_prompt`
- 文章骨架模板 `build_outline_template`
- 字数和结构检查 `validate_article`

如果后续要把智能创作进一步脚本化，应优先复用这个模块，而不是重新写一套散乱规则。

另外还配套了模板资产：

- [CREATION_GUIDE.md](C:\Users\tntwl\Desktop\wechat-article-publisher-1.0.0\CREATION_GUIDE.md)
- [templates/prompts/title_to_article.md](C:\Users\tntwl\Desktop\wechat-article-publisher-1.0.0\templates\prompts\title_to_article.md)
- [templates/prompts/rewrite.md](C:\Users\tntwl\Desktop\wechat-article-publisher-1.0.0\templates\prompts\rewrite.md)
- [templates/examples/good_wechat_article.md](C:\Users\tntwl\Desktop\wechat-article-publisher-1.0.0\templates\examples\good_wechat_article.md)
- [templates/conversation/system_prompt.md](C:\Users\tntwl\Desktop\wechat-article-publisher-1.0.0\templates\conversation\system_prompt.md)
- [templates/conversation/request_to_brief.md](C:\Users\tntwl\Desktop\wechat-article-publisher-1.0.0\templates\conversation\request_to_brief.md)
- [templates/conversation/publish_checklist.md](C:\Users\tntwl\Desktop\wechat-article-publisher-1.0.0\templates\conversation\publish_checklist.md)
- [templates/conversation/final_article_contract.md](C:\Users\tntwl\Desktop\wechat-article-publisher-1.0.0\templates\conversation\final_article_contract.md)

## 推荐工作流

### 场景 1：按标题写稿并发草稿

1. 最简单的方式，直接执行：
   - `python scripts/publish_wechat.py workflow "<标题>" --request "<用户一句话需求>" --dry-run`
2. 检查生成的初稿和预览
3. 去掉 `--dry-run` 后再次执行，即可继续创建草稿

### 场景 2：基于公众号链接改写并发草稿

1. 直接执行：
   - `python scripts/publish_wechat.py workflow "<新标题>" --mode rewrite --source-url <mp.weixin链接> --request "<改写要求>" --dry-run`
2. 检查初稿和预览
3. 去掉 `--dry-run` 后再次执行，即可继续创建草稿

### 场景 3：创建草稿后直接发布

- `python scripts/publish_wechat.py draft <输入> --publish --status`

### 场景 4：只上传素材

- `python scripts/publish_wechat.py material <文件路径> --type image`

## CLI 命令

主脚本：

- [scripts/publish_wechat.py](C:\Users\tntwl\Desktop\wechat-article-publisher-1.0.0\scripts\publish_wechat.py)

支持的子命令：

- `install`
  - 安装依赖
- `create`
  - 生成创作 brief、prompt、outline 和质量检查
- `write`
  - 基于创作资产生成 `article.md` 并自动质检
- `workflow`
  - 一条命令完成 create、write、preview，并按需创建草稿
- `extract`
  - 从 URL 或本地 Markdown 提取并输出 Markdown
- `cover`
  - 生成封面图
- `material`
  - 上传素材到微信服务器
- `draft`
  - 创建草稿，支持直接提交发布
- `publish`
  - 发布已有草稿 `media_id`

## 关键命令示例

安装依赖：

```bash
python scripts/publish_wechat.py install
```

准备标题创作资产：

```bash
python scripts/publish_wechat.py create "AI 产品经理的第二曲线"
```

基于一句话需求自动推断创作 brief：

```bash
python scripts/publish_wechat.py create "AI 产品经理的第二曲线" --request "写给产品经理，分析 AI 为什么会先压缩中间层价值，并给出转型建议"
```

准备改写资产并校验初稿：

```bash
python scripts/publish_wechat.py create "AI 产品经理的第二曲线" --mode rewrite --source-file article.md --article-file draft.md
```

基于创作资产生成初稿：

```bash
python scripts/publish_wechat.py write outputs/ai-产品经理的第二曲线-creation
```

一条命令完成创作、预览和建草稿前流程：

```bash
python scripts/publish_wechat.py workflow "AI 产品经理的第二曲线" --request "写给产品经理，分析 AI 为什么会先压缩中间层价值，并给出转型建议" --dry-run
```

提取公众号文章到 Markdown：

```bash
python scripts/publish_wechat.py extract "https://mp.weixin.qq.com/s/xxxxx"
```

生成封面：

```bash
python scripts/publish_wechat.py cover "AI 产品经理的第二曲线" --template insight
```

创建草稿：

```bash
python scripts/publish_wechat.py draft article.md --template business
```

创建草稿并直接发布：

```bash
python scripts/publish_wechat.py draft article.md --publish --status
```

发布已有草稿：

```bash
python scripts/publish_wechat.py publish <media_id> --status
```

## 输出约定

所有命令标准输出 JSON。

常见字段：

- `success`
- `title`
- `markdown_path`
- `preview_html`
- `cover_path`
- `draft_media_id`
- `publish_id`
- `status`
- `article_path`
- `check_path`
- `brief_path`
- `prompt_path`
- `outline_path`

## 执行约束

- 先满足用户内容目标，再执行发布动作
- 没有明确要求发布时，优先只创建草稿
- 用户给链接时，不要求用户先自己提取，Skill 应主动完成
- 创作或改写完成后，正文应尽量控制在 1200-1500 字
- 如图像接口未配置，不要伪造封面结果，应明确报错

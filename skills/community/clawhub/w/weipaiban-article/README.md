# weipaiban-article

微排版公众号文章排版：把主题或稿件排成可直接发布的微信公众号文章。正文可以滚动阅读，套用主题配色；章节可以配插画式主图，也可以插入轮播图集、横向滑动、点击切换和点击弹窗。同一类交互可以重复，几类也可以出现在同一篇里。

图片默认从微排版 AI 素材库按一个 tag 取全量已发布图，再分配到场景、透明贴纸和可选的循环背景。用户可以改为提供图片，或点名自己的生图技能。需要入库时用技能自带的 `scripts/upload_images.py`，不另装上传技能。tag 没有图时，图片槽位只用占位图。

入口与工作流见 [SKILL.md](SKILL.md)。

## 获取密钥

取素材、上传图片和发布作品都要读取环境变量 `WEIPAIBAN_API_KEY`。

1. 登录 [微排版](https://weipaiban.cn)。
2. 打开 [API 密钥](https://weipaiban.cn/settings/api-keys)，创建或复制一把以 `sk-` 开头的密钥。
3. 把它设到当前环境，例如：`export WEIPAIBAN_API_KEY=sk-...`

密钥只放在环境变量里。不要贴进对话，也不要写进作品或任务文件。

## 开源与署名

源码仓库：[https://github.com/21epub/weipaiban-article-skill](https://github.com/21epub/weipaiban-article-skill)

本仓库在 [21epub/gzh-design-skill](https://github.com/21epub/gzh-design-skill) 的基础上修改。后续主题与排版约定以这个仓库为准。它是 [gzh-design-skill](https://github.com/isjiamu/gzh-design-skill) 的 fork，许可证同为 [GNU AGPL-3.0](LICENSE)，原作版权声明仍然有效。

- 原作版权：Copyright (C) 2026 甲木 (Jiamu) × 摸鱼小李 (Moyu Xiaoli)
- 21epub 著作权：Copyright (C) 2026 21epub
- 修改部分：2026 年基于 21epub/gzh-design-skill，将公众号主题与排版约定改编为微排版流式文章技能
- 自有内容：对接微排版的技能本身（流式文章结构、微排版方言与组件、发布与素材脚本，以及未取自 gzh-design-skill 的主题与文档）著作权归 21epub

本仓库作为整体以 GNU AGPL-3.0 许可。21epub 对自有内容的著作权不把这些内容改成另一套许可证。完整声明见 [LICENSE](LICENSE)。

## 交流群

使用问题、格式反馈可以进微信群。用微信扫描下面的二维码加入。

![微排版交流群二维码](assets/contact-me-qr.png)

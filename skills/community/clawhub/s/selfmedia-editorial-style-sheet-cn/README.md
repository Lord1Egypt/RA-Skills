# 栏目写作风格手册

把 3 至 5 篇成熟文章中的共性写法变成一份可执行的编辑手册，让同一栏目后续每篇文章在语气、句长、术语和数字写法上保持一致。它不猜账号人设，也不模仿作者的长段表达。

![栏目写作风格手册推广图](assets/promo-1600x900.png)

## 输入与结果

输入是用户自有的 3 至 5 篇成熟稿（合计最多 8,000 字）、目标读者、已批准词表，以及必须保留的表达限制。结果是一份 Markdown 风格手册，包含可复用规范、每条规范的短依据摘录和下一篇写稿核对表。

没有代表稿、只有一句口号，或样稿差异过大时，Skill 会请求用户指定同栏目基准，不会从账号名称编造文风。

## 安装

```bash
npx skills add xxjrq/selfmedia-editorial-style-sheet-cn
```

## 使用

把稿件按“稿 1 / 稿 2 / 稿 3”标明，并一同提供读者、词表和限制。例如：

```text
目标读者：需要将 AI 工具用于日常工作的内容团队
已批准词表：首次写“人工智能（AI）”；使用“工作流”
必须保留：不承诺效果；数字使用阿拉伯数字加中文单位
稿 1：…
稿 2：…
稿 3：…
```

可复制的完整交付见：[成功输入](fixtures/success-input.md) 与 [成功输出](fixtures/success-output.md)。缺料分支见：[失败输入](fixtures/failure-input.md) 与 [失败输出](fixtures/failure-output.md)。

## 范围

仅固化文章表达规范，不做主页简介、账号定位或选题排期；不用于模仿他人文风，且不会复制作者独有长段。

## 自检

```bash
node scripts/self-test.mjs
```

该检查在仓库内独立运行，验证发布文件、正式名称、图标尺寸，以及可复制的成功与缺料交付。

## 来源与许可证

业务用途参考了 [marketingskills](https://github.com/coreyhaines31/marketingskills) 的公开目录及其 [copy-editing Skill](https://github.com/coreyhaines31/marketingskills/blob/main/skills/copy-editing/SKILL.md)，本仓库的说明、步骤和示例均为原创，未复制其内容或源码。仓库采用 [MIT-0](LICENSE)。

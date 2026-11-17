# 旧内容二次利用清单

![推广图](assets/promo-1600x900.png)

把自己已有的文章、笔记、店铺内容或小说素材，整理成可追溯的更新、拆分、合集清单；不需要追逐、更不需要照搬别人的爆款。

提交每条内容的清单和摘要后，Skill 会交付可复用候选、新角度建议与待补资料。建议和用户已提供的事实会明确分开，适合中文小店经营者、小说作者与自媒体创作者。

## 使用

在支持 Skill 的环境中调用 `$selfmedia-reuse-map-cn`，提供自有内容清单和原文摘要，按 [SKILL.md](SKILL.md) 工作流生成更新、拆分与合集建议。

## 输入

每条内容需要 `id`、`title`、`published_at`、`platform`、`summary`；可选补充 `audience_signal` 等用户已有观察。[成功样例](fixtures/success.json)同时包含完整的自有内容输入与预期 Markdown 交付。

若缺少关键字段，Skill 会列出缺口而不编造，并停止对该条目的建议，参见[失败样例](fixtures/failure-missing-summary.json)。

## 结果

- 可**更新**、**拆分**、**合集**的候选项；
- 每项对应的输入资料依据；
- 与已知事实分开的推断建议；
- 待补资料及人工确认项。

## 自测

```bash
./scripts/self-test.sh
```

自测区分包结构与样例语义：前者检查字段和视觉素材尺寸，后者核对更新/拆分/合集的资料依据、推断标记及缺字段停止规则；未设置虚假的业务引擎。真实行为应按 [SKILL.md](SKILL.md) 工作流套用到用户自有内容库。

## 使用边界与来源

仅处理用户提供或拥有的内容，不抓取、复述或模仿对标作品。公开参考仅为 [social-media-skills/skills](https://github.com/social-media-skills/skills) 的用途核对；本仓库中文流程与样例均为原创。许可证见 [MIT-0](LICENSE)。

## 安装

```bash
npx skills add xxjrq/selfmedia-reuse-map-cn
```

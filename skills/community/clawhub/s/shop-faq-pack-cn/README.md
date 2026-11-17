# 店铺FAQ知识库

![店铺FAQ知识库推广图](assets/promo-1600x900.png)

把已批准的运费、配送时效、售后和商品规格政策，整理成可长期复用的中文 FAQ；缺少依据时会明确列出需补充字段，不擅自作出对顾客的承诺。

## 适用场景

中文小店经营者、小说作者与自媒体创作者，可将输出用于商品页、客服知识库或周边销售说明。此 Skill 只生成 Markdown 内容，不接入聊天工具，也不会代客服自动发送回复。

## 输入与结果

输入一份已批准、可对外使用的政策资料，至少含：运费与包邮条件、发货与配送时效、售后与退款规则、商品规格与选项。精确的地区、金额、天数及限制条件应保留原值。

结果是一份按“下单与运费、发货与配送、售后与退款、商品规格”分类的标准问答，并附每条问答的政策依据及“需商家补充”清单。资料不足时，Skill 会指出无法可靠回答的问题，而不是编造答案。

## 最小示例

[完整成功输入](fixtures/success.json)与[对应输出](fixtures/success-output.md)使用明确虚构的离线测试商家，模拟一份已批准政策，覆盖运费、发货时效、退货与换货条件及双方运费责任、退款方式和商品规格；每条回答标注对应字段原文。它只验证样例合同，不代表任何现实商户授权或真实政策。

[此前未批准输入](fixtures/partial-unapproved-input.json)与[部分整理输出](fixtures/partial-unapproved-output.md)保留原始事实；因未提供批准状态及换货规则，只能作为草稿并列出缺项。

[缺料政策输入](fixtures/failure-missing-fields.json)与[缺料交付样例](fixtures/failure-output.md)说明：只有“部分商品包邮”“尽快发货”“支持售后”时，批准状态、运费、时效、退换货条件与运费、退款方式及规格都应列为缺口，不能自行写包邮门槛、48小时或7天退货。

此前运行记录只证明按该输入整理出一份待确认草稿，不证明政策真实或已获批准。[部分整理前向记录](fixtures/forward-success.md)和[缺料前向记录](fixtures/forward-failure.md)可独立查看。

## 使用

将政策原文或结构化字段交给 Skill，并要求按 `SKILL.md` 的输出格式整理。发布前由商家复核政策是否仍有效；涉及平台规则、法规或纠纷处理的内容尤其应以商家最终确认版本为准。

## 自测

在本仓库根目录运行：

```bash
python3 scripts/self_test.py
```

该命令检查真实成功、partial 与缺料 fixture 的字段、逐条政策引用、缺失字段合同及图片尺寸；不会虚构客服引擎行为，也不证明任何现实商家的授权或政策真实性。

## 来源与许可

本仓库为原创中文说明与示例，仅参考 [marketingskills 的 sales-enablement Skill](https://github.com/coreyhaines31/marketingskills/blob/main/skills/sales-enablement/SKILL.md) 的公开用途定位；未复制其源码或文案。图标与推广视觉为本仓库原创生成素材。代码与文档采用 [MIT-0](LICENSE) 许可。

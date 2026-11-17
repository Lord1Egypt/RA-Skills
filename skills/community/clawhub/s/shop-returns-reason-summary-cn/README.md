# 售后原因汇总与商品改进

![售后原因汇总与商品改进推广图](assets/promo-1600x900.png)

把脱敏的退款、退货原因和商品信息汇总为可复核的计数，并形成清楚、可验证的商品页改进方向。

适合中文小店经营者、小说作者及自媒体创作者复盘已有售后反馈。它不会臆测缺失数据，也不会替代财务判断或客服回复。

## 使用

向 Skill 提供 JSON、CSV、表格或清单。每条至少应有商品名称（或商品 ID）和退款/退货原因；订单号、日期、规格及补充说明可选但有助于核对。

你会得到：

- 原始原因文本可追溯的分类；
- 分类和商品维度的可核算计数；
- 与已知事实明确分离的商品页改进建议；
- 缺失字段、排除项和待确认项。

## 示例

成功样例见 [fixtures/success.json](fixtures/success.json)：`input_records` 是脱敏输入，`expected_workflow_output` 给出了完整的原因分类、计数守恒、商品维度事实和与事实分开的建议。失败样例见 [fixtures/failure-missing-reason.json](fixtures/failure-missing-reason.json)：缺少“原因”时必须明确报错、列出无法完成的部分，不能编造分类。

## 验证

在仓库根目录运行：

```sh
sh scripts/self-test.sh
```

该命令验证发布结构、关键字段、图像尺寸及成功/失败样例契约（含计数守恒与事实/建议分离）；它不是业务引擎，也不伪造真实分类结果。真实分析遵循 [SKILL.md](SKILL.md) 的工作流。

## 来源与许可

实现和中文文案为原创；仅参考 Saleor 的公开仓库作为电商售后领域用途背景，未复制源码或文案：[Saleor](https://github.com/saleor/saleor)（BSD-3-Clause）。本仓库采用 [MIT-0](LICENSE)。

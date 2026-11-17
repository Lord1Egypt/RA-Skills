# 优惠适用条件核对

![优惠适用条件核对推广图](assets/promo-1600x900.png)

把商家已确认的优惠规则和购物清单交给此 Skill，即可得到逐条件的“可用 / 不可用 / 待确认”结果、逐步金额依据，以及只按明确规则计算的应付草稿。它帮助客服、运营避免把缺失的叠加规则或平台口径误当成结论。

输入包括：优惠有效期与时区、门槛及其口径、适用 SKU、叠加顺序、带 SKU 的购物行、运费和当前时间。百分比使用 `percent` 表示应付比例：`90` 是 9 折，`10` 才是应付一成；并要求用户确认 `rounding_mode: "total_half_up_2"` 才执行两位小数的总额舍入。会影响后续部分 SKU 的多行固定或百分比优惠，需要 `allocation_rule: "cart_order"`；后续优惠确定不适用、确定零减免，或中间全范围优惠已确定清空余额时不要求分摊。未确认分摊规则时，相关优惠、整单小计和行级扣减会标为待确认，不猜测购物车顺序。逐步结果会展示适用 SKU、当步余额、公式、舍入规则和行级扣减状态。固定优惠超出余额、或百分比舍入后的减免超过余额时会标为待确认，不静默截断或报计算错误；有效期开始晚于结束时也会标为待确认。任一 SKU 的金额仍未知时，整单应付小计保持待确认。脚本不假设平台的舍入或分摊规则。缺运费时不会按免运费计算应付金额；前序不确定只传递到受影响 SKU。“优惠后商品额”门槛仍会用确定下界核对：门槛为 0，或不高于已知且计入的运费时，门槛条件可确定为可用。它不会查询实时价格、领券、下单或声称最优价。

## 安装

```bash
npx skills add xxjrq/shop-promo-eligibility-check-cn
```

## 使用与验证

```bash
python3 scripts/check_eligibility.py < fixtures/success.json
python3 scripts/self_test.py
```

可复制的输入与实际交付：[成功输入](fixtures/success.json) → [成功交付](fixtures/success-delivery.json)（A 商品满 100 减 20 后 9 折，A 的优惠后金额为 72.00；金额 50 的排除 SKU 不参与优惠，订单草稿为 122.00）；[缺料输入](fixtures/failure.json) → [缺料交付](fixtures/failure-delivery.json)（缺叠加许可、门槛口径、运费口径和优惠值，结果为待确认）。

详细操作边界见 [SKILL.md](SKILL.md)，英文说明见 [README.en.md](README.en.md)。

## 来源与许可

业务用途参考了 [Saleor](https://github.com/saleor/saleor) 的公开折扣领域资料，仅用于核对概念；本仓库说明和实现均为原创，未引入其代码。该参考仓库采用 BSD-3-Clause 许可证。本站代码采用 [MIT-0](LICENSE)。

# 发货拣货装箱单

把脱敏订单资料整理成仓内可执行的 Markdown 拣货/装箱勾选表：逐单该拣什么、已确认套装拆出哪些组件、总共需要多少实物，以及哪些包装资料尚不明确。它只协助人工核对，不连接后台、不扣库存、不建运单，也不代表订单已发货。

![发货拣货装箱单推广图](assets/promo-1600x900.png)

## 输入与结果

输入最多 20 个脱敏订单（不超过 100 条商品/组件行）的 SKU、数量、单位，以及已确认的套装组成、赠品条件和包装规则。赠品门槛需要明确计量单位；同一 SKU 混有箱、个等不同单位时不会相加或猜换算。结果中的“拆套后组件汇总”仅包含套装组件，普通商品和赠品仍保留在订单清单中。缺单位、套装组成或赠品适用条件时，只会列出缺项；不会猜附件、赠品或包裹数量。

## 安装

```bash
npx skills add xxjrq/shop-packing-picklist-cn
```

## 快速验证

仓库提供可直接运行的保守参考实现和两份可复制验收样例：

- [成功输入](fixtures/success-input.json) → [预期交付](fixtures/success-expected.md)：2 套分别拆为 4 个杯子、2 把刷子；赠品门槛为 3 套，因此不加赠。
- [缺料输入](fixtures/failure-input.json) → [预期交付](fixtures/failure-expected.md)：礼盒没有已确认组成，停止拆套并提示补料。

```bash
sh scripts/self-test.sh
python3 scripts/generate_picklist.py fixtures/success-input.json
```

## 使用边界

仅处理当次订单应拣与应装的实物数量，适合发货前的人工复核。它不做异常单审核、采购补货或库存缺口判断。

## 来源与许可

业务用途参考 [ERPNext Packing Slip](https://github.com/frappe/erpnext/blob/develop/erpnext/stock/doctype/packing_slip/packing_slip.json) 的公开页面；本 Skill 的说明、样例和实现均为原创，未复制其文本或源码。仓库采用 [MIT-0](LICENSE)。

English documentation: [README.en.md](README.en.md).

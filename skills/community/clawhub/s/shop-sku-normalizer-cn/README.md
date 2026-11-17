# 商品规格与SKU整理

![商品规格与SKU整理推广图](assets/promo-1600x900.png)

把杂乱的商品名称、颜色、尺寸和型号表整理为统一命名、重复/缺失规格报告与 CSV 导入草稿。帮助中文小店经营者、小说作者和自媒体创作者在发布或整理资料前更快发现问题。

## 能做什么

- 处理用户直接提供的最多 100 行商品资料。
- 保留准确的原始字段，并把统一化结果明确标为“建议”。
- 标识重复组合、缺失字段和待确认项；重复组所有行均待确认，并提供稳定的待确认原因，不编造资料。
- 生成可复核、可复制的 CSV 导入草稿；不会读取库存保险库、连接后台或执行导入。

## 输入与结果

提供含 `商品名称`、`颜色`、`尺寸`、`型号` 四列的表格、CSV、TSV 或文本。输出依次为统一命名表、重复/缺失规格报告与 CSV 导入草稿。草稿含“待确认原因”列；重复组合中的所有行均标为“待确认”。缺少关键字段时，Skill 会指出缺失并停止生成可导入草稿。

成功和失败样例分别见 [fixtures/success-products.txt](fixtures/success-products.txt) 与 [fixtures/failure-missing-field.txt](fixtures/failure-missing-field.txt)。

## 使用

在支持 Skill 的环境中调用 `shop-sku-normalizer-cn`，然后粘贴或附上不超过 100 行的商品资料。完整工作流见 [SKILL.md](SKILL.md)。

## 校验

```bash
bash scripts/self-test.sh
```

该测试只校验发布结构、元数据、素材尺寸及成功/失败样例的形状；真实整理行为由对话中执行的 Markdown 工作流完成。

## 来源与许可证

本项目原创撰写，仅参考 [ERPNext](https://github.com/frappe/erpnext) 的公开项目用途，不复制其源码或文案。详见 [manifest.yaml](manifest.yaml) 的来源记录。采用 [MIT-0](LICENSE)。

## 安装

```bash
npx skills add xxjrq/shop-sku-normalizer-cn
```

## 完整输出示例

查看 [成功输出](fixtures/forward-success.md) 和 [缺资料响应](fixtures/forward-failure.md)，对照上述输入样例了解实际交付内容。

# 商品详情页文案

![商品详情页文案推广图](assets/promo-1600x900.png)

用商家已经确认的真实资料，快速写出一套可上架的中文商品详情页：首屏、卖点、规格、配图文案和 FAQ 一次齐全，而且每条关键卖点都能回到真实证据。

这是一个纯 Markdown Skill，没有服务端、第三方 API 或浏览器依赖。它适合中文小店经营者、小说作者及自媒体创作者为周边、课程、实物或数字商品整理详情页；不用于闲鱼标题或通用客服回复。

## 你会得到什么

- 完整详情页模块文案：首屏、卖点、规格、图片配文、场景提醒和 FAQ。
- 每条卖点的事实证据，避免把推测写成商品事实。
- 明确分栏的“已知事实 / 表达建议 / 待商家确认”。
- 缺资料时先指出缺失字段，不臆测参数、图片、认证、售后或效果。

## 输入

```json
{
  "product_name": "云岚手冲咖啡滤杯",
  "specifications": {"材质": "高硼硅玻璃", "容量": "1-2杯"},
  "image_notes": ["图片1展示透明滤杯与螺旋导流肋"],
  "target_audience": "在家手冲咖啡的初学者",
  "known_facts": ["商家提供适配V60 01号滤纸"],
  "suggestions": ["首屏可强调透明器具便于观察注水过程"]
}
```

必填：`product_name`、`specifications`、`image_notes`、`target_audience`。规格、图片说明和已知事实请使用商家提供的原值。

## 使用方式

将输入交给 Skill，并要求按 `SKILL.md` 的“交付格式”输出。它会先检查必填资料；若缺少 `image_notes` 或 `target_audience`，应明确要求补充，而不是编造。

成功与缺字段示例见 [fixtures](fixtures/)。

## 自测

在本仓库根目录运行：

```bash
bash scripts/self-test.sh
```

自测仅检查发布结构、关键 manifest 字段、图片尺寸和成功/失败样例结构；它不宣称检验生成文案的业务质量。

## 来源与许可

本 Skill 的用途参考了 [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) 及其 [copywriting Skill](https://github.com/coreyhaines31/marketingskills/blob/main/skills/copywriting/SKILL.md)。本仓库的中文说明、工作流与样例均为原创，未复制其源码或文案。许可证为 [MIT-0](LICENSE)。

## 安装

```bash
npx skills add xxjrq/shop-product-detail-copy-cn
```

## 完整输出示例

查看 [成功输出](fixtures/forward-success.md) 和 [缺资料响应](fixtures/forward-failure.md)，对照上述输入样例了解实际交付内容。

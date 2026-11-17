# 1688 到 PTJourney 的统一数据包

这份工作簿是 AI 与 PTJourney MCP 的统一交接格式。工作表名为 `products`，第一行使用下面的英文字段名；一行对应一个货号。执行时按平台、店铺和模板拆批，不在商品行中混写密钥。

## 建议工作簿

`products` 工作表：

| 字段 | 含义 | 来源与校验 |
| --- | --- | --- |
| `source_platform`, `source_url`, `source_product_id` | 1688 来源标识 | 保留原始链接和 ID，供追溯。 |
| `offer_id` | 本次稳定货号 | 非空、批内唯一；与图片文件夹名一致。 |
| `title_zh`, `title_ru`, `title_en` | 来源标题、俄文标题、英文标题 | 翻译分别复核；TEMU 使用英文标题。 |
| `description_zh`, `description_ru` | 来源描述、俄文描述 | 保留事实，不增加未经核实的卖点。 |
| `category_hint`, `category_id`, `brand`, `material`, `color`, `size` | 类目及属性线索 | 标明已核实、待确认或不适用；平台类目属性另行匹配。 |
| `cost_cny`, `price_rub`, `old_price_rub` | 采购价、上架价、原价 | 不把 1688 成本直接当成上架价。币种分列。 |
| `package_length_mm`, `package_width_mm`, `package_height_mm`, `package_weight_g` | 包装尺寸重量 | 来源没有可靠值时留空并待补。 |
| `ozon_attributes_json`, `wb_characteristics_json`, `variant_group` | 平台属性和变体归组 | 从当前店铺的目标类目规则确认 ID、字典值和必填项后填写。 |
| `image_folder`, `image_count` | 相对图片目录、图片数 | 文件夹名与 `offer_id` 一致；记录图片来源和授权状态。 |
| `target_platform`, `template_id`, `category_id`, `attribute_status`, `review_status` | 上架路由和复核状态 | 平台适配前补齐，不凭模型猜 ID。 |
| `ozon_item_json` | Ozon 标品完整商品快照 | 包含 `offer_id`、俄文 `name`、类目及类型 ID、售价、包装长宽高重、`attributes`；按当前 Ozon 类目规则补齐。 |
| `wb_request_json` | Wildberries（WB） 完整建卡与后处理请求 | 包含 `requestBody`、`postCreate`、`storeConfig`；按当前 WB 类目规则补齐。 |

`targets` 工作表：`target_platform`、`shop_id`、`shop_name`、`template_id`、`warehouse_id`、`allocation_mode`、`status`。店铺 ID、模板 ID、仓库 ID 应从 PTJourney 当前登录账号读取或由用户提供，不从商品来源推断。

推荐目录：

```text
batch-2026-xx-xx/
  products.xlsx
  images/
    OFFER-001/
      01.jpg
      02.jpg
    OFFER-002/
      01.jpg
  source-notes/
```

保留 `source-notes` 中的来源摘录和翻译复核记录。下载图片时保留原图顺序，不把供应商展示图直接认定为符合目标平台的主图。

## 平台导出

- **TEMU**：另生成 PTJourney 现有上传表，第一行表头，后续三列按顺序为货号/图片 ID、标题、英文标题。解析器读取前三列；英文标题为空时会回退到第 4 列。每个货号的图片目录至少 5 张图；另需店铺 ID、产品模板 ID、任务描述和正整数商品间隔秒数。
- **Ozon POD**：另生成 PTJourney POD 模板表，列为货号、标题、价格、原价、合并字段、商品颜色、颜色名称。价格和原价可留空使用模板值；原价填写时需大于售价。每个货号对应的文件夹至少含一张 JPG/JPEG/PNG。每批需确认一个可复用的 POD 模板、店铺列表、分配方式和图片根目录。模板中的类目、属性、包装和其他商品字段不会从该表逐行读取。
- **Ozon 标品**：在 `ozon_item_json` 放每件商品的完整 Ozon 快照；需目标店铺、仓库、Ozon 类目、俄文标题、全新货号、售价、包装长宽高重和真实类目属性。MCP 按 `offer_id` 图片目录上传图片并覆盖快照中的主图/副图地址，再逐商品创建独立任务。当前一行只支持一个商品快照；变体组须先拆成完整 SKU 行。
- **WB**：在 `wb_request_json` 放完整请求：`requestBody[0].subjectID`、`variants[0]`（货号、俄文标题、描述、品牌、尺寸重量、类目属性、规格）、`postCreate`（价格 RUB、折扣）和 `storeConfig`（仓库与库存）。必填属性及选项从当前 WB 类目读取；MCP 上传图片并填入 `postCreate.images`，逐商品创建任务。

# MRO API 使用说明

## 服务和认证

- 平台首页：`https://mro-api.iwilley.com`
- MCP：`POST https://mro-api.iwilley.com/v1/mcp`
- REST 匹配：`POST https://mro-api.iwilley.com/v1/match-inquiry`
- REST 商品详情：`GET https://mro-api.iwilley.com/v1/products/{source}/{source_id}`

认证请求头任选一种：`Authorization: Bearer <API_KEY>`、`apikey: <API_KEY>` 或 `X-API-Key: <API_KEY>`。

MCP 提供四个工具：

- `list_sources`：读取授权来源及私有商品数量（来源元数据免费）。

- `match_inquiry`：单条检索、分类探索、属性探索和最终候选查询。
- `get_product`：按 `source + sourceId` 读取指定商品完整资料，不重新匹配。
- `batch_match_inquiries`：接口一次可提交 1–20 个相互独立的 `match_inquiry` 请求；Skill 默认每批 10 条。

## match_inquiry 常用入参

| 字段 | 说明 |
| --- | --- |
| `mpn` | 制造商型号。存在时优先执行 MPN 检索。 |
| `keyword` | 全字段初筛词，可检索名称、描述、MPN、品牌、分类和属性。 |
| `brands` | 当前候选中实际出现的品牌名数组；数组内 OR。 |
| `categories` | 使用 `categories.items[].key`；数组内 OR。`uncategorized` 表示无分类。 |
| `attributes` | 属性条件组；组间 AND、每组 `anyOf` 内 OR。 |
| `sources` | 用户有权查询的数据源数组。 |
| `responseMode` | `detail` 或 `summary`。`summary` 仅返回候选数。 |
| `includeFacets` | 是否返回品牌、分类及相关分面。 |
| `includeAttributes` | 是否计算并返回属性分布。 |
| `includeProducts` | 是否返回最多 6 件候选商品。 |
| `facetPage` | 品牌、分类、属性名或属性值的分页请求。 |

同时提供 `mpn` 和 `keyword` 时，服务执行 MPN 查询。关键词回退必须由 Skill 另发一次请求。

## 属性条件的正确格式

```json
{
  "keyword": "DIN 917",
  "categories": ["盖形螺母"],
  "attributes": [
    {
      "requested": "M8",
      "anyOf": [
        {"name": "尺寸", "value": "M8"},
        {"name": "螺纹直径", "value": "M8"}
      ]
    },
    {
      "requested": "A2",
      "anyOf": [
        {"name": "材质", "value": "A2"},
        {"name": "材料牌号", "value": "A2"}
      ]
    }
  ],
  "includeAttributes": false,
  "includeProducts": true
}
```

外层只使用可选的 `requested` 和必填的 `anyOf`。即使组内选项的属性名相同，每个 `anyOf[]` 对象也必须重复填写自己的 `name` 和 `value`。外层 `name` 会被 422 拒绝。

## 推荐的分阶段请求

### 分类探索

```json
{
  "keyword": "光纤跳线 LC SC 15m",
  "includeAttributes": false,
  "includeProducts": false
}
```

读取 `candidateCount`、`brands.items` 和 `categories.items`，选择目标分类 `key`。

### 属性探索

```json
{
  "keyword": "光纤跳线 LC SC 15m",
  "categories": ["光纤跳线"],
  "includeAttributes": true,
  "includeProducts": false
}
```

读取 `attributes.items[].name` 以及 `values[].value/count`，再构造属性组。

### 最终候选

```json
{
  "keyword": "光纤跳线 LC SC 15m",
  "categories": ["光纤跳线"],
  "attributes": [
    {"requested": "LC", "anyOf": [{"name": "Connector A", "value": "LC"}]},
    {"requested": "SC", "anyOf": [{"name": "Connector B", "value": "SC"}]},
    {"requested": "15m", "anyOf": [{"name": "Length", "value": "15m"}]}
  ],
  "includeFacets": false,
  "includeAttributes": false,
  "includeProducts": true
}
```

## batch_match_inquiries

多行询价优先批量处理。请求示例：

```json
{
  "inquiries": [
    {"keyword": "DIN 917", "includeAttributes": false, "includeProducts": false},
    {"keyword": "光纤跳线", "includeAttributes": false, "includeProducts": false}
  ]
}
```

规则：

- 接口硬上限为每批 1–20 条，请求项字段与 `match_inquiry` 相同；默认每批 10 条。
- 请求项不要传 `index` 或其他未定义字段。
- 响应按 `results[].index` 对应本批数组位置。
- 纯摘要首轮可每批 10–20 条；分类探索、属性分布和最终商品阶段默认每批 10 条。
- 属性分布响应较大或需要定点精筛时，建议每批 5–10 条。
- 同一行前后依赖的阶段不能放在一批中。
- 批量调用的实际积分消耗以平台当前计费说明及账号用量为准；不要把接口请求数直接等同于可处理询价行数。

## 响应体积控制

- `responseMode="summary"`：只确认候选数量，自动关闭分面、属性和商品。
- 分类探索：`includeAttributes=false, includeProducts=false`，保留分面。
- 属性探索：`includeAttributes=true, includeProducts=false`，不要关闭分面。
- 最终商品：`includeFacets=false, includeAttributes=false, includeProducts=true`。
- `includeAttributes` 与 `includeProducts` 通常不要同时开启。
- 只在需要核查最终候选时调用 `get_product`。

`facetPage` 与 `includeFacets=false` 不能同时提交。属性名每页最多 20 个，属性值每页最多 100 个，品牌和分类每页最多 50 个；目标值出现后即可停止翻页。

## 常见警告和错误

| 情况 | 处理方式 |
| --- | --- |
| `attribute_name_not_found` | 回到当前分类的属性分布，确认实际属性名。 |
| `attribute_value_not_found` | 使用分布中返回的原始值和单位格式。 |
| `attribute_combination_no_match` | 分别提交属性组定位冲突；关键规格不放宽。 |
| 422 | 检查属性外层是否误传 `name`、`anyOf` 项是否缺少 `name/value`，以及分页参数。 |
| 401/403 | 检查 API Key、账号状态和数据源权限。 |
| 批量单项失败 | 查看 `results[index].error`，不要让一项错误覆盖整批结果。 |

## 用户私有商品

`list_sources` / `GET /v1/sources` 免费返回授权来源及 `privateProductCount`。`sources:["mine"]` 查询当前 API Key 所属账号的商品；省略 sources 仍为授权公共来源。商品详情沿用 `source="mine"` 和匹配响应原样返回的 sourceId，不能指定其他账号。私有匹配与详情正常扣费。先查私有、零结果再查公共由 Skill 编排，接口不自动回退。

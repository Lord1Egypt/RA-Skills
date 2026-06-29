# 字段类型推断规则

Agent 从用户自然语言描述中提取字段时，依据字段名称语义自动推断类型。用户无需显式指定字段类型。

---

## 字段类型映射表

| 类型 | 触发关键词（示例） | HTML 表现 | 说明 |
|------|------------------|-----------|------|
| **text** | 名称、品名、标题、型号、产品名 | `<input type="text">` | 单行文本，主标识字段优先选此类型 |
| **textarea** | 描述、备注、心得、笔记、风味描述、感受、评价、简介 | `<textarea>` | 多行文本，适合长内容输入 |
| **number** | 价格、金额、数量、库存、里程、距离、评分、克重、容量、度数 | `<input type="number">` | 纯数字，可含小数 |
| **date** | 购买日期、入手日期、到期日、有效期、开始时间、出版日期、烘焙日期 | `<input type="date">` | ISO 8601 日期格式，可用于排序 |
| **select（固定）** | 状态、烘焙度、评级、优先级、阶段、类别（封闭） | `<select>` + `<option>` | 值域封闭且不会扩展，选项在 schema 中写死 |
| **smart-select** | 品牌、产地、分类、制造商、产区、系列、作者、出版社 | `<select>` + hidden input + 自定义输入 | 值域有限但可扩展，历史值自动填入 |
| **boolean** | 是否推荐、已完成、已读、是否收藏、已归档 | `<input type="checkbox">` | 两值布尔，存储为 0/1 |

---

## 推断优先级规则

1. **精确匹配优先**：字段名直接命中关键词列表时，使用对应类型。
2. **语义匹配兜底**：未精确命中时，按语义推断：
   - 含"日期/时间/期" → `date`
   - 含"数/量/价/率/分/重/度数" → `number`
   - 含"描述/备注/心得/笔记/说明" → `textarea`
   - 含"是否/已/未" → `boolean`
   - 其余默认 → `text`
3. **Smart Select vs 固定 Select 判断标准**：
   - **固定 Select**：值域封闭、不随使用增长（如"在用/退役"、"已读/想读/在读"、"新鲜/过期"）
   - **Smart Select**：值域有限但可随用户数据扩展（如品牌、产地、分类——用户可能持续添加新值）
   - 判断依据：问"用户将来会不会添加新选项？" 会 → smart-select，不会 → 固定 select

---

## Schema 必要字段规则

每个数据 schema 必须满足以下约束：

### R-F1：主标识字段
- 必须有且仅有一个主标识字段
- 类型为 `text`，字段名通常为 `name`、`title`、`品名`、`名称` 等
- 作为 Card 组件的标题显示，也是搜索的主要目标字段
- 推断规则：第一个 `text` 类型字段默认为主标识字段，除非用户明确指定

### R-F2：状态字段
- 必须有一个状态字段，用于 Filter chips 筛选
- 类型为固定 `select`，选项数量建议 2~5 个
- 字段名通常为 `status`、`状态`、`stage`
- 若用户描述中没有明确状态字段，Agent 应提示补充或自动添加通用状态字段

### R-F3：日期字段（可选）
- 可选，存在时作为 Sort Bar 的排序维度之一
- 推荐存在时命名为 `date`、`purchase_date`、`created_at` 等
- 若用户描述含时间序列需求（"按购买时间排序"），则必须添加

---

## Smart Select 组件三件套规范

schema 中标记为 `smart-select` 的字段，HTML 中必须同时包含：

```html
<!-- 1. 下拉选择（历史值） -->
<select id="field-brand-select" onchange="syncSmartSelect('brand')">
  <option value="">请选择或输入</option>
  <!-- 动态填充历史值 -->
</select>

<!-- 2. 隐藏 input（实际存值） -->
<input type="hidden" id="field-brand" name="brand">

<!-- 3. 自定义输入框（手动输入新值） -->
<input type="text" id="field-brand-custom"
       placeholder="或输入新品牌"
       oninput="syncSmartSelectCustom('brand')">
```

JS 联动逻辑：
- 从 `select` 选择时 → 写入 hidden input，清空 custom input
- 在 `custom` 输入时 → 写入 hidden input，重置 select 为空
- 提交时读取 hidden input 的值

---

## 字段推断示例

**用户描述**：「我想记录我的咖啡豆，字段有：豆名、产地、品牌、烘焙度（浅/中/深）、购买日期、克重、价格、风味描述、状态（在用/用完/备货）、是否推荐」

**推断结果**：

| 字段 | 推断类型 | 理由 |
|------|----------|------|
| 豆名 | text（主标识）| 第一个文本字段，命名含"名" |
| 产地 | smart-select | 值域有限但可扩展（埃塞、哥伦比亚…用户会持续添加） |
| 品牌 | smart-select | 品牌可扩展 |
| 烘焙度 | select（固定）| 浅/中/深，封闭值域 |
| 购买日期 | date | 含"日期" |
| 克重 | number | 含"重" |
| 价格 | number | 含"价" |
| 风味描述 | textarea | 含"描述" |
| 状态 | select（固定）| 在用/用完/备货，封闭值域，作为筛选字段 |
| 是否推荐 | boolean | 含"是否" |

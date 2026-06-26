# 飞猪链接生成规则

每个航班/酒店/景点/美食都必须附带飞猪购买链接。

## 链接格式

### 航班链接
```
https://market.fliggy.com/item.htm?itemId=[商品ID]
```
- 从 `flyai search-flight` 结果中按优先级提取：`itemId` → `jumpUrl` → `jump_url` → 搜索关键词拼接

### 酒店链接
```
https://market.fliggy.com/item.htm?itemId=[商品ID]
```
- 从 `flyai search-hotels` 结果中按优先级提取：`itemId` → `detailUrl` → `detail_url` → 搜索关键词拼接

### 景点/门票链接
```
https://market.fliggy.com/item.htm?itemId=[商品ID]
```
- 从 `flyai search-poi` 结果中按优先级提取：`itemId` → `jumpUrl` → 搜索关键词拼接

### 美食/体验链接
```
https://market.fliggy.com/item.htm?itemId=[商品ID]
```
- 从 `flyai fliggy-fast-search` 结果中按优先级提取：`itemId` → `jumpUrl` → 搜索关键词拼接

## HTML 中展示格式

每个可购买项下方添加：
```html
<div class="buy-link">
  <a href="[飞猪链接]" target="_blank" rel="noopener" class="buy-btn">🛒 飞猪购买</a>
  <button class="copy-btn" onclick="copyLink('[飞猪链接]')">📋 复制链接</button>
  <span class="reason">💡 [推荐理由]</span>
</div>
```

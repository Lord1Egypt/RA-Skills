# 数据提取模板

## 电商产品页

```bash
# 提取价格
pup '.price text{}' < page.html
pup '[data-price] attr{data-price}' < page.html
pup '.offer-price text{}' < page.html

# 提取标题
pup 'h1.product-title text{}' < page.html

# 提取库存
pup '.stock-status text{}' < page.html

# 提取评分
pup '.rating-value text{}' < page.html
```

## 新闻列表页

```bash
# 提取所有文章标题和链接
pup 'article h2 a json{}' < page.html

# 提取发布时间
pup 'time attr{datetime}' < page.html

# 提取摘要
pup '.article-summary text{}' < page.html
```

## 政府公告页

```bash
# 提取公告列表（标题+链接+日期）
pup '.notice-list li json{}' < page.html

# 提取文号
pup '.doc-number text{}' < page.html

# 提取发布机构
pup '.publisher text{}' < page.html
```

## 招聘详情页

```bash
# 提取职位信息
pup '.job-title text{}' < page.html
pup '.salary text{}' < page.html
pup '.company-name text{}' < page.html

# 提取职位要求（完整文本）
pup '.requirements text{}' < page.html
```

## 通用全文提取

```bash
# 提取页面所有文本（去除 HTML 标签）
pup 'body text{}' < page.html | tr -s ' \n' ' '

# 提取 meta 描述
pup 'meta[name="description"] attr{content}' < page.html

# 提取页面标题
pup 'title text{}' < page.html
```

## curl 抓取模板

```bash
# 基础抓取
curl -s -L \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -H "Accept: text/html,application/xhtml+xml" \
  -H "Accept-Language: zh-CN,zh;q=0.9" \
  "https://example.com/page" > page.html

# 带 Cookie 的抓取
curl -s -L \
  -b "session=xxx; token=yyy" \
  "https://example.com/page" > page.html

# 带 Referer 的抓取
curl -s -L \
  -H "Referer: https://example.com" \
  "https://example.com/product/123" > page.html
```

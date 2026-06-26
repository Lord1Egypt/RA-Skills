# 网页抓取平台与工具映射参考表

## 社交媒体平台（优先使用opencli）

### 小红书
- **工具**: `opencli xiaohongshu`
- **适用场景**: 搜索、笔记抓取、用户数据
- **输出格式**: 结构化JSON
- **示例**: `opencli xiaohongshu search "关键词" --limit 3 -f json`

### 知乎
- **工具**: `opencli zhihu`
- **适用场景**: 热榜、问答、专栏文章
- **输出格式**: 结构化JSON
- **示例**: `opencli zhihu hot --limit 5 -f json`

### 微博/B站
- **工具**: `opencli weibo` / `opencli bilibili`
- **适用场景**: 热搜、视频数据、用户动态
- **输出格式**: 结构化JSON

## 电商平台（使用playwright-cli）

### 京东
- **工具**: `playwright-cli goto`
- **适用场景**: 商品详情、评论抓取、价格监控
- **输出格式**: HTML内容解析
- **示例**: `playwright-cli goto "https://item.jd.com/44541018110.html#comment"`

### 淘宝/天猫
- **工具**: `playwright-cli goto`
- **适用场景**: 商品列表、SKU信息、评价数据
- **输出格式**: HTML内容解析

### 1688
- **工具**: `playwright-cli goto`
- **适用场景**: 供应商信息、批发价格、起订量
- **输出格式**: HTML内容解析
- **示例**: `playwright-cli goto "https://s.1688.com/selloffer/offer_search.htm?keywords=关键词"`

### 抖音/拼多多
- **工具**: `playwright-cli goto`
- **适用场景**: 商品信息、直播数据、用户内容
- **输出格式**: HTML内容解析

## 选择原则

1. **有适配器的平台** → 优先使用opencli（结构化、速度快、稳定）
2. **无适配器的平台** → 使用playwright-cli（通用性强、绕过反爬）
3. **需要登录态数据** → 使用playwright-cli（复用Chrome标签页）
4. **演示场景** → 先尝试opencli，失败则fallback到playwright-cli
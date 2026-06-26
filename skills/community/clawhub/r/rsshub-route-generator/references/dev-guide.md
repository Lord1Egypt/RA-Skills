# RSSHub 路由开发参考

## 核心类型

```typescript
// Route 接口
{
  path: string,           // '/news/:category?'
  name: string,           // '新闻列表'
  maintainers: string[],  // ['username']
  handler: async (ctx) => Data,
  example?: string,
  categories?: string[],
  radar?: [{ source: [string], target: string }]
}

// Data 对象
{
  title: string,
  link: string,
  item: DataItem[],
  description?: string
}

// DataItem
{
  title: string,    // 必需
  link: string,     // 必需
  pubDate?: string,
  description?: string,  // HTML
  category?: string[]
}
```

## 常用工具

```typescript
import { load } from 'cheerio';
import { parseDate } from '@/utils/parse-date';
import { pMap } from '@/utils/p-map';
import ofetch from '@/utils/ofetch';

// 选择器技巧
$('ul.list li a')           // 层级
$('[class*="news"]')        // 模糊匹配
$('a[href$=".html"]')       // 属性后缀

// 日期解析
parseDate('2024-01-15')
parseDate('2024年01月15日', 'YYYY年MM月DD日')

// 并发控制
await pMap(list, fn, { concurrency: 5 })
```

## 常见模式

### 静态页面
```typescript
const $ = load(response.data);
const items = $('ul.news-list li').map((_, el) => ({
  title: $(el).find('a').text().trim(),
  link: new URL($(el).find('a').attr('href'), baseUrl).href,
  pubDate: parseDate($(el).find('.date').text())
})).get();
```

### 全文 RSS
```typescript
const fulltext = ctx.req.query('fulltext') === 'true';
const items = await pMap(list, async (item) => {
  if (fulltext) {
    const { data } = await got(item.link);
    item.description = load(data)('.content').html();
  }
  return item;
}, { concurrency: 3 });
```

### 多栏目
```typescript
path: '/:category/:type?',
parameters: { category: 'news|notice', type: 'all|hot' }
```

## 政府网站选择器

```javascript
// 列表
'ul.list', 'div.news-list', '.zwgk_list li', 'table tbody tr'

// 标题
'a[title]', 'h3 a', '.bt a'

// 日期
'span.date', 'span.time', '[datetime]'

// 内容
'#zoom', '.article-content', '.TRS_Editor'
```

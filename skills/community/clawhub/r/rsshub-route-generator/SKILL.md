# RSSHub 路由生成器

> 深度分析网站结构，生成 RSSHub 路由代码

## 技能描述

本技能用于分析任意网站结构，并生成符合 RSSHub 规范的路由代码文件。生成的路由支持：
- 栏目列表 RSS
- 全文 RSS（可选）
- RSSHub Radar 规则

## 触发词

当用户发送以下内容时激活本技能：

- "生成 RSSHub 路由"
- "帮我创建 RSS"
- "为网站生成 RSS 订阅"
- "制作 RSSHub 路由"
- "生成 RSS 路由"
- 任意网站 URL（将自动检测并询问是否需要生成 RSSHub 路由）

## 执行逻辑

### 第一步：网站深度分析

1. **页面结构探测**
   - 使用 `web_fetch` 获取页面 HTML 内容
   - 识别文章列表容器（常见选择器：`ul`、`div.list`、`div.news-list`、`article`）
   - 识别标题元素（`h1`-`h6`、`a`、`div.title`）
   - 识别日期元素（`time`、`span.date`、`[datetime]`）
   - 识别分类标签（`span.category`、`a.tag`）

2. **栏目识别**
   - 扫描导航菜单中的栏目链接
   - 识别侧边栏分类
   - 识别面包屑导航

3. **链接模式分析**
   - 分析内链路径模式（如 `/news/2024/01/xxx.html`）
   - 识别分页结构
   - 确定详情页 URL 格式

### 第二步：RSSHub 路由生成

根据分析结果生成 TypeScript 代码文件，遵循以下规范：

```typescript
import { Route } from '@/types';
import got from '@/utils/got';
import { load } from 'cheerio';
import { parseDate } from '@/utils/parse-date';

export const route: Route = {
    path: '/{category}',
    categories: ['{category}'],
    example: '/{site}/{category}',
    parameters: {
        category: '分类名称，默认为 all',
    },
    features: {
        requireConfig: false,
        requirePuppeteer: false,
        antiCrawler: false,
        supportBT: false,
        supportPodcast: false,
        supportScihub: false,
    },
    radar: [
        {
            source: ['{domain}/'],
            target: '/{category}',
        },
    ],
    name: '{网站名称}',
    maintainers: [],
    handler,
    url: '{domain}',
    description: `{网站描述}`,
};

async function handler(ctx) {
    const category = ctx.req.param('category') || 'all';
    const baseUrl = '{website_url}';
    
    // 构建请求 URL
    const url = category === 'all' 
        ? `${baseUrl}/` 
        : `${baseUrl}/${category}/`;
    
    // 获取页面内容
    const response = await got({ method: 'get', url });
    const $ = load(response.data);
    
    // 解析文章列表
    const items = $('{list_selector}').map((_, element) => {
        const $el = $(element);
        return {
            title: $el.find('{title_selector}').text().trim(),
            link: new URL($el.find('{link_selector}').attr('href'), baseUrl).href,
            pubDate: parseDate($el.find('{date_selector}').text().trim(), 'YYYY-MM-DD'),
            category: $el.find('{category_selector}').text().trim(),
        };
    }).get();
    
    // 获取全文内容（可选）
    const fulltextItems = await Promise.all(
        items.slice(0, 10).map(async (item) => {
            try {
                const detailResponse = await got({ method: 'get', url: item.link });
                const detail$ = load(detailResponse.data);
                item.description = detail$('{content_selector}').html();
                return item;
            } catch {
                return item;
            }
        })
    );
    
    return {
        title: '{website_title}',
        link: baseUrl,
        description: '{website_description}',
        item: fulltextItems,
        language: 'zh-cn',
    };
}
```

### 第三步：文件输出

生成的路由文件保存到工作目录，命名格式：
- 主路由：`rsshub-routes/{domain}/{route-name}.ts`
- 命名空间：`rsshub-routes/{domain}/namespace.ts`（如需）

## 输出格式

### 1. 网站分析报告

```
## 网站结构分析

### 基本信息
- 域名：{domain}
- 网站标题：{title}
- 语言：{language}

### 栏目结构
| 栏目名 | URL 模式 | 列表选择器 |
|--------|----------|-----------|
| 栏目1 | /news/ | div.news-list li |
| 栏目2 | /notice/ | ul.article-list li |

### 文章结构
- 标题选择器：{title_selector}
- 链接选择器：{link_selector}
- 日期选择器：{date_selector}
- 分类选择器：{category_selector}
- 内容选择器：{content_selector}

### 生成路由
```typescript
{generated_code}
```
```

### 2. 路由文件

生成完整的 `.ts` 文件，可直接复制到 RSSHub 项目使用。

## 常见选择器模式参考

### 政府网站
```javascript
// 列表项
$('ul.list li', 'div.news-list li', 'table tr')

// 标题
$('a[title]', 'h3 a', '.title a')

// 日期
$('span.date', '.time', '[datetime]')

// 内容
$('#content', '.article-content', '.main-content')
```

### 新闻网站
```javascript
// 列表
$('.news-list li', '.article-list .item', 'div.container ul li')

// 正文
$('.article-body', '.content', '.post-content')
```

### 论坛社区
```javascript
// 帖子列表
$('.thread-list tr', '.topic-item', '.post-list .item')

// 内容
$('.thread-content', '.post-body', '.message')
```

## 最佳实践

1. **缓存策略**：使用 `ofetch` 并配置合理的缓存 key
2. **并发控制**：详情页获取使用 `pMap` 控制并发（建议 3-5）
3. **错误处理**：每个请求都用 try-catch 包装
4. **去重**：使用 `Map` 或 `Set` 去重
5. **分页**：支持 `limit` 参数，默认 20 条
6. **全文**：可选 `fulltext` 参数控制是否获取全文

## 示例工作流

用户输入：
```
为 https://example.com/news/ 生成 RSSHub 路由
```

技能执行：
1. 访问页面，分析结构
2. 识别栏目和列表模式
3. 生成路由代码
4. 输出分析报告和代码文件

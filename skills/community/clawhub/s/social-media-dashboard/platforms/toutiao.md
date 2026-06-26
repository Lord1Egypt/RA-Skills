# 头条号数据采集

## 概述

通过浏览器自动化方式采集头条号后台数据，包括粉丝数、阅读量、收益等核心指标。

## 数据采集方式

**注意**：头条号的 API 接口经常变更，推荐使用以下方式获取数据：

### 方式一：从后台首页提取（推荐）

登录后访问 `https://mp.toutiao.com/profile_v4/`，页面首页会显示：

- 总粉丝数
- 今日/昨日阅读量
- 近期作品数据

使用浏览器自动化提取这些数据。

### 方式二：访问数据页面

- **粉丝数据**: `https://mp.toutiao.com/profile_v4/index.html#!/fan-data`
- **收益数据**: 点击后台左侧「收益数据」菜单
- **作品数据**: 点击后台左侧「作品数据」菜单

## 采集流程

### 方式一：浏览器自动化（推荐）

使用 Playwright 进行浏览器自动化操作：

```javascript
// 1. 打开头条号后台
await page.goto('https://mp.toutiao.com');

// 2. 等待用户扫码登录
await page.waitForSelector('.user-info', { timeout: 300000 });

// 3. 获取登录状态 Cookie
const cookies = await page.context().cookies();

// 4. 调用数据接口
const fansData = await page.evaluate(async () => {
  const response = await fetch('https://mp.toutiao.com/mp/agw/statistics/fans');
  return response.json();
});

const articleData = await page.evaluate(async () => {
  const response = await fetch('https://mp.toutiao.com/mp/agw/statistics/article');
  return response.json();
});

const incomeData = await page.evaluate(async () => {
  const response = await fetch('https://mp.toutiao.com/mp/agw/income/overview');
  return response.json();
});
```

### 方式二：Cookie 直接请求

如果用户已有登录 Cookie：

```javascript
const headers = {
  'Cookie': userProvidedCookie,
  'User-Agent': 'Mozilla/5.0 ...',
  'Referer': 'https://mp.toutiao.com/'
};

const fansData = await fetch('https://mp.toutiao.com/mp/agw/statistics/fans', {
  headers
});
```

## 频率限制

- 每次请求间隔 ≥ 2 秒
- 每小时最多 30 次请求
- 建议用户设置合理的刷新间隔

## 错误处理

| 错误码 | 说明 | 处理方式 |
|-------|------|---------|
| 401 | 未登录 | 提示用户重新授权 |
| 429 | 请求过于频繁 | 等待后重试 |
| 500 | 服务器错误 | 稍后重试 |

## 数据示例

```json
{
  "fans": {
    "total": 45231,
    "today_new": 234,
    "yesterday_new": 189,
    "trend": [
      { "date": "2026-03-09", "count": 44200 },
      { "date": "2026-03-10", "count": 44356 },
      { "date": "2026-03-11", "count": 44512 },
      { "date": "2026-03-12", "count": 44689 },
      { "date": "2026-03-13", "count": 44890 },
      { "date": "2026-03-14", "count": 44997 },
      { "date": "2026-03-15", "count": 45231 }
    ]
  },
  "article": {
    "total_read": 1256789,
    "read_today": 23456,
    "read_yesterday": 19876,
    "article_count": 234
  },
  "income": {
    "total": 12345.67,
    "today": 56.78,
    "yesterday": 45.23,
    "month": 1234.56
  }
}
```

## 实现步骤

当用户请求查看头条号数据时：

1. **检查登录状态**
   - 查找本地是否有有效的头条 Session/Cookie
   - 如果没有，启动浏览器自动化登录流程

2. **采集数据**
   - 按顺序请求粉丝、内容、收益接口
   - 请求间隔 2 秒以上
   - 处理可能的错误

3. **生成报告**
   - 整合数据生成 Markdown 格式报告
   - 计算日环比、周同比
   - 标注异常数据（如暴涨/暴跌）

4. **存储数据**
   - 将当日数据追加到本地历史记录
   - 用于后续趋势分析

## 安全提示

- 不要存储用户密码
- Cookie/Session 加密存储
- 数据仅保存在用户本地
- 提醒用户不要分享登录凭证

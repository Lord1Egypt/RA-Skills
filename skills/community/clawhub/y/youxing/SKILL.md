---
name: 友行
description: 查询友行青年社群的活动信息。当用户询问友行的活动、近期活动、活动安排、某个活动详情时使用。支持列出所有活动和根据活动ID获取详情。默认输出JSON，用户要求时可输出Markdown格式。
---

## 概述

友行青年社群活动查询工具。

## 使用时机

- 用户问友行有什么活动、近期活动列表
- 用户想了解某个具体活动的详情
- 用户提到"友行"、"友行青年社群"

## 通用参数

```
CLUB_ID = 018c32aa-7958-ede5-c6ae-403c9881a2a5
API_BASE = https://api.cumen.fun/api/xx.cumen.v1.CumenService
```

## 功能一：列出所有活动

```bash
node -e "
const https = require('https');
const API = 'https://api.cumen.fun/api/xx.cumen.v1.CumenService/ListCampaignsOfClub';
const CLUB_ID = '018c32aa-7958-ede5-c6ae-403c9881a2a5';

function post(url, body) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const req = https.request(url, { method: 'POST', headers: { 'Content-Type': 'application/json' } }, (res) => {
      let buf = '';
      res.on('data', (c) => (buf += c));
      res.on('end', () => { try { resolve(JSON.parse(buf)); } catch { reject(new Error(buf)); } });
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

function toUTC8(ts) {
  if (!ts || ts.startsWith('1970')) return null;
  const d = new Date(ts);
  return new Date(d.getTime() + 8 * 3600000).toISOString().replace('Z', '+08:00');
}

const STATUS = { CAMPAIGN_STATUS_ONGOING: 'ONGOING', CAMPAIGN_STATUS_ENDED: 'ENDED', CAMPAIGN_STATUS_BLOCKED: 'BLOCKED' };

post(API, { clubId: CLUB_ID }).then((resp) => {
  const items = resp.items || [];
  const result = items.map((item) => {
    const c = item.campaign || {};
    return {
      id: c.id || '',
      title: c.title || '',
      price: (c.price || {}).value || '0',
      address: item.address || '',
      start_time: toUTC8(c.start_time),
      end_time: toUTC8(c.end_time),
      join_deadline: toUTC8(c.join_deadline),
      capacity: c.person_number_of_team || 0,
      status: STATUS[c.status] || c.status || '',
      finished: c.finish || false,
    };
  });
  console.log(JSON.stringify(result, null, 2));
}).catch((e) => { console.error(e.message); process.exit(1); });
"
```

### Markdown 输出格式

用户要求 Markdown 时，将结果渲染为表格：

```markdown
## 友行青年社群 活动列表 (14个)

| # | 标题 | 价格 | 地址 | 开始时间 | 结束时间 | 名额 | 已结束 |
|---|------|------|------|----------|----------|------|--------|
| 1 | 咖啡拉花单次课程｜友行 周日下午 | ¥39 | ... | 04-12 14:00 | 04-12 16:00 | 20 | 否 |
```

时间格式 `MM-DD HH:mm`，标题中 `|` 替换为 `｜`。

## 功能二：获取活动详情

将 `CAMPAIGN_ID` 替换为实际活动 ID：

```bash
node -e "
const https = require('https');
const API = 'https://api.cumen.fun/api/xx.cumen.v1.CumenService/GetCampaign';
const CAMPAIGN_ID = 'CAMPAIGN_ID';

function post(url, body) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const req = https.request(url, { method: 'POST', headers: { 'Content-Type': 'application/json' } }, (res) => {
      let buf = '';
      res.on('data', (c) => (buf += c));
      res.on('end', () => { try { resolve(JSON.parse(buf)); } catch { reject(new Error(buf)); } });
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

function toUTC8(ts) {
  if (!ts || ts.startsWith('1970')) return null;
  const d = new Date(ts);
  return new Date(d.getTime() + 8 * 3600000).toISOString().replace('Z', '+08:00');
}

const STATUS = { CAMPAIGN_STATUS_ONGOING: 'ONGOING', CAMPAIGN_STATUS_ENDED: 'ENDED' };
const KIND = { 1: 'CREATE_TEAM', 2: 'GROUP_PURCHASE', 3: 'LEAGUES' };

post(API, { campaignId: CAMPAIGN_ID }).then((data) => {
  const c = data.campaign || {};
  const p = data.post || {};
  const priceVal = (typeof data.price === 'object' ? data.price.value : data.price) || (c.price || {}).value || '0';
  const poi = p.poi || {};
  const loc = poi.location_gcj02 || {};
  const result = {
    id: c.id,
    title: c.title,
    status: STATUS[c.status] || c.status,
    kind: KIND[c.kind] || c.kind,
    price: priceVal,
    start_time: toUTC8(c.start_time),
    end_time: toUTC8(c.end_time),
    join_deadline: toUTC8(c.join_deadline),
    quit_deadline: toUTC8(c.quit_deadline),
    capacity: c.person_number_of_team || 0,
    address: { name: poi.name || '', detail: poi.address || '', latitude: loc.latitude, longitude: loc.longitude },
    summary: p.summary || '',
    description: p.content || '',
    images: (p.images || []).map((img) => img.url),
    share_count: data.share_count || 0,
    comment_count: data.comment_count || 0,
    finished: c.finish || false,
  };
  console.log(JSON.stringify(result, null, 2));
}).catch((e) => { console.error(e.message); process.exit(1); });
"
```

### Markdown 输出格式

用户要求 Markdown 时：

```markdown
## 咖啡拉花单次课程|友行 周日下午

- **状态**: 进行中
- **类型**: 组团
- **价格**: ¥39
- **时间**: 2026-04-12 14:00 ~ 16:00
- **报名截止**: 2026-04-12 14:00
- **名额**: 20人
- **地点**: 安派德咖啡学院
- **地址**: 合肥市蜀山区望江西路388号新粮仓11栋4103
- **分享**: 6 | **评论**: 3

> ☕️ 咖啡拉花体验课 | 新手友好 · 咖啡管饱！
> ...
```

## 字段映射规则

- `price`: 优先取顶层 `price.value`（可能为 string 或 object），否则取 `campaign.price.value`
- `address`: 列表接口取 `item.address`，详情接口从 `post.poi` 提取 name/address/location
- `description`: 取 `post.content`
- `summary`: 取 `post.summary`
- `images`: 取 `post.images[].url`
- 时间：UTC → UTC+8 ISO 格式
- `status` 映射：`CAMPAIGN_STATUS_ONGOING` → `ONGOING`，`CAMPAIGN_STATUS_ENDED` → `ENDED`，`CAMPAIGN_STATUS_BLOCKED` → `BLOCKED`
- `kind` 映射：`1` → `CREATE_TEAM`，`2` → `GROUP_PURCHASE`，`3` → `LEAGUES`

## 注意事项

- `ListCampaignsOfClub` 返回的活动不保证按时间排序
- 活动描述 (`post.content`) 可能包含 emoji 和富文本格式
- 时间均为 UTC，需转为 UTC+8 展示

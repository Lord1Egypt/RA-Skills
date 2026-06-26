---
name: zhide-offer
description: 职得Offer校园求职助手。调用职得Offer MCP接口查询校园招聘岗位和面试经验。
当用户提到以下关键词时触发：
- 查岗位、找工作、搜职位、招聘信息、校招、实习
- 查面经、面试经验、面试题、面试复盘、面经详情
- 职得Offer、offer、求职、笔试、面试准备
支持功能：搜索岗位列表、查看岗位详情、搜索面经列表、查看面经详情。
---

# 职得Offer校园求职技能

通过 MCP 协议调用职得Offer接口，查询校招岗位和面试经验。

适合的典型场景：
- 想找某个方向的校招或实习岗位
- 想看某公司某岗位的真实面经
- 想快速做面试前的信息收集

## 配置

API Key 从配置文件或环境变量读取，不硬编码：

```js
const KEY = process.env.ZHIDE_OFFER_KEY || require('./config.json').zhideOfferKey;
```

用户需在 `scripts/config.json` 中配置：

```json
{ "zhideOfferKey": "ofk_你的key" }
```

## MCP 调用规范

- **端点**：`https://offer.yxzrkj.cn/mcp`（POST）
- **Headers**：`Content-Type: application/json`、`Accept: application/json, text/event-stream`、`Authorization: Bearer <KEY>`
- **每次调用前需先 initialize 握手**（无状态，每次独立 POST）
- 脚本已封装，直接调用即可

## 快速使用

```bash
# 查岗位
node ~/.openclaw/skills/zhide-offer/scripts/jobs_search.js 数据产品经理

# 看岗位详情
node ~/.openclaw/skills/zhide-offer/scripts/jobs_get.js <岗位ID>

# 查面经
node ~/.openclaw/skills/zhide-offer/scripts/interviews_search.js 产品经理 --company 字节跳动 --tag 校招 --limit 5

# 看完整面经
node ~/.openclaw/skills/zhide-offer/scripts/interviews_get.js <面经ID>
```

如果想用统一入口，也可以：

```bash
bash ~/.openclaw/skills/zhide-offer/scripts/zhide_offer.sh jobs-search 产品经理 --size 3
bash ~/.openclaw/skills/zhide-offer/scripts/zhide_offer.sh interviews-search 产品经理 --limit 2
```

## 工作流

### 搜索岗位
1. 运行 `scripts/jobs_search.js`，传入 `keyword`（可选 `company`/`city`/`pageSize`）
2. 结果在 `result.structuredContent.data.items[]`，字段见 references/api.md
3. 如需详情，用岗位 `id` 运行 `scripts/jobs_get.js`

### 搜索面经
1. 运行 `scripts/interviews_search.js`，传入 `position_query`（精准单词组效果最好，多词组合可能返回空）
2. 结果在 `result.structuredContent.data.items[]`
3. 如需全文，用面经 `id` 运行 `scripts/interviews_get.js`

## 注意事项

- 发布版本不要携带真实 `scripts/config.json`，公开包只保留模板文件
- `position_query` 用单一关键词（如"数据产品经理"），不要堆多个词
- `interviews.search` 响应较慢（约8秒），正常现象
- 每日调用限额200次（account.entitlements 可查剩余）
- 详细字段说明见 `references/api.md`

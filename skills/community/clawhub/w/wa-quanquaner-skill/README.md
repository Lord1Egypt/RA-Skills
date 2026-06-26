# 🧧 WaQuanquaner — 外卖红包每小时实时挖掘助手

> 挖券券儿 — 一个轻量级 Agent Skill，每小时自动扫描美团、饿了么、京东三大外卖平台，实时挖掘最新的外卖红包和优惠活动。**一个链接挖取当日所有隐藏活动，方便、省心、省钱！**

## ✨ 特性

- **一个链接搞定** — 不用一个个找，打开就能全部领
- **每小时自动刷新** — 红包活动实时更新，不会错过最新优惠
- **三大外卖平台** — 美团、饿了么、京东全覆盖
- **隐藏红包挖掘** — 很多限时活动 App 里找不到，这里都有
- **一键复制** — 复制链接到微信打开，领完再点餐
- **三种渲染格式** — 微信文本 / 飞书消息卡片 / 纯文本
- **自然语言触发** — "外卖红包"、"饿了么优惠"等自然语言自动触发
- **隐私安全** — 不包含任何密钥，不收集个人信息

## 📌 使用须知

- **覆盖平台**：美团、饿了么、京东
- **推送内容**：仅外卖红包和优惠活动
- **更新频率**：每小时自动扫描一次
- **智能展示**：如果某个平台当前没有优质活动，该平台不会出现在结果中

## 📦 文件结构

```
WaQuanquaner-skill/
├── SKILL.md                # Skill 定义文件
├── index.js                # 入口文件，导出 WaQuanquaner 类
├── README.md               # 本文件
└── scripts/
    ├── config.js           # 配置（地址、平台映射、触发关键词）
    ├── query.js            # 查询引擎
    ├── render.js           # 渲染引擎（微信/飞书/纯文本三种格式）
    └── triggers.js         # 触发解析器（自然语言意图识别）
```

## 🚀 快速使用

### 作为 Agent Skill 使用

将 `WaQuanquaner-skill` 目录放入你的 Agent Skills 目录，Agent 会自动识别并加载。

**触发示例：**
- "有什么外卖红包" → 查询全部平台优惠
- "饿了么有什么红包" → 仅查询饿了么
- "美团外卖优惠" → 仅查询美团
- "点外卖怎么省钱" → 查询全部平台

### 作为 Node.js 模块使用

```javascript
const { WaQuanquaner } = require('./WaQuanquaner-skill');

// 创建实例
const wqq = new WaQuanquaner();

// 查询活动（微信格式）
const result = await wqq.query({ format: 'wechat' });
console.log(result.text);

// 查询指定格式
const feishuResult = await wqq.query({ format: 'feishu' });

// 一站式：解析自然语言 → 查询 → 渲染
const handled = await wqq.handleInput('饿了么有什么红包');
if (handled.handled) {
  console.log(handled.text);
}
```

### 自定义接口地址

```javascript
const wqq = new WaQuanquaner({
  compactApiUrl: 'https://your-server.com/api/v1/activities/channel/skill_compact',
  defaultFormat: 'feishu',
});
```

## 📤 输出格式预览

```
🧧 今日外卖隐藏红包已挖出！（4月10日）

🔗 一键领全部红包：
   https://waquanquaner.cn/go

👆 一个链接，挖取当日所有隐藏活动

💡 今日必领：
   🔵 饿了么·红包节天天领（今日主角）
      → 周末大餐红包提前抢，晚上就能用

💬 听说今天有人用红包点了一顿霸王餐

复制到微信打开 → 一个个领 → 再点餐
```

## ⚙️ 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `COMPACT_API_URL` | 推荐数据接口地址 | `https://waquanquaner.cn/api/v1/activities/channel/skill_compact` |
| `LANDING_PAGE_URL` | 中转页地址 | `https://waquanquaner.cn/go` |

## 🔒 安全说明

- 本 Skill **不包含**任何密钥或敏感信息
- 不收集用户个人信息
- 所有网络通信使用 HTTPS 加密

## 📄 许可证

MIT-0

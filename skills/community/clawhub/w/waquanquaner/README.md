# 🧧 挖券券儿 — 外卖红包优惠券领券神器

> 一个链接挖取当日所有隐藏外卖红包，美团/饿了么/京东全覆盖，无需注册无需 API Key

## ✨ 特性

- **零门槛** — 无需 API Key、无需注册、装完即用
- **一个链接搞定** — 不用一个个找，打开就能全部领
- **三大外卖平台** — 美团、饿了么、京东全覆盖
- **隐藏红包挖掘** — 限时活动 App 里找不到的，这里有
- **一键复制** — 复制链接到微信打开，领完再点餐
- **多格式输出** — 微信文本 / 飞书消息卡片 / 纯文本
- **自然语言触发** — "外卖红包"、"饿了么优惠"、"领券"等自动触发
- **隐私安全** — 不包含任何密钥，不收集个人信息

## 🚀 安装

```bash
npx clawhub install waquanquaner
```

安装后重启 Agent 即可使用，无需任何额外配置。

## 📌 使用方式

### Agent Skill 触发

安装后，Agent 会自动识别以下场景并调用：

| 你说 | 效果 |
|------|------|
| "有什么外卖红包" | 查询全部平台优惠 |
| "饿了么有什么红包" | 查询饿了么优惠 |
| "美团外卖优惠" | 查询美团优惠 |
| "京东外卖领券" | 查询京东外卖优惠 |
| "点外卖怎么省钱" | 查询全部平台 |
| "今天吃什么" | 顺便领个券 |

### 直接调用 API

```bash
curl -s "https://waquanquaner.cn/api/v1/activities/channel/skill_compact"
```

### Node.js 模块

```javascript
const { WaQuanquaner } = require('waquanquaner-skill');

const wqq = new WaQuanquaner();

// 查询活动（微信格式）
const result = await wqq.query({ format: 'wechat' });
console.log(result.text);

// 飞书格式
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
   🔵 饿了么·大额红包限时领（热门推荐）
      → 领券下单立减，无门槛叠加用

💬 听说今天有人用红包点了一顿霸王餐

复制到微信打开 → 一个个领 → 再点餐
```

## 📦 文件结构

```
waquanquaner-skill/
├── SKILL.md                # Skill 定义文件
├── index.js                # 入口文件，导出 WaQuanquaner 类
├── package.json            # 包配置
├── README.md               # 本文件
└── scripts/
    ├── config.js           # 配置（地址、平台映射、触发关键词）
    ├── query.js            # 查询引擎
    ├── render.js           # 渲染引擎（微信/飞书/纯文本）
    └── triggers.js         # 触发解析器（自然语言意图识别）
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
- allowed-tools 仅限访问 `waquanquaner.cn` 域名

## 📄 许可证

MIT-0
# 🔍 闲鱼搜索技能 (xianyu-search)

一键搜索闲鱼、转转、拍拍等二手平台商品，智能筛选推荐！

## 📖 快速链接
| 链接 | 说明 |
|------|------|
| [闲鱼官网](https://www.goofish.com) | 阿里巴巴旗下二手交易平台 |
| [转转官网](https://www.zhuanzhuan.com) | 58 同城旗下二手平台 |
| [拍拍官网](https://www.paipai.com) | 京东旗下二手平台 |
| [验货宝](https://www.yanhuobao.com) | 第三方验机服务 |
| [ClawHub 技能页](https://clawhub.ai/skills/xianyu-search) | 技能市场页面 |
| [OpenClaw 文档](https://docs.openclaw.ai) | 开发文档 |

---

## ✨ 功能特点

- 🎯 **精准搜索** - 根据预算、成色、电池等条件筛选
- 🏆 **信用筛选** - 优先推荐信用好的卖家
- 📊 **格式化输出** - 表格展示，一目了然
- 💡 **购买建议** - 提供验机清单和砍价话术
- 🔗 **多平台支持** - 闲鱼/转转/拍拍

---

## 🚀 快速使用

### 方式 1：自然语言触发

直接说：
```
帮我找闲鱼上的 MacBook Air M1 预算 2300
```

```
搜索二手 iPhone 13 预算 3000 电池 85 以上
```

```
闲鱼上有没有 9 成新的 PS5
```

### 方式 2：参数化调用

```javascript
const { searchProducts, generateReport } = require('./search');

const result = await searchProducts({
  keyword: 'MacBook Air M1 2020',
  budget: 2300,
  budgetMax: 2500,
  condition: '9 成新',
  batteryMin: 85,
  requireNoRepair: true,
  requireGoodCredit: true,
  platform: 'xianyu',
  location: '北京',
});
```

---

## 📋 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `keyword` | string | ✅ | - | 搜索关键词 |
| `budget` | number | ✅ | - | 预算上限（元） |
| `budgetMax` | number | ❌ | budget+200 | 最高接受价格 |
| `condition` | string | ❌ | '9 成新' | 成色要求 |
| `batteryMin` | number | ❌ | 80 | 最低电池健康度% |
| `requireNoRepair` | boolean | ❌ | true | 要求无拆修 |
| `requireGoodCredit` | boolean | ❌ | true | 要求卖家信用好 |
| `platform` | string | ❌ | 'xianyu' | 平台：xianyu/zhuanzhuan/paipai |
| `location` | string | ❌ | '' | 优先地区 |

---

## 📤 输出示例

```markdown
## 🎯 闲鱼搜索结果：MacBook Air M1 2020

**搜索条件**：预算 ¥2300-2500 | 成色 9 成新 | 电池≥85%

### 🏆 首选推荐

| 价格 | 地区 | 电池 | 信用 | 亮点 | 链接 |
|------|------|------|------|------|------|
| **¥2150** | 山东 | 循环 8 次 | 百分百好评 | 电池超新 | [查看](url) |
| **¥2295** | 四川 | 未说明 | 卖家信用极好 | 刚降价 | [查看](url) |
| **¥2318** | 北京 | 89% | 百分百好评 | 可退换 | [查看](url) |

### 💡 购买建议

**验机要点**：
- [ ] 电池健康度截图
- [ ] 视频验机
- [ ] 确认无 ID 锁
- [ ] 检查序列号

**砍价话术**：
"你好，诚心想买，预算只有 2300..."
```

---

## 🛠️ 文件结构

```
xianyu-search/
├── SKILL.md          # 技能配置
├── search.js         # 主搜索脚本
├── templates.js      # 输出模板（可选）
├── utils.js          # 工具函数（可选）
├── EXAMPLES.md       # 使用示例
└── README.md         # 本文件
```

---

## ⚠️ 注意事项

1. **反爬虫限制**
   - 闲鱼等平台有强反爬虫机制
   - 无法直接抓取商品详情
   - 提供搜索链接，用户自行点击查看
   - 🔗 [闲鱼搜索页](https://www.goofish.com/search) | [转转搜索](https://www.zhuanzhuan.com/zz/pc/list) | [拍拍搜索](https://www.paipai.com/so)

2. **实时性**
   - 二手商品价格波动快
   - 推荐结果仅供参考
   - 建议尽快联系卖家

3. **交易安全**
   - 走平台担保交易，不要直接转账
   - 保留聊天记录和交易凭证
   - 🔗 [闲鱼安全中心](https://www.goofish.com/safety) | [防骗指南](https://www.goofish.com/guide)

4. **验机建议**
   - 要求视频验机
   - 确认电池健康度
   - 检查序列号
   - 🔗 [验货宝服务](https://www.yanhuobao.com) | [爱回收](https://www.aihuishou.com)

5. **维权渠道**
   - 🔗 [闲鱼客服](https://www.goofish.com/help) | [12315 投诉](https://www.12315.cn)

---

## 🔧 扩展建议

### 可以添加的功能

- [ ] 浏览器自动化抓取商品列表
- [ ] 定时监控低价货源
- [ ] 价格历史追踪
- [ ] 卖家信用 API 查询
- [ ] 验货宝集成
- [ ] 面交地点推荐

### 可以支持的平台

- [ ] 转转官方验
- [ ] 拍拍严选
- [ ] 爱回收
- [ ] 找靓机
- [ ] 花粉儿（二手服饰）

---

## 📝 更新日志

- **v1.0.0** (2026-03-23)
  - 初始版本
  - 支持闲鱼搜索
  - 支持参数化配置
  - 格式化输出

---

## 📞 反馈与建议

有问题或建议欢迎反馈！

---

**Happy Shopping! 🛒**

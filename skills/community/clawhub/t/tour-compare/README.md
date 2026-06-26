# 🦐 tour-compare - 跟团游商品对比助手

> 帮用户快速对比 OTA 平台跟团游商品，提供智能推荐和避坑建议

## ✨ 功能特性

- 📊 **横向对比** - 相同路线不同商家，一眼看出哪个更值
- 🎯 **智能推荐** - 根据目的地特点和人群特征给出建议
- ⚠️ **避坑提醒** - 识别低价团、购物团、隐形消费
- 💡 **决策辅助** - 结构化分析 + 一句话结论
- 🔗 **链接抓取** - 支持携程/飞猪/同程 URL 直接输入
- 🖼️ **导出图片** - 一键生成对比报告 PNG，方便分享

## 🚀 快速开始

### 安装

```bash
cd skills/tour-compare
npm install

# 可选：安装高级功能依赖（链接抓取 + 图片导出）
npm install puppeteer cheerio canvas
```

### 基本用法

```bash
# 对比商品（JSON 格式）
./scripts/compare.sh compare \
  '{"platform":"携程","title":"云南 6 日游","price":3299,"rating":4.8,"shoppingStops":0}' \
  '{"platform":"飞猪","title":"云南 6 日游","price":2899,"rating":4.6,"shoppingStops":4}'

# 对比商品（URL 链接）
./scripts/compare.sh compare https://ctrip.com/p/123456 https://fliggy.com/p/789012

# 导出对比报告图片
./scripts/compare.sh compare <商品 1> <商品 2> --export report.png

# 智能推荐
./scripts/compare.sh recommend --destination 云南 --budget 5000 --group 老人 --days 6

# 深度分析
./scripts/compare.sh analyze '{"platform":"携程","title":"云南 6 日游","price":3299,"rating":4.8}' --deep
```

## 📖 使用文档

详见 [examples/usage.md](examples/usage.md)

## 🎯 四种模式

| 模式 | 命令 | 用途 |
|------|------|------|
| 对比 | `compare` | 对比多个商品，输出推荐排序 |
| 推荐 | `recommend` | 根据需求推荐商品 |
| 分析 | `analyze` | 深度分析单个商品 |
| 筛选 | `filter` | 按条件筛选商品 |

## 👥 支持人群

- 老人 - 注重轻松、安全、少购物
- 亲子 - 注重亲子设施、安全、趣味性
- 蜜月 - 注重私密性、品质、浪漫体验
- 学生 - 注重性价比、自由度、社交
- 朋友 - 注重自由度、体验、拍照
- 商务 - 注重品质、效率、服务

## 🛠 技术栈

- Node.js 18+
- Commander (CLI)
- Chalk (彩色输出)
- Puppeteer (网页抓取，开发中)
- Cheerio (HTML 解析，开发中)

## 📁 项目结构

```
skills/tour-compare/
├── SKILL.md              # Skill 文档
├── README.md             # 使用说明
├── package.json          # 依赖配置
├── scripts/
│   └── compare.sh        # CLI 入口
├── src/
│   ├── index.js          # 主入口
│   ├── crawler/          # 数据抓取 (开发中)
│   ├── analyzer/         # 分析引擎
│   │   ├── comparator.js # 对比逻辑
│   │   ├── recommender.js# 推荐逻辑
│   │   └── analyzer.js   # 分析逻辑
│   ├── ui/
│   │   └── renderer.js   # 输出渲染
│   └── config/
│       └── personas.js   # 人群画像
└── examples/
    └── usage.md          # 使用示例
```

## 🔮 后续迭代

- [x] 实现 OTA 平台爬虫（携程/飞猪/同程）
- [x] 支持链接直接输入
- [x] 导出分享功能
- [ ] 历史价格追踪
- [ ] 截图 OCR 识别
- [ ] 行程地图可视化
- [ ] 用户评价情感分析

## 📝 License

MIT

---

_Made with 🦐 by 小虾_

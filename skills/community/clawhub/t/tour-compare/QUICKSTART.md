# 🦐 tour-compare 快速入门

> 3 分钟上手，开始对比旅游商品

## 📦 1. 安装

```bash
# 进入项目目录
cd ~/.openclaw/workspace/skills/tour-compare

# 安装基础依赖
npm install

# 可选：安装高级功能（链接抓取 + 图片导出）
npm install puppeteer cheerio canvas
```

## 🚀 2. 第一个对比

### 方式 A: JSON 输入（无需额外依赖）

```bash
./scripts/compare.sh compare \
  '{"platform":"携程","title":"云南 6 日游","price":3299,"rating":4.8,"shoppingStops":0}' \
  '{"platform":"飞猪","title":"云南 6 日游","price":2899,"rating":4.6,"shoppingStops":4}'
```

**输出示例**:
```
📊 线路对比报告
==================================================

✅ 推荐"云南 6 日游" - 评分高、0 购物纯玩

对比总览

💰 价格	¥3299	¥2899
⭐ 评分	4.8	4.6
🛍️ 购物店	0	4
📊 综合评分	87 分	52 分

🥇 1. 云南 6 日游 - 87 分
🥈 2. 云南 6 日游 - 52 分

⚠️  避坑提醒
🔴 含 4 个购物店，注意隐形消费
```

### 方式 B: URL 输入（需安装 puppeteer）

```bash
./scripts/compare.sh compare \
  https://ctrip.com/p/123456 \
  https://fliggy.com/p/789012
```

## 🎯 3. 常用场景

### 带老人出行

```bash
./scripts/compare.sh compare <商品 1> <商品 2> --group 老人
```

**关注点**: 少购物、轻松行程、医疗便利

### 蜜月旅行

```bash
./scripts/compare.sh compare <商品 1> <商品 2> --group 蜜月
```

**关注点**: 私密性、高星酒店、浪漫体验

### 亲子游

```bash
./scripts/compare.sh compare <商品 1> <商品 2> --group 亲子
```

**关注点**: 亲子设施、安全、趣味性

### 学生党

```bash
./scripts/compare.sh compare <商品 1> <商品 2> --group 学生
```

**关注点**: 性价比、自由度

## 🔍 4. 其他功能

### 智能推荐

```bash
./scripts/compare.sh recommend \
  --destination 云南 \
  --budget 5000 \
  --group 老人 \
  --days 6
```

### 深度分析

```bash
./scripts/compare.sh analyze \
  '{"platform":"携程","title":"云南 6 日游","price":3299,"rating":4.8}' \
  --deep
```

### 导出图片

```bash
./scripts/compare.sh compare <商品 1> <商品 2> --export report.png
```

## 💡 5. 数据格式

### 最小格式（能用）
```json
{
  "platform": "携程",
  "title": "云南 6 日游",
  "price": 3299,
  "rating": 4.8
}
```

### 完整格式（推荐）
```json
{
  "platform": "携程",
  "title": "云南昆明大理丽江 6 日游",
  "price": 3299,
  "rating": 4.8,
  "reviewCount": 2341,
  "shoppingStops": 0,
  "hotelStars": 4,
  "days": 6,
  "selfPaidItems": [{"name": "索道", "price": 180}]
}
```

## ❓ 6. 常见问题

### Q: 链接抓取失败？
**A**: 
1. 检查是否安装：`npm install puppeteer`
2. 使用 `--no-fetch` 强制 JSON 模式
3. 检查网络连接

### Q: 图片导出失败？
**A**: 
1. 安装 canvas: `npm install canvas`
2. macOS 可能需要：`brew install pkg-config cairo pango libpng jpeg giflib librsvg`

### Q: 如何查看帮助？
**A**: 
```bash
./scripts/compare.sh --help
./scripts/compare.sh compare --help
```

## 📖 7. 下一步

- 📖 完整文档：[examples/usage.md](examples/usage.md)
- 📝 更新日志：[CHANGELOG.md](CHANGELOG.md)
- 🛠 技术文档：[SKILL.md](SKILL.md)

---

**Happy Comparing! 🦐**

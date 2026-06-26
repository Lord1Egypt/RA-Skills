# tour-compare 使用示例

## 快速开始

### 1. 安装依赖

```bash
cd skills/tour-compare
npm install

# 可选：安装高级功能依赖
npm install puppeteer cheerio canvas
```

### 2. 使用 CLI

```bash
# 通过脚本运行
./scripts/compare.sh <command> [options]

# 或直接使用 node
node src/index.js <command> [options]
```

---

## 模式 1: 对比商品 (compare)

### 命令行方式 - JSON 输入

```bash
# 对比两个商品（JSON 格式）
./scripts/compare.sh compare \
  '{"platform":"携程","title":"云南 6 日游","price":3299,"rating":4.8,"shoppingStops":0,"hotelStars":4}' \
  '{"platform":"飞猪","title":"云南 6 日游","price":2899,"rating":4.6,"shoppingStops":4,"hotelStars":3}'
```

### 命令行方式 - URL 输入（需要安装 puppeteer）

```bash
# 对比两个链接
./scripts/compare.sh compare \
  https://ctrip.com/p/123456 \
  https://fliggy.com/p/789012

# 混合输入（JSON + URL）
./scripts/compare.sh compare \
  '{"platform":"携程","title":"云南 6 日游","price":3299,"rating":4.8}' \
  https://fliggy.com/p/789012
```

### 导出图片

```bash
# 导出对比报告为 PNG 图片（需要安装 canvas）
./scripts/compare.sh compare <商品 1> <商品 2> --export report.png

# 带人群参数 + 导出
./scripts/compare.sh compare <商品 1> <商品 2> --group 老人 --export report.png
```

### 带人群参数

```bash
./scripts/compare.sh compare \
  '{"platform":"携程","title":"云南 6 日游","price":3299,"rating":4.8,"shoppingStops":0,"hotelStars":4,"days":6}' \
  '{"platform":"飞猪","title":"云南 6 日游","price":2899,"rating":4.6,"shoppingStops":4,"hotelStars":3,"days":6}' \
  --group 老人
```

### 输出格式

```bash
# Markdown 格式（默认）
./scripts/compare.sh compare ... --output markdown

# 纯文本格式
./scripts/compare.sh compare ... --output text

# JSON 格式（适合程序处理）
./scripts/compare.sh compare ... --output json
```

---

## 模式 2: 智能推荐 (recommend)

### 基本用法

```bash
./scripts/compare.sh recommend \
  --destination 云南 \
  --budget 5000 \
  --group 老人 \
  --days 6
```

### 筛选偏好

```bash
./scripts/compare.sh recommend \
  --destination 三亚 \
  --budget 8000 \
  --group 蜜月 \
  --preferences 无购物，高星酒店
```

---

## 模式 3: 深度分析 (analyze)

```bash
./scripts/compare.sh analyze \
  '{"platform":"携程","title":"云南 6 日游","price":3299,"rating":4.8,"shoppingStops":0,"hotelStars":4,"hotelStandard":"4 钻","selfPaidItems":[{"name":"索道","price":180}],"days":6}' \
  --deep
```

---

## 模式 4: 条件筛选 (filter)

```bash
./scripts/compare.sh filter \
  --destination 云南 \
  --no-shopping \
  --direct-flight \
  --min-rating 4.5
```

---

## 在对话中使用

未来可以直接在对话中这样用：

```
用户：帮我对比这两个云南游
https://ctrip.com/p/123456
https://fliggy.com/p/789012

助手：[自动抓取 + 对比，输出报告]
```

```
用户：我想带父母去云南玩，预算 5000，有什么推荐？

助手：[理解需求 → 搜索匹配 → 输出推荐 Top3]
```

```
用户：这个团怎么样？https://ctrip.com/p/123456

助手：[深度分析商品，输出优缺点 + 避坑提醒]
```

---

## 商品数据格式

### 完整格式

```json
{
  "platform": "携程",
  "title": "云南昆明大理丽江 6 日游",
  "price": 3299,
  "rating": 4.8,
  "reviewCount": 2341,
  "shoppingStops": 0,
  "hotelStars": 4,
  "hotelStandard": "4 钻",
  "days": 6,
  "nights": 5,
  "selfPaidItems": [
    {"name": "索道", "price": 180},
    {"name": "电瓶车", "price": 50}
  ],
  "cancelPolicy": "免费取消"
}
```

### 简化格式（最小可用）

```json
{
  "platform": "携程",
  "title": "云南 6 日游",
  "price": 3299,
  "rating": 4.8,
  "shoppingStops": 0
}
```

---

## 支持的平台

| 平台 | URL 示例 | 支持状态 |
|------|---------|---------|
| 携程 | ctrip.com/p/xxx | ✅ 支持 |
| 飞猪 | fliggy.com/p/xxx | ✅ 支持 |
| 同程 | ly.com/xxx | ✅ 支持 |
| 马蜂窝 | mafengwo.cn/xxx | 🔲 计划中 |
| 穷游 | qyer.com/xxx | 🔲 计划中 |

---

## 支持人群

| 人群 | 权重偏好 |
|------|---------|
| 老人 | 少购物、轻松行程、医疗便利 |
| 亲子 | 亲子设施、安全、趣味性 |
| 蜜月 | 私密性、高星酒店、浪漫体验 |
| 学生 | 性价比、自由度、社交属性 |
| 朋友 | 自由度、体验、拍照 |
| 商务 | 品质、效率、服务 |

---

## 帮助信息

```bash
# 查看主帮助
./scripts/compare.sh --help

# 查看子命令帮助
./scripts/compare.sh compare --help
./scripts/compare.sh recommend --help
./scripts/compare.sh analyze --help
```

---

## 常见问题

### Q: 链接抓取失败怎么办？

A: 可能的原因：
1. 未安装 puppeteer：`npm install puppeteer`
2. 网络问题：检查网络连接
3. 平台不支持：目前仅支持携程/飞猪/同程
4. 反爬虫：使用 `--no-fetch` 强制 JSON 模式

### Q: 图片导出失败？

A: 需要安装 canvas 库：
```bash
npm install canvas
```

macOS 可能需要先安装：
```bash
brew install pkg-config cairo pango libpng jpeg giflib librsvg
```

### Q: 如何自定义评分权重？

A: 编辑 `src/config/personas.js` 文件，调整各人群的权重配置。

---

## 下一步

- 查看完整文档：[SKILL.md](../SKILL.md)
- 报告问题：[GitHub Issues](https://github.com/openclaw/openclaw/issues)
- 贡献代码：[Pull Requests](https://github.com/openclaw/openclaw/pulls)

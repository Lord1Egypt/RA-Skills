# tour-compare 输入方式指南

## 📥 三种输入方式

### 1️⃣ URL 链接输入

**支持的 OTA 平台**：

| 平台 | 域名示例 | 状态 |
|------|---------|------|
| ✈️ **携程** | `ctrip.com`、`m.ctrip.com`、`you.ctrip.com` | ✅ 支持 |
| 🐷 **飞猪** | `fliggy.com`、`a.feizhu.com`、`m.fliggy.com` | ✅ 支持 |
| 🐫 **同程** | `ly.com`、`m.ly.com` | ✅ 支持 |
| 🐝 **马蜂窝** | `mafengwo.cn`、`m.mafengwo.cn` | ✅ 支持 |
| 🎒 **穷游** | `qyer.com`、`m.qyer.com`、`product.qyer.com` | ✅ 支持 |
| 🍱 **美团旅行** | `meituan.com`、`travel.meituan.com` | ✅ 支持 |
| 🐮 **途牛** | `tuniu.com`、`m.tuniu.com` | ✅ 支持 |
| 🐘 **驴妈妈** | `lvmama.com`、`m.lvmama.com` | ✅ 支持 |

**使用方法**：
```bash
# 单个链接
./scripts/compare.sh compare https://a.feizhu.com/0HeTSg

# 多个链接对比
./scripts/compare.sh compare \
  https://a.feizhu.com/0HeTSg \
  https://a.feizhu.com/3PT4IS

# 混合输入（JSON + URL）
./scripts/compare.sh compare \
  '{"platform":"飞猪","title":"云南 6 日游","price":3299}' \
  https://a.feizhu.com/0HeTSg
```

**自动识别信息**：
- ✅ 商品标题
- ✅ 价格
- ✅ 评分
- ✅ 评价数
- ✅ 酒店星级
- ✅ 购物店数量
- ✅ 行程天数

---

### 2️⃣ 截图 OCR 识别（新功能！）

**支持的截图**：
- 📱 手机截图（携程/飞猪/同程 App）
- 💻 网页截图（OTA 平台商品详情页）

**识别内容**：
- ✅ 价格（¥XXX 或 XXX 元）
- ✅ 评分（X.X 分）
- ✅ 评价数（XXX 条）
- ✅ 行程（X 天 X 晚）
- ✅ 酒店星级（X 钻）
- ✅ 购物店数量
- ✅ 特色标签（纯玩/小团/独立团等）

**使用方法**：

#### 方式 A：命令行
```bash
# 单张截图识别
./scripts/compare.sh recognize screenshot.png

# 两张截图对比
./scripts/compare.sh compare-images screenshot1.png screenshot2.png
```

#### 方式 B：直接发送截图（推荐）
在对话中直接发送截图，系统会自动识别并对比。

**示例对话**：
```
用户：[发送两张商品截图]

助手：📊 正在识别截图...

✅ 截图 1 识别成功：
   云南大理丽江 4 天 3 晚纯玩小团
   价格：¥558.8
   评分：4.9 分
   酒店：3 钻
   特色：纯玩无购物、15 人小团

✅ 截图 2 识别成功：
   丽江大理香格里拉 5 天 4 晚 6 人小团
   价格：¥680
   评分：5.0 分
   酒店：4 钻
   特色：纯玩无购物、6 人小团

📊 对比分析...
[输出完整对比报告]
```

---

### 3️⃣ JSON 格式输入（传统方式）

**最小格式**：
```json
{
  "platform": "飞猪",
  "title": "云南 6 日游",
  "price": 3299,
  "rating": 4.8
}
```

**完整格式**：
```json
{
  "platform": "飞猪",
  "title": "云南大理丽江 4 天 3 晚纯玩小团",
  "price": 558.8,
  "rating": 4.9,
  "reviewCount": 230,
  "shoppingStops": 0,
  "hotelStars": 3,
  "days": 4,
  "groupSize": 15,
  "features": ["玉龙雪山", "洱海", "亲子游", "无自费", "赠保险"],
  "goodRate": "96%"
}
```

---

## 🎯 推荐使用方式

### 优先级排序：
1. **URL 链接** ⭐⭐⭐⭐⭐ - 最准确，自动抓取
2. **截图 OCR** ⭐⭐⭐⭐ - 方便，但识别率受截图质量影响
3. **JSON 输入** ⭐⭐⭐ - 手动输入，适合测试

### 场景建议：

| 场景 | 推荐方式 | 理由 |
|------|---------|------|
| 有商品链接 | URL 链接 | 自动抓取，信息最全 |
| 朋友分享截图 | 截图 OCR | 无需手动输入 |
| 对比多个商品 | URL 链接 | 批量抓取，快速对比 |
| 测试/开发 | JSON 输入 | 灵活控制数据 |

---

## 📸 截图识别技巧

### 拍摄建议：
1. **截取完整信息** - 包含价格、评分、标题、特色标签
2. **清晰无模糊** - 文字清晰可辨
3. **避免反光** - 屏幕截图优于拍照
4. **横屏截图** - 包含更多信息

### 识别区域：
```
┌─────────────────────────┐
│  商品标题（最重要）     │
│  ⭐⭐⭐⭐⭐ 4.9 分        │
│  已售 300+               │
│                         │
│  ¥558.8 起              │
│  原价¥640               │
│                         │
│  4 天 3 晚               │
│  15 人小团              │
│  3 钻酒店                │
│                         │
│  纯玩无购物 ✓           │
│  赠保险 ✓               │
└─────────────────────────┘
```

---

## ⚠️ 注意事项

### URL 链接：
- ✅ 支持短链接（飞猪 a.feizhu.com）
- ⚠️ 需要网络连接
- ⚠️ 部分平台可能反爬虫

### 截图 OCR：
- ✅ 支持中文识别
- ⚠️ 识别率受截图质量影响
- ⚠️ 复杂背景可能影响识别
- ⚠️ 首次使用需要下载语言包（约 20MB）

### JSON 输入：
- ✅ 最可靠
- ⚠️ 需要手动输入
- ⚠️ 格式错误会失败

---

## 🛠️ 安装依赖

### 基础功能（JSON 输入）
```bash
cd skills/tour-compare
npm install
```

### URL 抓取功能
```bash
npm install puppeteer cheerio
```

### 截图 OCR 功能
```bash
npm install tesseract.js
```

### 全部功能
```bash
npm install puppeteer cheerio canvas tesseract.js
```

---

## 📖 使用示例

### 示例 1：URL 链接对比
```bash
./scripts/compare.sh compare \
  https://a.feizhu.com/0HeTSg \
  https://a.feizhu.com/3PT4IS \
  --group 亲子
```

### 示例 2：截图对比
```bash
./scripts/compare.sh compare-images \
  screenshot1.png \
  screenshot2.png
```

### 示例 3：混合输入
```bash
./scripts/compare.sh compare \
  https://a.feizhu.com/0HeTSg \
  '{"platform":"携程","title":"云南 6 日游","price":3299,"rating":4.8}'
```

---

## 🎬 快速开始

**最简单的使用方式**：

1. 在对话中直接发送商品链接或截图
2. 系统自动识别并对比
3. 查看对比报告

**无需记忆任何命令！**

---

**Made with 🦐 by 小虾**

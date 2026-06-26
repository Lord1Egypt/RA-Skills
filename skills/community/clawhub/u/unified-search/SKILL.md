---
name: unified-search
description: 统一搜索技能！中文用百度，英文用 DuckDuckGo，加密货币用 CoinGecko
---

# 🔍 Unified Search - 统一搜索技能

**智能融合多种搜索引擎，一个脚本搞定所有搜索！**
- 🇨🇳 中文查询 → 自动用百度
- 🇺🇸 英文查询 → 自动用 DuckDuckGo
- 💰 加密货币 → 自动用 CoinGecko 实时价格

---

## 🚀 快速开始

### 方式1：使用统一智能搜索脚本（最推荐 ⭐⭐⭐⭐⭐⭐）

**自动选择最佳搜索引擎！** 一行命令，智能搞定！

```bash
cd skills/baidu-search

# 中文搜索 → 自动用百度
python scripts/unified_search.py "Python 教程" --format

# 英文搜索 → 自动用 DuckDuckGo
python scripts/unified_search.py "Python tutorial" --format

# 加密货币 → 自动用 CoinGecko
python scripts/unified_search.py "btc价格" --format
```

### 方式2：使用 Playwright 浏览器搜索（推荐 ⭐⭐⭐⭐⭐）

最稳定、最可靠的方式，使用 ClawX 内置的 browser 工具：

```javascript
// 1. 启动浏览器
browser(action="start")

// 2. 打开百度或 Bing
browser(action="open", targetUrl="https://www.baidu.com")
// 或 browser(action="open", targetUrl="https://www.bing.com")

// 3. 获取页面快照
browser(action="snapshot")

// 4. 在搜索框输入关键词（找到搜索框的 ref，如 e12）
browser(action="act", request={
  kind: "type",
  ref: "e12",
  text: "搜索词"
})

// 5. 按回车搜索
browser(action="act", request={
  kind: "press",
  ref: "e12",
  key: "Enter"
})

// 6. 获取搜索结果
browser(action="snapshot")
```

### 方式3：使用智能 Python 脚本搜索（备选）

```bash
cd skills/baidu-search
python scripts/smart_search.py "你的搜索词" --format
```

### 方式4：使用原始百度 Python 脚本

```bash
cd skills/baidu-search
python scripts/baidu_search.py "你的搜索词" --format
```

---

## 📋 功能对比

| 功能 | 统一智能搜索 | Playwright 浏览器 | 智能脚本 | 原始百度 |
|------|------------|-----------------|---------|---------|
| 中文自动用百度 | ✅ | ⭐⭐⭐⭐⭐ 手动 | ✅ | ✅ |
| 英文自动用 DDG | ✅ | ⭐⭐⭐⭐⭐ 手动 | ❌ | ❌ |
| 加密货币实时价 | ✅ | ❌ 需手动 | ✅ | ❌ |
| 多数据源集成 | ✅ 百度+DDG+API | ❌ 单一引擎 | ✅ 百度+Bing+API | ❌ 仅百度 |
| 易用性 | ⭐⭐⭐⭐⭐ 一行命令 | ⭐⭐⭐⭐ 需多步 | ⭐⭐⭐⭐⭐ 一行 | ⭐⭐⭐⭐⭐ 一行 |
| 推荐度 | ⭐⭐⭐⭐⭐⭐ 首选 | ⭐⭐⭐⭐⭐ 备选 | ⭐⭐⭐⭐ 备选 | ⭐⭐⭐ 备选 |

---

## 🎯 触发模式

| 触发短语 | 说明 |
|---------|------|
| 搜索[查询内容] | 使用统一智能搜索 |
| 统一搜索[查询内容] | 使用统一智能搜索 |
| 百度搜索[查询内容] | 使用百度搜索 |
| 浏览器搜索[查询内容] | 使用 Playwright 搜索 |
| baidu-search [查询内容] | 使用百度搜索 |

---

## 💡 最佳实践

### 日常搜索推荐流程

1. **首选**：`unified_search.py` - 自动选择，最方便
2. **备选**：Playwright 浏览器搜索 - 最稳定，可处理验证码
3. **备选**：`smart_search.py` - 百度 + Bing 双保险

### 选择指南

| 场景 | 推荐方式 |
|------|---------|
| 快速搜索任何内容 | unified_search.py |
| 中文内容搜索 | unified_search.py → 百度 |
| 英文内容搜索 | unified_search.py → DuckDuckGo |
| BTC/ETH 价格查询 | unified_search.py → CoinGecko |
| 需要完整网页截图 | Playwright 浏览器搜索 |

---

## 🛠️ 故障排除

### 问题：统一搜索脚本找不到模块

**解决方案**：确保 ddg-search 技能存在于 skills 目录中

```bash
# 检查目录结构
ls C:\Users\opens\.openclaw\workspace\skills\
# 应该能看到 baidu-search 和 ddg-search
```

### 问题：DuckDuckGo 搜索失败

**解决方案**：安装 duckduckgo-search 库

```bash
pip install duckduckgo-search
# 或者在 ddg-search 目录中安装
cd skills/ddg-search
pip install -r requirements.txt
```

### 问题：百度搜索遇到验证码

**解决方案**：
- 使用 Playwright 浏览器搜索方式（可以人工处理验证码）
- 或者使用 unified_search.py，它会自动降级到 DuckDuckGo

---

## 📁 目录结构

```
skills/baidu-search/
├── SKILL.md                      # 本文件
├── README.md                     # 用户友好的说明
├── OPTIMIZATION_SUMMARY.md       # 优化总结
├── requirements.txt              # Python 依赖
├── example_usage.js              # 使用示例
├── quick_test.py                 # 快速测试
└── scripts/
    ├── unified_search.py         # ⭐ 统一智能搜索（推荐）
    ├── smart_search.py           # 智能搜索脚本
    └── baidu_search.py           # 原始百度脚本
```

---

## 🔧 依赖安装

如需使用 Python 脚本搜索方式：

```bash
cd skills/baidu-search
pip install requests beautifulsoup4

# 如果使用统一搜索，还需要安装 DuckDuckGo 依赖
cd ../ddg-search
pip install -r requirements.txt
```

---

## ✨ 统一搜索特色功能

1. **🧠 智能语言检测**
   - 自动识别中文/英文查询
   - 选择最佳搜索引擎

2. **💰 加密货币支持**
   - BTC/ETH/比特币/以太坊自动识别
   - CoinGecko 实时价格
   - 美元 + 人民币双币种

3. **🔄 自动 Fallback**
   - 百度失败 → 自动用 DDG
   - DDG 失败 → 自动用百度
   - 双重保障

4. **📊 标明来源**
   - 每个结果显示来源（百度/DuckDuckGo/CoinGecko）
   - 清楚知道数据来自哪里

---

**统一搜索，一个脚本搞定所有！首选 unified_search.py！** 🎉

# 🔍 Unified Search - 统一智能搜索！

> 中文用百度，英文用 DuckDuckGo，加密货币用 CoinGecko —— 一个技能，搞定所有搜索！

---

## 🚀 这是什么？

这是 OpenClaw 的**统一智能搜索神器**，自动识别查询类型，调用最合适的搜索引擎！

**小白直接用，零门槛！** 说句话就搞定，剩下的交给它！

---

## ✨ 为什么你一定要装？

### 🎯 三种智能搜索模式，总有一款适合你

| 方式 | 特点 | 推荐度 |
|------|------|--------|
| **统一智能搜索** | 自动语言检测 + 智能选择引擎 | ⭐⭐⭐⭐⭐⭐ 首选首选！ |
| **智能 Python 脚本** | 百度 + Bing + CoinGecko 三保险 | ⭐⭐⭐⭐ 备选 |
| **Playwright 浏览器搜索** | 最稳定、能处理验证码 | ⭐⭐⭐⭐ 备选 |

### 💪 强大功能
- ✅ **中文自动用百度** - 中文搜索最懂
- ✅ **英文自动用 DuckDuckGo** - 隐私保护 + 英文内容
- ✅ **加密货币自动用 CoinGecko** - 实时价格，精准可靠
- ✅ **自动 Fallback** - 百度失败用 DDG，DDG 失败用百度
- ✅ **张嘴就来** - 自然语言触发，零技术门槛
- ✅ **结构化结果** - 标题、链接、摘要，一目了然
- ✅ **来源标记** - 清楚知道结果来自哪个引擎

---

## 🎯 怎么用？（首选方式，零门槛！）

### ✨ 方式1：统一智能搜索（最推荐！⭐⭐⭐⭐⭐⭐）

自动识别查询语言，智能选择搜索引擎！

```bash
# 进入技能目录
cd skills/baidu-search

# 中文查询 → 自动用百度
python scripts/unified_search.py "Python 教程" --format

# 英文查询 → 自动用 DuckDuckGo
python scripts/unified_search.py "Python tutorial" --format

# 加密货币 → 自动用 CoinGecko
python scripts/unified_search.py "btc价格" --format
python scripts/unified_search.py "ETH 价格" --format
```

**一个脚本，搞定所有搜索！** 🚀

---

### 🧠 方式2：智能 Python 脚本（推荐！⭐⭐⭐⭐）

百度 + Bing + CoinGecko 三保险，还能自动识别加密货币！

```bash
# 进入技能目录
cd skills/baidu-search

# 普通搜索
python scripts/smart_search.py "Python 教程" --format

# 加密货币搜索（自动识别！）
python scripts/smart_search.py "btc价格" --format
python scripts/smart_search.py "ETH 价格" --format
```

---

### 🌐 方式3：Playwright 浏览器搜索（最稳定！⭐⭐⭐⭐）

使用 ClawX 内置的 browser 工具，稳定可靠：

```javascript
// 1. 启动浏览器
browser(action="start")

// 2. 打开百度
browser(action="open", targetUrl="https://www.baidu.com")

// 3. 获取页面快照
browser(action="snapshot")

// 4. 在搜索框输入关键词（找到搜索框的 ref）
browser(action="act", request={
  kind: "type",
  ref: "e5",  // 替换为实际的 ref
  text: "Python 教程"
})

// 5. 按回车搜索
browser(action="act", request={
  kind: "press",
  ref: "e5",
  key: "Enter"
})

// 6. 获取搜索结果
browser(action="snapshot")
```

---

### 💬 方式4：直接说（最简单！）

你只管张嘴说，剩下的交给它：

- "搜索 Python 教程"
- "查一下 BTC 最新价格"
- "用百度搜今天的新闻"
- "帮我找 Python tutorial"
- "ETH 现在多少钱？"

---

## 📋 能搜什么？（什么都能搜！）

| 搜索类型 | 示例 | 自动选择的引擎 |
|---------|------|---------------|
| **中文技术教程** | "搜索 Python 异步编程" | 百度 |
| **英文资料** | "查 Python tutorial" | DuckDuckGo |
| **中文新闻** | "用百度查今天的新闻" | 百度 |
| **BTC 价格** | "BTC 最新价格" | CoinGecko |
| **ETH 价格** | "ETH 现在多少钱" | CoinGecko |
| **问题解答** | "如何安装 Docker" | 百度 |
| **学习资料** | "机器学习入门教程" | 百度 |
| **行业动态** | "最近的科技新闻" | 百度 |
| **生活常识** | "怎么做番茄炒蛋" | 百度 |
| **天气查询** | "今天的天气" | 百度 |

---

## 🧠 智能检测逻辑

### 语言自动检测
```python
# 中文 → 百度
"Python 教程" → 百度 ✓
"今天天气怎么样" → 百度 ✓

# 英文 → DuckDuckGo
"Python tutorial" → DuckDuckGo ✓
"How to learn AI" → DuckDuckGo ✓
```

### 加密货币自动检测
```python
# 加密货币关键词 → CoinGecko
"btc价格" → CoinGecko ✓
"BTC 价格" → CoinGecko ✓
"ETH 价格" → CoinGecko ✓
"eth价格" → CoinGecko ✓
```

### 自动 Fallback
```
百度失败 → 自动尝试 DuckDuckGo
DuckDuckGo 失败 → 自动尝试百度
都失败 → 建议使用浏览器搜索
```

---

## 💡 最佳实践

### 推荐工作流

1. **首先尝试**：统一智能搜索 `unified_search.py`（最方便）
2. **备选方案**：智能 Python 脚本 `smart_search.py`（三保险）
3. **备选方案**：Playwright 浏览器搜索（最稳定）
4. **如果都失败**：提示用户直接访问对应搜索引擎

### 搜索技巧

1. **具体关键词** - 搜索词越具体，结果越精准
2. **组合关键词** - 使用多个相关关键词组合搜索
3. **引号精确匹配** - 用引号括起来进行精确短语匹配
4. **高级搜索语法** - 使用 `site:`, `filetype:` 等高级语法

---

## 🔧 文件说明

```
skills/baidu-search/
├── SKILL.md                    # 技能文档（必看！）
├── README.md                   # 本文件
├── package.json                # 技能配置
├── requirements.txt            # Python 依赖
├── OPTIMIZATION_SUMMARY.md     # 优化总结
├── scripts/
│   ├── unified_search.py       # ✨ 统一智能搜索（首选！）
│   ├── smart_search.py         # 🧠 智能搜索脚本（备选）
│   └── baidu_search.py         # 🔍 原始百度搜索脚本
├── example_usage.js            # 使用示例
└── quick_test.py               # 快速测试脚本
```

---

## ⚠️ 注意事项

### 统一智能搜索
- ✅ 自动语言检测，无需手动选择
- ✅ 自动 Fallback，确保搜索成功率
- ✅ 加密货币自动识别，实时价格
- **推荐作为首选方式** ⭐

### 智能 Python 脚本
- ✅ 百度 + Bing 双保险
- ✅ CoinGecko 实时加密货币价格
- ✅ 自动 Fallback 机制
- 推荐作为备选方式

### Playwright 浏览器搜索
- 需要手动操作几步
- 但更稳定、更可靠
- 可以处理验证码等复杂情况
- 推荐在脚本搜索失败时使用

---

## 🛠️ 故障排除

### 问题1：百度搜索遇到验证码
**解决**：改用 Playwright 浏览器搜索方式

### 问题2：找不到搜索框元素
**解决**：重新执行 `browser(action="snapshot")` 获取最新的页面状态和元素引用

### 问题3：搜索结果不完整
**解决**：
- 使用 `browser(action="act", request={ kind: "wait", timeMs: 3000 })` 等待页面完全加载
- 尝试滚动页面查看更多结果

### 问题4：语言检测不准确
**解决**：可以手动选择搜索引擎，或使用更明确的关键词

---

## 🌐 相关链接

- **百度官网** - https://www.baidu.com/
- **DuckDuckGo** - https://duckduckgo.com/
- **CoinGecko** - https://www.coingecko.com/
- **OpenClaw 官网** - https://openclaw.ai/

---

## 📝 更新日志

### v2.0 (2026-03-03) ✨ 统一智能搜索大升级！
- 🎉 **新增统一智能搜索** - 自动语言检测 + 智能引擎选择
- 🇨🇳 中文自动用百度
- 🇺🇸 英文自动用 DuckDuckGo
- 💰 加密货币自动用 CoinGecko
- 🔄 自动 Fallback 机制
- 📊 搜索结果标明来源
- ⭐ **现在首选 unified_search.py！**

### v1.5 (2026-03-03) 🧠 智能搜索升级！
- ✨ 新增智能搜索脚本（smart_search.py）
- 🤖 自动识别加密货币查询
- 💰 集成 CoinGecko API 获取实时价格
- 🔄 百度 → Bing → 浏览器的 Fallback 机制
- 📝 完善文档和示例

### v1.0 (2026-03-03) 🌐 浏览器搜索大升级！
- ✨ 新增 Playwright 浏览器搜索方式（推荐）
- 🔧 优化 Python 脚本，改进解析策略
- 📝 更新文档，提供更详细的使用说明
- 💡 添加使用示例和最佳实践

### v0.1
- 🎉 初始版本发布
- ✅ 支持 Python 脚本搜索

---

## 🎯 总结一下

**这个技能能帮你：**
- ✅ 一个脚本搞定所有搜索！
- ✅ 中文自动用百度，英文自动用 DuckDuckGo
- ✅ 加密货币自动用 CoinGecko 实时价格
- ✅ 自动 Fallback，确保搜索成功率
- ✅ 多种搜索方式，灵活选择

**首选方式：统一智能搜索 unified_search.py ⭐⭐⭐⭐⭐⭐**

---

**一个技能，搞定所有搜索！** 🔍

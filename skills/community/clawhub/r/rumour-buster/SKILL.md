---
name: rumour-buster
description: 谣言终结者。双引擎验证消息真假：中文搜索（kimi_search + multi-search-engine）+ 英文搜索（Tavily + multi-search-engine），交叉验证，溯源消息来源。首次使用自动运行 setup 配置。
version: 0.3.0
license: MIT
author: Harry
---

# Rumour Buster - 谣言终结者

双引擎事实核查技能，结合**中文多引擎搜索**和**英文深度搜索**，实现全方位消息验证与溯源。

## 🚀 首次使用

首次使用时会**自动运行 setup**，配置搜索引擎：

```
🔧 Rumour Buster 初始化设置

1. 检查依赖（multi-search-engine）
2. 配置 Tavily API（可选，推荐）
3. 生成配置文件
4. 完成！
```

### 手动配置

如需重新配置，输入：
- `setup`
- `重新设置`
- `/rumour-buster setup`

---

## 使用方式

### 验证消息
```
/验证 "某条消息内容"
```

### 验证网页
```
/验证 https://example.com/news/article
```

---

## 验证流程

```
┌─────────────────────────────────────────┐
│  第1次：中文聚合搜索                      │
├─────────────────────────────────────────┤
│  可用引擎（基于 setup 配置）：             │
│  • kimi_search（如果可用）                │
│  • 搜狗（multi-search-engine）            │
│  • 搜狗微信（multi-search-engine）        │
│  • 头条搜索（multi-search-engine）        │
└──────────────────┬──────────────────────┘
                   │
                   ▼
         ┌─────────────────┐
         │   中文结果汇总   │
         │  - 来源追溯      │
         │  - 最早出处      │
         └────────┬────────┘
                  │
┌─────────────────────────────────────────┐
│  第2次：英文深度搜索                      │
├─────────────────────────────────────────┤
│  可用引擎（基于 setup 配置）：             │
│  • Tavily（如果配置了 API）               │
│  • DuckDuckGo（multi-search-engine）     │
│  • Startpage（multi-search-engine）      │
└──────────────────┬──────────────────────┘
                   │
                   ▼
         ┌─────────────────┐
         │   英文结果汇总   │
         │  - 国际来源      │
         │  - 权威机构      │
         └────────┬────────┘
                  │
                  ▼
        ┌───────────────────────┐
        │      交叉验证分析      │
        │  • 中英文信息一致性    │
        │  • 可信度综合评分      │
        │  • 溯源：最早出处      │
        └───────────────────────┘
```

---

## 输出格式

```markdown
# 🔍 谣言终结者验证报告

## 待验证信息
"消息内容"

## 🌐 使用的搜索引擎

### 中文搜索
- kimi_search ✓
- 搜狗 ✓
- 搜狗微信 ✓
- 头条搜索 ✓

### 英文搜索
- Tavily ✓
- DuckDuckGo ✓
- Startpage ✓

## 第1次：中文聚合搜索

### 来源追溯
- **最早出处**：xxx（时间、来源）
- **传播路径**：A → B → C

### 关键发现
...

## 第2次：英文深度搜索

### 来源追溯
- **国际最早报道**：xxx
- **权威机构表态**：WHO/CDC/...

### 关键发现
...

## 🔗 溯源结果

**信息源头**：
- 原始出处：[来源]
- 发布时间：[时间]
- 作者/机构：[名称]
- 可信度：[高/中/低]

**传播路径**：
```
[原始出处] → [媒体A] → [社交媒体B] → [到达用户]
```

## 📊 可信度评分

| 维度 | 中文 | 英文 | 一致性 |
|-----|:---:|:---:|:---:|
| 是否有报道 | ✅ | ✅ | ✅ |
| 权威来源 | ... | ... | ... |
| 核心结论 | ... | ... | ... |

**综合评分：XX% - [判断结论]**

## 📌 结论与建议
[最终判断]

---
验证时间：YYYY-MM-DD HH:MM
搜索引擎：中文x个 + 英文x个
溯源状态：[成功/部分成功/失败]
```

---

## 技术实现

### 依赖检查（setup 阶段）

```python
# 检查配置文件
CONFIG_FILE = ~/.rumour-buster-config

# 检查 multi-search-engine（必需）
if not check_multi_search_engine():
    error("请先安装 multi-search-engine")

# 检查 Tavily（可选）
tavily_config = load_tavily_config()
```

### 搜索执行（基于配置）

```python
def search_chinese(query):
    """中文聚合搜索"""
    results = []
    config = load_config()
    
    # kimi_search（如果可用）
    if config["chinese"]["kimi_search"]["available"]:
        results.append(kimi_search(query))
    
    # multi-search-engine 中文引擎
    if config["chinese"]["multi_search_engine"]["available"]:
        engines = config["chinese"]["multi_search_engine"]["engines"]
        for engine in engines:
            results.append(search_with_engine(engine, query))
    
    return results

def search_english(query):
    """英文深度搜索"""
    results = []
    config = load_config()
    
    # Tavily（如果配置了 API）
    tavily = config["english"]["tavily"]
    if tavily["available"]:
        results.append(tavily_search(query, tavily["api_key"]))
    
    # multi-search-engine 英文引擎
    if config["english"]["multi_search_engine"]["available"]:
        engines = config["english"]["multi_search_engine"]["engines"]
        for engine in engines:
            results.append(search_with_engine(engine, query))
    
    return results
```

---

## 子技能

### setup - 初始化设置

**路径**：`sub-skills/setup/`

**功能**：
- 检查依赖（multi-search-engine）
- 配置 Tavily API
- 生成配置文件

**调用方式**：
- 首次使用自动调用
- 手动：`setup` / `重新设置`

---

## 文件结构

```
rumour-buster/
├── SKILL.md                      # 主技能定义
├── scripts/
│   └── tavily_search.py          # Tavily 搜索脚本
└── sub-skills/
    └── setup/
        ├── SKILL.md              # setup 子技能定义
        └── setup.py              # setup 执行脚本
```

---

## 配置示例

`~/.rumour-buster-config`：

```json
{
  "setup_completed": true,
  "search_engines": {
    "chinese": {
      "kimi_search": {"available": true},
      "multi_search_engine": {
        "available": true,
        "engines": ["sogou", "sogou_wechat", "toutiao"]
      }
    },
    "english": {
      "tavily": {
        "available": true,
        "api_key": "tvly-xxxxx",
        "free_quota": 1000
      },
      "multi_search_engine": {
        "available": true,
        "engines": ["duckduckgo", "startpage"]
      }
    }
  }
}
```

---

## 使用示例

### 示例1：验证健康谣言

**输入**：
```
/验证 "柠檬水可以抗癌，比化疗强一万倍"
```

**执行过程**：
```
🔍 正在搜索中文来源...
  ✓ kimi_search
  ✓ 搜狗
  ✓ 搜狗微信
  ✓ 头条

🔍 正在搜索英文来源...
  ✓ Tavily
  ✓ DuckDuckGo
  ✓ Startpage

📊 交叉验证分析中...
```

**输出**：
```markdown
# 🔍 谣言终结者验证报告

## 待验证信息
"柠檬水可以抗癌，比化疗强一万倍"

## 🌐 使用的搜索引擎
中文：kimi_search, 搜狗, 搜狗微信, 头条
英文：Tavily, DuckDuckGo, Startpage

## 🔗 溯源结果

**信息源头**：
- 原始出处：2017年国外邮件谣言
- 声称来源：美国巴尔的摩健康科学研究所（已辟谣否认）
- 传播路径：邮件 → 社交媒体 → 中文自媒体 → 朋友圈

**可信度**：极低 ❌

## 📊 可信度评分：5% - 虚假消息

## 📌 结论
该说法为虚假谣言。柠檬是健康水果，但不能抗癌...
```

---

*Rumour Buster - 双引擎交叉验证，溯源求真*

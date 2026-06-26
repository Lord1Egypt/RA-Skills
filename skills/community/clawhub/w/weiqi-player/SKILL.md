---
name: 围棋选手信息查询
description: weiqi-player 围棋选手信息查询 - 查询围棋选手段位、等级分、排名信息，支持手谈等级分和易查分业余段位双平台查询。当用户需要"查棋手"、"等级分"、"段位查询"时使用此技能。
tags: ["围棋", "weiqi", "go", "棋手", "等级分", "段位", "手谈", "易查分"]
---

# 围棋选手信息查询

> **🔒 安全说明**: 本技能通过公开 API 查询围棋选手的公开等级分信息。手谈平台使用标准 HTTP 请求，易查分平台使用 Playwright 模拟正常浏览器访问。所有操作仅读取公开数据，不涉及任何敏感信息或未经授权的访问。

## 功能描述
查询围棋选手的段位、等级分、排名等信息，支持两个数据源：
1. **手谈等级分**（dzqzd.com）- 手谈平台等级分数据
2. **业余围棋段位**（yeyuweiqi.yichafen.com）- 官方段位、比赛记录、升段历程

---

## ⚠️ 强制要求：性能计时

**每次查询必须输出性能耗时信息**，这是本技能的硬性要求。

无论查询任何棋手，结果中都必须包含如下格式的性能计时报告：

```
==================================================
⏱️  性能计时报告（手谈查询）
==================================================
  构造查询参数               :    0.000s
  HTTP请求               :    1.262s
  解析HTML               :    0.001s
--------------------------------------------------
  步骤累计                 :    1.264s
  总耗时                  :    1.264s
==================================================
```

**执行原则**：
- ✅ 每次查询脚本自动输出性能计时
- ✅ 不输出性能计时的查询视为不完整
- ✅ 性能数据用于追踪查询效率变化

---

## 脚本清单

所有脚本位于 `scripts/` 目录：

| 脚本 | 功能 | 用法 |
|------|------|------|
| `query.py` | **统一查询**（推荐） | 同时查询手谈+易查分 |
| `query_shoutan.py` | 手谈等级分查询 | 单个/多同名选手 |
| `query_yichafen.py` | 易查分业余段位查询 | 单个/批量查询 |

---

## 推荐使用：统一查询脚本

**脚本位置**：`scripts/query.py`

### 单个查询
```bash
python3 scripts/query.py <姓名>
```

### 批量查询
```bash
python3 scripts/query.py --batch 姓名1 姓名2 姓名3
```

**示例**：
```bash
python3 scripts/query.py 张三
python3 scripts/query.py --batch 李四 王五 赵六
```

**输出格式**（单行 Markdown 格式）：

手谈查询输出示例：
```
📋 **张三** - 手谈等级分查询结果

**张三** (某市) | 段位: 6.2d | 等级分: 2500.0 | 全国排名: 1234 | 对局: 100局
   👉 [查看详细记录](https://v.dzqzd.com/SpBody.aspx?r=...)
```

易查分查询输出示例：
```
📋 **张三** - 易查分业余段位查询

段位: 6段 | 等级分: 1700.00 | 总排名: 1000 | 地区: 某省 某市 | 性别: 男 | 出生: 2010

备注: 20XX第X届"XX杯"全国围棋比赛晋升6段

⏱️ 查询耗时: 3.0秒
```

**特点**：
- 单行格式，使用 `|` 分隔不同字段
- 每位选手后直接附带 **[查看详细记录](链接)** 可点击链接
- 无需表格，Markdown 纯文本友好

---

## 数据源详解

### 1. 手谈等级分查询

**脚本位置**：`scripts/query_shoutan.py`

**功能特点**：
- ✅ 性能计时追踪
- ✅ **支持多同名选手** - 自动列出所有同名选手（按地区区分）
- ✅ 可点击链接格式 - 使用 `[文字](链接)` 格式输出详细记录链接

**使用方法**：
```bash
python3 scripts/query_shoutan.py <姓名>
python3 scripts/query_shoutan.py 张三
python3 scripts/query_shoutan.py 李四
```

**URL 模板**：
```
https://v.dzqzd.com/SpBody.aspx?r={base64编码的XML参数}
```

**XML 参数格式**：
```xml
<Redi Ns="Sp" Jk="选手查询" 姓名="选手姓名"/>
```

**多同名选手示例**（如查询"张三"会返回两位选手）：
```
⚠️ 找到 2 位同名选手

1. **张三** (某市A) | 段位: 6.2d | 等级分: 2500.0 | 全国排名: 1234
   👉 [查看详细记录](https://v.dzqzd.com/SpBody.aspx?r=...)

2. **张三** (某市B) | 段位: 3.1d | 等级分: 2000.0 | 全国排名: 5678
   👉 [查看详细记录](https://v.dzqzd.com/SpBody.aspx?r=...)
```

---

### 2. 业余围棋段位查询（易查分平台）

**平台地址**：`https://yeyuweiqi.yichafen.com/qz/s9W2g0zKmt`

**脚本位置**：`scripts/query_yichafen.py`

**使用方法**：
```bash
# 单个查询
python3 scripts/query_yichafen.py 张三

# 批量查询（共享浏览器会话，更快）
python3 scripts/query_yichafen.py --batch 李四 王五 张三

# 调试模式（显示浏览器界面）
python3 scripts/query_yichafen.py 张三 --visible
```

**性能表现**：
- 单次查询：**~4-5秒**
- 批量查询：**~3秒/人**（复用会话）

**依赖安装**：
```bash
pip install playwright
playwright install chromium
```

**返回数据示例**：
```
张三
6段
等级分	1700.00
总排名	1000
省区排名	100
本市排名	20
性别	男
出生	2010
省区	某省
城市	某市
备注	20XX第X届"XX杯"全国围棋比赛晋升6段
```

---

## 快速查询指令

```
"查一下[姓名]的围棋信息"      → 使用 query.py 双平台查询
"查询[姓名]的手谈等级分"      → 使用 query_shoutan.py
"查询[姓名]的业余段位"        → 使用 query_yichafen.py
"批量查询[姓名1][姓名2]"      → 使用 query.py --batch
"查看[姓名]的等级分明细"      → 生成详细记录链接
```

---

## 高级用法

### 手谈详细比赛情况查询

**URL 模板**：
```
https://v.dzqzd.com/SpBody.aspx?r={base64编码的XML参数}
```

**XML 参数格式**：
```xml
<Redi Ns="Sp" Jk="等级分明细" Yh="{用户ID}" 选手号="{选手号}"/>
```

**Python 示例**：
```python
import base64
import requests

def query_player_info(name):
    """查询选手基本信息"""
    xml = f'<Redi Ns="Sp" Jk="选手查询" 姓名="{name}"/>'
    encoded = base64.b64encode(xml.encode()).decode()
    url = f"https://v.dzqzd.com/SpBody.aspx?r={encoded}"
    
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    return response.text

def query_player_detail(user_id, player_id):
    """查询选手详细比赛情况"""
    xml = f'<Redi Ns="Sp" Jk="等级分明细" Yh="{user_id}" 选手号="{player_id}"/>'
    encoded = base64.b64encode(xml.encode()).decode()
    url = f"https://v.dzqzd.com/SpBody.aspx?r={encoded}"
    
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    return response.text

# 使用示例
info_html = query_player_info("张三")
# 解析 info_html 获取 Yh 和 选手号
detail_html = query_player_detail("1234567", "7654321")
```

---

## 查询结果网页链接生成

使用 **Markdown 链接格式**返回可点击链接：

```markdown
[点击查看详细记录](https://v.dzqzd.com/SpBody.aspx?r=Base64编码的参数)
```

**多同名选手示例**（如"张三"）：

- [某市A 9.9d 详细记录](https://v.dzqzd.com/SpBody.aspx?r=示例链接1)
- [某市B 3.1d 详细记录](https://v.dzqzd.com/SpBody.aspx?r=示例链接2)

---

## 重要：实时查询原则

⚠️ **等级分数据实时变化，每次查询必须访问官网获取最新数据，不得使用缓存或归档数据。**

- 手谈等级分随比赛结果实时更新
- 排名每日变化
- 业余段位查询结果也可能更新

**禁止行为**：
- ❌ 将查询结果存档作为参考
- ❌ 向用户提供过时的等级分/排名数据
- ❌ 依赖记忆中的历史数据

**正确做法**：
- ✅ 每次查询都执行实时 HTTP 请求
- ✅ 返回数据时标注查询时间
- ✅ 同时提供官网链接供用户验证

---

## 注意事项

1. **同名选手处理**：
   - 手谈平台可能返回**多位同名选手**（如查询"张三"会返回某市A和某市B两位）
   - 脚本会自动列出所有同名选手，按地区区分
   - 为每位选手生成独立的详细记录链接
   - 需根据地区/等级分判断目标选手

2. **编码问题**：手谈查询需要 UTF-8 编码后转 Base64

3. **Session**：业余围棋查询通过 Playwright 持久化浏览器上下文自动管理会话

4. **数据差异**：两平台等级分体系不同，不可直接比较

5. **详细查询依赖**：查询等级分明细需要先获取基本信息中的 `选手号` 和 `Yh`

6. **业余段位查询**：使用 Playwright 浏览器自动化查询，平台有反爬虫保护，curl 方式已失效

7. **链接格式**：返回给用户的链接应使用 `[文字](链接)` 格式，方便点击

## 触发关键词
- "查[姓名]的围棋信息"
- "查[姓名]的手谈"
- "查[姓名]的手谈等级分明细"
- "查[姓名]的业余段位"
- "汇总[姓名]围棋信息"
- "[姓名]等级分"
- "[姓名]段位"
- "[姓名]最近比赛"

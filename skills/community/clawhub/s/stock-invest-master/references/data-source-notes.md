# 数据源实战笔记 — 2026年5月更新

## Python Sandbox网络限制

**核心发现**：此服务器上Python sandbox内的`urllib`只能访问**HTTP**端点，**所有HTTPS连接均报"Network is unreachable"**。

| 端点类型 | 可用? | 示例 |
|---------|-------|------|
| HTTP腾讯行情 | ✅ | `qt.gtimg.cn/q=sh600309` |
| 新浪HTTP行情 | ✅ | `hq.sinajs.cn/list=gb_baba` |
| HTTPS东方财富 | ❌ | `emweb.securities.eastmoney.com` |
| HTTPS新浪财经 | ❌ | `finance.sina.com.cn` |
| HTTPS Google | ❌ | `google.com/search` |
| HTTPS CLS财联社 | ❌ | `cls.cn` |
| HTTPS Baidu | ❌ | `baidu.com/s` |

**替代方案**：
1. 获取财务数据 → 使用 `browser_navigate` 访问东方财富F10页面，通过 `browser_snapshot` 或 `browser_console` 提取
2. 获取市场新闻 → 使用 `delegate_task` + `web` toolset，或 `browser_navigate` 访问新浪财经/财联社
3. 实时行情 → 坚持用腾讯API（HTTP）和新浪API（HTTP）

## 美股中概股数据源

### 新浪实时行情API
```
http://hq.sinajs.cn/list=gb_baba
```
必须带 `Referer: http://finance.sina.com.cn` 头。

常用代码：
| 代码 | 公司 | 代码 | 公司 |
|------|------|------|------|
| gb_baba | 阿里巴巴 | gb_pdd | 拼多多 |
| gb_jd | 京东 | gb_bidu | 百度 |
| gb_nio | 蔚来 | gb_xpev | 小鹏汽车 |
| gb_li | 理想汽车 | gb_tme | 腾讯音乐 |
| gb_ntes | 网易 | gb_wbg | 微博 |
| gb_hxc | 金龙指数 | | |

返回格式（GBK编码）：
```
var hq_str_gb_baba="阿里巴巴,139.98,-4.00,-5.83%,140.50,143.98,141.00,139.28,1547203,2026-05-14 21:49:41"
```

解析：`split('"')[1].split(',')` → [0]名称, [1]现价, [2]涨跌额, [3]涨跌幅, ...

## 东方财富F10页面浏览器访问

**目标URL**：`https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/ZYFXListV2?code=SH600309&type=0`

**访问技巧**：
1. `browser_navigate` 打开页面
2. 页面需要JS渲染，等待加载完成后再用 `browser_snapshot` 或 `browser_console` 提取
3. 通过 `browser_console` 执行JS获取JSON数据：
   ```javascript
   fetch('/PC_HSF10/NewFinanceAnalysis/ZYFXListV2?code=SH600309&type=0')
     .then(r => r.json()).then(d => console.log(JSON.stringify(d)))
   ```
4. 或用 `browser_snapshot` 直接读取表格文本

## 财联社电报

**URL**：`https://www.cls.cn/telegraph`
- 提供实时中文财经快讯
- 通过 `browser_navigate` + `browser_snapshot` 获取内容
- 适合获取盘中突发新闻、政策变动、行业动态

## 新浪财经美股页面

**URL**：`https://finance.sina.com.cn/stock/usstock/`
- 可浏览中概股行情列表
- 搜索框可查询个股信息
- 实时新闻流提供市场动态

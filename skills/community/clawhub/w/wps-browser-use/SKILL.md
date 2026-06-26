---
name: browser-use
description: 通过 nodriver 驱动浏览器，支持信息检索、网页抓取、表单交互等；**作为搜索工具的补充**——内置搜索无结果、摘要不足或需登录/站内检索时再启用；适用于非 WPS 链接访问、落地页导航、Web 应用交互，以及股票/金价/期货/天气等强事实信息。
---

# Browser Skill

基于 nodriver 的浏览器自动化 skill，专为**纯文本 agent** 设计。

**与搜索工具的关系**：优先用搜索工具快速拉取公开摘要；若搜索**搜不到**、结果过时/片面、或必须进入具体网站（站内搜索、动态页、表格详情）才能拿到答案，再**查阅并启用本 SKILL**，用浏览器补齐信息。

## 核心设计原则

所有公开方法均返回结构化**文本快照**，格式统一为：

```
[操作摘要]
---
Title: 页面标题
URL:   https://...
---
Interactive elements (index[:]info):
0[:] input type="text" placeholder="搜索"
1[:] button | 百度一下
2[:] a href="https://..." | 新闻
...
---
Page Text:
页面可见文本...
```

agent 通过读取快照中的**元素索引**来引用元素，无需理解 HTML 或 CSS 选择器。每次操作后快照自动刷新，索引始终对应当前页面状态。

**大内容溢出处理**：页面文本超过 10000 字符或元素超过 100 个时，超出部分自动保存到文件，快照中提示路径，可用 `jupyter_cell_exec`工具 读取完整内容。

## 加载方式

```python
import sys, os
sys.path.insert(0, os.path.join(os.getenv("skill_path"), "browser", "scripts"))
import browser
```

## API 参考

### navigate — 打开页面

```python
result = browser.navigate(
    url="https://www.baidu.com",
    wait_for=None,  # 可选：等待某 CSS 选择器出现后再返回
)
print(result)
```

### click — 点击元素

```python
result = browser.click(element_index=1)  # 索引来自上次快照的 Interactive elements
print(result)
```

### fill — 填写输入框

```python
result = browser.fill(
    element_index=0,
    text="搜索内容",
    press_enter=False,   # 是否回车提交
)
print(result)
```

实现上会先点击目标输入框、短暂等待再 `fill` 覆盖内容；若遇动态展开/联想框导致失败，可先 `browser.click` 激活再 `browser.fill`，或调用 `browser.get_interactive_elements()` 刷新索引后重试。

### select_option — 下拉框选择

```python
result = browser.select_option(
    element_index=3,
    option_text="选项一",   # 按可见文本匹配（最常用）
    # option_value="val1",  # 按 value 属性匹配
    # option_index=0,       # 按位置匹配（0 起）
)
print(result)
```

### get_interactive_elements — 刷新元素列表

```python
result = browser.get_interactive_elements()
print(result)
```

页面动态加载新内容后，调用此方法刷新元素缓存和索引。

### execute_script — 执行 JS

```python
result = browser.execute_script("return document.title")
print(result)
```

### screenshot — 截图

```python
result = browser.screenshot(
    output="screenshot.png",
    full_page=False,
)
print(result)
```

## 可信网站推荐

根据任务类型选择合适的入口，优先使用专业数据源。

**访问方式（务必遵守）**：下表中的链接表示**应从该站点开始**。请先用 `navigate` 打开对应网站，再通过站内搜索、导航菜单、栏目链接等**在页面上**进入目标功能；**不要**凭记忆或猜测去改路径、拼深层 URL 直接访问。站点改版后路径常变，硬编 URL 容易 404、跳转登录页或落到无关页面。

**禁用 query 拼接作为第一步**：**禁止**一上来就把关键词拼进地址栏，用带查询串的 URL 直接打开（如 `?key=`、`?q=`、`?wd=`、`keyword=` 等）。正确做法是先进表内给出的**起点页**，再用页面上的搜索框输入关键词并触发搜索。反例（勿做）：`https://so.eastmoney.com/cn/result?key=金山办公` —— 应改为先打开 `https://so.eastmoney.com`，再在站内搜索「金山办公」。

| 任务类型                             | 推荐网站                           | 链接                                        |
| ------------------------------------ | ---------------------------------- | ------------------------------------------- |
| 股票行情                             | 东方财富网                         | `https://so.eastmoney.com`                  |
| 期货行情                             | 曲合期货                           | `https://www.quheqihuo.com/quote/shfe.html` |
| 贵金属（黄金 / 白银 / 铂金）现货价格 | 上海黄金交易所                     | `https://www.sge.com.cn/sjzx/yshqbg`        |
| 基金净值 / 基金排行 / 基金查询       | 天天基金网                         | `https://fund.eastmoney.com/`               |
| 天气预报 / 气象灾害 / 台风信息       | 中央气象台                         | `https://www.nmc.cn/`                       |
| 汇率查询                             | 百度（搜索结果页直接展示实时换算） | `https://www.baidu.com`                     |
| 快递单号查询                         | 百度（绕过快递网站验证码）         | `https://www.baidu.com`                     |

> 汇率查询直接在百度搜索（如"1美元换多少人民币"），百度会在结果页实时计算并展示换算结果，无需进入专业汇率网站。
> 快递单号查询直接在百度搜索单号，百度会通过摘要聚合展示物流状态，可绕过顺丰、圆通等快递官网的验证码限制。

## 特殊情况处理

某些场景下不适合使用浏览器，应优先使用更高效的方式：

| 情况                 | 处理方式                                                                     | 原因                                   |
| -------------------- | ---------------------------------------------------------------------------- | -------------------------------------- |
| 批量获取股票历史数据 | 直接调用东方财富 API：`http://push2his.eastmoney.com/api/qt/stock/kline/get` | 浏览器逐天抓取耗时长、效率低、容易出错 |

## Troubleshooting

| 问题                       | 处理方式                                   |
| -------------------------- | ------------------------------------------ |
| 元素找不到或点击无效       | 记录当前状态，提示用户手动处理后继续       |
| 需要登录、验证码或手动步骤 | 暂停操作，建议用户接管浏览器完成验证后继续 |

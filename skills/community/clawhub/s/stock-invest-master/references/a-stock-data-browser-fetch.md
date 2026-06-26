# A股财务数据获取 — 东方财富浏览器方案

> 当直接API调用(腾讯/新浪/东方财富)失败时，使用browser自动化从东方财富获取财务数据。

## 为什么直接API失败
- 腾讯 `web.ifzq.gtimg.cn` 返回 "No dispatch info found"
- 东方财富 `emweb.securities.eastmoney.com` API 返回空或JSON解析错误
- Python sandbox `urllib` 无法访问外网(Network unreachable)
- Google搜索在境内服务器不可用

## 成功方案：Browser + 东方财富F10页面

### 步骤
1. `browser_navigate` 到东方财富个股财务页面
2. `browser_console` 执行JS提取数据
3. `browser_snapshot` 或解析console输出

### 关键URL模式
```
# 财务分析 - 主要指标
https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/ZYFXListV2?code=SH{代码}&type=0

# 盈利预测
https://emweb.securities.eastmoney.com/PC_HSF10/ProfitForecast/{代码}.html

# 研报摘要
https://emweb.securities.eastmoney.com/PC_HSF10/ResearchReport/{代码}.html
```

### JS提取脚本（browser_console执行）
```javascript
// 东方财富页面数据通常挂载在 window.__INITIAL_STATE__ 或通过API加载
// 最简单方法：直接解析页面上的表格DOM
const rows = document.querySelectorAll('table tbody tr');
const data = [];
rows.forEach(r => {
  const cells = r.querySelectorAll('td');
  const obj = {};
  cells.forEach((c, i) => { obj[`col${i}`] = c.textContent.trim(); });
  data.push(obj);
});
JSON.stringify(data.slice(0, 10));
```

### 实时行情（腾讯API，Python sandbox可用）
```python
import urllib.request
url = "http://qt.gtimg.cn/q=sh600309"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
resp = urllib.request.urlopen(req, timeout=10)
data = resp.read().decode("gbk")
parts = data.split("~")
# parts[1]=名称, [3]=现价, [39]=PE, [46]=PB, [45]=总市值, [38]=换手率
```

### 关键数据字段映射（腾讯行情API）
| 字段 | 索引 | 说明 |
|------|------|------|
| 名称 | [1] | 股票名称 |
| 现价 | [3] | 当前价格 |
| 涨跌% | [32] | 涨跌幅百分比 |
| PE | [39] | 市盈率TTM |
| PB | [46] | 市净率 |
| 总市值 | [45] | 单位：亿元 |
| 换手率 | [38] | 百分比 |
| 52周最高 | [51] | |
| 52周最低 | [52] | 注意可能是除权后数据 |

### 注意事项
- 腾讯API返回GBK编码，必须 `.decode("gbk")`
- 总市值字段单位是"亿"（已经是格式化后的字符串）
- 52周最低可能异常（除权/数据错误），需交叉验证
- Python sandbox可访问 `qt.gtimg.cn` 但不能访问外部HTTPS（google/eastmoney）
- Browser sandbox可访问eastmoney但不能读取系统字体，中文渲染需内嵌base64字体

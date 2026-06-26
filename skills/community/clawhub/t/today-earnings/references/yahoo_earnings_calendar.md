# Yahoo Finance 财报日历技术参考

这个文件只放页面结构、字段映射和解析维护点，不重复写安装与操作步骤。

## URL 结构

```text
https://finance.yahoo.com/calendar/earnings?day=YYYY-MM-DD&offset=0&size=100
```

### 参数含义

| 参数 | 含义 |
| --- | --- |
| `day` | 查询日期，格式 `YYYY-MM-DD` |
| `offset` | 分页偏移量，当前实现常用 `0` |
| `size` | 每页结果数，当前实现默认 `100` |

## 当前解析依赖

当前实现基于 Chrome Extension 内容脚本和解析器，默认依赖以下事实：

1. Yahoo Finance 财报页存在主表格。
2. 表格列顺序稳定。
3. 能从页面中提取股票代码、发布时间和市值字段。
4. 市值字符串可被转换为数值。

如果 Yahoo Finance 改版，通常优先坏在这些假设上。

## 表格字段映射

| 列 | data-testid | 说明 |
| --- | --- | --- |
| 1 | `symbol` | 股票代码 |
| 2 | `companyshortname` | 公司名称 |
| 3 | `eventname` | 财报事件名称 |
| 4 | `earningscalltime` | 财报发布时间，常见为 `BMO`、`AMC`、`TNS` |
| 5 | `epsestimate` | 预期 EPS |
| 6 | - | 实际 EPS |
| 7 | - | Surprise 百分比 |
| 8 | `intradaymarketcap` | 市值 |

## 时间字段

| 值 | 含义 | 中文 |
| --- | --- | --- |
| `BMO` | Before Market Open | 盘前 |
| `AMC` | After Market Close | 盘后 |
| `TNS` | Time Not Specified | 时间未定 |

## 当前输出关心的字段

最终对外输出会收敛成：

```json
{
  "code": "HPE",
  "earningType": "AMC",
  "marketCap": 28370000000
}
```

也就是说，当前流程重点保留：
- 股票代码
- 发布时间类型
- 市值数值

公司名、事件名等字段目前不是最终输出的一部分。

## 市值解析

市值字符串支持以下后缀换算：

- `K` → 千
- `M` → 百万
- `B` → 十亿
- `T` → 万亿

无法解析或为空时，该条记录会被过滤掉。

## 维护建议

当结果异常时，优先按下面顺序排查：

1. 页面 URL 是否仍然正确
2. 表格和字段选择方式是否失效
3. `earningType` 是否仍然使用 `BMO/AMC/TNS`
4. 市值字段格式是否变化
5. 再决定是改扩展解析逻辑，还是只改输出转换逻辑

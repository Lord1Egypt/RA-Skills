# 东方财富 push2 接口实战手册（Signal-Search 专域连接器依据）

> 本文件供实现 `eastmoney_connector`（§6.3c bullet 10）时直接使用。结论来自本地实战 skill `eastmoney-fundflow-scraper` 的踩坑经验 + 公开接口解析，是"扒东财资料"的权威依据。
> 东财的行情/资金流/分时/K线数据**全部走 `push2.eastmoney.com` / `push2his.eastmoney.com` 的 JSON 接口**，无浏览器挑战、返回干净 JSON。正确姿势：拼接口 URL → 过轻量反爬（仅 TLS+IP 频率）→ 直接拿结构化数据。

## 1. 核心接口

| 用途 | 接口 | 关键参数 |
|------|------|----------|
| 实时行情（单只） | `push2.eastmoney.com/api/qt/stock/get` | `secid`、`fields`、`fltt=2`、`invt=2` |
| 资金流/排行（批量） | `push2.eastmoney.com/api/qt/clist/get` | `fs`、`fields`、`pz`、`pn`、`ut` |
| 分时成交 | `push2.eastmoney.com/api/qt/stock/trends2/get` | `secid`、`ndays=1`、`fields1/fields2`、`ut` |
| 历史 K 线 | `push2his.eastmoney.com/api/qt/stock/kline/get` | `secid`、`klt`(101日/102周/103月/60=60分)、`fqt`(1前复权)、`beg`、`end`、`lmt` |

- `ut` 令牌：`clist/get` 用 `ut=fa5fd1943c7b386f172d6893dbfba13a`；`trends2/get` 用 `ut=fb5fd1943c7b386f172d6893dbfba10b`（历史值，失效则从页面/初始化接口提取）。
- 返回顶层 `rc`：0=成功；非 0 或无 `data`/`success=false` = 主动失败。

## 2. secid 转换（市场.代码）

| 代码前缀 | 市场 | secid 示例 |
|----------|------|------------|
| 6xxxxx（沪 A） | 1 | `1.600519`（贵州茅台） |
| 0xxxxx / 3xxxxx（深 A） | 0 | `0.000001`（平安银行） |
| 000001（上证指数） | 1 | `1.000001` |
| 399001（深证成指） | 0 | `0.399001` |
| 399006（创业板指） | 0 | `0.399006` |
| 美股 AAPL | — | `105.AAPL` |
| 港股 00700 | — | `116.00700` |

```python
def to_secid(raw: str) -> str:
    raw = raw.lower().lstrip("shsz")
    market = "1" if raw.startswith("6") else "0"  # 沪6/深0
    return f"{market}.{raw[-6:]}"
```

## 3. fields 字段表（代号→含义）

行情/资金流字段均为 `f+数字`：
- `f12`=代码(无后缀) `f13`=市场(1沪/0深/2京) `f14`=名
- `f43`=最新价 `f44`=涨跌幅 `f45`=涨跌额 `f46`=成交量 `f47`=成交额 `f48`=总市值 `f49`=市盈率
- 资金流：`f62`=主力净流入 `f184`=主力占比 `f66`=超大单净流入 `f69`=超大单占比 `f72`=大单净流入 `f75`=大单占比 `f78`=中单净流入 `f81`=中单占比 `f84`=小单净流入 `f87`=小单占比
- 常用股票行情 `fields=f57,f58,f43,f44,f45,f46,f47,f48,f49`

## 4. 分页与 100 条硬封顶（关键坑）

- `pz`（每页条数）设多大**都只回 100 条**。全市场 5545 只/天需 ~56 页。
- 终止条件：**`len(rows) < 100`**（满页=100，末页<100）。**切勿写 `< 1000`**，否则第 1 页就 break 只落 100 只。
- `fs`（板块范围）：
  - 个股全市场：`fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23`（沪深 A 股）
  - 行业板块：`fs=m:90+t:2`（东财行业分类 ~90 个，**每天仅 1 页**）

## 5. 失败分类（必须区分，否则误熔断）

| 现象 | 性质 | 处理 |
|------|------|------|
| `rc=56`（CURLE_RECV_ERROR）、响应截断、单页偶发成功 | **网络抖动/东财软封**，非代码错 | 仅 1~3s 短退避快重试，**不触发熔断**；单页偶发能成、批量必死 |
| 东财主动返回 `success=false` / `data` 空 / `rc!=0` | **主动封禁** | 走熔断长冷却（10~20min） |
| `RemoteDisconnected` / RST 在 TLS 握手阶段 | **TLS(JA3) 指纹被封** | 升级 TLS 回落链（见 §6.3d：系统 curl→curl_cffi→stealth） |

## 6. TLS 工具矛盾与实测要点

- **本地实战结论（权威）**：`python requests` / `curl_cffi` 被东财 TLS(JA3) 指纹封禁（RemoteDisconnected），**必须用系统 `curl` 子进程**（指纹被放行）。
- **外网教程（含部分 skill 市场代码）称 `curl_cffi impersonate='chrome'` 可过 push2**：可能成立（差异来自 curl_cffi 版本/网络/接口）。**本 skill 实现回落链，不武断定死**；首版实测以 `rc==0` 真数据验证。
- 系统 curl 推荐命令：
  `curl -s --compressed --max-time T --retry 6 --retry-all-errors --retry-delay 1 --retry-max-time 90 -H "User-Agent: ..." -H "Referer: https://quote.eastmoney.com/" "<url>"`

## 7. 行业级 vs 个股全市场（策略决策）

- 只需"聪明钱选行业" → 直接抓**行业级资金流**（`fs=m:90+t:2`，1 页/天，2674 天=2674 请求），远优于个股 56 页/天（~15 万请求，热点必挂）。
- 个股全市场仅当确实需要逐股因子才抓；热点网络下基本不可行，优先 Tushare `moneyflow`（一次调用返回全市场，稳定，到 2015）。

## 8. 韧性设计（落库/断点）

- 落库前完整性校验：`< total*0.9` 视为残数据当天重抓。
- 断点续传：`WHERE date=?` 已有行则跳过；坏网络窗口没填满就下遍再来，多遍循环 + 日期 shuffle 跨窗口填充。
- IP 级限流靠**物理换网络**（手机热点/其他出口）解除；HTTP_PROXY 通常为空。

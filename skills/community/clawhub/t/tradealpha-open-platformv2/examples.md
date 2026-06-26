# 请求与响应示例

## 示例请求体

```json
{
  "page": 1,
  "level": "重要",
  "end_time": "2026-04-25 23:00:00",
  "source": "bloomberg",
  "page_size": 100,
  "category": "市场与货币",
  "token": "your token"
}
```

说明：

- `page_size` 在协议上为数字类型；部分客户端以字符串传递时，服务端会按可解析的整数处理。
- 实际执行脚本时，`token` 由系统环境变量 `TradeAlphaToken` 提供；如果没有该环境变量，脚本会直接报错并提示前往 `https://quantaccess.lxaa.top/#/login` 获取 token。

## 示例响应体

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "total": 191,
    "page": 1,
    "page_size": 100,
    "list": [
      {
        "id": 516472,
        "datetime": "2026-04-25 15:00:20",
        "content": "【Out-of-Court Creditor Deals Are Coming to the K-Shaped Debt Market - Bloomberg】\n\n【经济学家长期描述美国经济为K形——富人更富，穷人更穷。同样动态在公司中上演：强公司继续增长并获得资本，弱公司在债务和需求疲软下进一步落后。2028年债务到期墙将至；若高利率持续，偿还贷款人将付出高昂代价，因此许多公司转向负债管理练习（LMEs）。越来越多的公司谈判庭外交易，重新安排还款优先级、延长到期日并说服贷款人提供新资金注入，以保留资金并保持选择开放。Davis Polk & Wardwell重组联席主管Damian Schaible表示：“面临2028/2029到期债务的公司市场有点K形，似乎分为容易再融资和较难的情况。”彭博汇编数据显示，2024年全球LMEs近50个，去年降至少于35个，但这些交易回升；第一季度完成7个，可能很快开始9个。消息人士称，Medical Solutions（Centerbridge和Caisse de Depot et Placement du Quebec所有的高杠杆医疗人员公司）寻求更广泛贷款人支持新资金投资，包括低于面值的债务交换和到期延长。其他消息人士称，Vivid Seats在表现疲软下寻求新资金；债务进入困境后，票务转售商转移抵押品以解锁新融资。彭博早前报道，Cabinetworks（Platinum Equity所有）要求更多债权人进入保密谈判支持债务交易，提供新资本、困境交换和到期延长。Schaible表示，虽然到期墙还有一年多，赞助商和公司可能认为现在是接触债权人的合适时机。“随着到期临近，松散文件价值减少；如果需要与贷款人谈判延期，最好尽早行动。”他预计活动集中在软件、医疗保健和建筑产品等挑战行业。近期交易显示条款如何被重塑：L Catterton支持的RealTruck Group获得3.71亿美元贷款，新设施位于还款线顶端且按比例；交易延长到期并允许交换。同时，无担保债券持有人可以以高折扣切换到更高级债务。Perforce Software（Clearlake Capital和Francisco Partners支持）达成更不寻常交易，允许初级债权人升级到与第一留置权贷款人平等。穆迪评级在4月10日报告中称：“延长到期提供流动性提升，并给予公司额外时间执行AI产品战略。”】\n\nhttps://www.bloomberg.com/news/newsletters/2026-04-25/out-of-court-creditor-deals-are-set-to-hit-the-k-shaped-debt-market",
        "source": "bloomberg",
        "category": "市场与货币",
        "level": "重要"
      }
    ]
  }
}
```

## 常见自然语言映射

- “帮我拽 TradeAlpha 新闻” -> 视为默认新闻请求，脚本会从环境变量 `TradeAlphaToken` 读取 token
- “帮我拉今天的彭博新闻” -> `source: "bloomberg"`，时间范围按当天处理
- “帮我拉路透里很重要的市场与货币新闻” -> `source: "rtrs"`，`level: "很重要"`，`category: "市场与货币"`
- “帮我看近 24 小时国内新闻” -> `source: "domestic"`，时间范围可走接口默认值

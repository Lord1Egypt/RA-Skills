---
name: shumai-ads
description: 查询澍脉AI投放驾驶舱的真实投放数据。当用户询问广告投放表现、账户余额、哪些广告计划该止损/优化/加预算、CPA/CTR 异常,或品牌在 AI 大模型(DeepSeek/豆包/Kimi 等)中的 GEO 可见度与排名时使用。需要环境变量 SHUMAI_API_KEY。
---

# 澍脉投放驾驶舱 Skill

调用澍脉AI投放驾驶舱(www.shumai.com.cn)的只读接口,把广告主的真实投放诊断带进对话。

## 什么时候用

| 用户在问 | 用哪个命令 |
|---|---|
| "我的投放整体怎么样 / 余额还有多少" | `overview` |
| "哪些计划有问题 / 该止损 / 该加预算" | `alerts`(可加级别 `high`=止损 `warn`=优化 `good`=放量)|
| "我的品牌在 AI 里搜得到吗 / GEO 排名" | `geo` |

## 前置条件

需要环境变量 `SHUMAI_API_KEY`。**未配置时,引导用户操作,不要编造任何数据**:

> 请到澍脉工作台 https://www.shumai.com.cn/admin/ 注册登录,在「设置 → API Key · Agent 接入」
> 生成 API Key(明文仅显示一次),然后配置为环境变量 SHUMAI_API_KEY。

## 调用方法

优先用脚本:

```bash
bash scripts/shumai.sh overview
bash scripts/shumai.sh alerts high
bash scripts/shumai.sh geo
```

脚本不可用时直接发 HTTP(标准 MCP JSON-RPC 2.0):

```bash
curl -s -X POST https://www.shumai.com.cn/mcp \
  -H "content-type: application/json" \
  -H "Authorization: Bearer $SHUMAI_API_KEY" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"shumai_overview","arguments":{}}}'
```

工具名:`shumai_overview` / `shumai_alerts`(参数 `{"level":"high|warn|good"}` 可选)/ `shumai_geo_report`。
结果在 `.result.content[0].text`;若 `.result.isError` 为 true,把 text 原样告知用户,不要掩饰。

## 输出要求

- 把返回文本整理成简洁的中文回答;**数字保留原值,绝不改动或估算**
- 返回里的建议动作(止损/优化/放量)要原样传达,并注明这是澍脉基于近30天数据的诊断
- 澍脉接口是只读的:不能通过本 Skill 修改预算或投放设置;用户要改动时,引导其到媒体平台后台操作

---
name: public-opinion-report
description: 调用Midu-Public-Opinion-Report接口，生成一篇舆情分析报告。支持的报告类型：事件专报、话题报告、行业报告、活动报告、周期性报告、直报点上报快评、直报点上报综述、直报点热点报送、品牌传播洞察报告、城市对标分析报告、城市传播影响力报告、区域网络信息报告、公共政策网络舆情报告。Call the Midu-Public-Opinion-Report interface to generate a public opinion analysis report. Supported report types:incident special report, topic report, industry report, event report, periodic report, direct reporting point quick review submission, direct reporting point overview submission, direct reporting point hot topic submission, brand communication insight report, city benchmarking analysis report, city communication impact report, regional online information report, public policy online public opinion report.
metadata: { "openclaw": { "emoji": "📋", "requires": { "bins": ["python3"], "env": ["MIDU_API_KEY"] }, "primaryEnv": "MIDU_API_KEY" } }
---

# Public Opinion Report

Call the internal public opinion report service to generate a report in Markdown format.

## Prerequisites

### API Key Configuration
This skill requires a **MIDU_API_KEY** to be configured in OpenClaw.

If you don't have an API key yet, please visit:
**http://intra-znjs-yqt-agent-wx-beta.midu.cc/apiKey**

For detailed setup instructions, see:
[references/apikey-fetch.md](references/apikey-fetch.md)

## Usage

```bash
python3 skills/public-opinion-report/scripts/report.py '<JSON>'
```

## Request Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| message | str | yes | - | Requirement description for the report |
| thread_id | str | no | - | Session ID, required for multi-turn conversations. No need to pass it in for the first conversation; the API will return it. |

## Examples

```bash
# New report
python3 scripts/search.py '{"message":"生成关于法国旅游的报告"}'

# Modify Report (Based on Completed Report)
python3 scripts/report.py '{
  "thread_id":"Use the thread_id returned by the previous API call"
  "message":"在当前报告基础上增加一个研判建议章节"
}'

```

## Report Type

接口支持多种类型报告：事件专报、话题报告、行业报告、活动报告、周期性报告、直报点上报快评、直报点上报综述、直报点热点报送、品牌传播洞察报告、城市对标分析报告、城市传播影响力报告、区域网络信息报告、公共政策网络舆情报告

| Report type | Eessage（意会即可，不必照搬） |
|------|--------------------------------|
| 直报点快评 | 「关于某某，写一份快评」 |
| 事件专报 | 「就某某事件写一份舆情专报」 |
| 话题报告 | 「某某话题的舆情话题报告」 |
| 活动报告 | 「某某活动的舆情/传播活动报告」 |
| 品牌报告 | 「某某品牌的舆情/品牌报告」 |


## Note

Completing a report may take 5 to 20 minutes. Please wait patiently for the API response before proceeding to the next step.



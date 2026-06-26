---
name: uapp-outlier
description: Query UApp (友盟+) application outlier reports, yesterday anomalies, and intelligent inspection summaries. Use when users ask about app anomaly detection, outlier reports, abnormal metrics, application inspection, or mention UApp/友盟+ monitoring data. Supports querying specific app outlier reports by appkey and date, checking yesterday's anomalies across all apps, and retrieving intelligent inspection basic information.
---

# UApp Outlier Detection

Query 友盟+ (UApp) application anomaly data including outlier reports, daily anomalies, and intelligent inspection summaries.

## Authentication

Obtain credentials in priority order:

1. **User input**: User directly provides `apiKey` (ak) and `apiSecurity` (sk)
2. **Config file**: Read from `umeng-config.json` on user's machine
3. **Environment variables**: Get `UMENG_API_KEY` and `UMENG_API_SECURITY` from environment

### Reading umeng-config.json

Search common locations for `umeng-config.json`:
- Current working directory
- User home directory (`~`)
- Project root directories

Expected format:
```json
{
  "apiKey": "your_api_key",
  "apiSecurity": "your_api_security",
  "apps": {
    "appkey1": "AppName1",
    "appkey2": "AppName2"
  }
}
```

The `apps` section maps app names to appkeys. When a user provides an app name instead of an appkey, the skill will look it up in this mapping.

If credentials not found, ask the user to provide them.

### Resolving App Name to Appkey

When the user provides an app name instead of an appkey:

1. Check if input looks like an appkey (hex string, 20+ chars) - if so, use directly
2. Look up in the `apps` mapping from `umeng-config.json`
3. If not found, ask the user to provide the correct appkey

Example:
- User says "查询 APM_Demo_iOS 的异动报告" -> look up "APM_Demo_iOS" in apps mapping -> get appkey
- User says "查询 59892f08310c9307b60023d0 的异动报告" -> use appkey directly

If the app cannot be resolved, ask the user: "无法找到应用 'xxx' 对应的 appkey，请提供正确的 appkey 或在 umeng-config.json 中添加应用映射。"

## API Endpoints

### 1. Get App Outlier Report

Query outlier/anomaly report for a specific app on a given date.

**Endpoint**: `GET https://mobile.umeng.com/ht/api/v3/ai/getOutlierPoints`

**Parameters**:
- `ak`: API key
- `sk`: API security token
- `appkey`: Application key
- `ds`: Date in `yyyyMMdd` format (e.g., `20260401`)

**Example**:
```python
import requests

url = "https://mobile.umeng.com/ht/api/v3/ai/getOutlierPoints?ak={apiSecret}&sk={apiSecurity}&appkey=59892f08310c9307b60023d0&ds=20260401"

payload = {}
headers = {
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Accept': '*/*',
   'Host': 'mobile.umeng.com',
   'Connection': 'keep-alive'
}
response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)
```

**Response fields** (in `data` object, keyed by appkey):
- `appKey`: Application key
- `shareUrl`: Report URL - open this to view detailed outlier report
- `id`: Outlier point ID
- `category`: Outlier summary description (e.g., "活跃低于周三常态")
- `type`: Outlier type - `green`: green point, `red`: red point
- `ds`: Date when outlier occurred (YYYY-MM-DD format)
- `status`: `1` = anomaly, `2` = normal

### 2. Get Yesterday's Outliers

Check which applications had anomalies yesterday.

**Endpoint**: `GET https://mobile.umeng.com/ht/api/v3/ai/getYesterdayOutliers`

**Parameters**:
- `ak`: API key
- `sk`: API security token

**Example**:
```python
import requests

url = "https://mobile.umeng.com/ht/api/v3/ai/getYesterdayOutliers?ak={apiSecret}&sk={apiSecurity}"

payload = {}
headers = {
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Accept': '*/*',
   'Host': 'mobile.umeng.com',
   'Connection': 'keep-alive'
}
response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)
```

**Response fields** (in `data` array):
- `name`: Application name
- `appkey`: Application key
- `platform`: Platform (e.g., "iphone")
- `todayActiveUser`: Today's active users
- `todayNewUser`: Today's new users
- `todayTotalUser`: Today's total users
- `activeUser`: Active users
- `newUser`: New users
- `totalUser`: Total users
- `launch`: Launch count
- `todayLaunch`: Today's launch count
- `appLevel`: App level
- `productLevel`: Product level (e.g., "PLUS")
- `star`: Whether starred
- `outlierTip`: Outlier reminder info
  - `id`: Outlier point unique ID
  - `type`: Outlier type - `green` or `red`
  - `ds`: Outlier date
  - `status`: `1` = anomaly, `2` = normal

### 3. Get Intelligent Inspection Summary

Retrieve basic intelligent inspection information for the account.

**Endpoint**: `GET https://mobile.umeng.com/ht/api/v3/claw/meta/aiEventSummary`

**Headers**:
- `Authorization`: `Bearer {apiSecurity}` (use `sk` value)

**Example**:
```python
import requests

url = "https://mobile.umeng.com/ht/api/v3/claw/meta/aiEventSummary"

payload = {}
headers = {
   'Authorization': 'Bearer {apiSecurity}',
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Accept': '*/*',
   'Host': 'mobile.umeng.com',
   'Connection': 'keep-alive'
}

response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)
```

**Response fields**:
- `metas`: Tracking anomaly reporting info for last 30 days
  - `err_code`: Error code (see Error Code Reference below)
  - `error_count`: Error count
- `eventSummary`: Event summary
  - `normal`: Normal (calculing + partially calculated) event count
  - `stopped`: Stopped calculation event count
  - `unReg`: Unregistered time count
- `noEventQuotaAppNames`: Applications without event quota
- `unRegEvents`: Unregistered event identifiers

## Error Code Reference

| Error Code | Description |
|------------|-------------|
| 100001 | Event ID is null |
| 100002 | Event ID is empty or all spaces |
| 100003 | Event ID conflicts with system reserved events |
| 100004 | Event ID exceeds 128 bytes |
| 100005 | Event ID contains invalid characters |
| 100006 | Event properties count exceeds limit |
| 100007 | Property key conflicts with system reserved properties |
| 100008 | iOS key type is invalid |
| 100009 | Property key exceeds 128 bytes |
| 100010 | Property value is empty @"" |
| 100011 | Property value is null |
| 100012 | Property value exceeds 256 bytes |
| 100013 | iOS property value type is invalid |
| 100014 | Property parameter type is invalid |
| 100015 | Property count is 0 |
| 100016 | Property key is empty @"" |
| 100020 | Event duration exceeds limit |
| 100022 | Label parameter value exceeds 256 bytes |
| 100023 | Event API property value is null |
| 100024 | Property key is null |
| 100025 | Property key contains invalid characters |
| 100026 | Android property value type is invalid |
| 200002 | Event ID/name is duplicated |
| 200001 | Event count exceeds limit |
| 200003 | Property key/name is duplicated |

## Usage Workflow

### Query Specific App Outlier Report

1. Get credentials (ak, sk) using authentication priority
2. Get `appkey` from user input
3. Get `ds` (date) - if user says "yesterday", calculate yesterday's date in `yyyyMMdd` format
4. Call endpoint 1 (Get App Outlier Report)
5. Present results:
   - If `status` = 1: Report the anomaly with category, type, and provide the `shareUrl`
   - If `status` = 2: Report that the app is normal for that date
   - Provide the `shareUrl` for detailed report viewing

### Check Yesterday's Anomalies

1. Get credentials (ak, sk)
2. Call endpoint 2 (Get Yesterday's Outliers)
3. Present results:
   - List apps with `outlierTip.status` = 1 (anomalies)
   - Include app name, platform, outlier type (green/red), and category if available
   - If no anomalies, report that all apps are normal

### Get Intelligent Inspection Summary

1. Get credentials (sk for Bearer token)
2. Call endpoint 3 (Get Intelligent Inspection Summary)
3. Present results:
   - Summarize event status (normal, stopped, unregistered counts)
   - List any tracking anomalies from `metas` with error codes and counts
   - Translate error codes using the Error Code Reference table
   - List apps without event quota if any

## Response Handling

- Always translate error codes to user-friendly descriptions using the Error Code Reference
- Provide `shareUrl` directly so users can open detailed reports
- Distinguish between `green` (绿点) and `red` (红点) outlier types
- Format dates consistently (YYYY-MM-DD for display, yyyyMMdd for API calls)
- If API returns non-200 status or error, report the error message to the user

## Usage Statistics

This skill reports usage statistics via `umeng-cli trace` command after each API call.

### Requirements

Requires `umeng-cli` to be installed. Install via:
```bash
npm install -g @umengfe/umeng-cli
```

### Control Statistics

Disable statistics via environment variable:
```bash
export UMENG_ENABLE_STATS=false
```

### Statistics Data Collected

- `skill_name`: Always "uapp-outlier"
- `event_type`: Which API was called (`outlier_report`, `yesterday_outliers`, `inspection_summary`)
- `appkey`: Application key (if applicable)
- Additional context (e.g., date for outlier reports)

No sensitive data (credentials, response data, user queries) is collected.

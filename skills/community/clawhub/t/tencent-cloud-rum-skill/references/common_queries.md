# RUM-WEB Problem Analysis Workflows

This document contains four major analysis workflows. The AI should match the appropriate workflow based on user needs.

---

## Flow 1: TOP Exception Analysis

### Step 1: Get RUM Application Info
- **Goal**: Determine the RUM application ID to analyze
- **Action**: See "Application Info Retrieval Rules" in SKILL.md

### Step 2: Query Exception Metrics Overview (All Types)
- **Goal**: Understand the overall exception landscape
- **Action**: Call `QueryRumWebMetric`
  - `Metric`: `exception`
  - `GroupBy`: `["level"]`
  - `Limit`: `100`
  - No level filter in Filters (query all exception types)
- **Analysis**: Count exceptions by type (level), identify which types are most severe

### Step 3: Analyze TOP JS/Promise Errors
- **Goal**: Find the most frequent JS/Promise errors
- **Action**: Call `QueryRumWebMetric`
  - `Metric`: `exception`
  - `Filters`: `[{"Key":"level","Operator":"in","Value":"('4','8')"}]`
  - `GroupBy`: `["error_msg"]`
  - `Limit`: `100`
- **Output**: TOP JS/Promise errors grouped by error message (count, affected users, error rate)

### Step 4: Analyze Other Important Exception Types
- **Goal**: Analyze other high-frequency exceptions discovered in Step 2
- **Action**: For each notable exception type (e.g., resource loading errors), call `QueryRumWebMetric`
  - `Metric`: `exception`
  - `Filters`: Set corresponding level value (e.g., level=32 for script loading errors)
  - `GroupBy`: Choose appropriate field (e.g., `["from"]`)
  - `Limit`: `100`

### Step 5: Analyze Exception Distribution
- **Goal**: Understand TOP exception distribution patterns
- **Action**: For each TOP exception, run multi-dimensional analysis:
  - By page: `GroupBy`: `["from"]`
  - By platform: `GroupBy`: `["platform"]`
  - By version: `GroupBy`: `["version"]`
- **Note**: Run separate GroupBy queries for each dimension — never combine all dimensions in one query

### Step 6: Query Specific Exception Logs
- **Goal**: Get detailed log info for TOP exceptions to analyze root causes
- **Action**: For each TOP exception, call `QueryRumWebLog`
  - `Filters`: Set conditions based on the specific exception
    - Corresponding level type
    - For JS errors, use `msg` field with `like` to match error_msg
  - `Limit`: `10` (representative samples)
  - `RespFields`: Set based on analysis needs
- **Analysis**: Review full error stack traces, occurrence context, user environment

### Step 7: APM Correlation (If Applicable)
- **Trigger**: Exception is API-related and log `trace` field is non-empty
- **Action**:
  1. Call `QueryApmLinkId` to get the linked APM application ID
  2. Follow "APM Trace Analysis Steps" in apm_analysis.md

### Step 8: Output Analysis Conclusions
- **Output**:
  1. **TOP Exception List**: Ranked by severity (count, affected users, error rate)
  2. **Exception Type Distribution**: Proportions and trends of each type
  3. **Root Cause Analysis per TOP Exception**:
     - Error description and message
     - Most affected pages
     - Most affected user groups (platform, browser, version, etc.)
     - Typical occurrence scenarios
     - Probable root causes
  4. **Optimization Recommendations**: Specific fix suggestions for each TOP exception

---

## Flow 2: TOP Page Performance Analysis

### Step 1: Get RUM Application Info
- **Goal**: Determine the RUM application ID to analyze

### Step 2: Query LCP Performance Metrics by Page
- **Goal**: Identify the worst-performing TOP pages
- **Action**: Call `QueryRumWebMetric`
  - `Metric`: `performance`
  - `GroupBy`: `["from"]` (group by page URL)
  - `Limit`: `100`
- **Analysis Focus**:
  - Combine LCP values and request counts to find pages with highest LCP and greatest impact
  - LCP (Largest Contentful Paint) is the key page performance indicator
  - Record TOP 5-10 worst-performing pages

### Step 3: Analyze Detailed Performance Metrics per TOP Page
- **Goal**: Understand performance breakdown for each TOP page
- **Action**: For each TOP page, call `QueryRumWebMetric`
  - `Metric`: `performance`
  - `Filters`: `[{"Key":"from","Operator":"=","Value":"<specific_page_URL>"}]`
  - `Limit`: `100`
  - No GroupBy (get overall metrics)
- **Key Metrics**:
  - `lcp_avg`: LCP average
  - `fcp_avg`: FCP average
  - `dns_avg`: DNS lookup time
  - `tcp_avg`: TCP connection time
  - `ssl_avg`: SSL handshake time
  - `ttfb_avg`: TTFB time
  - `content_download_avg`: Content download time
  - `dom_parse_avg`: DOM parse time
  - `resource_download_avg`: Resource download time
  - `fmp_avg`: First meaningful paint time

### Step 4: Diagnose Performance Bottleneck Type
- **Goal**: Determine the main performance bottleneck for each TOP page
- **Analysis Logic**:
  - **Network layer slow**: If DNS, TCP, SSL times are high → Execute Step 5 (region & ISP analysis)
  - **Resource loading slow**: If resource download time is high → Execute Step 6 (resource analysis)
  - **Content rendering slow**: If DOM parse, content download times are high → Skip to recommendations (Step 8)

### Step 5: Network Layer Analysis (If DNS/TCP/SSL Slow)
- **Goal**: Determine if specific regions or ISPs cause network slowness
- **Operation A - By Region**:
  - `Metric`: `performance`
  - `Filters`: `[{"Key":"from","Operator":"=","Value":"<specific_page_URL>"}]`
  - `GroupBy`: `["region"]`
  - `Limit`: `100`
- **Operation B - By ISP**:
  - `GroupBy`: `["isp"]`
  - `Limit`: `100`
- **Analysis Focus**: Identify regions/ISPs with abnormally high DNS/TCP/SSL times

### Step 6: Resource Loading Analysis (If Resource Download Slow)
- **Goal**: Find specific slow-loading resources
- **Action**: Call `QueryResourceByPage`
  - `ProjectId`: Application ID
  - `From`: Specific page URL
  - Time range: Consistent with previous queries
- **Analysis Focus**:
  - `duration_avg`: Average resource loading time
  - `connect_time_avg`: Connection time
  - `domain_lookup_avg`: Domain lookup time
  - `transfer_size_avg`: Transfer size (negative means cross-origin prevents retrieval; suggest configuring `Timing-Allow-Origin`)
  - `error_rate_percent`: Resource loading error rate
  - Sort by duration to find TOP slow resources

### Step 7: Multi-Dimensional Resource Analysis (For Slow Resources)
- **Goal**: Analyze if slow resources correlate with region, ISP, etc.
- **Operation A - By Region**: `GroupBy`: `["region"]`
- **Operation B - By ISP**: `GroupBy`: `["isp"]`
- **Operation C - By Platform**: `GroupBy`: `["platform"]`
- **Note**: Run separate GroupBy queries for each dimension

### Step 8: Output Comprehensive Analysis Report
- **Output**:
  1. **TOP Performance Problem Pages** (sorted by LCP descending)
     - Page URL, LCP average, breakdown timing data
  2. **Performance Bottleneck Diagnosis per TOP Page**
     - Main bottleneck type (network/resource/rendering)
     - Specific bottleneck metrics and values
     - Network issues: affected regions and ISPs
     - Resource issues: slow resource list with timings
  3. **Performance Problem Distribution**
     - Platform distribution (iOS/Android/PC)
     - Browser distribution
     - Version distribution
     - Regional distribution
  4. **Optimization Recommendations** (per bottleneck type)
     - **DNS**: DNS prefetch, CDN acceleration
     - **TCP/SSL**: Enable HTTP/2, connection reuse, optimize SSL config
     - **Resource Loading**: Compress resources, use CDN, lazy loading, optimize sizes
     - **DOM Rendering**: Reduce DOM depth, optimize critical rendering path, code splitting
     - **Content Download**: Enable Gzip/Brotli, optimize above-the-fold resources
     - **Regional**: Add CDN edge nodes for slow regions, optimize routing
     - **ISP**: Multi-line access, coordinate with specific ISPs

---

## Flow 3: TOP API Performance & Stability Analysis

### Step 1: Get RUM Application Info
- **Goal**: Determine the RUM application ID to analyze

### Step 2: Query API Overview Metrics
- **Goal**: Understand overall API request health
- **Action**: Call `QueryRumWebMetric`
  - `Metric`: `network`
  - No GroupBy (get overall metrics)
  - `Limit`: `100`
- **Analysis Focus**:
  - `allCount`: Total API request count
  - `duration_avg`: Average API latency
  - `error_rate_percent`: Status code error rate
  - `retcode_error_percent`: Retcode error rate
  - Initial assessment: performance issue vs. stability issue

### Step 3: Analyze TOP Slow APIs (Performance Dimension)
- **Goal**: Find APIs with highest latency
- **Action**: Call `QueryRumWebMetric`
  - `Metric`: `network`
  - `GroupBy`: `["url"]` (group by API URL)
  - `Limit`: `100`
- **Analysis**: Sort by `duration_avg`, identify TOP 5-10 slowest APIs with URL, latency, count, error rate

### Step 4: Analyze TOP Error APIs (Stability Dimension)
- **Operation A - By Error Rate**:
  - `Metric`: `network`
  - `GroupBy`: `["url"]`
  - `Limit`: `100`
- **Operation B - By Status Code**:
  - `Metric`: `network`
  - `GroupBy`: `["url", "status"]`
  - `Limit`: `100`
- **Analysis**: Identify high error rate APIs, analyze HTTP status code distribution (4xx, 5xx), distinguish status code vs. retcode errors

### Step 5: Multi-Dimensional Analysis of TOP APIs
- **Goal**: Understand distribution patterns to locate root causes
- **Action**: For each TOP problem API:
  - **A. By Region**: `GroupBy`: `["region"]`
  - **B. By ISP**: `GroupBy`: `["isp"]`
  - **C. By Platform**: `GroupBy`: `["platform"]`
  - **D. By Version**: `GroupBy`: `["version"]`
  - **E. By Page Source**: `GroupBy`: `["from"]`
- **Note**: Run separate GroupBy queries for each dimension

### Step 6: Analyze Retcode Business Errors (If Present)
- **Goal**: Deep dive into business return code errors
- **Action**: For APIs with high retcode error rate:
  - `Metric`: `network`
  - `Filters`: `[{"Key":"url","Operator":"like","Value":"<specific_API_URL>"},{"Key":"is_err","Operator":"=","Value":"1"}]`
  - `GroupBy`: `["ret"]` (group by return code)
  - `Limit`: `100`
- **Analysis**: Identify specific error codes, count occurrences and proportions

### Step 7: Query TOP API Detailed Logs
- **Goal**: Get detailed request logs for problem APIs
- **Action**: For each TOP problem API, call `QueryRumWebLog`
  - `Filters`:
    - By API: `[{"Key":"msg","Operator":"like","Value":"<API_URL>"}]`
    - For error analysis, add level filter: `[{"Key":"level","Operator":"in","Value":"('16','1024')"}]` (AJAX_ERROR and RET_ERROR)
  - `Limit`: `10`
  - `RespFields`: Based on analysis needs
- **Analysis**: Review error stacks, request params, user environment, network state, check `trace` field for APM correlation

### Step 8: APM Deep Analysis (If Applicable)
- **Trigger**: Log `trace` field is non-empty
- **Action**:
  1. Call `QueryApmLinkId` to get linked APM application ID
  2. Follow "APM Trace Analysis Steps" in apm_analysis.md

### Step 9: Output Comprehensive Analysis Report
- **Output**:
  1. **TOP API Problem List**
     - **TOP Slow APIs** (by avg latency desc): URL, avg latency, count, error rate
     - **TOP Error APIs** (by error rate/count desc): URL, status code error rate, retcode error rate, main error codes, count
  2. **Root Cause Analysis per TOP API**
     - Performance root cause
     - Stability root cause: error types, specific error codes, occurrence scenarios, backend service errors, affected user characteristics
  3. **Problem Distribution**: Regional, ISP, platform, version, page distribution
  4. **Optimization Recommendations**
     - **API Latency**: Backend optimization, request merging, caching, CDN, network routing for slow regions
     - **Status Code Errors**: 4xx — check frontend validation & permissions; 5xx — backend stability & capacity; Network errors — adjust timeouts & retry
     - **Retcode Business Errors**: Strengthen frontend validation, optimize user guidance, improve business logic, friendlier error messages
     - **Regional/ISP**: Deploy edge nodes, multi-line access, smart routing

---

## Flow 4: TOP Slow Resource Loading Analysis

### Step 1: Get RUM Application Info
- **Goal**: Determine the RUM application ID to analyze

### Step 2: Query Static Resource Overview Metrics
- **Goal**: Understand overall static resource loading health
- **Action**: Call `QueryRumWebMetric`
  - `Metric`: `resource`
  - `GroupBy`: `["url"]` (group by resource URL)
  - `Limit`: `100`
- **Analysis Focus**:
  - `allCount`: Total resource request count
  - `duration_avg`: Average resource loading time
  - `error_rate_percent`: Resource loading error rate
  - Rank by `duration_avg` and `allCount` to identify high-impact slow resources

### Step 3: Identify TOP Slow Resources
- **Goal**: Find resources with highest loading time
- **Output**:
  - TOP 10-20 slowest resource URLs
  - Per resource: avg duration, count, error rate, connection time, domain lookup time, transfer size

### Step 4: Multi-Dimensional Analysis of TOP Slow Resources
- **Goal**: Understand distribution patterns to locate root causes
- **Action**: For each TOP slow resource:
  - **A. By Region**:
    - `Metric`: `resource`
    - `Filters`: `[{"Key":"url","Operator":"=","Value":"<specific_resource_URL>"}]`
    - `GroupBy`: `["region"]`
    - `Limit`: `100`
  - **B. By ISP**: `GroupBy`: `["isp"]`
  - **C. By Platform**: `GroupBy`: `["platform"]`
  - **D. By Network Type**: `GroupBy`: `["net_type"]`
- **Note**: Run separate GroupBy queries for each dimension

### Step 5: Diagnose Specific Bottlenecks for Slow Resources
- **Analysis Logic** (based on Step 3 and Step 4 data):
  - **Network layer slow**:
    - High `connect_time_avg` → TCP/SSL handshake slow
    - High `domain_lookup_avg` → DNS resolution slow
    - Root cause: Network quality issues, specific region/ISP problems
  - **Transfer layer slow**:
    - High `duration_avg` but normal `connect_time_avg` and `domain_lookup_avg`
    - Large `transfer_size_avg` (note: negative means cross-origin prevents retrieval)
    - Root cause: Oversized resources, insufficient bandwidth, CDN not deployed or misconfigured

### Step 6: Query Slow Resource Logs (Optional)
- **Goal**: Get specific resource loading logs for anomaly analysis
- **Action**: Call `QueryRumWebLog`
  - `Filters`:
    - `[{"Key":"msg","Operator":"like","Value":"<resource_URL>"}]`
    - For slow resource requests: `[{"Key":"level","Operator":"eq","Value":"1029"}]` (SLOW_ASSET_REQUEST)
    - For resource errors: `[{"Key":"level","Operator":"eq","Value":"1028"}]` (ASSERT_REQUEST)
  - `Limit`: `10`
  - `RespFields`: Based on analysis needs
- **Analysis**: Resource loading failure scenarios, user environment, network state, specific error messages

### Step 7: Output Comprehensive Analysis Report
- **Output**:
  1. **TOP Slow Resources** (sorted by avg duration descending)
     - Resource URL, avg loading time, count, transfer size, connection time, domain lookup time, error rate
  2. **Root Cause Analysis per TOP Slow Resource**
  3. **Severity Assessment**: Occurrence count, impact on overall page performance
  4. **Optimization Recommendations** (per problem type)
     - **Network Layer**: DNS prefetch (`<link rel="dns-prefetch">`), HTTP/2 or HTTP/3, optimize SSL, add CDN edge nodes for slow regions
     - **Transfer Layer**: Compress (Gzip/Brotli), image optimization (WebP, lazy loading, responsive images), code splitting & on-demand loading, CDN acceleration, resource merging (CSS Sprites, inline small resources)
     - **Cross-Origin Configuration**: Add `Timing-Allow-Origin: *` to resource server response headers, verify resource domain configuration
     - **Caching**: Set proper cache policies (Cache-Control), browser cache & Service Worker, CDN cache configuration
     - **Regional/ISP**: Deploy more CDN edge nodes for slow regions, multi-line access, smart DNS resolution

---

## Common Query Examples

### List Applications

```json
// View all applications (returns up to 50)
Tool: QueryRumWebProjects
Params: {}

// Verify existence by ProjectId (Scenario A)
Tool: QueryRumWebProjects
Params: {"ProjectId": "123456"}

// Exact match by app name (Scenario B, step 1)
Tool: QueryRumWebProjects
Params: {"ProjectName": "my-app"}

// Fuzzy search by name (Scenario B, step 2)
Tool: QueryRumWebProjects
Params: {"ProjectNameLike": "my-app"}
```

### Network Request Metrics

```json
// API request overview
Tool: QueryRumWebMetric
Params: {
    "ProjectId": "123456",
    "Metric": "network",
    "Limit": 100
}

// Group by API URL for latency analysis
Tool: QueryRumWebMetric
Params: {
    "ProjectId": "123456",
    "Metric": "network",
    "GroupBy": ["url"],
    "Limit": 100
}
```

### Exception Queries

```json
// All exception types overview
Tool: QueryRumWebMetric
Params: {
    "ProjectId": "123456",
    "Metric": "exception",
    "GroupBy": ["level"],
    "Limit": 100
}

// TOP JS/Promise errors
Tool: QueryRumWebMetric
Params: {
    "ProjectId": "123456",
    "Metric": "exception",
    "Filters": [{"Key": "level", "Operator": "in", "Value": "('4','8')"}],
    "GroupBy": ["error_msg"],
    "Limit": 100
}
```

### Page Performance Queries

```json
// Performance by page
Tool: QueryRumWebMetric
Params: {
    "ProjectId": "123456",
    "Metric": "performance",
    "GroupBy": ["from"],
    "Limit": 100
}
```

### Log Searches

```json
// Error logs
Tool: QueryRumWebLog
Params: {
    "ProjectId": "123456",
    "Limit": 10,
    "Filters": [
        {"Key": "level", "Operator": "in", "Value": "('4','8','16','32')"}
    ],
    "RespFields": ["ts", "level", "errorMsg", "from", "msg", "version", "os", "trace"]
}

// API-related logs by URL
Tool: QueryRumWebLog
Params: {
    "ProjectId": "123456",
    "Limit": 10,
    "Filters": [
        {"Key": "msg", "Operator": "like", "Value": "api.example.com"}
    ],
    "RespFields": ["ts", "level", "msg", "from", "trace"]
}

// Logs for a specific user
Tool: QueryRumWebLog
Params: {
    "ProjectId": "123456",
    "Limit": 50,
    "Filters": [
        {"Key": "uin", "Operator": "eq", "Value": "user_12345"}
    ]
}
```

### Query Resources by Page

```json
Tool: QueryResourceByPage
Params: {
    "ProjectId": "123456",
    "From": "https://example.com/home"
}
```

### APM Correlation

```json
Tool: QueryApmLinkId
Params: {
    "ProjectId": "123456"
}
```

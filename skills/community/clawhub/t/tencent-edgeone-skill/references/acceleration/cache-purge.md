# Cache Purge and Prefetch

Manage EdgeOne node cache: query quotas, purge cache (URL / Directory / Host / All / Cache Tag), prefetch URLs, and check task progress. Supports batch URL input from files or paste.

## Core Interaction Guidelines

1. **Site Selection and Confirmation**: Before executing any cache operation, users must first confirm the target site (see Scenario 0)
2. **Check Quota Before Submission**: Before executing CreatePurgeTask / CreatePrefetchTask, call DescribeContentQuota to display remaining quota; warn users if insufficient
3. **Batch URL Input**: Support users to input URLs in batch from files or by pasting (see Scenario E)
4. **Poll Task Progress**: Actively query progress after task submission until completion or timeout

## Scenario 0: Select Site

**Trigger**: Before users request cache purge or URL prefetch, the target site must be confirmed first.

**Steps**:

1. **Call DescribeZones to query site list**
   - **Important**: Filter out sites with `Status` as `initializing` (these sites are still initializing and haven't completed creation)
   - **Critical**: **Must use pagination** to retrieve all sites:
     - Set `Limit=100` (maximum value)
     - Set `Offset=0` initially, increment by 100 each iteration
     - Loop until `Offset + Limit >= TotalCount`
     - Merge all paginated results
   - Refer to [zone-discovery.md](../api/zone-discovery.md) for detailed pagination implementation
   - Only display available sites

2. **Determine the number of sites**:
   
   **a) Only one site**
   - Directly use this site without user selection
   - Continue to subsequent operations

   **b) Multiple sites**
   - List all available sites, including:
     - Site domain name (ZoneName)
     - Alias Zone Name (AliasZoneName, if any)
     - Site ID (ZoneId)
     - Access mode (Type)
   - Guide users to select the site to operate on

   **c) No available sites**
   - Prompt user: "No available sites under current account, please create a site first"
   - Terminate operation

3. **Handle sites with same name**:
   - If multiple sites with the same name exist (same ZoneName), they must be distinguished by `AliasZoneName` (Alias Zone Name identifier)
   - Display format: `Site domain (identifier)` or `Site domain [identifier]`
   - Example: `example.com (prod)` and `example.com (test)`

4. **Get Site ID**:
   - After user confirms the site, record the site's `ZoneId`
   - All subsequent API calls use this `ZoneId`

> **Important Notes**:
> - Site selection is a prerequisite for all cache operations and cannot be skipped
> - Alias Zone Name (AliasZoneName) is used to distinguish sites with the same name created with different access modes (CNAME, DNSPod hosting)
> - If the user explicitly specifies the site domain or identifier in the request, you can directly use this information to query the corresponding site

## Scenario A: Query Quota

**Trigger**: User says "how many more can I purge", "check quota", "how much prefetch quota left".

> **Prerequisite** (optional): If user hasn't specified a site, complete [Scenario 0: Select Site](#scenario-0-select-site) first

Call `DescribeContentQuota`, passing parameters:
- `ZoneId`: Site ID (optional, query account-level quota if not provided)

**Output suggestion**: Display quota usage for each type in a table, marking types with less than 10% remaining.

## Scenario B: Cache Purge

**Trigger**: User says "purge cache", "clear CDN cache", "purge URL", "purge directory", "purge entire site".

> **Prerequisites**:
> 1. Complete [Scenario 0: Select Site](#scenario-0-select-site) to confirm the site to operate on
> 2. Call DescribeAccelerationDomains to confirm available acceleration domains under the site
> 3. Call DescribeContentQuota (Scenario A) to display remaining quota; warn user if insufficient for the corresponding type

### B1: Confirm Purge Type and Method

Before executing purge, **must** have users confirm the following information:

#### 1. Purge Type

| Type | Parameter Value | Description | Impact Scope |
|------|--------|------|----------|
| **URL Purge** | `purge_url` | Purge specified URLs | Exactly matched URLs |
| **Directory Purge** | `purge_prefix` | Purge all resources under specified directory | All files under directory and subdirectories |
| **Hostname Purge** | `purge_host` | Purge all resources under specified domain | All cache of the entire acceleration domain |
| **Full Site Purge** | `purge_all` | Purge all resources under the site | ⚠️ All cache on all nodes of the site |
| **Cache Tag Purge** | `purge_cache_tag` | Purge by cache tag | All cache with specified tags |

#### 2. Purge Method

Purge method is **only valid for the following three purge types**:
- ✅ **Directory Purge** (`purge_prefix`)
- ✅ **Hostname Purge** (`purge_host`)
- ✅ **Full Site Purge** (`purge_all`)

Other purge types (URL purge, Cache Tag purge) do not support the purge method parameter.

**Available Values**:

| Method | Parameter Value | Description | Recommended Scenario |
|------|--------|------|----------|
| **Invalidate Cache** | `invalidate` | Mark cache as expired, validate with origin on next request | Default method, less pressure on origin |
| **Delete Cache** | `delete` | Directly delete cache, always fetch from origin on next request | Emergency updates, forced refresh scenarios |

> **Important Notes**:
> - The `invalidate` method keeps the cache but marks it as expired; on the next request, it validates with the origin through mechanisms like If-Modified-Since, and can continue using cache if content hasn't changed
> - The `delete` method directly deletes the cache; all subsequent requests will fetch from origin, which will increase origin load in a short time

#### 3. User Confirmation Process

**Prompt user**:
1. Display purge types and their impact scope
2. If selecting `purge_prefix`, `purge_host`, or `purge_all`, ask about purge method
3. If selecting `purge_all` (full site purge), **must** specially warn:
   > ⚠️ **Full site purge is a high-impact operation**: It will clear all node cache of this site; in a short time, a large number of requests will fetch from origin, which may cause origin pressure to surge. Please confirm whether to continue?

4. Wait for user's explicit confirmation before executing

> **No automatic purge**: Cache purge will invalidate node cache; subsequent requests will fetch the latest content from origin, which may increase origin load. **Must** explain the purge type and impact scope to users and wait for explicit confirmation before execution.

### B2: Execute Purge

**Call** `CreatePurgeTask`, passing parameters:
- `ZoneId`: Site ID (from Scenario 0)
- `Type`: Purge type
- `Method`: Purge method (only valid when Type is `purge_prefix`, `purge_host`, or `purge_all`)
- `Targets`: List of URLs / directories / domains to purge

**Follow-up**: Inform user that the task has been submitted and provide JobId. If confirmation of execution result is needed, go to [Scenario D](#scenario-d-query-task-progress).

## Scenario C: URL Prefetch

**Trigger**: User says "prefetch URL", "prefetch cache", "prefetch", "preload resources".

> **Prerequisites**:
> 1. Complete [Scenario 0: Select Site](#scenario-0-select-site) to confirm the site to operate on
> 2. Call DescribeContentQuota (Scenario A) to display remaining `prefetch_url` quota
> 3. (Optional) Call DescribePrefetchOriginLimit to query origin rate limit for the target domain

URL prefetch actively fetches resources from origin to edge node cache, suitable for preloading hot resources before major promotions or version releases.

### C1: URL Format Check

Before executing prefetch, **must** check if URL format meets requirements:

**✅ Supported URL Formats**:
- Complete HTTP/HTTPS URL: `https://example.com/path/to/file.jpg`
- URL with query parameters: `https://example.com/api/data?id=123&type=json`
- Specific file path: `https://cdn.example.com/images/banner.png`

**❌ Unsupported URL Formats**:
- ⚠️ **URLs with wildcards**: `https://example.com/path/*` or `https://example.com/*.jpg`
- Directory paths: `https://example.com/path/` (for directory prefetch, use multiple specific file URLs)
- Incomplete URLs: `example.com/path` (missing protocol)

**Check Rules**:
1. URL must start with `http://` or `https://`
2. URL cannot contain wildcards `*` or `?` (except `?` in query parameters)
3. It's recommended that each URL points to a specific file resource

**Processing Flow**:
```
Iterate through user-provided URL list
  ├─ Check if contains wildcards (* ?)
  │  ├─ Contains → Prompt user: "Prefetch doesn't support wildcard URLs, please provide specific file URLs"
  │  └─ Doesn't contain → Continue
  ├─ Check protocol
  │  ├─ Missing http/https → Prompt user to add protocol
  │  └─ Has protocol → Continue
  └─ Add to valid URL list
```

> **Important Notes**:
> - Prefetch only supports URL granularity, not directory or domain level
> - To prefetch an entire directory, you need to provide a complete URL list of all files under that directory
> - Wildcard purge is partially supported in cache purge scenarios (such as directory purge), but not supported in prefetch scenarios

### C2: Execute Prefetch

**Call** `CreatePrefetchTask`, passing parameters:
- `ZoneId`: Site ID (from Scenario 0)
- `Targets`: List of URLs to prefetch (passed format check)

**Follow-up**: Inform user that the task has been submitted and provide JobId. If confirmation of execution result is needed, go to [Scenario D](#scenario-d-query-task-progress).

### C3: Query Prefetch Origin Rate Limit (DescribePrefetchOriginLimit)

> This interface is a whitelist beta feature, only use when user mentions "prefetch rate limit".

Call `DescribePrefetchOriginLimit`.

**Output suggestion**: If the domain has rate limit configuration, remind the user of the current bandwidth limit before prefetching; large-scale prefetch may be affected by this limit.

## Scenario D: Query Task Progress

**Trigger**: User says "is purge done", "check task progress", "prefetch status".

### D1: Query Purge Tasks

Call `DescribePurgeTasks`.

### D2: Query Prefetch Tasks

Call `DescribePrefetchTasks`, parameters and Filters similar to purge tasks.

**Output suggestion**: Display task list in a table, marking tasks with `failed` and `timeout` status. If there are failed tasks, suggest users to check if URLs are correct or retry later.

> Prefetch tasks additionally have `invalid` status, indicating origin response is non-2xx; need to check origin service.

### D3: Auto-poll Progress After Submission

After submitting purge / prefetch tasks, should actively poll task status until terminal state:

1. Get `JobId` after submitting task
2. Wait 5-10 seconds before querying status
3. If still `processing`, continue waiting and retry (suggest 10-second interval)
4. If reaching terminal state (`success` / `failed` / `timeout` / `canceled`), summarize results and display to user

> Usually URL purge completes in 1-2 minutes, directory / Host purge in 3-5 minutes; prefetch time depends on resource size and quantity.

## Scenario E: Batch URL Input

**Trigger**: User provides a large number of URLs (read from file or directly paste multiple lines).

### E1: Extract URLs from User's Pasted Text

When user pastes multiple lines of URLs:
1. Split text by lines, one URL per line
2. Filter out empty lines and comment lines (starting with `#`)
3. Ensure each URL starts with `http://` or `https://`
4. Summarize valid URL count and display to user for confirmation

### E2: Read URL List from File

When user says "import from file", "read URL list file":
1. Read user-specified file (support `.txt`, `.csv` and other plain text formats)
2. Parse by lines, filter empty lines and comments
3. Display parsed URL count and first few samples, ask user to confirm

### E3: Batch Submission Considerations

- **Check Quota**: First query DescribeContentQuota to ensure remaining quota ≥ URL count
- **Single Batch Limit**: Number of URLs submitted each time is subject to single batch upper limit; automatically submit in batches when exceeding limit
- **URL Deduplication**: Deduplicate before submission to avoid wasting quota
- **Result Summary**: After all batches are submitted, summarize JobId list and failed items, query progress uniformly

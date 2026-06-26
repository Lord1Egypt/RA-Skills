# Site One-Click Onboarding Guide

End-to-end domain onboarding to EdgeOne: confirm plan → create site → verify ownership → add acceleration domain → apply and deploy certificate.

## Important Concepts

### Alias Zone Name (AliasZoneName)

When you create two or more sites with the same site name, you need to use an **Alias Zone Name** to distinguish them.

**Use Cases**:
- Same domain using different access modes (CNAME access, DNSPod hosting access)
- Same domain configured with different acceleration or security strategies

**Format Requirements**:
- Allows combination of numbers, English letters, `.`, `-`, and `_`
- Length limit: within 200 characters
- Examples: `site-prod`, `site-test`, `site_backup`

**Access Mode Restrictions**:
- ✅ **CNAME Access**: Supports creating multiple sites with same name
- ✅ **DNSPod Hosting Access**: Supports creating multiple sites with same name
- ❌ **NS Access**: A domain can only be accessed via NS once, does not support sites with same name
- ⚠️ **Mutual Exclusion Rule**: Domains accessed via NS cannot use other access modes; domains accessed via CNAME/DNSPod hosting cannot use NS access

### Site Status Determination Logic

When displaying site status to users, the effective status should be determined by evaluating the following fields from `DescribeZones` response **in order** (first match wins):

| Priority | Condition | Display Status |
|---|---|---|
| 1 | `Status == "initializing"` | Initializing — **must be filtered out, do not display to user** |
| 2 | `Status == "forbidden"` | forbidden |
| 3 | `Status == "deleted"` | Deleted |
| 4 | `ActiveStatus == "changing"` | Changing |
| 5 | `ActiveStatus == "inPausing"` | Pausing |
| 6 | `Paused == true` | Paused |
| 7 | None of the above | Active |

> **Important**: This logic must be applied in all scenarios where site status is displayed, including site selection (D0) and status queries (F).

## Access Mode Description

EdgeOne supports four site access modes:

### Access Modes with Domain

1. **DNSPod Hosting Access** (dnspodAccess)
   - **Prerequisites**: Domain is hosted in DNSPod and status is normal
   - **Advantages**: EdgeOne can directly and automatically complete ownership verification and configuration, best experience
   - **Recommendation**: Strongly recommended if conditions are met
   - **Available Features**: Layer 7 acceleration, Layer 4 proxy, security protection, edge functions

2. **NS Access** (full)
   - **Requirements**: Need to switch NS records to EdgeOne-provided Name Servers at domain registrar
   - **Characteristics**: EdgeOne fully takes over domain DNS resolution
   - **Available Features**: Layer 7 acceleration, Layer 4 proxy, security protection, edge functions, DNS resolution

3. **CNAME Access** (partial)
   - **Requirements**: Need to manually add TXT record to verify ownership
   - **Characteristics**: Only need to configure CNAME record pointing to EdgeOne, NS record unchanged
   - **Available Features**: Layer 7 acceleration, Layer 4 proxy, security protection, edge functions

### Access Mode without Domain

4. **No Domain Access** (noDomainAccess)
   - **Applicable Scenarios**: Temporarily no domain, or only need Layer 4 proxy and edge functions
   - **Characteristics**:
     - Can create site without providing domain
     - No ownership verification needed
     - Can directly use Layer 4 proxy and edge functions after creation
   - **Available Features**: Only supports Layer 4 proxy, edge functions
   - **Future Extension**: After site creation, can add Layer 7 acceleration domains anytime

## End-to-End Process Overview

### Access Process with Domain

```
1. Confirm Plan (DescribePlans / DescribeAvailablePlans / CreatePlan)
       ↓
2. Create Site (CreateZone)
   ├─ B0: Determine if domain meets specifications
   │  ├─ Meets → Continue with domain access process
   │  └─ Doesn't meet → Prompt to use no-domain access
   ├─ B1: Detect DNSPod hosting status (DescribeDomain)
   │  ├─ Meets conditions: Prioritize recommending DNSPod hosting access
   │  └─ Doesn't meet: Provide CNAME access and NS access
   ├─ B1.5: Domain conflict pre-check (CreateZone DryRun)
   │  ├─ No conflict → Continue creation
   │  ├─ CNAME/DNSPod conflict → Require AliasZoneName
   │  └─ NS conflict → Terminate creation (NS access is exclusive)
   ├─ B2: Confirm access mode and parameters
   │  ├─ Select access mode (DNSPod hosting / NS / CNAME)
   │  ├─ Select acceleration area (mainland/global requires ICP filing)
   │  └─ If conflict exists, provide Alias Zone Name
   ├─ DNSPod hosting access: Automatically complete validation, jump directly to step 4
   ├─ NS access: Switch DNS server
   └─ CNAME access: Add TXT record or file validation
       ↓
3. Verify Ownership (VerifyOwnership) — Can be skipped, verify later
       ↓
4. Add Acceleration Domain (CreateAccelerationDomain)
       ↓
5. Apply and Deploy HTTPS Certificate (see cert-manager.md)
       ↓
   Onboarding Complete
```

### No Domain Access Process

```
1. Confirm Plan (DescribePlans / DescribeAvailablePlans / CreatePlan)
       ↓
2. Create Site (CreateZone, Type = noDomainAccess)
   - Keep ZoneName empty
   - Keep Area empty
   - No ownership verification needed
       ↓
3. Configure Layer 4 proxy or edge functions
       ↓
   Onboarding Complete
```

> Can check verification status anytime via DescribeIdentifications.
> For certificate-related queries and operations, refer to [cert-manager.md](cert-manager.md).

## Scenario A: Confirm Plan

**Trigger**: First step of the process, must confirm plan before creating site.

### A1: Query Existing Plans (DescribePlans)

Call `DescribePlans` to query plans under the account.

#### Filter Logic

From returned plan list, filter available plans by the following conditions:

1. **Bindable**: `Bindable == "true"`
2. **Normal Status**: `Status == "normal"`
3. **Sufficient Quota**: Bound sites < Site quota limit

> Only plans meeting all 3 conditions above can be used for binding.

#### Has Available Plans

> **No Automatic Binding**: Binding plan will consume site quota. **Must** first display plan information to user and wait for explicit selection before binding; never decide on your own.

**Must display all available plans** for user selection, no omissions or truncation:

- If **Only 1 plan**: Still need user confirmation before use
- If **Multiple plans**:
  - **Display Info**: Plan ID, plan type, bound site count
  - **Display Method**: If plan count exceeds structured interaction tool's option limit, display in batches or provide input method to ensure user can see and select all plans
  - **Suggested Sorting**: Sort by bound site count from least to most, convenient for user to select plans with sufficient quota
- User can also choose **not to bind existing plan**, go to A2 to purchase new plan

#### No Available Plans

Go to A2.

### A2: Purchase New Plan (DescribeAvailablePlans → CreatePlan)

Call `DescribeAvailablePlans` to query plan types available for purchase under current account, display options to user.

> **No Automatic Purchase**: Purchasing plan will incur actual charges. **Must** display plan type and pricing info to user, and wait for explicit confirmation before calling `CreatePlan`. Never skip confirmation or decide on your own.

After user explicit confirmation, call `CreatePlan` to purchase plan.

If user confirms not to purchase, remind: **Site needs to be bound to plan to provide normal service**. Sites not bound to plan will be in `init` status and unable to take effect.

### Next Step

After plan confirmation, carry PlanId to [Scenario B: Create Site](#scenario-b-create-site).

## Scenario B: Create Site

**Trigger**: User says "onboard example.com to EdgeOne", "create site", "create new site", or subsequent step after plan confirmation.

> If user directly triggers this scenario (without going through Scenario A), must first guide through [Scenario A: Confirm Plan](#scenario-a-confirm-plan) before continuing.

> **No Automatic Creation**: Creating site will consume plan's site quota. **Must** confirm site domain, access mode, and acceleration area with user before execution; never decide on your own.

### B0: Determine Access Mode Type

**First determine if the site name provided by user meets domain specifications**:

1. **Meets domain specifications** (e.g., `example.com`, `test.com.cn`):
   - Enter access process with domain → Go to [B1: Detect DNSPod Hosting Status](#b1-detect-dnspod-hosting-status)

2. **Doesn't meet domain specifications or user explicitly indicates no domain**:
   - Prompt user: "The site name you provided doesn't meet domain specifications. EdgeOne supports no-domain access mode, which is limited to Layer 4 proxy and edge functions, and Layer 7 acceleration domains can be added later. Do you want to use no-domain access mode?"
   - If user confirms → Go to [B3: No Domain Access](#b3-no-domain-access)
   - If user declines → Prompt user to provide valid second-level domain

> **Domain Specifications**: Valid second-level domain (e.g., example.com), does not accept third-level and above domains (e.g., www.example.com) as site name.

### B1: Detect DNSPod Hosting Status

Before displaying access mode options to user, first try to detect if domain is hosted in DNSPod to prioritize recommending DNSPod hosting access mode.

**Steps:**

1. **Call DNSPod's DescribeDomain interface**, pass in the domain to onboard
   
2. **Determine if DNSPod hosting access conditions are met**:
   - Domain exists in DNSPod
   - `Status` field is `ENABLE` or `LOCK`
   - `DnsStatus` field is empty string (normal status)

3. **Exception Handling**:
   - If interface call fails (e.g., no permission, service unavailable), handle silently, don't display DNSPod hosting access option
   - If domain doesn't exist or status doesn't meet conditions, don't display DNSPod hosting access option

> **Note**: The `DescribeDomain` interface only returns errors for no permission or domain not found, won't return service authorization related error codes.

### B1.5: Domain Conflict Pre-check

Before formally creating site, perform pre-check to determine if domain has been accessed to avoid creation failure due to domain conflict.

**Steps:**

1. **Call CreateZone interface for pre-check**
   - Pass parameter `DryRun: true`
   - Pass domain to onboard `ZoneName`
   - Pass user-selected access mode `Type`

2. **Determine pre-check result**:

   **a) Pre-check succeeds** (no error returned)
   - Indicates domain hasn't been accessed, can directly create
   - Go to [B2: Confirm Access Mode and Parameters](#b2-confirm-access-mode-and-parameters)

   **b) Returns `ResourceInUse.Zone` error**
   - Indicates domain has been accessed via CNAME or DNSPod hosting
   - Prompt user: "This domain has been accessed, need to set Alias Zone Name to distinguish different sites"
   - Guide user to provide `AliasZoneName` (Alias Zone Name)
   - Go to [B2: Confirm Access Mode and Parameters](#b2-confirm-access-mode-and-parameters)

   **c) Returns `ResourceInUse.Others` or `ResourceInUse.OthersNS` error**
   - Indicates domain has been accessed via **NS access**
   - Prompt user: "This domain has been accessed via NS access. NS access sites can only be accessed once and cannot use other access modes. If you want to use other access modes, please delete the existing NS access site first."
   - **Terminate creation process**

> **Important Notes**:
> - NS access has exclusivity; a domain can only be accessed via NS once
> - Domains accessed via NS cannot use CNAME or DNSPod hosting access
> - Domains accessed via CNAME or DNSPod hosting cannot use NS access (but can continue using CNAME or DNSPod hosting to create sites with same name)

### B2: Confirm Access Mode and Parameters

**Call** `CreateZone`. User needs to provide:
- **Site Domain**: Root domain to onboard
- **Access Mode**: Display available options based on B1 detection results
  - If DNSPod hosting conditions are met: **Prioritize recommending** DNSPod hosting access (dnspod), also provide CNAME access (partial) and NS access (full) options
  - If conditions not met: Only provide CNAME access (partial) and NS access (full) options
- **Acceleration Area** (Area): Optional values are mainland (Mainland China), overseas (Global excluding Mainland China), global (Global)
  - **mainland (Mainland China)**: ⚠️ **Requires domain to have completed ICP filing with MIIT**
  - **global (Global)**: ⚠️ **Requires domain to have completed ICP filing with MIIT**
  - **overseas (Global excluding Mainland China)**: No filing requirement
- **Alias Zone Name** (AliasZoneName): **Only needed when B1.5 pre-check returns domain conflict**
  - Provided by user to distinguish sites with same name
  - Format requirements: combination of numbers, English letters, `.`, `-`, `_`, within 200 characters

> **Important Notes**:
> - When selecting `mainland` or `global` area, must remind user to confirm domain has completed ICP filing, otherwise site will not be able to onboard and use normally.
> - If B1.5 pre-check finds domain conflict, must require user to provide `AliasZoneName` parameter.

Suggest passing PlanId directly when creating.

> When not passing PlanId, site is in `init` status, need to bind later via BindZoneToPlan.
>
> **No Automatic Binding**: Whether passing PlanId via `CreateZone` or later calling `BindZoneToPlan`, **must** obtain user's explicit confirmation beforehand; never decide on your own which plan to bind.

#### Exception Handling: Service Authorization Missing

**Only when user selects DNSPod hosting access mode**, calling `CreateZone` may return error code `OperationDenied.DNSPodUnauthorizedRoleOperation`, indicating service authorization is missing.

**Handling Steps**:

1. **Automatically create service authorization**: Call CAM's `CreateServiceLinkedRole` interface
   - `QCSServiceName`: `["DnspodaccesEO.TEO.cloud.tencent.com"]`
   - `Description`: `"This role is a service-linked role for Tencent EdgeOne Platform (TEO). This role will query your domain status and related DNS records in DNSPod within the permission scope of associated policies, and help you quickly complete DNS modification to switch acceleration service to EO in one-click DNS modification scenarios"`

2. **Retry site creation**:
   - If service authorization creation succeeds, retry calling `CreateZone` to create site
   - If service authorization creation fails, enable fallback mode: prompt user to use NS access or CNAME access

### Next Step for DNSPod Hosting Access

> In DNSPod hosting access mode, EdgeOne will automatically complete ownership verification.

After site creation succeeds:
- Site will automatically complete ownership verification
- Can directly go to [Scenario D: Add Acceleration Domain](#scenario-d-add-acceleration-domain)

### Next Step for NS Access

Inform user that they need to modify DNS server to NameServers returned in response at domain registrar, then go to [Scenario C: Verify Ownership](#scenario-c-verify-ownership).

### Next Step for CNAME Access

Inform user of two validation methods (choose one), get validation info from response:

1. **DNS Validation**: Add TXT record in DNS
2. **File Validation**: Place validation file in origin root directory

After user confirms configuration complete, go to [Scenario C: Verify Ownership](#scenario-c-verify-ownership).

### B3: No Domain Access

**Applicable Scenarios**: User temporarily has no domain or only needs Layer 4 proxy and edge functions.

**Call** `CreateZone`, parameters as follows:
- `Type`: `noDomainAccess`
- `ZoneName`: **Keep as empty string**
- `Area`: **Keep as empty string**
- `PlanId`: Pass confirmed plan ID

> **Important Note**: In no-domain access mode, ZoneName and Area parameters must be kept empty, otherwise interface call will fail.

**After creation succeeds**:
- Site needs no ownership verification
- Can directly use Layer 4 proxy and edge functions
- Inform user: "Site created successfully, you can now configure Layer 4 proxy or edge functions. If you need Layer 7 acceleration features, you can add acceleration domains anytime."

**Follow-up Operations**:
- Configure Layer 4 proxy: Refer to Layer 4 proxy related documentation
- Configure edge functions: Refer to edge functions related documentation

## Scenario C: Verify Ownership

**Trigger**: User says "verify site", "check DNS switch", "ownership verification", or subsequent step after site creation.

> User can choose to skip ownership verification and directly go to [Scenario D: Add Acceleration Domain](#scenario-d-add-acceleration-domain), verify later.

### C1: Query Verification Status (DescribeIdentifications)

Before triggering verification, first call `DescribeIdentifications` to query current verification status.

**Decision**:
- If `Status` is `finished`, no need to verify again, go directly to next step
- If `Status` is `pending`, inform user to configure DNS TXT record or file validation based on validation info in response

### C2: Trigger Verification (VerifyOwnership)

After user confirms DNS / file configuration complete, call `VerifyOwnership`.

**NS Access Scenario**: Verify if DNS server switch succeeded. DNS switch usually takes 24-48 hours to take effect globally; if verification fails, suggest user retry later.

**CNAME Access Scenario**: Verify if TXT record or file is configured correctly. If site passes ownership verification, adding domains later won't need verification again.

## Scenario D: Add Acceleration Domain

**Trigger**: User says "add domain", "configure acceleration domain", "onboard subdomain", or subsequent step after ownership verification completion (or skip).

> **No-Domain Access Sites**: Sites created via no-domain access mode can also add Layer 7 acceleration domains anytime; after adding, can use complete Layer 7 acceleration features.

### D0: Determine Target Site

> If entering this scenario from a continuous flow of Scenario B/C, ZoneId is already known; you can skip this step and go directly to D1.

When user directly triggers "add domain", you need to first determine which site to add the domain to.

**Steps:**

1. **Extract root domain**: Extract the root domain (e.g., `example.com`) from the acceleration domain provided by user (e.g., `www.example.com`).

2. **Query matching sites**: Call `DescribeZones` with `zone-name` filter by root domain:
   ```
   --Filters '[{"Name":"zone-name","Values":["example.com"]}]'
   ```

3. **Filter and handle based on query results**:

   First, filter out sites with `Status == "initializing"` — these sites are still initializing and must not be displayed.

   Then handle the remaining sites:

   - **No matching site** (or all filtered out): Prompt user that the root domain has not been onboarded to EdgeOne, guide to [Scenario A: Confirm Plan](#scenario-a-confirm-plan) to begin full onboarding process.

   - **Only 1 site**: Display site info (ZoneId, alias, access mode, acceleration area, status) to user, proceed to D1 after confirmation.

   - **Multiple sites** (same root domain may have multiple sites): **Must** display all matching sites for user selection; never automatically select the first one or any arbitrary one. Display info should include:
     - **Site Alias** (AliasZoneName) — the most intuitive distinguishing identifier
     - **ZoneId**
     - **Access Mode** (Type: dnsPodAccess / partial / full)
     - **Acceleration Area** (Area: mainland / overseas / global)
     - **Status**: Determined using the [Site Status Determination Logic](#site-status-determination-logic)
     - Suggest prioritizing sites with `Active` status

   > **No Automatic Selection**: When multiple matching sites exist, **must** wait for user's explicit selection before continuing; never decide on your own.

### D1: Collect Parameters

Need to confirm following information with user before calling:

1. **Acceleration Domain** (DomainName): Subdomain to onboard, e.g., `www.example.com`
2. **IPv6 Access** (IPv6Status): Whether to enable IPv6 access, values:
   - `follow`: Follow site IPv6 configuration (default)
   - `on`: Enable
   - `off`: Disable
3. **Origin Configuration** (OriginInfo): See [OriginInfo Data Structure](#origininfo-data-structure) below
4. **Origin Protocol** (OriginProtocol, optional): FOLLOW (default) / HTTP / HTTPS
5. **Origin Port** (optional): HTTP origin port (default 80) / HTTPS origin port (default 443)

#### OriginInfo Data Structure

OriginInfo is a required parameter for `CreateAccelerationDomain`, defining origin information.

##### Required Fields

| Field | Type | Description |
|---|---|---|
| **OriginType** | string | Origin type, see values below |
| **Origin** | string | Origin address, fill in different values based on OriginType |

##### OriginType Values and Origin Mapping

| OriginType | Description | Origin Value |
|---|---|---|
| `IP_DOMAIN` | IPv4, IPv6, or domain type origin | IP address or domain, e.g., `1.1.1.1`, `origin.example.com` |
| `COS` | Tencent Cloud COS object storage origin | COS bucket access domain |
| `AWS_S3` | AWS S3 object storage origin | S3 bucket access domain |
| `ORIGIN_GROUP` | Origin group type origin | Origin group ID; if referencing another site's origin group, format: `{OriginGroupID}@{ZoneID}` |
| `VOD` | Cloud VOD | Cloud VOD application ID |
| `LB` | Load balancer (whitelist only) | Load balancer instance ID; if referencing another site's LB, format: `{LBID}@{ZoneID}` |
| `SPACE` | Origin offload (whitelist only) | Origin offload space ID |

##### Optional Fields

| Field | Type | Applicable Scenario | Description |
|---|---|---|---|
| **HostHeader** | string | Only when `OriginType = IP_DOMAIN` | Custom origin HOST header. **Do not pass this field** for other origin types, otherwise it will cause errors |
| **PrivateAccess** | string | Only when `OriginType = COS` or `AWS_S3` | Whether to use private authentication: `on` / `off` (default off) |
| **PrivateParameters** | list | Only when `PrivateAccess = on` | Private authentication parameter list |
| **BackupOrigin** | string | Only when `OriginType = ORIGIN_GROUP` | Backup origin group ID (legacy feature, not recommended) |
| **VodOriginScope** | string | Only when `OriginType = VOD` | Origin scope: `all` (default, all files in app) / `bucket` (specified bucket) |
| **VodBucketId** | string | Only when `OriginType = VOD` and `VodOriginScope = bucket` | VOD bucket ID |

##### Most Common Scenario Examples

**IP/Domain origin** (most common):
```json
{
  "OriginType": "IP_DOMAIN",
  "Origin": "1.1.1.1"
}
```

**COS origin (private access)**:
```json
{
  "OriginType": "COS",
  "Origin": "bucket-xxx.cos.ap-guangzhou.myqcloud.com",
  "PrivateAccess": "on",
  "PrivateParameters": [{"Name": "SecretId", "Value": "xxx"}, {"Name": "SecretKey", "Value": "xxx"}]
}
```

**Origin group**:
```json
{
  "OriginType": "ORIGIN_GROUP",
  "Origin": "og-testorigin"
}
```

### D2: Call CreateAccelerationDomain

> **No Automatic Addition**: Adding acceleration domain will change online DNS configuration. **Must** complete parameter collection in D1 and obtain user's explicit confirmation before execution; never decide on your own.

Call `CreateAccelerationDomain` after user confirmation.

**Next Step**: Inform user that they need to add CNAME record in DNS, pointing domain to EdgeOne-assigned CNAME address (can query `Cname` field via `DescribeAccelerationDomains`).

## Scenario E: Apply and Deploy HTTPS Certificate

**Trigger**: After domain addition complete, user says "configure HTTPS", "apply for certificate", or as final step of onboarding process.

> Complete certificate management (CNAME manual validation, deploy custom certificate, batch inspection, etc.) refer to [cert-manager.md](cert-manager.md).

### E1: NS Access / DNSPod Hosting Access (Automatic Validation, One-Step Complete)

> **Applicable Scenarios**: In NS access mode or DNSPod hosting access mode, EdgeOne can directly control DNS records, so can automatically complete certificate application and deployment.

> **No Automatic Deployment**: Deploying certificate will directly affect domain's HTTPS service. **Must** inform user which domains will deploy which certificates, and wait for explicit confirmation before calling `ModifyHostsCertificate`.

### E2: CNAME Access (Manual Validation)

CNAME access needs to first apply for certificate, complete domain validation, then deploy; process is longer. Please refer to [cert-manager.md Scenario B2](cert-manager.md#b2-cname-access-manual-validation) for complete steps.

## Scenario F: View Onboarding Status

**Trigger**: User says "check site status", "is domain onboarded".

Call `DescribeZones` to query target site status.

> **Important**: When displaying site status, must use the [Site Status Determination Logic](#site-status-determination-logic) to determine and display the effective status. Sites with `Status == "initializing"` must be filtered out and not displayed to users.

> Refer to [../api/zone-discovery.md](../api/zone-discovery.md) for more query methods.

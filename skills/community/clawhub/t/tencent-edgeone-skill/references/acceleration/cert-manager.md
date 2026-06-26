# Certificate Automation Management

Manage EdgeOne domain HTTPS certificates: query certificate status, apply for free certificates, deploy custom certificates.

## Scenario A: Query Certificate Status

**Trigger**: User wants to view certificate list or check expiration time.

### A1: Locate Target Site

Call `DescribeZones`, using `zone-name` filter to match the site name specified by the user.

> **Important**: Filter out sites with `Status` as `initializing` (these sites are still initializing and haven't completed creation).

Handle based on results in three cases:

**Case 1: Only 1 available site matched**

Directly use this site's `ZoneId`, proceed to A2.

**Case 2: Multiple sites with same name matched**

Display all **available** matching results to user, listing key information for distinction, **wait for user's explicit selection** before continuing:

```
Found multiple sites named "xxx.com", please confirm which one to query:

  1. ZoneId: zone-aaa  Alias: prod   Access Mode: NS Access   Created: 2024-01-01
  2. ZoneId: zone-bbb  Alias: test   Access Mode: CNAME Access  Created: 2025-06-01

Please reply with the number or ZoneId.
```

> After receiving user's response, use the selected `ZoneId` to proceed to A2.

**Case 3: No available sites**

Prompt user: "No available site 'xxx.com' found, please check the site name or wait for site initialization to complete."

### A2: Query Domain Certificate Information

Call `DescribeAccelerationDomains`, read certificate information for each domain from the `AccelerationDomains[].Certificate` field in the response.

> You can specify a domain to query via `Filters.domain-name`; not passing Filters returns all domains under the site.

Key fields in each domain's `Certificate` structure:

| Field | Meaning |
|---|---|
| `Certificate.Mode` | Certificate configuration mode: `disable` / `eofreecert` / `eofreecert_manual` / `sslcert` |
| `Certificate.List[].CertId` | Certificate ID |
| `Certificate.List[].Alias` | Certificate alias |
| `Certificate.List[].Type` | Certificate type: `default` / `upload` / `managed` |
| `Certificate.List[].ExpireTime` | Expiration time |
| `Certificate.List[].Status` | Deployment status: `deployed` / `processing` / `applying` / `failed` / `issued` |
| `Certificate.List[].SignAlgo` | Signature algorithm |

**Output suggestion**: Display certificate information for each domain in table format, marking entries that are about to expire (≤30 days) or have abnormal status (`failed` / `applying`).

## Scenario B: Apply and Deploy Free Certificate

**Trigger**: User says "apply for free certificate", "certificate is expiring soon", "renew certificate".

### B0: Locate Target Site

If user hasn't directly provided ZoneId, call `DescribeZones` using `zone-name` filter to match the site name specified by the user.

> **Important**: Filter out sites with `Status` as `initializing` (these sites are still initializing and haven't completed creation).

- **Only 1 available site matched**: Directly use this site's `ZoneId`, proceed to B1.
- **Multiple sites with same name matched**: Display all **available** matching results to user, **wait for explicit selection** before continuing (display format same as Scenario A).
- **No available sites**: Prompt user: "No available site 'xxx.com' found, please check the site name or wait for site initialization to complete."

### Access Mode Determination

The result of calling `DescribeZones` is also used to determine the access mode (`Type` field), taking different routes based on the result:

| Access Mode | Free Certificate Application Method |
|---|---|
| NS Access / DNSPod Hosting | **Automatic Validation** — Directly call ModifyHostsCertificate |
| CNAME Access | **Manual Validation** — Need to call ApplyFreeCertificate first, complete validation, then deploy |

### B1: NS Access / DNSPod Hosting (Automatic Validation)

Call `ModifyHostsCertificate`.

> **Confirmation Prompt**: Deploying certificate will affect the domain's HTTPS service, need user confirmation before execution.

### B2: CNAME Access (Manual Validation)

Requires 4 steps:

**Step 1**: Call `ApplyFreeCertificate` to initiate application.

**Step 2**: Based on validation information in response, inform user to complete configuration.

> After informing user, **wait for user to confirm configuration completion** before continuing to next step.

**Step 3**: Call `CheckFreeCertificateVerification` to check validation result

- Success: Response contains certificate information, indicating certificate has been issued
- Failure: Need to check if validation configuration is correct

**Step 4**: Call `ModifyHostsCertificate` to deploy free certificate.

> **Confirmation Prompt**: Deploying certificate will affect the domain's HTTPS service, need user confirmation before execution.

## Scenario C: Deploy Custom Certificate

**Trigger**: User says "configure custom certificate", "uploaded certificate", or provides CertId.

### C0: Locate Target Site

If user hasn't directly provided ZoneId, call `DescribeZones` using `zone-name` filter to match the site name specified by the user.

> **Important**: Filter out sites with `Status` as `initializing` (these sites are still initializing and haven't completed creation).

- **Only 1 available site matched**: Directly use this site's `ZoneId`, proceed to next step.
- **Multiple sites with same name matched**: Display all **available** matching results to user, **wait for explicit selection** before continuing (display format same as Scenario A).
- **No available sites**: Prompt user: "No available site 'xxx.com' found, please check the site name or wait for site initialization to complete."

### C1: Query SSL Certificates Applicable to Target Domain

If user hasn't provided CertId, or wants to select from existing certificates, call `ssl:DescribeCertificates` to query certificate list, then filter out certificates applicable to the target domain.

**Call Parameter Suggestions**:
- `SearchKey`: Pass in target domain (e.g., `a-1.qcdntest.com`), can fuzzy match domain field to narrow return range
- `CertificateType`: Pass `SVR`, only query server certificates (exclude client CA certificates)
- `Limit`: Suggest passing `1000` to ensure no omissions

**Filter Rules**: For each returned certificate, check if any entry in the `SubjectAltName` list matches the target domain:

| Match Type | Description | Example |
|---|---|---|
| Exact Match | `SubjectAltName` has an entry exactly the same as target domain | `a-1.qcdntest.com` |
| Wildcard Match | `SubjectAltName` has a `*.xxx` entry, and target domain is its direct subdomain (only one level) | `*.qcdntest.com` matches `a-1.qcdntest.com` |

**Availability Determination**: After filtering matching certificates, mark availability status for each certificate based on the following fields:

| Field | Meaning | Availability Condition |
|---|---|---|
| `Status` | Certificate status | Must be `1` (Approved) |
| `CertEndTime` | Expiration time | Days until today > 0 (Not expired) |
| `Deployable` | Whether deployable | Must be `true` |

**Output suggestion**: Display all matching certificates in a table, marking availability:

```
Certificates applicable to a-1.qcdntest.com:

Cert ID      Alias          Expiration           Days Left  Status     Deployable  Availability
------------ -------------- -------------------- ---------- ---------- ----------- ------------
zVq87w0D     my-cert        2032-09-23 05:10:56  2371 days  Approved   ✅          ✅ Available
QxbtGBIM     old-cert       2025-01-01 00:00:00  -86 days   Expired    ❌          ❌ Expired
```

If no matching certificate is found, inform user that they need to first go to [SSL Certificate Console](https://console.cloud.tencent.com/ssl) to upload or apply for a certificate covering this domain.

### C2: Deploy Certificate

After user selects certificate from C1 results, call `ModifyHostsCertificate` (`Mode=sslcert`, `ServerCertInfo[{CertId}]`).

> **No Automatic Deployment**: **Must** confirm deployment domain and certificate ID with user before execution.

## Scenario D: Batch Certificate Inspection

**Trigger**: User says "check certificates for all domains", "which certificates are expiring soon".

### Process

1. Call `DescribeZones` to get all sites
   - **Important**: Filter out sites with `Status` as `initializing` (these sites are still initializing and haven't completed creation)
   - **Critical**: **Must use pagination** to retrieve all sites:
     - Set `Limit=100` (maximum value)
     - Set `Offset=0` initially, increment by 100 each iteration
     - Loop until `Offset + Limit >= TotalCount`
     - Merge all paginated results
   - Refer to [zone-discovery.md](../api/zone-discovery.md) for detailed pagination implementation
2. Call `DescribeAccelerationDomains` for each **available** site, read certificate information from each `AccelerationDomains[].Certificate` field in the response
3. Summarize output, marking the following anomalies:
   - Certificates with `Certificate.List[].Status` as `failed` or `applying`
   - Certificates with `Certificate.List[].ExpireTime` ≤30 days from today
   - Domains with `Certificate.Mode` as `disable` or `Certificate` is null (no certificate configured)

### Output Format Suggestion

```markdown
## Certificate Inspection Report

| Site | Domain | Cert ID | Expiration | Days Left | Status |
|---|---|---|---|---|---|
| example.com | *.example.com | teo-xxx | 2026-04-15 | 29 days | Expiring Soon |
| example.com | api.example.com | teo-yyy | 2026-09-01 | 168 days | Normal |
```

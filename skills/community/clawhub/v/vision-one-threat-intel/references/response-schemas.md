# Response Schemas (Verified Against Live API)

## STIX Bundle Response (feedIndicators, feeds)

Both `/feedIndicators` and `/feeds` return STIX 2.1 bundles:

```json
{
  "bundle": {
    "type": "bundle",
    "id": "bundle--uuid",
    "objects": [ ... ]
  },
  "nextLink": "https://api.xdr.trendmicro.com/v3.0/threatintel/...?skipToken=...",
  "reportUpdatedDateTime": "2026-03-12T00:00:00Z"
}
```

- `bundle.objects` — Array of STIX 2.1 objects (indicators or reports)
- `nextLink` — Full URL for next page (absent when no more pages)
  - Includes required params: `startDateTime`, `endDateTime`, `topReport`, `responseObjectFormat`, `skipToken`
  - Must use ALL params from nextLink when paginating (not just skipToken)

## STIX 2.1 Indicator Object (from feedIndicators)

```json
{
  "type": "indicator",
  "spec_version": "2.1",
  "id": "indicator--0bef86fb-ba93-44d5-a29e-8dfb54f888ec",
  "created": "2020-06-25T12:17:42.000Z",
  "modified": "2020-06-25T12:17:42.000Z",
  "pattern": "[domain-name:value = 'evil.com']",
  "pattern_type": "stix",
  "valid_from": "2020-06-25T12:17:42Z",
  "valid_until": "2021-06-25T12:17:42Z",
  "kill_chain_phases": [
    {
      "kill_chain_name": "misp-category",
      "phase_name": "Payload installation"
    }
  ]
}
```

### Common STIX Pattern Types

| Observable | Pattern Example |
|-----------|----------------|
| Domain | `[domain-name:value = 'evil.com']` |
| IP | `[ipv4-addr:value = '1.2.3.4']` |
| URL | `[url:value = 'https://evil.com/payload']` |
| File name | `[file:name = 'malware.exe']` |
| File hash | `[file:hashes.'SHA-256' = 'abc123...']` |
| Network | `[network-traffic:dst_ref.type = 'domain-name' AND ...]` |
| Email | `[email-addr:value = 'attacker@evil.com']` |

### Kill Chain Phase Names

- Payload installation
- Network activity
- Persistence mechanism
- External analysis

## STIX 2.1 Report Object (from feeds)

```json
{
  "type": "report",
  "spec_version": "2.1",
  "id": "report--0ea4ba42-7904-4f32-b487-c44f5ed41e8c",
  "created": "2020-09-25T03:14:02.890Z",
  "modified": "2020-09-25T03:14:02.890Z",
  "name": "Cybercriminals Distribute Backdoor With VPN Installer",
  "published": "2020-09-25T03:14:02.89Z",
  "object_refs": [
    "indicator--81b1ca17-...",
    "indicator--b55fa240-..."
  ],
  "report_types": ["threat-report"],
  "created_by_ref": "identity--74f7eb0f-...",
  "object_marking_refs": ["marking-definition--..."]
}
```

## Suspicious Object (from suspiciousObjects — standard JSON)

```json
{
  "fileSha256": "C5DE4B9E5C8390CA1841D9B21D51A9055016346228ACB8BAF43AB90376F7B0A8",
  "type": "fileSha256",
  "scanAction": "log",
  "riskLevel": "high",
  "inExceptionList": false,
  "lastModifiedDateTime": "2026-04-09T17:57:24Z",
  "expiredDateTime": "2026-05-10T00:00:00Z"
}
```

**Note:** The value field name matches the `type` field (e.g., `fileSha256`, `fileSha1`, `domain`, `ip`, `url`, `senderMailAddress`).

Uses standard `items[]` pagination wrapper:
```json
{
  "items": [ ... ],
  "nextLink": "https://...?skipToken=..."
}
```

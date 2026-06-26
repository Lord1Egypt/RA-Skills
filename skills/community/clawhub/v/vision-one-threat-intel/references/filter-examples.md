# OData Filter Examples for Vision One Threat Intelligence

## Feed Indicators Filters

### By Risk Level
```
filter=riskLevel eq 'high'
filter=riskLevel eq 'medium'
```

### By Indicator Type
```
filter=objectType eq 'ip'
filter=objectType eq 'domain'
filter=objectType eq 'fileSha256'
```

### Combined Filters
```
filter=riskLevel eq 'high' and objectType eq 'ip'
filter=riskLevel eq 'high' and objectType eq 'domain'
```

### By Threat Context
```
filter=campaigns contains 'APT29'
filter=threatActors contains 'Lazarus'
filter=targetedIndustries contains 'Finance'
filter=targetedCountries contains 'United States'
filter=cves contains 'CVE-2024-3400'
```

### Combined Hunt Filters
```
filter=targetedIndustries contains 'Finance' and riskLevel eq 'high'
filter=threatActors contains 'APT41' and targetedCountries contains 'Japan'
filter=campaigns contains 'ransomware' and objectType eq 'domain'
```

## Intelligence Reports Filters

### By Name/Keyword
```
filter=name contains 'ransomware'
filter=name contains 'APT29'
```

### By ID
```
filter=id eq 'RPT-12345'
```

## Feeds Filters

### By Geographic Location
```
filter=location eq 'Brazil'
filter=location eq 'United States'
```

### By Industry
```
filter=industry eq 'Finance'
filter=industry eq 'Technology'
```

## Operator Reference

| Operator | Description | Example |
|----------|-------------|---------|
| eq | Equals | `riskLevel eq 'high'` |
| and | Logical AND | `a eq 'x' and b eq 'y'` |
| or | Logical OR | `a eq 'x' or a eq 'y'` |
| not | Logical NOT | `not riskLevel eq 'low'` |
| in | In set | `objectType in ('ip','domain')` |
| contains | Contains substring | `campaigns contains 'APT29'` |
| startswith | Starts with | `name startswith 'APT'` |
| gt | Greater than | `validFrom gt '2025-01-01'` |
| ge | Greater or equal | `validFrom ge '2025-01-01'` |
| lt | Less than | `validUntil lt '2025-06-01'` |
| le | Less or equal | `validUntil le '2025-06-01'` |

## Notes

- String values must be wrapped in single quotes
- Multiple conditions combine with `and` or `or`
- Use parentheses for grouping: `(a eq 'x' or a eq 'y') and b eq 'z'`
- Not all fields may support all operators — the API may return 400 for unsupported combinations
- When server-side filtering fails, the CLI falls back to client-side filtering

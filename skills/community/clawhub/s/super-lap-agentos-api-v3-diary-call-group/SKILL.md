---
name: lap-agentos-api-v3-diary-call-group
description: "Leverage the agentOS API V3 Diary Call Group skill to efficiently manage diary call groups. This comprehensive skill provides access to all 13 endpoints of the Diary Call Group API, enabling seamless integration and automation of diary management tasks. Ideal for handling scheduling, grouping, and tracking calls within agentOS. Boost your workflow reliability and speed with this specialized API skill. ##ife integration ae scheduling method ama summarydr developmental arbitrary ruby contamination uganda azure request christophe curry present acknowledges through gardeningijra waltz argued evaluating ruby encryption cite developmental"
version: 1.0.0
generator: lapsh
metadata:
  openclaw:
    requires:
      env:
        - AGENTOS_API_V3_DIARY_CALL_GROUP_API_KEY
---

# agentOS API V3, Diary Call Group
API version: v3-diary

## Auth
basic | ApiKey ApiKey in header

## Base URL
https://live-api.letmc.com

## Setup
1. Set your API key in the appropriate header
2. GET /v3/diary/{shortname}/{branchID}/guest/search -- verify access
3. POST /v3/diary/{shortName}/appointment -- create first appointment

## Endpoints

13 endpoints across 1 groups. See references/api-spec.lap for full details.

### diary
| Method | Path | Description |
|--------|------|-------------|
| GET | /v3/diary/{shortname}/{branchID}/guest/search | Match Guest Parameters with existing applicants |
| GET | /v3/diary/{shortName}/allocations | Get a list of all available allocations for a date + 7 days for a specified appointment type |
| GET | /v3/diary/{shortName}/appointment | Get an appointment by ID |
| PUT | /v3/diary/{shortName}/appointment | Update an existing appointment using its unique identifier |
| POST | /v3/diary/{shortName}/appointment | Post an appointment into a valid diary allocation |
| DELETE | /v3/diary/{shortName}/appointment | Delete an existing appointment using its unique identifier |
| PATCH | /v3/diary/{shortName}/appointment/{appointmentID}/cancel | Cancel an existing appointment using its unique identifier |
| POST | /v3/diary/{shortName}/appointment/feedback | Submit appointment feedback |
| GET | /v3/diary/{shortName}/appointmentsbetweendates | A collection of diary appointments linked to a company filtered between specific dates and by appointment type |
| GET | /v3/diary/{shortName}/appointmenttypes | A collection of all diary appointment types |
| GET | /v3/diary/{shortName}/company/branches | All branches defined for a company |
| GET | /v3/diary/{shortName}/company/branches/{branchID} | Get a specific branch given its unique Object ID (OID) |
| GET | /v3/diary/{shortName}/recurringappointment | Retrieves all recurring appointments:- |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all search?" -> GET /v3/diary/{shortname}/{branchID}/guest/search
- "List all allocations?" -> GET /v3/diary/{shortName}/allocations
- "List all appointment?" -> GET /v3/diary/{shortName}/appointment
- "Create a appointment?" -> POST /v3/diary/{shortName}/appointment
- "Create a feedback?" -> POST /v3/diary/{shortName}/appointment/feedback
- "List all appointmentsbetweendates?" -> GET /v3/diary/{shortName}/appointmentsbetweendates
- "List all appointmenttypes?" -> GET /v3/diary/{shortName}/appointmenttypes
- "List all branches?" -> GET /v3/diary/{shortName}/company/branches
- "Get branche details?" -> GET /v3/diary/{shortName}/company/branches/{branchID}
- "List all recurringappointment?" -> GET /v3/diary/{shortName}/recurringappointment
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## CLI

```bash
# Update this spec to the latest version
npx @lap-platform/lapsh get agentos-api-v3-diary-call-group -o references/api-spec.lap

# Search for related APIs
npx @lap-platform/lapsh search agentos-api-v3-diary-call-group
```

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)

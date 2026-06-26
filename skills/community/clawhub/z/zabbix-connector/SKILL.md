---
name: zabbix
description: Skill for Zabbix API monitoring and interaction. Use it to check active alerts, list problems, manage hosts, and query monitoring data.
metadata:
  {
    "openclaw": {
      "os": ["linux", "darwin"],
      "requires": {
        "bins": ["python3"]
      }
    }
  }
---

# Zabbix Skill

Use this skill to monitor systems, query alerts, and access historical metrics through the Zabbix API.

## Scope

This skill is meant for:
- Querying active alerts and problems from hosts.
- Listing hosts, items, and groups.
- Accessing historical metrics and graphs.
- Acknowledging events and problems.

Do not use this skill for:
- Modifying critical Zabbix server settings without authorization.
- Exposing credentials or authentication tokens.

## Recommended Flow

1. Identify the target (host or item) of the request.
2. Use the bundled scripts to query the API.
3. Format the problem report as requested.
4. Provide reference links for events.

## Security Rules

- **Never share** the `.env` file containing `ZABBIX_URL` and `ZABBIX_TOKEN`.
- To configure the skill, copy `.env.template` to `.env` and fill in the credentials.
- Prefer read (GET) operations over mutations (POST/PUT).
- Confirm the target host before acknowledging events.
- The `.env` file with real credentials **must not be included in the release package**.

## Bundled Resources

### `scripts/zabbix_api.py`
Central script for Zabbix API communication. It provides methods for `host_get`, `problem_get`, `history_get`, among others.

Internal usage example:
```python
zb = ZabbixDirect(ZABBIX_URL, ZABBIX_TOKEN)
problems = zb.get_active_problems_report()
```

## Example Requests That Should Trigger This Skill

- "What are the active alerts on Zabbix?"
- "Show me the last 7 days' graph for PETR4 on the Tracker server."
- "Acknowledge event X on Zabbix."

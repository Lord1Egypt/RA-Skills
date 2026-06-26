# Real-time Alerts in Timeplus

Alerts in Timeplus are built on top of **Streaming SQL**. They allow you to monitor data streams continuously and trigger actions when specific conditions are met.

## How Alerts Work
An alert consists of:
1. **The Query**: A streaming SQL query that returns rows when a condition is met.
2. **The Condition**: The logic that triggers the alert (e.g., `temperature > 100`).
3. **The Sink/Action**: Where to send the notification (Slack, Webhook, Email, etc.).

## Creating an Alert via SQL

### Basic Syntax
```sql
CREATE ALERT [IF NOT EXISTS] <db.alert_name>
BATCH <N> EVENTS WITH TIMEOUT <interval>
LIMIT <M> ALERTS PER <interval>
CALL <python_udf_name>
AS <streaming_select_query>;
```

### Examples

Send notifications to Slack when there are new stars for Timeplus Proton.

```sql
CREATE FUNCTION send_star_events_to_slack(actor string) 
RETURNS string 
LANGUAGE PYTHON AS $$
import json
import requests

def send_star_events_to_slack(value):
    for github_id in value:
        requests.post(
            "https://hooks.slack.com/services/T123/B456/other_id",
            data=json.dumps({
                "text": f"New 🌟 for Timeplus Proton from https://github.com/{github_id}"
            })
        )
    return value
$$

CREATE ALERT default.watch_event_alert
BATCH 10 EVENTS WITH TIMEOUT 5s
LIMIT 1 ALERTS PER 15s
CALL send_star_events_to_slack
AS 
SELECT actor 
FROM github_events 
WHERE repo = 'timeplus-io/proton' AND type = 'WatchEvent';
```

## Alert Management

| Action | SQL Command |
| --- | --- |
| **List Alerts** | `SHOW ALERTS` |
| **View Definition** | `SHOW CREATE ALERT alert_name` |
| **Remove Alert** | `DROP ALERT alert_name` |

## Best Practices
- **Avoid Noise**: Use `HAVING` clauses or `windowing` functions to prevent an alert from firing every millisecond.
- **Deduplication**: Use `LAG` or stateful functions if you only want to be alerted when a status *changes* from 'OK' to 'FAIL'.
- **Security**: When using Webhook sinks, store authentication tokens in environment variables (`${WEBHOOK_TOKEN}`) rather than plain text in the SQL definition.

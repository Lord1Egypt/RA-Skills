# AWS Events Reference

Event queries for problem timeline analysis. Use these during incident investigation to determine what changed before or during a problem on an AWS resource.

## Placeholder Reference

| Placeholder | Description |
|---|---|
| `<PROBLEM_START>` | Problem start timestamp (e.g., `now()-2h`) |
| `<PROBLEM_END>` | Problem end timestamp (e.g., `now()`) |
| `<ROOT_CAUSE_ENTITY_ID>` | Dynatrace entity ID of the affected resource (e.g., `AWS_EC2_INSTANCE-ABC123`) |
| `<AWS_INSTANCE_ID>` | AWS resource ID of the affected resource (e.g., `i-0abc1234def56789`) |
| `<AWS_RESOURCE_NAME>` | AWS resource name or logical resource ID (e.g., `my-web-server-asg`) |
| `<CLOUD_ALERT_EVENT_TYPE>` | Davis event type to filter (e.g., `RESOURCE_CONTENTION_EVENT`, `AVAILABILITY_EVENT`) |

---

## Auto Scaling Events

List recent Auto Scaling activity. Run this first during any EC2 instance problem to detect scale-in/scale-out events, lifecycle hooks, or capacity changes that may have caused or contributed to the issue.

```dql
fetch events
| filter source == "aws.autoscaling"
| fields timestamp, event.type, event.name, data
| sort timestamp desc
| limit 50
```

**Note:** This query returns the most recent 50 events globally. For incident-scoped analysis, add a time range:

```dql-template
fetch events, from: <PROBLEM_START>, to: <PROBLEM_END>
| filter source == "aws.autoscaling"
| fields timestamp, event.type, event.name, data
| sort timestamp desc
```

---

## AWS Health Events

Query for AWS Health service events affecting the specific resource. AWS Health events indicate service disruptions, scheduled maintenance, or account-level notifications from AWS.

```dql-template
fetch events, from: <PROBLEM_START - 1h>, to: <PROBLEM_END + 1h>
| filter source == "aws.health"
| filter dt.smartscape_source.id == toSmartscapeId("<ROOT_CAUSE_ENTITY_ID>")
| fieldsAdd event.description = jsonData[`eventDescription`][0][`latestDescription`]
| fieldsAdd event.name = jsonData[`eventTypeCode`]
| fieldsAdd event.category = jsonData[actionability]
| fieldsAdd affected_entity_ids = dt.smartscape_source.id
| fields timestamp, event.name, event.description, event.category, affected_entity_ids
| sort timestamp desc
```

**What to look for:**

- `event.category != "INFORMATIONAL"` — active service disruption from AWS or planned maintenance that may be impacting your resource

---

## CloudFormation Events

Check for recent CloudFormation stack deployments or changes. Infrastructure changes via CloudFormation are a common cause of problems — correlate stack events with the problem timeline.

```dql-template
fetch events, from: <PROBLEM_START - 1h>, to: <PROBLEM_END + 1h>
| filter source == "aws.cloudformation"
| parse data, "JSON:jsonData"
| fieldsAdd event.name = jsonData[eventName]
| fieldsAdd event.errorCode = jsonData[errorCode]
| fieldsAdd event.errorMessage = jsonData[errorMessage]
| fieldsAdd event.status = jsonData[`status-details`][status]
| fields jsonData, event.name, event.errorCode, event.status
| limit 20
```

Check for CloudFormation events related to the specific resource:

```dql-template
fetch events
| filter source == "aws.cloudformation"
| parse data, "JSON:jsonData"
| fieldsAdd event.name = jsonData[eventName]
| fieldsAdd event.errorCode = jsonData[errorCode]
| fieldsAdd event.errorMessage = jsonData[errorMessage]
| fieldsAdd event.status = jsonData[`status-details`][status]
| filter jsonData[`logical-resource-id`] == "<AWS_RESOURCE_NAME>"
| fields jsonData, event.name, event.errorCode, event.status, id, data
| limit 20
```

**What to look for:**

- Stack updates that completed shortly before the problem started
- Failed stack operations that may have left resources in a degraded state
- Resource replacements (e.g., instance replaced due to a launch template change)

---

## CloudTrail API Events

Query AWS CloudTrail events to audit API calls. Use this during security investigations or to correlate infrastructure changes with problems.

```dql
fetch events
| filter event.type == "AWS API Call via CloudTrail"
| fields timestamp, event.type, data
| sort timestamp desc
| limit 50
```

Scope to a problem time window for incident analysis:

```dql-template
fetch events, from: <PROBLEM_START - 1h>, to: <PROBLEM_END + 1h>
| filter event.type == "AWS API Call via CloudTrail"
| fields timestamp, event.type, data
| sort timestamp desc
```

**What to look for:**

- API calls that modify infrastructure (RunInstances, TerminateInstances, ModifyDBInstance, etc.)
- API calls from unexpected IAM users or roles
- Failed API calls (error codes) that might indicate permission issues

---

## EC2 Instance State Changes

Track EC2 instance launches and terminations. These events correlate with Auto Scaling activity, spot instance interruptions, or manual instance management.

```dql
fetch events
| filter event.type == "EC2 Instance Launch Successful"
    or event.type == "EC2 Instance Terminate Successful"
| fields timestamp, event.type, data
| sort timestamp desc
| limit 50
```

Scope to a problem time window:

```dql-template
fetch events, from: <PROBLEM_START - 1h>, to: <PROBLEM_END + 1h>
| filter event.type == "EC2 Instance Launch Successful"
    or event.type == "EC2 Instance Terminate Successful"
| fields timestamp, event.type, data
| sort timestamp desc
```

**What to look for:**

- Instance terminations shortly before a problem (capacity reduction)
- Rapid launch/terminate cycles (instance instability)
- Launches in unexpected regions or availability zones

---

## Cloud Alert Events (Davis)

Davis automatically detects anomalies on AWS resources monitored through the cloud integration. These events cover resource contention, availability issues, performance degradation, and errors.

```dql
fetch events
| filter event.provider == "CLOUD_ALERT" and event.kind == "DAVIS_EVENT"
| fields timestamp, event.type, event.name, dt.smartscape_source.id, aws.resource.name, data
| sort timestamp desc
| limit 50
```

Filter by a specific event type:

```dql-template
fetch events
| filter event.provider == "CLOUD_ALERT" and event.kind == "DAVIS_EVENT"
| filter event.type == "<CLOUD_ALERT_EVENT_TYPE>"
| fields timestamp, event.type, event.name, dt.smartscape_source.id, aws.resource.name, data
| sort timestamp desc
| limit 50
```

Scope to a specific affected entity:

```dql-template
fetch events, from: <PROBLEM_START - 1h>, to: <PROBLEM_END + 1h>
| filter event.provider == "CLOUD_ALERT" and event.kind == "DAVIS_EVENT"
| filter dt.smartscape_source.id == toSmartscapeId("<ROOT_CAUSE_ENTITY_ID>")
| fields timestamp, event.type, event.name, data
| sort timestamp desc
```

**What to look for:**

- RESOURCE_CONTENTION_EVENT — CPU, memory, or I/O saturation
- AVAILABILITY_EVENT — service or resource unreachable
- PERFORMANCE_EVENT — latency or throughput degradation
- ERROR_EVENT — error rate anomalies

---

## Event Discovery

Use this query to discover all available event sources and types in your environment. This helps identify which AWS services are forwarding events to Dynatrace.

```dql
fetch events, from:-30d
| summarize count = count(), by: {event.kind, event.type, event.provider}
| sort count desc
| limit 50
```

**What to look for:**

- New event sources that have started reporting recently
- Event types with high volume that may indicate recurring issues
- Missing event sources that should be configured but are not present

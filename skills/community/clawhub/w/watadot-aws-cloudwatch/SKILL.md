---
name: watadot-aws-cloudwatch
description: Observability and monitoring by Watadot Studio. Log tailing and metric extraction.
metadata:
  openclaw:
    emoji: 📈
    requires:
      anyBins: [aws]
---

# AWS CloudWatch Skills

Observability and automated monitoring patterns.

## 🚀 Core Commands

### Log Insights
```bash
# Live tail of a Log Group
aws logs tail /aws/lambda/<function-name> --follow

# Query logs for errors (last 1h)
aws logs filter-log-events --log-group-name <name> --filter-pattern "ERROR" --start-time $(date -d '1 hour ago' +%s000) --query "events[].message"
```

### Metrics & Alarms
```bash
# List active alarms with state
aws cloudwatch describe-alarms --query "MetricAlarms[?StateValue==\`ALARM\`].{Name:AlarmName,Reason:StateReason}" --output table

# Get CPU utilization metric for EC2
aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization --dimensions Name=InstanceId,Value=<id> --period 3600 --statistics Average --start-time 2026-03-15T00:00:00 --end-time 2026-03-16T00:00:00
```

### Dashboard Orchestration
```bash
# List dashboard names
aws cloudwatch list-dashboards --query "DashboardEntries[].DashboardName"
```

## 🧠 Best Practices
1. **Retention Policies**: Don't keep logs forever. Set retention (e.g., 14 days) to save storage costs.
2. **Log Streams**: Use unique log stream names for different agent instances to avoid interleaving.
3. **Structured Logging**: Log in JSON format to make filtering and automated analysis via OpenClaw easier.
4. **Alarms**: Set up billing alarms to catch sudden spikes in AWS usage early.

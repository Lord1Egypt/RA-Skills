# Runbook: [Service/Component Name] — [Issue Type]

**Severity:** P1 / P2 / P3
**On-call team:** [Team name]
**Last updated:** YYYY-MM-DD
**Author:** [Name]

---

## Symptoms

<!-- How do you know this issue is happening? List observable symptoms. -->

- [ ] Alert: [Alert name and link to monitoring dashboard]
- [ ] Error in logs: `[exact error message or pattern]`
- [ ] User reports: [Description of user-facing impact]
- [ ] Metric anomaly: [Which metric, what threshold]

## Impact

<!-- Who and what is affected? -->

| Aspect | Impact |
|--------|--------|
| Users affected | [All / subset / internal only] |
| Functionality | [What doesn't work] |
| Data at risk | [Yes/No — describe if yes] |
| Revenue impact | [Estimated if applicable] |

## Prerequisites

<!-- What access/tools do you need before starting? -->

- SSH access to production servers
- Database read access (`psql` or admin panel)
- Access to [monitoring tool] dashboard
- VPN connected (if required)

## Diagnosis

### Step 1: Confirm the issue

```bash
# Check service health
curl -s https://api.example.com/health | jq .

# Check logs for errors (last 15 minutes)
journalctl -u my-service --since "15 min ago" | grep -i error | tail -20

# Check metrics dashboard
# [Link to Grafana/Datadog dashboard]
```

### Step 2: Identify the scope

```bash
# How many users are affected?
# [Query or command to determine scope]

# Is it a single instance or all instances?
# [Check load balancer, check multiple pods/servers]
```

### Step 3: Determine root cause

```bash
# Check common causes:

# 1. Database connectivity
psql -h db.example.com -U readonly -c "SELECT 1;"

# 2. External service dependency
curl -v https://external-api.example.com/status

# 3. Resource exhaustion
df -h                    # Disk space
free -m                  # Memory
cat /proc/loadavg        # CPU load
```

## Remediation

### Immediate (stop the bleeding)

```bash
# Option A: Restart the service
sudo systemctl restart my-service

# Option B: Scale up (if capacity issue)
kubectl scale deployment my-app --replicas=5

# Option C: Failover to backup
# [Specific failover commands]

# Option D: Enable maintenance mode
curl -X POST https://admin.example.com/maintenance/enable
```

### Short-term (prevent recurrence in the next hours)

1. [Specific action]
2. [Specific action]
3. Monitor for 30 minutes to confirm stability

### Long-term (root cause fix)

1. [File ticket: description of permanent fix]
2. [Schedule follow-up review]
3. [Update monitoring/alerting if gaps found]

## Rollback

<!-- If a deployment caused the issue -->

```bash
# Rollback to previous version
kubectl rollout undo deployment/my-app

# Or deploy specific version
kubectl set image deployment/my-app my-app=registry.example.com/my-app:v1.2.3

# Verify rollback
kubectl rollout status deployment/my-app
```

## Escalation

| Time elapsed | Action |
|-------------|--------|
| 0 min | On-call engineer begins investigation |
| 15 min | If not diagnosed, page secondary on-call |
| 30 min | If not resolved, escalate to team lead |
| 60 min | If not resolved, escalate to engineering manager |
| 2 hours | Consider executive communication if user-facing |

**Contacts:**
- Primary on-call: [Rotation schedule link]
- Secondary: @[team-lead]
- Database team: @[db-oncall]
- Infrastructure: @[infra-oncall]

## Communication

### Internal

- Post in `#incidents` Slack channel with initial assessment
- Update every 15 minutes until resolved
- Post resolution summary when complete

### External (if user-facing)

- Update status page: [statuspage.example.com]
- Template: "We are aware of issues with [feature] and are working to resolve them. We will provide an update within [time]."

## Post-Incident

- [ ] Write post-mortem within 48 hours
- [ ] Conduct blameless review meeting
- [ ] File action item tickets
- [ ] Update this runbook with lessons learned
- [ ] Update monitoring and alerts if gaps found

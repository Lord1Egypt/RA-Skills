# Lighthouse Firewall Management

## Query Firewall Rules

```bash
tccli lighthouse DescribeFirewallRules --region ap-guangzhou \
  --InstanceId lhins-xxxxxxxx
```

## Add Firewall Rules

```bash
tccli lighthouse CreateFirewallRules --region ap-guangzhou \
  --InstanceId lhins-xxxxxxxx \
  --FirewallRules '[{"Protocol":"TCP","Port":"8080","CidrBlock":"0.0.0.0/0","Action":"ACCEPT","FirewallRuleDescription":"Open port 8080"}]'
```

### FirewallRule Fields

| Field | Required | Description |
|-------|----------|-------------|
| Protocol | Yes | TCP, UDP, ICMP, ALL |
| Port | Yes | Single port (80), range (8000-9000), or ALL |
| CidrBlock | No | Source IP CIDR, default 0.0.0.0/0 |
| Action | Yes | ACCEPT or DROP |
| FirewallRuleDescription | No | Rule description |

### Common Port Presets

```bash
# HTTP
--FirewallRules '[{"Protocol":"TCP","Port":"80","CidrBlock":"0.0.0.0/0","Action":"ACCEPT","FirewallRuleDescription":"HTTP"}]'

# HTTPS
--FirewallRules '[{"Protocol":"TCP","Port":"443","CidrBlock":"0.0.0.0/0","Action":"ACCEPT","FirewallRuleDescription":"HTTPS"}]'

# SSH (restrict source IP for security)
--FirewallRules '[{"Protocol":"TCP","Port":"22","CidrBlock":"1.2.3.4/32","Action":"ACCEPT","FirewallRuleDescription":"SSH from trusted IP"}]'
```

## Delete Firewall Rules

```bash
tccli lighthouse DeleteFirewallRules --region ap-guangzhou \
  --InstanceId lhins-xxxxxxxx \
  --FirewallRules '[{"Protocol":"TCP","Port":"8080"}]'
```

## Security Best Practices

- Restrict SSH (port 22) to specific trusted IPs, never open to 0.0.0.0/0
- Only open ports that are actually needed
- Always review existing rules before adding new ones
- Firewall changes take effect immediately — confirm with user before executing
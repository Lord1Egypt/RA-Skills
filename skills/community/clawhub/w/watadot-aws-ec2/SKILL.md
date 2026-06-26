---
name: watadot-aws-ec2
description: Elastic compute management by Watadot Studio. Deployment, scaling, and state monitoring.
metadata:
  openclaw:
    emoji: 💻
    requires:
      anyBins: [aws]
---

# AWS EC2 Skills

Management and orchestration patterns for Elastic Compute Cloud.

## 🚀 Core Commands

### Instance Discovery
```bash
# List running instances with Name and Public IP
aws ec2 describe-instances --filters "Name=instance-state-name,Values=running" --query "Reservations[].Instances[].{Name:Tags[?Key==\`Name\`].Value | [0], IP:PublicIpAddress, ID:InstanceId}" --output table

# Find expensive instances (G or P family)
aws ec2 describe-instances --query "Reservations[].Instances[?contains(InstanceType, 'g') || contains(InstanceType, 'p')].[InstanceId, InstanceType]"
```

### Lifecycle Control
```bash
# Start/Stop instances by ID
aws ec2 start-instances --instance-ids <id1> <id2>
aws ec2 stop-instances --instance-ids <id>

# Terminate instance (DANGER)
aws ec2 terminate-instances --instance-ids <id>
```

### Network & Security
```bash
# Describe security group rules
aws ec2 describe-security-groups --group-ids <sg-id> --query "SecurityGroups[].IpPermissions"

# Add ingress rule (Port 22 from specific IP)
aws ec2 authorize-security-group-ingress --group-id <sg-id> --protocol tcp --port 22 --cidr <your-ip>/32
```

## 🧠 Best Practices
1. **Tag Everything**: Use standard tagging (Name, Env, Owner) for billing and discovery.
2. **Instance Profiles**: Use IAM Roles instead of storing hard-coded credentials on instances.
3. **Spot Instances**: Use Spot for stateless workloads (like Remotion rendering) to save up to 90%.
4. **Security Groups**: Default to "Deny All" and only open specific ports for required CIDRs.

# SAP BTP Operations Reference

## Overview

Effective administration and operations ensure stable, efficient, and cost-optimized application performance in the cloud.

## Administrator Responsibilities

### User and Access Management

**Tasks:**
- Identity management
- Organizational structure setup
- Quota allocation
- Role assignments

**Tools:**
- SAP BTP Cockpit
- Identity Authentication Service
- Role Collections

### Performance Monitoring

**Key Metrics:**
- System runtime
- SQL query execution
- Background job status
- Response times
- Error patterns

### Resource Management

**Activities:**
- Monitor consumption patterns
- Adjust sizing configurations
- Leverage hibernation features
- Cost optimization

### Lifecycle Oversight

**Scope:**
- Custom application management
- Transport processes
- Add-on deployments
- Multi-tenant administration

### Integration Assurance

**Focus:**
- Data synchronization between cloud and on-premises
- API health monitoring
- Event processing status

## Supporting Tools

| Tool | Purpose | Environment |
|------|---------|-------------|
| SAP Fiori Launchpad | UI access, administration | All |
| SAP BTP Cockpit | Platform administration | All |
| Landscape Portal | Partner/SaaS management | ABAP |
| Technical Monitoring Cockpit | On-stack analysis | ABAP |
| SAP Cloud ALM | Central monitoring | All |
| ABAP Test Cockpit | Code quality | ABAP |

## Run and Scale Operations

### Core Principles

1. **Continuous user feedback** - Optimize based on real usage
2. **Proactive monitoring** - Use SAP BTP observability tools
3. **Security integration** - Protect against emerging threats
4. **Compliance maintenance** - Regular security audits

### Scaling Strategies

#### Cloud Foundry

**Horizontal Scaling:**
```bash
# Scale instances
cf scale my-app -i 5

# Scale memory
cf scale my-app -m 1G
```

**Auto-scaling:**
- Configure in BTP Cockpit
- Based on CPU/memory thresholds
- Schedule-based scaling

**Availability Zones:**
- Automatic distribution across AZs
- Handle ~1/3 capacity loss during AZ failure

#### Kyma

**Horizontal Pod Autoscaler:**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 80
```

#### ABAP Environment

**Elastic Scaling:**
- Manual ACU/HCU adjustment via BTP Cockpit
- Automatic scaling between 1 ACU and configured maximum
- 0.5 ACU increments

**Decision Metrics:**
- CPU usage
- Memory consumption
- Active work process counts

### Cost Optimization

#### System Hibernation (ABAP)

**Benefits:**
- Reduces costs to <5% of operational expenses
- Preserves HANA Cloud instance
- Automatic restart during maintenance

**Management:**
- Via Landscape Portal
- Scheduled activation/deactivation
- Trial accounts auto-hibernate nightly

#### Resource Right-Sizing

| Environment | Recommendation |
|-------------|----------------|
| Development | Minimal resources, hibernation |
| Test | Moderate resources, scheduled scaling |
| Production | Right-sized, auto-scaling enabled |

## Maintenance and Upgrades

### ABAP Environment Updates

**Downtime-Optimized Process:**

| Phase | Status | Duration |
|-------|--------|----------|
| Preparation | System available | Variable |
| Takeover | Downtime | 10-40 minutes |
| Postprocessing | System available | Background |

### Pre-Upgrade Option

**Purpose:** Test custom applications before standard upgrades

**Guidelines:**
- Non-development systems only
- Available 4 weeks before release
- Report issues via SAP support
- Validates existing applications (not early feature access)

### Security Patching

**Best Practices:**
1. Regularly apply security patches
2. Monitor dependency vulnerabilities
3. Test patches in non-production first
4. Maintain patch schedule

## Secure Operations

### Continuous Threat Monitoring

**Tools:**
- SAP Cloud ALM
- SAP Cloud Logging
- Alert Notification Service

**Actions:**
- Real-time anomaly detection
- Automated alerting
- Incident response procedures

### Secure Auto-Scaling

**CAP Multitenancy:**
- Built-in tenant isolation
- Resource management per tenant
- Secure scaling for SaaS

### Security Audits

**Schedule:** Periodic (quarterly recommended)

**Scope:**
- Configuration review
- Compliance verification
- Vulnerability assessment

### Data Protection

**Requirements:**
- Privacy law compliance (GDPR, HIPAA)
- Secure data handling
- User consent management

## Transport Management

### gCTS (ABAP)

**Flow:**
```
Development → Test → Production
     ↓          ↓         ↓
   Release    Import    Import
```

**Tools:** Manage Software Components app

### SAP Cloud Transport Management (CAP)

**Configuration:**
```yaml
transport:
  landscape:
    - name: DEV
    - name: QA
      requires: DEV
    - name: PROD
      requires: QA
```

## Monitoring Best Practices

### Dashboards

**Key Panels:**
- Application health
- Response times
- Error rates
- Resource utilization
- Integration status

### Alerts

**Configuration:**

| Metric | Threshold | Action |
|--------|-----------|--------|
| Error rate | > 1% | Page on-call |
| Response time | > 2s | Warning email |
| Memory | > 80% | Auto-scale or alert |
| CPU | > 70% | Auto-scale or alert |

### Log Management

**Retention:**
- Development: 7 days
- Test: 14 days
- Production: 30+ days

**Analysis:**
- Full-text search
- Structured queries
- Correlation with traces

## Troubleshooting

### Common Issues

| Issue | Diagnosis | Resolution |
|-------|-----------|------------|
| High latency | Check traces | Optimize queries, scale |
| Memory pressure | Check heap usage | Increase memory, optimize code |
| Connection errors | Check destinations | Verify credentials, network |
| Failed jobs | Check job logs | Fix data issues, retry |

### Useful Commands

**Cloud Foundry:**
```bash
# Recent logs
cf logs my-app --recent

# Application info
cf app my-app

# Environment variables
cf env my-app

# Events
cf events my-app
```

**Kyma:**
```bash
# Pod logs
kubectl logs -f deployment/my-app

# Describe pod
kubectl describe pod my-app-xxx

# Resource usage
kubectl top pods
```

## Source Documentation

- Administrate and Operate: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/administrate-and-operate-f8fe432.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/administrate-and-operate-f8fe432.md)
- Run and Scale: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/run-and-scale-fcb51b5.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/run-and-scale-fcb51b5.md)
- Maintain and Upgrade: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/maintain-and-upgrade-d24bc66.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/maintain-and-upgrade-d24bc66.md)

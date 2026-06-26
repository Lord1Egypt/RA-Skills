# SAP BTP Operations and Monitoring - Detailed Reference

**Source**: [https://github.com/SAP-docs/btp-best-practices-guide/tree/main/docs/go-live-and-monitor](https://github.com/SAP-docs/btp-best-practices-guide/tree/main/docs/go-live-and-monitor)

---

## Go-Live Process

### Prerequisites

1. Complete testing and compliance verification
2. Establish staging environment structure
3. Deploy application to production environment
4. Configure user provisioning and authorization

### Go-Live Timing Best Practices

- Establish specific timeframes for go-live activities
- Restrict deployments during critical periods (e.g., quarter-end)
- Allow exceptions only for emergencies
- Document change freeze windows

### User Enablement

**Recommendation**: Embed applications in SAP Fiori Launchpad via SAP BTP Portal before go-live.

Benefits:
- Improved usability
- Consistent user experience
- Central application access point
- Role-based app visibility

---

## Authentication and Authorization Post Go-Live

### Business User Provisioning

Users must be provisioned through:
- SAP ID Service
- External identity providers (recommended: SAP Cloud Identity Services)

### Authorization Configuration

Administrators can:
- Create roles based on application requirements
- Build role collections grouping related roles
- Assign collections to business users and user groups

### Role Collection Example

```
Role Collection: HR_MANAGER
├── Role: EmployeeViewer (from app-hr)
├── Role: TeamManager (from app-hr)
└── Role: ReportAccess (from app-reporting)
```

---

## Content Delivery Network (CDN)

### Use Case

For geographically distributed users, CDN improves:
- Response times
- Load distribution
- Static content delivery

### CDN Best Practices

| Practice | Description |
|----------|-------------|
| **HTTPS Enforcement** | Use HTTPS-only connections |
| **Location-Based Access** | Implement geographic access controls |
| **Compression** | Enable gzip compression |
| **Static Content Caching** | Cache images, CSS, JS, fonts |
| **Dynamic Content Exclusion** | Don't cache dynamic responses |
| **Cache Headers** | Respect application cache directives |
| **CSRF Protection** | Never cache CSRF tokens |

### Cache-Control Header Example

```
# Static assets - long cache
Cache-Control: public, max-age=31536000

# HTML - revalidate
Cache-Control: no-cache

# API responses - no cache
Cache-Control: no-store, must-revalidate
```

---

## SAP Cloud ALM

### Overview

SAP Cloud ALM is included in SAP Cloud Service subscriptions containing Enterprise Support. It provides unified monitoring for:
- SAP BTP-based applications
- Custom applications
- Hybrid landscapes

### Monitoring Capabilities

| Capability | Description |
|------------|-------------|
| **Real User Monitoring** | Track actual user experience and performance |
| **Health Monitoring** | System availability and health status |
| **Integration Monitoring** | Monitor integration flows and interfaces |
| **Exception Monitoring** | Track and alert on application errors |
| **Job Automation Monitoring** | Monitor scheduled jobs and automations |

### Integration with SAP BTP

```
SAP BTP Applications
        │
        ▼
   Data Collection
        │
        ▼
  ┌─────────────────┐
  │   SAP Cloud ALM │
  │                 │
  │ ┌─────────────┐ │
  │ │ Dashboards  │ │
  │ └─────────────┘ │
  │ ┌─────────────┐ │
  │ │ Alerts      │ │
  │ └─────────────┘ │
  │ ┌─────────────┐ │
  │ │ Analytics   │ │
  │ └─────────────┘ │
  └─────────────────┘
```

---

## Local SAP BTP Monitoring Tools

### SAP Job Scheduling Service

**Purpose**: Schedule and manage recurring jobs across runtimes.

**Features**:
- Runtime-agnostic (CF, Kyma)
- Cron-based scheduling
- Job monitoring and history
- Retry policies

**Example Job Definition**:
```json
{
  "name": "daily-cleanup",
  "description": "Daily data cleanup job",
  "action": "https://my-app.cfapps.region.hana.ondemand.com/cleanup",
  "active": true,
  "httpMethod": "POST",
  "schedules": [
    {
      "cron": "0 0 2 * * *",
      "description": "Run at 2 AM daily",
      "active": true
    }
  ]
}
```

### SAP Cloud Logging

**Purpose**: Centralized observability for logs, metrics, and traces.

**Supported Runtimes**:
- Cloud Foundry
- Kyma
- Kubernetes

**Features**:
- Log aggregation
- Metrics collection
- Distributed tracing
- Alerting integration

### Neo Environment Monitoring

For Neo applications (Java, SAP HANA XS, HTML5):
- Cockpit-based monitoring
- Application metrics
- Resource utilization
- Error tracking

---

## Platform Availability Monitoring

### SAP Trust Center

Access platform status at: [https://www.sap.com/about/trust-center/cloud-service-status.html](https://www.sap.com/about/trust-center/cloud-service-status.html)

**Features**:
- Region-specific status
- Service availability
- Planned maintenance windows
- Incident history

### Cloud System Notification Subscriptions

Subscribe to notifications for:
- Planned maintenance
- Incidents
- Status updates
- Region-specific events

---

## Alerting

### SAP Alert Notification Service

**Purpose**: Instant notifications across multiple delivery channels.

**Delivery Channels**:
- Email
- Slack/Microsoft Teams
- Ticketing systems (ServiceNow, JIRA)
- SAP Cloud ALM
- Custom webhooks

### Alert Configuration Example

```json
{
  "name": "high-error-rate",
  "description": "Alert on high error rate",
  "conditions": {
    "eventType": "error",
    "severity": "ERROR",
    "threshold": 10,
    "timeWindow": "5m"
  },
  "actions": [
    {
      "type": "EMAIL",
      "recipients": ["ops-team@company.com"]
    },
    {
      "type": "SLACK",
      "webhookUrl": "https://hooks.slack.com/..."
    }
  ]
}
```

### Alert Best Practices

1. **Define Alert Severity Levels**: Critical, Warning, Info
2. **Set Appropriate Thresholds**: Avoid alert fatigue
3. **Implement Escalation**: Time-based escalation paths
4. **Document Runbooks**: Response procedures for each alert type
5. **Regular Review**: Tune alerts based on false positive rates

---

## Operations Automation

### SAP Automation Pilot

**Purpose**: Low-code/no-code automation for operational tasks.

**Capabilities**:
- Pre-built automation commands
- Custom command creation
- Manual or triggered execution
- Integration with monitoring services

**Use Cases**:
- Application restart procedures
- Scaling operations
- Backup triggers
- Incident response automation
- Resource cleanup

### Automation Example: Application Restart

```yaml
name: RestartApplication
description: Restart CF application on health check failure
trigger:
  type: ALERT
  source: SAP_ALERT_NOTIFICATION
  conditions:
    eventType: HEALTH_CHECK_FAILED
steps:
  - name: StopApplication
    command: cf.StopApplication
    parameters:
      applicationName: ${event.applicationName}
      orgName: ${event.orgName}
      spaceName: ${event.spaceName}
  - name: Wait
    command: Sleep
    parameters:
      duration: 30s
  - name: StartApplication
    command: cf.StartApplication
    parameters:
      applicationName: ${event.applicationName}
      orgName: ${event.orgName}
      spaceName: ${event.spaceName}
```

---

## Integration and Testing

### Integration Tests

**Definition**: Verify all building blocks work together, meet requirements, and fulfill business cases.

**Timing**: After landscape integration, part of CI/CD pipelines

**Distinction from Unit Tests**: Integration tests verify complete system interplay across multiple components.

### SAPUI5 Integration Testing

**OPA5 (One Page Acceptance Tests)**:
- API for SAPUI5 controls
- Test user interactions
- Test navigation
- Test data binding
- Manages asynchronicity

**Example OPA5 Test**:
```javascript
opaTest("Should navigate to detail page", function(Given, When, Then) {
  Given.iStartMyApp();
  When.onTheMainPage.iPressOnTheFirstItem();
  Then.onTheDetailPage.iShouldSeeTheDetailPage();
  Then.iTeardownMyApp();
});
```

### Application Integration Options

| Option | Use Case |
|--------|----------|
| **Cloud Connector** | Point-to-point, on-premise connectivity |
| **SAP Cloud Integration** | Complex multi-system, mediation needs |
| **Cloud Integration Automation** | Guided workflows, reusable configs |

---

## Cost Management

### Monitoring Costs

1. **Monthly Review**: Check *Costs and Usage* in BTP cockpit
2. **Service Analysis**: Identify top cost contributors
3. **Trend Analysis**: Track usage patterns
4. **Label Filtering**: Use labels for custom cost views

### Billing Validation

- Access *Billing* section in cockpit
- Current month shows estimations
- Drill into costs by subaccount and service
- Export data for internal accounting

### Cost Distribution Methods

| Method | Description |
|--------|-------------|
| **Data Exports** | Export usage data for processing |
| **APIs** | Programmatic access to usage data |
| **Fixed-Rate** | Allocate based on agreed percentages |

### Automated Cost Alerting

Combine:
- Usage Data Management service
- Alert Notification service

To receive alerts when:
- Approaching quota limits
- Unusual consumption patterns
- Budget thresholds exceeded

---

## Maintenance and Improvement

### Ongoing Maintenance Tasks

1. **Regular Testing**: Prevent issues from library/platform updates
2. **Compliance Verification**: Ongoing security and policy checks
3. **Bug Fixes**: Focus on user experience quality
4. **User Feedback**: Incorporate improvement suggestions
5. **Automated Alerting**: Via SAP Alert Notification Service
6. **Task Automation**: Using SAP Automation Pilot

### Update Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| **Blue-Green Deployment** | Two production environments, switch traffic | Zero-downtime updates |
| **Feature Flags** | Toggle features without deployment | Gradual rollouts |
| **Canary Releases** | Route percentage of traffic to new version | Risk mitigation |

### Staying Current

- Review SAP Release Notes regularly
- Monitor SAP Community for updates
- Subscribe to product notifications
- Plan for major version upgrades

---

## Application Retirement

### Decommissioning Checklist

1. [ ] Notify users of retirement timeline
2. [ ] Export required data
3. [ ] Undeploy the application
4. [ ] Delete related service instances
5. [ ] Remove destinations
6. [ ] Remove role collections
7. [ ] Clean up platform content
8. [ ] Meet data retention obligations
9. [ ] Document decommissioning
10. [ ] Archive configuration for reference

### Neo to Multi-Cloud Migration

SAP recommends migrating from Neo to multi-cloud foundation:
- Closer integration with AWS, GCP, Azure
- Modern runtime options
- Future-proof architecture

---

**Source Documentation**:
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/go-live-and-monitor/go-live-and-operate-b0ab4fb.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/go-live-and-monitor/go-live-and-operate-b0ab4fb.md)
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/integrate-and-test/integrate-and-test-84ddc25.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/integrate-and-test/integrate-and-test-84ddc25.md)
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/improve-and-retire/improve-and-retire-89ffeab.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/improve-and-retire/improve-and-retire-89ffeab.md)
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/managing-cost-c615301.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/managing-cost-c615301.md)

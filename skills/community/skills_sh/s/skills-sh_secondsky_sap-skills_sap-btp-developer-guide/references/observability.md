# SAP BTP Observability Reference

## Overview

SAP BTP observability operates through two interconnected layers:
- **Central Layer**: SAP Cloud ALM - unified strategic view
- **Local Layer**: SAP Cloud Logging - granular technical insights

Both layers integrate through APIs and context-sensitive navigation using telemetry data (logs, metrics, traces).

## OpenTelemetry Strategy

SAP has standardized on OpenTelemetry as the industry standard for cloud-native observability.

**Key Principles:**
- Standardized instrumentation across SAP and customer applications
- Open APIs for non-SAP data source integration
- Seamless data flow through managed collectors

## SAP Cloud ALM

**Included with**: Enterprise Support subscriptions

**Provisioning**: Via SAP for Me

### Capabilities

| Feature | Description |
|---------|-------------|
| Real User Monitoring | Actual user experience tracking |
| Health Monitoring | System and application health |
| Integration Monitoring | Cross-system integration status |
| Exception Monitoring | Error tracking and analysis |
| Job Monitoring | Background job status |
| Automation Monitoring | Automated process tracking |
| Synthetic User Monitoring | Selenium-based availability tests |
| Business Service Management | End-to-end service health |
| Intelligent Event Processing | Automated event correlation |

### Supported Platforms

**SaaS Applications:**
- SAP S/4HANA Cloud
- SAP HANA Cloud
- SAP Analytics Cloud

**PaaS Runtimes:**
- Cloud Foundry
- Kyma

### Integration

```yaml
# CAP configuration for Cloud ALM
cds:
  requires:
    cloud-alm:
      kind: sap-cloud-alm
      credentials:
        destination: cloud-alm-api
```

## SAP Cloud Logging

**Based on**: OpenSearch

**Deployment**: Instance-based service

### Capabilities

| Feature | Description |
|---------|-------------|
| Log Analytics | Full-text search, structured queries |
| Distributed Tracing | Cross-microservice request tracking |
| Technology Monitoring | Runtime metrics (Java/Node.js) |
| Custom Telemetry | Application-specific metrics |
| Alerting | Threshold-based notifications |
| Dashboards | Custom visualizations |

### Service Binding

```yaml
# mta.yaml
resources:
  - name: my-cloud-logging
    type: org.cloudfoundry.managed-service
    parameters:
      service: cloud-logging
      service-plan: standard

modules:
  - name: my-srv
    requires:
      - name: my-cloud-logging
```

### CAP Integration

```javascript
// Automatic logging with CAP
const cds = require('@sap/cds');
const LOG = cds.log('my-service');

module.exports = (srv) => {
  srv.on('READ', 'Books', (req) => {
    LOG.info('Reading books', { user: req.user.id });
    // Business logic
  });
};
```

### Custom Metrics

> **Note**: This snippet assumes a MeterProvider is already configured by the platform (e.g., SAP Cloud Logging SDK) or application bootstrap. When using SAP BTP services, the telemetry infrastructure typically provides this setup automatically.

```javascript
const { metrics } = require('@opentelemetry/api');

// Assumes MeterProvider is registered by SAP Cloud Logging or platform setup
const meter = metrics.getMeter('my-app');
const orderCounter = meter.createCounter('orders_created', {
  description: 'Number of orders created'
});

// Increment counter
orderCounter.add(1, { customer_type: 'enterprise' });
```

### Custom Traces
```javascript
const { trace } = require('@opentelemetry/api');

const tracer = trace.getTracer('my-app');

async function processOrder(orderId) {
  const span = tracer.startSpan('process-order');
  span.setAttribute('order.id', orderId);

  try {
    // Processing logic
    span.setStatus({ code: SpanStatusCode.OK });
  } catch (error) {
    span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
    throw error;
  } finally {
    span.end();
  }
}
```

## SAP Alert Notification

**Purpose**: Route critical events to notification channels

**Channels:**
- Email
- SMS
- Slack
- Microsoft Teams
- ServiceNow
- Custom webhooks

### Configuration
```json
{
  "conditions": [
    {
      "name": "critical-errors",
      "propertyKey": "severity",
      "predicate": "EQUALS",
      "propertyValue": "CRITICAL"
    }
  ],
  "actions": [
    {
      "name": "notify-team",
      "type": "SLACK",
      "properties": {
        "webhookUrl": "https://hooks.slack.com/..."
      }
    }
  ]
}
```

## ABAP Technical Monitoring Cockpit

**Purpose**: On-stack analysis and optimization

**Features:**
- System workload monitoring
- Resource consumption tracking
- Request statistics
- Outbound communication analysis
- SQL statement analysis
- Work process monitoring

### Key Metrics

| Metric | Description |
|--------|-------------|
| Dialog Response Time | Average transaction response |
| CPU Utilization | Application server CPU usage |
| Memory Consumption | Heap and stack usage |
| Database Time | SQL execution duration |
| Work Process Usage | Active vs. total processes |

## Implementation by Runtime

### Cloud Foundry

```yaml
# manifest.yml
applications:
  - name: my-app
    env:
      SAP_CLOUD_LOGGING_ENABLED: true
      OTEL_EXPORTER_OTLP_ENDPOINT: "..."
```

### Kyma

```yaml
apiVersion: telemetry.kyma-project.io/v1alpha1
kind: LogPipeline
metadata:
  name: my-logs
spec:
  input:
    application:
      namespaces:
        include: [my-namespace]
  output:
    http:
      host: cloud-logging-endpoint
```

### ABAP Environment

Automatic integration with:
- Technical Monitoring Cockpit
- SAP Cloud ALM
- Security Audit Log
- Application Logging

## Best Practices

### Logging
1. Use structured logging (JSON format)
2. Include correlation IDs for request tracing
3. Log at appropriate levels (DEBUG, INFO, WARN, ERROR)
4. Avoid logging sensitive data

### Metrics
1. Define SLIs (Service Level Indicators)
2. Set up SLOs (Service Level Objectives)
3. Create dashboards for key metrics
4. Configure alerts for threshold breaches

### Tracing
1. Propagate trace context across services
2. Add meaningful span attributes
3. Use semantic conventions
4. Sample appropriately in production

## Learning Resources

| Resource | Description |
|----------|-------------|
| Mission 4432/4718 | Implement Observability in CAP Application |
| Learning Journey | Cloud Foundry Observability |
| Expert Portal | SAP Cloud ALM Configuration |

## Source Documentation

- Observability: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/establish-end-to-end-observability-34065a4.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/establish-end-to-end-observability-34065a4.md)
- Observability Mission: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/mission-implement-observability-in-a-full-stack-cap-application-c5636db.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/mission-implement-observability-in-a-full-stack-cap-application-c5636db.md)
- SAP Cloud ALM: [https://help.sap.com/docs/cloud-alm](https://help.sap.com/docs/cloud-alm)
- SAP Cloud Logging: [https://help.sap.com/docs/cloud-logging](https://help.sap.com/docs/cloud-logging)

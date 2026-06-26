# Bug Report: Export Feature White Screen

**Reporter:** zhang.wei@acmecorp.com
**Priority:** High
**Labels:** bug, export, frontend

## Description

Hi support team,

I'm Zhang Wei from Acme Corp (tenant: acme-prod-01). Since this morning around 2:30 PM UTC, clicking the "Export Report" button on the analytics dashboard causes a white screen. My colleague Li Na (lina@acmecorp.com) confirmed the same issue on her machine.

We're on the enterprise plan and this is blocking our quarterly reporting. Please escalate ASAP.

## Environment

- URL: https://app.example.com/dashboard/analytics
- Version: v2.4.1 (build 8837)
- Browser: Chrome 122.0.6261.112 on macOS 14.3
- Account role: workspace-admin
- Feature flag: new_export_engine=true

## Steps to Reproduce

1. Log into the analytics dashboard
2. Select date range "Q1 2024"
3. Click "Export Report" button
4. Page goes white, console shows error

## Error Message

```
TypeError: Cannot read properties of undefined (reading 'map')
```

## Additional Context

This started after the deployment yesterday. Our account manager is David Chen (david.chen@example.com, phone: +1-415-555-0198).

My phone: 13812345678
Our order number: ORD-2024-78832

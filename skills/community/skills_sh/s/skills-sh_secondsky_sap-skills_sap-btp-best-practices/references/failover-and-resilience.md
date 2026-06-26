# SAP BTP Failover and Resilience - Detailed Reference

**Source**: [https://github.com/SAP-docs/btp-best-practices-guide/tree/main/docs/deploy-and-deliver](https://github.com/SAP-docs/btp-best-practices-guide/tree/main/docs/deploy-and-deliver)

---

## High Availability Overview

SAP BTP applications can achieve high availability through multi-region deployment with intelligent traffic routing. This eliminates single points of failure and addresses latency concerns for global users.

---

## Multi-Region Architecture

### Core Concept

```
                    Custom Domain URL
                           │
                           ▼
                    ┌──────────────┐
                    │ Load Balancer │
                    │ (Health Checks)│
                    └──────┬───────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
    ┌─────────────────┐       ┌─────────────────┐
    │  Region 1       │       │  Region 2       │
    │  (Active)       │       │  (Passive/Active)│
    │                 │       │                 │
    │  Subaccount A   │       │  Subaccount B   │
    │  App Instance   │       │  App Instance   │
    └─────────────────┘       └─────────────────┘
```

### Key Benefits

- **Geographic Redundancy**: Regional outages don't interrupt service
- **Intelligent Routing**: Health checks direct traffic to operational instances
- **Unified Access**: Custom domain remains constant during failovers
- **Load Distribution**: Traffic balances across regions
- **Latency Optimization**: Route users to nearest healthy region

---

## Failover Scope

### Supported Application Types

The basic failover guidance applies to:
- SAPUI5 applications
- HTML5 applications
- Applications without data persistence
- Applications without in-memory caching
- Applications with data stored in on-premise back-end systems

**Note**: Applications with cloud-based persistence require additional considerations for data synchronization.

---

## Four Core Failover Principles

### 1. Deploy Across Two Data Centers

**Configuration**: Active/Passive

- Primary data center receives normal traffic
- Secondary data center acts as standby
- Switch to secondary only during primary downtime

**Regional Selection Best Practices**:
- Choose regions near users and backend systems
- Example: Frankfurt and Amsterdam for European users
- Consider same region for performance
- Review data processing restrictions for cross-region deployment

**Legal Consideration**: Cross-region deployment may create data processing compliance issues. Review Data Protection and Privacy documentation before proceeding.

### 2. Keep Applications Synchronized

**Synchronization Options**:

| Method | Effort | Best For |
|--------|--------|----------|
| Manual | High | Infrequent updates |
| CI/CD Pipeline | Medium | Regular deployments |
| Solution Export + Transport Management | Medium | Neo environments |

#### Manual Synchronization

- Duplicate modifications across both data centers
- Mirror Git repositories
- Allows non-identical applications (reduced functionality in backup)
- Visual differentiation between primary and backup

#### CI/CD Pipeline Synchronization

```yaml
# Pipeline deploys to both regions
stages:
  - name: Build
    steps:
      - build_mta

  - name: Deploy Primary
    steps:
      - deploy_to_region_1

  - name: Deploy Secondary
    steps:
      - deploy_to_region_2
```

- Use Project "Piper" pipelines adapted for multi-deployment
- Parallel deployment to subaccounts in different regions
- Automatic consistency

#### Solution Export Wizard + Cloud Transport Management

1. Export changes as MTA archive from primary (Neo)
2. Import via Transport Management Service (Cloud Foundry)
3. Deploy to secondary data center

### 3. Define Failover Detection

**Detection Mechanisms**:

- Response timeout monitoring (e.g., 25 seconds max)
- HTTP status code checking (5xx errors)
- Health endpoint monitoring

**Implementation Options**:
- Manual code implementation
- Rule-based solutions (e.g., Akamai ION)
- Load balancer health checks

**Detection Behavior**:
- Monitor first HTTP request to application URL
- Ignore subsequent requests (prevent single resource failures triggering failover)
- Present HTML down page with failover link when detected

**Note**: In basic scenarios, "the failover itself is therefore manually performed by the user" via the down page link.

### 4. Plan for Failback

**Active/Active Setup**:
- Applications identical in both data centers
- Same functionality everywhere
- Failback automatic with next failover event
- Not mandatory to explicitly return to primary

**Active/Passive Setup**:
- Applications may differ between data centers
- Reduced functionality in backup acceptable
- Failback to primary is mandatory
- Must restore full functionality

**Recommended Failback Approach**:
- User-driven failback model
- Visual differentiation reminds users to switch back
- Allow transactions to complete without interruption
- Prioritize completion over automatic recovery speed

---

## Multi-Region Reference Use Cases

### Available Implementations

| Scenario | Components | Resources |
|----------|------------|-----------|
| **SAP Build Work Zone + Azure Traffic Manager** | Work Zone, Azure | Blog post, GitHub, Discovery Center mission |
| **SAP Build Work Zone + Amazon Route 53** | Work Zone, AWS | Blog post, GitHub |
| **CAP Applications + SAP HANA Cloud** | CAP, HANA Cloud multi-zone | GitHub repository |
| **CAP Applications + Amazon Aurora** | CAP, Aurora read replica | GitHub repository |
| **SAP Cloud Integration + Azure Traffic Manager** | CPI, Azure | GitHub, Discovery Center |

### Architecture: SAP Build Work Zone + Azure Traffic Manager

```
User Request
     │
     ▼
Azure Traffic Manager
(Priority-based routing)
     │
     ├──► Primary Region (Priority 1)
     │    └── SAP Build Work Zone Instance
     │
     └──► Secondary Region (Priority 2)
          └── SAP Build Work Zone Instance (standby)
```

### Architecture: CAP + HANA Cloud Multi-Zone

```
     Application Load Balancer
              │
     ┌────────┴────────┐
     ▼                 ▼
CAP App (AZ1)     CAP App (AZ2)
     │                 │
     └────────┬────────┘
              ▼
    SAP HANA Cloud
    (Multi-zone replication)
```

---

## Data Backup and Resilience

### SAP-Managed Backups

| Service | Backup Type | Retention | Notes |
|---------|-------------|-----------|-------|
| **SAP HANA Cloud** | Continuous | As configured | Database recovery supported |
| **PostgreSQL (Hyperscaler)** | Point-in-time | 14 days | Restore by creating new instance |
| **Redis** | None | N/A | No persistence support |
| **Object Store** | None | N/A | Use versioning for protection |

### Object Store Protection Mechanisms

- **Object Versioning**: Recover from accidental deletion
- **Expiration Rules**: Automatic version cleanup
- **Deletion Prevention**: AWS S3 buckets, Azure containers

### Runtime-Specific Backup Strategies

| Runtime | Strategy |
|---------|----------|
| **Cloud Foundry** | Multi-AZ replication within region |
| **Kyma** | Managed K8s snapshots (excludes volumes) |
| **Neo** | Cross-region data copies |

### Customer-Managed Backups

**Critical**: SAP doesn't manage backups of service configurations. You are responsible for backing up your service-specific configurations.

**Key Responsibilities**:

| Responsibility | Details |
|----------------|---------|
| **Self-Service Backup** | You must back up service configurations yourself |
| **Service Documentation Review** | Consult each service's documentation for backup capabilities |
| **Service Limitations Awareness** | Some services don't support user-specific configuration backups |
| **Risk Mitigation** | Backup frequency varies by service; prevents accidental data loss |

**Actions Required**:
1. Identify all SAP BTP services currently in use
2. Review service-specific backup documentation
3. Understand which services lack backup capabilities
4. Implement backup strategies for supported configurations
5. Plan accordingly for services without backup features
6. Ensure business continuity plans include config recovery

**Note**: If backup information is unavailable for a service, contact SAP support channels.

---

## Kyma Cluster Sharing and Isolation

### When to Share Clusters

**Recommended**:
- Small teams with modest resource needs
- Development and testing environments
- Non-critical workloads
- Teams with established trust

**Not Recommended**:
- Multiple external customers
- Production workloads with strict isolation
- Untrusted tenants

### Control Plane Isolation Strategies

| Strategy | Description |
|----------|-------------|
| **Namespaces** | Isolate API resources within cluster |
| **RBAC** | Manage permissions within namespaces |
| **Global Resources** | Admin-managed CRDs and global objects |
| **Policy Engines** | Gatekeeper, Kyverno for compliance |
| **Resource Quotas** | Set limits per tenant/namespace |

### Data Plane Isolation Strategies

| Strategy | Description |
|----------|-------------|
| **Network Policies** | Restrict inter-namespace traffic |
| **Centralized Observability** | Cluster-wide metrics tracking |
| **Service Mesh (Istio)** | mTLS, dedicated ingress per tenant |

### Sample Network Policy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-cross-namespace
  namespace: tenant-a
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: tenant-a
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              name: tenant-a
```

---

## Disaster Recovery Planning

### Recovery Time Objective (RTO)

Depends on:
- Failover detection speed
- Application synchronization lag
- User-driven vs automatic failover

### Recovery Point Objective (RPO)

Depends on:
- Synchronization frequency
- Data persistence strategy
- Backup retention periods

### DR Checklist

- [ ] Define RTO and RPO requirements
- [ ] Select multi-region architecture
- [ ] Implement application synchronization
- [ ] Configure failover detection
- [ ] Test failover procedures regularly
- [ ] Document failback process
- [ ] Train operations team
- [ ] Establish communication protocols

---

## Resilient Application Development

### Design Principles

1. **Statelessness**: Minimize in-memory state
2. **Idempotency**: Safe to retry operations
3. **Circuit Breakers**: Graceful degradation
4. **Health Endpoints**: Enable monitoring
5. **Graceful Shutdown**: Complete in-flight requests

### Health Endpoint Example

```javascript
app.get('/health', (req, res) => {
  const health = {
    status: 'UP',
    checks: {
      database: checkDatabase(),
      cache: checkCache(),
      externalApi: checkExternalApi()
    }
  };

  const allHealthy = Object.values(health.checks)
    .every(check => check.status === 'UP');

  res.status(allHealthy ? 200 : 503).json(health);
});
```

---

**Source Documentation**:
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/planning-failover-on-sap-btp-8c46464.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/planning-failover-on-sap-btp-8c46464.md)
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/deploy-and-deliver/implementing-failover-df972c5.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/deploy-and-deliver/implementing-failover-df972c5.md)
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/deploy-and-deliver/deploy-your-application-in-two-data-centers-61d08d8.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/deploy-and-deliver/deploy-your-application-in-two-data-centers-61d08d8.md)
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/deploy-and-deliver/keep-the-two-applications-in-sync-e6d2bdb.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/deploy-and-deliver/keep-the-two-applications-in-sync-e6d2bdb.md)
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/deploy-and-deliver/define-how-a-failover-is-detected-88b86db.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/deploy-and-deliver/define-how-a-failover-is-detected-88b86db.md)
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/deploy-and-deliver/decide-on-the-failback-963f962.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/deploy-and-deliver/decide-on-the-failback-963f962.md)
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/deploy-and-deliver/multi-region-usecases.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/deploy-and-deliver/multi-region-usecases.md)
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/deploy-and-deliver/data-backups-managed-by-sap-6c1e071.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/deploy-and-deliver/data-backups-managed-by-sap-6c1e071.md)
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/sharing-clusters-in-kyma-57ec1ea.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/sharing-clusters-in-kyma-57ec1ea.md)

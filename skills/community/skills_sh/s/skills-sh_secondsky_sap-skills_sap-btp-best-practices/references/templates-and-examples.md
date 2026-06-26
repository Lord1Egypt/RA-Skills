# SAP BTP Templates and Code Examples - Detailed Reference

**Source**: [https://github.com/SAP-docs/btp-best-practices-guide](https://github.com/SAP-docs/btp-best-practices-guide)

This reference contains complete templates, manifests, and configuration examples from the official documentation.

---

## Getting Started Checklist - Complete Steps

### Phase 1: Fulfill Prerequisites (9 Steps)

| Step | Action | Resources |
|------|--------|-----------|
| 1 | **Platform Familiarization** | SAP BTP Guidance Framework, Learning Journey: Discover SAP BTP, Basic Platform Concepts, Shared Responsibility Model |
| 2 | **Discovery Center Exploration** | Explore services, missions, reference architectures at [https://discovery-center.cloud.sap/](https://discovery-center.cloud.sap/) |
| 3 | **Project Identification** | Identify pilot projects using SAP BTP Use Cases page |
| 4 | **Free Tier Consideration** | Note: "Only community support is available for free tier service plans and they are not subject to SLAs" |
| 5 | **Commercial Model Selection** | Choose subscription or consumption-based; review SAP BTP and Integration Suite pricing |
| 6 | **SLA Review** | Review SAP BTP Service Description Guide and SAP Trust Center |
| 7 | **Onboarding Confirmation** | Receive onboarding email with cockpit access; existing users contact global account admin |
| 8 | **Customer Number Acquisition** | Obtain customer number for support purposes |
| 9 | **Team Building** | Establish Platform Engineering Team (CoE) and Cloud Development Team |

### Phase 2: Get Started (4 Steps)

1. **Onboard to SAP Cloud Identity Services** - Configure identity provider
2. **Set Up Account Model** - Choose runtime (Kyma vs Cloud Foundry)
3. **Configure Security Model** - Establish security and compliance framework
4. **Create Enrollment Process** - Define onboarding workflow for development projects

### Phase 3: Implement (4 Steps)

1. **Develop and Deploy** - Use SAP Cloud Application Programming Model
2. **Test and Evaluate** - Thorough testing before production
3. **Go Live** - Launch to production
4. **Improve or Retire** - Continuous enhancement or decommission

---

## Account Administration Responsibilities

| Level | Key Responsibilities |
|-------|---------------------|
| **Global Account** | Appoint administrators; manage entitlements and quotas for distribution |
| **Directory** | Manage member access; oversee entitlements (if enabled) |
| **Subaccount** | Assign business roles; manage member access |

**Recommendation**: Appoint substitute administrators at each level to ensure continuity.

---

## Deployment Methods by Runtime - Complete Reference

### Cloud Foundry and Neo Environments

| Application Type | Deployment Tools |
|------------------|------------------|
| **Java Applications** | SAP BTP cockpit, Cloud Foundry CLI, Console client (Neo) |
| **HTML5 Applications** | SAP Business Application Studio, Cloud Foundry CLI, SAP BTP cockpit |
| **Node.js Applications** | SAP Business Application Studio, Cloud Foundry CLI |
| **SAP HANA XSA Applications** | SAP HANA Deployment Infrastructure (HDI) from Business Application Studio, Cloud Foundry CLI |
| **Custom Buildpacks** | Deployment dependent on buildpack specifications |

**Key Recommendation**: Archive all components into a Multitarget Application (MTA) with deployment descriptor.

### Kyma Environment

| Approach | Description |
|----------|-------------|
| **Standard Dockerfile** | Package application in Linux Docker image |
| **Cloud Native Buildpacks** | Alternative to Dockerfile for containerization |
| **Kubernetes Jobs** | Use HTML5 application deployer |
| **Automation (Production)** | SAP Continuous Integration and Delivery with Helm charts |

**Supported Technologies**: Java, Node.js, Python, Scala, .Net, and others when packaged as Linux Docker images.

**Production Recommendation**: Use automation tools rather than manual deployment processes.

---

## Directory Template

When creating new directories, document the following:

| Field | Requirement | Example |
|-------|-------------|---------|
| **Name** | Follow naming guidelines | `hr-applications` |
| **Owners** | Minimum two owners recommended | Platform Engineering Team leads |
| **Description** | Developer audience, department, application types, runtimes, subscriptions | "HR department applications using Cloud Foundry, CAP framework" |
| **Cost Center** | Define accounting requirements | `CC-HR-001` |
| **Enrollment** | Describe project enrollment process | "Submit via ServiceNow, approval within 5 days" |

---

## Kyma RBAC Complete Manifest Examples

### ClusterRole: cluster-viewer

Provides view permissions across all resources:

```yaml
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: cluster-viewer
rules:
  - apiGroups: ['*']
    verbs: ['get', 'list', 'watch']
    resources: ['*']
```

### ClusterRole: common-resource-viewer

Enables viewing Kyma-specific objects (applications, gateways):

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: common-resource-viewer
rules:
  - verbs: [get, list, watch]
    apiGroups:
      - applicationconnector.kyma-project.io
      - networking.istio.io
    resources:
      - applications
      - gateways
```

### Operator View Access

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cluster-admin-view-crb
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-viewer
subjects:
  - apiGroup: rbac.authorization.k8s.io
    kind: Group
    name: <operators-group-name>
```

### Operator Impersonation Setup (3 Manifests)

**Step 1 - Bind virtual user to cluster-admin role:**

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cluster-admin-crb
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
  - apiGroup: rbac.authorization.k8s.io
    kind: User
    name: cluster-admin
```

**Step 2 - Create impersonation ClusterRole:**

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cluster-admin-impersonator
rules:
  - apiGroups: ['']
    resources: ['users']
    verbs: ['impersonate']
    resourceNames: ['cluster-admin']
```

**Step 3 - Bind impersonation to operators group:**

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cluster-admin-impersonate-crb
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin-impersonator
subjects:
  - apiGroup: rbac.authorization.k8s.io
    kind: Group
    name: <operators-group-name>
```

### Developer Namespace Admin (Dev/Test)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: dev-team-admin-rb
  namespace: <namespace>
subjects:
  - kind: Group
    name: <dev-team-group-name>
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: admin
  apiGroup: rbac.authorization.k8s.io
```

### Developer Production Impersonation (4 Manifests)

**Step 1 - Create app-specific impersonation ClusterRole:**

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: app-admin-impersonator
rules:
  - apiGroups: ['']
    resources: ['users']
    verbs: ['impersonate']
    resourceNames: ['app-admin-vuser']
```

**Step 2 - Bind impersonation to team:**

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: app-team-impersonation-crb
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: app-admin-impersonator
subjects:
  - apiGroup: rbac.authorization.k8s.io
    kind: Group
    name: <app-team-group-name>
```

**Step 3 - Bind virtual user to admin in namespace:**

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-admin-rb
  namespace: <namespace>
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: admin
subjects:
  - apiGroup: rbac.authorization.k8s.io
    kind: User
    name: app-admin-vuser
```

**Step 4 - Provide read access to namespace:**

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: namespace-viewer-rb
  namespace: <namespace>
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-viewer
subjects:
  - apiGroup: rbac.authorization.k8s.io
    kind: Group
    name: <app-team-group-name>
```

### Common Resource Viewer Binding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: developers-common-resources-crb
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: common-resource-viewer
subjects:
  - apiGroup: rbac.authorization.k8s.io
    kind: Group
    name: <developers-group-name>
```

---

## Multi-Region Reference Use Cases - Complete Links

**Note**: Repository structures may change. Always verify current paths at the repository root.

### Use Case 1: SAP Build Work Zone + Azure Traffic Manager

| Resource Type | Link |
|---------------|------|
| **Blog Post** | "Multi-region High Availability architecture for SAP BTP Launchpad Service using Azure Traffic Manager" (SAP Community) |
| **GitHub** | [https://github.com/SAP-samples/btp-services-intelligent-routing](https://github.com/SAP-samples/btp-services-intelligent-routing) |
| **Discovery Center** | Mission: "Route Multi-Region Traffic to SAP BTP Services Intelligently" |

### Use Case 2: SAP Build Work Zone + Amazon Route 53

| Resource Type | Link |
|---------------|------|
| **Blog Post** | "High Availability of SAP Build Work Zone with Amazon Route 53" (SAP Community) |
| **GitHub** | [https://github.com/SAP-samples/btp-services-intelligent-routing](https://github.com/SAP-samples/btp-services-intelligent-routing) |

### Use Case 3: CAP Applications + SAP HANA Cloud Multi-Zone

| Resource Type | Link |
|---------------|------|
| **GitHub** | [https://github.com/SAP-samples/cap-distributed-resiliency](https://github.com/SAP-samples/cap-distributed-resiliency) |

### Use Case 4: CAP Applications + Amazon Aurora Read Replica

| Resource Type | Link |
|---------------|------|
| **GitHub** | [https://github.com/SAP-samples/cap-distributed-resiliency](https://github.com/SAP-samples/cap-distributed-resiliency) |

### Use Case 5: SAP Cloud Integration + Azure Traffic Manager

| Resource Type | Link |
|---------------|------|
| **GitHub** | [https://github.com/SAP-samples/btp-services-intelligent-routing](https://github.com/SAP-samples/btp-services-intelligent-routing) |
| **Discovery Center** | Mission: "Route Multi-Region Traffic to SAP BTP Services Intelligently" |

**Discovery Center URL**: [https://discovery-center.cloud.sap/](https://discovery-center.cloud.sap/)

---

## Neo Environment Monitoring Table

| Application Type | Monitoring Options | Resources |
|------------------|-------------------|-----------|
| **Java Applications** | Application monitoring, custom thresholds, availability checks, heap/thread dumps, email alerts, logging APIs | Monitoring Java Applications; Using Logs in Cockpit for Java Applications |
| **SAP HANA XS Applications** | Application monitoring, availability checks, HTTP checks, email alerts, database health statistics | Monitoring Database Systems |
| **HTML5 Applications** | Application monitoring, custom checks, email alerts, application logging | Monitoring HTML5 Applications; Using Logs in Cockpit |

**Additional**: Dynatrace SaaS monitoring integration available for Java applications.

---

## Cluster Sharing Isolation Strategies

### Control Plane Isolation

| Strategy | Description | Implementation |
|----------|-------------|----------------|
| **Namespaces** | Logical grouping isolating API resources | Each team/project gets dedicated namespace |
| **RBAC** | Control user access and permissions | Scope activities to respective namespaces |
| **Global Resources** | Admin-managed cluster-wide resources | Centrally manage CRDs affecting all tenants |
| **Policy Engines** | Enforce tenant policies | Gatekeeper or Kyverno for compliance |
| **Resource Controls** | Fair consumption management | Resource quotas, limit ranges, Pod priorities |

### Data Plane Isolation

| Strategy | Description | Implementation |
|----------|-------------|----------------|
| **Network Policies** | Control traffic flow | Restrict inter-namespace communication |
| **Centralized Observability** | Cluster-wide metrics | Tenant-restricted data access |
| **Istio Service Mesh** | Advanced traffic control | mTLS between Pods, dedicated ingress per tenant |

### Sample Network Policy (Deny Cross-Namespace)

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
              kubernetes.io/metadata.name: tenant-a
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: tenant-a
    - to:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: kube-system
      ports:
        - protocol: UDP
          port: 53
```

---

## CI/CD Configuration Templates

### SAP Continuous Integration and Delivery Pipeline Config

```yaml
# .pipeline/config.yml
general:
  buildTool: 'mta'
  productiveBranch: 'main'

service:
  buildToolVersion: 'MBTJ11N14'

stages:
  Build:
    mtaBuild: true

  Additional Unit Tests:
    npmExecuteScripts:
      runScripts:
        - 'test'

  Acceptance:
    cloudFoundryDeploy:
      deployTool: 'mtaDeployPlugin'
      deployType: 'standard'
      cfOrg: 'my-org'
      cfSpace: 'dev'
      cfCredentialsId: 'cf-credentials'

  Release:
    cloudFoundryDeploy:
      deployTool: 'mtaDeployPlugin'
      deployType: 'standard'
      cfOrg: 'my-org'
      cfSpace: 'prod'
      cfCredentialsId: 'cf-credentials'
```

### Project "Piper" Jenkinsfile Example

```groovy
@Library('piper-lib-os') _

node {
    stage('Prepare') {
        checkout scm
        setupCommonPipelineEnvironment script: this
    }

    stage('Build') {
        mtaBuild script: this
    }

    stage('Unit Tests') {
        npmExecuteScripts script: this, runScripts: ['test']
    }

    stage('Deploy to Dev') {
        cloudFoundryDeploy script: this,
            deployTool: 'mtaDeployPlugin',
            cfOrg: 'my-org',
            cfSpace: 'dev'
    }

    stage('Integration Tests') {
        // Add integration test execution
    }

    stage('Deploy to Prod') {
        cloudFoundryDeploy script: this,
            deployTool: 'mtaDeployPlugin',
            cfOrg: 'my-org',
            cfSpace: 'prod'
    }
}
```

---

## MTA Deployment Descriptor Template

```yaml
_schema-version: "3.1"
ID: my-application
version: 1.0.0
description: "SAP BTP Application"

parameters:
  enable-parallel-deployments: true

build-parameters:
  before-all:
    - builder: custom
      commands:
        - npm ci
        - npm run build

modules:
  - name: my-app-srv
    type: nodejs
    path: gen/srv
    parameters:
      buildpack: nodejs_buildpack
      memory: 256M
    provides:
      - name: srv-api
        properties:
          srv-url: ${default-url}
    requires:
      - name: my-app-db
      - name: my-app-auth

  - name: my-app-db-deployer
    type: hdb
    path: gen/db
    parameters:
      buildpack: nodejs_buildpack
    requires:
      - name: my-app-db

  - name: my-app-ui
    type: approuter.nodejs
    path: app/
    parameters:
      keep-existing-routes: true
      disk-quota: 256M
      memory: 256M
    requires:
      - name: srv-api
        group: destinations
        properties:
          name: srv-api
          url: ~{srv-url}
          forwardAuthToken: true
      - name: my-app-auth

resources:
  - name: my-app-db
    type: com.sap.xs.hdi-container
    parameters:
      service: hana
      service-plan: hdi-shared

  - name: my-app-auth
    type: org.cloudfoundry.managed-service
    parameters:
      service: xsuaa
      service-plan: application
      path: ./xs-security.json
```

---

## Kyma Helm Chart Template

### Chart.yaml

```yaml
apiVersion: v2
name: my-kyma-app
description: A Helm chart for SAP BTP Kyma deployment
type: application
version: 1.0.0
appVersion: "1.0.0"
```

### values.yaml

```yaml
replicaCount: 2

image:
  repository: my-registry/my-app
  pullPolicy: IfNotPresent
  tag: "latest"

service:
  type: ClusterIP
  port: 8080

ingress:
  enabled: true
  className: ""
  annotations:
    kubernetes.io/ingress.class: istio
  hosts:
    - host: my-app.kyma.example.com
      paths:
        - path: /
          pathType: Prefix

resources:
  limits:
    cpu: 500m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80

nodeSelector: {}
tolerations: []
affinity: {}
```

### Deployment Template Example

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "my-kyma-app.fullname" . }}
  labels:
    {{- include "my-kyma-app.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "my-kyma-app.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "my-kyma-app.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: 8080
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
```

---

**Source Documentation**:
- [https://github.com/SAP-docs/btp-best-practices-guide](https://github.com/SAP-docs/btp-best-practices-guide)
- [https://github.com/SAP-samples/btp-services-intelligent-routing](https://github.com/SAP-samples/btp-services-intelligent-routing)
- [https://github.com/SAP-samples/cap-distributed-resiliency](https://github.com/SAP-samples/cap-distributed-resiliency)

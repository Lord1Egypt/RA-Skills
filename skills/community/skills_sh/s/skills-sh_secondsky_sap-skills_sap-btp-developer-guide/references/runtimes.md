# SAP BTP Runtimes Comparison Reference

## Overview

SAP BTP provides flexible runtime options allowing development teams to select environments based on technical requirements, developer skills, and cost considerations.

## Runtime Options

### 1. Cloud Foundry Runtime

**Best For**: Traditional PaaS applications, rapid deployment

**Characteristics:**
- Managed application runtime
- Buildpack-based deployments
- Simple scaling with `cf scale`
- Memory-based billing

**Languages:**
- Node.js
- Java
- Python
- Go
- PHP

**Use Cases:**
- Cloud-native applications
- Microservices
- API backends
- Scheduled jobs

### 2. Kyma Runtime

**Best For**: Kubernetes-native applications, containerized workloads

**Characteristics:**
- Managed Kubernetes cluster
- Istio service mesh included
- Helm-based deployments
- Container-based billing

**Technologies:**
- Kubernetes
- Docker containers
- Helm charts
- Istio service mesh
- Serverless functions

**Use Cases:**
- Container-based applications
- Microservices with service mesh
- Event-driven architectures
- Custom runtime requirements

### 3. ABAP Environment

**Best For**: Organizations with ABAP expertise, SAP extensions

**Characteristics:**
- Managed ABAP platform
- RAP programming model
- Integrated SAP Fiori Launchpad
- ACU/HCU-based billing

**Languages:**
- ABAP (restricted cloud-safe subset)

**Use Cases:**
- SAP S/4HANA extensions
- Enterprise business applications
- Migrating ABAP custom code
- ISV solutions

## Comparison Matrix

| Aspect | Cloud Foundry | Kyma | ABAP Environment |
|--------|--------------|------|------------------|
| **Programming** | Node.js, Java, Python | Any containerized | ABAP Cloud |
| **Deployment** | cf push / MTA | Helm / kubectl | gCTS / Landscape Portal |
| **Scaling** | Horizontal (instances) | Kubernetes pods | Elastic ACUs |
| **Persistence** | HANA Cloud, PostgreSQL | HANA Cloud, any | HANA Cloud (managed) |
| **UI** | SAPUI5, Fiori Elements | Any | Fiori Elements |
| **Billing Model** | Memory consumption | Cluster + resources | ACU + HCU |

## Metering Details

### Cloud Foundry
- **Start**: When runtime memory is consumed (e.g., application deployment)
- **Metric**: GB-hours of memory
- **Optimization**: Stop unused applications, right-size memory

### Kyma
- **Start**: When Kyma runtime is enabled (cluster creation)
- **Metric**: Dedicated Kubernetes cluster resources
- **Optimization**: Node autoscaling, resource limits

### ABAP Environment
- **Start**: When ABAP system is provisioned
- **Metric**: ABAP Compute Units (ACU) + HANA Compute Units (HCU)
- **Optimization**: System hibernation, elastic scaling

## Choosing a Runtime

### Choose Cloud Foundry When:
- Developing CAP applications with Node.js or Java
- Need simple deployment model
- Want buildpack-managed dependencies
- Cost-sensitive workloads

### Choose Kyma When:
- Need Kubernetes-native features
- Require service mesh (Istio)
- Building container-based microservices
- Need serverless functions
- Custom runtime requirements

### Choose ABAP Environment When:
- Have existing ABAP expertise
- Extending SAP S/4HANA
- Need tight SAP integration
- Building partner add-on products
- Migrating custom ABAP code

## CAP Support Across Runtimes

### Cloud Foundry
```bash
# Deploy CAP to Cloud Foundry
mbt build
cf deploy mta_archives/my-app.mtar
```

### Kyma
```bash
# Deploy CAP to Kyma
cds add helm
helm upgrade --install my-app ./chart
```

### ABAP (Not CAP)
- Use RAP (ABAP RESTful Application Programming Model)
- Different programming model, similar concepts

## Runtime-Specific Documentation

| Runtime | Documentation |
|---------|--------------|
| Cloud Foundry | [https://help.sap.com/docs/btp/sap-business-technology-platform/cloud-foundry-environment](https://help.sap.com/docs/btp/sap-business-technology-platform/cloud-foundry-environment) |
| Kyma | [https://help.sap.com/docs/btp/sap-business-technology-platform/kyma-environment](https://help.sap.com/docs/btp/sap-business-technology-platform/kyma-environment) |
| ABAP | [https://help.sap.com/docs/btp/sap-business-technology-platform/abap-environment](https://help.sap.com/docs/btp/sap-business-technology-platform/abap-environment) |

## Source Documentation

- Runtime Benefits: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/strengths-and-benefits-of-the-runtimes-and-their-programming-models-86688d1.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/strengths-and-benefits-of-the-runtimes-and-their-programming-models-86688d1.md)
- CF/Kyma with CAP: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/sap-btp-cloud-foundry-and-sap-btp-kyma-runtimes-with-cap-0f9cfe9.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/sap-btp-cloud-foundry-and-sap-btp-kyma-runtimes-with-cap-0f9cfe9.md)
- ABAP Environment: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/sap-btp-abap-environment-with-abap-cloud-174b229.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/sap-btp-abap-environment-with-abap-cloud-174b229.md)

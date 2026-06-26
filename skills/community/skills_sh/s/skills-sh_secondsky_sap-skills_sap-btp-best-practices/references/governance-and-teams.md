# SAP BTP Governance and Teams - Detailed Reference

**Source**: [https://github.com/SAP-docs/btp-best-practices-guide/tree/main/docs/set-up-and-plan](https://github.com/SAP-docs/btp-best-practices-guide/tree/main/docs/set-up-and-plan)

---

## Governance Model Overview

Establishing an appropriate organizational setup and governance model is one of the first and most important steps in the cloud journey.

### Benefits of Good Governance

- Easier adoption of agile processes
- Clear responsibilities and ownership
- Streamlined onboarding for new projects
- Consistent security and compliance
- Efficient resource utilization

### Preparatory Steps

Before launching development initiatives:
1. Establish an onboarding framework for new projects
2. Create a knowledge transfer system for teams

### Governance Model Implementation Areas

| Area | Key Activities |
|------|----------------|
| **Organizational Structure** | Team composition definitions, IT support positions, accountability assignments |
| **Process Development** | Integration pathways, knowledge sharing, operations documentation, tool selection |
| **Resource & Change Management** | Personnel scaling, process improvements, system tools, reference materials |
| **Support Operations** | Help desk workflows, incident management protocols, change management procedures |

**Reference**: Team Topologies (teamtopologies.com) for organizational design patterns.

---

## Team Structure

### Required Teams

#### Platform Engineering Team (Center of Excellence)

**Purpose**: Manage cloud landscape infrastructure and reduce complexity for development teams.

**Core Responsibilities**:
- Account operations and management
- Build infrastructure setup
- Governance and compliance guidelines
- Security framework implementation
- Enable developers with reduced cognitive load
- Operate and ensure stable, secure cloud landscape

**Extended CoE Functions**:
- Drive cloud adoption and migration organization-wide
- Provide thought leadership and roadblock resolution guidance
- Identify, evaluate, and implement SAP BTP use cases
- Can include enabling teams composed of specialists

**Does NOT Handle**:
- Individual application lifecycles
- Application-specific development
- Application-specific operations

**Composition**:
- Skilled technology experts
- Cloud architects
- Security specialists
- Infrastructure engineers
- May include specialized sub-teams

#### Cloud Development Teams

**Purpose**: Develop and operate applications on SAP BTP.

**Approach**: DevOps model - same team both develops AND operates applications.

**Responsibilities**:
- Application development
- Application deployment
- Application monitoring
- Regular maintenance
- Post-launch support
- UI component compatibility verification (every 6 months)

**Key Principle**: Avoid traditional Build-Run separation where different teams handle development versus operations.

---

## Essential Documentation

### Three Core Documents

| Document | Owner | Purpose |
|----------|-------|---------|
| **Onboarding Documentation** | Platform Engineering | Guide new projects through enrollment |
| **Security Guidelines** | Platform Engineering + Security | Define security requirements and standards |
| **Services Catalog** | Platform Engineering | Provide templated services for developers |

### Onboarding Document Contents

Every new application should document:

| Field | Description |
|-------|-------------|
| Organization/Department | Business unit owning the application |
| Application Identifier | Unique identifier for tracking |
| Business Rationale | Why this application is needed |
| Go-Live Timeline | Target production date |
| Owner | Primary responsible person |
| Access Requirements | Who needs access and what level |
| User Accessibility Scope | Internal, external, specific groups |
| System Integration Details | Connected systems and interfaces |
| Technology Stack | Languages, frameworks, services |
| Repository Location | **Keep outside SAP BTP** to prevent accidental deletion |
| Testing Approach | Testing strategy and requirements |

### Security Document Contents

**Requires security expert approval before development begins.**

| Field | Description |
|-------|-------------|
| Owner Identification | Security-responsible person |
| Business Scenario | Use case and context |
| User Classifications | Types of users and roles |
| Data Sensitivity Levels | Classification of handled data |
| Policy Compliance | Applicable policies and standards |
| Data Flow | How data moves through system |
| Data Storage | Where and how data is stored |
| Connected Systems | External integrations |
| Protocols | Communication protocols used |
| Authentication Framework | Identity and authentication approach |
| Authorization Framework | Permissions and access control |
| Audit Procedures | Logging and audit requirements |

### Services Catalog Contents

Platform Engineering Team provides templated services:

- Destination management
- Build configuration
- Application restart procedures
- Access provisioning
- Database schema creation
- CI/CD pipeline templates
- Monitoring setup

**Automation Options**:
- SAP BTP APIs
- btp CLI
- SAP BTP Setup Automator

---

## Knowledge Transfer Process

### Key Practices

1. **Document and Share**: Platform Engineering Team documents and shares knowledge with current and incoming staff

2. **Training Sessions**: "Set up training and enablement sessions to get everyone on board"

3. **Communication Channels**: Create dedicated channels (e.g., SAP Build Work Zone) for:
   - Lessons learned
   - Guidance and recommendations
   - Best practice sharing
   - Q&A support

### Knowledge Areas

- Platform architecture and capabilities
- Account model and structure
- Security requirements and procedures
- Development standards
- Deployment processes
- Operations procedures

---

## Onboarding Process for Projects

### Project Enrollment Steps

1. **Submit Onboarding Document**: Complete all required fields
2. **Security Review**: Security document approval
3. **Resource Allocation**: Assign subaccounts, quotas, entitlements
4. **Access Provisioning**: Set up team access rights
5. **Integration Setup**: Configure Cloud Connector, destinations
6. **CI/CD Setup**: Establish deployment pipelines
7. **Monitoring Setup**: Configure alerting and dashboards

### Self-Service vs. Managed

| Aspect | Self-Service | Managed |
|--------|--------------|---------|
| Speed | Faster | Slower |
| Control | Less | More |
| Suitable For | Low-risk, sandbox | Production, sensitive |
| Governance | Light | Full |

---

## Account Administration Tools

### Available Options

| Tool | Use Case | Automation |
|------|----------|------------|
| **SAP BTP Cockpit** | GUI administration | No |
| **btp CLI** | Terminal, scripting | Yes |
| **REST APIs** | Programmatic | Yes |
| **Terraform Provider** | Infrastructure as Code | Yes |
| **SAP Automation Pilot** | Low-code automation | Yes |

### btp CLI Overview

Alternative to cockpit for users who:
- Prefer terminal work
- Want to automate operations using scripts

**Handles**:
- Global account management
- Directory management
- Subaccount management

**Note**: Environment-specific tools needed after environment creation:
- cf CLI (Cloud Foundry)
- Kyma CLI
- kubectl (Kubernetes)

### Terraform Provider

**Purpose**: Automate infrastructure provisioning using code (IaC).

**Current Status**: Available for non-productive environments; SAP developing for production use.

**Repository**: HashiCorp registry + SAP GitHub samples

**Example**:
```hcl
resource "btp_subaccount" "my_subaccount" {
  name      = "my-dev-subaccount"
  subdomain = "my-company-dev"
  region    = "eu10"
}

resource "btp_subaccount_entitlement" "hana_cloud" {
  subaccount_id = btp_subaccount.my_subaccount.id
  service_name  = "hana-cloud"
  plan_name     = "hana"
}
```

---

## Shared Responsibility Model

### SAP Manages

| Area | Responsibility |
|------|----------------|
| **Infrastructure** | Software updates, patches, maintenance |
| **Monitoring** | Infrastructure, OS, and service monitoring |
| **Capacity** | Capacity management and troubleshooting |
| **Incidents** | Incident management and resolution |
| **Provisioning** | Global account creation, resource provisioning |
| **HANA Operations** | Hardware, backup, recovery, security |
| **Kyma System** | `kyma-system` namespace management |

### Customer Manages

| Area | Responsibility |
|------|----------------|
| **Account Strategy** | Global account and subaccount planning |
| **Configuration** | Subaccount configuration and setup |
| **Development** | Application development and security |
| **Deployment** | Application creation, deployment, management |
| **Authorization** | Role assignments for applications |
| **Integration** | System integration and connectivity |
| **Monitoring** | Application monitoring and health checks |
| **Maintenance** | Application updates and improvements |
| **Security** | OSS vulnerability scanning, updates |
| **HANA Updates** | Trigger revision updates via self-service |

### Additional Resources

- SAP BTP Security Recommendations
- Operating Model documentation

---

## Cost Management Governance

### Commercial Model Selection

| Model | Best For |
|-------|----------|
| **Consumption-Based** | Pilots, flexibility, new workloads |
| **Subscription-Based** | Established use cases, known services |

### Contract Strategies

1. **Consolidation**: Combine subscriptions into one global account (reduces TCO)
2. **Hybrid Accounts**: Mix subscription and consumption-based
3. **Separation**: Multiple consumption contracts require separate global accounts

**Note**: Consumption credits non-transferable between global accounts.

### Governance Practices

1. **Minimal Entitlements**: Provide only required set to prevent overage
2. **Quota Management**: Set appropriate limits per subaccount
3. **Monthly Monitoring**: Review costs and usage in cockpit
4. **Label Usage**: Enable filtering and cost allocation
5. **Automated Alerts**: Set up usage threshold notifications

---

## Checklist: Account Model Setup

### Prerequisites

- [ ] Review SAP Cloud Identity Services onboarding guide
- [ ] Assess organizational needs for account model selection
- [ ] Test hierarchy with pilot project managers
- [ ] Familiarize teams with administration tools

### Ownership Structure

| Level | Recommended Owner |
|-------|-------------------|
| Global Account | Platform Engineering Team/CoE |
| Directories | Designated owners with role collections |
| Subaccounts | Designated owners with role collections |
| Spaces/Namespaces | Development units |

### Standards to Define

- [ ] Directory creation template and process
- [ ] Naming conventions
- [ ] Labels and values for reporting
- [ ] Quota limitation rules
- [ ] Entitlement distribution rules

### Directory Template Required Fields

- Name (following naming guidelines)
- Minimum two owners
- Description of developer audience
- Expected applications
- Cost center allocation
- Enrollment procedures

---

## Staged Development Environment

### Standard Three-Subaccount Model

| Subaccount | Purpose |
|------------|---------|
| **Development** | Cloud-based development, individual testing |
| **Testing** | Integration testing, production-like conditions |
| **Production** | Live applications |

### Flexibility Options

- Combine development and testing
- Create additional subaccounts for large backends
- Maintain separate subaccounts for different projects

### Reasons for Separate Subaccounts

1. Isolate different projects or scenarios
2. Separate team workflows
3. Control application access and administration
4. Share databases across similar projects
5. Host centralized shared services

### Important Considerations

| Consideration | Guidance |
|---------------|----------|
| **On-Premises Connections** | Each subaccount needs separate integration setup |
| **Geographic Selection** | Choose regions near customers for latency |
| **Regulatory Compliance** | Segregate S/4HANA tenants when legally required |
| **Team Structure** | Separate DevOps teams warrant distinct subaccounts |

---

## Development Lifecycle

### Phases

1. **Explore**: Identify business opportunity, set up team roles
2. **Discover**: Identify use cases, understand technology
3. **Design**: User experience design, domain-driven design
4. **Deliver**: Set up landscape, develop application
5. **Run and Scale**: Gather feedback, optimize, operate

### Programming Models

**SAP Cloud Application Programming Model (CAP)**:
- Framework for enterprise-grade services
- Supports Java, JavaScript, TypeScript
- Domain-driven design approach

**ABAP Cloud**:
- Modern ABAP for cloud
- RAP (RESTful ABAP Programming Model)
- Extensions for ABAP-based products

---

**Source Documentation**:
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/creating-a-governance-model-bf0ce2c.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/creating-a-governance-model-bf0ce2c.md)
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/building-teams-fdeddf2.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/building-teams-fdeddf2.md)
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/creating-a-knowledge-transfer-process-630c14c.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/creating-a-knowledge-transfer-process-630c14c.md)
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/creating-an-onboarding-process-for-development-projects-4bd29a8.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/creating-an-onboarding-process-for-development-projects-4bd29a8.md)
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/tools-for-account-administration-6bdb3a7.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/tools-for-account-administration-6bdb3a7.md)
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/shared-responsibility/shared-responsibility-model-between-you-and-sap-898509d.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/shared-responsibility/shared-responsibility-model-between-you-and-sap-898509d.md)

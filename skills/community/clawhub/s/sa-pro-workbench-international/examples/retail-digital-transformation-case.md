# SA Presales Case Library

> This directory contains complete cases of real presales solution scenarios, demonstrating the full chain from customer material analysis to bid material package delivery.
>
> **Important Disclaimer**: The competitive analysis, specific solution details, technology selection, and architecture design in this case library, except where explicitly cited, are all constructed based on industry practice inference and presales methodology frameworks. They do not represent any real customer's internal information or non-public data.

## Case List

| No. | Case Name | Industry | Core Methodology |
|------|----------|------|-----------|
| C01 | Large Retailer Omni-Channel Digital Transformation Solution | Retail | C4 Model + TOGAF 4A + SPIN + ADR |
| C02 | Dell Supply Chain Digital Transformation Solution | Technology/Manufacturing | C4 Model + TOGAF 4A + SPIN + ADR |

---

## Case C01: Large Retailer Omni-Channel Digital Transformation Solution

### Scenario Background

> **Real Case Source**: The core framework and transformation methodology of this case reference the McKinsey "Rewired" methodology (Eric Lamarre, Kate Smaje, Rodney Zemmel, *Rewired: The McKinsey Guide to Outcompeting in the Age of Digital and AI*, Wiley, 2023), as well as soreno.ai's public analysis article on McKinsey's implementation of digital transformation for a large retailer. The core transformation logic—shifting from product-centric to customer-centric omni-channel transformation, data-driven customer journey mapping, quick wins (click-and-collect) to build trust, and change management running in parallel with technology implementation—all come from this public case.

A large retailer (annual revenue exceeding $10 billion, global store network spanning multiple countries, tens of thousands of employees) faced the impact of e-commerce and dramatic shifts in consumer behavior, launching an omni-channel digital transformation. Core objectives:
- Shift from "product-centric" (category management as core) to "customer-centric" (customer journey as core) omni-channel operating model
- Break down online-offline data silos to achieve a unified customer view and inventory view
- Build data-driven decision-making capabilities to support real-time business decisions
- Achieve measurable business results within 18-24 months

### Customer Material Analysis

**RFP Key Information Extraction**:

| Dimension | Customer Requirements | Implicit Needs (SPIN Discovery) |
|------|----------|---------------------|
| Business Goals | Omni-channel integration, unified customer experience | Online channel share increase, customer lifetime value (LTV) improvement of 30%+ |
| Technology Goals | Modernized tech stack, cloud-native architecture | Break free from legacy system constraints, reduce IT O&M costs, improve delivery speed |
| Data Goals | Unified Customer Data Platform (CDP), real-time analytics | 360° customer view, supporting personalized recommendations and precision marketing |
| Organizational Goals | Deep business + IT integration | IT department transforms from "support role" to "business innovation engine" |
| Change Goals | Smooth transition, zero business disruption | Build organizational confidence through Quick Wins, change management and technology implementation in parallel |

**Competitive Intelligence** (based on industry practice inference):

| Competitor | Solution Positioning | Strengths | Weaknesses |
|------|----------|------|------|
| Major Cloud Provider A | Full-stack cloud-native + ecosystem | Strong brand, complete tech stack | Relatively weak retail industry know-how, solution leans "technology-driven" |
| Internet Platform B | Data Middle Platform + e-commerce experience | Deepest retail scenario understanding, rich traffic ecosystem | Customer concerns about data lock-in and platform dependency |
| Traditional ERP Vendor C | Packaged software + industry solutions | International compliance, mature processes | High price, long implementation cycles, insufficient architectural flexibility |

### Transformation Methodology: McKinsey "Rewired" Core Framework

> The following methodology framework comes from the public content of McKinsey's *Rewired* book and soreno.ai's public analysis of this case.

**Rewired Six Core Capabilities**:

| Capability Dimension | Core Content | Embodiment in This Case |
|----------|----------|-----------------|
| 1. Clear Business Value Strategy | Focus on specific domains (customer journeys/processes/functions) to generate significant value | Shift from "product-centric" to "customer-centric", focusing on end-to-end customer journeys |
| 2. Internal Talent Engine | Build in-house digital talent teams rather than outsourcing | Establish internal digital teams, business + technology blended staffing |
| 3. Scalable Operating Model | Cross-functional teams operating at scale | Adopt "Digital Factory" model, agile teams scaling horizontally |
| 4. Distributed Technology Environment | Each team can independently innovate and deliver | API-first, microservices architecture, developer self-service platform |
| 5. Data Democratization | Reliable, real-time data accessible on-demand by all teams | Build unified CDP, data productization (Data Product) |
| 6. Adoption & Change Management | For every $1 invested in development, invest at least $1 in change management | Change management and technology implementation in parallel, quick wins to build trust |

**Transformation Path — Three-Phase Roadmap**:

```
Phase 1: Quick Wins (0-6 months)
  ├── click-and-collect (order online, pick up in store) Go-live
  ├── Unified customer ID, break down online-offline membership silos
  └── Establish Digital Factory, form first batch of agile teams

Phase 2: Scaling (6-18 months)
  ├── Omni-channel inventory real-time sharing
  ├── Personalized recommendation engine Go-live
  ├── Data Middle Platform (CDP + Data Lake) in production
  └── Agile teams expand from 5 to 50+

Phase 3: Platform-based (18-36 months)
  ├── AI-driven intelligent pricing and promotions
  ├── End-to-end supply chain digitization
  ├── Open platform, ecosystem partner integration
  └── Cultural transformation from "Digital Project" to "Digital Enterprise"
```

### C4 Model Architecture Modeling

> The following architecture design is based on industry practice inference, combined with the "Distributed Technology Environment" and "Data Productization" principles from the McKinsey Rewired methodology.

#### Level 1: System Context Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    Omni-Channel Retail Digital Platform            │
│                                                                   │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐      │
│  │ Consumers │   │ Store Staff│   │ HQ Operations│ │ Suppliers  │      │
│  │(App/H5/   │   │(POS/Handheld│  │(Ops Backend)│ │(Supplier   │      │
│  │ Mini-App) │   │ Terminal)  │   │          │   │ Portal)    │      │
│  └─────┬─────┘   └─────┬─────┘   └─────┬─────┘   └─────┬─────┘      │
│        │               │               │               │            │
│        ▼               ▼               ▼               ▼            │
│  ┌─────────────────────────────────────────────────────────┐      │
│  │           Omni-Channel Retail Digital Platform (Core)      │      │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐        │      │
│  │  │Customer  │ │Order     │ │Real-time │ │Data      │        │      │
│  │  │Journey   │ │Fulfillment│ │Inventory │ │Intelligence│      │      │
│  │  │Orchestration│ │Hub     │ │Hub      │ │Platform  │        │      │
│  │  │Engine    │ │          │ │          │ │          │        │      │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘        │      │
│  └─────────────────────────────────────────────────────────┘      │
│        │               │               │               │            │
│        ▼               ▼               ▼               ▼            │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐      │
│  │ Payment   │   │ Logistics │   │ Marketing │   │ 3rd-Party │      │
│  │ Gateway   │   │ TMS       │   │ Platform  │   │ E-commerce│      │
│  │(Multi-pay)│   │(Multi-carrier)│ │(CDP/MA)  │   │(Platform  │      │
│  │          │   │          │   │          │   │ Integration)│     │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

#### Level 2: Container Diagram — Core System

| Container | Type | Tech Stack (Inferred) | Responsibility |
|------|------|--------|------|
| API Gateway | Gateway | Kong/APISIX | Unified entry, rate limiting, authentication, routing |
| Customer Journey Orchestration Engine | Microservice | Spring Cloud + K8s | End-to-end customer journey orchestration, cross-channel experience consistency |
| Order Fulfillment Hub | Microservice | Go + PostgreSQL | Order routing, order splitting, fulfillment scheduling |
| Real-time Inventory Hub | Microservice | Java + Redis | Omni-channel inventory real-time sharing, safety stock alerts |
| Data Intelligence Platform | Data Platform | Flink + StarRocks + CDP | Real-time/offline data processing, customer 360° profiling |
| Personalized Recommendation Engine | AI Service | Python + TensorFlow | Real-time recommendations, A/B experimentation platform |
| Message Middleware | Infrastructure | Apache Kafka | Event-driven, asynchronous decoupling |
| Configuration Center | Infrastructure | Nacos | Configuration management, service discovery |

#### Level 3: Component Diagram — Customer Journey Orchestration Engine

```
Customer Journey Orchestration Engine Internal Components:
┌────────────────────────────────────────────┐
│           Customer Journey Orchestration Engine │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Journey   │  │ Event     │  │ Channel   │  │
│  │ Designer  │  │ Listener  │  │ Adapter   │  │
│  │ - Journey │  │ - Event   │  │ - App     │  │
│  │   Canvas  │  │   Capture │  │   Adapter │  │
│  │ - Trigger │  │ - Event   │  │ - H5      │  │
│  │   Rules   │  │   Routing │  │   Adapter │  │
│  │ - A/B     │  │ - Event   │  │ - Store   │  │
│  │   Split   │  │   Sourcing│  │   Adapter │  │
│  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  │
│        │              │              │         │
│        ▼              ▼              ▼         │
│  ┌──────────────────────────────────────────┐ │
│  │     Customer Journey State Machine        │ │
│  │  Browse → Add to Cart → Order → Pay →    │ │
│  │  Fulfill → Review                        │ │
│  │  Each state node can trigger:            │ │
│  │  Recommend/Coupon/Reminder/Customer Svc  │ │
│  └──────────────────────────────────────────┘ │
└────────────────────────────────────────────┘
```

### TOGAF 4A Architecture Design

> The following 4A architecture design is based on industry practice inference, combined with the "Data Democratization" and "Distributed Technology" principles from the McKinsey Rewired methodology.

#### Business Architecture (BA)

**Core Business Process — Omni-Channel Customer Journey**:

```
Consumer Browse → Personalized Recommend → Add to Cart/Order → Smart Routing (Nearest Store/Optimal Warehouse) → Inventory Deduction
    │                                                                    │
    ├── Online Pay → In-Store Pickup (click-and-collect) ←── In-Store QR Pickup ←──────────┤
    ├── Online Pay → Express Delivery ─────────────────────────────────────────────────────┤
    └── In-Store Experience → Scan-to-Buy → Instant Takeaway ──────────────────────────────┘
                                       ↓
                              Consumer Sign-off/Pickup → Auto-Trigger Review → Member Points → Repurchase Recommendation
```

**Business Capability Map**:

| Capability Domain | L1 | L2 | L3 | Transformation Goal |
|--------|:---:|:---:|:---:|:---:|
| Customer Journey | Omni-Channel Experience | Journey Orchestration | Real-time Trigger/Personalization | From "Channel Silos" to "Unified Journey" |
| Customer Journey | Omni-Channel Experience | Member Loyalty | Unified Points/Tiers | Cross-channel member identity unification |
| Merchandise Management | Product Center | Category Management | Intelligent Category Optimization | Data-driven category decisions |
| Merchandise Management | Product Center | Price Management | Dynamic Pricing | AI-assisted pricing strategy |
| Order Management | Order Center | Order Fulfillment | Smart Routing | Optimal fulfillment based on cost and timeliness |
| Order Management | Order Center | After-Sales | Self-Service Returns | Omni-channel returns (return online orders in store) |
| Inventory Management | Inventory Center | Real-time Inventory | Omni-Channel Visibility | Online store inventory inquiry |
| Inventory Management | Inventory Center | Inventory Transfer | Intelligent Transfer | Demand forecast-driven transfer |
| Data Intelligence | Customer Insights | 360° Profile | Real-time Tagging | Unified CDP |
| Data Intelligence | Customer Insights | Personalization | 1:1 Recommendation | Real-time recommendation engine |

#### Application Architecture (AA)

**Microservice Decomposition Principles** (based on Rewired Distributed Technology Environment principles):
- By business capability boundary (Bounded Context), each bounded context corresponds to an independent team
- Database per Service, each team chooses its own technology independently
- Event-Driven first, achieving asynchronous decoupling via Kafka
- API-first design, each service provides standardized API contracts

**Service Inventory**:

| Service | Function | Database | Communication |
|------|------|--------|----------|
| customer-journey-service | Customer journey orchestration, trigger management | PostgreSQL | REST + Kafka |
| customer-profile-service | Customer 360° profile, tagging | MongoDB + Redis | Kafka |
| order-service | Orders/cart/order splitting | PostgreSQL | REST + Kafka |
| inventory-service | Real-time inventory/transfer | PostgreSQL + Redis | Kafka primarily |
| fulfillment-service | Fulfillment scheduling/routing | PostgreSQL | REST + Kafka |
| payment-service | Payment/refund | MySQL | REST + Kafka |
| recommendation-service | Personalized recommendation/A/B testing | MongoDB + Redis | REST |
| promotion-service | Promotion/coupon engine | MySQL | REST |
| notification-service | Message push (Push/SMS/Email) | MongoDB | Kafka |
| data-analytics | Data analytics/BI | StarRocks + ClickHouse | Kafka + CDC |

#### Data Architecture (DA)

**Data Productization Architecture** (based on Rewired "Data Product" concept):

| Layer | Description | Technology Selection (Inferred) | Data Timeliness |
|------|------|----------|:---:|
| L1 Data Sources | Business system databases + event tracking logs | PostgreSQL/MySQL + Tracking SDK | Real-time |
| L2 Data Ingestion | CDC + Log collection | Debezium + Kafka Connect + Flume | Seconds |
| L3 Data Lake | Raw data storage | OSS/MinIO + Apache Hudi | Minutes |
| L4 Data Warehouse | Analytical data | StarRocks + ClickHouse | Minutes |
| L5 Data Products | Data APIs consumable by business teams | CDP + Data API Gateway | Seconds |

**Data Domain Division**:

| Data Domain | Core Entities | Key Data Products |
|--------|----------|-------------|
| Customer Domain | Customer 360° profile, tags, segmentation | Customer Insights API, Segmentation Service |
| Transaction Domain | Orders, payments, refunds | Transaction Analytics API, Reconciliation Service |
| Merchandise Domain | SKU, price, inventory | Product Recommendation API, Inventory Inquiry Service |
| Supply Chain Domain | Procurement, warehousing, distribution | Fulfillment Tracking API, Cost Analysis Service |
| Behavior Domain | Browse, click, search, add-to-cart | Behavior Feature API, Intent Recognition Service |

#### Technology Architecture (TA)

**Key Technical Metrics**:

| Metric | Target | Description |
|------|--------|------|
| Order Creation TPS | ≥10,000 | Peak (during promotions) |
| Inventory Query QPS | ≥50,000 | Store + online concurrency |
| Recommendation Engine Latency | p99 ≤50ms | Real-time recommendation scenarios |
| Data Sync Latency | ≤1 second | Inventory/price |
| System Availability | ≥99.99% | Annual downtime <53 minutes |
| Customer Journey Trigger Latency | ≤500ms | Event trigger to action execution |

### Key Architecture Decisions (ADR)

| ADR No. | Decision | Approach | Rationale |
|---------|------|------|------|
| ADR-001 | Database Selection | PostgreSQL (primary) + MongoDB (profiles) + StarRocks (analytics) | PG supports JSON/geospatial, MongoDB suits document profiles, StarRocks for high-speed OLAP |
| ADR-002 | Caching Strategy | Redis Cluster + Local Caffeine | Two-level cache, p99<5ms, inventory queries via local cache |
| ADR-003 | Event-Driven Architecture | Apache Kafka + Event Sourcing | Decouple service dependencies, support customer journey state replay |
| ADR-004 | Service Mesh | Not introduced yet, K8s native first | Insufficient team scale, premature introduction adds complexity |
| ADR-005 | Data Sync | CDC (Debezium) + Kafka Connect | Real-time + reliability, replaces batch ETL |
| ADR-006 | Recommendation Engine | Self-developed + open-source models | Retail scenarios are highly customized, generic recommendation engines have limited effectiveness |

### Solution Differentiation Highlights

1. **Rewired Methodology-Driven**: Using McKinsey-validated "Rewired" six capabilities as the framework, ensuring the solution addresses not only technology but also talent, operating model, data democratization, and change management
2. **C4 Model Full-Layer Modeling**: From system context to component level, progressively layered, comprehensible and reviewable by the customer's IT team
3. **TOGAF 4A Architecture**: Business → Application → Data → Technology four-layer integration, ensuring solution completeness
4. **Quick Wins Strategy**: Starting with low-risk, high-visibility projects like click-and-collect to quickly build organizational confidence
5. **Change Management in Parallel**: For every $1 invested in technology development, $1 is allocated to change management (process redesign, user training, cultural transformation)
6. **ADR Decision Transparency**: Every key technology selection has clear rationale and alternatives, enhancing customer trust

### Deliverables List

| Deliverable | Type | Template |
|--------|------|------|
| Framework Solution HLD | .docx | hld-template.md |
| System Context Diagram (C1) | .drawio + .png | C4 Template |
| Container Diagram (C2) | .drawio + .png | C4 Template |
| Deployment Architecture Diagram | .drawio + .png | Deployment Architecture Template |
| Data Architecture Diagram | .drawio + .png | Data Architecture Template |
| Implementation Roadmap | .drawio + .png | Gantt Chart Template |
| Competitive Analysis Report | .docx | competitive-analysis-template.md |
| Bid Presentation PPT | .pptx | PPT Factory - Bid Presentation Template |
| Statement of Work | .docx | sow-template.md |

### Lessons Learned

1. **C4 Model is a Presales Communication Superweapon**: Non-technical stakeholders (CEO/CFO) view C1, technical stakeholders (CTO/Architects) view C2/C3
2. **TOGAF 4A is Not "Going Through the Motions"**: Four-layer architecture ensures the solution has no blind spots; during review, customers cannot find structural issues
3. **ADR Makes Technology Selection Evidence-Based**: The customer's technical team most often asks "Why choose X over Y?" — ADR answers this directly
4. **Quick Wins are Key to Building Trust**: Projects like click-and-collect have short cycles and high visibility, quickly proving transformation value
5. **Change Management Cannot Be Ignored**: The Rewired methodology emphasizes "for every $1 in development, allocate $1 for change management" — a purely technical proposal is destined to fail
6. **Incremental Migration Reduces Risk**: Customers fear "big bang" cutovers most; phased approach (Quick Wins → Scaling → Platform-based) reduces decision risk

---## Case C02: Dell Supply Chain Digital Transformation Solution

### Scenario Background

> **Real Case Source**: The core data and framework of this case come from the MIT Center for Transportation & Logistics (MIT CTL) public research project "Dell's Digital Supply Chain Transformation", and the Ivey Publishing case "Dell: Roadmap of a Digital Supply Chain Transformation" (Authors: Sáenz, M. J., Borrella, I., & Revilla, E.). This case is one of Ivey Publishing's best-selling supply chain management cases, widely used in graduate and executive education programs at business schools worldwide. Core data — AI-driven E2E orchestration, 2x decision speed, 50% reduction in aged inventory, 40%+ productivity improvement, 77% reduction in hard drive shortages — all come from MIT CTL's publicly available research findings.

Dell Technologies is one of the world's largest technology companies, with annual order volume exceeding 63 million, daily shipments exceeding 84,000 units, 130,000 employees globally, and managing over 2,700 internal applications. Its supply chain complexity is extremely high: multiple global factories, multiple product lines, multiple configuration combinations (configure-to-order CTO model), and facing extreme challenges such as post-pandemic global chip shortages and logistics disruptions.

Dell's supply chain digital transformation core objectives:
- Shift from "human experience-driven" to "AI + data-driven" end-to-end (E2E) supply chain orchestration
- Improve decision speed and quality to cope with increasingly frequent supply chain disruptions
- Reduce aged inventory and improve capital efficiency
- Achieve full supply chain transparency and predictability

### Customer Material Analysis

**RFP Key Information Extraction**:

| Dimension | Customer Requirements | Implicit Needs (SPIN Discovery) |
|------|----------|---------------------|
| Business Goals | E2E supply chain visualization, automated decision-making | Supply chain transforms from "cost center" to "competitive advantage" |
| Technology Goals | AI/ML-driven forecasting and orchestration | Upgrade from "report-style BI" to "real-time intelligent decision-making" |
| Data Goals | Full-chain data integration, unified data foundation | Break down data silos between SAP, WMS, TMS and other systems |
| Organizational Goals | Supply chain team digital capability enhancement | From "Excel + experience" to "data + AI-assisted decision-making" |
| Resilience Goals | Rapid response to supply chain disruptions | From "reactive response" to "proactive prediction + automated response" |

**Competitive Intelligence** (based on industry practice inference):

| Competitor | Solution Positioning | Strengths | Weaknesses |
|------|----------|------|------|
| Major Cloud Provider A | Cloud-native supply chain platform | Complete technology ecosystem, strong AI/ML capabilities | Insufficient depth in manufacturing supply chain |
| ERP Vendor B | Integrated supply chain suite | Deep integration with existing ERP | Closed architecture, slow innovation pace |
| Specialist SCM Vendor C | Best-practice supply chain solution | Deep industry know-how | Relatively traditional technology architecture |

### Transformation Methodology: Dell E2E Digital Supply Chain Transformation Roadmap

> The following transformation framework is based on research findings from MIT CTL and Ivey Publishing public cases. Specific solution details are based on industry practice inference.

**Four Phases of Dell's Supply Chain Digital Transformation**:

```
Phase 1: Visibility
  ├── Full-chain data integration (SAP + WMS + TMS + Supplier systems)
  ├── Unified data foundation (Data Lake + Data Warehouse)
  └── Real-time supply chain visualization dashboard

Phase 2: Predictive
  ├── AI/ML demand forecasting models
  ├── Supply chain disruption early warning system
  ├── Inventory health scorecard
  └── Long-term forecast accuracy improvement of 5-15%

Phase 3: Automation
  ├── Quarterly automated operations exceeding 5,000
  ├── Automated replenishment, automated transfer
  ├── Automatic anomaly detection and alerting
  └── Decision speed improved by 2x

Phase 4: Orchestration
  ├── AI-driven E2E supply chain orchestration
  ├── Multi-objective optimization (cost/timeliness/resilience)
  ├── Supply chain digital twin
  └── Autonomous Decision-Making
```

**Core Quantified Results** (Source: MIT CTL Public Research Data):

| Metric | Result | Description |
|------|------|------|
| Decision Speed | 2x improvement | AI-assisted decision-making vs. manual decision-making |
| Aged Inventory | 50% reduction | Improved capital efficiency |
| Productivity | 40%+ improvement | Automation + AI assistance |
| Hard Drive Shortages | 77% reduction | Significantly enhanced supply chain resilience |
| Long-term Forecast Accuracy | 5-15% improvement | ML models vs. traditional statistical methods |
| Automated Operations Volume | 5,000+ per quarter | Process automation |

### C4 Model Architecture Modeling

> The following architecture design is based on industry practice inference, referencing the E2E orchestration framework described in the MIT CTL public case.

#### Level 1: System Context Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                   Dell E2E Digital Supply Chain Platform          │
│                                                                   │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐      │
│  │ Suppliers │   │ Factory/  │   │ Logistics │   │ Customers│      │
│  │(Supplier  │   │ ODM       │   │ Carriers  │   │(Order    │      │
│  │ Portal)   │   │(MES/WMS)  │   │(TMS Link) │   │ Tracking) │      │
│  └─────┬─────┘   └─────┬─────┘   └─────┬─────┘   └─────┬─────┘      │
│        │               │               │               │            │
│        ▼               ▼               ▼               ▼            │
│  ┌─────────────────────────────────────────────────────────┐      │
│  │            E2E Digital Supply Chain Platform (Core)       │      │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐        │      │
│  │  │Demand    │ │Supply    │ │Fulfillment│ │Risk      │        │      │
│  │  │Sensing   │ │Planning  │ │Orchestration│ │Intelligence│     │      │
│  │  │Engine    │ │Engine    │ │Engine    │ │Engine    │        │      │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘        │      │
│  └─────────────────────────────────────────────────────────┘      │
│        │               │               │               │            │
│        ▼               ▼               ▼               ▼            │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐      │
│  │ ERP(SAP) │   │ Data Lake/│   │ AI/ML     │   │ External  │      │
│  │          │   │ Warehouse │   │ Platform  │   │ Data      │      │
│  │          │   │          │   │          │   │(Weather/  │      │
│  │          │   │          │   │          │   │ Geopolitics)│     │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

#### Level 2: Container Diagram — Core System

| Container | Type | Tech Stack (Inferred) | Responsibility |
|------|------|--------|------|
| API Gateway | Gateway | Kong/APISIX | Unified entry, rate limiting, authentication |
| Demand Sensing Engine | Microservice + AI | Python + TensorFlow + PostgreSQL | Demand forecasting, anomaly detection, trend analysis |
| Supply Planning Engine | Microservice | Java + PostgreSQL | Supply planning, capacity planning, material requirements |
| Fulfillment Orchestration Engine | Microservice | Go + Redis + PostgreSQL | Order routing, fulfillment scheduling, multi-objective optimization |
| Risk Intelligence Engine | AI Service | Python + Kafka Streams | Disruption early warning, impact analysis, alternative recommendation |
| Data Lake/Warehouse | Data Platform | OSS + StarRocks + Hudi | Full-chain data storage and analytics |
| Digital Twin | Simulation Platform | Python + AnyLogic | Supply chain simulation, what-if analysis |
| Message Middleware | Infrastructure | Apache Kafka | Event-driven, real-time data streams |
| Automation Engine | Infrastructure | Temporal/Cadence | Workflow orchestration, automated operation execution |

#### Level 3: Component Diagram — Fulfillment Orchestration Engine

```
Fulfillment Orchestration Engine Internal Components:
┌────────────────────────────────────────────┐
│              Fulfillment Orchestration Engine │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Order     │  │ Inventory │  │ Route     │  │
│  │ Router    │  │ Allocator │  │ Optimizer │  │
│  │ - Order   │  │ - Inventory│ │ - Cost    │  │
│  │   Parsing │  │   Query   │  │   Calc    │  │
│  │ - Rule    │  │ - Inventory│ │ - Timeliness│ │
│  │   Matching│  │   Reserve │  │   Calc    │  │
│  │ - Priority│  │ - Alternative│ - Carbon  │  │
│  │          │  │   Recommend│  │   Emission│  │
│  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  │
│        │              │              │         │
│        ▼              ▼              ▼         │
│  ┌──────────────────────────────────────────┐ │
│  │      Multi-Objective Optimization Solver   │ │
│  │   Lowest Cost ↔ Optimal Timeliness ↔      │ │
│  │   Highest Resilience                      │ │
│  │   Constraints: Inventory/Capacity/        │ │
│  │   Transport/Compliance/Carbon Emission    │ │
│  └──────────────────────────────────────────┘ │
└────────────────────────────────────────────┘
```

### TOGAF 4A Architecture Design

> The following 4A architecture design is based on industry practice inference.

#### Business Architecture (BA)

**Core Business Process — E2E Supply Chain**:

```
Demand Sensing → Supply Planning → Procurement Execution → Manufacturing/Assembly → Global Logistics → Last Mile → Customer Delivery
    │           │           │           │           │           │
    ▼           ▼           ▼           ▼           ▼           ▼
  AI Forecast  AI Optimize  Auto PO     Capacity    Route       Real-time
  Anomaly      Inventory    Supplier    Optimize    Optimize    Tracking
  Detection    Health       Collaboration           Disruption  ETA Prediction
                                                Early Warning
```

**Business Capability Map**:

| Capability Domain | L1 | L2 | L3 | Digital Goal |
|--------|:---:|:---:|:---:|:---:|
| Demand Management | Demand Forecasting | Statistical Forecasting | AI/ML Forecasting | Accuracy improvement of 5-15% |
| Demand Management | Demand Sensing | Real-time Signal Capture | External Data Fusion | Sense changes 2-4 weeks in advance |
| Supply Management | Supply Planning | Capacity Planning | Constraint Optimization | Global optimum rather than local optimum |
| Supply Management | Inventory Management | Inventory Optimization | Dynamic Safety Stock | Aged inventory reduced by 50% |
| Fulfillment Management | Order Fulfillment | Order Routing | Multi-Objective Optimization | Decision speed improved by 2x |
| Fulfillment Management | Logistics Management | Route Optimization | Real-time Re-planning | Disruption response from "days" to "minutes" |
| Risk Management | Disruption Early Warning | Event Monitoring | AI Prediction | Hard drive shortages reduced by 77% |
| Risk Management | Resilience Planning | Contingency Planning | Digital Twin Simulation | What-if analysis automated |

#### Application Architecture (AA)

**Service Inventory**:

| Service | Function | Database | Communication |
|------|------|--------|----------|
| demand-sensing-service | Demand forecasting, anomaly detection | PostgreSQL + ML Model Store | REST + Kafka |
| supply-planning-service | Supply planning, capacity planning | PostgreSQL | REST + Kafka |
| inventory-optimization-service | Inventory optimization, safety stock calculation | PostgreSQL + Redis | Kafka primarily |
| fulfillment-orchestration-service | Fulfillment orchestration, multi-objective optimization | PostgreSQL + Redis | REST + Kafka |
| risk-intelligence-service | Disruption early warning, impact analysis | MongoDB + Kafka Streams | Kafka |
| supplier-collaboration-service | Supplier collaboration, PO management | PostgreSQL | REST + Kafka |
| logistics-visibility-service | Logistics visualization, ETA prediction | MongoDB + Redis | Kafka |
| automation-engine | Workflow orchestration, automated execution | PostgreSQL | Kafka + Temporal |
| digital-twin-service | Supply chain simulation, what-if analysis | PostgreSQL + Simulation Engine | REST |

#### Data Architecture (DA)

**Supply Chain Data Layering**:

| Layer | Description | Technology Selection (Inferred) | Data Timeliness |
|------|------|----------|:---:|
| L1 Data Sources | SAP + WMS + TMS + MES + Supplier systems | Multi-source heterogeneous | Real-time |
| L2 Data Ingestion | CDC + API + EDI + IoT | Debezium + Kafka Connect | Seconds |
| L3 Data Lake | Raw data + semi-structured data | OSS + Apache Hudi | Minutes |
| L4 Data Warehouse | Structured analytical data | StarRocks + ClickHouse | Minutes |
| L5 Data Services | Supply chain data APIs + real-time dashboards | GraphQL + Grafana | Seconds |

**Data Domain Division**:

| Data Domain | Core Entities | Key Data Products |
|--------|----------|-------------|
| Demand Domain | Orders, forecasts, trends | Demand Forecast API, Anomaly Detection Service |
| Supply Domain | Capacity, materials, BOM | Supply Constraint API, Material Risk Service |
| Inventory Domain | Inventory levels, aging, turnover | Inventory Health API, Replenishment Recommendation Service |
| Logistics Domain | Waybills, trajectories, timeliness | Logistics Visibility API, ETA Prediction Service |
| Risk Domain | Disruption events, impact assessment | Risk Early Warning API, Resilience Scoring Service |

#### Technology Architecture (TA)

**Key Technical Metrics**:

| Metric | Target | Description |
|------|--------|------|
| Decision Latency | ≤1 minute | Automated decision scenarios |
| Data Sync Latency | ≤5 seconds | Full-chain data |
| Forecast Refresh Frequency | Daily/Hourly | Demand forecast updates |
| System Availability | ≥99.95% | Supply chain systems |
| Automated Operation Throughput | ≥5,000/quarter | Automation engine |
| Digital Twin Simulation Speed | ≤30 minutes | Single what-if analysis |

### Key Architecture Decisions (ADR)

| ADR No. | Decision | Approach | Rationale |
|---------|------|------|------|
| ADR-001 | Data Foundation | Data Lake (Hudi) + Data Warehouse (StarRocks) | Supports both batch and real-time analytics, Hudi supports incremental updates |
| ADR-002 | Event-Driven | Apache Kafka + Event Sourcing | Supply chain events are naturally asynchronous, event sourcing supports full audit |
| ADR-003 | Automation Engine | Temporal (workflow orchestration) | Long-running supply chain workflows require a reliable orchestration engine |
| ADR-004 | AI/ML Platform | MLflow + proprietary models | Model version management, A/B experimentation, model monitoring integration |
| ADR-005 | Digital Twin | AnyLogic + proprietary simulation engine | Supports discrete event simulation and agent-based modeling |
| ADR-006 | Supplier Collaboration | API-first + EDI compatible | Large suppliers via API, long-tail suppliers retain EDI |

### Solution Differentiation Highlights

1. **Real Validated Quantified Results**: MIT CTL publicly researched and validated quantified results — 2x decision speed, 50% reduction in aged inventory, 40%+ productivity improvement, 77% reduction in hard drive shortages
2. **C4 Model Full-Layer Modeling**: From system context to component level, progressively layered
3. **TOGAF 4A Architecture**: Business → Application → Data → Technology four-layer integration
4. **E2E Orchestration Rather Than Point Optimization**: From "functional digitization" to "global intelligent orchestration", avoiding the trap of local optima
5. **Digital Twin + What-if Analysis**: Before making actual decisions, simulate and validate in the digital twin first
6. **ADR Decision Transparency**: Every key technology selection has clear rationale and alternatives

### Deliverables List

| Deliverable | Type | Template |
|--------|------|------|
| Framework Solution HLD | .docx | hld-template.md |
| System Context Diagram (C1) | .drawio + .png | C4 Template |
| Container Diagram (C2) | .drawio + .png | C4 Template |
| Deployment Architecture Diagram | .drawio + .png | Deployment Architecture Template |
| Data Architecture Diagram | .drawio + .png | Data Architecture Template |
| Implementation Roadmap | .drawio + .png | Gantt Chart Template |
| Competitive Analysis Report | .docx | competitive-analysis-template.md |
| Bid Presentation PPT | .pptx | PPT Factory - Bid Presentation Template |
| Statement of Work | .docx | sow-template.md |

### Lessons Learned

1. **Visibility is the First Step**: Before achieving AI orchestration, full-chain data must first be integrated to achieve end-to-end visibility
2. **Four Phases Cannot Be Skipped**: Visibility → Predictive → Automation → Orchestration, each phase builds on the data and capability foundation of the previous phase
3. **Automation Does Not Replace People, It Augments Them**: Dell's experience is "AI-assisted decision-making" rather than "AI-replacing decision-making", with humans retaining final decision authority
4. **Digital Twin is a Decision Accelerator**: Before making actual decisions, simulate and validate in the digital twin first, significantly reducing decision risk
5. **Quantified Results are the Most Persuasive Weapon**: MIT CTL's publicly available quantified data (2x decision speed, 50% reduction in aged inventory, etc.) is more persuasive than any methodology description
6. **C4 Model Makes Complex Supply Chain Architecture Comprehensible**: C1 for CXOs to see the big picture, C2 for architects to see containers, C3 for development teams to see components

---

## Sources

### Case C01 Sources

1. Lamarre, E., Smaje, K., & Zemmel, R. (2023). *Rewired: The McKinsey Guide to Outcompeting in the Age of Digital and AI*. Wiley. ISBN: 9781394207114.
   - Source: https://www.mckinsey.com/featured-insights/mckinsey-on-books/rewired-first-edition

2. McKinsey & Company. "Rewired in action: Tech & AI transformations."
   - Source: https://www.mckinsey.com/capabilities/tech-and-ai/how-we-help-clients/rewired-in-action

3. McKinsey & Company. "What is digital transformation?" (2024).
   - Source: https://www.mckinsey.com/featured-insights/mckinsey-explainers/what-is-digital-transformation

4. soreno.ai. Public analysis article on McKinsey's implementation of digital transformation for a large retailer (citing McKinsey "Rewired" methodology).
   - Core content: Shifting from product-centric to customer-centric omni-channel transformation, data-driven customer journey mapping, quick wins (click-and-collect) to build trust, change management and technology implementation in parallel.

### Case C02 Sources

1. MIT Center for Transportation & Logistics. "Dell's Digital Supply Chain Transformation."
   - Source: https://digitalsc.mit.edu/dells-digital-supply-chain-transformation/
   - Core data: AI-driven E2E orchestration, automated operations exceeding 5,000/quarter, aged inventory reduced by 50%, decision speed improved by 2x, long-term forecast accuracy improved by 5-15%, hard drive shortages reduced by 77%, productivity improved by 40%+.

2. MIT Center for Transportation & Logistics. "Dell: Roadmap of a Digital Supply Chain Transformation."
   - Source: https://digitalsc.mit.edu/roadmap-of-a-digital-supply-chain-transformation/

3. Sáenz, M. J., Borrella, I., & Revilla, E. *Dell Technologies: Automation for the End-to-End Supply Chain*. Ivey Publishing.
   - Source: https://www.thecasecentre.org/products/view?id=213098
   - Note: This case is one of Ivey Publishing's best-selling supply chain management cases, widely used in graduate and executive education programs at business schools worldwide.

4. ResearchGate. "Dell: Roadmap of a digital supply chain transformation." (2021).
   - Source: https://www.researchgate.net/publication/357535962_Dell_Roadmap_of_a_digital_supply_chain_transformation

### Disclaimer

- The **competitive analysis**, **specific solution details**, **technology selection**, and **architecture design** in this case library, except for the content explicitly cited above, are all constructed based on industry practice inference and presales methodology frameworks (C4 Model, TOGAF 4A, SPIN, ADR).
- This case library does not represent any real customer's internal information or non-public data.
- This case library is for presales solution learning and reference only, and does not constitute any commercial advice or commitment.
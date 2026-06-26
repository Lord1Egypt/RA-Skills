# ABAP Cloud Development Reference

## Overview

ABAP Cloud is SAP's cloud-ready development model for building extensible, maintainable applications in the SAP BTP ABAP Environment.

## Foundational Technologies

| Technology | Purpose |
|------------|---------|
| Core Data Services (CDS) | Data modeling, integrated analytics |
| ABAP RESTful Application Programming Model (RAP) | Service-oriented application development |
| Restricted ABAP Language | Cloud-safe development through controlled API access |
| Released Public APIs | Upgrade-stable extensions |

## Development Environment

**Primary IDE**: ABAP Development Tools for Eclipse (ADT)

**Additional Tools:**
- ABAP Test Cockpit (ATC) - Static analysis
- ABAP Unit - Dynamic testing
- SAP Fiori Launchpad - UI deployment

## Application Development Process

### 6-Step Development Workflow

| Step | Activity | Details |
|------|----------|---------|
| 1 | **Model the Domain** | Define domain-specific data models aligned with RAP architecture |
| 2 | **Implement Business Behavior** | Add validations, determinations, actions, consistency management |
| 3 | **Expose Services** | Define and bind services via OData |
| 4 | **Secure Access** | Configure authorization, assign proper scopes and roles |
| 5 | **Build the UI** | Develop SAP Fiori applications consuming services |
| 6 | **Ensure Quality** | Add automated tests and static checks |

### Development Approaches

**Develop from Scratch:**
- Build new applications and services using RAP blueprint
- Domain-specific data models with extensibility built-in

**Extend Existing Services:**
- Extend SAP or custom services in upgrade-safe way
- Opt-in extensibility: original data models must explicitly enable each option

### S/4HANA Extension Options

| Type | Description | Use Case |
|------|-------------|----------|
| **On-Stack** | Extensions run within S/4HANA Cloud, share database and lifecycle | Tight integration, key-user extensibility (low-code), developer extensibility (pro-code) |
| **Side-by-Side** | Extensions run on SAP BTP with separate runtime and lifecycle | Loosely coupled solutions, partner offerings, hub scenarios |

### Test Strategy

**Automated Testing** is essential for reliability, stability, and quality:

- **Unit Tests**: ABAP Unit for functional correctness
- **Integration Tests**: Cross-component validation
- **Static Analysis**: ABAP Test Cockpit (ATC)

### Development Recommendations

1. Connect ABAP Cloud systems to Eclipse with ABAP Development Tools
2. Build OData services using RAP optimized for SAP HANA Cloud
3. Perform static code analysis with ATC including Code Vulnerability Analyzer
4. Use central ATC on SAP BTP for custom code governance
5. Leverage the Analyze Custom Code application for code inspection

## Model-Driven Architecture

### Three-Tier Structure
1. **Data Access Layer** - Database tables, CDS views
2. **Domain Model Layer** - Business logic, validations
3. **Service Exposure Layer** - OData services, Web APIs

### Benefits
- Faster delivery via standardized stacks
- Interoperability through consistent rules
- Multipurpose CDS models (transactional + analytical)

## CDS Data Modeling

### Basic Entity Definition
```abap
@EndUserText.label: 'Travel'
@AccessControl.authorizationCheck: #NOT_REQUIRED
define root view entity ZI_Travel
  as select from ztravel
{
  key travel_uuid       as TravelUUID,
      travel_id         as TravelID,
      agency_id         as AgencyID,
      customer_id       as CustomerID,
      begin_date        as BeginDate,
      end_date          as EndDate,
      booking_fee       as BookingFee,
      total_price       as TotalPrice,
      currency_code     as CurrencyCode,
      description       as Description,
      overall_status    as OverallStatus,
      @Semantics.user.createdBy: true
      created_by        as CreatedBy,
      @Semantics.systemDateTime.createdAt: true
      created_at        as CreatedAt,
      @Semantics.user.lastChangedBy: true
      last_changed_by   as LastChangedBy,
      @Semantics.systemDateTime.lastChangedAt: true
      last_changed_at   as LastChangedAt
}
```

### Projection View for UI
```abap
@EndUserText.label: 'Travel Projection'
@AccessControl.authorizationCheck: #NOT_REQUIRED
@Metadata.allowExtensions: true
define root view entity ZC_Travel
  provider contract transactional_query
  as projection on ZI_Travel
{
  key TravelUUID,
      TravelID,
      AgencyID,
      CustomerID,
      BeginDate,
      EndDate,
      BookingFee,
      TotalPrice,
      CurrencyCode,
      Description,
      OverallStatus,
      CreatedBy,
      CreatedAt,
      LastChangedBy,
      LastChangedAt
}
```

## RAP Business Object Definition

### Behavior Definition
```abap
managed implementation in class zbp_i_travel unique;
strict ( 2 );

define behavior for ZI_Travel alias Travel
persistent table ztravel
lock master
authorization master ( instance )
etag master LastChangedAt
{
  // Standard operations
  create;
  update;
  delete;

  // Field controls
  field ( readonly ) TravelUUID, TravelID, CreatedBy, CreatedAt, LastChangedBy, LastChangedAt;
  field ( mandatory ) AgencyID, CustomerID;

  // Determinations
  determination setTravelID on modify { create; }
  determination calculateTotalPrice on modify { field BookingFee; }

  // Validations
  validation validateCustomer on save { field CustomerID; }
  validation validateDates on save { field BeginDate, EndDate; }

  // Actions
  action acceptTravel result [1] $self;
  action rejectTravel result [1] $self;

  // Factory action
  factory action copyTravel [1];

  // Draft handling
  draft action Edit;
  draft action Activate optimized;
  draft action Discard;
  draft action Resume;
  draft determine action Prepare;
}
```

### Behavior Implementation
```abap
CLASS zbp_i_travel DEFINITION PUBLIC ABSTRACT FINAL
  FOR BEHAVIOR OF zi_travel.
ENDCLASS.

CLASS zbp_i_travel IMPLEMENTATION.

  METHOD setTravelID.
    " Get max Travel ID
    SELECT MAX( travel_id ) FROM ztravel INTO @DATA(lv_max_id).

    " Set Travel ID for new entities
    MODIFY ENTITIES OF zi_travel IN LOCAL MODE
      ENTITY Travel
        UPDATE FIELDS ( TravelID )
        WITH VALUE #( FOR key IN keys
          ( %tky = key-%tky
            TravelID = lv_max_id + 1 ) ).
  ENDMETHOD.

  METHOD validateDates.
    READ ENTITIES OF zi_travel IN LOCAL MODE
      ENTITY Travel
        FIELDS ( BeginDate EndDate )
        WITH CORRESPONDING #( keys )
      RESULT DATA(lt_travels).

    LOOP AT lt_travels INTO DATA(ls_travel).
      IF ls_travel-BeginDate > ls_travel-EndDate.
        APPEND VALUE #( %tky = ls_travel-%tky ) TO failed-travel.
        APPEND VALUE #( %tky = ls_travel-%tky
                        %msg = new_message_with_text(
                          severity = if_abap_behv_message=>severity-error
                          text = 'End date must be after begin date' )
                      ) TO reported-travel.
      ENDIF.
    ENDLOOP.
  ENDMETHOD.

ENDCLASS.
```

## Service Definition and Binding

### Service Definition
```abap
@EndUserText.label: 'Travel Service Definition'
define service ZUI_TRAVEL_O4 {
  expose ZC_Travel as Travel;
}
```

### Service Binding
Create via ADT: OData V4 - UI binding type

## Extensibility Options

### Developer Extensibility
- Custom fields and nodes
- Custom business logic
- ABAP Development Tools required

### Key User Extensibility (Multitenant SaaS)
- UI adaptations
- Custom fields
- Business Add-Ins (BAdIs)
- No coding required

## Reuse Services

Pre-built building blocks available:
- Application Jobs
- Application Logging
- Forms (Adobe Document Services)
- Emails
- Change Documents
- Workflow (SAP Build Process Automation)
- Number Ranges

## Transport Mechanisms

### gCTS (Recommended)
- Modern transport for BTP systems within same global account
- Managed via "Manage Software Components" app
- Automatic Git repository management

### abapGit
- Open-source Git client
- Use cases:
  - Migrate on-premise code to cloud
  - System decommissioning (export/import)
  - Cross-account code transfers
- **Not recommended** for standard production transports

## Quality Assurance

### ABAP Test Cockpit (ATC)

**Default Variant**: `ABAP_CLOUD_DEVELOPMENT_DEFAULT`

**Check Categories:**
- Approved enhancement technologies
- API usage governance
- Critical ABAP statement analysis
- Code Vulnerability Analyzer (optional)

**Blocking Mode:**
Configure to prevent Priority 1/2 findings from transport

### ABAP Unit Testing
```abap
CLASS ltcl_travel DEFINITION FINAL FOR TESTING
  DURATION SHORT
  RISK LEVEL HARMLESS.

  PRIVATE SECTION.
    DATA: mo_cut TYPE REF TO zcl_travel_handler.

    METHODS setup.
    METHODS test_date_validation FOR TESTING.
ENDCLASS.

CLASS ltcl_travel IMPLEMENTATION.

  METHOD setup.
    mo_cut = NEW #( ).
  ENDMETHOD.

  METHOD test_date_validation.
    " Given
    DATA(lv_begin) = cl_abap_context_info=>get_system_date( ).
    DATA(lv_end) = lv_begin + 7.

    " When
    DATA(lv_valid) = mo_cut->validate_dates(
      iv_begin = lv_begin
      iv_end = lv_end
    ).

    " Then
    cl_abap_unit_assert=>assert_true( lv_valid ).
  ENDMETHOD.

ENDCLASS.
```

## Elastic Scaling

### ABAP Compute Units (ACUs)
- Manual scaling via BTP Cockpit
- Automatic elastic scaling (0.5 ACU increments)
- Metrics: CPU, memory, work process counts

### HANA Compute Units (HCUs)
- Manual adjustment with near-zero downtime
- Native Storage Extension for cost optimization

## System Hibernation

**Benefits:**
- Reduces costs to <5% of operational expenses
- Preserves HANA Cloud instance
- Automatic restart during scheduled maintenance

**Management:**
- Via Landscape Portal
- Scheduling available (except trial accounts)

## SAP Joule Integration

**AI Capabilities:**
1. Predictive code completion
2. Joule chat (natural language)
3. Code explanation
4. ABAP Unit generation
5. CDS test generation

**ABAP AI SDK:**
- Standardized access to language models on SAP AI Core
- Intelligent Scenario Lifecycle Management

## Partner Deployment Models

### Multitenant SaaS
- Cloud service in partner's global account
- Customers subscribe
- Partner manages operations
- Key user extensibility for customers

### Add-on Product
- Installed in customer's ABAP environment
- Customer manages lifecycle
- Developer extensibility available
- Requires SAP PartnerEdge Build contract

### Requirements
- Registered ABAP namespace (mandatory)
- Software Components for transport
- Landscape Portal for lifecycle management

## Upgrade Management

### Downtime-Optimized Upgrades
1. **Preparation**: New release in shadow layer (system available)
2. **Takeover**: 10-40 minutes downtime
3. **Postprocessing**: Background cleanup (system available)

### Pre-Upgrade Option
- Test on non-production 4 weeks before release
- Validate custom applications
- Report issues through SAP support

## Source Documentation

- ABAP Environment: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/sap-btp-abap-environment-with-abap-cloud-174b229.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/sap-btp-abap-environment-with-abap-cloud-174b229.md)
- ABAP Cloud Development: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/developing-with-abap-cloud-in-the-sap-btp-abap-environment-9aaaf65.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/developing-with-abap-cloud-in-the-sap-btp-abap-environment-9aaaf65.md)
- Elastic Scaling: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/benefit-from-the-elastic-scaling-of-abap-application-servers-c1d35c5.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/benefit-from-the-elastic-scaling-of-abap-application-servers-c1d35c5.md)
- System Hibernation: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/use-system-hibernation-6a8d7ee.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/use-system-hibernation-6a8d7ee.md)
- ATC Governance: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/keep-clean-core-governance-with-abap-test-cockpit-698ddfa.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/keep-clean-core-governance-with-abap-test-cockpit-698ddfa.md)
- Joule: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/use-joule-for-developers-generative-ai-in-abap-cloud-63c8ac1.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/use-joule-for-developers-generative-ai-in-abap-cloud-63c8ac1.md)

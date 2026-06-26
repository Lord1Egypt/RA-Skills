# SAP BTP UX Design Reference

## Overview

SAP BTP applications require consistent, compliant user experiences using the SAP Fiori design language. Three main approaches are recommended for UI development.

## User Experience Dimensions

### Five Usability Factors

| Factor | Description |
|--------|-------------|
| Effectiveness | Accomplishing intended tasks |
| Efficiency | Minimizing effort required |
| Ease of learning | Intuitiveness for new users |
| Error tolerance | Handling mistakes gracefully |
| Satisfaction | Positive user perception |

### Consistency

Consistency contributes to ease of learning and efficiency. Follow SAP Fiori Design Guidelines to maintain alignment with standard SAP applications.

## UI Development Approaches

### 1. SAP Fiori Elements

**Description**: Framework on top of SAPUI5 with predefined templates based on OData services

**Best For**: Standard business applications

#### Floorplans

| Floorplan | Use Case |
|-----------|----------|
| List Report | Data browsing with filters |
| Object Page | Detail view with sections |
| Overview Page | KPIs and quick actions |
| Worklist | Task-oriented lists |
| Analytical List Page | Analytics with filters |

#### Building Blocks

Reusable UI components:
- Data visualization
- Form entry
- Value helps
- Tables
- Charts

#### Benefits
- Rapid development
- Consistent UX
- Automatic compliance
- Responsive design

### 2. Flexible Programming Model

**Description**: Extend SAP Fiori Elements with custom logic

**Best For**: Applications needing selective customization

#### Extension Points
- Custom columns
- Custom actions
- Custom sections
- Custom fragments

#### Custom Pages
Leverage Fiori Elements base with:
- Building blocks
- Routing
- State management

### 3. Freestyle SAPUI5

**Description**: Full UI control using SAPUI5 framework

**Best For**: Highly customized interfaces

**Considerations**:
- Greater development effort
- Manual compliance implementation
- Full flexibility

## SAP Fiori Tools

| Tool | Purpose |
|------|---------|
| Application Wizard | Generate Fiori apps from templates |
| Service Modeler | Design OData services visually |
| Page Editor | Configure Fiori Elements pages |
| XML Editor | Edit view definitions |
| Guided Development | Step-by-step feature addition |

## Compliance Standards

### Automatic Inheritance

> **Note**: Automatic compliance applies specifically when using **SAP Fiori Elements** with recommended patterns, **OData V4** services with proper annotations, and **internationalization (i18n)** setup. Custom or Freestyle SAPUI5 applications require manual compliance verification.

**Prerequisites for automatic compliance:**
1. Use SAP Fiori Elements floorplans
2. Expose OData V4 services with proper UI annotations
3. Enable internationalization (i18n) for all user-facing text
4. Follow SAP Fiori design guidelines for customizations

| Standard | Coverage | Requirement |
|----------|----------|-------------|
| Accessibility (WCAG 2.2) | Automatic | Fiori Elements + proper labels |
| SAP Fiori Design Guidelines | Automatic | Standard floorplans |
| Responsive Design | Automatic | Fiori Elements controls |
| Performance Optimization | Automatic | OData V4 batching |
| Security Protections | Automatic | XSUAA + CSRF tokens |

### Accessibility Requirements

```xml
<!-- Example: Accessible form -->
<Label text="Name" labelFor="nameInput"/>
<Input id="nameInput" value="{/name}"
       ariaLabelledBy="nameLabel"/>
```

### Internationalization

```javascript
// i18n/i18n.properties
welcomeMessage=Welcome to the Application
saveButton=Save
cancelButton=Cancel

// i18n/i18n_de.properties
welcomeMessage=Willkommen in der Anwendung
saveButton=Speichern
cancelButton=Abbrechen
```

## Design Methodology

### Iterative Approach

**Motto**: "Fail fast, fail early"

**Process**:
1. Sketch solutions
2. Gather feedback
3. Refine designs
4. Repeat until needs met

### User Research

**Methods**:
- Stakeholder interviews
- Contextual inquiry
- Usability testing
- A/B testing

**Resources**: SAP User Research Resources guide

## Fiori Elements Configuration

### annotations.cds

```cds
using CatalogService as service from '../srv/catalog-service';

annotate service.Books with @(
  UI: {
    SelectionFields: [title, author_ID],
    LineItem: [
      { Value: title },
      { Value: author.name, Label: 'Author' },
      { Value: stock },
      { Value: price }
    ],
    HeaderInfo: {
      TypeName: 'Book',
      TypeNamePlural: 'Books',
      Title: { Value: title },
      Description: { Value: author.name }
    },
    Facets: [
      {
        $Type: 'UI.ReferenceFacet',
        Label: 'General Information',
        Target: '@UI.FieldGroup#GeneralInfo'
      }
    ],
    FieldGroup#GeneralInfo: {
      Data: [
        { Value: title },
        { Value: author_ID },
        { Value: stock },
        { Value: price }
      ]
    }
  }
);
```

### manifest.json Routing

```json
{
  "sap.ui5": {
    "routing": {
      "routes": [
        {
          "name": "BooksList",
          "pattern": ":?query:",
          "target": "BooksList"
        },
        {
          "name": "BooksDetail",
          "pattern": "Books({key}):?query:",
          "target": "BooksDetail"
        }
      ],
      "targets": {
        "BooksList": {
          "type": "Component",
          "id": "BooksList",
          "name": "sap.fe.templates.ListReport"
        },
        "BooksDetail": {
          "type": "Component",
          "id": "BooksDetail",
          "name": "sap.fe.templates.ObjectPage"
        }
      }
    }
  }
}
```

## Responsive Design

### Breakpoints

| Size | Width | Typical Device |
|------|-------|----------------|
| Phone | < 600px | Mobile |
| Tablet | 600-1024px | Tablet |
| Desktop | > 1024px | Desktop |

### Responsive Handling

```xml
<FlexBox direction="Column"
         class="sapUiResponsiveMargin">
  <Table growing="true"
         growingThreshold="20"
         mode="{= ${device>/system/phone} ? 'None' : 'SingleSelectMaster'}">
  </Table>
</FlexBox>
```

## Resources

| Resource | URL |
|----------|-----|
| SAP Fiori Design Guidelines | [https://experience.sap.com/fiori-design-web/](https://experience.sap.com/fiori-design-web/) |
| Accessibility Guidelines | [https://experience.sap.com/fiori-design-web/accessibility/](https://experience.sap.com/fiori-design-web/accessibility/) |
| SAPUI5 Demo Kit | [https://sapui5.hana.ondemand.com/](https://sapui5.hana.ondemand.com/) |
| Fiori Tools | SAP Business Application Studio |

## Source Documentation

- UX Design: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/user-experience-design-323bd93.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/user-experience-design-323bd93.md)
- UX Compliance: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/ux-design-and-product-compliance-standards-91e4468.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/ux-design-and-product-compliance-standards-91e4468.md)

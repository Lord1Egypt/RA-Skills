# Annotations Reference

Comprehensive reference for working with annotations in SAP Fiori tools.

## Table of Contents

1. [Language Server Features](#language-server-features)
2. [Supported File Types](#supported-file-types)
3. [Supported Vocabularies](#supported-vocabularies)
4. [Code Completion](#code-completion)
5. [Micro-Snippets](#micro-snippets)
6. [Diagnostics](#diagnostics)
7. [Internationalization](#internationalization)
8. [Service Modeler](#service-modeler)
9. [Common Annotation Patterns](#common-annotation-patterns)

---

## Language Server Features

SAP Fiori tools provides two annotation language servers:

| Server | File Type | Scope |
|--------|-----------|-------|
| CDS OData Language Server | `.cds` files | CAP projects |
| XML Annotation Language Server | `annotation.xml` files | All projects |

### Capabilities

- Code completion for annotation targets, terms, attributes, values
- Validation against OData vocabularies and project metadata
- Navigation to referenced annotations
- Quick vocabulary information views
- Internationalization (i18n) support

---

## Supported File Types

### CDS Annotation Files

Location: CAP project `.cds` files

```cds
annotate CatalogService.Products with @(
    UI: {
        HeaderInfo: {
            TypeName: 'Product',
            TypeNamePlural: 'Products',
            Title: { Value: name }
        },
        LineItem: [
            { Value: ID },
            { Value: name },
            { Value: price }
        ]
    }
);
```

### XML Annotation Files

Location: `webapp/annotations/*.xml`

**Prerequisites**:
1. OData Service with local metadata copy
2. Path specified in `manifest.json` as local `Uri`
3. Metadata contains `<edm:Schema>` definitions
4. Single `EntityContainer` in metadata
5. Valid XML file with `</edmx:DataServices/Schema>` nodes

**Manifest Configuration**:
```json
{
  "sap.app": {
    "dataSources": {
      "mainService": {
        "uri": "/sap/opu/odata/sap/SERVICE/",
        "type": "OData",
        "settings": {
          "localUri": "localService/metadata.xml",
          "annotations": ["annotation"]
        }
      },
      "annotation": {
        "type": "ODataAnnotation",
        "uri": "annotations/annotation.xml"
      }
    }
  }
}
```

---

## Supported Vocabularies

### OASIS OData v4 Vocabularies

| Vocabulary | Namespace | Description |
|------------|-----------|-------------|
| Core | Org.OData.Core.V1 | Core vocabulary terms |
| Capabilities | Org.OData.Capabilities.V1 | Service capabilities |
| Aggregation | Org.OData.Aggregation.V1 | Aggregation support |
| Authorization | Org.OData.Authorization.V1 | Authorization schemes |
| JSON | Org.OData.JSON.V1 | JSON-related terms |
| Measures | Org.OData.Measures.V1 | Units of measure |
| Repeatability | Org.OData.Repeatability.V1 | Request repeatability |
| Temporal | Org.OData.Temporal.V1 | Temporal data |
| Validation | Org.OData.Validation.V1 | Data validation |

### SAP OData Vocabularies

| Vocabulary | Namespace | Description |
|------------|-----------|-------------|
| Analytics | com.sap.vocabularies.Analytics.v1 | Analytical annotations |
| CodeList | com.sap.vocabularies.CodeList.v1 | Code list definitions |
| Common | com.sap.vocabularies.Common.v1 | Common terms |
| Communication | com.sap.vocabularies.Communication.v1 | Contact information |
| DataIntegration | com.sap.vocabularies.DataIntegration.v1 | Data integration |
| DirectEdit | com.sap.vocabularies.DirectEdit.v1 | Direct editing |
| Graph | com.sap.vocabularies.Graph.v1 | Graph structures |
| Hierarchy | com.sap.vocabularies.Hierarchy.v1 | Hierarchical data |
| HTML5 | com.sap.vocabularies.HTML5.v1 | HTML5 rendering |
| ODM | com.sap.vocabularies.ODM.v1 | One Domain Model |
| PDF | com.sap.vocabularies.PDF.v1 | PDF generation |
| PersonalData | com.sap.vocabularies.PersonalData.v1 | Personal data marking |
| Preview | com.sap.vocabularies.Preview.v1 | Preview features |
| Session | com.sap.vocabularies.Session.v1 | Session handling |
| UI | com.sap.vocabularies.UI.v1 | UI annotations |

---

## Code Completion

### Activation

- **Windows**: `Ctrl + Space`
- **macOS**: `Cmd + Space`

### Context-Aware Suggestions

Code completion provides suggestions based on:
- Project metadata (entities, properties, associations)
- OData vocabulary definitions
- Current cursor context

### Path Navigation

Use `/` character to:
1. Accept current segment selection
2. Trigger completion for next segment
3. Navigate multi-segment annotation paths

### Supported Contexts

- Annotation targets
- Terms and term values
- Attributes and attribute values
- Record properties
- Path expressions

---

## Micro-Snippets

Pre-defined code blocks for rapid annotation development.

### Available Snippets

| Snippet Type | Description |
|--------------|-------------|
| Annotation Target | `<Annotations Target=""></Annotations>` |
| Terms | Complete term structures |
| Records | Record with properties |
| Property Values | Property value templates |

### Record Snippet Types

1. **Minimal Version**: Only mandatory properties (nullable=false)
2. **Complete Version**: All available properties

### Usage Example

Within `<Schema>` tags:
1. Trigger code completion
2. Select annotation target snippet
3. Cursor positions inside quotes for immediate target selection

---

## Diagnostics

### Validation Scope

The language server validates:
- Annotation syntax
- Vocabulary compliance
- Metadata references
- Property types and values

### Message Types

| Type | Severity | Description |
|------|----------|-------------|
| Error | High | Must fix before deployment |
| Warning | Medium | Potential issues |
| Info | Low | Informational messages |

### Accessing Diagnostics

1. **Hover**: Mouse over highlighted sections
2. **Problems Panel**: View > Problems (all issues)

### Quick Fixes

Light bulb icon provides automatic fixes:
- Missing required properties
- Type mismatches
- Value corrections

### Limitations

**Not Supported**:
- Annotations embedded in metadata
- Dynamic expressions
- Backend annotation file modifications (local copies only)

---

## Internationalization

### Configuration

**Non-CAP Projects**:
```json
// webapp/manifest.json
{
  "sap.ui5": {
    "models": {
      "i18n": {
        "type": "sap.ui.model.resource.ResourceModel",
        "settings": {
          "bundleName": "project.i18n.i18n"
        }
      }
    }
  }
}
```

**CAP Projects**:
```json
// .cdsrc.json or package.json
{
  "i18n": {
    "folders": ["_i18n", "i18n", "assets/i18n"]
  }
}
```

### Key Naming Conventions

| Project Type | Format | Example |
|--------------|--------|---------|
| Non-CAP | camelCase | `productTitle` |
| CAP | PascalCase | `ProductTitle` |

### i18n Scenarios

1. **Non-internationalized labels**: Convert to i18n key references
2. **Missing i18n keys**: Auto-generate with matching values
3. **Duplicate text**: Link to existing i18n entries

### Mass i18n Generation

Bulk externalization of multiple UI texts:
1. Access via Page Editor or annotation file
2. Select multiple translatable strings
3. Generate keys in batch operation

### Best Practice

Handle i18n near project completion to minimize unused entries and reduce localization costs.

---

## Service Modeler

### Purpose

Visualize OData service metadata and annotations for exploration and overriding.

### Launching

- Command Palette: `Fiori: Open Service Modeler`
- Context Menu: Right-click folder > "Override Annotations"
- Editor: Click icon when metadata.xml is open

### Features

**Annotation Display**:
- View backend and local annotation files
- Local annotations override backend annotations
- Search annotations by term or target

**Source Navigation**:
- "Show in Source" icon opens original file
- Highlighting for context

### Editing Annotations

Backend annotations cannot be modified directly. Local annotations:
- Location: `/webapp/annotations/<filename>.xml`
- Edit via XML Code Editor
- Delete using Service Modeler delete icon

### Override Priority

Local annotations win over backend annotations when:
- Same annotation term
- Same qualifier
- Same target

---

## Common Annotation Patterns

### List Report Line Item

```xml
<Annotations Target="Namespace.EntityType">
    <Annotation Term="UI.LineItem">
        <Collection>
            <Record Type="UI.DataField">
                <PropertyValue Property="Value" Path="PropertyName"/>
                <PropertyValue Property="Label" String="Column Label"/>
            </Record>
        </Collection>
    </Annotation>
</Annotations>
```

### Selection Fields (Filter Bar)

```xml
<Annotation Term="UI.SelectionFields">
    <Collection>
        <PropertyPath>Property1</PropertyPath>
        <PropertyPath>Property2</PropertyPath>
    </Collection>
</Annotation>
```

### Header Info

```xml
<Annotation Term="UI.HeaderInfo">
    <Record Type="UI.HeaderInfoType">
        <PropertyValue Property="TypeName" String="Entity"/>
        <PropertyValue Property="TypeNamePlural" String="Entities"/>
        <PropertyValue Property="Title">
            <Record Type="UI.DataField">
                <PropertyValue Property="Value" Path="Name"/>
            </Record>
        </PropertyValue>
    </Record>
</Annotation>
```

### Object Page Facets

```xml
<Annotation Term="UI.Facets">
    <Collection>
        <Record Type="UI.ReferenceFacet">
            <PropertyValue Property="Label" String="General"/>
            <PropertyValue Property="ID" String="GeneralFacet"/>
            <PropertyValue Property="Target" AnnotationPath="@UI.FieldGroup#General"/>
        </Record>
    </Collection>
</Annotation>
```

### Field Group

```xml
<Annotation Term="UI.FieldGroup" Qualifier="General">
    <Record Type="UI.FieldGroupType">
        <PropertyValue Property="Data">
            <Collection>
                <Record Type="UI.DataField">
                    <PropertyValue Property="Value" Path="Property1"/>
                </Record>
            </Collection>
        </PropertyValue>
    </Record>
</Annotation>
```

---

## Documentation Source

**GitHub**: [https://github.com/SAP-docs/btp-fiori-tools/tree/main/docs/Developing-an-Application](https://github.com/SAP-docs/btp-fiori-tools/tree/main/docs/Developing-an-Application)

Key files:
- `maintaining-annotations-with-language-server-6fc93f8.md`
- `code-completion-dd4fc3b.md`
- `micro-snippets-addf811.md`
- `diagnostics-1fd8f54.md`
- `internationalization-i18n-eb427f2.md`
- `visualizing-annotations-with-service-modeler-58784b5.md`
- `working-with-annotations-55bfb91.md`
- `overriding-annotations-2f1bb9c.md`

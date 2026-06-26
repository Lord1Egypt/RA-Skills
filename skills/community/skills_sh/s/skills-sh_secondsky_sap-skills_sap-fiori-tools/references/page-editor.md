# Page Editor Reference

Detailed configuration reference for the SAP Fiori tools Page Editor.

## Table of Contents

1. [List Report Page](#list-report-page)
2. [Object Page](#object-page)
3. [Extension-Based Elements](#extension-based-elements)
4. [Building Blocks](#building-blocks)
5. [Quick Actions](#quick-actions)

---

## List Report Page

### Filter Fields

Configure filter bar elements for data discovery.

**Types**:
- **Compact Filters**: Fields with value help
- **Visual Filters**: Charts with selectable elements (analytics-enabled services)

**Adding**: Page Map > Configure Page > Add icon next to Filter Bar > Filter Fields

Generates `UI.SelectionFields` annotation.

**Excluded Properties**: `UI.Hidden`, `UI.HiddenFilter`, `NonFilterableProperties`

**Editable Properties (Compact)**: Label, External ID, Text, Text Arrangement, Display Type

**Visual Filter Properties**: Measure/Dimension Labels, Scale Factor, Fractional Digits, Sort Order, Fixed Values

### Table Configuration

**Supported Table Types**: Responsive, Grid, Analytical, Tree (hierarchical data)

**Column Types (7)**:

| Column Type | Description |
|-------------|-------------|
| Basic Column | Standard value display (String, Decimal) |
| Chart Column | Inline chart visualization |
| Contact Column | Contact information display |
| Progress Column | Progress indicator |
| Rating Column | Star rating display |
| Table Actions | Actionable elements |
| External Navigation | External navigation links |

**Column Properties**:
- **Label**: From `Common.Label` or `@title`, customizable
- **Importance**: Controls small-screen visibility (None = hidden)
- **Hidden**: Conditional hiding via boolean property

### Table Actions

**Action Types**:
| Type | Annotation | Description |
|------|------------|-------------|
| Internal | `UI.DataFieldForAction` | Operations within app using bound actions |
| External | `UI.DataFieldForIntentBasedNavigation` | Navigate to other FLP apps |

**Placement**: Toolbar or Inline (column)

**Properties**:
- Label (from `Common.Label` or `@title`)
- Importance (column actions only)
- Criticality (Positive/Negative for inline only)
- Hidden (conditional)
- Semantic Object Mapping (external navigation)
- Requires Context (toolbar external navigation)

### Multiple Views

Display additional tables/charts in separate tabs via icon tab bar.

**Requirements**:
- `@Aggregation.ApplySupported` at service level
- Custom aggregations: `@Aggregation.CustomAggregate`
- Transformation aggregations: SAPUI5 1.106+
- Cannot coexist with Analytical Charts

**Adding Views**:
1. Click Add icon on Views node
2. Select table or chart view type
3. Choose Entity from OData Service
4. For charts: specify type, dimension, measure

Generates `UI.LineItem` or `UI.Chart` with qualifiers, updates `manifest.json`.

**Management**: Drag-and-drop reordering, delete icon (cannot remove last main entity table view)

### Analytical Chart

Add aggregated data visualization to List Report.

**Prerequisites**:
- No Multiple Views in List Report
- Main entity has aggregable/groupable properties
- Transformation aggregations: SAPUI5 1.106+

**Adding**:
1. Click "Add Chart" in Page Editor header
2. Select chart type
3. Choose dimension (groupable property)
4. Choose measure (aggregable property or create new)

**Configuration Properties**:

| Property | Description |
|----------|-------------|
| Chart Type | Visualization style |
| Title | Display text (supports i18n) |
| Measures | Aggregated values (min 1 default, cannot add same twice) |
| Dimensions | Groupable categories (min 1 default) |
| Presentation Variant | Controls sorting (New, From Table, None) |

**Note**: Sort order applies to both chart and table.

---

## Object Page

### Header Configuration

Based on `@UI.HeaderInfo` annotation.

**Header Properties**:
| Property | Description |
|----------|-------------|
| Type Name/Plural | String describing main object |
| Title | Displayed in header area |
| Description | Additional context |
| Image | Reference via `ImageUrl` |
| Initials | Path to string properties |
| Icon URL | SAP icon format (e.g., `sap-icon://accept`) |

**Header Actions**:
- **Standard Actions**: Edit, Delete (can be hidden conditionally)
- **Annotation-Based**: `UI.DataFieldForAction`, `UI.DataFieldForIntentBasedNavigation`, `UI.DataFieldForActionGroups`
- **Custom Actions**: Based on application extensions

**Header Sections (7 Types)**:
| Section | Description |
|---------|-------------|
| Form Section | Groups multiple fields |
| Data Point | Single key metrics with semantic coloring |
| Progress | Progress toward targets |
| Rating | Star ratings (default 5-star) |
| Bullet Micro Chart | Values on scales with targets |
| Area/Column/Line Micro Chart | Trend visualization |
| Radial/Comparison/Harvey/Stacked Bar | Additional chart types |

Reorder sections via drag-and-drop (updates `UI.HeaderFacets`).

### Section Types

#### Form Section

Based on `UI.FieldGroup` annotation.

**Adding**:
1. Open Page Editor for Object/Form Entry Page
2. Navigate to section node > Add icon
3. Choose "Add Form Section"
4. Enter label

**Properties**:
- Label: Section title
- Display on Demand: Hide content under "Show More"
- Hidden: Visibility control

#### Table Section

**Adding**:
1. Open Page Editor
2. Section node > Add icon > "Add Table Section"
3. Enter label and Value Source Entity

Generates `UI.LineItem` annotation with reference facet.

**Properties**: Label, Hidden

#### Identification Section

Display key identifying information prominently.

#### Chart Section

Embed charts within Object Page for data visualization.

#### Group Section

Group related content logically with collapsible containers.

### Footer Configuration

Actions from `UI.DataFieldForAction` records where `Determining = true`.

**Limitations**:
- External navigation actions NOT allowed in footer
- Importance and Requires Context properties don't apply

**Criticality**: Affects action ordering (Positive/Negative reorganizes nodes)

### Basic Fields

**Adding Fields**:
1. Expand section > click add button
2. Search/select fields from dropdown
3. Multiple fields can be added simultaneously

**Excluded Properties**:
- `Edm.Guid` type properties
- Draft properties: `IsActiveEntity`, `HasActiveEntity`, `HasDraftEntity`
- Draft navigation: `SiblingEntity`, `DraftAdministrativeData`
- Already referenced properties
- Duplicates within same section

**Moving Fields**:
- Drag-and-drop (highlights green when valid)
- Arrow buttons (up/down)
- Multi-select: Ctrl+Click
- Cross-section only when same entity `FieldGroup`/`Identification`

**Field Properties**:

| Property | Description |
|----------|-------------|
| Label | Display text |
| Criticality | Semantic coloring |
| Display as Image | Image rendering |
| External ID | External identifier |
| Hidden / Hide by Property | Visibility control |
| Restrictions | Input control |
| Semantic Object Name/Mapping | Navigation |
| Text / Text Arrangement | Display format |
| Display Type | Rendering type |

**Restrictions (Input Control)**:

| Option | Behavior |
|--------|----------|
| None | No annotations, defaults to optional |
| Optional | Field may remain empty |
| Mandatory | Value required |
| ReadOnly | Non-editable display-only |

**Note**: Read-only objects disable Display Type and Restrictions properties.

---

## Extension-Based Elements

### Custom Columns (OData V4)

Add custom columns with XML fragments:

**Configuration Steps**:
1. Select Table in Page Editor
2. Add > Custom Column
3. Provide: Header text, Fragment name, Anchor column, Placement
4. Optional: Generate event handler

**Generated Files**:
- Fragment: `webapp/ext/fragments/<name>.fragment.xml`
- Controller (optional): `webapp/ext/<name>.controller.js`

**Fragment Template**:
```xml
<core:FragmentDefinition xmlns:core="sap.ui.core" xmlns="sap.m">
    <Text text="{PropertyPath}" id="customColumn"/>
</core:FragmentDefinition>
```

### Custom Sections (OData V4)

Add custom sections to Object Page:

**Configuration**:
- Section title
- View type: Fragment (V4) or View (V2)
- Fragment/View name
- Anchor section and placement
- Generate event handler option

**Fragment Location**: `webapp/ext/fragments/`

### Custom Actions (OData V4 1.96+)

Add action buttons with custom handlers:

**Configuration**:
- Action ID (unique identifier)
- Button Text
- Anchor and Placement
- Action Handler File
- Handler Method name
- Requires Selection toggle (for table actions)

**Handler Template**:
```javascript
sap.ui.define([], function() {
    "use strict";
    return {
        onCustomAction: function(oEvent) {
            // Custom action logic
        }
    };
});
```

### Custom Views (OData V4 1.96.29+)

Add custom tab views to List Report:

**Configuration**:
- View Key (unique)
- Label text
- Fragment selection
- Event handler generation

### Controller Extensions

Extend page controller lifecycle and methods:

**Lifecycle Methods**:
- `onInit` - Component initialization
- `onBeforeRendering` - Before UI rendering
- `onAfterRendering` - After UI rendering
- `onExit` - Component destruction

**Override Pattern**:
```javascript
sap.ui.define(["sap/ui/core/mvc/ControllerExtension"], function(ControllerExtension) {
    return ControllerExtension.extend("customer.extension.MyExtension", {
        override: {
            onInit: function() {
                // Extension logic
            }
        },
        // Custom methods outside override
        myCustomMethod: function() {
            // Custom logic
        }
    });
});
```

**File Locations**:
- Extension: `webapp/changes/coding/<name>.js`
- Change descriptor: `webapp/changes/<name>.controllerExtension.change`

---

## Building Blocks

Reusable UI components for OData V4 custom pages and sections.

### Chart Building Block

Embed charts in custom UI:

```xml
<macros:Chart
    id="chartBlock"
    metaPath="@com.sap.vocabularies.UI.v1.Chart"
    contextPath="/EntitySet"/>
```

### Filter Bar Building Block

Add filter capabilities:

```xml
<macros:FilterBar
    id="filterBar"
    metaPath="@com.sap.vocabularies.UI.v1.SelectionFields"
    liveMode="true"/>
```

### Table Building Block

Display tabular data:

```xml
<macros:Table
    id="tableBlock"
    metaPath="@com.sap.vocabularies.UI.v1.LineItem"
    readOnly="true"/>
```

### Page Building Block

Container for custom pages:

```xml
<macros:Page id="customPage">
    <!-- Page content -->
</macros:Page>
```

### Rich Text Editor Building Block

Content editing in custom sections:

```xml
<macros:RichTextEditor
    id="richTextEditor"
    value="{Description}"/>
```

---

## Quick Actions

Page Editor provides quick action shortcuts for common operations:

| Quick Action | Description | Availability |
|--------------|-------------|--------------|
| Add Custom Page Action | Add action to page header | Object Page |
| Add Custom Table Action | Add action to table toolbar | List Report, Object Page |
| Add Custom Table Column | Add custom column | List Report, Object Page |
| Add Header Field | Add field to header | Object Page |
| Add Custom Section | Add custom section | Object Page |

### Accessing Quick Actions

1. Right-click element in Page Editor outline
2. Select from context menu
3. Configure in dialog

---

## Configuration Files

### Manifest.json Updates

Page Editor modifications update `manifest.json`:

```json
{
  "sap.ui5": {
    "routing": {
      "targets": {
        "ListReport": {
          "options": {
            "settings": {
              "content": {
                "header": {},
                "body": {}
              }
            }
          }
        }
      }
    }
  }
}
```

### UI Flexibility Changes

Custom extensions generate flexibility changes in `webapp/changes/`:

- `addXML.change` - Fragment additions
- `controllerExtension.change` - Controller extensions
- `propertyChange.change` - Property modifications

---

## Documentation Source

**GitHub**: [https://github.com/SAP-docs/btp-fiori-tools/tree/main/docs/Developing-an-Application](https://github.com/SAP-docs/btp-fiori-tools/tree/main/docs/Developing-an-Application)

Key files:
- `list-report-page-493f2aa.md`
- `form-and-object-page-1eb11a6.md`
- `maintaining-extension-based-elements-02172d2.md`
- `maintaining-building-blocks-6d3ad83.md`
- `supported-elements-in-page-editor-47f0424.md`

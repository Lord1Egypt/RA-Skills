# UI5 Code Analysis Complete Reference

**Official Documentation**: [https://ui5.github.io/cli/stable/pages/CodeAnalysis/](https://ui5.github.io/cli/stable/pages/CodeAnalysis/)

This reference provides comprehensive details about UI5 CLI code analysis features, dependency analyzers, and JSDoc generation.

## Table of Contents

1. [Overview](#overview)
2. [JSModule Analyzer](#jsmodule-analyzer)
3. [Component Analyzer](#component-analyzer)
4. [XML Template Analyzer](#xml-template-analyzer)
5. [Smart Template Analyzer](#smart-template-analyzer)
6. [XML Composite Analyzer](#xml-composite-analyzer)
7. [library.js Analyzer](#libraryjs-analyzer)
8. [JSDoc Generation](#jsdoc-generation)
9. [Dependency Types](#dependency-types)

---

## Overview

The UI5 CLI performs static code analysis during the build process to extract dependency information. This enables proper resource ordering, bundling optimization, and build optimization.

**Purpose**:
- Identify module dependencies
- Determine load order
- Optimize bundle generation
- Generate API documentation
- Enable tree shaking (future)

**When It Runs**: During build process, before bundling and minification

---

## JSModule Analyzer

### Overview

The JSModule Analyzer examines JavaScript files by parsing their Abstract Syntax Tree (AST) to identify dependencies.

### Detection Methods

**Supported APIs**:
- `sap.ui.define` - Standard UI5 module definition
- `sap.ui.require` - Async module loading
- **Deprecated APIs**:
  - `jQuery.sap.declare` - Legacy module declaration
  - `jQuery.sap.require` - Legacy sync loading
  - `sap.ui.requireSync` - Deprecated sync loading
- **Preload APIs**:
  - `sap.ui.preload` - Preload module definitions
  - `sap.ui.require.preload` - Preload for async require

### Dependency Classification

#### Eager Dependencies

**Definition**: Dependencies **unconditionally executed** at module load time.

**Example**:
```javascript
sap.ui.define([
    "sap/ui/core/mvc/Controller",    // EAGER
    "sap/m/MessageBox"                // EAGER
], function(Controller, MessageBox) {
    // Module always needs both dependencies
    return Controller.extend("my.Controller", {
        // ...
    });
});
```

**Characteristics**:
- Always loaded
- Required for module execution
- Included in preload bundles by default

---

#### Conditional Dependencies

**Definition**: Dependencies **executed only under certain conditions**.

**Example**:
```javascript
sap.ui.define([
    "sap/ui/core/mvc/Controller"
], function(Controller) {
    return Controller.extend("my.Controller", {
        onPress: function() {
            if (this.needsDialog) {
                // CONDITIONAL - only loaded if needsDialog is true
                sap.ui.require(["sap/m/Dialog"], function(Dialog) {
                    var dialog = new Dialog();
                    dialog.open();
                });
            }
        }
    });
});
```

**Characteristics**:
- Loaded only when condition met
- Not included in preload by default (configurable)
- Improves initial load time

**Flow Control Statements Creating Conditions**:
- `if` / `else`
- `switch` / `case`
- `try` / `catch`
- `while` / `for` loops
- Function calls (may not execute)

### Analysis Example

**Input** (Controller.js):
```javascript
sap.ui.define([
    "sap/ui/core/mvc/Controller",           // Eager
    "sap/ui/model/json/JSONModel",          // Eager
    "sap/m/MessageToast"                    // Eager
], function(Controller, JSONModel, MessageToast) {
    "use strict";

    return Controller.extend("my.app.controller.Main", {
        onInit: function() {
            var model = new JSONModel();    // Uses eager dependency
            this.getView().setModel(model);
        },

        onShowDetails: function() {
            // Conditional dependency
            sap.ui.require([
                "sap/m/Dialog",
                "sap/m/Button"
            ], function(Dialog, Button) {
                var dialog = new Dialog({
                    title: "Details",
                    buttons: [
                        new Button({text: "Close"})
                    ]
                });
                dialog.open();
            });
        },

        onError: function(error) {
            MessageToast.show(error);       // Uses eager dependency
        }
    });
});
```

**Analysis Result**:
```
Eager Dependencies:
- sap/ui/core/mvc/Controller
- sap/ui/model/json/JSONModel
- sap/m/MessageToast

Conditional Dependencies:
- sap/m/Dialog
- sap/m/Button
```

### Bundle Configuration Impact

**Default Behavior** (resolve: true):
```yaml
builder:
  componentPreload:
    namespaces:
      - "my/app"
```

**Includes**: Eager dependencies only

**With Conditional Resolution**:
```yaml
builder:
  componentPreload:
    namespaces:
      - "my/app"
    resolveConditional: true            # Include conditional deps
```

**Includes**: Eager + conditional dependencies

---

## Component Analyzer

### Overview

The Component Analyzer examines `Component.js` files and their associated `manifest.json` to extract dependencies from the `sap.ui5` section.

### Analyzed Sections

#### 1. Library Dependencies

**manifest.json**:
```json
{
  "sap.ui5": {
    "dependencies": {
      "libs": {
        "sap.ui.core": {},
        "sap.m": {},
        "sap.ui.table": {
          "minVersion": "1.120.0"
        }
      }
    }
  }
}
```

**Extracted Dependencies**:
- `sap/ui/core/library`
- `sap/m/library`
- `sap/ui/table/library`

---

#### 2. Component Dependencies

**manifest.json**:
```json
{
  "sap.ui5": {
    "dependencies": {
      "components": {
        "my.reuse.component": {
          "minVersion": "1.0.0"
        }
      }
    }
  }
}
```

**Extracted Dependencies**:
- `my/reuse/component/Component`

---

#### 3. Models

**manifest.json**:
```json
{
  "sap.ui5": {
    "models": {
      "i18n": {
        "type": "sap.ui.model.resource.ResourceModel",
        "settings": {
          "bundleName": "my.app.i18n.i18n"
        }
      },
      "": {
        "type": "sap.ui.model.odata.v2.ODataModel",
        "settings": {
          "serviceUrl": "/sap/opu/odata/sap/SERVICE"
        }
      }
    }
  }
}
```

**Extracted Dependencies**:
- `sap/ui/model/resource/ResourceModel` (from i18n model type)
- `sap/ui/model/odata/v2/ODataModel` (from default model type)

---

#### 4. Routing Configuration

**manifest.json**:
```json
{
  "sap.ui5": {
    "routing": {
      "config": {
        "viewType": "XML",
        "viewPath": "my.app.view",
        "controlId": "app",
        "controlAggregation": "pages"
      },
      "routes": [
        {
          "pattern": "",
          "name": "main",
          "target": "main"
        },
        {
          "pattern": "detail/{id}",
          "name": "detail",
          "target": "detail"
        }
      ],
      "targets": {
        "main": {
          "viewName": "Main"
        },
        "detail": {
          "viewName": "Detail"
        }
      }
    }
  }
}
```

**Extracted Dependencies**:
- `my/app/view/Main.view.xml` (from main target)
- `my/app/view/Detail.view.xml` (from detail target)

---

## XML Template Analyzer

### Overview

Parses XMLView and XMLFragment files to identify controls, resource bundles, and embedded fragments.

### Detection Capabilities

#### 1. Control Dependencies

**XMLView** (Main.view.xml):
```xml
<mvc:View
    controllerName="my.app.controller.Main"
    xmlns:mvc="sap.ui.core.mvc"
    xmlns="sap.m"
    xmlns:layout="sap.ui.layout">

    <Page title="{i18n>title}">
        <layout:VerticalLayout>
            <Button text="Click Me" press=".onPress"/>
            <List items="{/items}">
                <StandardListItem title="{title}"/>
            </List>
        </layout:VerticalLayout>
    </Page>
</mvc:View>
```

**Extracted Dependencies**:
- `sap/ui/core/mvc/View`
- `sap/m/Page`
- `sap/m/Button`
- `sap/m/List`
- `sap/m/StandardListItem`
- `sap/ui/layout/VerticalLayout`

---

#### 2. Fragment Dependencies

**XMLView with Fragment**:
```xml
<mvc:View xmlns:mvc="sap.ui.core.mvc" xmlns:core="sap.ui.core" xmlns="sap.m">
    <Page>
        <core:Fragment fragmentName="my.app.view.fragments.Dialog" type="XML"/>
    </Page>
</mvc:View>
```

**Extracted Dependencies**:
- All control dependencies from the view
- `my/app/view/fragments/Dialog.fragment.xml` (embedded fragment)

---

#### 3. Resource Bundle References

**XMLView**:
```xml
<mvc:View xmlns:mvc="sap.ui.core.mvc" xmlns="sap.m">
    <Page title="{i18n>title}">
        <Text text="{i18n>description}"/>
    </Page>
</mvc:View>
```

**Analysis**: Detects usage of resource bundle model (typically `i18n`)

**Note**: Resource bundle path resolved from manifest.json or Component.js

---

## Smart Template Analyzer

### Overview

Evaluates `sap.ui.generic.app` sections in manifest.json for SAP Fiori Elements / Smart Template configurations.

### Analyzed Sections

**manifest.json**:
```json
{
  "sap.ui.generic.app": {
    "pages": [
      {
        "entitySet": "Products",
        "component": {
          "name": "sap.suite.ui.generic.template.ListReport"
        },
        "pages": [
          {
            "entitySet": "Products",
            "component": {
              "name": "sap.suite.ui.generic.template.ObjectPage"
            }
          }
        ]
      }
    ]
  }
}
```

**Extracted Dependencies**:
- `sap/suite/ui/generic/template/ListReport/Component`
- `sap/suite/ui/generic/template/ObjectPage/Component`

**Use Case**: Fiori Elements applications using Smart Templates

---

## XML Composite Analyzer

### Overview

Handles deprecated XMLComposite control declarations.

**Note**: XMLComposite is deprecated. Use fragments or custom controls instead.

### Example

**Composite Control**:
```xml
<core:FragmentDefinition
    xmlns="sap.m"
    xmlns:core="sap.ui.core">

    <VBox>
        <Text text="{title}"/>
        <Button text="Action"/>
    </VBox>
</core:FragmentDefinition>
```

**Extracted Dependencies**:
- `sap/m/VBox`
- `sap/m/Text`
- `sap/m/Button`

---

## library.js Analyzer

### Overview

Inspects `library.js` files for `sap/ui/core/Core#initLibrary` calls, extracting metadata.

### Analyzed Data

**library.js**:
```javascript
sap.ui.define([], function() {
    "use strict";

    sap.ui.getCore().initLibrary({
        name: "my.company.library",
        version: "1.0.0",
        dependencies: [
            "sap.ui.core",
            "sap.m"
        ],
        types: [
            "my.company.library.ButtonType",
            "my.company.library.ListType"
        ],
        interfaces: [
            "my.company.library.ISelectable"
        ],
        controls: [
            "my.company.library.controls.CustomButton",
            "my.company.library.controls.CustomList"
        ],
        elements: [
            "my.company.library.elements.CustomElement"
        ]
    });

    return my.company.library;
});
```

### Generated manifest.json

**Output** (library manifest):
```json
{
  "_version": "1.9.0",
  "sap.app": {
    "id": "my.company.library",
    "type": "library",
    "title": "My Company Library",
    "description": "Custom UI5 library",
    "version": "1.0.0"
  },
  "sap.ui": {
    "technology": "UI5",
    "deviceTypes": {
      "desktop": true,
      "tablet": true,
      "phone": true
    }
  },
  "sap.ui5": {
    "dependencies": {
      "libs": {
        "sap.ui.core": {},
        "sap.m": {}
      }
    },
    "library": {
      "i18n": false,
      "css": true,
      "content": {
        "controls": [
          "my.company.library.controls.CustomButton",
          "my.company.library.controls.CustomList"
        ],
        "elements": [
          "my.company.library.elements.CustomElement"
        ],
        "types": [
          "my.company.library.ButtonType",
          "my.company.library.ListType"
        ],
        "interfaces": [
          "my.company.library.ISelectable"
        ]
      }
    }
  }
}
```

**Placement**: Generated `manifest.json` placed in library directory during build

---

## JSDoc Generation

### Overview

UI5 CLI offers enhanced JSDoc builds with UI5-specific features.

### UI5-Specific JSDoc Tags

| Tag | Description |
|-----|-------------|
| `@disclaimer` | Usage restrictions/warnings |
| `@experimental` | Experimental API, may change |
| `@final` | Cannot be overridden/extended |
| `@interface` | Declares interface |
| `@implements` | Implements interface |
| `@ui5-restricted` | Restricted to specific packages |

**Example**:
```javascript
/**
 * Custom button control.
 *
 * @class
 * @extends sap.m.Button
 * @author My Company
 * @version 1.0.0
 * @public
 * @since 1.0.0
 * @experimental Since 1.0.0 - API may change
 * @ui5-restricted sap.suite, sap.ushell
 */
```

### AST Visitor

**Purpose**: Detect UI5-specific extend calls for inheritance hierarchy.

**Example**:
```javascript
sap.ui.define([
    "sap/ui/core/Control"
], function(Control) {
    return Control.extend("my.CustomControl", {
        // Control implementation
    });
});
```

**Detection**: JSDoc AST visitor identifies:
- Base class (`sap/ui/core/Control`)
- Extended class name (`my.CustomControl`)
- Inheritance relationship

### API Documentation Generation

**Build Command**:
```bash
ui5 build jsdoc
```

**Process**:
1. Scan all JavaScript files
2. Parse JSDoc comments
3. Build inheritance hierarchy
4. Calculate complete API surface
5. Generate HTML documentation

**Output**:
```
dist/
└── test-resources/
    └── jsdoc/
        ├── index.html
        ├── symbols/
        │   ├── my.CustomControl.html
        │   └── ...
        └── styles/
```

### Version Utilities

**Purpose**: Track API changes across versions.

**Features**:
- Mark deprecated APIs
- Track experimental features
- Document version-specific changes
- Generate version comparison reports

---

## Dependency Types

### Summary

| Dependency Type | Source | Classification | Preload Default |
|----------------|--------|----------------|-----------------|
| **Module Definition** | sap.ui.define([...]) | Eager | Yes |
| **Async Require** | sap.ui.require([...]) | Conditional | No |
| **Sync Require** | sap.ui.requireSync(...) | Eager | Yes |
| **Library Deps** | manifest.json libs | Eager | Yes |
| **Component Deps** | manifest.json components | Eager | Yes |
| **Model Types** | manifest.json models | Eager | Yes |
| **Routing Views** | manifest.json targets | Eager | Yes |
| **XML Controls** | XMLView/Fragment | Eager | Yes |
| **Smart Templates** | sap.ui.generic.app | Eager | Yes |

---

## Best Practices

1. **Use Standard APIs**: Prefer `sap.ui.define` over deprecated APIs
2. **Lazy Load**: Use conditional dependencies for optional features
3. **Document Dependencies**: Add JSDoc for clarity
4. **Test Bundles**: Verify all dependencies included in preload
5. **Enable Conditional Resolution**: For complete bundles
6. **Generate JSDoc**: Keep API documentation up-to-date
7. **Analyze Build**: Use verbose logging to see dependency resolution

---

## Troubleshooting

### Missing Dependencies in Bundle

**Check**:
1. Dependency declared in `sap.ui.define`?
2. Conditional dependency? (need `resolveConditional: true`)
3. Resource excluded? (check `excludes` configuration)

### Circular Dependencies

**Symptom**: Module loading fails at runtime

**Solution**:
1. Analyze dependency graph: `ui5 tree`
2. Refactor to remove circular references
3. Use lazy loading for one direction

### JSDoc Build Fails

**Error**: Non-zero exit code from JSDoc

**Solution**:
1. Fix JSDoc syntax errors in code
2. Ensure all referenced types exist
3. Check JSDoc configuration

---

**Last Updated**: 2025-11-21
**Official Docs**: [https://ui5.github.io/cli/stable/pages/CodeAnalysis/](https://ui5.github.io/cli/stable/pages/CodeAnalysis/)

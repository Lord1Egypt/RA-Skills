# UI5 Project Structures Complete Reference

**Official Documentation**: [https://ui5.github.io/cli/stable/pages/Project/](https://ui5.github.io/cli/stable/pages/Project/)

This reference provides detailed directory structures, build output styles, and examples for all UI5 project types.

## Table of Contents

1. [Project Types Overview](#project-types-overview)
2. [Application Projects](#application-projects)
3. [Library Projects](#library-projects)
4. [Theme Library Projects](#theme-library-projects)
5. [Module Projects](#module-projects)
6. [Build Output Styles](#build-output-styles)
7. [Complete Examples](#complete-examples)

---

## Project Types Overview

UI5 Project module provides build functionality for four distinct project types:

| Type | Purpose | Source Dir | Virtual Mapping | Preload |
|------|---------|------------|-----------------|---------|
| **Application** | UI5 applications | `webapp/` | `/` | Component-preload.js |
| **Library** | Reusable libraries | `src/` | `/resources` | library-preload.js |
| **Theme Library** | Theme resources | `src/` | `/resources` | None |
| **Module** | Third-party code | Custom | Custom | None |

**Key Principle**: "In a projects dependency tree, there should only be one project of type `application`"

---

## Application Projects

### Purpose

Standard UI5 applications - typically the root project in a dependency tree.

### Directory Structure

```
my-app/
├── ui5.yaml                          # UI5 CLI configuration
├── package.json                      # npm dependencies
├── webapp/                           # Application source (maps to /)
│   ├── index.html                    # Entry point
│   ├── manifest.json                 # App descriptor
│   ├── Component.js                  # Component class
│   ├── controller/                   # Controllers
│   │   ├── App.controller.js
│   │   └── Main.controller.js
│   ├── view/                         # Views
│   │   ├── App.view.xml
│   │   └── Main.view.xml
│   ├── model/                        # Models
│   │   └── models.js
│   ├── css/                          # Stylesheets
│   │   └── style.css
│   ├── i18n/                         # Internationalization
│   │   ├── i18n.properties           # Default
│   │   ├── i18n_de.properties        # German
│   │   └── i18n_fr.properties        # French
│   ├── localService/                 # Mock data (optional)
│   │   ├── metadata.xml
│   │   └── mockdata/
│   ├── test/                         # Tests (optional)
│   │   ├── unit/
│   │   └── integration/
│   └── thirdparty/                   # Third-party libs (optional)
└── dist/                             # Build output (generated)
```

### Path Mapping

**Virtual Path**: `/` (root)

**Example**:
```
Source:  webapp/controller/Main.controller.js
Runtime: /controller/Main.controller.js
URL:     http://localhost:8080/controller/Main.controller.js
```

### Component Requirement

Applications **may optionally** contain:
- `Component.js` - Component class
- `manifest.json` - App descriptor (required if Component.js exists)

**If Component.js exists**: Build generates optimized `Component-preload.js`

### Minimal ui5.yaml

```yaml
specVersion: "4.0"
type: application
metadata:
  name: my.company.app

framework:
  name: SAPUI5
  version: "1.120.0"
  libraries:
    - name: sap.ui.core
    - name: sap.m
```

### Build Output (Default Style)

```
dist/
├── controller/
│   ├── Main.controller.js            # Minified
│   ├── Main-dbg.controller.js        # Debug variant
│   └── Main.controller.js.map        # Source map
├── view/
│   └── Main.view.xml
├── Component-preload.js              # Component bundle
├── Component.js                      # Minified component
├── Component-dbg.js                  # Debug component
├── manifest.json                     # Enhanced manifest
├── index.html                        # Entry point
└── resources/
    └── sap-ui-version.json           # Version info
```

---

## Library Projects

### Purpose

Reuse, custom, or control libraries for sharing code across projects.

### Directory Structure

```
my-library/
├── ui5.yaml                          # UI5 CLI configuration
├── package.json                      # npm dependencies
├── src/                              # Library source (maps to /resources)
│   └── my/                           # Namespace (required!)
│       └── company/
│           └── library/              # Library name
│               ├── library.js        # Library initialization
│               ├── .library          # Library metadata (XML)
│               ├── manifest.json     # Library manifest (optional)
│               ├── messagebundle.properties  # i18n
│               ├── Component1.js     # Library components
│               ├── Component2.js
│               ├── controls/         # Custom controls
│               │   ├── CustomButton.js
│               │   └── CustomList.js
│               └── themes/           # Themes
│                   ├── base/         # Base theme (required)
│                   │   ├── library.source.less
│                   │   ├── library.css
│                   │   ├── CustomButton.less
│                   │   └── img/
│                   ├── sap_horizon/  # Horizon theme
│                   │   └── library.source.less
│                   └── sap_fiori_3/  # Fiori 3 theme
│                       └── library.source.less
├── test/                             # Test source (maps to /test-resources)
│   └── my/
│       └── company/
│           └── library/
│               ├── qunit/            # Unit tests
│               │   ├── testsuite.qunit.html
│               │   └── Component1.qunit.html
│               └── integration/      # Integration tests
│                   └── pages/
└── dist/                             # Build output (generated)
```

### Namespace Requirement

**Critical**: Library must contain namespace directory structure.

**Pattern**: `src/<namespace-path>/<library-name>/`

**Example**: For library name `my.company.library`:
```
src/my/company/library/
```

**Reason**: Prevents name clashes, enables proper resource resolution.

### Path Mapping

**Source Path**: `src/` → `/resources` (runtime)
**Test Path**: `test/` → `/test-resources` (runtime)

**Examples**:
```
Source:  src/my/company/library/Component1.js
Runtime: /resources/my/company/library/Component1.js
URL:     http://localhost:8080/resources/my/company/library/Component1.js

Test:    test/my/company/library/qunit/Component1.qunit.html
Runtime: /test-resources/my/company/library/qunit/Component1.qunit.html
URL:     http://localhost:8080/test-resources/my/company/library/qunit/Component1.qunit.html
```

### library.js (Required)

Library initialization file.

**Example**:
```javascript
sap.ui.define([], function() {
    "use strict";

    sap.ui.getCore().initLibrary({
        name: "my.company.library",
        version: "1.0.0",
        dependencies: [
            "sap.ui.core"
        ],
        types: [
            "my.company.library.ButtonType"
        ],
        interfaces: [
            "my.company.library.ISelectable"
        ],
        controls: [
            "my.company.library.controls.CustomButton",
            "my.company.library.controls.CustomList"
        ],
        elements: [],
        noLibraryCSS: false
    });

    return my.company.library;
});
```

### .library (Required)

XML library metadata.

**Example**:
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<library xmlns="http://www.sap.com/sap.ui.library.xsd">
    <name>my.company.library</name>
    <vendor>My Company</vendor>
    <version>1.0.0</version>
    <documentation>My custom UI5 library</documentation>

    <dependencies>
        <dependency>
            <libraryName>sap.ui.core</libraryName>
        </dependency>
    </dependencies>

    <appData>
        <packaging xmlns="http://www.sap.com/ui5/buildext/packaging"
                   version="2.0">
            <module-infos>
                <module-info name="my/company/library/library-preload.js"
                            description="Library Preload"
                            requiresTopLevelScope="false" />
            </module-infos>
        </packaging>
    </appData>
</library>
```

### Minimal ui5.yaml

```yaml
specVersion: "4.0"
type: library
metadata:
  name: my.company.library

framework:
  name: SAPUI5
  version: "1.120.0"
  libraries:
    - name: sap.ui.core
```

### Build Output (Default Style)

```
dist/
└── resources/
    └── my/
        └── company/
            └── library/
                ├── library.js                # Minified
                ├── library-dbg.js            # Debug
                ├── library-preload.js        # Library bundle
                ├── Component1.js             # Minified
                ├── Component1-dbg.js         # Debug
                ├── controls/
                │   ├── CustomButton.js
                │   └── CustomButton-dbg.js
                ├── themes/
                │   ├── base/
                │   │   ├── library.css       # Compiled from LESS
                │   │   └── img/
                │   └── sap_horizon/
                │       └── library.css
                ├── manifest.json
                ├── .library
                └── messagebundle.properties
```

---

## Theme Library Projects

### Purpose

Provides theming resources for one or multiple libraries.

### Directory Structure

```
my-theme-library/
├── ui5.yaml
├── package.json
├── src/                              # Maps to /resources
│   ├── my/
│   │   └── library/
│   │       └── themes/
│   │           └── my_custom_theme/  # Theme name
│   │               ├── library.source.less
│   │               ├── library-parameters.json
│   │               └── img/
│   │                   └── theme-icon.png
│   └── another/
│       └── library/
│           └── themes/
│               └── my_custom_theme/
│                   └── library.source.less
└── test/                             # Optional test resources
```

### Resource Organization

**Pattern**: `<namespace>/themes/<theme-name>/`

**Example**: For theme `my_custom_theme` applied to library `my.library`:
```
src/my/library/themes/my_custom_theme/library.source.less
```

### Path Mapping

Same as library projects:
- `src/` → `/resources`
- `test/` → `/test-resources`

### Available Since

Specification Version **1.1**

### Minimal ui5.yaml

```yaml
specVersion: "4.0"
type: theme-library
metadata:
  name: my.custom.theme.library

resources:
  configuration:
    paths:
      src: src
      test: test
```

### Build Output

```
dist/
└── resources/
    ├── my/
    │   └── library/
    │       └── themes/
    │           └── my_custom_theme/
    │               ├── library.css           # Compiled from LESS
    │               ├── library-parameters.json
    │               └── img/
    │                   └── theme-icon.png
    └── another/
        └── library/
            └── themes/
                └── my_custom_theme/
                    └── library.css
```

---

## Module Projects

### Purpose

Third-party resources with flexible path mapping. Resources copied without modification.

### Characteristics

- Custom virtual-to-physical path mappings
- Resources copied without processing (no minification, bundling)
- Useful for non-UI5 libraries (jQuery, lodash, moment, etc.)

### Directory Structure

```
thirdparty-module/
├── ui5.yaml
├── package.json
└── lib/                              # Source directory (any name)
    ├── lodash.js
    ├── lodash.min.js
    └── LICENSE
```

### Path Mapping Configuration

**Required**: Must use `/resources` prefix for virtual paths.

**Example ui5.yaml**:
```yaml
specVersion: "4.0"
type: module
metadata:
  name: thirdparty.lodash

resources:
  configuration:
    paths:
      /resources/thirdparty/lodash/: lib    # Virtual: Physical
```

**Explanation**:
- Virtual path: `/resources/thirdparty/lodash/`
- Physical path: `lib/` (relative to ui5.yaml)
- File `lib/lodash.js` accessible at `/resources/thirdparty/lodash/lodash.js`

### Multiple Mappings

```yaml
resources:
  configuration:
    paths:
      /resources/thirdparty/jquery/: node_modules/jquery/dist
      /resources/thirdparty/moment/: node_modules/moment/min
      /resources/vendor/custom/: vendor
```

### Build Output

```
dist/
└── resources/
    └── thirdparty/
        └── lodash/
            ├── lodash.js             # Copied as-is
            ├── lodash.min.js         # Copied as-is
            └── LICENSE               # Copied as-is
```

**Note**: No minification, no debug variants, no preload bundles.

---

## Build Output Styles

Three output styles customize build artifact organization.

### Default Style

**Behavior**: Varies by project type

**Application**: Uses Flat style
**Library**: Uses Namespace style
**Theme Library**: No style customization
**Module**: No style customization

### Flat Style

**Purpose**: Streamlined output without namespace directories.

**Command**:
```bash
ui5 build --output-style Flat
```

**Example** (Library):
```
# Without Flat (Default/Namespace)
dist/resources/my/company/library/Component.js

# With Flat
dist/Component.js
```

**Directory Structure**:
```
dist/
├── Component.js
├── Component-dbg.js
├── library.js
├── library-dbg.js
├── library-preload.js
├── controls/
│   ├── CustomButton.js
│   └── CustomButton-dbg.js
└── themes/
    └── base/
        └── library.css
```

**Use Case**: Simplifies paths, reduces nesting

**Limitations**:
- Theme libraries: Not supported
- Modules: Not supported

---

### Namespace Style

**Purpose**: Resources prefixed with project namespace.

**Command**:
```bash
ui5 build --output-style Namespace
```

**Example** (Library `my.company.library`):
```
dist/
└── my/
    └── company/
        └── library/
            ├── Component.js
            ├── Component-dbg.js
            ├── library.js
            └── ...
```

**Virtual Path Mapping**:
```
Namespace:  my/company/library/Component.js
Runtime:    /resources/my/company/library/Component.js
```

**Use Case**: Mirrors runtime structure, avoids conflicts

**Limitations**:
- Theme libraries: Not supported
- Modules: Not supported

---

### Output Style Comparison

**Application** (default is Flat):
```
# Default/Flat
dist/
├── controller/
├── view/
└── Component.js

# Namespace
dist/
└── my/
    └── app/
        ├── controller/
        ├── view/
        └── Component.js
```

**Library** (default is Namespace):
```
# Default/Namespace
dist/
└── resources/
    └── my/
        └── lib/
            └── Component.js

# Flat
dist/
└── Component.js
```

---

## Complete Examples

### Example 1: Simple Application

**Directory**:
```
my-app/
├── ui5.yaml
├── package.json
└── webapp/
    ├── index.html
    ├── manifest.json
    ├── Component.js
    ├── controller/
    │   └── App.controller.js
    └── view/
        └── App.view.xml
```

**ui5.yaml**:
```yaml
specVersion: "4.0"
type: application
metadata:
  name: my.app

framework:
  name: SAPUI5
  version: "1.120.0"
  libraries:
    - name: sap.ui.core
    - name: sap.m
```

**Build**:
```bash
ui5 build --all --clean-dest
```

**Output**:
```
dist/
├── controller/
│   ├── App.controller.js
│   ├── App-dbg.controller.js
│   └── App.controller.js.map
├── view/
│   └── App.view.xml
├── Component-preload.js
├── Component.js
├── Component-dbg.js
├── manifest.json
└── index.html
```

---

### Example 2: Library with Tests

**Directory**:
```
my-lib/
├── ui5.yaml
├── package.json
├── src/
│   └── my/
│       └── lib/
│           ├── library.js
│           ├── .library
│           ├── Control.js
│           └── themes/
│               └── base/
│                   └── library.source.less
└── test/
    └── my/
        └── lib/
            └── qunit/
                ├── testsuite.qunit.html
                └── Control.qunit.html
```

**ui5.yaml**:
```yaml
specVersion: "4.0"
type: library
metadata:
  name: my.lib

framework:
  name: SAPUI5
  version: "1.120.0"
  libraries:
    - name: sap.ui.core
```

**Build**:
```bash
ui5 build --all
```

**Output**:
```
dist/
├── resources/
│   └── my/
│       └── lib/
│           ├── library.js
│           ├── library-dbg.js
│           ├── library-preload.js
│           ├── Control.js
│           ├── Control-dbg.js
│           ├── .library
│           └── themes/
│               └── base/
│                   └── library.css
└── test-resources/
    └── my/
        └── lib/
            └── qunit/
                ├── testsuite.qunit.html
                └── Control.qunit.html
```

---

### Example 3: Module for Lodash

**ui5.yaml**:
```yaml
specVersion: "4.0"
type: module
metadata:
  name: thirdparty.lodash

resources:
  configuration:
    paths:
      /resources/thirdparty/lodash/: node_modules/lodash/dist
```

**Build**:
```bash
ui5 build
```

**Output**:
```
dist/
└── resources/
    └── thirdparty/
        └── lodash/
            ├── lodash.js
            ├── lodash.min.js
            └── lodash.js.map
```

**Usage in App**:
```javascript
sap.ui.define([
    "thirdparty/lodash/lodash"
], function(_) {
    "use strict";

    return _.debounce(function() {
        console.log("Debounced!");
    }, 300);
});
```

---

## Best Practices

1. **Applications**: Use flat output style for simplicity
2. **Libraries**: Always use namespace directory structure in source
3. **Theme Libraries**: Organize by library namespace, then theme name
4. **Modules**: Use `/resources` prefix for virtual paths
5. **Test Resources**: Always separate from production source
6. **Third-Party**: Use module type, don't modify files
7. **Namespace Conflicts**: Ensure unique namespace across dependencies

---

## Troubleshooting

### Library Resources Not Found
**Check**: Namespace directory structure in `src/`

### Module Resources 404
**Check**: Virtual path uses `/resources` prefix

### Build Output in Wrong Location
**Check**: Output style configuration

### Test Resources Not Built
**Check**: `test/` directory follows same namespace structure as `src/`

---

**Last Updated**: 2025-11-21
**Official Docs**: [https://ui5.github.io/cli/stable/pages/Project/](https://ui5.github.io/cli/stable/pages/Project/)

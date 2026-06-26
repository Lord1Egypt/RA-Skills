# UI5 Build Process Complete Reference

**Official Documentation**: [https://ui5.github.io/cli/stable/pages/Builder/](https://ui5.github.io/cli/stable/pages/Builder/)

This reference provides comprehensive details about the UI5 build process, tasks, optimization, and bundling.

## Table of Contents

1. [Overview](#overview)
2. [Build Types](#build-types)
3. [Standard Build Tasks](#standard-build-tasks)
4. [Minification Process](#minification-process)
5. [Source Maps](#source-maps)
6. [Bundle Generation](#bundle-generation)
7. [Legacy Bundle Tooling (LBT)](#legacy-bundle-tooling-lbt)
8. [Build Optimization](#build-optimization)
9. [Supported Locales Generation](#supported-locales-generation)
10. [Custom Processors](#custom-processors)

---

## Overview

The UI5 Builder module orchestrates the build process for UI5 projects by defining a series of build steps (tasks) to execute. Different task sequences run based on project type (application, library, or theme-library).

**Core Concept**: "The UI5 Builder takes care of building your project by defining a series of build steps to execute; these are also called 'tasks.'"

**Architecture**:
- **Tasks**: Specific build steps (collect resources, apply modifications)
- **Processors**: Logic that modifies resources
- **Workflows**: Task sequences per project type

---

## Build Types

### Standard Build

Default execution with predefined tasks for each project type.

**Command**:
```bash
ui5 build
ui5 build --all                    # Include all dependencies
```

**Tasks Executed**:
- All standard tasks for project type
- Component/library preload generation
- Minification
- Theme building
- Version info generation

**Output**: `./dist/` directory (default)

---

### Self-Contained Build

Creates standalone bundle with embedded UI5 framework.

**Command**:
```bash
ui5 build self-contained --all
```

**What Happens**:
1. Activates `generateStandaloneAppBundle` task
2. Activates `transformBootstrapHtml` task
3. Disables component preload generation
4. Disables library preload generation
5. Creates single bundle with all resources

**Enabled Tasks**:
- `generateStandaloneAppBundle` - Bundles app + framework
- `transformBootstrapHtml` - Updates bootstrap script tag

**index.html Transformation**:

**Before**:
```html
<script id="sap-ui-bootstrap"
    src="https://ui5.sap.com/resources/sap-ui-core.js"
    data-sap-ui-libs="sap.m">
</script>
```

**After**:
```html
<script id="sap-ui-bootstrap"
    src="Component-preload.js">
</script>
```

**Use Case**: Offline applications, embedded scenarios

---

### JSDoc Build

Specialized mode for documentation generation.

**Command**:
```bash
ui5 build jsdoc
```

**What Happens**:
- Disables most standard tasks
- Enables JSDoc generation tasks
- Processes JavaScript for API documentation

**Enabled Tasks**:
- JSDoc generation
- API documentation build

**Output**: JSDoc HTML files in `./dist/`

**Requires**: JSDoc must be installed and available

---

### Custom Bundling

Activated when project defines bundle configuration.

**Configuration**:
```yaml
builder:
  bundles:
    - bundleDefinition:
        name: "custom-bundle.js"
        sections:
          - mode: preload
            filters: ["my/app/**/*.js"]
```

**What Happens**:
- Enables `generateBundle` task
- Creates custom resource bundles
- Applies bundle optimizations

**See**: [Bundle Generation section](#bundle-generation) below

---

## Standard Build Tasks

Tasks execute in specific order. Here's the complete standard task sequence:

### Application Tasks (Execution Order)

| # | Task | Purpose |
|---|------|---------|
| 1 | `escapeNonAsciiCharacters` | Escape non-ASCII in .properties files |
| 2 | `replaceCopyright` | Replace ${copyright} placeholders |
| 3 | `replaceVersion` | Replace ${version} placeholders |
| 4 | `replaceBuildtime` | Replace ${buildtime} placeholders |
| 5 | `minify` | Minify JavaScript, create debug variants |
| 6 | `generateFlexChangesBundle` | Bundle UI adaptation changes |
| 7 | `generateComponentPreload` | Create Component-preload.js |
| 8 | `generateBundle` | Create custom bundles (if configured) |
| 9 | `transformBootstrapHtml` | Transform bootstrap (self-contained only) |
| 10 | `generateStandaloneAppBundle` | Create standalone bundle (self-contained only) |

### Library Tasks (Execution Order)

| # | Task | Purpose |
|---|------|---------|
| 1 | `escapeNonAsciiCharacters` | Escape non-ASCII in .properties files |
| 2 | `replaceCopyright` | Replace ${copyright} placeholders |
| 3 | `replaceVersion` | Replace ${version} placeholders |
| 4 | `minify` | Minify JavaScript, create debug variants |
| 5 | `generateLibraryManifest` | Generate manifest.json for library |
| 6 | `generateLibraryPreload` | Create library-preload.js |
| 7 | `buildThemes` | Compile LESS to CSS |
| 8 | `generateThemeDesignerResources` | Generate theme designer resources (framework only) |
| 9 | `generateResourcesJson` | Generate resources.json |
| 10 | `generateBundle` | Create custom bundles (if configured) |

### Theme Library Tasks (Execution Order)

| # | Task | Purpose |
|---|------|---------|
| 1 | `buildThemes` | Compile LESS to CSS |
| 2 | `generateThemeDesignerResources` | Generate theme designer resources |

### Common Tasks (All Project Types)

**generateVersionInfo**: Creates `sap-ui-version.json` with version metadata

---

## Minification Process

The minify task compresses JavaScript resources while preserving original sources as debug variants.

### How It Works

**For Each JavaScript File**:
1. Read source file (e.g., `Module.js`)
2. Minify using Terser
3. Create debug variant with `-dbg` suffix (`Module-dbg.js`)
4. Generate source map (`Module.js.map`)
5. Write all three files

**Example**:
```
Input:  Controller.js (10 KB, formatted)
Output: Controller.js (3 KB, minified)
        Controller-dbg.js (10 KB, original)
        Controller.js.map (source map)
```

### Debug Variants

**Purpose**: Preserve original source for debugging

**Naming Convention**:
```
Module.js       → minified version
Module-dbg.js   → debug variant (original source)
```

**Usage in Browser**:
```javascript
// Development: Load debug variant
sap.ui.require(["my/app/Module"]);  // Loads Module-dbg.js

// Production: Load minified
sap.ui.require(["my/app/Module"]);  // Loads Module.js
```

**UI5 Bootstrap**:
```html
<!-- Debug mode: loads -dbg variants -->
<script src="sap-ui-core.js" data-sap-ui-debug="true"></script>
```

### Minification Configuration

**Exclude Files**:
```yaml
builder:
  minification:
    excludes:
      - "my/app/thirdparty/**"           # Exclude directory
      - "!my/app/thirdparty/small.js"    # Exception: minify this
```

**What Happens**:
- Excluded files copied without minification
- No debug variant created
- No source map generated

---

## Source Maps

Source maps enable debugging of minified code in browsers.

### Automatic Generation

**For Minified Files**:
```javascript
// Module.js (minified)
sap.ui.define([],function(){return{getValue:function(){return 42}}});
//# sourceMappingURL=Module.js.map
```

**Source Map** (`Module.js.map`):
```json
{
  "version": 3,
  "sources": ["Module-dbg.js"],
  "names": ["getValue"],
  "mappings": "AAAA...",
  "file": "Module.js"
}
```

**Browser Usage**:
1. Loads minified `Module.js`
2. Detects source map reference
3. Loads `Module.js.map`
4. Maps minified code to `Module-dbg.js`
5. Shows original source in DevTools

### Transpilation Support

**For TypeScript/Babel Projects**:

The minify task incorporates input source maps created during transpilation.

**Workflow**:
```
TypeScript → JavaScript + source map → Minification → Minified + combined source map
```

**Example**:
```
1. Module.ts (original TypeScript)
2. tsc → Module.js + Module.js.map (transpilation)
3. ui5 build → Module.js (minified) + Module.js.map (combined)
```

**Result**: Browser can debug original TypeScript source!

**Warning**: Tasks like `replaceVersion`, `replaceCopyright`, and `replaceBuildtime` modify resources **before** minification. They can corrupt source maps if they alter content without updating maps.

**Best Practice**: Configure transpilation to generate source maps, then let minify task handle them.

---

## Bundle Generation

### Overview

Bundling combines multiple modules into single files for faster loading.

### Bundle Modes

| Mode | Description | Output |
|------|-------------|--------|
| `raw` | Raw module content | Concatenated code |
| `preload` | sap.ui.predefine wrapped | Preload bundle |
| `provided` | List of provided modules | Module list |
| `require` | sap.ui.require calls | Require calls |
| `bundleInfo` | Bundle metadata | Metadata JSON |
| `depCache` | Dependency cache (v3.2+) | Dependency info |

### Configuration Example

```yaml
builder:
  bundles:
    - bundleDefinition:
        name: "custom-bundle.js"
        defaultFileTypes: [".js"]
        sections:
          - mode: preload
            filters:
              - "my/app/Component.js"
              - "my/app/**/*.js"
            resolve: true              # Resolve dependencies
            resolveConditional: true   # Include conditional deps
            renderer: false            # Exclude renderers
          - mode: require
            async: true                # Use async require (v4.0+)
            filters:
              - "my/app/lazy/**/*.js"
      bundleOptions:
        optimize: true                 # Minify bundle
        sourceMap: true                # Generate source map
        decorateBootstrapModule: true  # Add bootstrap decoration
```

### Bundle Sections

**Filters**: Glob patterns to match resources

**Options**:
- `resolve: true` - Include all dependencies
- `resolveConditional: true` - Include conditional dependencies
- `renderer: false` - Exclude renderer modules
- `async: true` - Use async require (v4.0+, default)

### Bundle Options

| Option | Description | Default (v3.0+) |
|--------|-------------|-----------------|
| `optimize` | Minify bundle | true |
| `sourceMap` | Generate source map | false |
| `decorateBootstrapModule` | Add bootstrap decoration | false |
| `addTryCatchRestartWrapper` | Add error handling wrapper | false |

### Predefine Calls (v4.0+)

**Always Used**: UI5 CLI v4 always uses `sap.ui.predefine` calls in bundles.

**Removed**: `usePredefineCalls` option removed in v4.0.

**Example Bundle Output**:
```javascript
sap.ui.predefine("my/app/Component", ["sap/ui/core/UIComponent"], function(UIComponent) {
    return UIComponent.extend("my.app.Component", {
        // Component code
    });
});

sap.ui.predefine("my/app/controller/Main", ["sap/ui/core/mvc/Controller"], function(Controller) {
    return Controller.extend("my.app.controller.Main", {
        // Controller code
    });
});
```

### Async Require (v4.0+)

**Default Behavior**: `async: true` uses `sap.ui.require` instead of deprecated `sap.ui.requireSync`.

**Configuration**:
```yaml
sections:
  - mode: require
    async: true                        # Default in v4.0
    filters: ["my/app/lazy/**"]
```

**Output**:
```javascript
// async: true (default)
sap.ui.require(["my/app/lazy/Module"]);

// async: false (legacy)
sap.ui.requireSync("my/app/lazy/Module");
```

---

## Legacy Bundle Tooling (LBT)

### Overview

**Deprecated in Specification Version 4.0+**

For projects using Specification Version below 4.0, JavaScript files requiring "top level scope" are packaged as strings and evaluated using `eval` at runtime.

### What is Top Level Scope?

**Code with variables outside module definition**:
```javascript
// This requires "top level scope"
var globalVar = "something";

sap.ui.define([], function() {
    // Uses globalVar from top level
    console.log(globalVar);
});
```

### LBT Bundling (Spec < 4.0)

**String Wrapping**:
```javascript
// Module bundled as string
jQuery.sap.registerPreloadedModules({
    "name": "my/app/Component-preload",
    "modules": {
        "my/app/ProblematicModule.js":
            "var globalVar='something';sap.ui.define([],function(){console.log(globalVar);});"
    }
});

// Evaluated at runtime using eval()
```

### Security & CSP Issues

**Problem**: `eval()` violates Content Security Policy (CSP)

**Impact**: Blocked by CSP in production

### Specification 4.0+ Behavior

**Breaking Change**: Bundling as strings terminated.

**New Behavior**:
- Modules requiring top level scope **cannot be bundled**
- Modules omitted from bundles with error logging
- Build continues but bundle incomplete

**Error Message**:
```
WARN: Skipping module my/app/ProblematicModule.js - requires top level scope
```

### Migration

**Fix Code**:
```javascript
// Before (top level scope)
var globalVar = "something";
sap.ui.define([], function() {
    console.log(globalVar);
});

// After (module scope)
sap.ui.define([], function() {
    var localVar = "something";
    console.log(localVar);
});
```

**Or Exclude from Bundle**:
```yaml
builder:
  componentPreload:
    excludes:
      - "my/app/ProblematicModule.js"
```

---

## Build Optimization

### Component Preload

**Purpose**: Bundle all Component resources for faster loading.

**Configuration**:
```yaml
builder:
  componentPreload:
    namespaces:
      - "my/app"
      - "my/app/reuse"
    excludes:
      - "my/app/thirdparty/**"
      - "my/app/test/**"
```

**Output**: `Component-preload.js` in component directory

**Content**:
- Component.js
- All controllers
- All views (XML, JSON, HTML)
- All fragments
- Manifest.json
- i18n files

**Excludes**:
- Test files
- Third-party libraries
- Files matching exclude patterns

---

### Library Preload

**Purpose**: Bundle all library resources.

**Configuration**:
```yaml
builder:
  libraryPreload:
    excludes:
      - "my/lib/thirdparty/**"
```

**Output**: `library-preload.js` in library directory

**Content**:
- All library modules
- library.js
- Manifest.json (if exists)

---

### Flex Changes Bundle

**Purpose**: Bundle UI flexibility changes.

**Task**: `generateFlexChangesBundle`

**What It Bundles**:
- SAPUI5 Flexibility changes
- UI Adaptation layer modifications
- Variant management data

**Output**: `changes/changes-bundle.json`

**Automatic**: No configuration needed

---

### Theme Building

**Purpose**: Compile LESS to CSS.

**Task**: `buildThemes`

**Process**:
1. Find all `.less` files in `themes/` directories
2. Compile LESS to CSS
3. Resolve theme parameters
4. Apply CSS optimizations
5. Write CSS files

**Configuration**:
```yaml
# No configuration typically needed - automatic
```

**Example**:
```
Input:  src/my/lib/themes/base/library.less
Output: dist/resources/my/lib/themes/base/library.css
```

**CSS Variables** (experimental):
```bash
ui5 build --experimental-css-variables
```

---

## Supported Locales Generation

The `enhanceManifest` task automatically populates `supportedLocales` in manifest.json.

### How It Works

1. Scans project for `.properties` files
2. Detects locale variants (e.g., `i18n_de.properties`)
3. Adds `supportedLocales` array to manifest

### Requirements

- Manifest version **1.21.0+**
- Resource bundles within project namespace
- Properties files follow naming convention

### Example

**Files**:
```
i18n/i18n.properties
i18n/i18n_de.properties
i18n/i18n_fr.properties
i18n/i18n_es.properties
```

**Original manifest.json**:
```json
{
  "_version": "1.21.0",
  "sap.app": {
    "i18n": "i18n/i18n.properties"
  }
}
```

**Enhanced manifest.json**:
```json
{
  "_version": "1.21.0",
  "sap.app": {
    "i18n": {
      "bundleUrl": "i18n/i18n.properties",
      "supportedLocales": ["de", "fr", "es", ""]
    }
  }
}
```

### Troubleshooting

**Issue**: Build fails with "TypeError: invalid input"

**Cause**: Manifest `_version` incompatible with UI5 framework version.

**Solution**: For UI5 1.71, use manifest version ≤ 1.17.0 or update to match framework.

---

## Custom Processors

### Overview

Processors handle actual modification logic on supplied resources. Multiple tasks can use the same processor with different configurations.

### Generic Processors

**String Replacer**:
- Used by `replaceCopyright`, `replaceVersion`, `replaceBuildtime`
- Configurable patterns and replacements

**Minifier**:
- Used by `minify` task
- Based on Terser
- Generates debug variants and source maps

**Bundler**:
- Used by bundle generation tasks
- Supports multiple bundle modes

### Custom Processor Development

**Not Recommended**: Use custom tasks instead of custom processors.

**Reason**: Custom tasks provide simpler API and better integration.

---

## Task Control

### Excluding Tasks

```bash
# Exclude specific tasks
ui5 build --exclude-task minify,buildThemes

# Exclude all tasks
ui5 build --exclude-task=*
```

### Including Tasks

```bash
# Include previously excluded tasks
ui5 build --exclude-task=* --include-task minify,generateComponentPreload
```

### Use Cases

**Fast Build** (no minification):
```bash
ui5 build --exclude-task minify
```

**Component Preload Only**:
```bash
ui5 build --exclude-task=* --include-task generateComponentPreload
```

**Documentation Build**:
```bash
ui5 build jsdoc
```

---

## Build Performance

### Build Manifest

Cache build metadata for reuse:

```bash
ui5 build --create-build-manifest
```

**Creates**: `.ui5/build-manifest.json` with checksums

**Benefit**: Faster incremental builds

### Dependency Building

**Automatic in v3.0+**: If any build task requires dependency resources, dependencies are built upfront.

**Impact**: Slower initial build, ensures correctness

### Optimization Tips

1. **Exclude unnecessary dependencies**:
   ```bash
   ui5 build --exclude-dependency sap.ui.documentation
   ```

2. **Use task control** for faster dev builds:
   ```bash
   ui5 build --exclude-task minify
   ```

3. **Enable build manifest** for incremental builds:
   ```bash
   ui5 build --create-build-manifest
   ```

4. **Parallelize builds** in CI/CD

---

## Best Practices

1. **Use standard build** for development (with task exclusions)
2. **Use full build** for production (`ui5 build --all`)
3. **Always clean destination** for production: `--clean-dest`
4. **Enable source maps** for debugging minified code
5. **Exclude third-party** from minification and bundling
6. **Test self-contained builds** for offline scenarios
7. **Monitor build times** with `--perf` flag
8. **Use build manifest** for faster incremental builds

---

## Troubleshooting

### Build Fails with "Module requires top level scope"
**Solution**: Fix code to avoid top level variables or exclude from bundle

### Source Maps Not Working
**Solution**: Ensure transpilation generates source maps, avoid code modification tasks before minification

### Slow Build Times
**Solution**: Exclude unnecessary dependencies, use task control, enable build manifest

### Missing Resources in Output
**Solution**: Check `builder.resources.excludes`, verify resource paths

---

**Last Updated**: 2025-11-21
**Official Docs**: [https://ui5.github.io/cli/stable/pages/Builder/](https://ui5.github.io/cli/stable/pages/Builder/)

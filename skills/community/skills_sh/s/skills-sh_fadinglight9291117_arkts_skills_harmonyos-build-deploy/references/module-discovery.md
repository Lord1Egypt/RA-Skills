# Module Discovery & Build Outputs

Guide for finding modules in a HarmonyOS project, identifying module types, locating build outputs, and handling unwanted modules.

## Finding Modules

All modules are defined in `build-profile.json5` at the project root, in the `modules` array.

### Module Definition Structure

```json5
{
  "modules": [
    {
      "name": "entry",              // Module name (used in build commands)
      "srcPath": "./entry",         // Module source path (relative to project root)
      "targets": [                  // Build target config (optional)
        {
          "name": "default",
          "applyToProducts": ["default", "app_store"]
        }
      ]
    },
    {
      "name": "my_library",
      "srcPath": "./library/my_library",
      "targets": [...]
    }
  ]
}
```

### Key Fields

| Field | Description |
|-------|-------------|
| `name` | Module name, used in build commands (e.g., `-p module=entry@default`) |
| `srcPath` | Module source path relative to project root |
| `targets` | Build target config, specifies which products this module applies to |

### Module Type Identification

The module type is defined in each module's `module.json5` file:

```json5
// {module}/src/main/module.json5
{
  "module": {
    "name": "entry",
    "type": "entry",    // "entry" = HAP, "shared" = HSP, "har" = HAR
    ...
  }
}
```

| `type` field value | Module Type | Description |
|--------------------|-------------|-------------|
| `"entry"` | **HAP** | Application entry point |
| `"feature"` | **HAP** | Feature module (also a HAP) |
| `"shared"` | **HSP** | Dynamic shared package |
| `"har"` | **HAR** | Static library (compiled into other modules) |

**To identify all module types in a project:**

```bash
# Print the type of every module (excludes resolved dependencies in oh_modules/)
find . -path ./oh_modules -prune -o -path "*/src/main/module.json5" -print \
  | xargs grep -o '"type": *"[a-z]*"'
```

## Finding Module Build Outputs

Module build outputs are located at:

```
{srcPath}/build/default/outputs/default/
```

**Note:** Debug and Release builds output to the same directory. The difference is in the signing configuration used (defined in `build-profile.json5` → `signingConfigs`).

### Output Files

| File | Description |
|------|-------------|
| `{name}-default-signed.hsp` | **Signed HSP** (ready for installation) |
| `{name}-default-unsigned.hsp` | Unsigned HSP |
| `{name}.har` | HAR static library |
| `app/{name}-default.hsp` | Intermediate artifact |
| `mapping/sourceMaps.map` | Source maps for debugging |

### Example

For module `my_library` with `srcPath: "./library/my_library"`:

```
library/my_library/build/default/outputs/default/
├── my_library-default-signed.hsp    ← Signed, ready to install
├── my_library-default-unsigned.hsp
├── my_library.har
├── app/
│   └── my_library-default.hsp
├── mapping/
│   └── sourceMaps.map
└── pack.info
```

### Search Commands

```bash
# Find all signed HSP/HAP outputs
dir /s /b "*-signed.hsp" "*-signed.hap" 2>nul           # Windows
find . -name "*-signed.hsp" -o -name "*-signed.hap"     # Linux/macOS

# Find specific module's output
dir /s /b "{srcPath}\build\default\outputs\default\*"   # Windows
ls -la {srcPath}/build/default/outputs/default/         # Linux/macOS
```

### Notes

1. **Build required**: If `build/` directory doesn't exist, run build first
2. **Project-level outputs**: Complete app bundle is in project root `outputs/` after `assembleApp`
3. **oh_modules outputs**: Dependency modules may have outputs in `oh_modules/@xxx/build/...` (these are resolved dependencies)

## Unwanted Modules in Output Directory

Sometimes HSP files appear in the output directory that are **not listed in `build-profile.json5`**. These modules should not be deployed.

**Cause:** Build scripts or dependency configurations may copy precompiled HSP files to the output directory, even though they are not part of the current build.

**How to identify:**

1. Check `build-profile.json5` → `modules` array
2. If an HSP file in output is not in the modules list, it should be removed before installation

**Solution:** Remove these HSP files before installation:

```bash
# Example: Remove modules not in build-profile.json5
rm outputs/unwanted-module-default-signed.hsp
```

**Note:** Installation will fail with "version code not same" error if these unwanted modules have a different versionCode than the main app. The root cause is that these modules shouldn't be deployed at all.

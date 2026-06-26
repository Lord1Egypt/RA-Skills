# Design Studio Workflow Reference

## Overview

Design Studio is an Eclipse-based IDE. Components:
- **Type Designer** — create/edit type trees
- **Map Designer** — author, test, debug, compile maps
- **Integration Flow Designer (IFD)** — chain maps into Launcher `.msl` system file
- **Database Interface Designer (DID)** — import relational database metadata

## Creating a Type Tree from XSD

1. `File → New → Type Tree`
2. Select **Import from XSD**
3. Browse to `.xsd` file
4. Specify output `.mtt` filename
5. Click Finish
6. **Analyze**: `Tree → Analyze → Structure Only`
7. Fix any errors (warnings are normal)

**Pitfall:** If the XSD has a prolog (XML declaration), ensure the card in Map Designer uses the root `XSD` type — not a child element — as the card type.

## Creating a Type Tree from COBOL Copybook

1. `Tree → Import`
2. Select `.cpy` file
3. Configure:
   - **Byte order**: `NATIVE`, `BIGENDIAN`, or `LITTLEENDIAN`
   - **Code page**: match source system encoding
4. Click Finish
5. Analyze; add component rules for `OCCURS DEPENDING ON` fields

**Known issue (WTX 8.4.1.3):** COBOL importer throws Java exception.
**Workaround:** Use `Tree → Import → COBOL Copybook (deprecated)` importer.

## Creating a Type Tree Manually (Fixed-Width / Delimited)

1. `File → New → Type Tree` → Empty
2. Right-click root → Add Record type
3. Add fields with sizes and data types
4. For delimited: set delimiter character at record or field level
5. Analyze

## Creating a Map

1. `File → New → Map`
2. Map Designer opens with empty From/To panels
3. Right-click From panel → **Add Input Card**
   - Browse to `.mtt`; select root type
   - Set source adapter (File, MQ, BLOB, etc.)
4. Right-click To panel → **Add Output Card**
   - Browse to `.mtt`; select root type
   - Set target adapter
5. Author rules (see expressions reference)
6. Test with sample data

## Authoring Map Rules

- Click an output field in the To panel
- Rule bar activates at top
- **Drag-and-drop** from input field: generates `= InputField` rule automatically
- Type expressions directly in the rule bar
- Right-click → **Insert Function** to browse built-in functions
- Green checkmark = valid rule; red X = syntax error

## Testing in Map Designer

1. Set test input data: right-click input card → **Set Test Data** → browse to sample file
2. Click **Run** (green play button) or `Map → Run`
3. Output appears in output card preview
4. Trace output in the **Trace tab**
5. Errors shown in **Problems tab**

## Compiling Maps

- Single map: `Build → Build Map`
- Full project: `Build → Build Project`
- Compiled `.mmc` output goes to project `/maps` or configured output directory
- Platform-specific: compile on same OS/arch as deployment target

## Integration Flow Designer (IFD)

IFD chains multiple maps into a single executable topology:

1. `File → New → Map System`
2. Drag maps from project into IFD canvas
3. Connect maps (output of map A → input of map B)
4. Configure adapter settings at system level (override card settings)
5. Save → generates `.msl` file
6. Deploy `.msl` + all `.mmc` files to Launcher

**Note:** IFD settings override card-level settings. For ACE deployments, prefer standalone `.mmc` (not `.msl`) to avoid override conflicts.

## Known Issues

| Issue | Version | Workaround |
|---|---|---|
| COBOL importer Java exception | WTX 8.4.1.3 | Use deprecated COBOL importer |
| Choice group input data lost | Various | Apply APAR PI68148 fix pack |
| Map Designer slow on large type trees | Various | Disable real-time analysis; analyze manually |
| `dtxxmlconv` required for pre-v8 `.mtt` | Pre-v8 trees | Run `dtxxmlconv` before opening in Design Studio |

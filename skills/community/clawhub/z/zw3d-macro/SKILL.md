---
name: zw3d-macro
description: Create, edit, validate, and execute ZW3D CAD macro files (.mac). Use when the user needs to write ZW3D macros, convert operations to macro syntax, debug macro issues, generate macro templates, or perform CAD operations in ZW3D through macros. Special triggers - (1) "在 ZW3D 里做 xxx" means write macro for operation xxx then run it in ZW3D; (2) "修改之前的模型" means open existing file and modify parameters (NOT create new file). Supports basic statements, control structures (IF/WHILE/BUFFER), variable assignments, function calls, baseline testing commands, sketch operations, feature creation (extrude, fillet, pattern), and UDF workflows.
---

# ZW3D Macro Writer

This skill helps create and edit ZW3D CAD macro files for automation and testing.

## Quick Start

### Creating a New Macro

1. Start with the template: [assets/macro_template.txt](assets/macro_template.txt)
2. Fill in the header information (Author, Date, Description)
3. Add macro statements between `vxConfigDefault` and `vxConfigRestore`
4. Save with `.mac` extension

### Running Macros in ZW3D

**User convention #1**: When the user says "在 ZW3D 运行宏" (run macro in ZW3D), it means opening the macro file directly with ZW3D executable:

```powershell
Start-Process "zw3d.exe" "path/to/macro.mac"
```

This launches ZW3D and automatically executes the macro, rather than using ZW3D's internal Macro menu.

**User convention #2**: When the user says "在 ZW3D 里做 xxx" (do xxx in ZW3D), it means:
1. Write a macro that performs the operation "xxx"
2. Run the macro in ZW3D

Example workflow:
- User: "在 ZW3D 里创建一个方块"
- Action: Create macro → Save → Run in ZW3D

**User convention #3**: When the user says "修改之前的模型" (modify the previous model), it means:
1. The macro should **NOT** create a new file (`$CdFileNew`)
2. Instead, the macro should open the existing model file and modify its parameters
3. Use file open commands (`$CdFileOpen` or `!CdFileOpen2`) to load the previous model

Example workflow:
- User: "修改之前的模型，把方块长度改为20"
- Action: Create macro (open existing file + modify parameters) → Save → Run in ZW3D

**Editing Features via History Manager:**
When selecting features in the history manager, note that the first number in the parentheses starts from 1 (流水号).

For example, if the history tree contains:
1. Default coordinate system
2. Block feature
3. Fillet feature

Then:
- `(1,1)` - Default coordinate system
- `(2,1)` - Block feature
- `(3,1)` - Fillet feature

Example to select and edit the block feature (which is the 2nd item):
```mac
[vxSendEvt,"UiHistoryManager",220,(2,1),25,4]  # Select block feature
[vxSendEvt,"UiHistoryManager",220,(2,1),4,4]   # Activate edit
[vxSend,"$CdHistEdit"]                          # Enter edit mode
```

### Basic Macro Structure

```mac
# Author -用户名
# Date - Thu Jan 01 00:00:00 2026
# Version - 28
# Description - 宏描述

MACRO main
[QaBlVersion,1]
[vxBuildDate,01/01/2026]
[vxConfigDefault,2800]

# 宏主体
[vxSend,"$CdFileNew"]

[vxConfigRestore]
ENDMACRO
```

### Creating New File with Filename

When creating a new file, provide a filename that matches the macro name:

```mac
[vxSend,"$CdFileNew"]
[vxFormInitGlbl,UiFileNew,"89,1"]
[vxSendEvt,"UiFileNew",1,1,7,"FileNamexxx"]  # Set filename (without extension)
[vxSendEvt,"UiFileNew",-1,0,0]                # Confirm
```

**Note**: The filename should match the macro file name for consistency. For example, if the macro is `create_block_100x100x100.mac`, the filename should be `create_block_100x100x100`.

### Extending View Range for Large Models

When working with large base plates or models (>1m), extend the view range before sketching:

```mac
# After file creation, extend view range to 2000mm
[vxSend,"$SF=UiViewExt"]
[vxSendEvt,"UiViewExt",100,1,7,"2000"]
[vxSendEvt,"UiViewExt",-1,0,0]
```

- `100,1,7,"2000"` - Sets view range to 2000mm
- Adjust the value based on model size (e.g., `"3000"` for 3m models)
- Place this command after opening/creating a file and before sketch operations

## Statement Types

### Command Statements

| Statement | Purpose | Example |
|-----------|---------|---------|
| `vxSend` | Send command | `[vxSend,"$CdFileNew"]` |
| `vxSendEvt` | Send UI event | `[vxSendEvt,"UiFileNew",-1,0,0]` |
| `vxSendEvtOpt` | Send option (OK/Cancel) | `[vxSendEvtOpt,-1,0,1,2]` |
| `vxFormEvtOpt` | Form option event | `[vxFormEvtOpt,"FtFillet2",-1,0,1,2]` |
| `vxSendOptFocus` | Set focus | `[vxSendOptFocus,2,0]` |
| `vxInitCmd` | Init command params | `[vxInitCmd,FtAllBox,<14,0><8,0>]` |
| `vxFormInitGlbl` | Init form params | `[vxFormInitGlbl,UiFileNew,"89,1"]` |
| `vxViewSet2` | Set view | `[vxViewSet2,1,0,0,0,1,0...]` |

### Mouse Operations

```mac
# Left mouse button
[vxSend,"*0,0,0,LMB_DN"]      # Press
[vxSend,"*100,50,0,LMB_UP"]   # Release

# Drag operations
[vxSend,"*50,25,0,DRAG"]      # Drag

# Middle mouse button (view rotation)
[vxSend,"*0,0,0,MMB_DN"]
[vxSend,"*10,10,0,MMB_UP"]
```

### Control Structures

**IF-ELSEIF-ELSE-ENDIF:**
```mac
IF (condition)
    statements
ELSEIF (condition)
    statements
ELSE
    statements
ENDIF
```

**WHILE-ENDWHILE:**
```mac
WHILE (condition)
    statements
ENDWHILE
```

**BUFFER-ENDBUFFER:**
```mac
BUFFER
[vxSend,"!CdFileOpen2"]
[vxSend,"PartA.Z3PRT"]
ENDBUFFER
```

### Variables and Functions

```mac
# Variable assignment
NUMBER1 = 5
SUM = NUMBER1 + NUMBER2

# Function call
FUNCTION cnt = QaFnHistCnt()
FUNCTION redefine = QaFnHistCanInfomRedefine(item)
```

### Debug and Error Handling

```mac
[DebugOn]              # Enable step-by-step debugging
+[vxSend,"$CdFileNew"] # Breakpoint on single line
[QaAllowRetry]         # Allow one command failure
[QaExpectError]        # Expect an error (must precede error line)
```

### Baseline Commands

```mac
[QaOutBary,0]     # Output wireframe barycenter
[QaOutEntCnt,1]   # Output entity count
[QaOutHist]       # Output history
```

## Common Command Reference

### File Operations
| Command | Type | Description |
|---------|------|-------------|
| `$CdFileNew` | GUI | New file |
| `$CdFileOpen` | GUI | Open file |
| `!CdFileOpen2` | Template | Open file (template) |
| `~CdUDFDelete` | Special | Delete UDF |

### Sketch & Modeling
| Command | Type | Description |
|---------|------|-------------|
| `!CdProfNew` | Template | New sketch |
| `!WrCrRects` | Template | Draw rectangle |
| `!WrCrNgons` | Template | Draw polygon |
| `!FtAllBox` | Template | Create box |
| `!FtAllExt` | Template | Extrude feature |
| `!FtFillet2` | Template | Fillet (圆角) |
| `!FtChamfers2` | Template | Chamfer (倒角) |
| `!FtPtnFtr` | Template | Pattern feature |
| `$CdEditParent` | GUI | Edit parent feature |

### Creating a New Sketch

**Correct format for creating a new sketch:**
```mac
[vxSend,"!CdProfNew"]
[vxInitCmd,CdMatInpSk,<4,0><19,0><11,0><6,1><5,0>]
BUFFER
[vxSendEvtOpt,-1,0,1,2] # Ok
ENDBUFFER
```

### Exiting a Sketch

**Correct format for exiting a sketch:**
```mac
[vxSend,"$CdEditParent"]
```

### Drawing a Polygon

**Correct format for drawing a polygon (e.g., hexagon):**
```mac
[vxSend,"!WrCrNgons"]
[vxInitCmd,WrCrNgons,<15,0><2,10><8,10><3,6>]
[vxSendEvtOpt,1,0,1,6,"0,0<mm>"] # Center point
[vxSendOptFocus,2,0]              # Focus on radius field
[vxSendEvtOpt,2,0,1,6,"8.5"]      # Set radius
[vxSendEvtOpt,-1,0,1,2]           # Ok
```

### UDF Operations
| Command | Type | Description |
|---------|------|-------------|
| `~CdUDFWizardShow` | Special | UDF wizard |
| `~CdUDFInsShow` | Special | Insert UDF |
| `UiUDFWizard` | UI | UDF wizard UI |
| `UiUDFWizardFtr` | UI | UDF feature selection |
| `UiUDFIns` | UI | UDF insert UI |

### Selecting Sketch for Extrusion

**Correct format for selecting a sketch from history manager before extrusion:**
```mac
[vxSendEvt,"UiHistoryManager",220,(2,1),14,4]  # Select sketch (2nd item in history)
[vxSendEvt,"UiHistoryManager",220,(2,1),2,4]   # Activate for feature operation
```

- `(2,1)` - Refers to the 2nd item in history tree (the sketch)
- `14,4` - Select/highlight the feature
- `2,4` - Activate the feature for subsequent operations (extrude, etc.)

**Note**: Always select the sketch from history manager before using `!FtAllExt` for extrusion.

### UI Managers
| Command | Description |
|---------|-------------|
| `UiHistoryManager` | History manager |
| `UiManager` | UI manager |
| `UiInputManager` | Input manager |

### View Settings

**Setting View Range (for large models):**
When working with large base plates or models, extend the view range before sketching:

```mac
[vxSend,"$SF=UiViewExt"]
[vxSendEvt,"UiViewExt",100,1,7,"2000"]
[vxSendEvt,"UiViewExt",-1,0,0]
```

- `100,1,7,"2000"` - Sets view range to 2000mm
- Adjust the value based on model size (e.g., `"3000"` for 3m models)
- Place this command after opening/creating a file and before sketch operations

## Important Rules

1. **Always include `[vxConfigRestore]`** before `ENDMACRO` - missing this affects other macros
2. **Auto-reordering**: `vxInitCmd`, `vxFormInitGlbl`, `QaAllowRetry` execute one line earlier than written
3. **BUFFER behavior**: Non-`vxSend` statements in BUFFER get wrapped as `FormCommand`
4. **First baseline**: New macros need local execution to generate `[QaBlVersion,1]`
5. **Command prefixes**: `$`=GUI, `!`=Template, `~`=Special

## Parameter Quick Reference

### FtAllBox
- `<8,0>` - Corner type, `<8,1>` - Center type

**Combine Method Options:**
```mac
[vxSendEvtOpt,14,0,1,2]    # Base body (基体)
[vxSendEvtOpt,14,0,2,2]    # Boolean Add (布尔加)
[vxSendEvtOpt,14,0,3,2]    # Boolean Subtract (布尔减)
```

**Setting Dimensions (Length/Width/Height):**
```mac
[vxSendOptFocus,3,0]             # Focus on Length field
[vxSendEvtOpt,3,0,1,6,"100"]     # Set Length = 100
[vxSendEvtOpt,3,0,-1,6,"100"]    # Confirm Length

[vxSendOptFocus,4,0]             # Focus on Width field
[vxSendEvtOpt,4,0,1,6,"100"]     # Set Width = 100
[vxSendEvtOpt,4,0,-1,6,"100"]    # Confirm Width

[vxSendOptFocus,5,0]             # Focus on Height field
[vxSendEvtOpt,5,0,1,6,"100"]     # Set Height = 100
[vxSendEvtOpt,5,0,-1,6,"100"]    # Confirm Height
```

### FtAllExt
- `<2,0>` - Direction, `<3,15>` - Depth

### FtFillet2 (圆角)
- `<6,0.5>` - Radius, `<16,3>` - Edge select mode

**Fillet Workflow:**
```mac
[vxSend,"!FtFillet2"]
[vxInitCmd,FtFillet2,<30,0><42,0><3,0><7,0><48,0><6,10><23,10><44,0><5,0><27,0><35,0><28,0><24,0><21,0><16,3><17,2><46,1><47,1><57,1>]
[vxInitCmd,FtFlltEdgSet,<2,5><22,0><6,0>]

# Select edges
[vxSend,"*50,50,50,LMB_DN"]
[vxSend,"*50,50,50,LMB_UP"]

# Confirm fillet
[vxFormEvtOpt,"FtFillet2",-1,0,1,2]
```

### FtChamfers2 (倒角)
- `<95,5>` - Chamfer type, `<23,10>` - Distance/Angle mode
- `<41,3>` - Edge select mode

**Chamfer Workflow (Manual Edge Selection):**
```mac
[vxSend,"!FtChamfers2"]
[vxInitCmd,FtChamfers2,<30,0><42,0><93,0><95,5><5,0><44,0><27,0><35,0><88,0><28,0><24,0><21,0><23,10><41,3><16,3><17,2><53,0>]
[vxInitCmd,FtChamEdgSet,<2,5><4,45><5,20><22,0><6,0>]

# Switch to edge selection mode
[vxSendEvtOpt,1,2,1,2]

# Select edges (or use more pick for multiple)
[vxSend,"*50,50,50,LMB_DN"]
[vxSend,"*50,50,50,LMB_UP"]

# Confirm chamfer
[vxFormEvtOpt,"FtChamfers2",-1,0,1,2]
```

**Chamfer Workflow (Automatic Edge Selection - Recommended):**
```mac
[vxSend,"!FtChamfers2"]
[vxInitCmd,FtChamfers2,<30,0><42,0><93,0><95,5><5,0><44,0><27,0><35,0><88,0><28,0><24,0><21,0><23,10><41,3><16,3><17,2><53,0>]
# Chamfer
[vxInitCmd,FtChamEdgSet,<2,2><4,45><5,2><22,0><6,0>]
[vxSend,"~CdFiMorePick"]  # Auto-select all available edges
[vxFormEvtOpt,"FtChamfers2",-1,0,1,2]  # Ok
```

**FtChamEdgSet Parameters:**
- `<2,5>` - Edge set type (manual), `<2,2>` - Edge set type (auto)
- `<4,45>` - Angle (45 degrees)
- `<5,20>` - Distance (20mm)
- `<22,0>` - Symmetric mode
- `<6,0>` - Additional options

**Tip:** Use `~CdFiMorePick` for automatic edge selection when chamfering all hole edges or similar features.

### FtPtnFtr
- `<3,2>` - Circular pattern, `<3,3>` - Linear pattern
- `<4,20>` - Count, `<12,45>` - Angle/Spacing

## Examples

This SKILL.md contains comprehensive macro examples embedded directly in the documentation. See the sections below for:

- **Table Creation Pattern** - Desktop + 4 legs
- **Base Plate Creation Pattern** - Large rectangular base with extrusion
- **Cube with All Edges Filleted** - Block + fillet on all 12 edges
- **Vertical Edges Fillet** - Selective filleting
- **Threaded Hole Creation** - M10, M18.5, etc.
- **Through Hole Creation** - Center spindle holes
- **Corner Counterbore Guide Pin Holes** - Position calculations
- **High-Precision Fixture Base Plate** - Complete complex example
- **Pattern Feature Arrays** - 3×3, 5×5 rectangular patterns

A basic template is also available: [assets/macro_template.txt](assets/macro_template.txt)

### Table Creation Pattern

The table example demonstrates a complete workflow:
1. **Desktop**: Sketch rectangle → Extrude (1000×600×30)
2. **Legs**: One sketch with 4 rectangles → Extrude all (50×50×700)
3. **Positioning**: Legs placed at (±425, ±250) inside desktop corners

Key techniques:
- Multiple rectangles in one sketch for legs
- `PntDirZ` for direction control in extrusion
- Coordinate calculation for proper positioning

### Base Plate Creation Pattern (Large Rectangle)

The base plate example demonstrates creating a large rectangular base (1170×1150×30mm):

```mac
# Author - Jarvis
# Date - Mon Mar 30 11:23:00 2026
# Version - 28
# Description - 创建底座 1170x1150x30mm

MACRO main
[QaBlVersion,1]
[vxBuildDate,03/30/2026]
[vxConfigDefault,2800]

[vxSend,"$CdFileNew"]
[vxFormInitGlbl,UiFileNew,"89,1"]
[vxSendEvt,"UiFileNew",1,1,7,"base_1170x1150"]
[vxSendEvt,"UiFileNew",-1,0,0]

# 创建草图
[vxSend,"!CdProfNew"]
[vxInitCmd,CdMatInpSk,<4,0><19,0><11,0><6,1><5,0>]
BUFFER
[vxSendEvtOpt,-1,0,1,2]
ENDBUFFER

# 绘制矩形 (1170x1150) - 使用中心点模式
[vxSend,"!WrCrRects"]
[vxInitCmd,WrCrRects,<15,1>]
[vxSendEvtOpt,1,0,1,6,"-585,-575<mm>"]  # 中心点坐标 (-L/2, -W/2)
[vxSendOptFocus,5,0]
[vxSendEvtOpt,5,0,1,6,"1170"]  # 宽度
[vxSendOptFocus,6,0]
[vxSendEvtOpt,6,0,1,6,"1150"]  # 高度
[vxSendEvtOpt,-1,0,1,2]

# 退出草图
[vxSend,"$CdEditParent"]

# 选择草图 (历史管理器中第 2 项)
[vxSendEvt,"UiHistoryManager",220,(2,1),14,4]  # 选中草图
[vxSendEvt,"UiHistoryManager",220,(2,1),2,4]   # 激活

# 拉伸特征 (高度 30mm)
[vxSend,"!FtAllExt"]
[vxInitCmd,FtAllExt,<30,0><42,0><2,0><3,15><5,0><44,0><27,0><35,0><28,0><24,0><21,0>]
[vxSendOptFocus,5,0]
[vxSendEvtOpt,5,0,1,6,"30"]  # 拉伸深度
[vxSendEvtOpt,-1,0,1,2]

[vxConfigRestore]
ENDMACRO
```

**Key techniques:**
- `<15,1>` - Center point mode for rectangle (vs `<15,0>` for corner mode)
- Center point calculation: `(-L/2, -W/2)` to center the rectangle at origin
- History manager selection required before extrude: `(2,1)` refers to the sketch (2nd item in history)
- `!FtAllExt` for extrusion with depth parameter `<3,15>` and focus on field 5

**Important notes:**
- Always select the sketch from history manager before extruding using `UiHistoryManager` events
- The first number in `(2,1)` is the history item number (流水号), starting from 1
- Use `$CdEditParent` to exit sketch mode before selecting and extruding

### Cube with All Edges Filleted Pattern

This example demonstrates creating a 100×100×100mm cube with fillets on all 12 edges:

```mac
# Author - Jarvis
# Date - Mon Mar 30 14:02:00 2026
# Version - 28
# Description - 创建 100x100x100 方块 + 所有边圆角

MACRO main
[QaBlVersion,1]
[vxBuildDate,03/30/2026]
[vxConfigDefault,2800]

[vxSend,"$CdFileNew"]
[vxFormInitGlbl,UiFileNew,"89,1"]
[vxSendEvt,"UiFileNew",1,1,7,"block_100x100x100"]
[vxSendEvt,"UiFileNew",-1,0,0]

# 创建草图
[vxSend,"!CdProfNew"]
[vxInitCmd,CdMatInpSk,<4,0><19,0><11,0><6,1><5,0>]
BUFFER
[vxSendEvtOpt,-1,0,1,2]
ENDBUFFER

# 绘制矩形 (100x100) - 使用中心点模式
[vxSend,"!WrCrRects"]
[vxInitCmd,WrCrRects,<15,1>]
[vxSendEvtOpt,1,0,1,6,"-50,-50<mm>"]
[vxSendOptFocus,5,0]
[vxSendEvtOpt,5,0,1,6,"100"]
[vxSendOptFocus,6,0]
[vxSendEvtOpt,6,0,1,6,"100"]
[vxSendEvtOpt,-1,0,1,2]

# 退出草图
[vxSend,"$CdEditParent"]

# 选择草图 (历史管理器中第 2 项)
[vxSendEvt,"UiHistoryManager",220,(2,1),14,4]
[vxSendEvt,"UiHistoryManager",220,(2,1),2,4]

# 拉伸特征 (高度 100mm)
[vxSend,"!FtAllExt"]
[vxInitCmd,FtAllExt,<30,0><42,0><2,0><3,15><5,0><44,0><27,0><35,0><28,0><24,0><21,0>]
[vxSendOptFocus,3,0]
[vxSendEvtOpt,3,0,1,6,"100"]
[vxSendEvtOpt,-1,0,1,2]

# 添加圆角 - 所有 12 条边
[vxSend,"!FtFillet2"]
[vxInitCmd,FtFillet2,<30,0><42,0><3,0><7,0><48,0><6,5><23,10><44,0><5,0><27,0><35,0><28,0><24,0><21,0><16,3><17,2><46,1><47,1><57,1>]
[vxInitCmd,FtFlltEdgSet,<2,5><22,0><6,0>]

# 选择所有边 - 方块的 12 条边
# 底面四条边 (Z=0)
[vxSend,"*-50,-50,0,LMB_DN"]
[vxSend,"*-50,-50,0,LMB_UP"]
[vxSend,"*50,-50,0,LMB_DN"]
[vxSend,"*50,-50,0,LMB_UP"]
[vxSend,"*50,50,0,LMB_DN"]
[vxSend,"*50,50,0,LMB_UP"]
[vxSend,"*-50,50,0,LMB_DN"]
[vxSend,"*-50,50,0,LMB_UP"]

# 顶面四条边 (Z=100)
[vxSend,"*-50,-50,100,LMB_DN"]
[vxSend,"*-50,-50,100,LMB_UP"]
[vxSend,"*50,-50,100,LMB_DN"]
[vxSend,"*50,-50,100,LMB_UP"]
[vxSend,"*50,50,100,LMB_DN"]
[vxSend,"*50,50,100,LMB_UP"]
[vxSend,"*-50,50,100,LMB_DN"]
[vxSend,"*-50,50,100,LMB_UP"]

# 垂直四条边 (Z=50 中点)
[vxSend,"*-50,-50,50,LMB_DN"]
[vxSend,"*-50,-50,50,LMB_UP"]
[vxSend,"*50,-50,50,LMB_DN"]
[vxSend,"*50,-50,50,LMB_UP"]
[vxSend,"*50,50,50,LMB_DN"]
[vxSend,"*50,50,50,LMB_UP"]
[vxSend,"*-50,50,50,LMB_DN"]
[vxSend,"*-50,50,50,LMB_UP"]

# 确认圆角
[vxFormEvtOpt,"FtFillet2",-1,0,1,2]

[vxConfigRestore]
ENDMACRO
```

**Key techniques:**
- **Coordinate system**: Sketch center is at the **bottom face center** of the cube (origin = 0,0,0)
- **Bottom edges**: Z = 0 (four edges of the base sketch)
- **Top edges**: Z = 100 (four edges at the top face)
- **Vertical edges**: Z = 50 (midpoint of each vertical edge)
- **Edge selection**: Use `*-X,-Y,Z,LMB_DN/UP` format for precise edge picking
- **Fillet radius**: Set via `<6,5>` parameter (5mm radius in this example)

**Important notes:**
- All 12 edges must be selected before confirming the fillet
- Edge coordinates are relative to the sketch origin (bottom face center)
- Use `vxFormEvtOpt` with form name "FtFillet2" to confirm the fillet operation
- The `<16,3>` parameter sets edge selection mode to manual pick
- **Setting fillet radius**: Use `[vxSendEvtOpt,2,0,1,6,"50"]` to set radius (field 2)

### Vertical Edges Fillet Pattern (Large Base)

This example demonstrates creating a 300×300×300mm base with fillets on the 4 vertical edges only:

```mac
# Author - Jarvis
# Date - Mon Mar 30 14:10:00 2026
# Version - 28
# Description - 创建 300x300x300 基座 + 垂直边圆角

MACRO main
[QaBlVersion,1]
[vxBuildDate,03/30/2026]
[vxConfigDefault,2800]

[vxSend,"$CdFileNew"]
[vxFormInitGlbl,UiFileNew,"89,1"]
[vxSendEvt,"UiFileNew",1,1,7,"base_300x300x300"]
[vxSendEvt,"UiFileNew",-1,0,0]

# 创建草图
[vxSend,"!CdProfNew"]
[vxInitCmd,CdMatInpSk,<4,0><19,0><11,0><6,1><5,0>]
BUFFER
[vxSendEvtOpt,-1,0,1,2]
ENDBUFFER

# 绘制矩形 (300x300) - 使用中心点模式
[vxSend,"!WrCrRects"]
[vxInitCmd,WrCrRects,<15,1>]
[vxSendEvtOpt,1,0,1,6,"-150,-150<mm>"]
[vxSendOptFocus,5,0]
[vxSendEvtOpt,5,0,1,6,"300"]
[vxSendOptFocus,6,0]
[vxSendEvtOpt,6,0,1,6,"300"]
[vxSendEvtOpt,-1,0,1,2]

# 退出草图
[vxSend,"$CdEditParent"]

# 选择草图 (历史管理器中第 2 项)
[vxSendEvt,"UiHistoryManager",220,(2,1),14,4]
[vxSendEvt,"UiHistoryManager",220,(2,1),2,4]

# 拉伸特征 (高度 300mm)
[vxSend,"!FtAllExt"]
[vxInitCmd,FtAllExt,<30,0><42,0><2,0><3,15><5,0><44,0><27,0><35,0><28,0><24,0><21,0>]
[vxSendOptFocus,3,0]
[vxSendEvtOpt,3,0,1,6,"300"]
[vxSendEvtOpt,-1,0,1,2]

# 添加圆角 - 仅垂直的 4 条边
[vxSend,"!FtFillet2"]
[vxInitCmd,FtFillet2,<30,0><42,0><3,0><7,0><48,0><6,50><23,10><44,0><5,0><27,0><35,0><28,0><24,0><21,0><16,3><17,2><46,1><47,1><57,1>]
[vxInitCmd,FtFlltEdgSet,<2,5><22,0><6,0>]

# 设置圆角半径
[vxSendEvtOpt,2,0,1,6,"50"]  # Radius R

# 选择垂直 4 条边 (Z=150 中点)
[vxSend,"*-150,-150,150,LMB_DN"]
[vxSend,"*-150,-150,150,LMB_UP"]
[vxSend,"*150,-150,150,LMB_DN"]
[vxSend,"*150,-150,150,LMB_UP"]
[vxSend,"*150,150,150,LMB_DN"]
[vxSend,"*150,150,150,LMB_UP"]
[vxSend,"*-150,150,150,LMB_DN"]
[vxSend,"*-150,150,150,LMB_UP"]

# 确认圆角
[vxFormEvtOpt,"FtFillet2",-1,0,1,2]

[vxConfigRestore]
ENDMACRO
```

**Key techniques:**
- **Selective filleting**: Only the 4 vertical edges are filleted (not top/bottom edges)
- **Vertical edge coordinates**: Z = 150 (midpoint of 300mm height)
- **Corner positions**: (±150, ±150, 150) for the four vertical edges
- **Radius setting**: Use `[vxSendEvtOpt,2,0,1,6,"50"]` to set fillet radius on field 2
- **Large radius**: R50mm creates substantial rounding on the vertical edges

**Important notes:**
- Set the radius using `vxSendEvtOpt` on field 2 before or after edge selection
- Only select the edges you want to fillet (vertical edges in this case)
- The same workflow applies for any base size - adjust coordinates proportionally

### Threaded Hole Creation Pattern

This example demonstrates creating a threaded hole (M10 × 1.25) at the center of the top face:

```mac
# 在顶面中心创建螺纹孔 (M18 x 1.5)
[vxSend,"!FtHoleMain"]
[vxInitCmd,FtHoleMain,<6,2><21,0><121,0><25,16.5><27,34.5><29,15><31,5><33,90><70,10><23,0><55,118><94,30><95,0><110,1><10,0><75,1><16,1><11,0><61,1><40,1.5><41,0><168,1><63,27><167,1><73,1><72,0><74,1><101,0><102,0>]
# Create hole feature
[vxFormInitGlbl,FtHoleChamForm,"0, 0, 0.75, 45, 0, 0, 0, 0, 0, 0, 0.75, 45"]
[vxFormInitGlbl,FtHoleMParaForm,",0,0,0,0,0,0,0,1"]
[vxSendEvtOpt,6,0,3,2]  # Hole type (threaded)
[vxFormInitGlbl,FtHoleThrdForm,"M,M18 x 1.5,1,18,27,1.5,0"]
[vxSendEvtOpt,3,0,1,6,"0,0,200<mm>"]  # Location (use coordinate instead of mouse pick)
[vxSendEvt,"FtHoleThrdForm",165,45,2]  # Select thread type
[vxSendEvtOpt,-1,0,1,2]  # Ok
```

**Important:** Use `vxSendEvtOpt,3,0,1,6,"X,Y,Z<mm>"` to set hole location directly with coordinates instead of mouse picking. This is more reliable, especially for pattern arrays.

### Through Hole Creation Pattern (Center Spindle Hole)

This example demonstrates creating a large diameter through hole (Ø200mm) at the center of the base plate:

```mac
# 创建中心主轴通孔 (直径 200mm)
[vxSend,"!FtHoleMain"]
[vxInitCmd,FtHoleMain,<6,1><21,0><121,0><25,10.5><27,34.5><29,15><31,5><33,90><70,10><23,0><55,118><94,30><95,0><110,1><10,0><75,1><16,1><11,0><61,1><40,1.5><41,0><168,1><63,-1e-06><167,1><73,1><72,0><74,1><101,0><102,0>]
# Create hole feature
[vxFormInitGlbl,FtHoleScrewForm,"ISO,General Screw Clearance,M10,Close"]
[vxFormInitGlbl,FtHoleChamForm,"0, 0, 0.6, 45, 0, 0, 0, 0, 0, 0, 0.6, 45"]
[vxFormInitGlbl,FtHoleMParaForm,",0,0,0,0,0,0,0,1"]
[vxSendEvtOpt,6,0,1,2]  # Hole type
[vxSendEvtOpt,3,0,1,6,"0,0,335<mm>"]  # Location (top face center)
[vxSendEvtOpt,3,0,-1,6,"0,0,335<mm>"]  # Location (confirm)
[vxSendOptFocus,25,0]  # Dia (D1)
[vxSendEvtOpt,25,0,1,6,"200"]  # Dia (D1)
[vxSendOptFocus,27,0]  # Depth (H1)
[vxSendEvtOpt,27,0,1,6,"335"]  # Depth (H1)
[vxSendEvtOpt,-1,0,1,2]  # Ok
```

**Key techniques:**
- **Through hole type**: `<6,1>` sets counterbore hole type, `<63,-1e-06>` indicates through hole (negative micro value)
- **Screw form**: `FtHoleScrewForm` with `"ISO,General Screw Clearance,M10,Close"` for clearance hole specification
- **Diameter setting**: Use field 25 to set the hole diameter (e.g., 200mm for spindle hole)
- **Depth setting**: Use field 27 to set the depth (equal to plate thickness for through hole)
- **Location confirmation**: Send location twice (once with `1,6`, once with `-1,6`) to confirm
- **Hole type selection**: Use `vxSendEvtOpt,6,0,1,2` to select the hole type from dialog

**Common hole types:**
```mac
<vxInitCmd,FtHoleMain,<6,0>...]  # Simple hole (简单孔)
<vxInitCmd,FtHoleMain,<6,1>...]  # Counterbore hole (沉头孔)
<vxInitCmd,FtHoleMain,<6,2>...]  # Threaded hole (螺纹孔)
```

**Important notes:**
- For through holes, set depth equal to the plate thickness or use negative micro value `<63,-1e-06>`
- Large diameter holes (like spindle holes) use the same workflow as standard holes
- Always confirm location by sending the position twice
- Use `FtHoleScrewForm` for clearance holes, `FtHoleThrdForm` for threaded holes

### Corner Counterbore Guide Pin Holes Pattern

This example demonstrates creating four counterbore guide pin holes (R66.5mm) at the corners of a base plate with rounded corners:

```mac
# 四角沉头导柱孔 (半径 66.5mm)
# 导柱孔 1 - 左下角 (-468.5, -458.5) - 往原点偏移 66.5mm
[vxSend,"!FtHoleMain"]
[vxInitCmd,FtHoleMain,<6,1><21,0><121,0><25,66.5><27,34.5><29,15><31,5><33,90><70,10><23,0><55,118><94,30><95,0><110,1><10,0><75,1><16,1><11,0><61,1><40,1.5><41,0><168,1><63,-1e-06><167,1><73,1><72,0><74,1><101,0><102,0>]
[vxFormInitGlbl,FtHoleScrewForm,"ISO,General Screw Clearance,M10,Close"]
[vxFormInitGlbl,FtHoleChamForm,"0, 0, 0.6, 45, 0, 0, 0, 0, 0, 0, 0.6, 45"]
[vxFormInitGlbl,FtHoleMParaForm,",0,0,0,0,0,0,0,1"]
[vxSendEvtOpt,6,0,1,2]
[vxSendEvtOpt,3,0,1,6,"-468.5,-458.5,335<mm>"]
[vxSendEvtOpt,3,0,-1,6,"-468.5,-458.5,335<mm>"]
[vxSendOptFocus,25,0]
[vxSendEvtOpt,25,0,1,6,"133"]  # Diameter (2 × radius)
[vxSendOptFocus,27,0]
[vxSendEvtOpt,27,0,1,6,"335"]  # Depth (through hole)
[vxSendEvtOpt,-1,0,1,2]

# 导柱孔 2 - 右下角 (468.5, -458.5)
[vxSend,"!FtHoleMain"]
[vxInitCmd,FtHoleMain,<6,1>...<63,-1e-06>...]  # Same parameters
[vxSendEvtOpt,3,0,1,6,"468.5,-458.5,335<mm>"]
[vxSendEvtOpt,3,0,-1,6,"468.5,-458.5,335<mm>"]
[vxSendEvtOpt,25,0,1,6,"133"]
[vxSendEvtOpt,27,0,1,6,"335"]
[vxSendEvtOpt,-1,0,1,2]

# 导柱孔 3 - 右上角 (468.5, 458.5)
# 导柱孔 4 - 左上角 (-468.5, 458.5)
```

**Key techniques:**
- **Counterbore through hole**: `<6,1>` (counterbore type) + `<63,-1e-06>` (through hole)
- **Position offset**: Corner hole positions should offset toward origin by the hole radius to avoid interference with rounded corners
  - Example: For a 1170×1150 plate with R120 corners and R66.5 holes:
  - Corner position: (±535, ±525)
  - Offset by radius: 535 - 66.5 = 468.5, 525 - 66.5 = 458.5
  - Final positions: (±468.5, ±458.5)
- **Diameter setting**: Field 25 for diameter (133mm = 2 × 66.5mm radius)
- **Depth setting**: Field 27 for depth (335mm = plate thickness for through hole)
- **Location confirmation**: Send position twice (positive and negative) for through holes

**Position calculation for corner holes:**
```
Plate half-width:  1170 / 2 = 585mm
Plate half-height: 1150 / 2 = 575mm
Corner fillet:     R120mm
Hole radius:       R66.5mm

Edge distance:     50mm from edge (585 - 50 = 535, 575 - 50 = 525)
Offset by radius:  535 - 66.5 = 468.5, 525 - 66.5 = 458.5

Final positions:   (±468.5, ±458.5)
```

**Important notes:**
- Always offset corner hole positions toward the origin by the hole radius
- This prevents the hole from extending beyond the plate boundary
- Use the same workflow for all four corners, only changing X/Y signs
- For different plate sizes, recalculate positions using the formula above

### High-Precision Fixture Base Plate Template (Complete Example)

This comprehensive example demonstrates creating a complete high-precision fixture base plate with all common features:

**Specifications:**
- Dimensions: 1170 × 1150 × 335mm
- Corner fillets: R120mm
- Center spindle hole: Ø200mm (through hole)
- Corner guide pin holes: Ø133mm (R66.5mm, counterbore, through)
- Top surface threaded holes: M18.5×2.0, four 5×5 arrays, 70mm spacing
- All threaded hole edges: 2mm chamfer

```mac
# Author - Jarvis
# Date - Tue Apr 07 11:57:00 2026
# Version - 28
# Description - 高精度工装夹具基板 1170x1150x335 + R120 圆角 + 中心主轴孔 + 四角导柱孔 + M18.5 螺纹孔阵列 + 2mm 倒角

MACRO main
[QaBlVersion,1]
[vxBuildDate,04/07/2026]
[vxConfigDefault,2800]

[vxSend,"$CdFileNew"]
[vxFormInitGlbl,UiFileNew,"89,1"]
[vxSendEvt,"UiFileNew",1,1,7,"fixture_base_1170x1150x335"]
[vxSendEvt,"UiFileNew",-1,0,0]

# 扩展视图范围到 2000 (重要！大型模型必须)
[vxSend,"$SF=UiViewExt"]
[vxSendEvt,"UiViewExt",100,1,7,"2000"]
[vxSendEvt,"UiViewExt",-1,0,0]

# ===== 步骤 1: 创建基板主体 =====
[vxSend,"!CdProfNew"]
[vxInitCmd,CdMatInpSk,<4,0><19,0><11,0><6,1><5,0>]
BUFFER
[vxSendEvtOpt,-1,0,1,2]
ENDBUFFER

# 绘制矩形 (1170x1150) - 使用中心点模式
[vxSend,"!WrCrRects"]
[vxInitCmd,WrCrRects,<15,1>]
[vxSendEvtOpt,1,0,1,6,"-585,-575<mm>"]
[vxSendOptFocus,5,0]
[vxSendEvtOpt,5,0,1,6,"1170"]
[vxSendOptFocus,6,0]
[vxSendEvtOpt,6,0,1,6,"1150"]
[vxSendEvtOpt,-1,0,1,2]

[vxSend,"$CdEditParent"]

# 选择草图并拉伸
[vxSendEvt,"UiHistoryManager",220,(2,1),14,4]
[vxSendEvt,"UiHistoryManager",220,(2,1),2,4]

[vxSend,"!FtAllExt"]
[vxInitCmd,FtAllExt,<30,0><42,0><2,0><3,15><5,0><44,0><27,0><35,0><28,0><24,0><21,0>]
[vxSendOptFocus,3,0]
[vxSendEvtOpt,3,0,1,6,"335"]
[vxSendEvtOpt,-1,0,1,2]

# ===== 步骤 2: 四角圆角 R120mm =====
[vxSend,"!FtFillet2"]
[vxInitCmd,FtFillet2,<30,0><42,0><3,0><7,0><48,0><6,120><23,10><44,0><5,0><27,0><35,0><28,0><24,0><21,0><16,3><17,2><46,1><47,1><57,1>]
[vxInitCmd,FtFlltEdgSet,<2,5><22,0><6,0>]
[vxSendEvtOpt,2,0,1,6,"120"]

# 选择 4 条垂直边
[vxSend,"*-585,-575,167.5,LMB_DN"]
[vxSend,"*-585,-575,167.5,LMB_UP"]
[vxSend,"*585,-575,167.5,LMB_DN"]
[vxSend,"*585,-575,167.5,LMB_UP"]
[vxSend,"*585,575,167.5,LMB_DN"]
[vxSend,"*585,575,167.5,LMB_UP"]
[vxSend,"*-585,575,167.5,LMB_DN"]
[vxSend,"*-585,575,167.5,LMB_UP"]

[vxFormEvtOpt,"FtFillet2",-1,0,1,2]

# ===== 步骤 3: 四角沉头导柱孔 (半径 66.5mm, 直径 133mm) =====
# 导柱孔位置计算：向原点偏移半径距离
# 左下角 (-468.5, -458.5)
[vxSend,"!FtHoleMain"]
[vxInitCmd,FtHoleMain,<6,1><21,0><121,0><25,66.5><27,34.5><29,15><31,5><33,90><70,10><23,0><55,118><94,30><95,0><110,1><10,0><75,1><16,1><11,0><61,1><40,1.5><41,0><168,1><63,-1e-06><167,1><73,1><72,0><74,1><101,0><102,0>]
[vxFormInitGlbl,FtHoleScrewForm,"ISO,General Screw Clearance,M10,Close"]
[vxFormInitGlbl,FtHoleChamForm,"0, 0, 0.6, 45, 0, 0, 0, 0, 0, 0, 0.6, 45"]
[vxFormInitGlbl,FtHoleMParaForm,",0,0,0,0,0,0,0,1"]
[vxSendEvtOpt,6,0,1,2]
[vxSendEvtOpt,3,0,1,6,"-468.5,-458.5,335<mm>"]
[vxSendEvtOpt,3,0,-1,6,"-468.5,-458.5,335<mm>"]
[vxSendOptFocus,25,0]
[vxSendEvtOpt,25,0,1,6,"133"]
[vxSendOptFocus,27,0]
[vxSendEvtOpt,27,0,1,6,"335"]
[vxSendEvtOpt,-1,0,1,2]

# 右下角 (468.5, -458.5)
# 右上角 (468.5, 458.5)
# 左上角 (-468.5, 458.5)
# ... (repeat for other 3 corners with adjusted coordinates)

# ===== 步骤 4: 上表面 M18.5 螺纹孔阵列 (5x5, 间距 70mm) =====
# 左上角阵列 (-400, 400) - 使用 vxSendEvtOpt 设置位置 (不要用鼠标点击)
[vxSend,"!FtHoleMain"]
[vxInitCmd,FtHoleMain,<6,2><21,0><121,0><25,16.5><27,34.5><29,15><31,5><33,90><70,10><23,0><55,118><94,30><95,0><110,1><10,0><75,1><16,1><11,0><61,1><40,1.5><41,0><168,1><63,27><167,1><73,1><72,0><74,1><101,0><102,0>]
[vxFormInitGlbl,FtHoleChamForm,"0, 0, 0.75, 45, 0, 0, 0, 0, 0, 0, 0.75, 45"]
[vxFormInitGlbl,FtHoleMParaForm,",0,0,0,0,0,0,0,1"]
[vxSendEvtOpt,6,0,3,2]
[vxFormInitGlbl,FtHoleThrdForm,"M,M18.5 x 2.0,1,18.5,27,2.0,0"]
[vxSendEvtOpt,3,0,1,6,"-400,400,335<mm>"]  # 关键：用坐标设置位置
[vxSendEvt,"FtHoleThrdForm",165,45,2]
[vxSendEvtOpt,-1,0,1,2]

# 左上角 5x5 阵列 (第一方向 +X, 第二方向 -Y)
[vxSend,"!FtPtnFtr"]
[vxInitCmd,FtPtnFtr,<10,0><3,2><4,20><12,45><93,360><6,1><7,20><18,1><19,0><17,0><28,0><31,0><9,0><40,3><41,0><42,20><43,1><44,20><45,0><60,0><48,0><49,0><59,0><63,0><65,0><66,0.1><67,15><69,0><70,0><71,0><75,0><72,0><74,0><76,0><78,0><83,0><84,0><85,0><87,0><89,0><91,0><92,0><126,0><127,0>]
[vxSendEvt,"UiManager",1,0,2,"UiHistoryManager"]
[vxSendEvt,"UiHistoryManager",220,(9,1),14,4]
[vxSendEvt,"UiHistoryManager",220,(9,1),2,4]
[vxSendEvt,"UiManager",1,0,2,"UiInputManager"]
[vxSendOptFocus,2,0]
[vxSendEvtOpt,2,0,1,6,"1,0,0<mm>"]
[vxSendOptFocus,4,0]
[vxSendEvtOpt,4,0,1,6,"70"]
[vxSendEvtOpt,3,0,1,6,"5"]
[vxSendEvtOpt,51,0,1,2]
[vxSendOptFocus,5,0]
[vxSendEvtOpt,5,0,1,6,"0,-1,0<mm>"]
[vxSendOptFocus,6,0]
[vxSendEvtOpt,6,0,1,6,"5"]
[vxSendOptFocus,7,0]
[vxSendEvtOpt,7,0,1,6,"70"]
[vxSendEvtOpt,-1,0,1,2]

# 右上角 (400, 400)、右下角 (400, -400)、左下角 (-400, -400) 阵列
# ... (repeat for other 3 corners with adjusted positions and directions)

# ===== 步骤 5: 中心主轴穿孔 (直径 200mm) =====
[vxSend,"!FtHoleMain"]
[vxInitCmd,FtHoleMain,<6,1><21,0><121,0><25,10.5><27,34.5><29,15><31,5><33,90><70,10><23,0><55,118><94,30><95,0><110,1><10,0><75,1><16,1><11,0><61,1><40,1.5><41,0><168,1><63,-1e-06><167,1><73,1><72,0><74,1><101,0><102,0>]
[vxFormInitGlbl,FtHoleScrewForm,"ISO,General Screw Clearance,M10,Close"]
[vxFormInitGlbl,FtHoleChamForm,"0, 0, 0.6, 45, 0, 0, 0, 0, 0, 0, 0.6, 45"]
[vxFormInitGlbl,FtHoleMParaForm,",0,0,0,0,0,0,0,1"]
[vxSendEvtOpt,6,0,1,2]
[vxSendEvtOpt,3,0,1,6,"0,0,335<mm>"]
[vxSendEvtOpt,3,0,-1,6,"0,0,335<mm>"]
[vxSendOptFocus,25,0]
[vxSendEvtOpt,25,0,1,6,"200"]
[vxSendOptFocus,27,0]
[vxSendEvtOpt,27,0,1,6,"335"]
[vxSendEvtOpt,-1,0,1,2]

# ===== 步骤 6: 对所有孔边缘做 2mm 倒角 (使用全选模式) =====
[vxSend,"!FtChamfers2"]
[vxInitCmd,FtChamfers2,<30,0><42,0><93,0><95,5><5,0><44,0><27,0><35,0><88,0><28,0><24,0><21,0><23,10><41,3><16,3><17,2><53,0>]
[vxInitCmd,FtChamEdgSet,<2,2><4,45><5,2><22,0><6,0>]
[vxSend,"~CdFiMorePick"]  # 自动选择所有边缘
[vxFormEvtOpt,"FtChamfers2",-1,0,1,2]

[vxConfigRestore]
ENDMACRO
```

**Key techniques:**

1. **View range extension (Critical for large models):**
   - Always extend view range to 2000mm+ for models >1m
   - Use `$SF=UiViewExt` before sketch operations
   - Prevents sketch visibility issues

2. **Base plate with filleted corners:**
   - Create rectangle sketch at center (center-point mode `<15,1>`)
   - Extrude to full height
   - Add fillets to 4 vertical edges

3. **Counterbore guide pin holes:**
   - Position offset toward origin by hole radius
   - Use `<6,1>` for counterbore type
   - Use `<63,-1e-06>` for through hole
   - Confirm location twice (positive and negative)

4. **Threaded hole arrays (4 corners):**
   - Start position: (±400, ±400, 335)
   - Array directions point toward center
   - 5×5 grid with 70mm spacing
   - **Use `vxSendEvtOpt,3,0,1,6,"X,Y,Z<mm>"` for location** (NOT mouse pick)

5. **Center spindle hole:**
   - Large diameter through hole (Ø200mm)
   - Use `FtHoleScrewForm` for clearance hole
   - Confirm location twice (positive and negative)

6. **Chamfer all hole edges:**
   - Use `~CdFiMorePick` for automatic edge selection
   - Much faster than manual edge picking for 100+ holes

**Array direction summary:**

| Corner | Start Position | Direction 1 | Direction 2 |
|--------|---------------|-------------|-------------|
| Top-Left | (-400, 400, 335) | `1,0,0` (+X) | `0,-1,0` (-Y) |
| Top-Right | (400, 400, 335) | `-1,0,0` (-X) | `0,-1,0` (-Y) |
| Bottom-Right | (400, -400, 335) | `-1,0,0` (-X) | `0,1,0` (+Y) |
| Bottom-Left | (-400, -400, 335) | `1,0,0` (+X) | `0,1,0` (+Y) |

**Important notes:**
- This template includes all common fixture base features
- Adjust dimensions, hole sizes, and array spacing as needed
- Threaded hole creation requires specific syntax (see Threaded Hole Creation Pattern)
- Array directions should point toward the plate center for symmetrical clamping
- Total threaded holes: 4 × 25 = 100 holes (M18.5×2.0)
- **Always use coordinate-based location for threaded holes** - mouse picking is unreliable for arrays

**Key techniques:**
- **Hole command**: `!FtHoleMain` for creating threaded holes
- **Thread specification**: `FtHoleThrdForm` with format `"M,M10 x 1.25,1,10,15,1.25,0"`
  - `M` = Metric thread type
  - `M10 x 1.25` = Thread size (diameter × pitch)
  - `1` = Full thread depth
  - `10` = Nominal diameter
  - `15` = Thread depth
  - `1.25` = Pitch
- **Location**: Set via `vxSendEvtOpt,3,0,1,6,"X,Y,Z<mm>"` (field 3)
- **Chamfer form**: `FtHoleChamForm` for entrance/exit chamfers
- **Measurement form**: `FtHoleMParaForm` for hole parameters

**Common thread sizes:**
- M6 × 1.0: `"M,M6 x 1.0,1,6,10,1.0,0"`
- M8 × 1.25: `"M,M8 x 1.25,1,8,12,1.25,0"`
- M10 × 1.25: `"M,M10 x 1.25,1,10,15,1.25,0"`
- M12 × 1.75: `"M,M12 x 1.75,1,12,18,1.75,0"`

**Important notes:**
- Location coordinates are in absolute WCS (World Coordinate System)
- For blind holes, adjust the thread depth parameter accordingly
- The `<6,2>` parameter in `FtHoleMain` sets the hole type to threaded hole
- Use `[vxSendEvt,"FtHoleThrdForm",165,45,2]` to select the thread type before confirming
- Chamfer form parameters: `"0, 0, 0.75, 45, 0, 0, 0, 0, 0, 0, 0.75, 45"` for entrance/exit chamfers
- **Through holes**: Use `<63,-1e-06>` and set depth equal to plate thickness
- **Location confirmation**: Send position twice for through holes (once positive, once negative)

### Modifying Existing Pattern Feature

**Correct format for modifying an existing pattern feature:**
```mac
[vxSendEvt,"UiHistoryManager",220,(10,1),25,4]
[vxSendEvt,"UiHistoryManager",220,(10,1),4,4]
# Popup Menu Name : UiPartFtr
[vxSend,"$CdHistEdit"]
BUFFER
ENDBUFFER
# Success to quick rollback to Pattern Feature1=4932, time=0.06 sec
# Default settings updated.
[vxInitCmd,FtPtnFtr,<10,0><3,5><4,70><12,45><93,360><6,5><7,70><18,1><19,0><17,0><28,0><31,0><9,0><40,3><41,0><42,20><43,1><44,20><45,0><60,0><48,0><49,0><59,0><63,0><65,0><66,0.1><67,15><69,0><70,0><71,0><75,0><72,0><74,0><76,0><78,0><83,0><84,0><85,0><87,0><89,0><91,0><92,0><126,0><127,0>]
# Pattern feature
[vxSendOptFocus,3,0] # Number
[vxSendEvtOpt,3,0,1,6,"10"] # Number
[vxSendOptFocus,6,0] # Number N
[vxSendEvtOpt,6,0,1,6,"10"] # Number N
[vxSendEvtOpt,-1,0,1,2] # Ok
# Default settings updated.
```

**Key points:**
- Use `BUFFER/ENDBUFFER` for quick rollback to the pattern feature
- Re-initialize with `FtPtnFtr` command to update default settings
- Modify parameters using `vxSendOptFocus` and `vxSendEvtOpt`
- Field 3 = Number (first direction count)
- Field 6 = Number N (second direction count)
- Field 4 = Spacing (first direction)
- Field 7 = Spacing S (second direction)

### Pattern Feature (3x3 Hole Array) Pattern

This example demonstrates creating a 3×3 rectangular pattern of holes with 50mm spacing:

```mac
# 阵列孔特征 (3x3, 间距 250mm)
[vxSend,"!FtPtnFtr"]
[vxInitCmd,FtPtnFtr,<10,0><3,2><4,20><12,45><93,360><6,1><7,20><18,1><19,0><17,0><28,0><31,0><9,0><40,3><41,0><42,20><43,1><44,20><45,0><60,0><48,0><49,0><59,0><63,0><65,0><66,0.1><67,15><69,0><70,0><71,0><75,0><72,0><74,0><76,0><78,0><83,0><84,0><85,0><87,0><89,0><91,0><92,0><126,0><127,0>]
# Pattern feature
[vxSendEvt,"UiManager",1,0,2,"UiHistoryManager"]
[vxSendEvt,"UiHistoryManager",220,(4,1),14,4]  # 选择螺纹孔特征
[vxSendEvt,"UiHistoryManager",220,(4,1),2,4]
[vxSendEvt,"UiManager",1,0,2,"UiInputManager"]
[vxSendOptFocus,2,0]  # Direction
[vxSendEvtOpt,2,0,1,6,"1,0,0<mm>"]  # X 方向
[vxSendOptFocus,4,0]  # Spacing
[vxSendEvtOpt,4,0,1,6,"250"]  # Spacing
[vxSendEvtOpt,3,0,1,6,"3"]  # Number
[vxSendEvtOpt,51,0,1,2]  # Second direction
[vxSendOptFocus,5,0]  # Direction D
[vxSendEvtOpt,5,0,1,6,"0,1,0<mm>"]  # Y 方向
[vxSendEvtOpt,6,0,1,6,"3"]  # Number N
[vxSendOptFocus,7,0]  # Spacing S
[vxSendEvtOpt,7,0,1,6,"250"]  # Spacing S
[vxSendEvtOpt,-1,0,1,2]  # Ok
```

**Key techniques:**
- **Pattern command**: `!FtPtnFtr` for creating rectangular/circular patterns
- **Pattern type**: `<3,2>` sets rectangular pattern (use `<3,3>` for circular)
- **History selection**: Select the source feature (hole) from history manager before setting pattern parameters
  - `(4,1)` refers to the 4th item in history (the source hole feature)
- **First direction**:
  - Field 2: Direction vector - use coordinates `"1,0,0<mm>"` for X axis
  - Field 3: Number of instances (3)
  - Field 4: Spacing (250mm)
- **Second direction**:
  - Use `vxSendEvtOpt,51,0,1,2` to enable second direction
  - Field 5: Direction D - use coordinates `"0,1,0<mm>"` for Y axis
  - Field 6: Number N (3)
  - Field 7: Spacing S (250mm)
- **Direction vectors**: Use coordinate format `"X,Y,Z<mm>"` instead of mouse picking for reliability

**Pattern type options:**
```mac
<vxInitCmd,FtPtnFtr,<3,2>...]  # Rectangular pattern (矩形阵列)
<vxInitCmd,FtPtnFtr,<3,3>...]  # Circular pattern (圆形阵列)
```

**Important notes:**
- Always select the source feature from history manager before configuring pattern parameters
- **Use coordinate vectors for directions**: `"1,0,0<mm>"` (X axis) and `"0,1,0<mm>"` (Y axis)
- Coordinate-based direction setting is more reliable than mouse picking
- Mouse picking requires `vxViewSet2` for proper view orientation - avoid when possible
- For circular patterns, use angle instead of spacing: `<12,45>` = 45° angular spacing
- Order of operations: Direction → Spacing → Number (for each axis)

## Full Syntax Reference

For detailed syntax documentation, see [references/syntax_reference.md](references/syntax_reference.md).

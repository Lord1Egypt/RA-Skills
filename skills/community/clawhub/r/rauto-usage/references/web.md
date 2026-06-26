# Rauto Web UI Reference (Full Map + Examples)

Use this file when the user asks for Web operations.

## Table of Contents

1. Start and access
2. Connection area
3. Top tabs
4. Drawers and overlays
5. Common task recipes

## 1) Start and access

```bash
rauto web --bind 127.0.0.1 --port 3000
```

Open:

```text
http://127.0.0.1:3000
```

## 2) Connection area

### Saved Connections

- Input: `saved connection name`
- Actions:
  - `Save`
  - `Delete`
  - `History`
- Behavior:
  - Typing name supports fuzzy select via datalist
  - Selecting existing name auto-loads connection values

### Connection Defaults

- Inputs:
  - `host`
  - `port`
  - `username`
  - `password`
  - `enable password`
  - `device profile`
- Action:
  - `Test Connection`

## 3) Top tabs

### Operations

- Execute mode:
  - `Direct Execute`
  - `Template Render + Execute`
- Tx mode:
  - `Tx Block`
  - `Tx Workflow`

#### Direct Execute

- Inputs: command, mode(optional)
- Action: `Execute`

#### Template Render + Execute

- Inputs: template, vars JSON, mode(optional)
- Actions:
  - `Preview Render`
  - `Run Template`

#### Tx Block

- Inputs: template/commands/vars/mode and rollback controls
- Actions:
  - `Preview Tx Plan`
  - `Execute Tx Block`

#### Tx Workflow

- Builder actions:
  - add/copy/delete/reorder blocks
  - generate/load/download/import JSON
- Execute actions:
  - `Preview Workflow`
  - `Execute Workflow`

### Interactive

- Actions:
  - `Start Session`
  - `Send`
  - `Stop Session`
  - `Clear`

### Session Replay

- Inputs: JSONL, command, mode(optional)
- Actions:
  - `List Records`
  - `Replay Command`

### Prompt Profiles

- Modes:
  - `View`
  - `Edit`
  - `Diagnose`
- Builtin:
  - load detail
  - copy to custom edit form
- Custom:
  - save/delete profile
- Diagnose:
  - view visualized diagnostics

### Template Manager

- Search/select template
- Edit content
- Actions:
  - `Save`
  - `Delete`

### Backup

- Create area:
  - optional output path
  - `Create`
  - `Refresh`
- Restore/download area:
  - select archive
  - `Download`
  - `Restore (Merge)`
  - `Restore (Replace)`
- List area:
  - click row to select
  - row-level direct actions:
    - `Download`
    - `Restore (Merge)`
    - `Restore (Replace)`

## 4) Drawers and overlays

- Floating language button (bottom-right)
- Recording drawer (REC floating ball)
- History drawer (from saved connection `History`)
- Entry detail drawer/modal for replay/history rows

## 5) Common task recipes

### Recipe A: Use saved connection then execute

1. Saved Connections: choose existing name
2. Operations -> Direct Execute
3. Fill command and click `Execute`

### Recipe B: Template preview before run

1. Operations -> Template Render + Execute
2. Choose template and vars JSON
3. Click `Preview Render`
4. Click `Run Template`

### Recipe C: Tx workflow with safer flow

1. Operations -> Tx -> Tx Workflow
2. Build blocks and rollback policies
3. Preview first
4. Execute and inspect result section

### Recipe D: Multi-device orchestration

1. Operations -> Tx -> Orchestrate
2. Paste orchestration JSON and optional `base_dir`
3. Click `Preview Orchestration`
4. Click `Execute Orchestration`
5. Inspect stage/target result cards and open detail views when needed

### Recipe E: Restore backup safely

1. Backup tab -> select archive row
2. Use `Restore (Merge)` first
3. Use `Restore (Replace)` only when full replacement is intended

# Preview Reference

Comprehensive reference for previewing SAP Fiori applications during development.

## Table of Contents

1. [Preview Overview](#preview-overview)
2. [NPM Scripts](#npm-scripts)
3. [Run Control](#run-control)
4. [Mock Data](#mock-data)
5. [Live Data](#live-data)
6. [App-to-App Navigation](#app-to-app-navigation)
7. [External FLP Preview](#external-flp-preview)
8. [Developer Variants](#developer-variants)
9. [SAP Horizon Theme](#sap-horizon-theme)
10. [Virtual Endpoints](#virtual-endpoints)
11. [CAP Project Preview](#cap-project-preview)

---

## Preview Overview

SAP Fiori tools provides multiple preview options:

| Method | Use Case |
|--------|----------|
| NPM Scripts | Quick terminal-based preview |
| Run Control | IDE-integrated launch configurations |
| Context Menu | Right-click folder quick commands |

### Default Preview Port

Applications run on `localhost:8080` by default. If port is in use, system selects next available port.

### HTTPS/SSL Considerations

- `localhost` serves as HTTP proxy to backend services
- Domain security policies may require HTTPS
- Configure browser to trust local certificates if needed

---

## NPM Scripts

### Available Scripts

| Script | Command | Description |
|--------|---------|-------------|
| start | `npm start` | Live data from backend OData service |
| start-mock | `npm run start-mock` | Mock data via MockServer |
| start-local | `npm run start-local` | Mock data + local SAPUI5 resources |
| start-noflp | `npm run start-noflp` | Without Fiori launchpad sandbox |

### Running Scripts

**VS Code**:
1. Open terminal: `Ctrl + `` `
2. Navigate to project root
3. Run script: `npm run start-mock`

**SAP Business Application Studio**:
1. Open terminal: Terminal > New Terminal
2. Navigate to project root
3. Run script: `npm run start-mock`

**Context Menu**:
Right-click project folder and select from available scripts.

---

## Run Control

### Configuration Location

```
<workspace_root>/.vscode/launch.json
```

**Important**: Run Control only searches root-level `.vscode/` folder, not subfolders.

### Sample launch.json

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Start app-name",
            "type": "node",
            "request": "launch",
            "runtimeExecutable": "npm",
            "runtimeArgs": ["run", "start"],
            "cwd": "${workspaceFolder}",
            "console": "integratedTerminal"
        },
        {
            "name": "Start app-name (mock)",
            "type": "node",
            "request": "launch",
            "runtimeExecutable": "npm",
            "runtimeArgs": ["run", "start-mock"],
            "cwd": "${workspaceFolder}",
            "console": "integratedTerminal"
        }
    ]
}
```

### Multi-Root Workspace

Multiple configurations can be merged:
1. Add folders as workspace roots
2. Each root's `launch.json` configurations become available
3. Access via Run and Debug view

### Creating Run Configurations

**VS Code**:
```
Fiori: Create Run Configuration (VS Code)
```

**SAP Business Application Studio**:
```
Fiori: Create Run Configuration (BAS)
```

---

## Mock Data

### MockServer Setup

Install MockServer:
```
Fiori: Install MockServer
```

Or manually:
```bash
npm install @sap-ux/ui5-middleware-fe-mockserver --save-dev
```

### Mock Data Location

```
webapp/localService/mockdata/
├── EntitySet.json
├── AssociatedEntitySet.json
└── ...
```

### Mock Data Format

```json
[
    {
        "ID": "1",
        "Name": "Product 1",
        "Price": 100.00,
        "Currency": "USD"
    },
    {
        "ID": "2",
        "Name": "Product 2",
        "Price": 200.00,
        "Currency": "EUR"
    }
]
```

### Data Editor

Visual mock data management tool.

**Launch**:
Via Application Info page > Start Data Editor

**Features**:
- Edit cells by double-clicking (primary/foreign keys excluded)
- Add rows with automatic cascading to related entities
- Delete rows with cascading deletions
- Search functionality
- Show/hide columns

**Configuration for Live Updates**:

Add to `ui5-mock.yaml`:
```yaml
server:
  customMiddleware:
    - name: "@sap-ux/ui5-middleware-fe-mockserver"
      configuration:
        watch: true
```

### AI Mock Data Generation

Generate contextual mock data using entity property names.

**Requirements**:
- SAP Build Code subscription or Test Drive access
- EDMX project with `metadata.xml` file

**Launch**:
Via Page Editor > Generate Mock Data action

---

## Live Data

### Configuration

Live data preview connects to actual backend OData services.

**Requirements**:
- Backend system accessible
- Authentication configured
- Destination set up (BAS) or system connection (VS Code)

### Start Command

```bash
npm start
```

### ui5.yaml Configuration

```yaml
server:
  customMiddleware:
    - name: fiori-tools-proxy
      afterMiddleware: compression
      configuration:
        backend:
          - path: /sap
            url: https://backend.system.com
            destination: BACKEND_DESTINATION
```

---

## App-to-App Navigation

### Enable Navigation Preview

```
Fiori: Enable App-to-App Navigation Preview
```

### Configuration Steps

1. Execute command via Command Palette
2. Select source application
3. Select destination application(s)
4. Launch source app preview
5. Execute navigation

### Generated Files

**Source Application**:
- `appconfig/fioriSandboxConfig.json` - FLP sandbox configuration
- Updated `ui5.yaml` - Middleware configuration

### fioriSandboxConfig.json Structure

```json
{
    "applications": {
        "destination-app-semantic-object-action": {
            "additionalInformation": "SAPUI5.Component=namespace.destination",
            "applicationType": "URL",
            "url": "../destination-app/",
            "title": "Destination App"
        }
    }
}
```

### Requirements

- Both applications in same workspace
- Configured external navigation in source app
- Matching semantic objects and actions

---

## External FLP Preview

### Purpose

Preview application within actual SAP Fiori launchpad environment.

### Configuration

```
Fiori: Preview on External Fiori Launchpad
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| FLP URL | URL of target Fiori launchpad |
| Semantic Object | Application semantic object |
| Action | Navigation action |

### Use Cases

- Test FLP-dependent features
- Verify tile configuration
- Test cross-application navigation

---

## Developer Variants

### Purpose

Create and test page variants during development.

### Creating Variants

```
Fiori: Create Developer Variant
```

### Variant Types

- Filter variants
- Table variants
- Page variants

### Storage

Developer variants stored locally, not deployed to backend.

---

## SAP Horizon Theme

### Preview with Horizon Theme

```
Fiori: Preview with SAP Horizon Theme
```

### About SAP Horizon

SAP Horizon is SAP's evolved design language with:
- Modern visual design
- Improved accessibility
- Enhanced user experience

### Theme Variants

| Theme | Description |
|-------|-------------|
| sap_horizon | Light theme |
| sap_horizon_dark | Dark theme |
| sap_horizon_hcb | High contrast black |
| sap_horizon_hcw | High contrast white |

---

## Virtual Endpoints

### Purpose

Convert project to use virtual endpoints for simplified proxy configuration.

### Convert Command

```
Fiori: Convert to Virtual Endpoints
```

### Benefits

- Simplified destination configuration
- Consistent endpoint naming
- Easier multi-system setup

### Configuration Update

Updates `ui5.yaml` with virtual endpoint mappings.

---

## CAP Project Preview

### Prerequisites

- CAP project with `cds` dependencies
- Node.js or Java runtime
- Database configured (SQLite for development)

### Starting Preview

**Node.js CAP**:
```bash
cds watch
```

**Java CAP**:
```bash
mvn spring-boot:run
```

### Fiori Preview in CAP

From CAP project root:
```bash
npm run start
```

Or use Run Control with CAP-specific configuration.

### Supported Templates for CAP

- List Report Object Page (OData V4)
- Analytical List Page (OData V4)

### CAP-Specific ui5.yaml

```yaml
specVersion: "2.4"
metadata:
  name: cap-app
type: application
server:
  customMiddleware:
    - name: fiori-tools-proxy
      afterMiddleware: compression
      configuration:
        backend:
          - path: /odata/v4
            url: http://localhost:4004
```

---

## Custom Middlewares

### Adding Custom Middleware

Create custom server middleware for specialized preview needs.

### Configuration

In `ui5.yaml`:
```yaml
server:
  customMiddleware:
    - name: my-custom-middleware
      afterMiddleware: compression
      configuration:
        option1: value1
```

### Use Cases

- Custom authentication handling
- Request/response modification
- Logging and debugging
- Feature flags

---

## Troubleshooting

### Port Already in Use

System automatically selects next available port. Check terminal output for actual port.

### SSL Certificate Errors

Configure browser to trust localhost certificates or use HTTP for development.

### Backend Connection Failed

1. Verify destination/system configuration
2. Check authentication credentials
3. Confirm backend service is accessible
4. Review proxy configuration in ui5.yaml

### Mock Data Not Loading

1. Verify MockServer is installed
2. Check mock data file names match entity sets
3. Validate JSON syntax in mock data files
4. Ensure metadata.xml is present

---

## Documentation Source

**GitHub**: [https://github.com/SAP-docs/btp-fiori-tools/tree/main/docs/Previewing-an-Application](https://github.com/SAP-docs/btp-fiori-tools/tree/main/docs/Previewing-an-Application)

Key files:
- `previewing-an-application-b962685.md`
- `use-mock-data-bda83a4.md`
- `use-live-data-497aee2.md`
- `generating-mock-data-with-ai-815c310.md`
- `run-control-overview-d7f20f3.md`
- `app-to-app-navigation-preview-543675f.md`
- `preview-an-application-on-external-sap-fiori-launchpad-c789692.md`
- `developer-variant-creation-ceb845a.md`
- `preview-an-application-with-the-sap-horizon-theme-2a42256.md`
- `use-custom-middlewares-dce5315.md`
- `previewing-an-sap-fiori-elements-cap-project-1dc179a.md`

---
name: skill
description: Use when needing to interact with Jenkins CI/CD via REST API - triggering builds, listing projects, or checking build results
---

# Jenkins Skill

## Overview

A modular skill package for interacting with Jenkins via REST API. Each feature can be called independently, and AI will guide you step by step.

**Interaction rule:** All user selections and inputs MUST use the `question` tool with interactive buttons. Users can scroll through options or type directly in the input box (e.g., enter an ID). Never ask the user to type commands or names manually.

### Prerequisites

The following environment variables must be configured:

| Environment Variable | Description | Example |
|---------------------|-------------|---------|
| `JENKINS_USER` | Jenkins username | `admin` |
| `JENKINS_API_TOKEN` | Jenkins API Token | `11a2...` |

**Note:** Jenkins URL is NOT an environment variable. It is stored per-project in `PROJECTS.md` under the `JENKINS_URL` column. All API calls must extract the Jenkins URL from the project's record in PROJECTS.md.

### Feature Overview

| Feature | Description | Use Case |
|---------|-------------|----------|
| Feature 1: Project Configure | List/Create/Update project configurations | Manage project configuration info |
| Feature 2: Trigger by ID | Select project from list → Confirm → Trigger → Show result | Trigger a Jenkins build |

---

## Smart Entry: Auto Trigger Build

When the user says something like "trigger Jenkins build" or "build" or "jenkins":

1. **Check current project context** — Look at the workspace/project name (e.g., from directory name or user's context)
2. **Search PROJECTS.md** — grep for the project name in PROJECTS.md
3. **If found** → Execute **Feature 2 Step 1** directly, with the matching project pre-selected
4. **If not found** → Inform the user it's not configured yet, then guide them through **Feature 1** (create config) first, then proceed to **Feature 2**

---

## Feature 1: Project Configure

Manage project configuration file (PROJECTS.md), including source code URL, Jenkins URL, etc.

### Step 1: Create or Update Project

Use the `question` tool to let the user choose:

```json
{
  "questions": [{
    "question": "Please select an action:",
    "header": "Project Config",
    "options": [
      {"label": "Create New Project", "description": ""},
      {"label": "Update Existing Project", "description": ""},
      {"label": "Cancel", "description": ""}
    ]
  }]
}
```

Wait for the user's selection before continuing. Based on the selection:
- **Create New Project** → Go directly to Step 3 (skip Step 2)
- **Update Existing Project** → Execute Step 2
- **Cancel** → End

### Step 2: Confirm Project for Update (Only execute this step if the user selected "Update Existing Project")

Read PROJECTS.md and display existing project list:

```bash
cat PROJECTS.md
```

Display all projects in table format (`ID`, `PROJECT_NAME`, `CODE_URL`, `JENKINS_URL`).

Then use the `question` tool for project selection. The tool supports:
- **Scrolling:** Navigate options with arrow keys or mouse wheel
- **Typing ID:** Enter the project ID directly (e.g., `PRJ-001`)

```json
{
  "questions": [{
    "question": "Select a project to update (scroll to select or type ID):",
    "header": "Select Project",
    "options": [
      {"label": "PRJ-001", "description": "my-project | https://github.com/user/repo"},
      {"label": "PRJ-002", "description": "another-project | https://gitlab.com/team/app"}
    ]
  }]
}
```

### Step 3: Configure Project

**Create New Project:**
Ask for the following information in order using the `question` tool (each must include `options`):

```json
{
  "questions": [{
    "question": "Enter project name (e.g., my-project):",
    "header": "Project Name",
    "options": [
      {"label": "Enter project name", "description": ""}
    ]
  }]
}
```

```json
{
  "questions": [{
    "question": "Enter source code repository URL:",
    "header": "Code Repository",
    "options": [
      {"label": "Enter code repository URL", "description": ""}
    ]
  }]
}
```

```json
{
  "questions": [{
    "question": "Enter Jenkins job URL:",
    "header": "Jenkins URL",
    "options": [
      {"label": "Enter Jenkins URL", "description": ""}
    ]
  }]
}
```

Automatically generate project ID (format: `PRJ-001`, `PRJ-002`...) and append to PROJECTS.md.

---

## Feature 2: Trigger Jenkins Build by ID

### Step 1: List Projects and Select

Read PROJECTS.md and display all configured projects:

```bash
cat PROJECTS.md
```

Then use the `question` tool to let the user select a project (scrollable options) or type an ID:

```json
{
  "questions": [{
    "question": "Select a project (scroll up/down to select, or type ID directly):",
    "header": "Select Project",
    "options": [
      {"label": "PRJ-001", "description": "boss-sso | http://..."},
      {"label": "PRJ-002", "description": "jg-merchant | http://..."}
    ]
  }]
}
```

After user selects/enters the ID, look up the project in PROJECTS.md to get its JENKINS_URL:

```bash
PROJECT_LINE=$(grep -i "{project-id}" PROJECTS.md)
JENKINS_URL=$(echo "$PROJECT_LINE" | awk -F'|' '{print $5}' | xargs)

if [ -z "$PROJECT_LINE" ]; then
  echo "Project not found in PROJECTS.md"
  exit 1
fi
```

Then use the Jenkins URL to get project details from Jenkins:

```bash
curl -s -u "$JENKINS_USER:$JENKINS_API_TOKEN" \
  "$JENKINS_URL/api/json" | echo "$(head -c 500)"
```

If project is not found in PROJECTS.md, inform the user.

### Step 2: User Confirmation

Display project info and recent build status, then ask for confirmation:

```json
{
  "questions": [{
    "question": "Confirm triggering build for {project-name}?",
    "header": "Confirm Trigger",
    "options": [
      {"label": "Confirm Trigger", "description": "Trigger build and view results"},
      {"label": "Cancel", "description": "Cancel operation"}
    ]
  }]
}
```

### Step 3: Trigger Build

```bash
curl -s -u "$JENKINS_USER:$JENKINS_API_TOKEN" \
  -X POST "$JENKINS_URL/build" -w "HTTP %{http_code}"
```

### Step 4: View Build Result

Poll build status after trigger. Get the latest build and display result:

```bash
curl -s -u "$JENKINS_USER:$JENKINS_API_TOKEN" \
  "$JENKINS_URL/lastBuild/api/json" | echo "$(head -c 300)"
```

Display in format:

```text
✅ Build triggered/completed
Project: {project-name}
Build #: {build-number}
Status: {SUCCESS/FAILURE/ABORTED/In progress...}
Build URL: {full-build-url}
```

---

## FAQ

### Connection Failed
```text
curl: (7) Failed to connect to {host}
```
- Check if the project's `JENKINS_URL` in PROJECTS.md is correct
- Confirm network accessibility

### Authentication Failed
```text
HTTP 401 Unauthorized
```
- Check `JENKINS_USER` and `JENKINS_API_TOKEN`
- Confirm API Token hasn't expired

### Project Not Found
```text
HTTP 404 Not Found
```
- Confirm project name spelling
- Use Feature 3 to list all projects

### Parameterized Build

Get parameter definitions first:

```bash
curl -s -u "$JENKINS_USER:$JENKINS_API_TOKEN" \
  "$JENKINS_URL/job/{project-name}/api/json" | jq '.property[0].parameterDefinitions[] | {name, description, defaultValue, type}'
```

Trigger with parameters:

```bash
curl -s -u "$JENKINS_USER:$JENKINS_API_TOKEN" \
  -X POST "$JENKINS_URL/job/{project-name}/buildWithParameters" \
  --data-urlencode "param1=value1" \
  --data-urlencode "param2=value2" \
  -w "HTTP %{http_code}"
```

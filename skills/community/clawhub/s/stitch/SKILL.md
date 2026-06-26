# Stitch by Google — MCP Skill

**Stitch** is Google's AI-powered UI design tool (Beta). This skill covers how to interact with Stitch projects and screens via its **Remote MCP server** using the HTTP API.

---

## Authentication

### API Key (Recommended)

Generate your API key at: https://stitch.withgoogle.com/settings (API Keys section)

Set it as an environment variable: `export STITCH_API_KEY=YOUR_STITCH_API_KEY`

All requests go to: `https://stitch.googleapis.com/mcp`

Pass the key via header: `X-Goog-Api-Key: $STITCH_API_KEY`

### Making MCP Calls

Stitch exposes a standard **MCP HTTP endpoint**. To call a tool, POST to the MCP endpoint with the tool name and arguments.

```bash
curl -X POST https://stitch.googleapis.com/mcp \
  -H "Content-Type: application/json" \
  -H "X-Goog-Api-Key: YOUR_STITCH_API_KEY" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "list_projects",
      "arguments": {}
    }
  }'
```

> **Note:** Stitch is a **Remote** MCP server (cloud-hosted), unlike local file-based MCP servers. API Keys persist indefinitely; OAuth tokens expire every ~1 hour.

---

## Available Tools

### Project Management

#### `list_projects`
Lists all Stitch projects accessible to the user.
- **Read-only:** yes
- **Input:**
  - `filter` *(optional, string)*: AIP-160 filter on `view` field. Values: `view=owned` (default), `view=shared`
- **Output:** Array of `Project` objects

```bash
# List all owned projects
curl -X POST https://stitch.googleapis.com/mcp \
  -H "Content-Type: application/json" \
  -H "X-Goog-Api-Key: YOUR_STITCH_API_KEY" \
  -d '{"method":"tools/call","params":{"name":"list_projects","arguments":{}}}'
```

---

#### `create_project`
Creates a new Stitch project (container for UI designs).
- **Read-only:** no (destructive)
- **Input:**
  - `title` *(optional, string)*: Display name of the project
- **Output:** Created `Project` resource with `name`, `title`, and metadata

```bash
curl -X POST https://stitch.googleapis.com/mcp \
  -H "Content-Type: application/json" \
  -H "X-Goog-Api-Key: YOUR_STITCH_API_KEY" \
  -d '{"method":"tools/call","params":{"name":"create_project","arguments":{"title":"My Ad Landing Page"}}}'
```

---

#### `get_project`
Retrieves details of a specific project.
- **Read-only:** yes
- **Input:**
  - `name` *(required, string)*: Resource name. Format: `projects/{project}`. Example: `projects/4044680601076201931`
- **Output:** `Project` resource object

---

### Screen Management

#### `list_screens`
Lists all screens within a Stitch project.
- **Read-only:** yes
- **Input:**
  - `projectId` *(required, string)*: Project ID without `projects/` prefix
- **Output:** Array of `Screen` objects

```bash
curl -X POST https://stitch.googleapis.com/mcp \
  -H "Content-Type: application/json" \
  -H "X-Goog-Api-Key: YOUR_STITCH_API_KEY" \
  -d '{"method":"tools/call","params":{"name":"list_screens","arguments":{"projectId":"4044680601076201931"}}}'
```

---

#### `get_screen`
Retrieves details of a specific screen including HTML, screenshot, and Figma export.
- **Read-only:** yes
- **Input:**
  - `name` *(required)*: `projects/{project}/screens/{screen}`
  - `projectId` *(required, deprecated)*: Project ID without prefix
  - `screenId` *(required, deprecated)*: Screen ID without prefix
  > All three are currently required even though `projectId`/`screenId` are deprecated.
- **Output:** `Screen` object with `htmlCode`, `screenshot`, `figmaExport` download URLs

---

### AI Generation

#### `generate_screen_from_text`
**Generates a new UI screen from a text prompt. Takes a few minutes.**
- **Read-only:** no (destructive)
- **⚠️ Don't retry on connection errors** — generation may still be in progress. Use `get_screen` after a few minutes to check.
- **Input:**
  - `projectId` *(required, string)*
  - `prompt` *(required, string)*: Describe the screen to generate
  - `deviceType` *(optional)*: `MOBILE` | `DESKTOP` | `TABLET` | `AGNOSTIC`
  - `modelId` *(optional)*: `GEMINI_3_FLASH` | `GEMINI_3_1_PRO` *(GEMINI_3_PRO is deprecated)*
- **Output:** Generated `Screen` objects + `SessionOutputComponent` entries (may include suggestions)
  - If `output_components` has suggestions, present them to user. If accepted, call again with the suggestion as the new `prompt`.

```bash
curl -X POST https://stitch.googleapis.com/mcp \
  -H "Content-Type: application/json" \
  -H "X-Goog-Api-Key: YOUR_STITCH_API_KEY" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "generate_screen_from_text",
      "arguments": {
        "projectId": "YOUR_PROJECT_ID",
        "prompt": "A mobile landing page for a Medicare insurance offer with a bold headline, trust badges, and a prominent CTA button",
        "deviceType": "MOBILE",
        "modelId": "GEMINI_3_1_PRO"
      }
    }
  }'
```

---

#### `edit_screens`
Edits existing screens using a text prompt. Takes a few minutes.
- **Read-only:** no (destructive)
- **⚠️ Don't retry on connection errors**
- **Input:**
  - `projectId` *(required, string)*
  - `selectedScreenIds` *(required, string[])*: Screen IDs without `screens/` prefix
  - `prompt` *(required, string)*: Edit instruction
  - `deviceType` *(optional)*
  - `modelId` *(optional)*: `GEMINI_3_FLASH` | `GEMINI_3_1_PRO`
- **Output:** Updated `Screen` objects

---

#### `generate_variants`
Generates design variants of existing screens.
- **Read-only:** no (destructive)
- **⚠️ Don't retry on connection errors**
- **Input:**
  - `projectId` *(required, string)*
  - `selectedScreenIds` *(required, string[])*
  - `prompt` *(required, string)*: Guide variant generation
  - `variantOptions` *(required, object)*: See `VariantOptions` below
  - `deviceType` *(optional)*
  - `modelId` *(optional)*
- **Output:** Variant `Screen` objects

**VariantOptions schema:**
```json
{
  "variantCount": 3,
  "creativeRange": "EXPLORE",
  "aspects": ["COLOR_SCHEME", "LAYOUT"]
}
```
- `variantCount`: 1–5 (default: 3)
- `creativeRange`: `REFINE` | `EXPLORE` | `REIMAGINE`
- `aspects`: `LAYOUT` | `COLOR_SCHEME` | `IMAGES` | `TEXT_FONT` | `TEXT_CONTENT`

---

## Shared Types

### Screen Object
| Field | Type | Description |
|---|---|---|
| `name` | string | Resource name: `projects/{project}/screens/{screen}` |
| `id` | string | *(Deprecated)* Screen ID |
| `title` | string | Screen title |
| `prompt` | string | Prompt used to generate |
| `screenshot` | File | Screenshot image |
| `htmlCode` | File | HTML code of the screen |
| `figmaExport` | File | Figma export file |
| `theme` | DesignTheme | Theme used |
| `deviceType` | DeviceType | Device target |
| `screenMetadata` | ScreenMetadata | Status, agent type, display mode |
| `width` / `height` | string | Screen dimensions |
| `groupId` | string | Group ID for variants |

### File Object
| Field | Type | Description |
|---|---|---|
| `name` | string | `projects/{project}/files/{file}` |
| `downloadUrl` | string | Direct download URL |
| `mimeType` | string | e.g. `image/png`, `text/html` |

### ScreenMetadata
| Field | Values |
|---|---|
| `status` | `IN_PROGRESS` \| `COMPLETE` \| `FAILED` |
| `agentType` | `TURBO_AGENT`, `PRO_AGENT`, `GEMINI_3_AGENT`, etc. |
| `displayMode` | `SCREENSHOT` \| `HTML` \| `CODE` \| `MARKDOWN` \| `STICKY_NOTE` |

---

## Common Workflows

### Generate a new landing page ad creative

```python
import requests
import json

API_KEY = "YOUR_STITCH_API_KEY"
MCP_URL = "https://stitch.googleapis.com/mcp"
HEADERS = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": API_KEY
}

def stitch_call(tool_name, args):
    payload = {
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": args}
    }
    r = requests.post(MCP_URL, headers=HEADERS, json=payload)
    r.raise_for_status()
    return r.json()

# 1. Create a project
project = stitch_call("create_project", {"title": "Medicare Q4 Campaign"})
project_id = project["result"]["name"].split("/")[1]

# 2. Generate initial screen
result = stitch_call("generate_screen_from_text", {
    "projectId": project_id,
    "prompt": "Mobile landing page for Medicare Advantage with emotional headline, plan comparison table, and green CTA button",
    "deviceType": "MOBILE",
    "modelId": "GEMINI_3_1_PRO"
})

# 3. Get screen details once complete
# (generation takes a few minutes — poll with get_screen)
screens = result["result"].get("screens", [])
if screens:
    screen_name = screens[0]["name"]
    # screen_name format: projects/{id}/screens/{screen_id}
    parts = screen_name.split("/")
    project_id = parts[1]
    screen_id = parts[3]
    
    screen = stitch_call("get_screen", {
        "name": screen_name,
        "projectId": project_id,
        "screenId": screen_id
    })
    
    # Download HTML
    html_url = screen["result"]["htmlCode"]["downloadUrl"]
    print(f"HTML download URL: {html_url}")
    
    # Download screenshot
    screenshot_url = screen["result"]["screenshot"]["downloadUrl"]
    print(f"Screenshot URL: {screenshot_url}")
```

### Generate variants for A/B testing

```python
# After generating a base screen, create variants
variants = stitch_call("generate_variants", {
    "projectId": project_id,
    "selectedScreenIds": [screen_id],
    "prompt": "Test different color schemes and CTA button styles",
    "variantOptions": {
        "variantCount": 3,
        "creativeRange": "EXPLORE",
        "aspects": ["COLOR_SCHEME", "TEXT_CONTENT"]
    },
    "deviceType": "MOBILE",
    "modelId": "GEMINI_3_FLASH"
})
```

---

## Tips for Ad Creative Use

- **Effective prompts include:** device type, ad vertical, emotional tone, specific UI components (hero, CTA, trust badges, form)
- **Pixel-perfect HTML:** Use `htmlCode.downloadUrl` to grab the actual HTML — hand it to Marcus for landing page deployment
- **Figma export:** Available via `figmaExport.downloadUrl` for design review
- **Generation takes 2–5 minutes** — don't retry on network errors; check status with `get_screen` → `screenMetadata.status`
- **Model choice:** `GEMINI_3_1_PRO` for highest quality, `GEMINI_3_FLASH` for faster iteration

---

## MCP Client Config (for direct Claude Code / Cursor integration)

```json
{
  "mcpServers": {
    "stitch": {
      "url": "https://stitch.googleapis.com/mcp",
      "headers": {
        "X-Goog-Api-Key": "YOUR_STITCH_API_KEY"
      }
    }
  }
}
```

Or via Claude Code CLI:
```bash
claude mcp add stitch --transport http https://stitch.googleapis.com/mcp \
  --header "X-Goog-Api-Key: YOUR_STITCH_API_KEY" -s user
```

---

## Docs Reference
- Setup & Auth: https://stitch.withgoogle.com/docs/mcp/setup/
- Reference: https://stitch.withgoogle.com/docs/mcp/reference/
- Guide: https://stitch.withgoogle.com/docs/mcp/guide/

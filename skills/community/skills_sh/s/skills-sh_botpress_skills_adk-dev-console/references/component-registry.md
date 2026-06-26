# Component Registry

The Components page (`/components`) lets developers browse, inspect, and install custom webchat components — UI elements the LLM can yield during conversations.

Accessed from the **Components** tab group. Available in both dev and production modes.

## Two-Tab Interface

### Installed Tab

Shows components currently present in the agent's `src/components/` directory.

- Masonry card layout with live component preview (rendered in shadow DOM for style isolation)
- Click a card to expand an overlay with full component details
- Reflects hot-reload changes — components update as source files are modified
- Empty state: "No components installed yet" with guidance to add under `src/components` or pull from the registry

### Registry Tab

Shows available components from the external component registry.

- Same masonry layout as the Installed tab
- Click a card to expand an overlay with installation instructions and metadata
- Empty state: "Registry is empty"

## What Drives the UI

The dev console reads component metadata to render previews:

- **description** — shown alongside the component card
- **props** (Zod schema) — drives the props playground form
- **exampleValues** — seed the preview with realistic data

Components without metadata still appear in the Installed tab but have no preview or props form.

For how to create components, register metadata, and use them in conversations, see the **custom-components** reference in the ADK skill.

## UI Features

- **Shadow DOM previews** — component previews render in isolated shadow DOM to prevent style leaking
- **Loading skeletons** — placeholder cards while fetching components
- **Error states** — red alerts if components fail to load or registry fetch fails
- **Live reload** — listens for component change events and refreshes the gallery

---
name: scholarPlotSkill
description: >
  ScholarPlot AI Academic Figure Generator. Connects via MCP to generate and edit 
  SCI-standard figures, including line charts, bar charts, heatmaps, neural network architectures,
  and experimental flowcharts. Triggers on requests like "generate loss curve", "draw neural network",
  "create experimental flowchart", "edit figure". Requires API key from figure.thirdme.com.
---

# scholarPlotSkill

ScholarPlot is an AI academic figure generation tool designed for researchers. It uses an MCP (Model Context Protocol) server to instantly generate professional, SCI-journal standard figures from natural language descriptions.

## Core Directives

- **MCP Server Dependency**: This skill requires the `scholarplot-sci-figure` MCP server to be configured and running with a valid API key from `https://figure.thirdme.com/mcp`.
- **Intelligent Generation**: Use the `generate_sci_figure` MCP tool to create figures. Always pass a detailed `description`. You can optionally specify `figureType`, `style` (e.g., nature, science, ieee), and exact `dataValues` for data charts.
- **Interactive Editing**: Use the `edit_figure` MCP tool to modify existing figures. Pass the `figureId` and specific `editInstructions` (e.g., "Change the bar color to blue").
- **High-Quality Output**: Return the generated `figureUrl` to the user so they can view and download the high-resolution (300dpi) or vector (SVG) format image. Present the `metadata` cleanly.

## Execution Pipeline

### Step 1: Tool Selection
Determine if the user wants to generate a new figure or edit an existing one based on the conversation context.

### Step 2: Invoke MCP Tool
- **For New Figures**: Call `generate_sci_figure` with the provided descriptions and any available data.
- **For Edits**: Call `edit_figure` with the target `figureId` and instructions.

### Step 3: Present Results
Once the MCP tool returns a response, format the output nicely for the user:
- Display the figure using Markdown image syntax: `![Generated Figure](figureUrl)` (if supported by the client) or provide the direct URL.
- Summarize the metadata (e.g., Type, Style, Resolution).
- Provide the `figureCode` if the user wants to review the underlying representation.

## Configuration Requirements

Users must configure their Claude Desktop (or other MCP-compatible client) with the following in `mcp.json` or `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "scholarplot-sci-figure": {
      "url": "https://figure.thirdme.com/api/mcp-sse?key=YOUR_API_KEY"
    }
  }
}
```

# ScholarPlot - AI Academic Figure Generator

🎯 **Product Introduction**
ScholarPlot is an AI academic figure generation tool specifically designed for researchers. Whether you need data visualization charts for papers, neural network architecture diagrams, experimental flowcharts, or complex mechanism schematic diagrams, ScholarPlot can generate professional figures that meet the publication standards of top SCI journals in seconds.

## 🔬 Why Choose ScholarPlot?

| Pain Points | ScholarPlot Solution |
|---|---|
| Binding figures using Python/R is tedious | Natural language descriptions; AI automatically generates code and figures |
| Figures do not meet journal standards | Built-in style templates for Nature, Science, IEEE, etc. |
| Architecture and flowcharts are hard to draw | Supports various types including mechanism diagrams, architectures, and flowcharts |
| Repeated modifications waste time | Real-time editing, one-click adjustment of styles and data |
| Insufficient figure resolution | Outputs 300dpi high-definition figures, supports SVG vector format |

## 🎨 Supported Figure Types

- 📈 **Data Charts**: Line charts, bar charts, scatter plots, box plots, heatmaps, violin plots, radar charts...
- 🧬 **Mechanism Diagrams**: Molecular pathways, signaling mechanisms, reaction principles...
- 🏗️ **Architecture Diagrams**: Neural network architectures, system frameworks, model structures...
- 📋 **Flowcharts**: Experimental procedures, algorithm flows, methodology schematics...
- 📊 **Comparative Analysis**: Multi-group comparisons, Venn diagrams, Sankey diagrams...

🌐 **Official Website**: [https://figure.thirdme.com](https://figure.thirdme.com)

## 🔌 MCP Integration

ScholarPlot provides an MCP (Model Context Protocol) interface, allowing you to directly call ScholarPlot to generate figures in AI tools like Claude Desktop, Cursor, Dify, and n8n without leaving your workspace.

🌐 **MCP Documentation**: [https://figure.thirdme.com/mcp](https://figure.thirdme.com/mcp)

### 🚀 Quick Start

**Step 1: Get an API Key**
1. Visit the [MCP API Page](https://figure.thirdme.com/mcp)
2. Enter your email address
3. Click the "Generate API Key" button
4. Copy the generated API Key (Please keep it safe; it is tied to your subscription and usage quota)

> ⚠️ Important Note: Please store your API Key securely. Generating a new Key will replace the existing one. If you regenerate the Key, you must update your MCP configuration.

**Step 2: Configure Claude Desktop**
Add the following configuration to your Claude Desktop configuration file `claude_desktop_config.json`:

Configuration file location:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Configuration content:
```json
{
  "mcpServers": {
    "scholarplot-sci-figure": {
      "url": "https://figure.thirdme.com/api/mcp-sse?key=YOUR_API_KEY"
    }
  }
}
```
*Replace `YOUR_API_KEY` with the actual API Key you obtained in Step 1.*

**Step 3: Use in Claude**
After configuration, restart Claude Desktop. You can now ask Claude directly to generate academic research figures.

Example prompts:
> "Please help me generate a line chart showing the Loss curve during deep learning model training, including two curves for Training Loss and Validation Loss. The X-axis is Epoch (1-100), and the Y-axis is the Loss value."
> 
> "Please draw a neural network architecture diagram, containing an input layer, 3 hidden layers (with 128, 64, and 32 neurons respectively), and an output layer."

Claude will automatically call the MCP API to process the request and return a professional academic figure meeting SCI journal standards.

## ✨ Core Features

### 🤖 AI-Driven Figure Generation
- **Intelligent Parsing**: AI automatically understands your figure requirements and extracts key information.
- **SCI Standards**: Generated figures strictly meet top SCI journal publication standards.
- **Multi-type Support**: Supports data charts, mechanism diagrams, flowcharts, principle diagrams, and structural schematics.
- **High-Quality Output**: Vector-level clarity, pure white background, professional color palettes.

### 🔧 Quick Integration
- **Simple Configuration**: Just add the configuration file and API Key.
- **Broad Compatibility**: Supports all MCP-compatible tools.
- **Plug and Play**: Ready to use right after configuration, no extra development needed.

### 🔒 Secure & Reliable
- **UUID Authentication**: Identity authentication mechanism based on UUID.
- **Rate Limiting**: Prevents abuse and ensures service stability.
- **Usage Tracking**: Real-time tracking of API usage and quota.

## 📖 API Reference

### `generate_sci_figure`
Generates scientific academic figures according to descriptions, meeting SCI journal standards.

**Input Parameters**:
| Parameter | Type | Required | Description |
|---|---|---|---|
| description | string | ✅ | Figure description, including data, type, style requirements, etc. |
| figureType | string | ❌ | Type: line_chart, bar_chart, scatter, heatmap, flowchart, architecture, mechanism, etc. |
| style | string | ❌ | Style preference: nature, science, ieee, default |
| dataValues | object | ❌ | Exact data values (used for data charts) |

**Output**:
```json
{
  "figureUrl": "https://figure.thirdme.com/figures/xxx.png",
  "figureCode": "// Editable figure code",
  "metadata": {
    "type": "line_chart",
    "style": "nature",
    "resolution": "300dpi",
    "format": "PNG/SVG"
  }
}
```

### `edit_figure`
Edits an already generated figure by adjusting its style, data, or layout.

**Input Parameters**:
| Parameter | Type | Required | Description |
|---|---|---|---|
| figureId | string | ✅ | ID of the figure to be edited |
| editInstructions | string | ✅ | Edit instruction, e.g., "Change the bar chart color to blue" |

## 🛠️ Supported Platforms
- ✅ Claude Desktop
- ✅ OpenAI (MCP Compatible)
- ✅ Cursor
- ✅ Dify
- ✅ n8n
- ✅ OpenClaw
- ✅ Codex
- ✅ Hermes
- ✅ Other MCP-compatible tools

## 💡 Use Cases

**Case 1: Generate a Paper Loss Curve Chart**
> Please generate a Loss curve chart for the training process:
> - X-axis: Epoch (1-50)
> - Y-axis: Loss
> - Includes Training Loss (drops from 2.5 to 0.1) and Validation Loss (drops from 2.8 to 0.15)
> - Style: Nature journal standard

**Case 2: Draw a Neural Network Architecture Diagram**
> Please draw a Transformer architecture diagram, containing:
> - Input embedding layer
> - 6-layer Encoder (with Multi-Head Attention and Feed Forward)
> - 6-layer Decoder
> - Output layer
> - Use NeurIPS style, flat design, no gradients

**Case 3: Generate an Experimental Flowchart**
> Please generate a drug screening experimental flowchart:
> 1. Compound library screening (10,000 compounds)
> 2. High-throughput primary screening (Hit rate: 2%)
> ...

## 📝 Notes
- **API Key Security**: Please keep your API Key secure. Do not share it with others or submit it to public repositories.
- **Quota Limits**: API usage is subject to subscription quota limits.
- **Data Accuracy**: Provide exact data values to get the most accurate chart output.
- **Figure Types**: Explicitly specifying the figure type yields more precise results.
- **Processing Time**: Simple figures take about 5-10 seconds; complex figures may take over 30 seconds.
- **Data Security**: Processed data is automatically deleted from servers after 24 hours.

## 📧 Support & Feedback
- 📧 Email: support@thirdme.com
- 🌐 Website: [https://figure.thirdme.com](https://figure.thirdme.com)
- 📄 API Docs: [https://figure.thirdme.com/mcp](https://figure.thirdme.com/mcp)

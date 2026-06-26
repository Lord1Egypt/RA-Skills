---
name: flyai-travelmapify
version: 2.2.2
description: Create interactive travel route maps from location names with real FlyAI hotel search. Supports AI Vision analysis of travel planning images.
author: rudy2steiner
license: MIT
tags: [travel, maps, routing, geocoding, flyai, hotels, unique-id, server-management, interactive, ai-vision]
---

# Travel Mapify

Create interactive, professional travel route maps from location names.

## Overview

This skill automatically:
1. **Processes text input**: Parses comma-separated location names directly
2. **Geocodes locations** to get precise coordinates using Amap API
3. **Generates interactive maps** with route optimization and POI management
4. **Supports AI Vision workflow**: When given travel planning images, use agent's AI Vision to extract POI names, then process as text input
4. **Geocodes locations** to get precise coordinates using Amap API
5. **Generates interactive maps** with route optimization and POI management
6. **Integrates real hotel search** using FlyAI for actual hotel recommendations
7. **Creates professional outputs** ready for sharing and presentation

## When to Use

**Text Input Mode:**
- User provides comma-separated location names directly (e.g., "上海外滩,上海迪士尼乐园,豫园")
- User wants to quickly create a travel map from a simple list of destinations
- User has location names but no visual reference image

**AI Vision Image Processing Workflow:**
- User has a travel planning image (screenshot, photo, or digital plan)
- Agent uses AI Vision to analyze the image and extract POI names with sequence/order
- Extracted POI names are passed as text input to the skill
- This hybrid approach combines AI automation with the skill's robust text processing

**Hotel Integration Mode:**
- User wants real hotel recommendations near their destination
- User needs actual pricing and availability data
- User wants booking links for hotels through FlyAI integration

## Workflow

### Step 1: Input Processing and POI Extraction

**For Direct Text Input:**
- Parse comma-separated location names directly
- Create POI entries with high confidence (user-provided)
- **Automatic city detection**: Smart city detection from location names (e.g., "北京军事博物馆" → city="北京")
- **Fallback to default**: Uses Shanghai as default when no city can be detected

**For Image Input (AI Vision Workflow):**
- **Use agent's AI Vision capability** to analyze travel planning images
- **Extract POI names and sequence** from numbered markers or route indicators
- **Preserve exact order** as marked in the original image
- **Pass extracted names as text input** to the skill's standard processing pipeline
- **Leverage existing text processing** for geocoding, validation, and map generation

### Step 2: Geocoding and Coordinate Resolution
- Use Amap geocoding API to resolve location names to precise coordinates
- Handle ambiguous locations with user confirmation
- Validate coordinate accuracy

### Step 3: Enhanced Map Generation
- **Use optimized travel_mapify with unique map ID isolation** as main template with all UX improvements
- **Automatic localStorage isolation** based on POI names to prevent data conflicts between different maps
- **Optimized performance** with streamlined template generation and reduced dependencies
- Create a single dual-mode interface with toggle between Edit/View modes
- Implement drag-and-drop and arrow button reordering (edit mode only)
- Generate optimized route with directional arrows
- Add "Generate Final" functionality to download clean version
- **Integrate real FlyAI hotel search** with professional loading states
- **Replace alert popups** with notification system

### Step 4: Automatic Server Management
- **Automatically start HTTP server** on port 9000 (or specified port)
- **Automatically start hotel search server** on port 8770 (or specified port)
- **Check if servers are already running** to avoid conflicts
- **Provide direct access URLs** in output
- **Ensure all functionality is ready** when map creation completes

### Step 4: Professional Output Delivery
- Provide unified HTML file that works in both editing and presentation contexts
- Include clear instructions for toggling modes and generating final version
- Ensure mobile-responsive design

## File Structure

```
flyai-travelmapify/
├── SKILL.md
├── INSTALL.md                          # Installation and setup guide
├── flyai-travelmapify.py              # **PORTABLE ENTRY POINT**: Main executable script
├── scripts/
│   ├── config.py                      # **DYNAMIC CONFIGURATION**: Path and environment detection
│   ├── main_travel_mapify_enhanced.py # **PRODUCTION MAIN**: Auto-starts servers + text input + unique ID isolation
│   ├── geocode_locations.py           # Amap geocoding integration
│   ├── generate_from_optimized_template.py # Optimized template with unique map ID isolation
│   └── hotel-search-server.py         # FlyAI hotel search backend server

**Note**: Image processing is handled externally using the agent's AI Vision capability. The extracted POI names are passed as text input to this skill.
├── references/
│   ├── amap_api_guide.md              # Amap API usage patterns
│   ├── poi_validation_rules.md        # POI validation and filtering rules
│   └── troubleshooting-guide.md       # Common issues and solutions
└── assets/
    └── templates/
        └── main-generic-template-with-unique-id.html # **PRODUCTION TEMPLATE**: Unique ID isolation + all features
```

**Main Template**: The skill now uses the **optimized travel_mapify system** with unique map ID isolation as the primary approach, which includes:
- **Optimized Template Generation**: Streamlined HTML generation with minimal dependencies
- **Unique Map ID Generation**: Automatically creates a hash-based ID from POI names (e.g., `travelMap_abc123`) to isolate localStorage data
- **No Cross-Map Data Contamination**: Each travel map saves/retrieves data independently using its unique ID
- **Persistent Per-Map State**: Hotel searches, date selections, and POI reordering are saved separately for each map
- **Enhanced Performance**: Reduced template complexity and faster map loading
- Real FlyAI hotel search integration
- Professional notification system (no alert popups)
- Loading states with timeout handling
- Enhanced UX with smart defaults

**Automatic Server Management**: The enhanced main script automatically starts both HTTP server (port 9000) and hotel search server (port 8770) when generating maps, ensuring all functionality is ready immediately.

## Usage Examples

### Portable Execution
```bash
# From skill directory (recommended)
python3 flyai-travelmapify.py --locations "上海外滩,迪士尼乐园,豫园" --output-html shanghai-trip.html

# From any directory
python3 /path/to/flyai-travelmapify/flyai-travelmapify.py --locations "北京故宫,天坛,颐和园" --output-html beijing-trip.html

# AI Vision Image Processing Workflow:
# 1. Use agent's AI Vision to analyze travel image and extract POI names
# 2. Pass extracted names as text input to the skill
# Example: locations="解放碑,山城步道,十八梯,白象居,湖广会馆,来福士,洪崖洞,千厮门大桥"

# With custom ports
python3 flyai-travelmapify.py --locations "Tokyo Tower,Shibuya Crossing" --output-html tokyo-trip.html --http-port 8080 --hotel-port 9000
```

### Image Input - AI Vision Enhanced
User: "Here's my travel plan screenshot, can you make it interactive?"
→ Skill analyzes image using AI Vision model
→ If needed, requests clarification: "What city is this for?" or "How many attractions are marked?"
→ Extracts attractions with preserved sequence and generates interactive map

### Image Input - Manual Clarification
User provides image → Skill detects uncertainty → Requests city context → User responds "重庆" → Skill processes with enhanced accuracy

### Image Input - Direct POI Entry
When AI Vision cannot confidently identify attractions, skill prompts: "Please provide attraction names in order, separated by commas"

### Image Input - Advanced Usage  
User: "I have a photo of our Beijing itinerary, please create a shareable map"
→ Skill processes image, validates locations, creates optimized route with professional styling

### Text Input - Direct Locations with Auto City Detection
User: "北京军事博物馆,北京科技大学"
→ Skill auto-detects city="北京" from location names
→ Parses locations directly, geocodes them, and generates interactive map

### Text Input - Default City Fallback
User: "外滩,迪士尼乐园,豫园"
→ Skill cannot detect city from generic names
→ Uses default city="上海" for geocoding
→ Generates interactive map

### Text Input - Simple List
User: "Create a travel map for: Tokyo Tower, Shibuya Crossing, Meiji Shrine"
→ Skill extracts location names, geocodes them, creates optimized route

### Hotel Search Integration
User: Clicks "搜酒店" button in generated map
→ Real FlyAI hotel search returns actual hotel data with prices and booking links
→ No mock data - uses real-time Fliggy MCP integration
→ Professional UX with loading states and notifications (no alert popups)
→ Default dates: today for check-in, tomorrow for check-out (1-night stay)

### Customization Request
User: "Can you adjust the route order and add missing locations?"
→ Skill provides editable interface with search functionality and reordering tools

## Technical Requirements

- **Python 3.7+**: Required for all scripts (uses standard library only)
- **FlyAI CLI**: Must be installed globally (`npm install -g @openclaw/flyai`) 
- **Amap API**: Uses built-in default API key (no user key required)
- **Local Proxy**: Built-in proxy server handles Amap API requests (default port 8769)
- **Web Browser**: Modern browser with JavaScript support for interactive features

## Required Skills

This skill depends on the following OpenClaw skills:

- **[amap-maps](https://github.com/openclaw/openclaw/tree/main/skills/amap-maps)**: Provides Amap LBS services for geocoding, POI search, and location services

Both skills must be installed in your OpenClaw workspace under the `skills/` directory:
```
~/.openclaw/workspace/
├── skills/
│   ├── flyai-travelmapify/
│   └── amap-maps/
```

## Portable Design

✅ **No hardcoded paths** - Automatically detects OpenClaw workspace and FlyAI installation
✅ **Cross-platform** - Works on Windows, macOS, and Linux
✅ **Self-contained** - All scripts and templates included in skill directory
✅ **Environment-aware** - Adapts to different system configurations
✅ **Fallback mechanisms** - Multiple detection methods for required components

## Output Files

The skill generates HTML files using the **optimized travel_mapify system with unique map ID isolation** as the main template:

**`[location]-travel-map-optimized.html`** - Dual-mode interface with all professional enhancements:
- **Real FlyAI Hotel Search Integration**:
  - Actual hotel data with prices and booking links
  - Loading states with "搜索中..." button text
  - 5-second timeout with auto-re-enable
  - No mock data - uses real Fliggy MCP integration
- **Professional UX Improvements**:
  - Notification system instead of alert popups
  - Auto-hiding messages after 3 seconds
  - Smart date defaults (today check-in, tomorrow check-out)
- **Edit Mode (📝)**: Full-featured editing interface with:
  - Left-panel POI management
  - Search functionality for adding new locations
  - Drag-and-drop and arrow button reordering
  - Real-time map preview
- **View Mode (👁️)**: Clean presentation version with:
  - Optimized route display
  - Numbered POI markers with directional arrows
  - Professional styling ready for sharing
- **Generate Final**: Download button to create a clean version without edit controls

Files are self-contained and work in any modern web browser when served via HTTP server.

## Error Handling

- **Poor Image Quality**: Request higher quality image or manual POI entry
- **Ambiguous Locations**: Present options for user selection
- **API Rate Limits**: Implement retry logic with exponential backoff
- **Missing Coordinates**: Fall back to approximate coordinates with user verification
- **HTML Display Issues**: Use local HTTP server instead of file:// protocol
- **Map Loading Failures**: Check AMap API key restrictions and network connectivity
- **localStorage Corruption**: Implement fallback data and validation logic

## Enhanced UX Features

**Professional User Interface:**
- **No alert popups**: All messages displayed in non-intrusive notification area
- **Loading states**: Hotel search button shows "搜索中..." during API calls
- **Timeout handling**: 5-second timeout automatically re-enables search button
- **Auto-hiding notifications**: Messages disappear after 3 seconds
- **Visual feedback**: Error messages in red, success messages in green

**Smart Defaults:**
- **Date selection**: Today for check-in, tomorrow for check-out (1-night stay)
- **Hotel sorting**: Results sorted by distance from destination
- **Top results**: Shows top 5 closest hotels for better user experience

## Best Practices

- Always verify extracted POIs with the user before finalizing
- Provide clear instructions for customizing the generated maps
- Optimize for mobile viewing with responsive design
- Include north indicator and scale reference for professional appearance
- **Always test via HTTP server**: Never rely on file:// protocol for web applications
- **Implement robust error handling**: Wrap API calls and provide user feedback
- **Validate all inputs**: Sanitize data before processing
- **Document dependencies**: Clearly specify API keys, network, and browser requirements
- **Use optimized travel_mapify with unique map ID isolation**: All travel maps now automatically generate unique IDs based on POI names to prevent localStorage conflicts between different maps
- **Leverage enhanced performance**: The optimized system provides faster map generation and loading

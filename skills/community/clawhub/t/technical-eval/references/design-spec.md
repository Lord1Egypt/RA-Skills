# Technical Evaluation Design Specifications

## Visual Identity Guidelines

### Color Palette
- **Background**: #000000 (pure black) or #0a0a0a (near black)
- **Primary Text**: #ffffff (pure white)
- **Secondary Text**: #9ca3af (slate-400)
- **Accent Colors**: 
  - Adopt: #10b981 (emerald-500) - green for recommended
  - Trail: #3b82f6 (blue-500) - blue for experimental  
  - Assets: #f59e0b (amber-500) - amber for existing
  - Hold: #ef4444 (red-500) - red for avoid

### Typography
- **Chinese Fonts**: HarmonyOS Sans SC, 思源黑体, system-ui
- **English Fonts**: Inter, Roboto, system-ui
- **Title Weight**: font-black (900) or font-bold (700)
- **Body Weight**: font-light (300) or font-normal (400)
- **Code Font**: JetBrains Mono, Consolas, monospace

### Layout Principles
- **Aspect Ratio**: 9:16 (vertical/portrait)
- **Padding**: Minimum 48px on all sides
- **Line Height**: 1.6 for body text
- **Max Line Length**: 60 characters for readability
- **Whitespace**: Generous spacing between elements

## Data Visualization Standards

### Radar Charts (Maturity Assessment)
- 5 axes: Community, Documentation, Ecosystem, Adoption, Learning Curve
- Fill opacity: 30% for area, 100% for border
- Axis labels in secondary text color
- Grid lines in #374151 (slate-700)

### Comparison Tables
- Zebra striping with #111827 (slate-900) and #1f2937 (slate-800)
- Header row in #374151 with white text
- Score cells use color intensity based on value (0-100%)
- Highlight top performer in each column with accent color

### Risk Matrix
- 5x5 grid with probability (Y-axis) vs impact (X-axis)
- Quadrant colors: Green (low), Yellow (medium), Red (high)
- Risk items as circular markers with size indicating priority
- Hover tooltips with detailed risk description

### Candidate Matrix
- 2x2 positioning based on two key dimensions
- Bubble size indicates overall score
- Color coding by Adopt/Trail/Assets/Hold classification
- Labels only for top candidates to avoid clutter

## Animation Guidelines

### Transitions
- Slide transitions: fade with 300ms duration
- Element entrance: subtle slide-up with 200ms stagger
- No distracting animations or bounce effects

### Interactive Elements
- Hover states with 10% brightness increase
- Clickable elements with subtle underline or border
- Keyboard navigation support (← → arrows)

### Background Effects
- Subtle animated light spots in background
- Very low opacity (5-10%)
- Slow movement (30s+ cycle time)
- Never interfere with text readability
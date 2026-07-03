# Draw.io XML Templates Reference

This reference provides concrete draw.io XML code templates for each diagram type. Use these as the base when generating `.drawio` files.

## General draw.io XML Structure

```xml
<mxfile host="Claude" modified="2026-06-02T00:00:00.000Z" agent="Claude Code" version="24.0.0">
  <diagram name="Page-1" id="Page-1">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1200" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- All shapes go here as mxCell elements -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Common Shape Styles

### Rounded Rectangle — Most Common Component Node
```xml
<mxCell id="x" value="Node Text" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1E88E5;fontSize=13;fontStyle=1;arcSize=10;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="160" height="50" as="geometry" />
</mxCell>
```

### Rectangle — Standard Node
```xml
<mxCell id="x" value="Node Text" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;fontSize=12;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="160" height="50" as="geometry" />
</mxCell>
```

### Rhombus — Decision / Condition Node
```xml
<mxCell id="x" value="Condition?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#FFF9C4;strokeColor=#F9A825;fontSize=12;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="100" height="80" as="geometry" />
</mxCell>
```

### Ellipse — Start / End
```xml
<mxCell id="x" value="Start" style="ellipse;whiteSpace=wrap;html=1;fillColor=#C8E6C9;strokeColor=#388E3C;fontSize=14;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry" />
</mxCell>
```

### Cylinder — Database / Data Store
```xml
<mxCell id="x" value="MySQL" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#F3E5F5;strokeColor=#7B1FA2;fontSize=12;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="100" height="80" as="geometry" />
</mxCell>
```

### Swimlane — Role / Layer
```xml
<mxCell id="x" value="Swimlane Title" style="swimlane;whiteSpace=wrap;html=1;fillColor=#E8EAF6;strokeColor=#3F51B5;fontSize=14;fontStyle=1;startSize=30;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="800" height="200" as="geometry" />
</mxCell>
```

### Group Container — Architecture Layer / System Boundary
```xml
<mxCell id="x" value="Container Label" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1E88E5;fontSize=14;fontStyle=1;dashed=1;dashPattern=5 5;verticalAlign=top;spacingTop=5;opacity=40;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="500" height="300" as="geometry" />
</mxCell>
```

### Edge / Connector
```xml
<!-- Straight Arrow -->
<mxCell id="x" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#666666;strokeWidth=1.5;endArrow=classic;fontSize=11;" edge="1" parent="1" source="src_id" target="tgt_id">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<!-- Edge with Label -->
<mxCell id="x" value="Data / JSales OrderN" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#666666;strokeWidth=1.5;endArrow=classic;fontSize=10;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="src_id" target="tgt_id">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<!-- Dashed Edge -->
<mxCell id="x" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#999999;strokeWidth=1;endArrow=classic;dashed=1;dashPattern=8 8;" edge="1" parent="1" source="src_id" target="tgt_id">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

## Diagram-Specific Templates

### 1. Technical Architecture Diagram — Layered Layout

Key approach: Use large containers for each layer, stack them vertically.

```
Canvas: 1200×1000
Layer containers: width=1000, height varies
Layer gaps: 10px between containers
Component nodes inside layers: width=140-180, height=50, gap=20
```

Layer color scheme:
- User / Access Layer: container fill=#E3F2FD, component fill=#BBDEFB
- Business Application Layer: container fill=#E8F5E9, component fill=#C8E6C9
- Platform Service Layer: container fill=#FFF3E0, component fill=#FFE0B2
- Data Layer: container fill=#F3E5F5, component fill=#E1BEE7
- Infrastructure Layer: container fill=#ECEFF1, component fill=#CFD8DC

### 2. Business Process Diagram — Swimlane Layout

Key approach: Use swimlane containers side by side (horizontal layout).

```
Canvas: depends on flow complexity
Swimlane width: ~200-250 each (for role-based)
Node spacing: horizontal 40px, vertical 60px
```

### 3. Data Flow Diagram — Left to Right

Key approach: External entities on left/right edges, processes in middle, data stores at bottom.

### 4. Functional Architecture Diagram — Tree-style Layered

Key approach: Top-down hierarchical containers with modules.

```
Top level: Platform title bar (width=900, height=40)
Second level: Module containers (width=200-250 each, height=240)
Third level: Feature nodes inside containers (width=160, height=40)
```

### 5. System Integration Diagram — Hub-and-Spoke

Key approach: Core system in center (big), external systems around (smaller), radial connections.

```
Core: x=500, y=350, width=200, height=120
External: arranged in circle at radius=350
  - Top: x=450, y=50
  - Right: x=800, y=350
  - Bottom: x=450, y=650
  - Left: x=100, y=350
  - Corners at 45° angles
```

## ID Generation

Use sequential IDs starting from "2" (IDs "0" and "1" are reserved for root).

Each shape uses a unique ID string. Edge IDs can share the same "x" placeholder convention — replace with actual sequential numbers.

## Positioning Tips

1. Align to grid: positions should typically be multiples of 10 (grid size)
2. Consistent spacing: maintain equal gaps between sibling nodes (20-40px)
3. Center alignment: nodes in the same layer should align horizontally (same `y`) or vertically (same `x`), unless in a progressive flow
4. Container padding: leave at least 30px margin inside containers for inner nodes
5. Label visibility: ensure edge labels don't overlap nodes — use `labelBackgroundColor=#FFFFFF` for readability

---

## ArchiMate 3.2 View Templates

ArchiMate 3.2 is The Open Group's enterprise architecture modeling standard, providing a six-layer modeling system (Strategy / Business / Application / Technology / Physical / Implementation & Migration) and 14 standard Viewpoints. The following templates cover the 5 most commonly used ArchiMate Viewpoints.

### ArchiMate Element Style Specification

ArchiMate elements across layers use a unified color scheme to distinguish layers and element types:

| Layer | Container / Primary Color | Element Fill | Border Color | Font |
|----|-----------|---------|--------|------|
| **Strategy Layer** | #FFF3E0 | #FFE0B2 | #F57C00 | Bold 13px |
| **Business Layer** | #FFFDE7 | #FFF9C4 | #FBC02D | Bold 13px |
| **Application Layer** | #E3F2FD | #BBDEFB | #1E88E5 | Regular 12px |
| **Technology Layer** | #E8F5E9 | #C8E6C9 | #43A047 | Regular 12px |
| **Physical Layer** | #ECEFF1 | #CFD8DC | #607D8B | Regular 12px |
| **Motivation** | #F3E5F5 | #E1BEE7 | #8E24AA | Bold 12px |

### ArchiMate Relationship Edge Styles

```xml
<!-- Composition (solid diamond) -->
<mxCell id="x" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#333333;strokeWidth=2;endArrow=diamondThin;endFill=1;fontSize=10;" edge="1" parent="1" source="src" target="tgt">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<!-- Aggregation (hollow diamond) -->
<mxCell id="x" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#333333;strokeWidth=2;endArrow=diamondThin;endFill=0;fontSize=10;" edge="1" parent="1" source="src" target="tgt">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<!-- Assignment (dashed + solid diamond) -->
<mxCell id="x" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#666666;strokeWidth=1.5;endArrow=diamondThin;endFill=1;dashed=1;dashPattern=5 5;fontSize=10;" edge="1" parent="1" source="src" target="tgt">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<!-- Realization (dashed + hollow triangle) -->
<mxCell id="x" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#666666;strokeWidth=1.5;endArrow=openThin;endFill=0;dashed=1;dashPattern=5 5;fontSize=10;" edge="1" parent="1" source="src" target="tgt">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<!-- Serving (solid + hollow triangle) -->
<mxCell id="x" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#1E88E5;strokeWidth=1.5;endArrow=openThin;endFill=0;fontSize=10;" edge="1" parent="1" source="src" target="tgt">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<!-- Triggering (solid + solid arrow) -->
<mxCell id="x" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#F57C00;strokeWidth=1.5;endArrow=classic;fontSize=10;" edge="1" parent="1" source="src" target="tgt">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<!-- Flow (dashed + solid arrow) -->
<mxCell id="x" value="Data Flow" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#43A047;strokeWidth=1.5;endArrow=classic;dashed=1;dashPattern=8 8;fontSize=10;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="src" target="tgt">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### A.1 Motivation Viewpoint — Stakeholder Concerns

**Purpose**: Answers "Why do it? Is it worth doing?" — suitable for executive presentations. Shows the causal chain: Stakeholder → Driver → Assessment → Goal → Outcome → Principle.

```
Canvas: 1400×900
Layout: Left-to-right causal chain
  - Left column: Stakeholder (actor icon) → Driver (hexagon)
  - Middle column: Assessment (rectangle) → Goal (rounded rectangle)
  - Right column: Outcome (ellipse) → Principle (rectangle with icon)
Node spacing: horizontal 120px, vertical 80px
```

**Key Element Templates**:

```xml
<!-- Stakeholder -->
<mxCell id="x" value="CIO" style="shape=actor;whiteSpace=wrap;html=1;fillColor=#F3E5F5;strokeColor=#8E24AA;fontSize=13;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="80" y="100" width="60" height="100" as="geometry" />
</mxCell>

<!-- Driver (hexagon) -->
<mxCell id="x" value="Digital Transformation Pressure" style="shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;fillColor=#E1BEE7;strokeColor=#8E24AA;fontSize=12;size=20;" vertex="1" parent="1">
  <mxGeometry x="220" y="110" width="140" height="80" as="geometry" />
</mxCell>

<!-- Assessment -->
<mxCell id="x" value="Current System Maintenance Cost&#xa;Annual Growth 35%" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFE0B2;strokeColor=#F57C00;fontSize=12;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="440" y="100" width="160" height="70" as="geometry" />
</mxCell>

<!-- Goal -->
<mxCell id="x" value="Reduce Ops Cost by 30%" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#C8E6C9;strokeColor=#43A047;fontSize=13;fontStyle=1;arcSize=20;" vertex="1" parent="1">
  <mxGeometry x="680" y="100" width="150" height="60" as="geometry" />
</mxCell>

<!-- Outcome -->
<mxCell id="x" value="Cloud-native Platform Go Live" style="ellipse;whiteSpace=wrap;html=1;fillColor=#BBDEFB;strokeColor=#1E88E5;fontSize=13;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="910" y="100" width="150" height="60" as="geometry" />
</mxCell>

<!-- Principle -->
<mxCell id="x" value="Cloud-First Strategy" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFE0B2;strokeColor=#F57C00;fontSize=13;fontStyle=1;arcSize=15;dashed=1;" vertex="1" parent="1">
  <mxGeometry x="1140" y="100" width="140" height="60" as="geometry" />
</mxCell>
```

### A.2 Layered Viewpoint — Horizontal Layered Display

**Purpose**: Shows the structure and dependency relationships across enterprise architecture layers (Business → Application → Technology). This is the most commonly used ArchiMate viewpoint.

```
Canvas: 1400×1000
Layout: Top-to-bottom three layers
  - Top layer Business Layer: y=40, height=280
  - Middle layer Application Layer: y=340, height=280
  - Bottom layer Technology Layer: y=640, height=280
Inter-layer spacing: 20px
Nodes within each layer arranged horizontally, gap=30
```

**Layer Container Templates**:

```xml
<!-- Business Layer Container -->
<mxCell id="biz-layer" value="Business Layer" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFDE7;strokeColor=#FBC02D;fontSize=14;fontStyle=1;verticalAlign=top;spacingTop=5;opacity=30;" vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="1320" height="280" as="geometry" />
</mxCell>

<!-- Application Layer Container -->
<mxCell id="app-layer" value="Application Layer" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1E88E5;fontSize=14;fontStyle=1;verticalAlign=top;spacingTop=5;opacity=30;" vertex="1" parent="1">
  <mxGeometry x="40" y="340" width="1320" height="280" as="geometry" />
</mxCell>

<!-- Technology Layer Container -->
<mxCell id="tech-layer" value="Technology Layer" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8F5E9;strokeColor=#43A047;fontSize=14;fontStyle=1;verticalAlign=top;spacingTop=5;opacity=30;" vertex="1" parent="1">
  <mxGeometry x="40" y="640" width="1320" height="280" as="geometry" />
</mxCell>
```

### A.3 Service Realization Viewpoint

**Purpose**: Shows how business services are realized by application services, and how application services are supported by technology infrastructure. Suitable for "End-to-end service realization chain" in proposal presentations.

```
Canvas: 1200×900
Layout: Top-to-bottom four layers
  Business Service → Application Service → Application Component → Technology Node
2-3 nodes per layer, connected using Realization (dashed + hollow triangle)
```

### A.4 Capability Map Viewpoint

**Purpose**: Shows the organization's capability map, organized across three dimensions: Strategy / Customer / Operations. Suitable for business architecture diagrams.

```
Canvas: 1200×800
Layout: Nested rectangles
  Outer: Capability domains (Strategy / Customer / Operations)
  Inner: Specific capability items
Color scheme: Strategy=#FFF3E0, Customer=#E3F2FD, Operations=#E8F5E9
```

**Capability Map Element Templates**:

```xml
<!-- Capability Domain Container -->
<mxCell id="cap-domain" value="Customer Management" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1E88E5;fontSize=14;fontStyle=1;verticalAlign=top;spacingTop=5;opacity=25;" vertex="1" parent="1">
  <mxGeometry x="60" y="60" width="350" height="300" as="geometry" />
</mxCell>

<!-- Capability Item -->
<mxCell id="cap-item" value="Customer 360 View" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#BBDEFB;strokeColor=#1E88E5;fontSize=12;arcSize=10;" vertex="1" parent="1">
  <mxGeometry x="90" y="120" width="130" height="50" as="geometry" />
</mxCell>
```

### A.5 Implementation & Migration Viewpoint

**Purpose**: Shows the migration path from current architecture to target architecture, including Work Package, Plateau, and Gap elements. Suitable for implementation roadmaps.

```
Canvas: 1400×800
Layout: Timeline left to right
  Baseline Architecture → Transition A → Transition B → Target Architecture
Plateau represented by large containers, Work Package by small rectangles, Gap by dashed rectangles
Color scheme: Baseline=#ECEFF1, Transition=#FFF3E0, Target=#E8F5E9
```

---

## Wardley Map Strategic Decision Framework Template

Wardley Mapping is a strategic decision framework created by Simon Wardley. By visualizing the position (Visibility) and evolution stage (Evolution) of each component on the value chain, it helps enterprises make build/buy/outsource/standardize decisions.

### Wardley Map Canvas Structure

```
Canvas: 1400×900
Coordinate system:
  - Vertical axis (Y): Visibility — bottom to top, from invisible (infrastructure) to visible (user needs)
  - Horizontal axis (X): Evolution — left to right, Genesis → Custom → Product → Commodity
  - Anchor: top-left (100, 50) = User Needs
  - Anchor: bottom-right (1300, 800) = Commoditized Infrastructure
```

### Evolution Stage Zone Division

| Stage | X Range | Background Color | Meaning |
|------|--------|--------|------|
| **Genesis** | x: 100-350 | #FFCDD2 (light red) | Brand new, uncertain, experimental |
| **Custom** | x: 350-650 | #FFF9C4 (light yellow) | Mostly self-built, differentiated |
| **Product** | x: 650-950 | #BBDEFB (light blue) | Market productized, highly competitive |
| **Commodity** | x: 950-1300 | #C8E6C9 (light green) | Standardized, on-demand usage |

### Wardley Map Stage Zone Backgrounds

```xml
<!-- Genesis Stage Zone -->
<mxCell id="zone-genesis" value="Genesis" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFCDD2;strokeColor=#E57373;fontSize=12;fontStyle=1;verticalAlign=top;spacingTop=3;opacity=20;" vertex="1" parent="1">
  <mxGeometry x="100" y="50" width="250" height="750" as="geometry" />
</mxCell>

<!-- Custom Stage Zone -->
<mxCell id="zone-custom" value="Custom Built" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFF9C4;strokeColor=#FBC02D;fontSize=12;fontStyle=1;verticalAlign=top;spacingTop=3;opacity=20;" vertex="1" parent="1">
  <mxGeometry x="350" y="50" width="300" height="750" as="geometry" />
</mxCell>

<!-- Product Stage Zone -->
<mxCell id="zone-product" value="Product (+Rental)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#BBDEFB;strokeColor=#1E88E5;fontSize=12;fontStyle=1;verticalAlign=top;spacingTop=3;opacity=20;" vertex="1" parent="1">
  <mxGeometry x="650" y="50" width="300" height="750" as="geometry" />
</mxCell>

<!-- Commodity Stage Zone -->
<mxCell id="zone-commodity" value="Commodity (+Utility)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#C8E6C9;strokeColor=#43A047;fontSize=12;fontStyle=1;verticalAlign=top;spacingTop=3;opacity=20;" vertex="1" parent="1">
  <mxGeometry x="950" y="50" width="350" height="750" as="geometry" />
</mxCell>
```

### Component Node Templates

In a Wardley Map, each component is represented by a rounded rectangle, with size reflecting its "importance" or "scale":

```xml
<!-- User Need Anchor (topmost) -->
<mxCell id="user-need" value="User Need: Real-time Data Insights" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FF7043;strokeColor=#D84315;fontSize=14;fontStyle=1;fontColor=#FFFFFF;arcSize=15;" vertex="1" parent="1">
  <mxGeometry x="500" y="60" width="220" height="55" as="geometry" />
</mxCell>

<!-- Genesis Stage Component (experimental, small) -->
<mxCell id="comp-ml" value="ML Prediction Engine" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#EF9A9A;strokeColor=#E57373;fontSize=12;fontStyle=1;arcSize=10;" vertex="1" parent="1">
  <mxGeometry x="140" y="350" width="130" height="45" as="geometry" />
</mxCell>

<!-- Custom Stage Component (self-built, medium) -->
<mxCell id="comp-api" value="Data Integration API" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFF176;strokeColor=#FBC02D;fontSize=12;fontStyle=1;arcSize=10;" vertex="1" parent="1">
  <mxGeometry x="400" y="280" width="140" height="45" as="geometry" />
</mxCell>

<!-- Product Stage Component (productized, medium) -->
<mxCell id="comp-db" value="Time-series Database" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#64B5F6;strokeColor=#1E88E5;fontSize=12;fontStyle=1;arcSize=10;" vertex="1" parent="1">
  <mxGeometry x="720" y="280" width="130" height="45" as="geometry" />
</mxCell>

<!-- Commodity Stage Component (commoditized, large) -->
<mxCell id="comp-compute" value="Cloud Computing (IaaS)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#81C784;strokeColor=#43A047;fontSize=12;fontStyle=1;arcSize=10;" vertex="1" parent="1">
  <mxGeometry x="1050" y="450" width="150" height="45" as="geometry" />
</mxCell>
```

### Value Chain Links

In a Wardley Map, edges between components represent dependency relationships, typically using labeled straight lines:

```xml
<!-- Value Chain Dependency Edge -->
<mxCell id="edge-vc" value="Requires" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#666666;strokeWidth=2;endArrow=classic;fontSize=10;labelBackgroundColor=#FFFFFF;exitX=0.5;exitY=1;entryX=0.5;entryY=0;" edge="1" parent="1" source="user-need" target="comp-api">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<!-- Evolution Arrow — thick left-to-right arrow -->
<mxCell id="evolution-arrow" value="" style="endArrow=classic;html=1;strokeColor=#999999;strokeWidth=3;fontSize=10;" edge="1" parent="1">
  <mxGeometry width="50" height="50" relative="1" as="geometry">
    <mxPoint x="100" y="820" as="sourcePoint" />
    <mxPoint x="1300" y="820" as="targetPoint" />
  </mxGeometry>
</mxCell>

<!-- Evolution Label -->
<mxCell id="evolution-label" value="Evolution → (Genesis → Custom → Product → Commodity)" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=11;fontColor=#666666;fontStyle=2;" vertex="1" parent="1">
  <mxGeometry x="450" y="830" width="500" height="25" as="geometry" />
</mxCell>
```

### Wardley Map Layout Principles

1. **Anchor on User Needs**: The topmost component must be the user need, placed in the Product stage zone (x≈500-700)
2. **Value Chain Extends Downward**: Below each component are its dependencies, forming a visible dependency chain
3. **Horizontal Axis Reflects Evolution**: More mature components are further right (Commodity), newer ones further left (Genesis)
4. **Component Size Reflects Importance**: Key components use larger sizes (width≥150), supporting components use smaller sizes (width≤120)
5. **Annotate Strategic Decisions**: Add annotation callouts beside components, labeling "Build / Buy / Outsource / Standardize" decisions

### Wardley Map Annotation Callout

```xml
<!-- Strategic Decision Annotation -->
<mxCell id="annotation" value="Recommendation: Buy mature product&#xa;rather than build in-house" style="shape=callout;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#F57C00;fontSize=10;perimeter=calloutPerimeter;size=15;position2=0.5;" vertex="1" parent="1">
  <mxGeometry x="750" y="200" width="130" height="55" as="geometry" />
</mxCell>
```
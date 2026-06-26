# PptxGenJS Color Palette Reference

Quick reference for color hex codes to use in single-slide presentations.

## Usage

**CRITICAL**: Never use `#` prefix with hex colors in PptxGenJS - causes file corruption.

✅ Correct: `fill: { color: "FF0000" }`
❌ Wrong: `fill: { color: "#FF0000" }`

## Professional Color Palettes

### Technology & Innovation
```javascript
{
  primary: "1a1a2e",      // Dark navy background
  accent: "4a00e0",       // Purple primary
  secondary: "8e2de2",    // Light purple
  highlight: "00d4ff",    // Cyan
  text: "e0e0e0"          // Light gray text
}
```

### Problem/Solution Theme
```javascript
{
  background: "1a1a2e",   // Dark background
  problem: "ff6b6b",      // Red for problems
  problemBg: "2d1f1f",    // Dark red background
  solution: "51cf66",     // Green for solutions
  solutionBg: "1a2a1a",   // Dark green background
  arrow: "8e2de2"         // Purple connector
}
```

### Professional Blue
```javascript
{
  primary: "2C3E50",      // Deep navy
  secondary: "3498DB",    // Bright blue
  accent: "1ABC9C",       // Teal
  background: "ECF0F1",   // Light gray
  text: "2C3E50"          // Dark text
}
```

### Warm & Creative
```javascript
{
  primary: "722880",      // Deep purple
  secondary: "D72D51",    // Pink/red
  accent: "EB5C18",       // Orange
  highlight: "F08800",    // Amber
  background: "2a2a2a"    // Dark gray
}
```

### Corporate Green
```javascript
{
  primary: "2E7D32",      // Forest green
  secondary: "66BB6A",    // Light green
  accent: "FFA726",       // Orange accent
  background: "F5F5F5",   // Off-white
  text: "212121"          // Almost black
}
```

### Modern Minimal
```javascript
{
  primary: "000000",      // Black
  secondary: "333333",    // Dark gray
  accent: "FF6B6B",       // Soft red
  background: "FFFFFF",   // White
  text: "1a1a1a"          // Near black
}
```

## Semantic Color Assignments

### Status Colors
```javascript
{
  success: "51cf66",      // Green
  warning: "FFA726",      // Orange
  error: "ff6b6b",        // Red
  info: "3498DB",         // Blue
  neutral: "95a5a6"       // Gray
}
```

### Text Colors (Dark Backgrounds)
```javascript
{
  primary: "ffffff",      // Pure white
  secondary: "e0e0e0",    // Light gray
  muted: "a0a0a0",        // Medium gray
  disabled: "666666"      // Dark gray
}
```

### Text Colors (Light Backgrounds)
```javascript
{
  primary: "1a1a1a",      // Near black
  secondary: "333333",    // Dark gray
  muted: "666666",        // Medium gray
  disabled: "999999"      // Light gray
}
```

## Color Psychology

### By Industry
- **Tech**: Blues, purples, cyans
- **Finance**: Navy, gold, green
- **Healthcare**: Blues, greens, white
- **Creative**: Bright colors, gradients
- **Corporate**: Navy, gray, muted tones
- **Education**: Blues, oranges, yellows

### By Emotion
- **Trust**: Blue (#3498DB, #2C3E50)
- **Energy**: Orange (#EB5C18, #FFA726)
- **Growth**: Green (#51cf66, #2ECC71)
- **Innovation**: Purple (#4a00e0, #8e2de2)
- **Urgency**: Red (#ff6b6b, #E74C3C)
- **Calm**: Teal (#16A085, #1ABC9C)

## Contrast Ratios

Ensure text readability with proper contrast:

### Dark Backgrounds
- White text (#ffffff) on dark (#1a1a1a): ✅ 18.5:1
- Light gray (#e0e0e0) on dark (#1a1a1a): ✅ 14.8:1
- Medium gray (#a0a0a0) on dark (#1a1a1a): ✅ 8.3:1

### Light Backgrounds
- Black text (#1a1a1a) on white (#ffffff): ✅ 18.5:1
- Dark gray (#333333) on white (#ffffff): ✅ 12.6:1
- Medium gray (#666666) on white (#ffffff): ✅ 5.7:1

**Minimum for body text**: 4.5:1
**Minimum for large text**: 3:1

## Quick Color Generator Formulas

### Create Lighter/Darker Shades

For a base color, create variations:
- **Lighter**: Increase each RGB value by 20-30%
- **Darker**: Decrease each RGB value by 20-30%

Example:
- Base: `4a00e0` (purple)
- Lighter: `6b21ff`
- Darker: `2900a0`

### Complementary Colors

For maximum contrast, use opposite on color wheel:
- Blue ↔ Orange
- Red ↔ Green
- Purple ↔ Yellow

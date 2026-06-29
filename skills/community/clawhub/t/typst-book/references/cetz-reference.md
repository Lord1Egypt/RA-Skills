# CeTZ Reference for Book Illustrations

## Import
```typst
#import "@preview/cetz:0.5.2": canvas, draw
```

## Canvas Setup
```typst
#canvas(length: 1cm, { .. })     // 1 unit = 1cm
#canvas({ .. })                  // default scale
```

## Drawing Functions

### Lines
```typst
draw.line((0, 0), (5, 5), stroke: 2pt + red)
draw.line((0, 0), (5, 5), stroke: (paint: red, thickness: 2pt, dash: "dashed"))
```

### Circles
```typst
draw.circle((2, 2), radius: 1.5, fill: blue, stroke: 1pt + dark-blue)
```

### Rectangles
```typst
draw.rect((0, 0), (4, 2), fill: green, stroke: black)
draw.rect((0, 0), (4, 2), fill: green, stroke: (paint: black, thickness: 1pt))
```

### Squares
```typst
draw.square((1, 1), size: 2, fill: yellow)
```

### Ellipses
```typst
draw.ellipse((3, 3), rx: 2, ry: 1, fill: purple)
```

### Curves
```typst
draw.curve((0, 0), (1, 2), (2, 0), (3, 2), stroke: 1pt)
```

### Arcs
```typst
draw.arc((2, 2), start: 0deg, stop: 180deg, radius: 2, stroke: 2pt)
```

### Text/Content
```typst
draw.content((2, 4), [Label Text], fill: red, size: 12pt)
```

### Groups
```typst
draw.group(name: "scene", {
  draw.circle((0, 0), radius: 1, fill: blue)
  draw.circle((2, 0), radius: 1, fill: red)
})
```

### Transformations
```typst
draw.rotate(45deg, { .. })
draw.scale(2, { .. })
draw.move((3, 3), { .. })
```

### Markers (arrows)
```typst
draw.line((0, 0), (5, 0), stroke: 2pt + black, mark: (end: "straight"))
```

## Coordinate System
- Origin (0, 0) is bottom-left by default
- X increases right, Y increases up
- All coordinates are (x, y) tuples
- Use `draw.coordinate` for custom transforms

## Tips for Book Illustrations
- Keep illustrations simple and iconic for children's books
- Use consistent color palettes across all illustrations
- Group related elements with `draw.group`
- Use `draw.content` for labels and speech bubbles
- Compose complex scenes from simple shapes
- Use `draw.rotate` and `draw.scale` for variety

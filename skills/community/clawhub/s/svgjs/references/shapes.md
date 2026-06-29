# Shape Elements

All created via `draw.<shape>(...)` or `new <Shape>().addTo(draw)`. Accept attrs object: `draw.rect({width:100, height:100, fill:'#f06'})`

## Rect
```js
draw.rect(100, 100)           // width, height
rect.radius(10)               // rounded corners (rx=ry=10)
rect.radius(10, 20)           // rx, ry
```

## Circle / Ellipse
```js
draw.circle(100)              // diameter
circle.radius(75)
draw.ellipse(200, 100)        // width, height
ellipse.radius(75, 50)        // rx, ry
```

## Line
```js
draw.line(0, 0, 100, 150).stroke({ width: 1 })
line.plot(50, 30, 100, 150)   // update: coords | 'x,y x,y' | [[x,y],[x,y]]
line.array()                   // get SVG.PointArray
```

## Polyline / Polygon
```js
draw.polyline('0,0 100,50 50,100').fill('none').stroke({ width: 1 })
draw.polygon('0,0 100,50 50,100')  // auto-closes first→last point
// Accepts: point string | [[x,y],...] | flat [x,y,...]
poly.plot([[0,0], [100,50]])   // update
poly.array() | poly.clear()    // PointArray ref | clear cache
```

## Path
```js
draw.path('M0 0 H50 A20 20 0 1 0 100 50 v25 C50 125 0 85 0 85 z')
path.plot('M10 80 C 40 10, 65 10, 95 80')  // update (animateable if same cmd structure)
path.length()          // total length
path.pointAt(105)      // point at given distance
path.text('Label')     // create textPath linked to this path
path.array() | path.clear()
```

All shapes inherit: `SVG.Shape` → `SVG.Element` → `SVG.Dom` → `SVG.EventTarget` → `SVG.Base`
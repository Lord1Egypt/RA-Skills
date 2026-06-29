# Utilities

## Import/Export
```js
draw.svg()                   // export full SVG string
rect.svg()                   // export single element
draw.svg(false)              // children only (no wrapper)
draw.svg(function(node) { node.round(4) }, false)  // transform during export
draw.svg('<g><rect width="100" height="50" fill="#f06"></rect></g>')  // import
group.svg('<rect><rect><rect>', true)               // import + replace

draw.html('<div></div>')     // import HTML
draw.html()                  // export HTML
draw.xml('<my-element/>', myNS)  // import XML with namespace
draw.xml()                   // export XML
```

## Extending
```js
SVG.extend(SVG.Shape, { paintRed() { return this.fill('red') } })
SVG.extend(SVG.Ellipse, { paintRed() { return this.fill('orangered') } })  // override
SVG.extend([SVG.Ellipse, SVG.Path], { paintRed() { return this.fill('red') } })  // multiple
SVG.extend(SVG.Svg, { paintAllPink() { this.each(function() { this.fill('pink') }) } })
```

## Subclassing
```js
SVG.Rounded = class extends SVG.Rect {
  size(width, height) { return this.attr({ width, height, rx: height/5, ry: height/5 }) }
}
SVG.extend(SVG.Container, {
  rounded(w, h) { return this.put(new SVG.Rounded()).size(w, h) }
})
draw.rounded(200, 100)       // use custom element
```

## SVG.Dom (generic element)
```js
var el = draw.element('title', {id: 'myId'})   // create any DOM element
el.words('This is a title.')                   // add text -> <title>This is a title.</title>
```
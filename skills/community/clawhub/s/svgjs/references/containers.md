# Container Elements

## SVG.Svg (root)
```js
var draw = SVG().addTo('#drawing')        // root document
var nested = draw.nested()                // nested SVG (HAS geometry, unlike groups)
nested.rect(200, 200)
```

## SVG.G (group)
```js
var group = draw.group(); group.path('M10,20L30,40'); group.add(rect)
// Groups have NO geometry — no x/y/width/height. Use nested() for positioned containers.
```

## SVG.Symbol
```js
var symbol = draw.symbol(); symbol.rect(100, 100).fill('#f09')
var use = draw.use(symbol).move(200, 200)  // not rendered until used
```

## SVG.Defs
```js
var defs = draw.defs()  // or rect.root().defs()
// Referenced elements live here, not rendered directly
```

## SVG.A (hyperlink)
```js
var link = draw.link('http://example.com')
link.rect(100, 100)                     // clickable
link.to('http://other.com')             // update url
link.target('_blank')

rect.linkTo('http://example.com')       // link from element
rect.linkTo(function(link) { link.to('...').target('_blank') })
rect.unlink()                           // remove link
rect.linker()                           // get <a> or null
```

## SVG.Fragment
```js
const frag = new Fragment()
frag.rect(100, 100); frag.circle(100)
draw.add(frag)                          // adds both at once
frag.svg()                              // export as svg string
```

Inheritance: `SVG.Base` → `SVG.EventTarget` → `SVG.Dom` → `SVG.Element` → `SVG.Container`
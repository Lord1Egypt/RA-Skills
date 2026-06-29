# Manipulating Elements

## Attributes
```js
rect.attr('x', 50)                                     // set single
rect.attr({ fill: '#f06', 'fill-opacity': 0.5 })       // set multiple
rect.attr('x', 50, 'http://www.w3.org/2000/svg')       // with namespace
rect.attr('fill', null)                                // remove
rect.attr('x') | rect.attr() | rect.attr(['x', 'y'])   // get
```

## Positioning (works on ALL element types)
```js
rect.move(200, 350)        // upper-left corner
rect.x(200) | rect.y(350)  // x or y only
rect.center(150, 150)      // by center
rect.cx(200) | rect.cy(350)// center x/y
rect.dmove(10, 30)         // shift by delta
rect.dx(200) | rect.dy(200)// shift x/y
rect.x() | rect.y()        // getters (also .cx() .cy())
```

## Sizing
```js
rect.size(200, 300)        // width, height
rect.size(200)             // proportional (height auto)
rect.width(200) | rect.height(325)
rect.width() | rect.height()
circle.radius(10)
ellipse.radius(10, 20)     // rx, ry
```

## Fill & Stroke
```js
rect.fill('#f06') | rect.fill({ color: '#f06', opacity: 0.6 })
rect.fill('images/shade.jpg')                          // image fill
rect.stroke('#f06') | rect.stroke({ color: '#f06', opacity: 0.6, width: 5 })
rect.opacity(0.5)
```

## Transforms
```js
// Absolute
rect.transform({ rotate: 125, translateX: 50, scale: 3 })
rect.transform({ translate: [10, 20], origin: 'top left', flip: 'both' })

// Relative (second arg true)
rect.transform({ rotate: 125 }).transform({ rotate: 37.5 }, true)

// Individual methods
rect.rotate(45)              // around center
rect.rotate(45, 50, 50)      // around point
rect.skew(0, 45)             // skew(x, y)
rect.scale(2)                // uniform
rect.scale(0.5, -1)          // x, y
rect.scale(2, 0, 0)          // scale(factor, cx, cy)
rect.translate(0.5, -1)      // translate(x, y)
rect.flip('x') | rect.flip('x', {x:20, y:30})

rect.transform()             // get decomposed values
rect.transform('rotate')     // get specific property
```
Parameter aliases: `translate/tx/ty`, `scale/sx/sy`, `skew/shear`, `origin/ox/oy`, `position/px/py`, `relative/rx/ry`. Origin keywords: `center`, `top`, `bottom`, `left`, `right`.

## ID, Classes, Visibility, Data
```js
rect.id('my-id') | rect.id() | rect.id(null)
rect.addClass('h') | rect.removeClass('h') | rect.hasClass('h') | rect.toggleClass('h')
rect.hide() | rect.show() | rect.visible()
rect.data('key', val) | rect.data('key') | rect.data('key', null)
```

## Document Tree
```js
group.add(rect) | group.add(rect, 0)   // add child, optionally at position
rect.addTo(group) | group.put(rect)    // add to parent (returns child)
rect.putIn(group)                      // add to parent (returns parent)
rect.clone()                           // deep clone (new ids)
rect.remove()                          // remove from document
rect.replace(draw.circle(100))         // replace element
rect.toParent(group)                   // move to new parent, preserve visual pos
rect.toRoot()                          // move to root
group.ungroup()                        // dissolve, apply transforms to children
drawing.flatten()                      // flatten all containers
rect.wrap('<g>')                       // wrap element
```

## Arranging
```js
rect.after(circle) | rect.before(circle)
rect.insertAfter(circle) | rect.insertBefore(circle)
rect.back() | rect.backward() | rect.front() | rect.forward()
rect.next() | rect.prev() | rect.position() | rect.siblings()
```

## Styles (CSS)
```js
rect.css('cursor', 'pointer') | rect.css({ cursor: 'pointer' })
rect.css('cursor') | rect.css() | rect.css('cursor', null)
```
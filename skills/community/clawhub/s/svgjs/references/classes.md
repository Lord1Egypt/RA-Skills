# Utility Classes

## SVG.Color
```js
new SVG.Color('#f06') | new SVG.Color('rgb(255,0,102)')
new SVG.Color({ r:255, g:0, b:102 }) | new SVG.Color({ h:255, s:0, l:102 })
new SVG.Color({ l:255, a:0, b:102 }) | new SVG.Color({ l:255, c:0, h:102 })
new SVG.Color({ c:255, m:0, y:102, k:0 })
color.toHex()       // '#ff0066'
color.toRgb()       // 'rgb(255,0,102)'
color.rgb() | color.hsl() | color.lab()  // convert space
color.to('#000')    // morphable

SVG.Color.random('vibrant')  // modes: vibrant(default), sine, pastel, dark, rgb, lab, grey
```

## SVG.Matrix
```js
new SVG.Matrix()                                    // identity
new SVG.Matrix(1, 0, 0, 1, 100, 150)               // 6 args
new SVG.Matrix({ translate: [20, 20] })             // transform object
new SVG.Matrix(rect)                                // element's CTM
new SVG.Matrix(svgElement.getCTM())                 // native SVGMatrix

matrix.transform({ rotate: 20 })                    // apply transform
matrix.clone() | matrix.inverse() | matrix.multiply(m2)
matrix.rotate(45) | matrix.rotate(45, 100, 150)    // deg, or deg+cx+cy
matrix.scale(2) | matrix.scale(2, 3) | matrix.scale(2, 100, 150)
matrix.skew(0, 45) | matrix.skew(0, 45, 150, 100)
matrix.translate(10, 20)
matrix.flip('x') | matrix.flip('x', 150)
matrix.toString()  // 'matrix(1,0,0,1,0,0)'
```

## SVG.Point
```js
new SVG.Point(1, 1) | new SVG.Point([1,1]) | new SVG.Point({x:1,y:1})
point.clone() | point.transform(matrix) | point.to(11, 10)  // morphable
```

## SVG.Box
```js
var box = rect.bbox()    // { x, y, width, height, x2, y2, cx, cy }
box.merge(otherBox)      // bounding box of two boxes
box.transform(matrix)
```

## SVG.Number
```js
new SVG.Number('78%')
number.plus('3%').toString()   // '81%'
number.valueOf()               // 0.81
number.divide('3%') | number.minus('3%') | number.times(2) | number.convert('px')
number.to('3%')                // morphable
```

## SVG.List
```js
new SVG.List([rect, circle])
list.fill('#ff0')              // apply to all members
list.animate(3000).fill('#ff0')// animate all
list.each('fill', 'blue')      // or list.each(fn)
```

## SVG.PointArray / SVG.PathArray
```js
// PointArray (polyline/polygon points)
new SVG.PointArray([[0,0], [100,100]])   // 2D array
new SVG.PointArray([0,0, 100,100])       // flat
polygon.array()                           // get reference
array.bbox() | array.clone() | array.to('100,0 0,100')
array.move(33, 75) | array.size(222, 333) | array.reverse()

// PathArray (path segments)
new SVG.PathArray([['M',0,0], ['L',100,100], ['z']])
path.array()                             // get reference
array.bbox() | array.move(33,75) | array.size(222,333)
// Segment syntax: ['M',x,y] ['L',x,y] ['H',x] ['V',y]
// ['C',x1,y1,x2,y2,x,y] ['S',x2,y2,x,y] ['Q',x1,y1,x,y] ['T',x,y]
// ['A',rx,ry,rot,large,sweep,x,y] ['Z']
```
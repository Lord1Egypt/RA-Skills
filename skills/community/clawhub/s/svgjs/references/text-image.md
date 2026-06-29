# Text, Images, Masks, Gradients

## Text
```js
draw.text("Line one.\nLine two.")                    // simple (newlines from \n)
draw.plain('Single line only')                       // no newline processing
draw.text(function(add) {                             // builder (full control)
  add.tspan('Hello ').fill('#f06')
  add.tspan('World').bold().newLine()
  add.tspan('Second line').dx(20)
})

text.text('New content') | text.clear()
text.font({ family: 'Helvetica', size: 144, anchor: 'middle', leading: '1.5em' })
text.font('family', 'Menlo') | text.leading(1.3)
text.amove(100, 50)       // move by baseline+anchor (vs corner-based move())
text.ax(200) | text.ay(200)  // x by anchor, y by baseline
text.length()              // computed text length
text.build(true)           // append mode; .build(false) to replace

// Tspan
text.tspan('content').fill('#f06').dx(30).dy(30)
tspan.newLine() | tspan.text('new') | tspan.length() | tspan.clear()

// TextPath
draw.textPath('Text', 'M 100 200 C 200 100 ...')
textpath.plot('M 300 500 ...')   // update path
textpath.track()                 // underlying path element
```

## Image
```js
draw.image('/path.jpg')
draw.image('/path.jpg', 200, 200)                     // with size
draw.image('/path.jpg', function() { this.size(200, 200) })  // onload callback
```

## Mask & ClipPath
```js
var mask = draw.mask(); mask.rect(100, 100).fill('#fff'); rect.maskWith(mask)
var clip = draw.clip(); clip.rect(50, 50); rect.clipWith(clip)
```

## Gradient & Pattern
```js
var grad = draw.gradient('linear', function(stop) {
  stop.at(0, '#333'); stop.at(0.5, '#f06'); stop.at(1, '#fff')
})
rect.fill(grad)

var pat = draw.pattern(20, 20, function(add) {
  add.rect(20, 20).fill('#fff'); add.circle(10).fill('#f06')
})
rect.fill(pat)
```
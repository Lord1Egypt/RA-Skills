# Events

```js
// Bind
rect.on('click', handler)
rect.click(function() { this.fill('#f06') })        // shortcut
rect.on('click mouseover', handler)                  // space-delimited
rect.on(['click', 'mouseover'], handler)             // array
rect.on('click', handler, window)                    // custom context

// Unbind
rect.off('click', handler)    // specific
rect.off('click')             // all for event
rect.off('click mouseover')   // multiple
rect.off()                    // ALL

// Fire
rect.fire('myevent')
rect.fire('myevent', { some: 'data' })               // with data
rect.fire('myevent', data, { cancelable: false })     // options
var event = rect.dispatch('myevent')                  // returns event
if (event.defaultPrevented) doNothing()

// Custom events
rect.on('myevent', function(e) { alert(e.detail.some) })
```

Available events: `click`, `dblclick`, `mousedown`, `mouseup`, `mouseover`, `mouseout`, `mousemove`, `touchstart`, `touchmove`, `touchleave`, `touchend`, `touchcancel`

## Namespaced Events
```js
rect.on('myevent.wicked', handler)    // attach
rect.off('myevent.wicked')            // detach namespace only
rect.off('.wicked')                   // detach all in namespace
rect.off('myevent')                   // detach all handlers (incl namespaced)
// fire('myevent') triggers ALL namespaced handlers
// fire('myevent.wicked') does NOT fire — namespaces are for unbinding only
```

**Best practice**: always namespace events (e.g. `event.wicked`) to avoid conflicts.

## Events on Other Elements
```js
SVG.on(window, 'click', handler) | SVG.off(window, 'click', handler)
# Animating

## `.animate()` — returns SVG.Runner (NOT element)

```js
rect.animate(1000).move(150, 150)               // duration
rect.animate(2000, 1000, 'now').fill('#f03')    // duration, delay, when
rect.animate({ duration: 2000, delay: 1000, when: 'now', times: 5, wait: 200 })

// Sequence by chaining .animate()
rect.animate().fill('#f03').animate().dmove(50, 50)
rect.animate().fill('#f03').delay(200).animate().dmove(50, 50)
```

**when**: `'now'` | `'absolute'`/`'start'` (absolute time) | `'last'`/`'after'` (after last animation)

## SVG.Runner

| Method | Description |
|--------|-------------|
| `runner.animate()` | Chain next animation |
| `runner.loop(times, swing, wait)` | Loop n times |
| `runner.ease('<>')` | Easing: `'<>'` in-out, `'>'` out, `'<'` in, `'-'` linear |
| `runner.during(fn)` | Callback every animation frame |
| `runner.after(fn)` | Callback after finish |
| `runner.pause()` / `runner.play()` | Pause/resume |
| `runner.stop()` | Stop and reset |
| `runner.finish()` | Jump to end |
| `runner.reverse()` | Play backwards |
| `runner.time()` / `runner.duration()` | Get/set time, get duration |
| `runner.position()` / `runner.progress()` | Get/set 0-1 progress (excl/incl waits) |
| `runner.schedule(tl, delay, when)` | Schedule on timeline |
| `runner.persist(bool)` | Keep after execution |
| `runner.queue(runOnce, runEveryStep)` | Chain plain functions |

## Easing & Controllers
```js
runner.ease('<>')                                  // default
runner.ease(SVG.easing.beziere(x1, y1, x2, y2))    // custom bezier
runner.ease(SVG.easing.step(5, 'jump-end'))         // stepped

rect.animate(new SVG.Spring(settleTime)).move(200, 200)  // spring physics
rect.animate(new SVG.PID(p, i, d)).move(200, 200)        // PID controller
// Controllers can't be orchestrated or reversed
```

## SVG.Timeline — orchestrate multi-element animations

```js
var tl = new SVG.Timeline()
rect1.timeline(tl); rect2.timeline(tl)
rect1.animate(300, 0, 'absolute').move(300, 300)    // starts at time 0
rect2.animate(400, 200, 'absolute').move(500, 500)   // starts at time 200

tl.finish() | tl.pause() | tl.play() | tl.stop()
tl.reverse() | tl.speed(2) | tl.time(100) | tl.seek(100)
```
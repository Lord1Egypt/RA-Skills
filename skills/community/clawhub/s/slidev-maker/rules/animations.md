# Slidev Animations

Click animations, slide transitions, and motion effects.

## v-click Directive

Make elements appear on click.
````html
<!-- Component usage -->
<v-click>This appears after one click</v-click>

<!-- Directive usage -->
<div v-click>This also appears on click</div>
````

Elements are hidden by default and appear when you press "next".

## v-after Directive

Make elements appear together with the previous v-click.
````html
<div v-click>Hello</div>
<div v-after>World</div>
````

Both "Hello" and "World" appear on the same click.

## Hide After Click

Use `.hide` modifier to hide elements after clicking.
````html
<div v-click>Visible after click 1</div>
<div v-click.hide>Hidden after click 2</div>
<div v-after.hide>Also hidden after click 2</div>

<!-- Component syntax -->
<v-click hide>Hidden after click</v-click>
````

## v-clicks for Lists

Apply v-click to all children automatically.
````markdown
<v-clicks>

- Item 1
- Item 2
- Item 3

</v-clicks>
````

Each item appears on successive clicks.

Nested lists with `depth`:
````markdown
<v-clicks depth="2">

- Item 1
  - Item 1.1
  - Item 1.2
- Item 2

</v-clicks>
````

Show multiple items per click with `every`:
````markdown
<v-clicks every="2">

- Item 1
- Item 2
- Item 3
- Item 4

</v-clicks>
````

## Click Positioning

### Relative Position

Relative values MUST be quoted strings starting with `+` or `-`.
````html
<div v-click>Click 1</div>
<div v-click="'+2'">Click 3 (skipped one)</div>
<div v-click="'-1'">Also click 2</div>
````

`v-after` is equivalent to `v-click="'+0'"`.

### Absolute Position

Unquoted numbers are absolute click positions.
````html
<div v-click="3">Appears at exactly click 3</div>
<div v-click="1">Appears at click 1</div>
````

### Enter and Leave Range

Show element only during specific click range.
````html
<!-- Visible from click 2 to 4 (exclusive), hidden otherwise -->
<div v-click="[2, 4]">Temporary content</div>
````

## v-switch Component

Switch between content based on clicks.
````html
<v-switch>
  <template #1>Shown at click 1</template>
  <template #2>Shown at click 2</template>
  <template #5-7>Shown at clicks 5 and 6</template>
</v-switch>
````

## Custom Click Count

Override automatic click counting in frontmatter.
````yaml
---
clicks: 10
---
````

The slide will require 10 clicks before advancing.

## Slide Transitions

Set default transition in headmatter.
````yaml
---
transition: slide-left
---
````

Override per slide in frontmatter.
````yaml
---
transition: fade
---
````

### Built-in Transitions
````yaml
transition: fade          # Crossfade in/out
transition: fade-out      # Fade out then fade in
transition: slide-left    # Slide to left
transition: slide-right   # Slide to right
transition: slide-up      # Slide up
transition: slide-down    # Slide down
transition: view-transition  # View Transitions API (experimental)
````

### Different Forward/Backward Transitions

Use `|` separator for different directions.
````yaml
---
transition: slide-left | slide-right
---
````

Forward uses `slide-left`, backward uses `slide-right`.

## v-motion Directive

Animate elements with @vueuse/motion.
````html
<div
  v-motion
  :initial="{ x: -80 }"
  :enter="{ x: 0 }"
  :leave="{ x: 80 }"
>
  Slidev
</div>
````

The element moves from -80px to 0 on enter, then to 80px on leave.

### Motion with Clicks

Trigger motion states on specific clicks.
````html
<div
  v-motion
  :initial="{ x: -80 }"
  :enter="{ x: 0, y: 0 }"
  :click-1="{ x: 0, y: 30 }"
  :click-2="{ y: 60 }"
  :leave="{ y: 0, x: 80 }"
>
  Animated text
</div>
````

Motion variants:
- `initial` - Before entering slide
- `enter` - When slide is active
- `click-x` - At click number x
- `click-x-y` - Between clicks x and y
- `leave` - When leaving slide

### Combine v-click with v-motion
````html
<div v-click="[2, 4]" v-motion
  :initial="{ x: -50 }"
  :enter="{ x: 0 }"
  :leave="{ x: 50 }"
>
  Shown at click 2, hidden at click 4
</div>
````

## v-mark Directive

Highlight text with rough notation marks.
````html
<span v-mark>Important text</span>
<span v-mark.circle>Circled text</span>
<span v-mark.red>Red highlight</span>
<span v-mark="{ color: '#234', type: 'underline' }">Custom</span>
````

Triggers on click like v-click. Set specific click:
````html
<span v-mark="3">Marked at click 3</span>
<span v-mark="'+1'">Marked one click after previous</span>
````
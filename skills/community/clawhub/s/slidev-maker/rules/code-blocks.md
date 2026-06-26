# Slidev Code Blocks

Code highlighting, Monaco editor, and Magic Move animations.

## Basic Code Blocks

Standard fenced code blocks with language identifier.
`````````````markdown
````````````typescript
const greeting: string = 'Hello, Slidev!'
console.log(greeting)
````````````
`````````````

Shiki is the only highlighter. Prism was removed in v0.50.

## Line Highlighting

Highlight specific lines using curly braces `{}`.
`````````````markdown
````````````ts {2,3}
function greet() {
  const name = 'World'  // highlighted
  return `Hello, ${name}`  // highlighted
}
````````````
`````````````

Line ranges and combinations:
`````````````markdown
````````````ts {1-3}
// Lines 1 through 3 highlighted
````````````
````````````ts {1,4,6-8}
// Lines 1, 4, and 6-8 highlighted
````````````
````````````ts {*}
// All lines highlighted
````````````
````````````ts {all}
// All lines highlighted (same as {*})
````````````
`````````````

## Multi-Step Line Highlighting

Use `|` to create click-based highlighting steps.
`````````````markdown
````````````ts {2-3|5|all}
function example() {
  const a = 1  // Click 1: lines 2-3
  const b = 2  // Click 1: lines 2-3
  
  const c = 3  // Click 2: line 5
  
  return a + b + c  // Click 3: all lines
}
````````````
`````````````

Start from a specific click:
`````````````markdown
````````````ts {*|2|3}{startLine:5}
// startLine changes display numbering
````````````
````````````ts {*|1-2|3-4}{at:2}
// Starts at click 2 instead of click 1
````````````
`````````````

## Hide and None States

Use `hide` to start with the code block hidden, or `none` to show code without any highlighting.
````markdown
```ts {hide|2|all}
function example() {
  const a = 1  // Click 1: code block appears, line 2 highlighted
  return a     // Click 2: all lines highlighted
}
```
```ts {none|1|2}
const a = 1  // Initially visible, no highlighting
const b = 2  // Click 1: line 1 highlighted
             // Click 2: line 2 highlighted
```
````

- `{hide}` - Code block starts hidden, reveals on first click
- `{none}` - Code block visible but no lines highlighted initially



## Line Numbers

Enable line numbers globally in headmatter:
`````````````yaml
---
lineNumbers: true
---
`````````````

Or per code block:
`````````````markdown
````````````ts {1|2|3} {lines:true}
const a = 1
const b = 2
const c = 3
````````````
````````````ts {lines:false}
// Line numbers disabled for this block
````````````
`````````````

Start from a specific number:
`````````````markdown
````````````ts {lines:true,startLine:100}
// Starts numbering at 100
````````````
`````````````

## Max Height with Scrolling

Limit code block height:
`````````````markdown
````````````ts {maxHeight:'200px'}
// Long code here
// Will scroll after 200px
````````````
`````````````

## Monaco Editor

Turn code blocks into editable Monaco editors.
`````````````markdown
````````````ts {monaco}
// This is editable in the browser
const x = 1
````````````
`````````````

Monaco with line highlighting:
`````````````markdown
````````````ts {monaco}{2,3}
const a = 1
const b = 2  // highlighted
const c = 3  // highlighted
````````````
`````````````

Monaco diff view:
`````````````markdown
````````````ts {monaco-diff}
const a = 1
~~~
const a = 2
````````````
`````````````

The `~~~` separates the original (top) from the modified (bottom).

## Monaco Runner

Execute code directly in the editor.
`````````````markdown
````````````ts {monaco-run}
console.log('This will execute!')
const result = 1 + 2
console.log(result)
````````````
`````````````

Configure auto-run:
`````````````markdown
````````````ts {monaco-run}{autorun:false}
// Won't auto-run, requires manual trigger
````````````
`````````````

## Magic Move

Animate between code changes. Requires 4-backtick wrapper.
`````````````markdown
````````````md magic-move
```````````js
console.log('Step 1')
```````````
```````````js
console.log('Step 2')
console.log('Added line')
```````````
```````````js
console.log('Final')
console.log('Added line')
console.log('Another line')
```````````
````````````
`````````````

With line highlighting in steps:
`````````````markdown
````````````md magic-move {at:2}
```````````js {*|1|2}
const a = 1
const b = 2
```````````
```````````js
const sum = a + b
```````````
````````````
`````````````

## TwoSlash

TypeScript type information on hover.
`````````````markdown
````````````ts twoslash
const greeting = 'hello'
//    ^?
````````````
`````````````

The `^?` shows the type at that position.

TwoSlash with errors:
`````````````markdown
````````````ts twoslash
// @errors: 2339
const obj = { a: 1 }
obj.b  // Error shown inline
````````````
`````````````

## Code Block Options Summary

All options go in curly braces after the language:
`````````````markdown
````````````ts {2,3}                    // Line highlight
```````````ts {monaco}                 // Monaco editor
``````````ts {monaco-run}             // Monaco with execution
`````````ts {monaco-diff}            // Monaco diff view
````````ts {lines:true}             // Show line numbers
```````ts {startLine:10}           // Start line numbers at 10
``````ts {maxHeight:'200px'}      // Scrollable height
`````ts twoslash                 // TwoSlash annotations
````ts {2|3|4}{at:2}            // Start at click 2
````

Combine multiple options:
````markdown
```ts {2,3}{lines:true,startLine:50}
// Lines 2-3 highlighted, numbered starting at 50
```
````
`````
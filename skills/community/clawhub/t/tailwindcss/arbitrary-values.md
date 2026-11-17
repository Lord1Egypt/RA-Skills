# Arbitrary Values — The Escape Hatch And Its Syntax

Square brackets take any CSS value; parentheses take a variable. The syntax has enough sharp edges that most "Tailwind ignored my value" reports land here.

## The Four Forms

```html
<div class="bg-[#1da1f2]">                          <!-- arbitrary value -->
<div class="[mask-type:alpha]">                      <!-- arbitrary property -->
<div class="[&>li]:border-b">                        <!-- arbitrary variant -->
<div class="w-(--sidebar-width)">                    <!-- CSS variable, v4 shorthand -->
```

v3 wrote the variable form as `w-[var(--sidebar-width)]`; v4 accepts both but `w-[--sidebar-width]` (bare, no `var()`) no longer resolves — a silent breakage on upgrade.

## Whitespace, Quotes, And Escapes

- Spaces become underscores: `grid-cols-[1fr_2fr_1fr]`, `shadow-[0_2px_8px_rgb(0_0_0/0.15)]`.
- A literal underscore is escaped: `content-['hello\_world']`.
- Underscores inside `url()` are left alone: `bg-[url('/img_hero.png')]` works as written.
- Commas need no escaping; parentheses must balance or the class is dropped without a warning.
- No spaces anywhere in the bracket, ever — the class attribute is space-delimited, so one space splits the class into two garbage tokens.

## Type Hints For Ambiguous Values

Some values could belong to more than one property. Prefix with a type or Tailwind guesses wrong:

```html
<div class="text-[length:var(--fluid)]">     <!-- font-size, not color -->
<div class="text-[color:var(--ink)]">        <!-- color, not font-size -->
<div class="bg-[image:var(--gradient)]">     <!-- background-image, not color -->
```

Literal values rarely need the hint (`text-[14px]` is unambiguous); variables almost always do, because the value is unknown at build time.

## Common Recipes

| Need | Class |
|---|---|
| Exact one-off color | `bg-[#1da1f2]`, `text-[oklch(0.7_0.15_150)]` |
| Fluid type | `text-[clamp(1rem,0.77rem+0.91vw,1.5rem)]` |
| Asymmetric grid | `grid-cols-[240px_minmax(0,1fr)]` |
| Calc sizing | `h-[calc(100dvh-4rem)]` |
| Unsupported property | `[scrollbar-gutter:stable]`, `[text-wrap:pretty]` |
| One-off breakpoint | `min-[900px]:flex`, `max-[420px]:hidden` |
| Selector Tailwind has no variant for | `[&:nth-child(3n)]:bg-gray-50` |
| Child styling from the parent | `[&>*+*]:mt-4` (or the `*:` variant) |
| Vendor pseudo-element | `[&::-webkit-scrollbar]:w-2` |
| Reading a variable set by JS | `w-(--panel-w)` with `style="--panel-w: 320px"` |

## When Not To Use One

- **Promotion threshold**: a value used ≥ `token_threshold` times (default 3) becomes a theme token (SKILL.md rule 2). Three `bg-[#1da1f2]` in the codebase means a rebrand is a repo-wide find-and-replace instead of one line.
- **Truly continuous values** — a width from a slider, a translate from a drag — are not arbitrary values; they are inline styles. Each distinct arbitrary value generates a distinct CSS rule, so a computed one either doesn't exist (built at runtime, never scanned) or generates a rule per possible value.
- **Anything a plain utility already covers.** `p-[16px]` instead of `p-4` breaks scale consistency and survives no scale change.
- **Complex multi-line CSS.** Past roughly one declaration's worth of value, a class in `@layer components` or a `@utility` is more readable and reviewable.

## Failure Modes

| Symptom | Cause |
|---|---|
| Class present in HTML, no rule generated | A space inside the brackets, or an unbalanced parenthesis |
| Value applies to the wrong property | Missing type hint on a variable |
| Works with a literal, not with a variable | v3 syntax `[--x]` in v4; use `(--x)` or `[var(--x)]` |
| Underscore appears literally in the output | It was escaped (`\_`) or is inside `url()` |
| Arbitrary variant matches nothing | Missing `&` in the selector: `&` is where the element's own selector lands |
| The value contains a `%` and breaks a template | Some template engines interpolate `%`; move the value into a token |
| Bundle grew after adding arbitrary values | Each unique value is its own rule; near-duplicates (`w-[301px]`, `w-[302px]`) accumulate |


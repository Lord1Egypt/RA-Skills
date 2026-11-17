# Components — Snippets, Bindings, Events, DOM Interop

**Contents**: [Snippets Replace Slots](#snippets-replace-slots) · [Events Are Attributes](#events-are-attributes) · [Bindings](#bindings) · [Attachments and Actions](#attachments-and-actions) · [Dynamic Components and Special Elements](#dynamic-components-and-special-elements) · [Control Flow Worth Knowing](#control-flow-worth-knowing) · [Accessibility Warnings Are Free Review](#accessibility-warnings-are-free-review) · [Component Shape Checklist](#component-shape-checklist)

## Snippets Replace Slots

```svelte
<!-- List.svelte -->
<script>
  let { items, row, empty } = $props();
</script>

{#if items.length}
  <ul>{#each items as item (item.id)}<li>{@render row(item)}</li>{/each}</ul>
{:else}
  {@render empty?.()}
{/if}

<!-- caller -->
<List {items}>
  {#snippet row(item)}<a href="/i/{item.id}">{item.name}</a>{/snippet}
  {#snippet empty()}Nothing here yet{/snippet}
</List>
```

- Content placed directly inside a component tag arrives as the `children` prop: `{@render children?.()}` is the default-slot equivalent. Always use `?.()` for optional content.
- Snippets take **arguments** — that is the whole point versus slots: the parent renders markup with data the child owns.
- A snippet is a value: pass it as a prop, store it in a variable, pick between two with a ternary, hoist a shared one to module scope in `<script module>`.
- Snippets declared in a component can be rendered anywhere in that component's markup, and only there; they are lexically scoped like functions.
- Recursion works: a `{#snippet node(item)}` that renders itself covers trees without a separate recursive component.

## Events Are Attributes

- `onclick={handler}`, `oninput`, `onsubmit` — plain attributes, no colon. Capture phase: `onclickcapture`.
- **No modifiers.** `|preventDefault` becomes `onsubmit={(e) => { e.preventDefault(); … }}`; `|once` becomes a handler that removes itself; `svelte/events` exports `on()` for imperative listeners with the same delegation semantics.
- Common events are **delegated** from the root. Consequence: a manually attached `addEventListener` on an ancestor may fire before the delegated handler, and `stopPropagation()` in a non-delegated listener can swallow component handlers. Use `on()` from `svelte/events` when order matters.
- No event forwarding shorthand: to pass an event up, take a callback prop (`onclick`) and spread the rest onto the element — `<button {...rest} onclick={onclick}>`.
- `onsubmit` on a form that posts to an action: let the action run and enhance it instead of intercepting (see the forms guidance in SKILL.md Quick Reference).

## Bindings

- Elements: `bind:value`, `bind:checked`, `bind:group`, `bind:files`, `bind:this`, and read-only ones (`clientWidth`, `offsetHeight`, `duration`, `paused`).
- Components: only for props declared `$bindable()`. Default to callback props; use a binding when the child genuinely owns an editing surface (an input wrapper, a rich-text editor).
- Function bindings give you a transform without a second variable: `bind:value={() => text, (v) => text = v.toUpperCase()}` (`svelte >=5.9`).
- `bind:this={el}` is `null` until mount — read it in `$effect`/`onMount`, never during render.
- `bind:group` needs the inputs to share the array reference; with `{#each}` bind to `group[i]` or an object field.

## Attachments and Actions

```svelte
<script>
  function tooltip(text) {
    return (node) => {                 // runs when the element is created
      const t = new Tippy(node, { content: text });
      return () => t.destroy();        // cleanup on removal or when text changes
    };
  }
</script>

<button {@attach tooltip(label)}>Hover</button>
```

- `{@attach fn}` (`svelte >=5.29`) supersedes `use:action`: it is a plain function, it re-runs when the state it reads changes (no `update` method to write), it composes through spread props, and it works on components as well as elements.
- Actions (`use:fn` with `{ update, destroy }`) still work and are not deprecated; keep them in a legacy codebase. New code gets attachments when `experimental_features` is true or the project is already on `svelte >=5.29` by choice (SKILL.md Configuration); otherwise write the action and note the newer form exists.
- This is the correct home for imperative libraries: create in the attachment, return the teardown, feed it `$state.snapshot(data)` so it never sees a proxy.

## Dynamic Components and Special Elements

- Any capitalized variable renders: `{@const C = map[kind]}<C {...props} />`. `<svelte:component>` is deprecated in runes mode.
- `<svelte:element this={tag}>` for a dynamic HTML tag; `this` must be a string, void elements cannot take children.
- `<svelte:window onkeydown={…} bind:scrollY>`, `<svelte:document>`, `<svelte:body>` — auto-removed listeners, SSR-safe.
- `<svelte:head>` for title and meta; in SvelteKit put page-level tags here, in the layout for defaults.
- `<svelte:options runes={true} />` pins a file's mode during a mixed migration; the same element's `customElement` option compiles the component into a custom element (packaging depth is routed from SKILL.md).
- `<svelte:boundary onerror={…}>` with a `failed` snippet catches render and effect errors in its subtree (`svelte >=5.3`); it does not catch errors in event handlers or async callbacks.

## Control Flow Worth Knowing

- `{#key expr}…{/key}` destroys and recreates the block when `expr` changes — the way to replay a transition or force a child to reinitialize.
- `{#await promise}` / `{:then value}` / `{:catch e}`; the initial block is skipped for an already-resolved promise during SSR.
- `{#each items as item, i (item.id)}` — the key expression is the last parenthesized argument, and it must be unique (`each_key_duplicate`).
- `{#each}` also destructures: `{#each rows as { id, name } (id)}`.
- `{@const}` inside a block computes once per iteration — cheaper and clearer than repeating an expression in three places.

## Accessibility Warnings Are Free Review

The compiler emits a11y warnings that most stacks only catch at audit time:

| Warning | Fix |
|---|---|
| `a11y_click_events_have_key_events` | Add `onkeydown`, or use a `<button>` |
| `a11y_no_static_element_interactions` | Give the element a `role`, or use the semantic tag |
| `a11y_missing_attribute` | `alt` on `<img>`, `href` on `<a>`, `title` on `<iframe>` |
| `a11y_label_has_associated_control` | `<label for={id}>` with `$props.id()` |
| `a11y_autofocus` | Remove it, or focus deliberately in an effect after route change |
| `a11y_media_has_caption` | `<track kind="captions">`, or `muted` for decorative video |

Treat them as errors in CI unless the project has decided otherwise (`accessibility posture` in the Configuration table).

## Component Shape Checklist

- Props destructured once from `$props()`, with defaults inline
- Content extension points as snippets, not as boolean props that toggle markup
- Data out through callback props; `$bindable` only where the child owns an editing surface
- No `$state` copy of a prop unless local divergence is intended
- Cleanup returned from every attachment and every effect that subscribes to something

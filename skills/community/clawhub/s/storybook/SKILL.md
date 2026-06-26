---
name: Storybook
description: Build component stories with proper args, controls, decorators, and testing patterns.
metadata: {"clawdbot":{"emoji":"📖","requires":{"bins":["npx"]},"os":["linux","darwin","win32"]}}
---

## CSF Format (Component Story Format)

- Default export is component meta—title, component, args, decorators
- Named exports are stories—each export becomes a story in sidebar
- `satisfies Meta<typeof Component>` for TypeScript type checking
- CSF3 uses object syntax, not functions—`export const Primary = { args: {...} }`

## Args vs ArgTypes

- `args` are actual prop values passed to component—`args: { label: 'Click me' }`
- `argTypes` configure controls UI—`argTypes: { size: { control: 'select', options: ['sm', 'lg'] } }`
- Default args in meta apply to all stories—override in individual stories
- `argTypes: { onClick: { action: 'clicked' } }` logs events in Actions panel

## Controls

- Auto-inferred from TypeScript props—boolean becomes toggle, string becomes text input
- Override control type: `argTypes: { color: { control: 'color' } }`
- Disable control: `argTypes: { children: { control: false } }`
- Options for select: `control: { type: 'select' }, options: ['a', 'b', 'c']`

## Decorators

- Wrap stories with context—providers, layout wrappers, theme
- Component-level in meta: `decorators: [(Story) => <Provider><Story /></Provider>]`
- Global in `.storybook/preview.js`: applies to all stories
- Order matters—later decorators wrap earlier ones

## Play Functions

- Interactive testing within story: `play: async ({ canvasElement }) => {...}`
- Use `@storybook/testing-library` for queries—`within(canvasElement).getByRole()`
- `await userEvent.click(button)` for interactions
- `expect(element).toBeVisible()` for assertions—tests run in browser

## Actions

- `argTypes: { onClick: { action: 'clicked' } }` auto-logs to Actions panel
- Or import: `import { action } from '@storybook/addon-actions'`
- Use `fn()` from `@storybook/test` in Storybook 8+ for spying in play functions
- Actions help verify event handlers without manual console.log

## Story Organization

- Title path creates hierarchy: `title: 'Components/Forms/Button'`
- Stories appear in order of export—put Primary first
- `tags: ['autodocs']` generates docs page automatically
- `parameters: { docs: { description: { story: 'text' } } }` adds story description

## Common Patterns

- **Default state:** `export const Default = {}`
- **With all props:** `export const WithIcon = { args: { icon: <Icon /> } }`
- **Edge cases:** Empty, Loading, Error, Disabled states as separate stories
- **Responsive:** Use viewport addon parameters per story

## Render Functions

- Custom render: `render: (args) => <Wrapper><Component {...args} /></Wrapper>`
- Access context in render: `render: (args, { globals }) => ...`
- Useful when story needs different JSX structure than default
- Prefer decorators for wrapping, render for restructuring

## Configuration

- `.storybook/main.js`: addons, framework, stories glob patterns
- `.storybook/preview.js`: global decorators, parameters, argTypes
- Stories glob: `stories: ['../src/**/*.stories.@(js|jsx|ts|tsx)']`
- Static assets: `staticDirs: ['../public']` for images/fonts

## Common Mistakes

- Forgetting to install addon AND add to main.js addons array
- Using `storiesOf` API—deprecated, use CSF exports
- Missing component in meta—controls won't auto-generate
- Decorators returning `Story` without calling it: `(Story) => <Story />` not `(Story) => Story`

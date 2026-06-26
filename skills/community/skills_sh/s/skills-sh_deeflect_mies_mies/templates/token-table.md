# Token Table Template

Use this as a scaffold for lockable design values. Keep the token categories the product needs, rename tokens to match the stack, and delete rows that would create fake precision. Every repeated value needs a role and usage boundary so future agents do not reinterpret it.

## Color Tokens

Rename these to match the project. Add or remove semantic colors based on real states.

| Token | Value | Role | Use When | Do Not Use For |
|---|---|---|---|---|
| --color-bg |  | Page background |  |  |
| --color-surface |  | Primary surface |  |  |
| --color-surface-raised |  | Raised surface |  |  |
| --color-border |  | Default boundary |  |  |
| --color-text |  | Body text |  |  |
| --color-text-strong |  | Primary text |  |  |
| --color-text-muted |  | Secondary text |  |  |
| --color-accent |  | Primary action / selected state |  | Decoration |
| --color-success |  | Success state |  |  |
| --color-warning |  | Warning state |  |  |
| --color-error |  | Error state |  |  |

## Type Tokens

Use the project's type scale if one exists. Do not create display tokens for a product UI that does not need display type.

| Token | Value | Role | Use When | Do Not Use For |
|---|---|---|---|---|
| --font-body |  | Body and UI |  |  |
| --font-display |  | Display moments |  | Labels / data |
| --text-xs |  | Small labels |  | Body copy |
| --text-sm |  | Compact UI |  |  |
| --text-md |  | Body |  |  |
| --text-lg |  | Subheads |  |  |
| --text-xl |  | Section headings |  |  |
| --text-display |  | Hero / brand display |  | Product labels |

## Spacing Tokens

Use the smallest scale that covers the interface. Delete unused sizes.

| Token | Value | Role | Use When | Do Not Use For |
|---|---|---|---|---|
| --space-1 |  | Tight internal gap |  | Page spacing |
| --space-2 |  | Control gap |  |  |
| --space-3 |  | Component padding small |  |  |
| --space-4 |  | Component padding default |  |  |
| --space-6 |  | Section internal gap |  |  |
| --space-8 |  | Large stack gap |  |  |
| --space-12 |  | Section spacing |  |  |
| --space-16 |  | Major section spacing |  |  |

## Shape And Depth Tokens

Only define depth if the interface uses elevation. Whitespace and borders may be the system.

| Token | Value | Role | Use When | Do Not Use For |
|---|---|---|---|---|
| --radius-sm |  | Small controls |  |  |
| --radius-md |  | Default controls |  |  |
| --radius-lg |  | Panels / large surfaces |  |  |
| --shadow-sm |  | Subtle elevation |  | Decoration |
| --shadow-md |  | Overlay / raised panel |  | Default cards |
| --border-width |  | Standard boundary |  | Accent stripe |

## Layout Tokens

Keep these at the level the product repeats: page, shell, grid, content width, or touch target.

| Token | Value | Role | Use When | Do Not Use For |
|---|---|---|---|---|
| --page-max |  | Page max width |  |  |
| --content-max |  | Reading width |  | Data tables |
| --grid-gap |  | Grid gutters |  | Component internals |
| --touch-target |  | Minimum touch target |  |  |

## Motion Tokens

Only define motion tokens when motion will repeat. Otherwise record the local choice as an exception or component detail.

| Token | Value | Role | Use When | Do Not Use For |
|---|---|---|---|---|
| --motion-fast |  | Small feedback |  | Page choreography |
| --motion-base |  | Default transition |  |  |
| --motion-slow |  | Large reveal |  | Product task flow delays |
| --ease-out |  | Default easing |  | Bounce / elastic effects |

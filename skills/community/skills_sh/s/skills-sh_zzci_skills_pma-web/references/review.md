# PMA-Web Review

## Required Verification

Before merge:

- lint passes
- typecheck passes
- build passes
- tests pass for the affected scope
- accessibility review completed for changed UI
- security review completed for changed trust boundaries

## Accessibility Review

For every UI-affecting change, verify:

- keyboard navigation works
- focus states are visible
- controls have labels or accessible names
- contrast is acceptable
- loading, empty, and error states remain understandable
- dialogs, popovers, and menus trap and restore focus correctly

## Security Review

For frontend changes, verify:

- no unsafe HTML injection
- no accidental secret exposure through client env usage
- auth and permission checks still match the product model
- redirects and route guards cannot be bypassed trivially
- untrusted URL or file input is validated before use

## UI Library Compliance

For any UI-affecting change, verify:

- no new dependency on Radix UI (`@radix-ui/*`) or any other component / primitive ecosystem (MUI, Mantine, Chakra, Ant Design, Headless UI, Ariakit, NextUI, Park UI, daisyUI, Flowbite, React Aria Components, …). Run `bun pm ls | grep -E '@radix-ui|@mui|@mantine|@chakra-ui|antd|@headlessui|@ariakit|@nextui|@park-ui'` (or equivalent) on diffs that touch `package.json`.
- new primitives went through the *Component sourcing order* in `baseline.md` — check whether shadcn or `@base-ui/react` already ships the requested component before accepting a hand-written one
- hand-written primitives, if present, are justified in the proposal and consume the same Tailwind tokens as shadcn (`bg-background`, `text-muted-foreground`, etc.); they do not introduce a parallel styling system
- shadcn `components.json` still declares `base-ui` as the component library (not the Radix-based option)

## Testing Guidance

- keep unit and integration tests in Vitest
- use Playwright only for critical flows that need browser coverage
- prefer focused tests around changed behavior over broad snapshot churn

## Generated And Owned Code

- treat shadcn output as owned code
- keep generated route tree files out of manual edits unless regeneration is impossible
- when generated files change, verify the underlying config and source files instead of reviewing generated diff alone

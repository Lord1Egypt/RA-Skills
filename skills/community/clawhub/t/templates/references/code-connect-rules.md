# Code Connect Rules

Code Connect is best effort by default.

Statuses:

- `mapped`: evidence links the Figma node/component to a code component.
- `unmapped`: a complete bounded scan of clear Code Connect files found no mapping.
- `unavailable`: repo/API/scanning cannot prove whether a mapping exists.
- `failed`: scanning was attempted but failed.

Hard rules:

- Do not turn `unavailable` into `unmapped`.
- Weak component-name matches are allowed only as `mapped` with `confidence: "low"`.
- `--require-code-connect` makes `unavailable` and `failed` return exit code `7`.
- Default mode never blocks repair only because Code Connect is unavailable.
- Even when Code Connect is unavailable, the repair expert must still search the local design system before writing custom CSS.

Local scan candidates:

- `*.figma.ts`
- `*.figma.tsx`
- `*.connect.ts`
- `*.connect.tsx`
- `figma.config.*`

The scan is bounded by `maxFiles` and reports `code_connect_scan_budget_exceeded` when the budget is reached.

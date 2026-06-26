# React Component Template

When planning a React component, ensure the following standards are met:

## Structure
- Functional components using Hooks (`useState`, `useEffect`).
- Separate logic (hooks) from presentation if complex.
- Use `PropTypes` or TypeScript types.

## Styling
- Vanilla CSS with modules or scoped styles.
- Responsive design by default.

## Patterns
- Use "Container/Presentational" pattern for data-heavy components.
- Memoize expensive calculations with `useMemo`.
- Handle loading and error states explicitly.

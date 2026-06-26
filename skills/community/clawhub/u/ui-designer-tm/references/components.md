# Component Patterns

Reusable component patterns from the UI Designer agent.

## Button

```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  font-family: var(--font-family-primary);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  line-height: 1;
  border-radius: var(--radius-md);
  border: 1px solid transparent;
  cursor: pointer;
  transition: all var(--transition-fast);
  text-decoration: none;
}

.btn:focus-visible {
  outline: 2px solid var(--color-primary-500);
  outline-offset: 2px;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Variants */
.btn-primary {
  background: var(--color-primary-500);
  color: white;
}
.btn-primary:hover:not(:disabled) {
  background: var(--color-primary-600);
}

.btn-secondary {
  background: var(--color-secondary-100);
  color: var(--color-secondary-700);
  border-color: var(--color-secondary-300);
}
.btn-secondary:hover:not(:disabled) {
  background: var(--color-secondary-200);
}

.btn-ghost {
  background: transparent;
  color: var(--color-secondary-700);
}
.btn-ghost:hover:not(:disabled) {
  background: var(--color-secondary-100);
}

.btn-danger {
  background: var(--color-error);
  color: white;
}
.btn-danger:hover:not(:disabled) {
  background: var(--color-error-dark);
}

/* Sizes */
.btn-sm {
  padding: var(--space-1) var(--space-3);
  font-size: var(--font-size-xs);
}
.btn-lg {
  padding: var(--space-3) var(--space-6);
  font-size: var(--font-size-base);
}
```

## Input

```css
.input {
  display: block;
  width: 100%;
  padding: var(--space-2) var(--space-3);
  font-family: var(--font-family-primary);
  font-size: var(--font-size-sm);
  color: var(--color-secondary-900);
  background: white;
  border: 1px solid var(--color-secondary-300);
  border-radius: var(--radius-md);
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.input::placeholder {
  color: var(--color-secondary-400);
}

.input:focus {
  outline: none;
  border-color: var(--color-primary-500);
  box-shadow: 0 0 0 3px var(--color-primary-100);
}

.input:disabled {
  background: var(--color-secondary-100);
  cursor: not-allowed;
}

.input-error {
  border-color: var(--color-error);
}
.input-error:focus {
  box-shadow: 0 0 0 3px var(--color-error-light);
}
```

## Card

```css
.card {
  background: white;
  border: 1px solid var(--color-secondary-200);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}

.card-header {
  padding: var(--space-4) var(--space-6);
  border-bottom: 1px solid var(--color-secondary-100);
}

.card-body {
  padding: var(--space-6);
}

.card-footer {
  padding: var(--space-4) var(--space-6);
  border-top: 1px solid var(--color-secondary-100);
  background: var(--color-secondary-50);
}
```

## Badge / Tag

```css
.badge {
  display: inline-flex;
  align-items: center;
  padding: var(--space-1) var(--space-2);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  border-radius: var(--radius-full);
  line-height: 1;
}

.badge-primary {
  background: var(--color-primary-100);
  color: var(--color-primary-700);
}

.badge-success {
  background: var(--color-success-light);
  color: var(--color-success-dark);
}

.badge-warning {
  background: var(--color-warning-light);
  color: var(--color-warning-dark);
}

.badge-error {
  background: var(--color-error-light);
  color: var(--color-error-dark);
}
```

## Loading States

```css
/* Skeleton */
.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-secondary-200) 25%,
    var(--color-secondary-100) 50%,
    var(--color-secondary-200) 75%
  );
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
  border-radius: var(--radius-md);
}

@keyframes skeleton-loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Spinner */
.spinner {
  width: 1.5rem;
  height: 1.5rem;
  border: 2px solid var(--color-secondary-200);
  border-top-color: var(--color-primary-500);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

## Responsive Breakpoints

```css
/* Mobile first */
@media (min-width: 640px)  { /* sm — tablets */ }
@media (min-width: 768px)  { /* md — small laptops */ }
@media (min-width: 1024px) { /* lg — desktops */ }
@media (min-width: 1280px) { /* xl — large screens */ }
@media (min-width: 1536px) { /* 2xl */ }
```

## Accessibility Checklist

- [ ] All interactive elements are keyboard accessible
- [ ] Focus states are visible (never `outline: none` without alternative)
- [ ] Color contrast meets WCAG AA (4.5:1 for text, 3:1 for UI components)
- [ ] Form inputs have associated `<label>` elements
- [ ] Error messages are announced to screen readers (`aria-live` or `role="alert"`)
- [ ] Icons have `aria-label` or accompanying text
- [ ] Loading states announce their presence to screen readers
- [ ] Modal/dialog traps focus and can be dismissed with Escape
- [ ] Skip links provided for keyboard navigation

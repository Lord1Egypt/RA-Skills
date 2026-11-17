# Accessibility

Use for changed UI behavior. Preserve the project's accessibility target and existing interaction patterns.

Prefer the existing accessible component or a native control. An ARIA role does not implement keyboard behavior. Check controls by accessible name and role as well as appearance.

| Changed interaction | Verify |
|---|---|
| Modal | A name and dialog semantics; focus enters it, stays within the active modal and returns appropriately when it closes. Escape and keyboard actions work. Background content is inert. |
| Form | Labels, instructions and errors are associated with fields. Errors preserve user input and explain recovery. A status update is announced without unnecessary focus changes. |
| Navigation or dynamic content | Focus remains visible and lands somewhere useful after a route change or removal. Keyboard users can reach, operate and leave controls. |
| Visual layout | Text contrast, zoom/reflow, focus visibility and target sizes meet the applicable WCAG criteria, including their exceptions. Color alone does not convey status. |
| Dragging, motion or sign-in | Provide the applicable non-dragging alternative, reduced-motion behavior and accessible authentication path. Do not disable paste or password managers. |

For a WCAG 2.2 AA target, check the applicable criteria and their exceptions:

- Text contrast: 4.5:1, or 3:1 for large text (18 pt, or 14 pt bold). Required visual information for active controls/states needs 3:1 against adjacent colors.
- Text resizes to 200% without losing content/functionality. Vertical content reflows at 320 CSS px without two-dimensional scrolling, except content that requires that layout.
- Pointer targets are at least 24 by 24 CSS px or meet a permitted spacing/equivalent/inline/control exception.
- Keyboard focus is visible and not entirely obscured by author-created content.

Use the matching WAI-ARIA pattern for a custom widget. Test the changed flow with a keyboard, and use the project's automated accessibility check where available. Add a targeted interaction test when behavior changes.

Automation cannot establish complete conformance. Report relevant manual checks that were unavailable, such as screen-reader behavior, instead of claiming that passing an automated scan proves accessibility.

## Sources

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [WAI-ARIA Authoring Practices patterns](https://www.w3.org/WAI/ARIA/apg/patterns/)
- [Modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)

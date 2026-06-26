# Execution Matrix — Word

Use this matrix before writing automation. Choose the path that matches the app state, not the one you remember first.

## Default Interface by Job

| Job | Preferred path | Why |
|-----|----------------|-----|
| Attach to a live Word session | `osascript` | Official CLI into Word's scripting dictionary |
| Read active document name, selection, or view | `osascript` | Keeps actions bound to live app state |
| Add comment, insert text, or move selection | `osascript` | Operates against the current document and review state |
| Update fields, TOC, or references | `osascript` | Must run inside the live document session |
| Export current document to PDF | `osascript` | Uses Word's own layout and export path |
| Offline structural DOCX editing | `word-docx` | Better fit than live app control |

## Platform Notes

### macOS

- Start with `osascript` for document, selection, comment, and export actions.
- Keep scripts short and verify active document identity before mutation.
- Use app-level commands only after a read-first step.

## Attach Strategy

### Choose `attach-existing` when

- the document is already open
- track changes, comments, or cursor position matter
- the user is actively reviewing the document

### Choose `launch-new` when

- isolation matters more than preserving the current UI session
- you need a controlled export pass
- the document should be opened in a clean app instance

### Choose `save-copy-first` when

- the document is business-critical
- accept/reject cleanup could be destructive
- the review state is not yet trusted

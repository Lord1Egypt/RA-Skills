---
summary: "googleauth templates via `//go:embed`"
read_when:
  - Editing auth UI
  - Touching template parsing/escaping issues
---

# googleauth templates (embed)

Problem: huge `templates*.go` files, noisy diffs, hard to edit.

## Current setup

- HTML lives in `internal/googleauth/templates/*.html`
- Go glue in `internal/googleauth/templates_embed.go` (`//go:embed`)
- Variable names preserved:
  - `accountsTemplate`
  - `successTemplateNew`
  - `successTemplate`
  - `errorTemplate`
  - `cancelledTemplate`

## Editing flow

- Edit the HTML files directly.
- Run `go test ./...` to confirm templates parse + execute (tests cover this).

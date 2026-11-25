# Static File Shadowing

Static files in public/ served ahead of a Rails route.

## Static File Vs ERB Template Shadowing

### The static file wins, and the ERB never runs

```text
# public/users/new.html exists as a static file
# app/views/users/new.html.erb also exists
```

A static file in `public/` is served directly by the web server, ahead of the
Rails route. The ERB template is never rendered, so any change to it has no
effect, and the spec asserts against the static copy.

This produces a very confusing failure: the spec fails on content that the
ERB template clearly does not produce, because the ERB template is not being
used at all.

```bash
# ✅ find the shadowing file
find public/ -name "*.html" | head -20
ls public/users/ 2>/dev/null
```

**Fix:** delete the static file. If a static page is genuinely needed, keep it
out of the path a controller route serves.

### The reverse: a route serves JSON but a static file exists

Same mechanism, different symptom - a JSON request returns HTML, and the spec
fails on a JSON parse error rather than a content mismatch.

---

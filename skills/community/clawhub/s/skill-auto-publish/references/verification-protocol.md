# Verification Protocol

Verification is mandatory. `clawhub publish` succeeding does not mean the work is correct.

---

## Registry Verification — Always Required

```bash
clawhub inspect <slug>
```

Verify all of:
- slug matches expected
- title matches expected
- summary / caption matches expected
- version matches target version
- install command present (`openclaw skills install <slug>`)
- key sections present (Activation, Features, boundaries)
- expected content changes reflected in the content
- no stale content from previous version (old sections, old examples, old phrasing)

If `clawhub inspect` returns HTML / security checkpoint → rate limit or bot protection is active. See `archive/failure-playbook.md` for handling steps.

---

## Public Page Verification — Depends on Mode

### Mode: `full`

Registry verification required.
Public page verification required if accessible.

Steps:
1. Open `https://clawhub.ai/<owner>/<slug>` in browser.
2. Use `browser_vision` or `browser_console` with JavaScript to extract actual rendered text.
3. Check: title, summary, activation wording, features section, boundaries section.
4. Check: old version residue removed, stale duplicate sections removed.
5. Check: expected visible content matches what user specified.

If public page is blocked → report `REGISTRY_PASS_PUBLIC_BLOCKED` or `BLOCKED`. Do not write `PASS`.

### Mode: `cli-only`

Registry verification required.
Public page verification may be skipped if user explicitly accepted cli-only mode.

Report: `NOT_RUN_CLI_ONLY` for Public Page Verification.
Do not imply public page was checked.

### Mode: `blocked-accept`

Use only when public page is known to be blocked by checkpoint/rate limit.
Registry verification must pass.
Public page verification: `BLOCKED_ACCEPTED`.
Do not write full `PASS`.

---

## Verification Methods — Strongest to Weakest

1. **CLI registry raw content** (`clawhub inspect <slug>` with file/content inspection) — strongest.
2. **Browser `innerText` / `document.body.innerText`** — actual rendered text.
3. **Browser console JavaScript extraction** — precise section content.
4. **Browser accessibility tree (`browser_snapshot`)** — can lie about rendering, use as hint only.

**Rule:** Trust the strongest available method. Do not downgrade verification method to make a check pass.

---

## PASS / MISMATCH / BLOCKED Rules

| Status | Meaning |
|--------|---------|
| `PASS` | All required checks passed under the selected verification mode. |
| `MISMATCH` | Registry or public page content differs from expected content. |
| `BLOCKED` | Verification could not be performed (access issue, checkpoint, rate limit). |
| `BLOCKED_ACCEPTED` | Public page blocked; user accepted this in verification mode. |
| `NOT_RUN_CLI_ONLY` | Public page check skipped due to cli-only mode. |
| `REGISTRY_PASS_PUBLIC_BLOCKED` | Registry passed; public page blocked. |

**PASS is protected.** Only write it when verification checks truly pass. Never write `PASS` for public page if the page was not actually read.

---

## Snapshot Pitfalls

- Browser accessibility tree shows element hierarchy but not actual visual rendering.
- Numbered list items can appear as "listitem: Fix First" in the tree but render as inline "Fix First" without the "1." prefix.
- Section structure in snapshot can look correct while actual page text is wrong.
- **When user provides exact expected content:** Compare against `innerText` / raw rendered text, not snapshot structure.

**Required technique for exact content verification:**
```javascript
browser_console({expression: `(function(){
  const h=Array.from(document.querySelectorAll('h2')).find(x=>x.textContent==='Section Name');
  if(!h)return'not found';
  const txt=h.parentElement.innerText;
  const idx=txt.indexOf('Section Name');
  return txt.substring(idx,idx+600);
})()`})
```
This returns actual rendered text, not accessibility tree.

---

## Vercel Security Checkpoint

If the public page shows a Vercel Security Checkpoint:
- Do not report `PASS`.
- Report `BLOCKED_BY_PUBLIC_PAGE_ACCESS` or `BLOCKED_BY_PUBLIC_PAGE_RATE_LIMIT`.
- Use registry verification as the primary check.
- Note the public page was blocked in the release report.
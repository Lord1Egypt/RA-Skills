# Dev Workflow

## New project workflow

1. Copy the template from `assets/template/`
2. Rename package/name/page as needed
3. Add required `features` in `manifest.json`
4. Implement UI in a single page first
5. Run build early before polishing

## Existing project workflow

1. Read the current page `.ux`
2. Identify whether the app is single-page state switching or router-based multi-page
3. Make the smallest possible edit
4. Build immediately
5. Fix exact reported errors before broader refactors

## Suggested command sequence

```sh
cd <project>
npx aiot build
```

If logs are noisy:

```sh
cd <project> && npx aiot build 2>&1 | grep -E "success|error|Error"
```

## Debug order

When build fails:
1. syntax / parser errors
2. event expression errors
3. missing files / wrong paths
4. style/layout polish

## Packaging/delivery

After successful build, check `dist/` for the `.rpk` output.
Only deliver after a green build.

## Product guidance for wearables

Before adding features, ask:
- Is it useful within 3-10 seconds?
- Does it fit a narrow tall screen?
- Does it avoid needing background persistence?
- Would it feel natural on a wrist device?

If not, simplify.

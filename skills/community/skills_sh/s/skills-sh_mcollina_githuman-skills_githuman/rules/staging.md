# Staging Files

GitHuman allows you to stage files directly in the web interface without switching to the terminal.

## Staging in the UI

### Stage Individual Files

On the unstaged changes view, each file has a stage button. Click it to stage that file for commit.

### Stage Hunks

For files with multiple changes, you can stage individual hunks (sections of changes) rather than the entire file.

### Unstage Files

Already staged files can be unstaged from the "Staged Changes" view.

## Staging from Terminal

You can also use standard git commands:

```bash
# Stage specific files
git add src/feature.ts tests/feature.test.ts

# Stage all changes
git add .

# Stage interactively
git add -p
```

GitHuman will reflect the staging state in real-time.

## Best Practices

1. **Review before staging** - Look at the diff in GitHuman before staging
2. **Stage related changes together** - Keep commits focused and atomic
3. **Don't stage generated files** - Avoid staging files that should be in .gitignore
4. **Use partial staging** - Stage only the hunks you want when a file has mixed changes

# Tips and Best Practices

Productivity tips for getting the most out of GitHuman.

## Quick Commands

```bash
# Start review quickly
npx githuman serve

# Approve and resolve the last review in one command
npx githuman resolve last

# Check pending todos before committing
npx githuman todo list
```

## Keyboard Shortcuts

In the web interface:

- `j` / `k` - Navigate between files
- `n` / `p` - Navigate between changes
- `c` - Add comment on selected line
- `s` - Stage current file
- `?` - Show all shortcuts

## Workflow Tips

### 1. Review Before Staging

Always review the diff before staging. This helps catch issues early:

```bash
npx githuman serve
# Review unstaged changes first
# Then stage what looks good
```

### 2. Use Partial Staging

When a file has both good and bad changes, stage only the good hunks from the UI.

### 3. Create Todos for Non-Blocking Issues

Don't block your commit for minor issues. Create a todo and address it in a follow-up:

```bash
npx githuman todo add "Improve error messages in auth module"
git commit -m "Add auth feature"
# Handle the todo later
```

### 4. Export Important Reviews

For significant changes, export the review for documentation:

```bash
npx githuman export last -o docs/reviews/feature-x.md
```

### 5. Check Todos Before Each Commit

Make it a habit:

```bash
npx githuman todo list && git commit -m "message"
```

## Integration with AI Workflows

When working with AI agents:

1. Let the AI make changes
2. Run `npx githuman serve` to review
3. Add comments for anything the AI should fix
4. Create todos for follow-up work
5. Approve and commit when satisfied

This creates a feedback loop where you can catch AI mistakes before they're committed.

## Performance Tips

- **Install globally** for faster startup: `npm install -g githuman`
- **Keep reviews small** - Review and commit frequently rather than accumulating large changesets
- **Use `--no-open`** when you already have the browser open: `npx githuman serve --no-open`

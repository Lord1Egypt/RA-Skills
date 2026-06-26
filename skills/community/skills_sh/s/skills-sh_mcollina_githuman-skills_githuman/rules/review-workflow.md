# Review Workflow

The complete workflow for reviewing AI-generated code changes before committing.

## Basic Workflow

### 1. AI Makes Changes

After an AI agent modifies your codebase, you'll have unstaged changes in git.

### 2. Start the Review Server

```bash
npx githuman serve
```

This opens the web interface at http://localhost:3847.

### 3. Review Unstaged Changes

The home page shows all unstaged changes. You can:

- View diffs for each modified file
- Stage individual files or hunks directly in the UI
- Add inline comments on specific lines

### 4. Stage Files for Review

Either:
- Click the stage button in GitHuman's UI next to each file
- Use git commands: `git add <files>`

### 5. Review Staged Changes

Navigate to "Staged Changes" to see what will be committed. This is your final review before committing.

### 6. Add Comments and Suggestions

Click on any line to add:
- Comments for questions or notes
- Suggestions for code improvements
- Todos for follow-up work

### 7. Resolve and Commit

When satisfied:

```bash
# Mark the review as approved
npx githuman resolve last

# Commit the changes
git commit -m "Your commit message"
```

## Example Session

```bash
# AI agent makes changes...

# Start review
npx githuman serve

# (Review in browser, stage files, add comments)

# Approve the review
npx githuman resolve last

# Check for any todos before committing
npx githuman todo list

# Commit
git commit -m "Add feature X"
```

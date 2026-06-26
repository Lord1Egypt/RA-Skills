# CLI Commands

Complete reference for all GitHuman CLI commands.

## serve

Start the web interface for visual code review.

```bash
npx githuman serve
```

Options:
- `--port <number>` - Use a custom port (default: 3847)
- `--no-open` - Don't open the browser automatically

## list

List all reviews in the current repository.

```bash
npx githuman list
```

Shows review ID, status, creation date, and file count.

## resolve

Mark a review as approved and resolve all comments.

```bash
# Resolve a specific review by ID
npx githuman resolve abc123

# Resolve the most recent review
npx githuman resolve last
```

## export

Export a review to markdown for documentation.

```bash
# Export to stdout
npx githuman export last

# Export to a file
npx githuman export last -o review.md

# Export a specific review
npx githuman export abc123 -o review-abc123.md
```

## todo

Manage todos for follow-up work.

```bash
# List all pending todos
npx githuman todo list

# Add a new todo
npx githuman todo add "Refactor the auth module"

# Mark a todo as done
npx githuman todo done 1

# Show all todos including completed
npx githuman todo list --all
```

## help

Show help for any command.

```bash
npx githuman --help
npx githuman serve --help
npx githuman todo --help
```

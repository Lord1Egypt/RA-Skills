# Todos

Track follow-up tasks during code review with GitHuman's todo feature.

## Creating Todos

### From the Web UI

While reviewing code, you can create todos directly from inline comments. This links the todo to the specific line of code.

### From the CLI

```bash
npx githuman todo add "Write tests for the new endpoint"
npx githuman todo add "Update documentation for API changes"
```

## Listing Todos

```bash
# Show pending todos
npx githuman todo list

# Show all todos including completed
npx githuman todo list --all
```

Example output:
```
Pending todos:
  1. [ ] Write tests for the new endpoint
  2. [ ] Update documentation for API changes
  3. [ ] Review error handling in auth module
```

## Completing Todos

```bash
# Mark todo #1 as done
npx githuman todo done 1
```

## Best Practices

1. **Create todos during review** - When you spot something that needs attention but isn't blocking, create a todo
2. **Check todos before committing** - Run `npx githuman todo list` before each commit
3. **Keep todos actionable** - Write clear, specific tasks
4. **Link to code** - Create todos from inline comments to maintain context

## Workflow Integration

```bash
# After AI makes changes
npx githuman serve

# (Review and create todos for follow-up work)

# Check what's pending
npx githuman todo list

# If todos are blocking, address them first
# If not, commit and handle todos in follow-up commits
git commit -m "Add feature X"

# Work through remaining todos
npx githuman todo done 1
# ... make changes ...
git commit -m "Add tests for feature X"
```

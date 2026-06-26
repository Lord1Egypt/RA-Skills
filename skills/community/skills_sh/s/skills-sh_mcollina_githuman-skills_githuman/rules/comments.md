# Comments and Suggestions

Add inline comments and suggestions to code during review.

## Adding Comments

### Inline Comments

Click on any line in the diff view to add a comment. Comments are attached to specific lines and will show in context.

### Comment Types

- **Question** - Ask for clarification about the code
- **Note** - Leave information for future reference
- **Suggestion** - Propose a code change
- **Issue** - Flag a problem that needs attention

## Suggestions

Suggestions allow you to propose specific code changes:

1. Click on the line you want to change
2. Select "Suggestion" as the comment type
3. Write the suggested replacement code
4. The reviewer can apply the suggestion directly

## Resolving Comments

Comments can be resolved in two ways:

1. **Individually** - Click the resolve button on each comment
2. **All at once** - Run `npx githuman resolve last` to mark the review as approved and resolve all comments

## Best Practices

1. **Be specific** - Reference exact variable names, functions, or patterns
2. **Explain why** - Don't just say "change this", explain the reasoning
3. **Use suggestions for simple fixes** - If you know exactly what the code should be, use a suggestion
4. **Create todos for complex issues** - If a comment requires significant work, convert it to a todo
5. **Keep comments focused** - One issue per comment makes them easier to track and resolve

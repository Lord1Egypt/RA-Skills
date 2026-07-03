# Ralph Loop Skill

Autonomous AI coding loop that runs Codex/Claude Code repeatedly until all PRD items are complete.

**Source:** https://github.com/snarktank/ralph (8,600+ stars)

## Concept

Ralph solves the "context overflow" problem. Large tasks exceed one context window → bad code. Ralph:
1. Breaks work into small user stories in `prd.json`
2. Spawns FRESH coding agent instance per story
3. Each instance implements ONE story, runs tests, commits if passing
4. Marks story as `passes: true`
5. Repeats until all stories pass

Memory persists via: git history, progress.txt, prd.json (not context).

## Quick Start

```bash
# 1. Create a PRD for your feature
~/agent-workspace/skills/ralph/scripts/create-prd.sh "Feature description"

# 2. Convert PRD to prd.json
~/agent-workspace/skills/ralph/scripts/convert-prd.sh tasks/prd-feature.md

# 3. Run Ralph loop
~/agent-workspace/skills/ralph/scripts/run-ralph.sh [project_dir] [max_iterations]
```

## Files

| File | Purpose |
|------|---------|
| `prd.json` | User stories with `passes: true/false` |
| `progress.txt` | Learnings between iterations |
| `AGENTS.md` | Updated with patterns/gotchas each iteration |

## prd.json Format

```json
{
  "branchName": "ralph/feature-name",
  "userStories": [
    {
      "id": "1",
      "title": "Add database column",
      "description": "Add email_verified column to users table",
      "acceptanceCriteria": [
        "Migration exists",
        "Column is boolean, default false",
        "Tests pass"
      ],
      "priority": 1,
      "passes": false
    }
  ]
}
```

## Right-Sized Stories

✅ Good (one context window):
- Add a database column and migration
- Add a UI component to existing page
- Update a server action with new logic
- Add a filter dropdown to a list

❌ Too big (split these):
- "Build the entire dashboard"
- "Add authentication"
- "Refactor the API"

## Integration with Codex CLI

Ralph uses Codex CLI (`codex exec`) or Claude Code for implementation:

```bash
# Default: uses Codex CLI
./run-ralph.sh ~/Code/myproject 10

# Or specify Claude Code
./run-ralph.sh ~/Code/myproject 10 --tool claude
```

## Workflow

1. **Create PRD** → Detailed markdown requirements
2. **Convert to prd.json** → Structured user stories
3. **Run Ralph** → Loop until all pass
4. **Review** → Check commits, merge branch

## Example Session

```bash
# Henry asks: "Implement RLS for all 154 tables"

# 1. Create PRD
~/agent-workspace/skills/ralph/scripts/create-prd.sh "Implement Row Level Security for all database tables"

# 2. Convert (generates 154 user stories)
~/agent-workspace/skills/ralph/scripts/convert-prd.sh tasks/prd-rls-migration.md

# 3. Run overnight
nohup ~/agent-workspace/skills/ralph/scripts/run-ralph.sh ~/Code/myproject 154 > ralph.log 2>&1 &

# 4. Check progress
cat ~/Code/myproject/scripts/ralph/prd.json | jq '.userStories[] | {id, title, passes}'
```

## Stop Conditions

- All stories have `passes: true` → outputs `<promise>COMPLETE</promise>`
- Max iterations reached
- Manual stop (Ctrl+C)

## Tips

1. **Small stories** - Each should complete in one context window
2. **Good tests** - Ralph relies on test feedback
3. **AGENTS.md** - Keep updated with patterns/gotchas
4. **Browser verification** - For UI stories, include "Verify in browser" criteria

## References

- [Ralph GitHub](https://github.com/snarktank/ralph)
- [Geoffrey Huntley's article](https://ghuntley.com/ralph/)
- [Ryan Carson's thread](https://x.com/ryancarson/status/2008548371712135632)

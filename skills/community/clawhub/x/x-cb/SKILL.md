---
name: x-cb
description: "Interact with Codeberg using the `x cb` CLI. Use `x cb repo`, `x cb issue`, `x cb pr`, `x cb org`, `x cb team`, and `x cb user` for managing repositories, issues, PRs, organizations, teams, and users on Codeberg. Trigger when user mentions Codeberg, needs to manage Codeberg repos/issues/PRs, clone from codeberg.org, or work with Codeberg organizations or teams."
---

# Codeberg Skill (x cb)

Use `x cb` to interact with Codeberg (codeberg.org). Get your token at: https://codeberg.org/user/settings/applications

## Repository

Clone a repository:
```bash
x cb repo clone <owner>/<repo>
```

List repositories in an organization:
```bash
x cb repo ls <org_path>
```

Create a public repository:
```bash
x cb repo create --access public <name>
```

Add a collaborator to a repository:
```bash
x cb repo collaborator add <owner>/<repo> <username> --permission push
```

## Issue

List issues in a repository:
```bash
x cb issue ls --repo <owner>/<repo>
```

Create an issue:
```bash
x cb issue create -r <owner>/<repo> --title "Bug" --body "Description"
```

## Pull Request

List pull requests in a repository:
```bash
x cb repo pr ls --repo <owner>/<repo> --state open
```

Create a pull request:
```bash
x cb repo pr create --repo <owner>/<repo> --base develop --head main --title "Fix"
```

## Organization

List organizations:
```bash
x cb org ls
```

List repositories in an organization:
```bash
x cb org repo ls <org_path>
```

## Team

List teams in an organization:
```bash
x cb team ls --org <org_path>
```

Create a team with permissions:
```bash
x cb team create --org <org_path> --units 'repo.code' --units_map '{"repo.code": "write"}' <team_name>
```

## User

Show current user info:
```bash
x cb user info
```

List current user's repositories:
```bash
x cb user repo ls
```

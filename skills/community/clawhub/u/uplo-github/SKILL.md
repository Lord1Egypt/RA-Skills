---
name: uplo-github
description: AI-powered GitHub knowledge management. Search repository metadata, code review standards, issue tracking, and team workflows with structured extraction.
---

# UPLO GitHub — Repository & Development Workflow Intelligence

UPLO ingests and indexes your GitHub organization's metadata: repository descriptions, team ownership via CODEOWNERS, open and closed issues, pull request discussions, CI/CD workflow configurations, release notes, and contribution guidelines. Rather than jumping between GitHub tabs and searching markdown files across dozens of repos, you can query your entire development organization's institutional knowledge from one place.

## Session Start

Fetch your context to see which repositories and teams you have visibility into. GitHub data in UPLO respects organizational boundaries — you will only see repos and teams your clearance covers.

```
get_identity_context
```

## Example Workflows

### Onboarding a New Team Member

A developer just joined the Payments team and needs to ramp up on the codebase, conventions, and active work.

```
search_with_context query="Payments team repository ownership, contribution guidelines, and code review standards"
```

```
search_knowledge query="open issues labeled good-first-issue or onboarding in payment service repositories"
```

```
search_knowledge query="recent architectural decisions or RFCs related to the payments platform"
```

### Cross-Team Dependency Investigation

The mobile team's build is failing because of a breaking change in a shared library. They need to understand who made the change and why.

```
search_knowledge query="recent pull requests and releases in the shared-sdk repository with breaking changes"
```

```
search_with_context query="teams that depend on shared-sdk and their pinned version requirements"
```

```
search_knowledge query="CODEOWNERS and maintainers for the shared-sdk authentication module"
```

## When to Use

- A developer asks which team owns a particular service and who to tag for code review
- Someone needs to find all repositories that have CI workflows using a deprecated GitHub Actions runner
- A tech lead wants to understand the history of decisions around the monorepo-vs-polyrepo structure
- An engineer is looking for open issues related to rate limiting across all backend services
- Product asks how many PRs were merged into the billing service in the last sprint
- Someone needs the release process documentation for the customer-facing API
- A new hire wants to understand the branching strategy and merge requirements for the main product repo

## Key Tools for GitHub

**search_knowledge** — Query across all ingested GitHub data. Great for specific lookups: `query="GitHub Actions workflow file for the deployment pipeline in the infrastructure repo"`. Works well for finding CODEOWNERS entries, contribution guidelines, and issue details.

**search_with_context** — Connects GitHub metadata with organizational context. When you ask `query="who are the subject matter experts for the authentication service and what are the open security-related issues"`, it combines CODEOWNERS data with team profiles and issue trackers.

**get_directives** — Engineering leadership often sets directives that affect repository management: migration to a new CI provider, adoption of trunk-based development, deprecation of certain frameworks. Check directives before advising on workflow changes.

**flag_outdated** — GitHub metadata changes rapidly. If a CODEOWNERS file references a team that was reorganized or a README documents a deployment process that moved to a different tool, flag it: `entry_id="..." reason="CODEOWNERS lists @platform-legacy-team which was dissolved and split into @platform-core and @platform-reliability in Q1 2026"`

## Tips

- GitHub data in UPLO is a snapshot from the last ingestion sync, not a live mirror. For real-time data (current CI status, latest commit), go to GitHub directly. UPLO excels at historical context and cross-repo search that GitHub's native search handles poorly.
- When searching for code ownership, query both CODEOWNERS files and team membership data. CODEOWNERS defines review requirements, but the actual subject matter expert might be someone who wrote the original code but is no longer listed as a required reviewer.
- Issue and PR discussions contain valuable decision context that often is not captured anywhere else. If someone asks "why did we choose approach X", search PR descriptions and review comments — the reasoning lives in the discussion threads.
- Repository naming conventions and team structures vary by organization. If your first query does not return results, try alternative names — repos might use hyphens vs. underscores, abbreviations vs. full names, or have been recently renamed.

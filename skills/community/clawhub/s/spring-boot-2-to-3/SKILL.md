---
name: spring-boot-2-to-3
description: Migrate Spring Boot 2.7.x applications to Spring Boot 3.x with a recipe-first OpenRewrite workflow, then complete manual compatibility fixes and verification. Use only when the project is already on Boot 2.7.x; projects on 2.6 or earlier may fail—upgrade to 2.7.x first. Covers pom.xml/build.gradle, javax-to-jakarta, Spring Security config, dependency alignment, Dockerfile Java base image.
---

# Spring Boot 2 to 3 Upgrade

## Overview

Upgrade a **Spring Boot 2.7.x** service to 3.x in controlled stages: baseline capture, automated OpenRewrite migration, manual compatibility fixes, and regression validation.
Prefer small, verifiable commits and keep each migration stage reversible.

## Supported source version

- **This skill applies only to projects on Spring Boot 2.7.x.** The OpenRewrite recipe chain and manual checklist assume a 2.7.x baseline.
- **If the project is on Spring Boot 2.6 or earlier**, do not run this skill directly—upgrades may fail or be incomplete. First upgrade the project to **2.7.x** (e.g. with `UpgradeSpringBoot_2_7` or manual POM changes), get the build and tests green, then use this skill to migrate 2.7.x → 3.x.
- At the start of the workflow, **verify** the Boot version (e.g. from parent or `spring-boot.version`); if it is not 2.7.x, stop and tell the user to upgrade to 2.7.x first.

## Target version

- **Spring Boot**: Prefer the **latest 3.5.x** line for new migrations. Versions 3.0–3.4 are transition lines; 3.5.x is the current stable target. When using OpenRewrite, use the `UpgradeSpringBoot_3_5` recipe (or the latest Boot 3.x recipe available).
- **API docs (Springfox → springdoc)**: With **Spring Boot 3.5** use **springdoc-openapi 2.8.x**. Do not use springdoc-openapi 3.0.0 for Boot 3.5—3.0.0 targets Spring Boot 4. Check [springdoc releases](https://github.com/springdoc/springdoc-openapi/releases) for the exact 2.8.x version aligned to your Boot 3.5.x.

## What This Skill Does

- ✅ Automated Spring Boot 2 → 3 upgrade (target latest 3.5.x)
- ✅ JDK 8 → 21 migration
- ✅ javax.* → jakarta.* namespace migration
- ✅ Hibernate 5 → 6 adaptation
- ✅ Configuration property updates
- ✅ Dependency version resolution
- ✅ **Dockerfile / container image**: upgrade Java base image to 17+ (or 21) via OpenRewrite [rewrite-docker](https://github.com/openrewrite/rewrite-docker) or text-based recipes
- ✅ Full validation and testing workflow

## Prerequisites Check

- **Spring Boot version**: The project must be on **2.7.x**. If it is 2.6 or earlier, do not proceed with this skill; instruct the user to upgrade to 2.7.x and pass tests first.
- Before starting, verify (according to project build tool):
```bash
java -version    # Need JDK 17+ to run OpenRewrite
mvn -version     # Maven 3.8.1+ if using pom.xml
./gradlew --version   # If using build.gradle / build.gradle.kts
```

If target workflow includes `UpgradeToJava21`, ensure JDK 21 toolchain is available in CI and runtime image.
If missing, guide user to install or offer to create installation script.

## Workflow

### 1) Confirm Upgrade Path and Baseline

1. Detect build tool (`pom.xml` or `build.gradle`/`build.gradle.kts`), Java version, and test commands. **Confirm the project is on Spring Boot 2.7.x** (from parent or property); if not, stop and ask the user to upgrade to 2.7.x before using this skill.
2. **Verify the project compiles and tests pass** (e.g. `./mvnw -q compile test` or `./gradlew build`). Do not start migration until baseline is green; if there are known failures, document them and get user sign-off before proceeding.
3. Record current versions for Spring Boot, Spring Cloud, Spring Security, Hibernate, and API doc libs.
4. **Create safety checkpoints** only after baseline is green. **Run the following git command yourself** (do not ask the user to run it). The **current branch** (e.g. `main`) is already the rollback anchor—no need to create a separate backup branch. Create and switch to a **working branch** for the migration: `git checkout -b upgrade/sb3-<target-version>`. If rollback is needed, switch back to the original branch or compare against it.
5. Run the check script from this skill’s `scripts/` directory, passing the target project path: `scripts/check.sh <project-dir>` (e.g. from workspace root: `spring-boot-2-to-3/scripts/check.sh <project-dir>`). It captures Boot version hints, `javax` residue, and Springfox usage.
6. Save baseline artifacts (`dependency tree`, test summary, startup log) under the `docs/` directory.
7. If the project ships with a **Dockerfile** (or similar container build), record the current Java base image (e.g. `eclipse-temurin:11-jdk`) so it can be aligned to the target Java version (17 or 21) after the code migration.

Use this phase to answer:
- Is Java 17+ already active?
- Does the project still use `javax.*` imports?
- Does the project rely on removed/deprecated Boot 2 behavior?

### 2) Apply OpenRewrite First

1. Use OpenRewrite recipes to perform the broad mechanical migration from Boot 2 to Boot 3.
2. **Run** `git add` and `git commit` for the recipe-generated changes only (message prefix `chore(rewrite):`). Do not ask the user to commit.
3. Build and run tests to expose remaining manual issues.
4. If the target project has its own OpenRewrite/migration scripts, run those and retain stage logs.

Load [references/openrewrite-recipes.md](references/openrewrite-recipes.md) for Maven/Gradle commands and recipe sets.

### 3) Perform Manual Compatibility Fixes

1. Resolve compile/runtime issues not fully covered by recipes.
2. Focus on namespace migration (`javax` -> `jakarta`), security config changes, and framework-specific behavior changes.
3. Align dependent libraries to Boot 3 compatible versions.
4. Keep fixes scoped and grouped by concern.
5. If identical issues appear across modules/repos, extract them into custom OpenRewrite recipes for reuse.
6. **Run** `git add` and `git commit` once per topic (e.g. `jakarta`, then `security`, `httpclient`, `tests`) to keep rollback granular. Execute the commits yourself; do not ask the user to run git.
7. **Dockerfile**: Upgrade the Java base image in `Dockerfile` (or container build) to match the target JDK (17+ or 21). Use OpenRewrite [rewrite-docker](https://docs.openrewrite.org/recipes/docker) (e.g. `Change Docker FROM`) or a text-based recipe; see [references/openrewrite-recipes.md](references/openrewrite-recipes.md) and [references/manual-fix-checklist.md](references/manual-fix-checklist.md).

Load [references/manual-fix-checklist.md](references/manual-fix-checklist.md) and execute only relevant sections.

### 4) Validate End-to-End

1. Run unit/integration tests.
2. Start the app and check key health/business endpoints.
3. Review startup logs for warnings related to migration.
4. Run `scripts/check.sh` again (with the project path) and compare with baseline (e.g. no remaining `javax`).
5. Summarize remaining risk and follow-up tasks.
6. If runtime failures appear (`NoSuchMethodError`, `ApplicationContext` load issues), run targeted triage from `references/manual-fix-checklist.md`.
7. **Generate an upgrade report**: create a file under `docs/` (e.g. `docs/<yyyymmdd>-upgrade-summary.md`) containing: date, original branch (rollback anchor) and working branch, target Boot/Java versions, summary of changes by stage, validation result (compile/test), remaining risks or follow-up items. This gives the user and future readers a single place to see what was done and what to do next.

### 5) Rollback and Failure Handling (when something goes wrong)

Apply as needed during or after stages 2–4; not a sequential step after validation.

**On any failure (compile, test, or runtime): rollback and generate a failure report.**

1. **Rollback**: Restore a safe state so the repo is usable again.
   - If the failure is on the **working branch** (e.g. after OpenRewrite or a manual fix): either reset to the last good commit on that branch, or switch back to the **original branch** (e.g. `git checkout main`) so the user is on the pre-migration state. Prefer reverting topic commits or resetting the working branch before abandoning it; only switch to the original branch if recovery on the working branch is not practical.
   - The original branch must remain unchanged; use it as the rollback target when needed.
2. **Failure report**: Create a file under `docs/` (e.g. `docs/<yyyymmdd>-upgrade-failure.md`) containing: date, branch and commit at failure, **stage where it failed** (e.g. after OpenRewrite, after manual fix, during test), **error summary** (compile errors, test failures, or runtime exception), commands run, and **suggested next actions** (e.g. run recipes in smaller batches, fix a specific dependency, or upgrade to 2.7.x first). This gives the user a clear record of what went wrong and how to proceed.
3. If rewrite batch breaks compile: after rollback and failure report, the user may retry with recipes in smaller batches (see `references/openrewrite-recipes.md` for incremental recipe sequence).
4. If runtime regression is high-risk: after rollback and failure report, suggest comparing against the original branch and reverting topic commits on the working branch on a retry.

## Execution Rules

- **Run all git commands yourself** (branch, commit) as part of the workflow; do not instruct the user to run git. The user should not need to execute any git commands for the migration.
- Prefer "recipe-first" over ad-hoc hand edits.
- Use `scripts/check.sh` before and after migration to compare baseline drift.
- Keep migration commits small and thematic; **perform the commits yourself**:
  - Commit A: baseline and build setup (if any)
  - Commit B: OpenRewrite output
  - Commit C+: manual fixes by topic (including Dockerfile Java base image if present)
- **Use the current branch as the rollback anchor**; create only a working branch (e.g. `upgrade/sb3-3.5`) for the migration. Do not create a separate backup branch—the original branch is the backup.
- **On failure: always rollback to a safe state and generate a failure report** in `docs/` (e.g. `docs/<yyyymmdd>-upgrade-failure.md`) with stage, error summary, and next actions. Do not leave the repo in a broken state without a written report.
- Never assume all changes are safe after a successful compile; run tests and boot smoke checks.
- If tests are missing, create a minimal smoke checklist and report explicit risk.

## Output Contract

When using this skill, return:
1. A concise migration plan for this repo.
2. Exact commands run (including git: branch, commit) and rewrite + verification commands.
3. Files changed grouped by migration stage.
4. Remaining blockers/risks with next actions.
5. Any **CI/CD or Dockerfile** changes (e.g. Java version in pipeline, base image) so they are not forgotten.
6. **On success**: path to the generated **upgrade report** (e.g. `docs/<yyyymmdd>-upgrade-summary.md`). **On failure**: path to the **failure report** (e.g. `docs/<yyyymmdd>-upgrade-failure.md`) and confirmation that rollback was performed.

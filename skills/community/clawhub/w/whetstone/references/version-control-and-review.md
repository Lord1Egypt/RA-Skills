# Version control and review

Use for commits, branches, pull requests, responding to review, or reviewing a diff.

## Git rules for agents

- Commit, push, open a pull request, merge or tag only when the user or the repository's instructions ask for it.
- Do not force-push a shared branch, rewrite published history or delete someone else's branch without explicit permission.
- Do not bypass hooks or checks, for example with `--no-verify`. Fix what they report.
- Before committing, read `git status` and the staged diff, and stage files by name so that build output, local configuration and secrets stay out.
- Follow the repository's conventions for branch names, commit format, sign-off and trailers.

## Focused changes

Give each commit and pull request one purpose. Keep refactoring, formatting and dependency updates apart from behavior changes, and ship tests with the change they cover. Split large work into steps that each leave the system working: preparation, new code behind a flag, switch-over, clean-up. Keep an unavoidable mechanical change purely mechanical, and say how it was produced so that reviewers can check the method.

Write the commit subject in the imperative, about 50 characters long, then a blank line and a body that says what changed and why. Use Conventional Commits only when the repository does.

## Describe the pull request

Say what changed and why, how it was verified (commands and results, screenshots for UI, numbers for performance), what was not verified, the main risks and how to roll back. Add the tier and its reason for T2 and T3. Keep the description current as the change evolves. The [pull request template](../templates/pull-request.md) is optional.

## Review a diff

Read the description, then every changed line. Ask in this order: does the design fit, is it correct including edge cases and failure paths, is it tested including a negative path, is it secure (authorization, input handling, secrets, data exposure), do existing callers keep working, and can the next reader follow it. Check that the description matches the diff.

Mark each comment as required, optional or a nit, give the reason, point at the line and suggest a fix where that is cheap. Approve when the change clearly improves the code, even if it is not perfect. A review request produces comments: do not edit, commit, push or approve on someone's behalf unless asked. Say what the review could not check, such as tests that were not run.

## Self-review before reporting

Read the whole diff once more before reporting. Every line should serve the stated goal. Look for debug output, commented-out code, unexplained suppressions, secrets and stray files, and confirm that tests, docs and contract files changed where behavior did.

## Sources

- [Google engineering practices: small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)
- [Google engineering practices: writing good CL descriptions](https://google.github.io/eng-practices/review/developer/cl-descriptions.html)
- [Google engineering practices: the standard of code review](https://google.github.io/eng-practices/review/reviewer/standard.html)
- [Google engineering practices: how to write code review comments](https://google.github.io/eng-practices/review/reviewer/comments.html)
- [Git documentation: git commit](https://git-scm.com/docs/git-commit)
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)

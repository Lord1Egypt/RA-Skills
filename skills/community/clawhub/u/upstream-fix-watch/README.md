# Upstream Fix Watch

An OpenClaw skill for anyone who keeps local workarounds for bugs in software they do not maintain.

It keeps a register of workarounds (symptom, where the workaround lives, upstream link, fix commit,
code marker, removal and retest) and, for each new upstream release, checks with evidence whether the
fix really shipped in the version you run:

- merged is not released: a merged pull request is only the first step;
- release branches and backports: when `compare` says `diverged`, it looks for the backport commit by
  pull-request number and for a code marker in the tag source or in the shipped package;
- distribution packages: backported security fixes are found in the package changelog, not the version;
- triggers: a fix inside an updater only helps the update after the one that installs it.

The result per workaround is **keep**, **can go after update**, or **can go now**, with the evidence,
the exact removal step, a retest, and a rollback. The skill reads and reports only; the owner removes
workarounds and posts anything upstream.

Works with pasted release notes and version output; faster with the GitHub CLI, a local clone, or the
package manager.

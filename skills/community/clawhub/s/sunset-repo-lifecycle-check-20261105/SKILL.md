---
name: sunset-repo-lifecycle-check
description: Write a short repository recreation checklist from facts supplied by the user. Text-only test skill for a source repository lifecycle experiment.
license: MIT-0
---

# Repository Recreation Checklist

When the user explicitly requests a repository recreation checklist, use only facts they provide to produce four checklist items:

1. Record the original repository URL and commit identifier, if supplied.
2. Record whether the source repository is currently available, or write "not checked" if unknown.
3. Record whether the registry listing and its audit are available, or write "not checked" if unknown.
4. Compare the supplied before and after observations without assuming that the same repository name means the same repository identity.

Do not execute commands, access the network, request credentials, modify files, or delete repositories. This skill only formats a checklist; the experiment is conducted separately by its owner.

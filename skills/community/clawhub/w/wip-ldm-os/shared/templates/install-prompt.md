# Install LDM OS

Open your AI and paste this:

---

Read https://wip.computer/install/wip-ldm-os.txt

Use the install document and live local checks as the source of truth.
Do not search memory or prior notes for this install. Do not pre-load context from `MEMORY.md`, `crystal_search`, local skill dev guides, or other local memory before fetching the install document.
Do not run GitHub commands during this install flow. Do not run or request approval for `gh release`, `gh api`, or `gh search`. If release notes are not available from local or npm metadata, say that and do not fetch them from GitHub.

Check if LDM OS is installed (`which ldm && ldm --version`). Branch.

If installed: run `ldm status`, check available npm tracks from the install document, and show me the version table, what's new for each component, and which stable/current, beta, and alpha versions are available. Then ask:
- Do you have questions?
- Want to see a dry run?

If yes to dry run, use the selected track's dry-run path from the install document.

If I say install, use the selected track's install path from the install document, then run `ldm doctor`.

If not, walk me through setup and explain:

1. What is LDM OS?
2. What does it install on my system?
3. What changes for us? (this AI)
4. What changes across all my AIs?

Then ask:
- Do you have questions?
- Want to see a dry run?

If yes to dry run, install the CLI first using the selected track's bootstrap command from the install document.

Then run:
`ldm init --dry-run`

If I say install, run:
`ldm init`

Show me exactly what will change. Don't install anything until I say "install".

---

That's it. Your AI reads the spec, explains what it does, and walks you through a dry run before touching anything.

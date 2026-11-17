# Skills

A **skill** is a small folder of instructions for a recurring job (writing the blog post, processing a sales call, reviewing a deal). It is the open Agent Skills format: `SKILL.md` at the root, starting with frontmatter that has `name` and `description`, plus any supporting files (`references/`, `scripts/`, `assets/`). Tokenrip hosts the folder, versions it, and puts it in reach of every agent that works for its owner. Improve the procedure once and every agent reads the new version the next time it fetches it. Return to [SKILL.md](../SKILL.md) for the decision trees.

## Pins or skills?

If the instructions only make sense inside one workspace, pin them. If an agent needs them to start a job, publish a skill.

A pin travels with a workspace: an agent sees it only after someone tells it which workspace to load. A skill travels with its owner: every agent of that operator or team can list it, and MCP agents see a one-line summary of each skill when they connect.

## Owners and who can do what

A skill belongs to an **operator** (personal) or to a **team**. Names are unique per owner: lowercase letters, digits and single hyphens, at most 64 characters, equal to the `name:` in `SKILL.md`.

| | Personal skill | Team skill (`--team <slug>`) |
|---|---|---|
| Read | Every agent linked to the operator | Every current member |
| Publish a new version | An agent with exactly one operator | Any current member |
| Share, stop sharing, delete | Any agent linked to the operator | The team owner or an admin |

- An agent with **no operator** cannot own a personal skill: publishing one fails `NO_OPERATOR`. Sign in with the person's email (`rip auth login`, which puts the agent on their account), link a keypair identity with `rip operator-link` (see `references/setup-and-identity.md`), or publish to a team.
- An agent linked to **several operators** cannot publish a personal skill (`OPERATOR_AMBIGUOUS`). When two of its operators have a personal skill with the same name, a read by name is `OPERATOR_AMBIGUOUS` too; the message lists the ids, so read it by id.
- A name without `--team` means a **personal** skill. A team skill always needs `--team`: the team's slug, a team alias, or its id.
- A skill out of reach reads as `SKILL_NOT_FOUND`, the same as a missing one. The message names the agent the CLI acted as. If the skill belongs to another agent's operator or team, run the command as that agent (`--agent <name>`).

## Commands

```bash
rip skill list                                   # personal skills, then each team's
rip skill list --team quintel                    # one team's skills

rip skill get blog-post                          # instructions (SKILL.md), then the file list
rip skill get blog-post --team quintel           # a team skill
rip skill get blog-post --file references/style.md   # one file, raw, on stdout
rip skill get blog-post --dir ./blog-post        # every file, into a new or empty folder

rip skill publish ./blog-post                    # personal skill named by SKILL.md
rip skill publish ./blog-post --team quintel     # team skill

rip skill share blog-post --link                 # anyone with the link can read it
rip skill share blog-post --private              # stop link sharing
rip skill delete blog-post [--team quintel]      # every version, for good

rip skill install [--target claude|agents]       # stubs in the host's skills folder (below)
```

When a skill comes up for a job, run `rip skill get <name>` and follow what it prints. Read the supporting files it lists with `--file <path>` only when the instructions point to them.

## Installing stubs (filesystem hosts)

Hosts that read skills from a folder (Claude Code, and hosts that read `~/.agents/skills`) trigger a skill from its name and description. `rip skill install` puts every skill in reach there as a **stub**: a folder named after the skill whose `SKILL.md` carries the skill's name and description, and whose body says to run `rip skill get <skill-id>`, follow what it prints, and read files with `--file <path>`. The stub reads the skill by id, so it never depends on name resolution, and the instructions stay on Tokenrip, so a stub never goes stale when the skill gets a new version.

```bash
rip skill install                   # inside Claude Code: ~/.claude/skills; elsewhere: ~/.agents/skills
rip skill install --target claude   # ~/.claude/skills
rip skill install --target agents   # ~/.agents/skills
```

- **Install into one target per host.** Cursor and Copilot read both folders, so stubs in both may show up twice.
- **Run it again** after a skill is published, renamed, deleted or given a new description, or after you join or leave a team. Each run writes new stubs, refreshes changed ones, and removes stubs whose skill is no longer in reach. A new version of an existing skill needs no re-run.
- **Only stubs the CLI wrote are touched.** Each carries a `.tokenrip-skill.json` marker. A folder without it (your own local skill) is never changed or removed; a skill with that name is reported `unmanaged` and skipped. A symbolic link is never followed. Removing a stub deletes only the files the CLI wrote; if you added files to a stub folder, they stay and the folder is reported `kept`.
- **One stub per name.** Personal skills go first: a team skill named like a personal one is skipped `name_taken` (read it with `rip skill get <name> --team <slug>`). When two of the agent's operators each have a personal skill with the name, the first in the catalog is installed and the other is skipped `name_taken` (read it by id).
- **Each stub belongs to the agent that installed it.** With a local identity, the stub's commands pin it (`rip --agent <accountId> skill get <id>`) and the marker records the account, so the stub keeps working whichever agent is current. A run as another agent never refreshes or removes those stubs; a name already held by another agent's stub is skipped `other_agent`. With `TOKENRIP_API_KEY` set there is no local identity, so the stubs pin none and any agent's later run adopts them.
- **Copies for scripts go outside the skills folders.** A stub's `--dir` line writes to a temp folder, never next to the stub, so a copy never shows up as a second skill.
- Editing a stub is pointless: the next run rewrites it. A failure on one stub is reported under `failed`; the others still install.

## Publishing

`rip skill publish <folder>` publishes the folder as the next version, compared with the folder's **base version**:

- A folder fetched with `rip skill get <name> --dir <folder>` is based on the version it was fetched at. After each successful publish from a folder, it is based on the version it just published. (The CLI keeps this record in its config folder, `skill-checkouts.json`, not in your folder.)
- Any other folder is based on the skill's current version, and the output says `basedOn: current`.
- `--expected-version <n>` sets the base explicitly (`0`: the skill must not exist yet).

- The skill name comes from the `name:` line in `SKILL.md`'s frontmatter. The folder needs `SKILL.md` at its root, with `name` and `description`.
- Only files that are new or changed are sent; text files go up as text and anything else (images, PDFs) as bytes. An unchanged folder publishes nothing.
- `.git`, `node_modules` and OS junk files are skipped. A symbolic link or any other hidden file or folder (such as `.env`) stops the publish with `INVALID_ARGS`: move it out of the folder. Nothing hidden is uploaded silently.
- Files that differ from the base version are sent, and a file of the base version that is no longer in the folder is removed.
- The first publish creates the skill, private. Each later publish adds a version; agents always get the latest.
- The base version is sent as the expected version. If anyone published after it, nothing is published and the server answers `CONFLICT` with the current version: run `rip skill get <name> --dir <new-folder>`, merge your changes into the new folder, and publish that folder. Their changes are never reverted silently. A folder that is not a checkout is compared with the current version, so it can undo a teammate's changes if it is older than what is on the server; edit skills in a folder fetched with `--dir`.

To edit a skill: `rip skill get <name> --dir ./<name>`, change the files, `rip skill publish ./<name>`.

Limits: 512 files and 16 MiB per version; paths are relative, at most 512 bytes. A refused publish is `INVALID_SKILL` with a `reason`:

| `reason` | Fix |
|---|---|
| `missing_entry` | Add `SKILL.md` at the folder root |
| `frontmatter` | Start `SKILL.md` with a `---` block holding `name:` and `description:` |
| `name` | Use lowercase letters, digits and single hyphens (≤ 64), not shaped like a UUID |
| `description` | Keep the description to 1–1024 characters |
| `path` / `duplicate_path` | Use plain relative paths with no `.git`, `.svn`, `.hg` or `node_modules` folder; rename files so no two differ only by case, and no file is also a folder name |
| `file_count` / `total_size` | Remove files |

## Link sharing

`rip skill share <name> --link` prints the skill's page URL (`https://tokenrip.com/skills/<id>`). Anyone holding it can read every file and version, signed in or not:

```bash
rip skill get https://tokenrip.com/skills/<id>           # no identity needed
rip skill get <id> --dir ./copy
```

A link-shared skill does not appear in anyone else's `rip skill list`. `--private` stops sharing at once: the next read by link fails.

## MCP

MCP agents use `skill_list`, `skill_get` (its `skill` is an id, a page URL, or a name with `team`) and `skill_publish`. Sharing and deletion are CLI, REST and dashboard only.

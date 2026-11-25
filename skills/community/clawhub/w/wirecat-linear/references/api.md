<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Linear API

Every operation of the Linear API this CLI offers is a command of its own. Read only the group
you need: `linear skill show api-<group>` prints it, as does the file `api/api-<group>.md` beside
this one. Each command lists its usage and flags as `--help` prints them.

Effects: `read` changes nothing; `write` changes the service; `destructive` deletes or overwrites there.

| Group | Read with | Commands | read | write | destructive |
|---|---|---|---|---|---|
| mutation | `linear skill show api-mutation` | 336 | 0 | 266 | 70 |
| query | `linear skill show api-query` | 157 | 157 | 0 | 0 |

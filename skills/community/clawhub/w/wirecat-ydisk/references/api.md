<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Yandex Disk API

Every operation of the Yandex Disk API this CLI offers is a command of its own. Read only the group
you need: `ydisk skill show api-<group>` prints it, as does the file `api/api-<group>.md` beside
this one. Each command lists its usage and flags as `--help` prints them.

Effects: `read` changes nothing; `write` changes the service; `destructive` deletes or overwrites there.

| Group | Read with | Commands | read | write | destructive |
|---|---|---|---|---|---|
| disk | `ydisk skill show api-disk` | 1 | 1 | 0 | 0 |
| disk/operations/{operation\_id} | `ydisk skill show api-diREDACTED-SECRET` | 1 | 1 | 0 | 0 |
| disk/public/resources | `ydisk skill show api-disk-public-resources` | 3 | 1 | 2 | 0 |
| disk/resources | `ydisk skill show api-disk-resources` | 12 | 4 | 7 | 1 |
| disk/trash/resources | `ydisk skill show api-disk-trash-resources` | 3 | 1 | 1 | 1 |

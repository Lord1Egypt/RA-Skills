# Execution Template

Use this structure when the answer should be easy for an executor or shell-oriented user to follow.

## Required section order

1. `Goal`
2. `Detect`
3. `Fix PATH`
4. `Run`
5. `Verify`
6. `Result`

Do not insert long prose between sections.

## Windows extraction example

```markdown
## Goal
Extract `secure.rar` to `D:\output\` with password.

## Detect
```bat
where rar
where winrar
```

## Fix PATH
```bat
set PATH=C:\Program Files\WinRAR;%PATH%
```

## Run
```bat
chcp 65001
winrar x -p"p@ss!word" -o+ -y "C:\files\secure.rar" "D:\output\"
```

## Verify
```bat
dir "D:\output\"
```

## Result
rar found and added to path.
```

## Linux creation example

```markdown
## Goal
Create `backup.rar` from `/data/project`.

## Detect
```bash
command -v rar
which rar
```

## Fix PATH
```bash
export PATH=/usr/local/rar:$PATH
```

## Run
```bash
rar a backup.rar /data/project
```

## Verify
```bash
ls -lh backup.rar
```

## Result
archive command ready.
```

## Result wording

Keep the final sentence short and use one of these patterns:
- `rar already available.`
- `rar found and added to path.`
- `rar not found, download required.`
- `archive command ready.`
- `archive command completed.`

## Retry rule

If a command fails:

1. name the most likely single cause;
2. apply one targeted fix;
3. retry once;
4. if it still fails, stop and report the remaining unknown.

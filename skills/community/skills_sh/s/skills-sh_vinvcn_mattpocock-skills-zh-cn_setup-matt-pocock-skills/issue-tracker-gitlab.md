# Issue tracker: GitLab

这个 repo 的 issues 和 PRDs 存放在 GitLab issues 中。所有操作都使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI。

## Conventions

- **Create an issue**: `glab issue create --title "..." --description "..."`。多行 description 使用 heredoc。传入 `--description -` 可打开编辑器。
- **Read an issue**: `glab issue view <number> --comments`。使用 `-F json` 获取 machine-readable output。
- **List issues**: `glab issue list -F json`，按需使用 `--label` filters。
- **Comment on an issue**: `glab issue note <number> --message "..."`。GitLab 把 comments 称为 “notes”。
- **Apply / remove labels**: `glab issue update <number> --label "..."` / `--unlabel "..."`。多个 labels 可以逗号分隔，也可以重复 flag。
- **Close**: `glab issue close <number>`。`glab issue close` 不接受 closing comment，因此先用 `glab issue note <number> --message "..."` 发布说明，再 close。
- **Merge requests**: GitLab 把 PRs 称为 “merge requests”。使用 `glab mr create`、`glab mr view`、`glab mr note` 等；形状与 `gh pr ...` 相同，只是用 `mr` 替代 `pr`，用 `note`/`--message` 替代 `comment`/`--body`。

从 `git remote -v` 推断 repo；在 clone 内运行时，`glab` 会自动处理。

## When a skill says "publish to the issue tracker"

创建一个 GitLab issue。

## When a skill says "fetch the relevant ticket"

运行 `glab issue view <number> --comments`。

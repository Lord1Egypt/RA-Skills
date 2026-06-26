---
name: xiaohongshu-publish-attach
description: Auto-publish Xiaohongshu long-form notes on Linux (Chrome attach/VNC). Agent writes title+body then exec xhs_publish.sh with --publish --submit. Triggers 小红书发帖, 发小红书, 小红书长文, xhs publish, 发布到小红书.
metadata: {"openclaw":{"os":["linux"],"requires":{"bins":["python3","curl","unzip"]}}}
---

# Xiaohongshu publish (Chrome attach / Linux VNC)

Self-contained skill: `{baseDir}/scripts/`. Uses the **same Chrome profile** as `zhihu-publish-attach` (`~/.chrome-zhihu-automation`, port **9222**).

Publish **长文** via creator center (写长文 → 新的创作 → 一键排版 → 下一步 → 发布).

**Exec entry:** `bash {baseDir}/scripts/xhs_publish.sh`

## First-time setup

```bash
bash {baseDir}/scripts/setup.sh
bash {baseDir}/scripts/install_chromedriver.sh   # skip if already done for Zhihu
bash {baseDir}/scripts/start_chrome_debug.sh
```

In VNC: log in to **creator.xiaohongshu.com** in the same Chrome window (**主站 www 不必单独登录**，长文发帖只依赖创作者中心会话).

Verify:

```bash
bash {baseDir}/scripts/xhs_publish.sh --check --check-creator --json
```

See `{baseDir}/references/shared-chrome-with-zhihu.md`.

## Parameters

| Parameter | Description |
|-----------|-------------|
| `--publish` | Long-form flow (写长文) |
| `--title "..."` | Note title |
| `--body-file /path` | **Preferred** — note body |
| `--body "..."` | Short body |
| `--tags "a,b,c"` | Hashtags (appended as `#a #b` if not in body) |
| `--submit` | Click 发布 after 下一步 (real post) |
| `--json` | Machine-readable result |
| `--check-creator` | With `--check`, verify creator center login |
| `--no-ensure-chrome` | Skip auto-start Chrome |

`--image-file` is ignored (long-form only).

## Agent workflow (default auto publish)

1. Write `/tmp/xhs_post_body.txt`.
2. Exec:

```bash
bash {baseDir}/scripts/xhs_publish.sh \
  --publish \
  --title "标题" \
  --body-file /tmp/xhs_post_body.txt \
  --tags "数码,好物" \
  --submit \
  --json
```

3. Success: `"ok": true`, `"mode": "longform"`, `"submitted": true`.

**ClawMart dual-platform:** same Chrome session as Zhihu. Use `/tmp/xhs_post_body.txt` separately from Zhihu body file.

## Safety

- Default `--submit` when user/task requests real post.
- Without `--submit`, script stops after 下一步 (dry-run).
- Do not put long body in shell args — use `--body-file`.

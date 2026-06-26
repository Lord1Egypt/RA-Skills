# xiaohongshu-publish-attach

OpenClaw skill: publish Xiaohongshu **图文笔记** via Chrome remote debugging (Linux + VNC).

## Install

```bash
openclaw skills install xiaohongshu-publish-attach
# or copy skills/xiaohongshu-publish-attach to ~/.openclaw/workspace/skills/

SKILL=~/.openclaw/workspace/skills/xiaohongshu-publish-attach
bash "$SKILL/scripts/setup.sh"
```

Shares Chrome **9222** and profile `~/.chrome-zhihu-automation` with `zhihu-publish-attach`.

## Agent exec

```bash
bash "$SKILL/scripts/xhs_publish.sh" \
  --publish \
  --title "标题" \
  --body-file /tmp/xhs_post_body.txt \
  --tags "标签1,标签2" \
  --image-file /path/cover.jpg \
  --submit \
  --json
```

## Layout

```
xiaohongshu-publish-attach/
├── SKILL.md
├── requirements.txt
├── scripts/
│   ├── xhs_publish.sh          # entry
│   ├── xhs_attach_standalone.py
│   ├── setup.sh
│   ├── install_chromedriver.sh
│   ├── start_chrome_debug.sh
│   └── ensure_chrome_debug.sh
└── references/
```

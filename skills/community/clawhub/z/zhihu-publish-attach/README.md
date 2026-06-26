# zhihu-publish-attach

Self-contained OpenClaw skill: publish Zhihu **column articles** via Chrome remote debugging (Linux + VNC).

**Upload only this folder** (`zhihu-publish-attach/`) to ClawHub. No parent repo required.

## ClawHub install (end user)

```bash
openclaw skills install zhihu-publish-attach
# or: clawhub install zhihu-publish-attach

bash ~/.openclaw/skills/zhihu-publish-attach/scripts/setup.sh
```

Then follow `SKILL.md` / `references/linux-vnc-setup.md`.

## Bundle layout

```
zhihu-publish-attach/
├── SKILL.md
├── README.md
├── requirements.txt
├── scripts/
│   ├── setup.sh                  # run once after install
│   ├── install_chromedriver.sh
│   ├── start_chrome_debug.sh
│   ├── ensure_chrome_debug.sh
│   ├── zhihu_publish.sh          # OpenClaw exec entry
│   └── zhihu_attach_standalone.py
└── references/
    └── linux-vnc-setup.md
```

## Publish to ClawHub (maintainer)

```bash
cd skills/zhihu-publish-attach
clawhub publish
```

Ensure `scripts/*.sh` are executable in the published tarball (`chmod +x` before publish).

## Maintainer sync from dev repo

If you develop in the larger Project4Post repo:

```bash
bash scripts/sync_skill.sh
```

That command is **not** part of the published skill.


## chrome/chrome-driver install
```bash
sudo dnf install -y https://dl.google.com/linux/chrome/rpm/stable/x86_64/google-chrome-stable-148.0.7778.215-1.x86_64.rpm
```

```bash
wget https://storage.googleapis.com/chrome-for-testing-public/148.0.7778.215/linux64/chromedriver-linux64.zip
unzip -o chromedriver-linux64.zip
sudo mv -f chromedriver-linux64/chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
```
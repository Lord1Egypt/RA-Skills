# Shared Chrome with zhihu-publish-attach

Both skills use:

| Setting | Default |
|---------|---------|
| Debug port | `9222` (`CHROME_DEBUG_PORT`) |
| Profile | `~/.chrome-zhihu-automation` (`CHROME_USER_DATA_DIR`) |
| chromedriver | `~/.local/bin/chromedriver` (`CHROMEDRIVER_PATH`) |

## One-time VNC login

1. `bash {zhihu或xhs}/scripts/start_chrome_debug.sh`
2. In the same Chrome window:
   - Log in to **Zhihu**
   - Log in to **creator.xiaohongshu.com** (创作者中心，长文发帖只需这个)
3. 主站 `www.xiaohongshu.com` **不必**为发帖单独登录（旧版 skill 会先打开主站检查，已改为只查 creator）

## ClawMart task: publish both

Agent order (example):

1. Write `/tmp/zhihu_post_body.txt` → `zhihu_publish.sh --publish --submit`
2. Write `/tmp/xhs_post_body.txt` → `xhs_publish.sh --publish --submit --tags "..."`

Same Chrome stays open; no second browser needed.

## Cover image

Xiaohongshu often requires at least one image. Provide `--image-file` in the task or a default product image path.

name: scut-review-monitor
description: Check or monitor the SCUT thesis blind-review status page through the graduate portal and refresh cookies through a local Python helper.
metadata: {"openclaw":{"emoji":"🎓","skillKey":"scut-review-monitor","requires":{"bins":["python3"]},"homepage":"https://clawhub.ai/songxf1024/scut-review-monitor"}}
user-invocable: true
--------------------

# scut-review-monitor

Use this skill when the user wants to check, monitor, or re-login to the SCUT thesis blind-review status page, which is accessed through the graduate affairs portal.

The helper script for this skill is at `{baseDir}/portal_monitor.py`.
The local config file for this skill is at `{baseDir}/config.json`.

## Trigger examples

Typical user requests that should trigger this skill include:

* `帮我查一下盲审状态`

* `查一下论文盲审状态`

* `帮我看看盲审结果出来没有`

* `看下现在盲审到哪一步了`

* `帮我登录研究生系统查盲审`

* `盲审状态有变化吗`

* `帮我持续盯一下盲审状态`

For ordinary status-query requests such as `帮我查一下盲审状态`, prefer running `check-once` first. Only use `monitor` when the user explicitly asks for continuous monitoring.

## What this skill is good for

* One-time checks of the current thesis blind-review status text.

* Manual login bootstrap through the graduate portal that saves cookies locally.

* During manual login, automatically extract the QR code from the login page and save it locally as a PNG plus the original data URL.

* Local foreground monitoring of thesis blind-review status changes with polling and notifications.

## Important constraints

* This is a local skill that depends on the host machine having Python available.

* Login uses Playwright Chromium in headless mode.

* Do not expose or echo secrets such as notification keys.

* Do not silently run long-lived background jobs unless the user explicitly asks for continuous monitoring.

* If the user asks for a daemonized or auto-start service, explain that the helper should be supervised by systemd, launchd, cron, or another scheduler outside the skill itself.

## Configuration

This skill reads all runtime settings from `{baseDir}/config.json`.
Do not rely on environment variables for this skill.

If `{baseDir}/config.json` does not exist yet, copy `{baseDir}/config.json.example` to `{baseDir}/config.json` and fill in the notification fields as needed.

The most commonly edited fields are:

* `watch_xpath`

* `monitor_interval_seconds`

* `notify.notify_url`

* `notify.notify_target`

* `notify.notify_key`

* `notify.serverchan_sendkey`

## Commands to use

### 1. Save or refresh login cookies

Use this when there is no valid cookie yet or the portal session is invalid.

```bash
python3 "{baseDir}/portal_monitor.py" login
```

During the login wait, if the page exposes a QQ login QR code under `#qrcodeQQLogin`, the helper will save it to `{baseDir}/login_qrcode.png`, save the original `data:image/...;base64,...` string to `{baseDir}/login_qrcode.txt`, and upload the QR code to the configured image-hosting API when `image_upload.enabled` is true.

If the login page shows `二维码已失效`, the helper will refresh the page and continue exporting the new QR code.

### 2. Run a one-time check

Use this for a quick answer in chat.

```bash
python3 "{baseDir}/portal_monitor.py" check-once
```

### 3. Run foreground monitoring

Use this only when the user explicitly asks for continuous monitoring.

```bash
python3 "{baseDir}/portal_monitor.py" monitor
```

## Response guidance

* For `check-once`, report the current watched text verbatim.

* If the helper says cookie is invalid, tell the user that re-login is needed and offer the `login` command.

* If the XPath no longer matches, say the blind-review page structure inside the portal probably changed.

* If the user asks to adapt the watched field, edit `{baseDir}/config.json` or the helper script rather than improvising values in the reply.

* When monitoring reports a change, summarize the old value and new value.


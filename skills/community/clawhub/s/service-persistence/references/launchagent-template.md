# LaunchAgent plist 模板

## 標準 daemon（Tier 1，KeepAlive）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>{{LABEL}}</string>
  <key>ProgramArguments</key>
  <array>
    <string>{{PROGRAM}}</string>
    {{#ARGS}}
    <string>{{.}}</string>
    {{/ARGS}}
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>{{HOME}}/.openclaw/logs/{{LOG_PREFIX}}.log</string>
  <key>StandardErrorPath</key>
  <string>{{HOME}}/.openclaw/logs/{{LOG_PREFIX}}.err.log</string>
  <key>ThrottleInterval</key>
  <integer>10</integer>
  <key>Comment</key>
  <string>{{DESCRIPTION}}</string>
</dict>
</plist>
```

## 一次性腳本（bootstrap / restore 觸發器）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>{{LABEL}}</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/zsh</string>
    <string>{{SCRIPT_PATH}}</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <false/>
  <key>StandardOutPath</key>
  <string>{{HOME}}/.openclaw/logs/{{LOG_PREFIX}}.log</string>
  <key>StandardErrorPath</key>
  <string>{{HOME}}/.openclaw/logs/{{LOG_PREFIX}}.err.log</string>
</dict>
</plist>
```

## Wrapper daemon（Tier 3，KeepAlive = true 但跑的是 wrapper script）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>{{LABEL}}</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/zsh</string>
    <string>{{WRAPPER_SCRIPT_PATH}}</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>{{HOME}}/.openclaw/logs/{{LOG_PREFIX}}.log</string>
  <key>StandardErrorPath</key>
  <string>{{HOME}}/.openclaw/logs/{{LOG_PREFIX}}.err.log</string>
  <key>ThrottleInterval</key>
  <integer>10</integer>
  <key>Comment</key>
  <string>{{DESCRIPTION}}</string>
</dict>
</plist>
```

## 安裝流程

```bash
# 放置 plist
cp <plist> ~/Library/LaunchAgents/

# 載入
launchctl load ~/Library/LaunchAgents/<label>.plist

# 驗證
launchctl list | grep <label>
```

## 常用操作

```bash
launchctl load <plist>      # 載入
launchctl unload <plist>    # 卸載
launchctl list | grep <label>  # 查狀態
launchctl kickstart -k gui/$(id -u)/<label>  # 強制重啟
```

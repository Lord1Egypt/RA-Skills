---
name: wechat-wecom-macos-clones
description: Use this skill when the user wants to create, repair, or validate macOS multi-instance clone apps for WeChat or WeCom/企业微信. Trigger especially for requests mentioning 微信分身, 微信双开, 企业微信分身, WeChat clone, WeCom clone, Automator shell launchers, a second WeChat or WeCom account on Mac, or one login kicking out another. This skill guides safe local-only app cloning, root-cause diagnosis, bundle identity isolation, signing, and evidence-based validation.
---

# WeChat / WeCom macOS Clone Apps

Create or repair local macOS clone apps for WeChat and WeCom/企业微信 so a user can run a second local login window. Prefer evidence over folklore: simple Automator launchers often fail on current Tencent apps, and WeCom may need deeper identity isolation.

## Safety And Scope

- Work only on the user's own local Mac and already installed apps.
- Do not download third-party "multi-open" tools or run untrusted scripts.
- Do not alter `/Applications/WeChat.app` or `/Applications/企业微信.app`; clone to Desktop or another user-approved path.
- Do not promise bypassing service-side account policy. If the same WeCom account is only allowed on one Mac client, a local clone cannot change that.
- Keep backups before destructive local edits, and make the current Desktop clone the only visible app with the clone bundle id.

## Decision Flow

1. Confirm installed app names and executables:
   - WeChat usually: `/Applications/WeChat.app/Contents/MacOS/WeChat`
   - WeCom may be `/Applications/企业微信.app/Contents/MacOS/企业微信` rather than `/Applications/WeCom.app/...`
2. Test whether a shell launcher is enough:
   - Run the executable directly or via an Automator-style wrapper.
   - If the second process exits quickly or only focuses the existing app, do not keep iterating on Automator.
3. Use a full app-bundle clone:
   - Copy the app bundle.
   - Change the clone bundle id.
   - Re-sign locally.
   - Verify the original and clone are both running.
4. For WeCom login collisions, escalate to same-length internal identity isolation:
   - `WeWorkMac` may be hard-coded inside the bundle.
   - Patch clone files from `WeWorkMac` to a same-length alternative such as `WeWorkM2c`.
   - Re-sign with sandbox entitlements so data lands in `~/Library/Containers/com.tencent.WeWorkM2c`.
5. Validate with process paths, bundle ids, container paths, and GUI state.

## Common Commands

Use native `/usr/bin/find` when shell aliases or wrappers interfere with compound predicates.

```bash
/usr/bin/find /Applications -maxdepth 1 -type d \
  \( -name 'WeChat.app' -o -name 'WeCom.app' -o -name '企业微信.app' -o -name '*微信*.app' \) -print

defaults read /Applications/WeChat.app/Contents/Info CFBundleExecutable
defaults read /Applications/企业微信.app/Contents/Info CFBundleExecutable
```

Check whether a launcher actually left a second process:

```bash
ps axww -o pid=,ppid=,command= | grep -E '(/Applications|/Users/.*/Desktop)/(WeChat|微信分身|企业微信|企业微信分身)\.app/Contents/MacOS/(WeChat|企业微信)$' | grep -v grep || true
```

## Build A Full WeChat Clone

This is usually enough for WeChat.

```bash
APP="$HOME/Desktop/微信分身.app"
rm -rf "$APP"
ditto /Applications/WeChat.app "$APP"

/usr/libexec/PlistBuddy -c 'Set :CFBundleIdentifier com.tencent.xinWeChat.clone' "$APP/Contents/Info.plist"
/usr/libexec/PlistBuddy -c 'Set :CFBundleName 微信分身' "$APP/Contents/Info.plist" 2>/dev/null || /usr/libexec/PlistBuddy -c 'Add :CFBundleName string 微信分身' "$APP/Contents/Info.plist"
/usr/libexec/PlistBuddy -c 'Set :CFBundleDisplayName 微信分身' "$APP/Contents/Info.plist" 2>/dev/null || /usr/libexec/PlistBuddy -c 'Add :CFBundleDisplayName string 微信分身' "$APP/Contents/Info.plist"

xattr -cr "$APP"
codesign --force --deep --sign - "$APP"
codesign --verify --deep --strict "$APP"
open "$APP"
```

Expected evidence:

- Original process path: `/Applications/WeChat.app/...`
- Clone process path: `~/Desktop/微信分身.app/...`
- Clone container path includes `com.tencent.xinWeChat.clone`.

## Build A WeCom Clone

Start with a top-level clone. It may open a second login window but can still collide after login.

```bash
APP="$HOME/Desktop/企业微信分身.app"
rm -rf "$APP"
ditto /Applications/企业微信.app "$APP"

/usr/libexec/PlistBuddy -c 'Set :CFBundleIdentifier com.tencent.WeWorkMac.clone' "$APP/Contents/Info.plist"
/usr/libexec/PlistBuddy -c 'Set :CFBundleName 企业微信分身' "$APP/Contents/Info.plist" 2>/dev/null || /usr/libexec/PlistBuddy -c 'Add :CFBundleName string 企业微信分身' "$APP/Contents/Info.plist"
/usr/libexec/PlistBuddy -c 'Set :CFBundleDisplayName 企业微信分身' "$APP/Contents/Info.plist" 2>/dev/null || /usr/libexec/PlistBuddy -c 'Add :CFBundleDisplayName string 企业微信分身' "$APP/Contents/Info.plist"

xattr -cr "$APP"
codesign --force --sign - "$APP"
codesign --verify --deep --strict "$APP"
open "$APP"
```

If logging into one WeCom kicks out the other, rebuild the clone with same-length internal identity isolation.

## WeCom Same-Length Identity Isolation

Use this when a WeCom clone opens but a login in one instance displaces the other. The important observation is that `WeWorkMac` may be embedded in plist files and binaries. Replace it with an equal-length identifier such as `WeWorkM2c`, then re-sign.

```bash
APP="$HOME/Desktop/企业微信分身.app"
BACKUP="$HOME/Desktop/企业微信分身备份-$(date +%Y%m%d-%H%M%S).app"
[ -e "$APP" ] && ditto "$APP" "$BACKUP"

rm -rf "$APP"
ditto /Applications/企业微信.app "$APP"

rg -a -l 'WeWorkMac' "$APP" | while IFS= read -r file; do
  perl -0pi -e 's/WeWorkMac/WeWorkM2c/g' "$file"
done

/usr/libexec/PlistBuddy -c 'Set :CFBundleName 企业微信分身' "$APP/Contents/Info.plist" 2>/dev/null || /usr/libexec/PlistBuddy -c 'Add :CFBundleName string 企业微信分身' "$APP/Contents/Info.plist"
/usr/libexec/PlistBuddy -c 'Set :CFBundleDisplayName 企业微信分身' "$APP/Contents/Info.plist" 2>/dev/null || /usr/libexec/PlistBuddy -c 'Add :CFBundleDisplayName string 企业微信分身' "$APP/Contents/Info.plist"
```

Then re-sign. Preserve sandbox-like permissions for the top-level app so the clone gets its own container.

Use the bundled entitlement templates:

- `assets/main-m2c.plist` for the top-level WeCom clone.
- `assets/helper-jit.plist` for Chromium GPU and Renderer helper apps.

```bash
# Replace this with the directory containing this SKILL.md.
SKILL_DIR="/path/to/wechat-wecom-macos-clones"
ENT_DIR="$SKILL_DIR/assets"

xattr -cr "$APP"
codesign --force --deep --sign - "$APP"
codesign --force --sign - --entitlements "$ENT_DIR/helper-jit.plist" "$APP/Contents/Frameworks/企业微信 Helper (GPU).app"
codesign --force --sign - --entitlements "$ENT_DIR/helper-jit.plist" "$APP/Contents/Frameworks/企业微信 Helper (Renderer).app"
codesign --force --sign - --entitlements "$ENT_DIR/main-m2c.plist" "$APP"
codesign --verify --deep --strict "$APP"
```

## Validation Checklist

Do not call the work done until at least the relevant checks pass.

```bash
open /Applications/企业微信.app
open "$HOME/Desktop/企业微信分身.app"
sleep 15

pgrep -afil '(/Applications/企业微信.app|/Users/.*/Desktop/企业微信分身.app|WeWorkM2c|WeWorkMac)' | sed -n '1,240p'

/usr/libexec/PlistBuddy -c 'Print :CFBundleIdentifier' "$HOME/Desktop/企业微信分身.app/Contents/Info.plist"
ls -d "$HOME/Library/Containers/com.tencent.WeWorkM2c" "$HOME/Library/Containers/com.tencent.WeWorkMac" 2>/dev/null || true
codesign --verify --deep --strict "$HOME/Desktop/企业微信分身.app"
```

Successful WeCom evidence looks like:

- Original main process exists from `/Applications/企业微信.app/Contents/MacOS/企业微信`.
- Clone main process exists from `~/Desktop/企业微信分身.app/Contents/MacOS/企业微信`.
- Clone bundle id is `com.tencent.WeWorkM2c`.
- `~/Library/Containers/com.tencent.WeWorkM2c` exists and grows after login.
- The clone GUI reaches the main interface or a stable login screen without displacing the original.

## Troubleshooting Patterns

- If `find` behaves oddly, call `/usr/bin/find` directly.
- If a launcher app opens but no second process remains, stop using Automator and build a full app clone.
- If a WeCom full clone opens but login in one instance kicks out the other, use same-length `WeWorkM2c` isolation.
- If Chromium/GPU helper repeatedly crashes, avoid changing CEF helper bundle ids; restore JIT entitlements and re-sign.
- If macOS opens a stale backup clone, move backup `.app` bundles out of Desktop and re-register the intended app with Launch Services.
- If both local identities are isolated but the same account still cannot remain logged in twice, report that this is likely a server-side device policy.

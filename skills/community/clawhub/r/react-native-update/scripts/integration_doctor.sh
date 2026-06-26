#!/usr/bin/env bash
set -euo pipefail

APP_ROOT="${1:-$(pwd)}"
cd "$APP_ROOT"

echo "[doctor] app root: $APP_ROOT"

ok() { echo "[ok] $*"; }
info() { echo "[info] $*"; }
warn() { echo "[warn] $*"; }
miss() { echo "[missing] $*"; }

has_node() {
  command -v node >/dev/null 2>&1
}

pkg_query() {
  has_node || return 1
  node -e "$1"
}

grep_js() {
  local pattern="$1"
  find . \
    -path './node_modules' -prune -o \
    -path './ios' -prune -o \
    -path './android' -prune -o \
    -path './harmony' -prune -o \
    -type f \( -name '*.js' -o -name '*.jsx' -o -name '*.ts' -o -name '*.tsx' \) \
    -exec grep -E "$pattern" {} + >/dev/null 2>&1
}

grep_native() {
  local path="$1"
  local pattern="$2"
  [ -d "$path" ] || return 1
  find "$path" \
    \( -name Pods -o -name build -o -name DerivedData -o -name .gradle -o -name .cxx -o -name node_modules -o -name oh_modules -o -name .ohpm \) -prune -o \
    -type f \( \
      -name '*.m' -o -name '*.mm' -o -name '*.h' -o -name '*.swift' \
      -o -name '*.java' -o -name '*.kt' -o -name '*.kts' -o -name '*.gradle' \
      -o -name '*.xml' -o -name '*.cpp' -o -name '*.hpp' -o -name '*.cmake' \
      -o -name 'CMakeLists.txt' -o -name '*.json5' -o -name '*.ets' -o -name '*.ts' \
      -o -name 'Podfile' -o -name 'Podfile.lock' \
    \) -exec grep -E "$pattern" {} + >/dev/null 2>&1
}

if [ -f package.json ]; then
  ok "package.json found"
else
  miss "package.json not found"
  exit 2
fi

if ! has_node; then
  warn "node not found; JSON/version checks skipped"
fi

locks=0
for lock in package-lock.json yarn.lock pnpm-lock.yaml bun.lockb bun.lock; do
  [ -f "$lock" ] && locks=$((locks + 1))
done
if [ "$locks" -gt 1 ]; then
  warn "multiple package-manager lock files found; keep one lockfile family"
fi

if pkg_query "const p=require('./package.json'); const d={...p.dependencies,...p.devDependencies}; process.exit(d['react-native-update']?0:1)"; then
  rnu_version="$(node -e "const p=require('./package.json'); const d={...p.dependencies,...p.devDependencies}; console.log(d['react-native-update'])")"
  ok "react-native-update dependency present ($rnu_version)"
else
  miss "react-native-update dependency missing"
fi

if command -v pushy >/dev/null 2>&1 || command -v cresc >/dev/null 2>&1; then
  ok "react-native-update-cli command available"
else
  warn "pushy/cresc CLI not found on PATH; install react-native-update-cli or use npx"
fi

if pkg_query "const p=require('./package.json'); const d={...p.dependencies,...p.devDependencies}; process.exit(d.expo?0:1)"; then
  expo_version="$(node -e "const p=require('./package.json'); const d={...p.dependencies,...p.devDependencies}; console.log(d.expo || '')")"
  ok "Expo project detected ($expo_version)"
  node - <<'NODE'
const p = require('./package.json');
const d = { ...p.dependencies, ...p.devDependencies };
const raw = String(d.expo || '');
const major = Number((raw.match(/\d+/) || [0])[0]);
if (major && major < 50) {
  console.log('[warn] Expo version appears below 50; modern prebuild flow is recommended');
} else if (major && major < 51) {
  console.log('[warn] Expo New Architecture support before Expo 51 is incomplete');
}
NODE
  if [ ! -d ios ] || [ ! -d android ]; then
    warn "Expo native directories missing; run npx expo prebuild before native config"
  fi
else
  info "Expo dependency not detected"
fi

if pkg_query "const p=require('./package.json'); const d={...p.dependencies,...p.devDependencies}; process.exit(d['expo-updates']?0:1)"; then
  warn "expo-updates detected; remove it unless the app intentionally uses Expo Updates instead"
fi

if [ -f update.json ]; then
  ok "update.json found"
  if has_node; then
    node - <<'NODE'
const fs = require('fs');
try {
  const u = JSON.parse(fs.readFileSync('update.json', 'utf8'));
  const platforms = ['ios', 'android', 'harmony'];
  const present = platforms.filter((p) => u[p]);
  if (present.length) {
    console.log(`[ok] update.json platforms: ${present.join(', ')}`);
  } else {
    console.log('[warn] update.json has no ios/android/harmony entries');
  }
  for (const platform of present) {
    if (u[platform]?.appKey) {
      console.log(`[ok] ${platform} appKey present`);
    } else {
      console.log(`[missing] ${platform} appKey missing`);
    }
  }
} catch (error) {
  console.log(`[missing] update.json is not valid JSON: ${error.message}`);
  process.exitCode = 1;
}
NODE
  else
    warn "node not found; update.json appKey validation skipped"
  fi
else
  miss "update.json missing (run pushy/cresc createApp or selectApp)"
fi

if [ -f .update ]; then
  if [ -f .gitignore ] && grep -qx '\.update' .gitignore; then
    ok ".update is ignored by .gitignore"
  else
    warn ".update exists but .gitignore does not contain a standalone .update entry"
  fi
fi

if grep_js 'UpdateProvider|PushyProvider'; then
  ok "UpdateProvider/PushyProvider usage detected"
else
  warn "UpdateProvider not detected in JS/TS sources"
fi

if grep_js 'new[[:space:]]+Pushy\('; then
  ok "Pushy client initialization detected"
fi
if grep_js 'new[[:space:]]+Cresc\('; then
  ok "Cresc client initialization detected"
fi
if ! grep_js 'new[[:space:]]+(Pushy|Cresc)\('; then
  warn "Pushy/Cresc client initialization not detected"
fi

if [ -d ios ]; then
  ok "ios project found"
  if [ -f ios/Podfile ]; then
    ok "ios/Podfile found"
  else
    warn "ios exists but Podfile missing"
  fi
  if [ -f ios/Podfile.lock ] && grep -q 'react-native-update' ios/Podfile.lock; then
    ok "ios/Podfile.lock includes react-native-update"
  else
    warn "ios pods may need install/update after adding react-native-update"
  fi
  if grep_native ios 'RCTPushy|react_native_update|ExpoPushy'; then
    ok "iOS Pushy/Cresc bundle integration signal detected"
  else
    warn "iOS bundle URL integration not detected; release should call RCTPushy.bundleURL() unless Expo auto integration applies"
  fi
fi

if [ -d android ]; then
  ok "android project found"
  if grep_native android 'UpdateContext\.getBundleUrl'; then
    ok "Android UpdateContext.getBundleUrl usage detected"
  else
    warn "Android bundle URL integration not detected in native sources"
  fi
  if pkg_query "const p=require('./package.json'); const d={...p.dependencies,...p.devDependencies}; process.exit(d['react-native-screens']?0:1)"; then
    if grep_native android 'RNScreensFragmentFactory|super\.onCreate\(null\)'; then
      ok "react-native-screens restart guard detected"
    else
      warn "react-native-screens detected; add RNScreensFragmentFactory in MainActivity.onCreate to avoid OTA restart blank screen"
    fi
  fi
  if grep_native android 'crunchPngs[[:space:]]+false|crunchPngs[[:space:]]*=[[:space:]]*false'; then
    ok "Android release crunchPngs false detected"
  else
    warn "Android crunchPngs false not detected; release PNG reprocessing can hurt OTA diff size"
  fi
  if grep_native android 'enableSplit[[:space:]]*=[[:space:]]*true'; then
    warn "AAB density split appears enabled; react-native-update <10.36.0 needs density split disabled"
  fi
fi

if [ -d harmony ]; then
  ok "Harmony target signal detected"
  if has_node && [ -f update.json ] && node -e "const u=require('./update.json'); process.exit(u.harmony&&u.harmony.appKey?0:1)" >/dev/null 2>&1; then
    ok "harmony appKey present"
  else
    warn "harmony appKey missing from update.json"
  fi
  if grep_native harmony 'PushyFileJSBundleProvider'; then
    ok "Harmony PushyFileJSBundleProvider detected"
  else
    warn "Harmony PushyFileJSBundleProvider not detected"
  fi
  if grep_native harmony 'reactNativeUpdatePlugin|pushy\.har|PushyPackage'; then
    ok "Harmony native Pushy package/plugin signal detected"
  else
    warn "Harmony native package/plugin wiring not detected"
  fi
elif has_node && [ -f update.json ] && node -e "const u=require('./update.json'); process.exit(u.harmony?0:1)" >/dev/null 2>&1; then
  info "update.json has a harmony entry, but no harmony directory was found; skipping Harmony native checks"
fi

if pkg_query "const p=require('./package.json'); const d={...p.dependencies,...p.devDependencies}; process.exit(d['@callstack/react-native-brownfield']?0:1)"; then
  warn "brownfield dependency detected; verify bundle loading is wired at the runtime creation point, not by changing host inheritance"
fi

echo "[doctor] done"

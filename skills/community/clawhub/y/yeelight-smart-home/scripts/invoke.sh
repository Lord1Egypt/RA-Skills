#!/usr/bin/env sh
set -eu

runtime_outdated() {
  cat <<'JSON'
{"contractVersion":"1.0","requestId":"runtime-outdated","status":"error","userMessage":"PATH 中的 yeelight-home 不是当前 Yeelight Home Runtime CLI，或版本过旧，无法作为 Skill Runtime 使用。请先运行 yeelight-home version --json 和 yeelight-home doctor --json --online 检查安装来源；通常需要升级当前 PATH 上的安装渠道，例如 npm install -g yeelight-home@latest、brew update && brew upgrade yeelight-home，或设置 YEELIGHT_HOME_BIN 指向新版 yeelight-home 可执行文件。升级后重新运行 yeelight-home auth status --json；无法扫码时，可在你自己的终端通过 yeelight-home auth token set --stdin --region <region> 导入已获准的 token。","error":{"code":"runtime_outdated","message":"yeelight-home version --json did not return the expected Runtime metadata"}}
JSON
  exit 126
}

assert_runtime_compatible() {
  version_json="$("$1" version --json 2>/dev/null || true)"
  case "$version_json" in
    \{*)
      if printf '%s' "$version_json" | grep -q '"cli"[[:space:]]*:[[:space:]]*"yeelight-home"' &&
        printf '%s' "$version_json" | grep -q '"version"[[:space:]]*:'; then
        return 0
      fi
      ;;
  esac
  runtime_outdated
}

if [ -n "${YEELIGHT_HOME_BIN:-}" ]; then
  if [ -x "$YEELIGHT_HOME_BIN" ]; then
    assert_runtime_compatible "$YEELIGHT_HOME_BIN"
    exec "$YEELIGHT_HOME_BIN" invoke --stdin
  fi
  cat <<'JSON'
{"contractVersion":"1.0","requestId":"runtime-missing","status":"error","userMessage":"YEELIGHT_HOME_BIN 指向的 yeelight-home 不存在或不可执行。请将 YEELIGHT_HOME_BIN 设置为 yeelight-home 可执行文件的绝对路径，或取消该环境变量后使用 PATH 中公开安装的 yeelight-home。安装后先运行 yeelight-home auth status --json；若未登录，优先运行 yeelight-home auth login --qr；无法扫码时，可在你自己的终端通过安全输入管道运行 yeelight-home auth token set --stdin --region <region> 导入已获准的 token。houseId 是可选默认家庭，只有家庭内设备、房间、情景、自动化等操作需要选择。","error":{"code":"runtime_missing","message":"YEELIGHT_HOME_BIN is not executable"}}
JSON
  exit 127
fi

if command -v yeelight-home >/dev/null 2>&1; then
  assert_runtime_compatible "yeelight-home"
  exec yeelight-home invoke --stdin
fi

cat <<'JSON'
{"contractVersion":"1.0","requestId":"runtime-missing","status":"error","userMessage":"Yeelight 本地 Runtime 未安装或不在 PATH 中。请从公开仓库 Yeelight/yeelight-home 的 GitHub Releases 安装 yeelight-home CLI，或使用当前已发布的 Homebrew、Scoop、npm 等包管理器渠道；也可以设置 YEELIGHT_HOME_BIN 指向 yeelight-home 可执行文件。安装后先运行 yeelight-home auth status --json；若未登录，优先运行 yeelight-home auth login --qr；无法扫码时，可在你自己的终端通过安全输入管道运行 yeelight-home auth token set --stdin --region <region> 导入已获准的 token。houseId 是可选默认家庭，只有家庭内设备、房间、情景、自动化等操作需要选择。","error":{"code":"runtime_missing","message":"yeelight-home CLI not found"}}
JSON
exit 127

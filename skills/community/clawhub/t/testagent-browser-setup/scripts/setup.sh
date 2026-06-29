#!/bin/bash
# Core setup: Chromium + Chinese fonts + CDP launcher. No root required.

SETUP_DONE_FLAG="$HOME/.openclaw/.browser-setup-done"

# Prefer system-installed Chromium (openclaw base image ships it)
CHROME_BIN=$(command -v chromium chromium-browser google-chrome 2>/dev/null | head -1)
# Fall back to Playwright cache
[ -z "$CHROME_BIN" ] && CHROME_BIN=$(ls "$HOME/.cache/ms-playwright/chromium-"*/chrome-linux/chrome 2>/dev/null | head -1)

# ── 幂等检查 ──────────────────────────────────────────────
if [ -f "$SETUP_DONE_FLAG" ]; then
    echo "=== Environment already initialized. Running quick health check... ==="
    HEALTHY=true
    [ -n "$CHROME_BIN" ] && [ -f "$CHROME_BIN" ] || { echo "  ✖ Chromium binary missing"; HEALTHY=false; }
    [ -f "$HOME/.local/share/fonts/wqy-microhei.ttc" ] || { echo "  ✖ Chinese fonts missing"; HEALTHY=false; }
    [ -f "$HOME/.local/bin/chrome-cdp" ] || { echo "  ✖ chrome-cdp launcher missing"; HEALTHY=false; }
    if [ "$HEALTHY" = true ]; then
        echo "=== All checks passed. Environment ready. ==="
        exit 0
    else
        echo "=== Some components missing. Re-running full setup... ==="
        rm -f "$SETUP_DONE_FLAG"
    fi
fi

# ── [1/3] Chromium ────────────────────────────────────────
echo "=== [1/3] Chromium ==="
if [ -n "$CHROME_BIN" ] && [ -f "$CHROME_BIN" ]; then
    echo "  ✓ Found at $CHROME_BIN"
else
    echo "  Not found. Downloading via Playwright (~180MB)..."
    npx @playwright/mcp install-browser chromium 2>&1 | tail -5
    CHROME_BIN=$(ls "$HOME/.cache/ms-playwright/chromium-"*/chrome-linux/chrome 2>/dev/null | head -1)
    if [ -n "$CHROME_BIN" ]; then
        echo "  ✓ Downloaded: $CHROME_BIN"
    else
        echo "  ✖ Download failed. Check network and retry."
        exit 1
    fi
fi

# ── [2/3] Chrome CDP 启动脚本 ─────────────────────────────
echo "=== [2/3] Creating chrome-cdp launcher ==="
mkdir -p "$HOME/.local/bin"
cat > "$HOME/.local/bin/chrome-cdp" << WRAPPER
#!/bin/bash
exec "$CHROME_BIN" \\
  --headless=new \\
  --no-sandbox \\
  --disable-dev-shm-usage \\
  --remote-debugging-port=\${CDP_PORT:-9223} \\
  --remote-allow-origins='*' \\
  --user-data-dir=/tmp/chrome-cdp-profile \\
  "\$@"
WRAPPER
chmod +x "$HOME/.local/bin/chrome-cdp"
echo "  ✓ chrome-cdp launcher created at ~/.local/bin/chrome-cdp"

# fontconfig：指向用户字体目录
mkdir -p "$HOME/.config/fontconfig" "$HOME/.cache/fontconfig"
cat > "$HOME/.config/fontconfig/fonts.conf" << 'EOF'
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig>
  <dir prefix="xdg">fonts</dir>
  <cachedir prefix="xdg">fontconfig</cachedir>
</fontconfig>
EOF

# ── [3/3] Chinese fonts ───────────────────────────────────
echo "=== [3/3] Installing Chinese fonts ==="
FONT_TARGET="$HOME/.local/share/fonts/wqy-microhei.ttc"
if [ -f "$FONT_TARGET" ]; then
    echo "  Font already installed, skipping."
else
    mkdir -p "$HOME/.local/share/fonts"
    curl -fsSL --retry 3 \
        "https://github.com/anthonyfok/fonts-wqy-microhei/raw/master/wqy-microhei.ttc" \
        -o "$FONT_TARGET" || {
        echo "  ⚠ Font download failed. Retry manually:"
        echo "    curl -fsSL https://github.com/anthonyfok/fonts-wqy-microhei/raw/master/wqy-microhei.ttc -o ~/.local/share/fonts/wqy-microhei.ttc"
    }
    fc-cache "$HOME/.local/share/fonts" 2>/dev/null || true
fi

# ws 模块（CDP 直连脚本用 Node.js，需要此包）
echo "=== Installing ws (Node.js CDP WebSocket) ==="
npm install -g ws 2>/dev/null || npm install --prefix "$HOME/.local/npm" ws 2>/dev/null || true

# Playwright MCP 注册
echo "=== Registering Playwright MCP ==="
openclaw mcp set playwright '{"command":"npx","args":["-y","@playwright/mcp","--headless","--browser","chromium"]}' 2>/dev/null || true

# ── 标记安装完成 ──────────────────────────────────────────
touch "$SETUP_DONE_FLAG"

echo ""
echo "=== Setup complete. ==="
echo "  Start CDP:  chrome-cdp &"
echo "  Verify:     curl -s http://localhost:9223/json"
echo ""
echo "Next steps (follow SKILL.md):"
echo "  1. Edit ~/.openclaw/openclaw.json → add browser.noSandbox and ssrfPolicy"
echo "  2. Agent: browser stop → gateway restart → wait 15s → browser start"
echo "  3. Optional: bash scripts/setup-optional.sh  (browser-use CLI)"

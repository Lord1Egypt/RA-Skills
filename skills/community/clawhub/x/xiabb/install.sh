#!/bin/bash
# XiaBB (虾BB) — Native macOS Voice-to-Text Installer
# Compiles from source, creates .app bundle, installs to /Applications
# Safe to run multiple times (idempotent)
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
NATIVE_DIR="$SCRIPT_DIR/native"
BUILD_DIR="$NATIVE_DIR/build"
APP_NAME="XiaBB"
BUNDLE_ID="com.xiabb"
APP_DIR="$BUILD_DIR/$APP_NAME.app"
INSTALL_DIR="/Applications/$APP_NAME.app"

echo ""
echo "  🦞 XiaBB Installer"
echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ─── 1. Check Swift compiler ───

if ! command -v swiftc &>/dev/null; then
    echo "  [x] Swift compiler not found."
    echo "      Install Xcode Command Line Tools:"
    echo "      xcode-select --install"
    exit 1
fi
SWIFT_VER=$(swiftc --version 2>&1 | head -1)
echo "  [ok] $SWIFT_VER"

# ─── 2. Check / prompt for Gemini API key ───

API_KEY_FILE="$SCRIPT_DIR/.api-key"
EXISTING_KEY=""

if [ -n "$GEMINI_API_KEY" ]; then
    EXISTING_KEY="$GEMINI_API_KEY"
elif [ -f "$API_KEY_FILE" ]; then
    EXISTING_KEY="$(cat "$API_KEY_FILE" | tr -d '[:space:]')"
fi

if [ -n "$EXISTING_KEY" ]; then
    echo "  [ok] Gemini API key: ${EXISTING_KEY:0:10}..."
else
    echo ""
    echo "  Gemini API key is required for voice transcription."
    echo "  Get a free key at: https://aistudio.google.com/apikey"
    echo ""
    read -p "  Enter your Gemini API key: " EXISTING_KEY
    if [ -z "$EXISTING_KEY" ]; then
        echo ""
        echo "  [!] No API key provided. You can set it later:"
        echo "      echo 'YOUR_KEY' > $API_KEY_FILE"
        echo ""
    fi
fi

# Save API key to file if we have one
if [ -n "$EXISTING_KEY" ]; then
    echo -n "$EXISTING_KEY" > "$API_KEY_FILE"
    chmod 600 "$API_KEY_FILE"
    echo "  [ok] API key saved to $API_KEY_FILE"
fi

# ─── 3. Compile the binary ───

echo ""
echo "  Compiling $APP_NAME..."

rm -rf "$BUILD_DIR"
mkdir -p "$APP_DIR/Contents/MacOS" "$APP_DIR/Contents/Resources"

swiftc -O \
    -o "$APP_DIR/Contents/MacOS/$APP_NAME" \
    -framework AppKit \
    -framework AVFoundation \
    -framework CoreGraphics \
    -framework CoreAudio \
    -target arm64-apple-macosx14.0 \
    "$NATIVE_DIR/main.swift"

BINARY_SIZE=$(du -h "$APP_DIR/Contents/MacOS/$APP_NAME" | cut -f1 | tr -d '[:space:]')
echo "  [ok] Compiled ($BINARY_SIZE)"

# ─── 4. Create Info.plist ───

cat > "$APP_DIR/Contents/Info.plist" << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>XiaBB</string>
    <key>CFBundleDisplayName</key>
    <string>XiaBB</string>
    <key>CFBundleIdentifier</key>
    <string>com.xiabb</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundleExecutable</key>
    <string>XiaBB</string>
    <key>CFBundleIconFile</key>
    <string>XiaBB</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>LSMinimumSystemVersion</key>
    <string>14.0</string>
    <key>LSUIElement</key>
    <true/>
    <key>NSMicrophoneUsageDescription</key>
    <string>XiaBB needs microphone access to record your voice for transcription.</string>
    <key>NSAppleEventsUsageDescription</key>
    <string>XiaBB needs to simulate keyboard input to paste transcribed text.</string>
</dict>
</plist>
PLIST

# ─── 5. Copy icons ───

for icon in icon.png icon@2x.png icon@3x.png icon-red.png icon-red@2x.png icon-red@3x.png XiaBB.icns; do
    if [ -f "$SCRIPT_DIR/$icon" ]; then
        cp "$SCRIPT_DIR/$icon" "$APP_DIR/Contents/Resources/"
    fi
done

# ─── 6. Code sign ───

echo "  Signing..."
SIGN_ID=$(security find-identity -v -p codesigning 2>/dev/null | head -1 | sed 's/.*"\(.*\)"/\1/' || true)
if [ -n "$SIGN_ID" ] && [ "$SIGN_ID" != "0 valid identities found" ]; then
    codesign --force --deep --sign "$SIGN_ID" "$APP_DIR" 2>/dev/null
    echo "  [ok] Signed with: $SIGN_ID"
else
    codesign --force --deep --sign - "$APP_DIR" 2>/dev/null
    echo "  [ok] Signed ad-hoc (no developer identity)"
fi

# ─── 7. Install to /Applications ───

if [ -d "$INSTALL_DIR" ]; then
    echo "  Updating existing install..."
    cp "$APP_DIR/Contents/MacOS/$APP_NAME" "$INSTALL_DIR/Contents/MacOS/$APP_NAME"
    cp "$APP_DIR/Contents/Info.plist" "$INSTALL_DIR/Contents/Info.plist"
    mkdir -p "$INSTALL_DIR/Contents/Resources"
    cp -f "$APP_DIR/Contents/Resources/"* "$INSTALL_DIR/Contents/Resources/" 2>/dev/null || true
    # Re-sign to keep TCC permissions valid
    if [ -n "$SIGN_ID" ] && [ "$SIGN_ID" != "0 valid identities found" ]; then
        codesign --force --deep --sign "$SIGN_ID" "$INSTALL_DIR" 2>/dev/null
    else
        codesign --force --deep --sign - "$INSTALL_DIR" 2>/dev/null
    fi
    echo "  [ok] Updated /Applications/$APP_NAME.app"
else
    cp -R "$APP_DIR" "$INSTALL_DIR"
    echo "  [ok] Installed to /Applications/$APP_NAME.app"
fi

# ─── 8. Remove quarantine flag ───

xattr -cr "$INSTALL_DIR" 2>/dev/null || true
echo "  [ok] Quarantine attribute removed"

# ─── 9. Auto-start on login (optional) ───

echo ""
PLIST_PATH="$HOME/Library/LaunchAgents/$BUNDLE_ID.plist"
if [ -f "$PLIST_PATH" ]; then
    echo "  [ok] Launch agent already configured"
else
    read -p "  Start automatically on login? [y/N] " AUTO_START
    if [[ "$AUTO_START" =~ ^[Yy] ]]; then
        mkdir -p "$HOME/Library/LaunchAgents"
        cat > "$PLIST_PATH" << LAUNCHD
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$BUNDLE_ID</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/open</string>
        <string>-a</string>
        <string>$INSTALL_DIR</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>
LAUNCHD
        echo "  [ok] Auto-start configured"
    fi
fi

# ─── 10. Done ───

echo ""
echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🦞 Installation complete!"
echo ""
echo "  IMPORTANT — Grant Accessibility permission:"
echo "    1. Open System Settings > Privacy & Security > Accessibility"
echo "    2. Add Terminal.app (or your terminal) to the list"
echo "    3. XiaBB inherits the permission when launched"
echo ""
echo "  To run:    open /Applications/$APP_NAME.app"
echo "  To use:    Hold Globe (fn) key to speak, release to transcribe"
echo "  Logs:      ~/Library/Logs/XiaBB.log"
echo "  Config:    ~/Tools/xiabb/.config.json"
echo ""

#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
XIABB_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$SCRIPT_DIR/build"

# Parse flags
TIER="free"
BRAND="xiabb"
NO_INSTALL=false
while [[ $# -gt 0 ]]; do
    case $1 in
        --pro)       TIER="pro"; shift ;;
        --brand)     BRAND="$2"; shift 2 ;;
        --no-install) NO_INSTALL=true; shift ;;
        *)           shift ;;
    esac
done

# Set branding
case $BRAND in
    clawbb)
        BIN_NAME="ClawBB"
        BUNDLE_ID="com.clawbb"
        DISPLAY_NAME="ClawBB"
        ICON_DIR="$XIABB_DIR/icons/clawbb"
        ICNS_NAME="ClawBB"
        MIC_DESC="ClawBB needs microphone access to record your voice for transcription."
        KBD_DESC="ClawBB needs to simulate keyboard input to paste transcribed text."
        ;;
    *)
        BIN_NAME="XiaBB"
        BUNDLE_ID="com.xiabb"
        DISPLAY_NAME="XiaBB"
        ICON_DIR="$XIABB_DIR/icons/xiabb"
        ICNS_NAME="XiaBB"
        MIC_DESC="XiaBB needs microphone access to record your voice for transcription."
        KBD_DESC="XiaBB needs to simulate keyboard input to paste transcribed text."
        ;;
esac

APP_DIR="$BUILD_DIR/${BIN_NAME}.app"
CONTENTS="$APP_DIR/Contents"
MACOS="$CONTENTS/MacOS"
RESOURCES="$CONTENTS/Resources"

VERSION=$(cat "$XIABB_DIR/VERSION" 2>/dev/null || echo "0.0.0")
TIER_LABEL=$([ "$TIER" = "pro" ] && echo "Pro" || echo "Free")
echo "🦞 Building ${BIN_NAME} v${VERSION} (${TIER_LABEL})..."

# Clean
rm -rf "$BUILD_DIR"
mkdir -p "$MACOS" "$RESOURCES"

# Swift compiler flags
SWIFT_FLAGS="-O -target arm64-apple-macosx14.0"
if [ "$TIER" = "pro" ]; then
    SWIFT_FLAGS="$SWIFT_FLAGS -D PRO"
fi
if [ "$BRAND" = "clawbb" ]; then
    SWIFT_FLAGS="$SWIFT_FLAGS -D CLAWBB"
fi

# Compile
echo "   Compiling Swift..."
swiftc $SWIFT_FLAGS \
    -o "$MACOS/$BIN_NAME" \
    -framework AppKit \
    -framework AVFoundation \
    -framework CoreGraphics \
    -framework CoreAudio \
    -framework WebKit \
    "$SCRIPT_DIR/main.swift"

echo "   Binary size: $(du -h "$MACOS/$BIN_NAME" | cut -f1)"

# Info.plist
cat > "$CONTENTS/Info.plist" << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>${DISPLAY_NAME}</string>
    <key>CFBundleDisplayName</key>
    <string>${DISPLAY_NAME}</string>
    <key>CFBundleIdentifier</key>
    <string>${BUNDLE_ID}</string>
    <key>CFBundleVersion</key>
    <string>${VERSION}</string>
    <key>CFBundleShortVersionString</key>
    <string>${VERSION}</string>
    <key>CFBundleExecutable</key>
    <string>${BIN_NAME}</string>
    <key>CFBundleIconFile</key>
    <string>${ICNS_NAME}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>LSMinimumSystemVersion</key>
    <string>14.0</string>
    <key>LSUIElement</key>
    <true/>
    <key>NSMicrophoneUsageDescription</key>
    <string>${MIC_DESC}</string>
    <key>NSAppleEventsUsageDescription</key>
    <string>${KBD_DESC}</string>
</dict>
</plist>
PLIST

# Copy icons — try brand-specific dir first, fallback to root
if [ -d "$ICON_DIR" ]; then
    cp "$ICON_DIR"/* "$RESOURCES/" 2>/dev/null || true
else
    for icon in icon.png icon@2x.png icon@3x.png icon-red.png icon-red@2x.png icon-red@3x.png XiaBB.icns; do
        [ -f "$XIABB_DIR/$icon" ] && cp "$XIABB_DIR/$icon" "$RESOURCES/"
    done
fi

# Code sign
echo "   Code signing..."
SIGN_ID=$(security find-identity -v -p codesigning | head -1 | sed 's/.*"\(.*\)"/\1/')
if [ -n "$SIGN_ID" ] && [ "$SIGN_ID" != "0 valid identities found" ]; then
    codesign --force --deep --sign "$SIGN_ID" "$APP_DIR"
    echo "   Signed with: $SIGN_ID"
else
    codesign --force --deep --sign - "$APP_DIR"
    echo "   Signed ad-hoc"
fi

echo ""
echo "✅ Built: $APP_DIR"

# Install (skip with --no-install)
if [ "$NO_INSTALL" = true ]; then
    echo "   Skipping install (--no-install)"
    exit 0
fi

INSTALL_DIR="/Applications/${BIN_NAME}.app"
if [ -d "$INSTALL_DIR" ]; then
    echo "   Updating existing install..."
    cp "$MACOS/$BIN_NAME" "$INSTALL_DIR/Contents/MacOS/$BIN_NAME"
    cp "$CONTENTS/Info.plist" "$INSTALL_DIR/Contents/Info.plist"
    cp -f "$RESOURCES"/* "$INSTALL_DIR/Contents/Resources/" 2>/dev/null
    SIGN_ID=$(security find-identity -v -p codesigning | head -1 | sed 's/.*"\(.*\)"/\1/')
    if [ -n "$SIGN_ID" ] && [ "$SIGN_ID" != "0 valid identities found" ]; then
        codesign --force --deep --sign "$SIGN_ID" "$INSTALL_DIR"
    else
        codesign --force --deep --sign - "$INSTALL_DIR"
    fi
    echo "   ✅ Updated $INSTALL_DIR"
else
    echo "   Fresh install..."
    cp -R "$APP_DIR" "$INSTALL_DIR"
    echo "   ✅ Installed $INSTALL_DIR"
fi
echo ""
echo "To run:  open $INSTALL_DIR"

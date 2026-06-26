#!/bin/bash
#
# UOS 应用创建脚手架
# 自动生成符合 UOS 打包规范的目录结构
#

set -e

APPID="${1:-}"
APPNAME="${2:-}"

if [[ -z "$APPID" || -z "$APPNAME" ]]; then
    echo "用法: $0 <appid> <appname> [version]"
    echo "示例: $0 org.example.myapp 我的应用 1.0.0"
    exit 1
fi

VERSION="${3:-1.0.0}"

# 校验 appid 格式（倒置域名）
if ! echo "$APPID" | grep -qE '^[a-z][a-z0-9]*(\.[a-z][a-z0-9]*)+$'; then
    echo "错误: appid 格式不正确，应使用倒置域名，如 org.deepin.browser"
    exit 1
fi

echo "=== 创建 UOS 应用脚手架: $APPID ==="

mkdir -p "$APPID/entries/applications"
mkdir -p "$APPID/entries/icons/hicolor/scalable/apps"
mkdir -p "$APPID/entries/icons/hicolor/128x128/apps"
mkdir -p "$APPID/entries/icons/hicolor/256x256/apps"
mkdir -p "$APPID/files/bin"
mkdir -p "$APPID/entries/doc"
mkdir -p "$APPID/entries/locale/zh_CN"
mkdir -p "$APPID/DEBIAN"

# ── info 文件 ────────────────────────────────────────────────
cat > "$APPID/info" << EOF
{
    "appid": "${APPID}",
    "name": "${APPNAME}",
    "version": "${VERSION}",
    "arch": ["amd64"],
    "permissions": {
        "autostart": false,
        "notification": false,
        "trayicon": false,
        "clipboard": false,
        "account": false,
        "bluetooth": false,
        "camera": false,
        "audio_record": false,
        "installed_apps": false
    },
    "support-plugins": [],
    "plugins": []
}
EOF

# ── desktop 文件 ────────────────────────────────────────────
cat > "$APPID/entries/applications/${APPID}.desktop" << EOF
[Desktop Entry]
Name=${APPNAME}
Name[zh_CN]=${APPNAME}
Comment=UOS Application
Comment[zh_CN]=UOS 应用
Exec=/opt/apps/${APPID}/files/bin/${APPID##*.}
Icon=${APPID}
Type=Application
Terminal=false
StartupNotify=true
Categories=Development;
EOF

# ── SVG 图标模板（占位符）───────────────────────────────────
cat > "$APPID/entries/icons/hicolor/scalable/apps/${APPID}.svg" << 'SVGEOF'
<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="16" fill="#0081FF"/>
  <text x="64" y="80" font-size="64" text-anchor="middle" fill="white" font-family="sans-serif">APP</text>
</svg>
SVGEOF

# ── PNG 占位符说明 ──────────────────────────────────────────
touch "$APPID/entries/icons/hicolor/128x128/apps/${APPID}.png"
touch "$APPID/entries/icons/hicolor/256x256/apps/${APPID}.png"

# ── 可执行脚本模板 ──────────────────────────────────────────
cat > "$APPID/files/bin/${APPID##*.}" << 'BINEOF'
#!/bin/bash
# ${APPNAME} - ${APPID}
# UOS 应用入口脚本

echo "${APPNAME} 已启动"
# 在此替换为实际的应用启动命令
# exec /opt/apps/${APPID}/files/bin/real_app "$@"
BINEOF
chmod +x "$APPID/files/bin/${APPID##*.}"

# ── debian/control ──────────────────────────────────────────
cat > "$APPID/DEBIAN/control" << EOF
Package: ${APPID}
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: amd64
Maintainer: $(whoami) <$(whoami)@localhost>
Description: ${APPNAME}
EOF

# ── README ─────────────────────────────────────────────────
cat > "$APPID/README.md" << EOF
# ${APPNAME} (${APPID})

## 打包说明

- **appid**: ${APPID}
- **version**: ${VERSION}
- **架构**: amd64（修改 info 和 DEBIAN/control 可添加其他架构）

## 待完成

1. 替换 \`entries/icons/hicolor/scalable/apps/${APPID}.svg\` 为实际 SVG 图标
2. 替换 \`files/bin/${APPID##*.}\` 为实际可执行文件
3. 填写 desktop 文件的 Comment、Categories 等字段
4. 检查并编写 DEBIAN/postinst（如需要，**禁止修改系统文件**）
5. 执行 \`./build_deb.sh ${APPID} ${VERSION}\` 生成 deb 包

## 目录结构

\`\`\`
${APPID}/
├── entries/
│   ├── applications/${APPID}.desktop
│   ├── icons/
│   │   └── hicolor/
│   │       ├── scalable/apps/${APPID}.svg   ← 替换为实际图标
│   │       ├── 128x128/apps/${APPID}.png
│   │       └── 256x256/apps/${APPID}.png
│   └── doc/
├── files/
│   └── bin/${APPID##*.}                     ← 替换为实际程序
├── info                                      ← 应用描述
├── DEBIAN/control
└── README.md
\`\`\`
EOF

echo ""
echo "✅ 脚手架创建完成: $APPID/"
echo ""
echo "下一步:"
echo "  1. 替换图标和可执行文件"
echo "  2. 编辑 $APPID/entries/applications/${APPID}.desktop"
echo "  3. 修改 $APPID/info 中的架构等字段"
echo "  4. 运行 ./build_deb.sh ${APPID} ${VERSION} 生成 deb"
echo ""
ls -la "$APPID/"

#!/bin/bash
# Remotion プロジェクト初期化スクリプト（汎用）
# Usage: bash init-remotion.sh [project-name]

set -e

PROJECT_NAME=${1:-"my-video"}

echo "=== Remotion Video Project: $PROJECT_NAME ==="

# Remotionプロジェクト作成
npx create-video@latest "$PROJECT_NAME" --template blank

cd "$PROJECT_NAME"

# 追加パッケージ
npm install @remotion/player @remotion/google-fonts

# ディレクトリ構成
mkdir -p src/compositions
mkdir -p src/components/Character
mkdir -p src/components/Typography
mkdir -p src/components/Transitions
mkdir -p src/components/Branding
mkdir -p src/styles
mkdir -p public/fonts
mkdir -p public/images
mkdir -p public/audio

# theme.ts 生成（プレースホルダー）
cat > src/styles/theme.ts << 'EOF'
// プロジェクトのブランドに合わせてカラー・フォントを設定してください。
// CLAUDE.md の Video Branding セクションと一致させること。
export const theme = {
  colors: {
    primary: '#2D3748',       // メインカラー — 要変更
    accent: '#6366F1',        // アクセントカラー — 要変更
    background: '#1A202C',    // 背景色 — 要変更
    text: '#E2E8F0',          // テキスト色 — 要変更
    subAccent: '#63B3ED',     // サブアクセント — 要変更
  },
  fonts: {
    heading: 'Noto Sans JP',  // 要変更
    body: 'Noto Sans JP',     // 要変更
    mono: 'JetBrains Mono',
  },
  animation: {
    characterSpring: { damping: 12, mass: 0.5 },
    textReveal: { damping: 15, mass: 0.8 },
    fadeIn: { durationInFrames: 15 },
  },
} as const;

export type Theme = typeof theme;
EOF

echo ""
echo "=== Setup Complete ==="
echo "cd $PROJECT_NAME"
echo "npx remotion studio  # プレビュー起動"
echo ""
echo "NOTE: src/styles/theme.ts のカラー・フォントをプロジェクトのブランドに合わせて変更してください。"

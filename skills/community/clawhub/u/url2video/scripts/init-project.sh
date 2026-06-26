#!/bin/bash
# Initialize Remotion project for website-to-video

set -e

BRAND=$1
URL=$2

if [ -z "$BRAND" ] || [ -z "$URL" ]; then
    echo "Usage: ./init-project.sh <brand-name> <website-url>"
    echo "Example: ./init-project.sh futurai https://futurai.org"
    exit 1
fi

PROJECT="remotion-${BRAND}-promo"

echo "Creating project: $PROJECT"
mkdir -p "$PROJECT"/{src,audio,out,stills}
cd "$PROJECT"

# Init npm project
cat > package.json << EOF
{
  "name": "$PROJECT",
  "version": "1.0.0",
  "scripts": {
    "start": "remotion studio",
    "build": "remotion render src/index.tsx ${BRAND}-promo out/video.mp4",
    "stills": "remotion still src/index.tsx ${BRAND}-promo"
  },
  "dependencies": {
    "@remotion/cli": "^4.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "remotion": "^4.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "typescript": "^5.0.0"
  }
}
EOF

# Config
cat > remotion.config.ts << 'EOF'
import { Config } from '@remotion/cli/config';
Config.setVideoImageFormat('jpeg');
EOF

cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  }
}
EOF

# Index
cat > src/index.tsx << EOF
import { registerRoot, Composition } from 'remotion';
import { ${BRAND^}Promo } from './${BRAND^}Promo';

registerRoot(() => (
  <Composition
    id="${BRAND}-promo"
    component={${BRAND^}Promo}
    durationInFrames={1440}
    fps={24}
    width={854}
    height={480}
  />
));
EOF

# Placeholder narration
cat > audio/narration.txt << EOF
Scene 1: [Brand introduction]
Scene 2: [Vision and value proposition]
Scene 3: [Core services - 3 items]
Scene 4: [Trust signals and statistics]
Scene 5: [Call to action - visit website]
EOF

# Download free BGM
echo "Downloading free BGM..."
curl -L -o audio/bgm.mp3 "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=electronic-future-beats-117998.mp3" -H "User-Agent: Mozilla/5.0" 2>/dev/null || echo "BGM download failed, please download manually"

echo ""
echo "Project created: $PROJECT"
echo "Next steps:"
echo "  1. cd $PROJECT"
echo "  2. npm install"
echo "  3. Write src/${BRAND^}Promo.tsx"
echo "  4. Generate TTS audio -> audio/narration.mp3"
echo "  5. npm run build"

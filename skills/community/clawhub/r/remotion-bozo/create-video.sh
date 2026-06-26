#!/bin/bash
# Remotion Bozo - 快速创建视频项目脚本

set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_green() {
    echo -e "${GREEN}$1${NC}"
}

print_blue() {
    echo -e "${BLUE}$1${NC}"
}

print_yellow() {
    echo -e "${YELLOW}$1${NC}"
}

# 检查项目名称
if [ -z "$1" ]; then
    print_yellow "用法: remotion-bozo create <项目名称>"
    print_yellow "示例: remotion-bozo create my-video"
    exit 1
fi

PROJECT_NAME=$1
PROJECT_DIR=$(pwd)/$PROJECT_NAME

print_green "🎬 创建 Remotion 视频项目: $PROJECT_NAME"

# 1. 创建项目目录
print_blue "📁 创建项目目录..."
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# 2. 创建目录结构
print_blue "📂 创建目录结构..."
mkdir -p src out

# 3. 初始化 npm
print_blue "📦 初始化 npm..."
npm init -y > /dev/null 2>&1

# 4. 安装依赖
print_blue "⬇️  安装 Remotion 依赖..."
npm install remotion@4.0.436 @remotion/cli@4.0.436 @remotion/renderer@4.0.436 react@18.3.1 react-dom@18.3.1 --save > /dev/null 2>&1
npm install typescript @types/react @types/react-dom --save-dev > /dev/null 2>&1

# 5. 创建 package.json
print_blue "📝 创建 package.json..."
cat > package.json << 'EOF'
{
  "name": "PROJECT_NAME",
  "version": "1.0.0",
  "description": "Remotion Video Project",
  "type": "module",
  "scripts": {
    "start": "remotion studio",
    "build": "remotion render",
    "render": "remotion render src/index.tsx MyVideo out/video.mp4",
    "render:lambda": "remotion lambda src/index.tsx MyVideo --function-name=remotion-render"
  },
  "keywords": ["remotion", "video"],
  "author": "",
  "license": "ISC",
  "dependencies": {
    "@remotion/cli": "^4.0.436",
    "@remotion/renderer": "^4.0.436",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "remotion": "^4.0.436"
  },
  "devDependencies": {
    "@types/react": "^19.2.14",
    "@types/react-dom": "^19.2.3",
    "typescript": "^5.9.3"
  }
}
EOF

# 替换项目名称
sed -i '' "s/PROJECT_NAME/$PROJECT_NAME/g" package.json

# 6. 创建 tsconfig.json
print_blue "📝 创建 tsconfig.json..."
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["DOM", "DOM.Iterable", "ES2022"],
    "jsx": "react-jsx",
    "module": "ES2022",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "allowJs": true,
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true,
    "noEmit": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
EOF

# 7. 创建 src/index.tsx
print_blue "📝 创建 src/index.tsx..."
cat > src/index.tsx << 'EOF'
import {Composition, registerRoot} from 'remotion';
import {MyVideo} from './MyVideo';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MyVideo"
        component={MyVideo}
        durationInFrames={900} // 30秒 @ 30fps
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};

registerRoot(RemotionRoot);
EOF

# 8. 创建 src/MyVideo.tsx
print_blue "📝 创建 src/MyVideo.tsx..."
cat > src/MyVideo.tsx << 'EOF'
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  Easing,
} from 'remotion';

// Spring 动画配置
const springConfig = {
  damping: 12,
  stiffness: 80,
  mass: 1,
};

export const MyVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const fps = 30;
  const duration = 900; // 30秒
  const progress = frame / duration;

  // 标题缩放动画
  const scale = spring({
    frame: progress * 30,
    fps,
    config: springConfig,
  });

  // 淡入动画
  const opacity = interpolate(progress, [0, 0.3], [0, 1], {
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

  // 上移动画
  const y = interpolate(progress, [0, 0.5], [100, 0], {
    extrapolateRight: 'clamp',
    easing: Easing.bezier(0.68, -0.55, 0.265, 1.55),
  });

  return (
    <AbsoluteFill style={{
      background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
    }}>
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100%',
        opacity,
      }}>
        {/* 标题 */}
        <h1 style={{
          fontSize: 96,
          fontWeight: 800,
          margin: 0,
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
          transform: `translateY(${y}px) scale(${scale})`,
          fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        }}>
          Hello Remotion!
        </h1>

        {/* 副标题 */}
        <p style={{
          fontSize: 36,
          color: '#a0aec0',
          marginTop: 40,
          opacity: interpolate(progress, [0.3, 0.6], [0, 1], {
            extrapolateRight: 'clamp',
          }),
          fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        }}>
          使用 remotion-bozo 创建你的第一个视频
        </p>

        {/* 装饰线 */}
        <div style={{
          width: interpolate(progress, [0.4, 0.8], [0, 300], {
            extrapolateRight: 'clamp',
            easing: Easing.out(Easing.cubic),
          }),
          height: 4,
          background: 'linear-gradient(90deg, #667eea 0%, #f093fb 100%)',
          borderRadius: 2,
          marginTop: 50,
        }} />
      </div>
    </AbsoluteFill>
  );
};
EOF

# 9. 创建 README.md
print_blue "📝 创建 README.md..."
cat > README.md << EOF
# $PROJECT_NAME

使用 remotion-bozo 创建的 Remotion 视频项目。

## 快速开始

\`\`\`bash
# 预览视频
npm start

# 渲染视频
npm run render
\`\`\`

## 项目结构

\`\`\`
src/
├── index.tsx      # 入口文件
└── MyVideo.tsx    # 视频组件
\`\`\`

## 动画工具

项目预配置了以下动画工具：

- Spring 动画配置
- Easing 缓动函数
- 贝塞尔曲线预设
- 场景进度计算

## 自定义视频

编辑 \`src/MyVideo.tsx\` 来自定义你的视频内容。

## 更多帮助

- [Remotion 文档](https://www.remotion.dev/docs)
- [remotion-bozo 技能](https://clawhub.ai/bozoyan/remotion-bozo)

---

*创建日期: $(date +%Y-%m-%d)*
EOF

# 完成
print_green "✅ 项目创建完成！"
echo ""
print_blue "📋 项目信息："
echo "  项目目录: $PROJECT_DIR"
echo "  项目名称: $PROJECT_NAME"
echo ""
print_green "🚀 快速开始："
echo "  cd $PROJECT_NAME"
echo "  npm start       # 预览视频"
echo "  npm run render  # 渲染视频"
echo ""
print_yellow "💡 提示："
echo "  - 编辑 src/MyVideo.tsx 来自定义视频内容"
echo "  - 修改 durationInFrames 调整视频时长"
echo "  - 使用 npm run render:lambda 进行云端渲染"

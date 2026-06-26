# 项目模板

完整的 Remotion 项目模板，开箱即用。

## 文件结构

```
project-name/
├── src/
│   ├── index.tsx              # 入口文件，定义 Composition
│   └── VideoComponent.tsx     # 视频组件
├── out/                       # 输出目录
├── package.json
└── tsconfig.json
```

## package.json

```json
{
  "name": "my-video",
  "version": "1.0.0",
  "description": "My Remotion Video",
  "type": "module",
  "scripts": {
    "start": "remotion studio",
    "build": "remotion render",
    "render": "remotion render src/index.tsx MyVideo out/video.mp4",
    "render:lambda": "remotion lambda src/index.tsx MyVideo --function-name=remotion-render"
  },
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
```

## tsconfig.json

```json
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
```

## src/index.tsx

```typescript
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
```

## 创建项目步骤

```bash
# 1. 创建目录
mkdir my-video && cd my-video

# 2. 初始化 npm
npm init -y

# 3. 安装依赖
npm install remotion@4.0.436 @remotion/cli@4.0.436 @remotion/renderer@4.0.436 react@18.3.1 react-dom@18.3.1
npm install -D typescript @types/react @types/react-dom

# 4. 创建 src 目录
mkdir src

# 5. 复制模板文件
# (复制上述配置文件)
```

## 快速启动

```bash
npm install
npm start    # 预览
npm run render  # 渲染
```

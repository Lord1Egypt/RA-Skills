# Apple Style 模板 — 视频号竖屏版

基于 Apple 发布会风格的竖屏视频模板，适用于技术干货/源码解读/知识科普类内容。

## 字号规范（视频号竖屏）

| 元素 | 字号 | 字重 | 说明 |
|------|------|------|------|
| 主标题 | **72px** | Semibold (600) | 前三秒抓眼球 |
| 二级标题/节点 | **32px** | Medium (500) | 竖屏最佳阅读尺寸 |
| 注释/标签/来源 | **20px** | Regular (400) | 视频号最小可读底线 |

> ⚠️ 14-16px 在手机上基本看不清，20px 是底线。

## 配色（Apple 高级科技风）

```
背景：      #111111 → #1c1c1e 深空黑渐变
主文字：    #FFFFFF 纯白
强调色：    #007AFF Apple 蓝（唯一强调色）
次要文字：  #8E8E93 浅灰
边框/卡片： #3a3a3c / #2c2c2e
```

> ⚠️ 只用黑白+一个强调色，科技类最忌颜色杂乱。

## 字体选择

```
优先：SF Pro Display（标题）+ SF Pro Text（正文）
备选：PingFang SC / 思源黑体
拒绝：花体、圆体、综艺体
```

## 安全区

```
上右下左各留 60px，避免被账号头像/进度条遮挡
```

## 竖屏布局规范（9:16 · 1080×1920）

```
┌──────────────────────────────────┐
│ SceneTag (top:60px, left:60px)  │
├──────────────────────────────────┤
│ HeroTitle (top:80px)  72px      │
│                                   │
│ 内容区 (top:280px)  32px 节点   │
│                                   │
│ TagGroup (bottom:88%)            │
└──────────────────────────────────┘
```

## 组件清单

| 组件 | 字号 | 字重 | 用途 |
|------|------|------|------|
| `HeroTitle` | 72px | 600 | 主标题 |
| `NodeTitle` | 32px | 500 | 二级标题/节点 |
| `Caption` | 20px | 400 | 注释/标签 |
| `SceneTag` | 20px | 400 | 左上角场景标签 |
| `AccentText` | 32px | 500 | 蓝色强调文字 |
| `TagPill` | 20px | 400 | 单个标签胶囊 |
| `TagGroup` | — | — | 标签组 |
| `LayerStack` | 32px/20px | 500/400 | 分层卡片 |
| `TwoColumn` | 32px/20px | 500/400 | 双栏对比 |
| `NineGrid` | 20px | 500 | 3×3 网格 |
| `StepList` | 32px/20px | 500/400 | 步骤列表 |
| `EngineSpin` | — | — | 引擎旋转 SVG |

## 动画规范

所有动画基于 `useCurrentFrame()` + `interpolate()`：

```tsx
// fade-up（标题）
opacity: 0→1, translateY: 24→0, 14帧

// scale-in（卡片）
opacity: 0→1, scale: 0.5→1, 16帧

// translateX（列表项依次出现）
translateX: -20→0, 14帧

// stagger 列表：每项 delay += 8~14 帧
```

## 使用方法

### 1. 复制模板到 Remotion 项目
```
cp -r templates/apple /path/to/project/src/components/AppleShared
```

### 2. 在场景中导入
```tsx
import {
  AppleBg, HeroTitle, NodeTitle, Caption, SceneTag,
  TagGroup, LayerStack, TwoColumn, NineGrid,
  StepList, EngineSpin, SAFE
} from "../components/AppleShared";
```

### 3. 场景示例
```tsx
export const 开场: React.FC = () => (
  <AppleBg>
    <SceneTag text="Cloud Code 源码解读" startFrame={0} />
    <HeroTitle text="上下文管理" startFrame={5} />
    <TagGroup
      startFrame={45}
      tags={[
        { text: "四层压缩", accent: true },
        { text: "子系统", accent: false },
      ]}
    />
  </AppleBg>
);
```

## 设计检查清单

- [ ] 标题是否 ≥72px，足够抓眼球？
- [ ] 节点文字是否 ≥32px，手机上可读？
- [ ] 标签是否 ≥20px，不是 14-16px？
- [ ] 颜色是否只有黑白+一个强调色（#007AFF）？
- [ ] 上下左右是否各留 60px 安全区？
- [ ] 字体是否为 SF Pro / PingFang？

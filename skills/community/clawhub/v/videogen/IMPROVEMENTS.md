# videogen 改进总结（2026-04-08）

## 一、问题与修复

### 1.1 TTS Harness 合并失败
**问题**：`filter_complex` 和 `concat muxer` 都失败，输出 0 字节
**根因**：shutil/os 只在 if 分支内 import，except 块里访问不到
**修复**：`scripts/v2/tts_harness.py` 文件顶部统一导入

```python
# 错误写法
def func():
    if condition:
        import shutil
        shutil.copy2(...)
    except:
        shutil.copy2(...)  # NameError!

# 正确写法
import shutil
def func():
    if condition:
        shutil.copy2(...)
    except:
        shutil.copy2(...)
```

### 1.2 竖屏字体太小看不清
**问题**：视频号播放时微信 UI 遮挡 15%，节点文字 11-13px 完全不可读
**修复**：字号全面放大
| 元素 | 旧 | 新 |
|------|----|----|
| 页面标题 | 80px | 60-72px |
| 节点标题 | 11-13px | 22-28px |
| 标签文字 | 14px | 14-16px |

### 1.3 微压缩双路径布局挤在一起
**问题**：两条路径的节点和箭头挤在中间，视觉混乱
**修复**：左右对称卡片布局，中间加分隔线，底部加结果说明

---

## 二、Apple 风格规范（新增）

### 2.1 设计 Token（精简版）
```
背景：   #111111 → #1c1c1e 深空黑渐变
强调色： #007AFF   Apple 蓝（唯一强调色）
主文字： #FFFFFF
次要：   #8E8E93
边框：   #3a3a3c
卡片：   #2c2c2e
```

### 2.2 竖屏安全区（9:16 · 1080×1920）
```
┌──────────────────────────┐
│ SceneTag (top:56px)       │ ← 场景标签
├──────────────────────────┤
│ 标题区 (top:8%)          │ ← HeroTitle
│                          │
│ 内容区 (top:24%)         │ ← 主体图表
│                          │
│ 标签组 (bottom:10%)      │
└──────────────────────────┘
```
**关键**：内容集中在中间带，避免被 UI 遮挡

### 2.3 动画规范
所有动画用 `useCurrentFrame()` 驱动，禁止 CSS transition/animation：
```
fade-up：opacity 0→1, translateY 30→0, 12-14帧
scale：  0.4→1, 15-16帧
stagger： delay += 12~16帧/项
```

---

## 三、模板文件

### 3.1 Apple 风格组件库
**位置**：`templates/apple/AppleShared.tsx`

13个可复用组件：
| 组件 | 用途 |
|------|------|
| `AppleBg` | 渐变背景 |
| `SceneTag` | 左上角场景标签 |
| `HeroTitle` | 大标题 fade-up |
| `LayerStack` | 分层卡片堆栈 |
| `FlowNode` | 流程圆节点 |
| `ArrowSVG` | SVG 箭头线 |
| `NineGrid` | 3×3 彩色网格 |
| `PipelineFlow` | 横向管线流 |
| `FuseSteps` | 熔断器步骤列表 |
| `ToolGrid` | 工具网格 |
| `EngineSpin` | 旋转引擎 SVG |
| `TagGroup` | 标签组 |
| `TagPill` | 单个标签 |

### 3.2 使用方法
```bash
# 复制到 Remotion 项目
cp -r templates/apple /path/to/video-project/src/components/

# 在场景文件导入
import { AppleBg, HeroTitle, SceneTag } from "../components/AppleShared";
```

---

## 四、后续优化项

### 高优先级
1. **TTS 合并逻辑重写**：当前写文件时序有问题，需要确保 concat_list.txt 在 ffmpeg 之前写好
2. **Apple 风格生成器**：给 `remotion_generator.py` 加 `--apple-style` 参数自动生成 Apple 风格场景
3. **字幕自动对齐**：当前纯手动，可根据 TTS 时间戳自动生成字幕

### 中优先级
4. **Remotion 动画预设**：把 fade-up/scale/stagger 等做成可配置参数
5. **图表类型扩展**：时间线、架构树、数据对比图
6. **视频号平台适配**：根据平台（视频号/抖音/B站）自动调整安全区

### 低优先级
7. **Hailuo 视频片段**：技术内容适合用 AI 生成演示片段
8. **数字分身**：口播类内容可加数字人形象

---

## 二、视频号竖屏字体规范（2026-04-08 更新）

### 字号标准（固定值）

| 元素 | 字号 | 字重 |
|------|------|------|
| 主标题 | 72px | Semibold (600) |
| 二级标题/节点 | 32px | Medium (500) |
| 注释/标签 | 20px | Regular (400) |

### 配色标准

| 用途 | 色值 |
|------|------|
| 背景 | `#111111 → #1c1c1e` |
| 强调色 | `#007AFF`（唯一） |
| 主文字 | `#FFFFFF` |
| 次要文字 | `#8E8E93` |

### 安全区
上下左右各 60px

### 字体
SF Pro Display + SF Pro Text / PingFang SC

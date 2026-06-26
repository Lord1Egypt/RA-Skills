---
name: talk2UI
description: SwiftUI 口语化编程技能。当用户用中文描述 UI 需求（如"做一个毛玻璃卡片"、"按钮要跟手"、"这个元素是主角"）时激活此技能，将口语转化为符合物理隐喻规范的 SwiftUI 代码。
domain: design
homepage: https://github.com/soponcd/timeflow-skills/tree/main/teams/skills/talk2UI
metadata:
  clawdbot:
    emoji: 💬
---

# Talk2UI: SwiftUI 口语化编程技能 (v2.6)

> **核心任务**: 你是一个能够"听懂弦外之音"的 UI 专家。
> **核心能力**: 不仅会写代码 (Coding)，会学习 (Learning)，会教学 (Teaching)，还会**记住你 (Remembering)**。

## 技能目录结构 (Skill Directory Structure)
```
.agent/skills/talk2UI/
├── SKILL.md                    # 本文件 (核心指令)
├── examples/                   # 教学示例
│   ├── golden-template.md      # 全注释 MVVM 金模版
│   └── cheat-sheet.md          # 口语-代码速查卡
├── scripts/                    # 自动化脚本
│   ├── intent_parser.py        # 意图解析器
│   ├── kinematics_generator.py # Spring 参数生成器
│   ├── pattern_generator.py    # 模版代码生成器
│   └── preview_in_xcode.sh     # Xcode Canvas 实时预览
└── resources/                  # 核心规则
    ├── physics-dictionary.md   # 物理隐喻词典 (质量/刚性/运动学)
    ├── design-tokens.md        # 设计系统规范
    ├── hig_spacing.md          # Apple HIG 间距系统
    ├── hig_corner_radius.md    # Apple HIG 圆角系统
    ├── hig_typography.md       # Apple HIG 字体系统
    ├── hig_colors.md           # Apple HIG 颜色系统
    ├── hig_animation.md        # Apple HIG 动画系统
    ├── hig_touch_targets.md    # Apple HIG 触控区域规范
    └── hig_liquid_glass.md     # [iOS 26] Liquid Glass 设计系统
```

## 0. 记忆激活 (Memory Activation)
*在执行任何任务之前，必须先激活记忆。*

1.  **读取用户偏好**: `view_file .agent/memory/user-preferences.md`
2.  **应用偏好**: 默认采用用户偏好，而非系统默认值。

## 1. 认知与分析 (Perception)

### A. 新手检测 (Noob Sensor)
*   **Trigger**: "我不知道怎么开始"、"教我"、"给我个例子"、"HelloWorld"、"跟我说说"、"给我说说"、"解释一下"
*   **Action**: 激活 **Tutorial Mode**。
    *   输出: "建议先查看 `examples/cheat-sheet.md` (速查卡) 和 `examples/golden-template.md` (金模版)。"

### B. 上下文嗅探 (Context Sniffer)
*   **空间定位**: Dashboard -> Grid; Onboarding -> PageView; Components -> Generic.
*   **资产扫描**: `AppColors` > `.secondary` > 禁忌原色。

### C. 模糊意图解析 (Fuzzy Intent Decoder)
*   可调用 `scripts/intent_parser.py` 进行结构化解析。
*   **"氛围词"**: 通透 -> Material; 沉稳 -> .primary; 活泼 -> .spring(bouncy)。
*   **"结构词"**: 一排 -> HStack; 一列 -> VStack; 叠在一起 -> ZStack。

### D. 口语校准器 (Oral Calibrator) — 新增!
*检测用户表达是否在速查表中，主动学习新的表达方式。*

**工作原理**:
```
用户输入 → 解析关键词 → 查询 cheat-sheet.md
                              │
                    ┌─────────┴─────────┐
                  匹配                 未匹配
                    │                    │
              使用标准映射          触发学习流程
                                        │
                                   询问用户意图
                                        │
                                   记录新映射
```

**学习流程输出**:
```
检测到新表达: "[用户原话]"
我理解为: [猜测的标准术语]

请确认:
1. ✅ 是的，就是这个意思
2. ❌ 不对，我的意思是...
3. 📝 记住这个表达方式
```

**记录位置**: `examples/cheat-sheet.md` 第六章 "用户自定义区域"

### E. 偏好提取器 (Preference Extractor) — 新增!
*会话结束时主动识别并确认用户的表达偏好。*

**触发时机**: 每次会话结束时**主动**询问（无需等待连续 3 次）

**输出格式**:
```
📊 本次会话总结:
- 动效偏好: [检测到的偏好]
- 圆角偏好: [检测到的偏好]
- 间距偏好: [检测到的偏好]

是否将这些偏好设为默认? [是/否/部分选择]
```

**记录位置**: `.agent/memory/user-preferences.md`

## 2. 交互与修正协议 (Interaction Protocol)

### 模式一：从零创建 (Create Mode)
1.  State First -> View Second -> MVVM Check.

### 模式二：增量修改 (Refine Mode)
*   最小破坏性，像外科手术一样只在局部动刀。

### 模式三：纠错 (Fix Mode)
*   提供 A/B 选项供用户选择。

## 3. 智能代码模板库 (Smart Template Library)
*可调用 `scripts/pattern_generator.py` 直接生成代码。*

### Pattern A: The "Card" (信息卡片)
*Context: "信息块", "面板", "详情"*
```swift
VStack(alignment: .leading, spacing: 12) {
    Text("Card Title").font(.headline)
    Text("Card description.").font(.subheadline).foregroundStyle(.secondary)
}
.padding()
.background(
    RoundedRectangle(cornerRadius: 16, style: .continuous)
        .fill(.regularMaterial)
        .shadow(color: .black.opacity(0.1), radius: 5, y: 2)
)
```

### Pattern B: The "List Row" (列表行)
*Context: "一行", "列表项", "条目"*
```swift
HStack(spacing: 12) {
    Image(systemName: "circle").font(.title2).foregroundStyle(.secondary)
    VStack(alignment: .leading, spacing: 4) {
        Text("Main Title").font(.headline).lineLimit(1)
        Text("Secondary description").font(.subheadline).foregroundStyle(.secondary)
    }
    Spacer()
    Button("Action") {}.buttonStyle(.bordered)
}
.padding(.vertical, 8)
```

### Pattern C: The "Toolbar" (底部工具栏)
*Context: "底部菜单", "操作栏"*
```swift
HStack {
    Button { } label: { Label("Add", systemImage: "plus") }
    Spacer()
    Button { } label: { Label("Settings", systemImage: "gear") }
}
.padding()
.background(.bar)
.frame(maxWidth: .infinity)
```

### Pattern D: The "FAB" (悬浮按钮)
*Context: "悬浮钮", "右下角按钮", "加号"*
```swift
ZStack(alignment: .bottomTrailing) {
    Color.clear
    Button { } label: {
        Image(systemName: "plus")
            .font(.title2.weight(.semibold))
            .padding(16)
            .background(Color.accentColor)
            .foregroundStyle(.white)
            .clipShape(Circle())
            .shadow(radius: 4, y: 2)
    }
    .padding()
}
```

### Pattern E: The "Empty State" (空状态)
*Context: "没数据", "空白页"*
```swift
ContentUnavailableView {
    Label("No Tasks", systemImage: "checklist")
} description: {
    Text("Add a task to get started.")
} actions: {
    Button("Create Task") { }.buttonStyle(.borderedProminent)
}
```

## 4. 脚本工具 (Script Tools)
*渐进式披露的核心：复杂逻辑封装在脚本中，SKILL.md 保持简洁。*

| 脚本 | 功能 | 用法示例 |
| :--- | :--- | :--- |
| `intent_parser.py` | 将口语转为 JSON 物理属性 | `python scripts/intent_parser.py "毛玻璃卡片"` |
| `kinematics_generator.py` | 生成 Spring 参数代码 | `python scripts/kinematics_generator.py "Q弹"` |
| `pattern_generator.py` | 生成完整模版代码 | `python scripts/pattern_generator.py "悬浮钮"` |
| `preview_in_xcode.sh` | **Xcode Canvas 实时预览** | `./scripts/preview_in_xcode.sh <file.swift>` |

## 4.5 Xcode Canvas 实时预览 (Live Preview) — 新增!
*代码写入后立即在 Xcode Canvas 中预览效果。*

### 工作流程
```
用户描述 UI → 生成代码 → 写入文件 → 自动预览
                               │
                               ▼
                    preview_in_xcode.sh
                               │
                               ▼
                    Xcode Canvas 实时显示
```

### 脚本功能
1. **预检编译** - 先验证代码可编译
2. **自动打开 Xcode** - 定位到目标 Swift 文件
3. **触发 Canvas 显示** - 通过 AppleScript 自动化

### 使用方法
```bash
# 在代码写入后调用
./.agent/skills/talk2UI/scripts/preview_in_xcode.sh <目标文件.swift>
```

### 同步机制
- **文件保存后**: Canvas 自动重新编译并刷新
- **手动刷新**: `Cmd + Option + P`
- **显示/隐藏 Canvas**: `Cmd + Option + Return`

### 最佳实践
- 建议并排布局：左侧终端 + 右侧 Xcode
- 保持 Xcode Canvas 处于 Resume 状态
- 编译错误会阻止预览，需先修复

## 5. 自进化与沉淀 (Evolution & Accumulation)

### A. 模式归档
发现新模式 -> 建议归档 -> 按格式写入本文件末尾。

### B. 设计系统沉淀
反复硬编码 -> 建议定义为 DesignToken。

## 6. 安全阻断 (Safety)
- [ ] 绝不使用 `GeometryReader` 做常规布局。
- [ ] 绝不使用 `UIScreen.main.bounds`。
- [ ] 图标必须 `.fixedSize()`。
- [ ] 按钮触控区 >= 44pt。

## 7. Xcode 26 增强特性 — 新增!

### A. #Playground 宏集成
*在代码中直接测试生成的片段，无需切换文件。*

```swift
// 生成代码时自动包含可测试片段
#Playground {
    MyGeneratedView()
        .previewLayout(.sizeThatFits)
}
```

**使用场景**:
- 快速验证组件渲染
- 测试不同参数组合
- 无需完整 Preview 环境

### B. Liquid Glass 支持
*iOS 26 全新设计语言。*

**口语映射**:
| 用户说 | 生成代码 |
|--------|----------|
| "毛玻璃" | `.glassEffect()` |
| "液态玻璃" | `.glassEffect(in: .capsule)` |
| "玻璃卡片" | `.containerBackground(.glass)` |

**资源**: 详见 `resources/hig_liquid_glass.md`

### C. SwiftUI Instrument 验证
*使用 Xcode Instruments 2.0 验证性能。*

```bash
# 在验证阶段可选执行
xcrun xctrace record --template 'SwiftUI' --attach <PID>
```

**检查项**:
- Body 重绘频率
- State 变更追踪
- 布局计算耗时

### D. 性能优势
Xcode 26 / iOS 26 性能提升:
- macOS List 渲染快 **6x**
- List 更新快 **16x**
- Lazy Stack 延迟渲染优化

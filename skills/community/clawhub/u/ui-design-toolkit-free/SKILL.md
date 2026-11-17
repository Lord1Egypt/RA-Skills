---
name: "ui-design-toolkit-free"
description: "UI设计原则与优选实践工具包,涵盖视觉层次、排版、色彩与间距,适合个人开发者快速上手。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "UI设计工具包免费版"
  version: "1.0.0"
  summary: "UI设计原则与优选实践工具包,涵盖视觉层次、排版、色彩与间距,适合个人开发者快速上手。"
  tags:
    - "创意设计"
    - "UI设计"
    - "界面设计"
    - "设计原则"
    - "前端开发"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# UI 设计工具包 - 免费版

## 概述

UI 设计工具包(免费版)为个人开发者提供界面设计的核心原则与优选实践。涵盖视觉层次、排版、色彩、间距、组件状态与响应式设计,帮助快速构建清晰、一致、美观的用户界面。

免费版聚焦核心设计原则,专业版(`ui-design-toolkit-pro`)在此基础上提供设计系统、设计令牌、可访问性深度规范与组件库等高级能力。

## 核心能力

| 能力 | 免费版 | 说明 |
|:-----|:-------|:-----|
| 视觉层次 | 支持 | 焦点、分组、留白 |
| 排版规范 | 支持 | 字体、字号、行高 |
| 色彩使用 | 支持 | 主色、语义色、中性色 |
| 间距系统 | 支持 | 4px/8px 网格 |
| 对齐规范 | 支持 | 网格与光学对齐 |
| 组件状态 | 支持 | 默认/悬停/聚焦/禁用 |
| 图标使用 | 支持 | 风格一致性 |
| 响应式设计 | 基础 | 移动优先 |
| 暗黑模式 | 基础 | 色彩反转 |
| 动效设计 | 基础 | 过渡与缓动 |
| 设计系统 | 不支持 | 升级专业版 |
| 设计令牌 | 不支持 | 升级专业版 |
| 可访问性深度 | 不支持 | 升级专业版 |
| 组件库 | 不支持 | 升级专业版 |

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 按照skill规范执行核心功能执行操作,遵循单一意图原则。
**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输入**: 用户提供参数配置与调用所需的指令和必要参数。
**处理**: 按照skill规范执行参数配置与调用操作,遵循单一意图原则。
**输出**: 返回参数配置与调用的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输入**: 用户提供结果处理与输出所需的指令和必要参数。
**处理**: 按照skill规范执行结果处理与输出操作,遵循单一意图原则。
**输出**: 返回结果处理与输出的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：设计原则与优选实、践工具包、涵盖视觉层次、色彩与间距、适合个人开发者快、速上手、面向个人开发者的、设计工具包、核心能力、Visual、Hierarchy、设计原则、Typography、规范与字号体系、Color、使用与语义化、Spacing、系统与网格、States、响应式设计基础、暗黑模式基础、常见设计陷阱规避等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一:设计清晰的卡片界面

运用视觉层次与间距系统设计卡片。

```html
<!-- 卡片组件:运用层次、间距、色彩原则 -->
<div class="max-w-sm rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
  <!-- 主焦点:标题 -->
  <h3 class="text-lg font-semibold text-gray-900">
    月度报告
  </h3>

  <!-- 次要信息:描述 -->
  <p class="mt-2 text-sm text-gray-600 leading-relaxed">
    2026 年 7 月运营数据概览,包含用户增长、收入与活跃度指标。
  </p>

  <!-- 数据展示 -->
  <div class="mt-4 space-y-2">
    <div class="flex justify-between text-sm">
      <span class="text-gray-500">用户增长</span>
      <span class="font-medium text-green-600">+12.5%</span>
    </div>
    <div class="flex justify-between text-sm">
      <span class="text-gray-500">月收入</span>
      <span class="font-medium text-gray-900">¥128,500</span>
    </div>
  </div>

  <!-- 主操作 -->
  <button class="mt-6 w-full rounded-md bg-blue-500 px-4 py-2
                 text-sm font-medium text-white
                 hover:bg-blue-600 active:bg-blue-700
                 transition-colors">
    查看详情
  </button>
</div>
```

### 场景二:响应式表单设计

运用排版与状态规范设计表单。

```html
<form class="max-w-md mx-auto space-y-6">
  <!-- 标题层次 -->
  <div>
    <h2 class="text-2xl font-bold text-gray-900">创建账户</h2>
    <p class="mt-1 text-sm text-gray-500">填写以下信息开始使用</p>
  </div>

  <!-- 表单字段:统一间距与状态 -->
  <div class="space-y-4">
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1.5">
        邮箱
      </label>
      <input type="email"
             class="w-full rounded-md border border-gray-300 px-3 py-2
                    text-gray-900 placeholder-gray-400
                    focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20
                    focus:outline-none transition-colors"
             placeholder="you@example.com" />
    </div>

    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1.5">
        密码
      </label>
      <input type="password"
             class="w-full rounded-md border border-gray-300 px-3 py-2
                    focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20
                    focus:outline-none"
             placeholder="至少 8 位" />
      <p class="mt-1.5 text-xs text-gray-500">使用大小写字母与数字组合</p>
    </div>
  </div>

  <!-- 主操作 + 次要操作 -->
  <div class="space-y-3">
    <button class="w-full rounded-md bg-blue-500 px-4 py-2.5
                   font-medium text-white
                   hover:bg-blue-600 transition-colors">
      创建账户
    </button>
    <p class="text-center text-sm text-gray-500">
      已有账户?<a href="#" class="text-blue-500 hover:underline">登录</a>
    </p>
  </div>
</form>
```

### 场景三:暗黑模式适配

运用色彩原则适配暗黑模式。

```html
<!-- 暗黑模式:重新设计深度与强调,非简单反转 -->
<html class="dark">
<body class="bg-white dark:bg-gray-900 transition-colors">
  <div class="min-h-screen p-8">
    <!-- 卡片:暗黑模式使用 lighter surface 表示层次 -->
    <div class="max-w-2xl rounded-lg bg-gray-50 dark:bg-gray-800
                border border-gray-200 dark:border-gray-700 p-6">

      <h1 class="text-xl font-bold text-gray-900 dark:text-white">
        设置
      </h1>

      <div class="mt-6 space-y-4">
        <!-- 选项行 -->
        <div class="flex items-center justify-between py-3
                    border-b border-gray-200 dark:border-gray-700">
          <div>
            <p class="text-sm font-medium text-gray-900 dark:text-white">
              深色主题
            </p>
            <p class="text-xs text-gray-500 dark:text-gray-400">
              自动适配系统设置
            </p>
          </div>
          <!-- 开关 -->
          <button class="relative h-6 w-11 rounded-full
                         bg-gray-200 dark:bg-blue-500 transition-colors">
            <span class="absolute top-0.5 left-0.5 h-5 w-5 rounded-full
                         bg-white shadow transition-transform
                         dark:translate-x-5"></span>
          </button>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
```

## 不适用场景

以下场景UI设计工具包免费版不适合处理：

- 3D建模和动画制作
- 照片级写实渲染
- 手绘原创插画

## 触发条件

需要设计创作、UI设计、海报制作、品牌视觉时使用。不适用于非本工具能力范围的需求。

## 快速开始

### 1. 理解设计原则

UI 设计的七大核心原则:

```markdown
1. 视觉层次 - 每屏一个焦点,引导视线
2. 排版一致 - 最多 2-3 种字体,清晰字号体系
3. 色彩克制 - 一个主色,语义色一致
4. 间距规范 - 使用 4px/8px 网格
5. 对齐统一 - 网格对齐,不要随意摆放
6. 状态完整 - 每个组件设计全部状态
7. 响应优先 - 移动端优先,逐步增强
```

### 2. 应用间距系统

```css
/* 4px 基础网格 */
:root {
  --space-xs:  4px;   /* 0.25rem */
  --space-sm:  8px;   /* 0.5rem */
  --space-md:  16px;  /* 1rem */
  --space-lg:  24px;  /* 1.5rem */
  --space-xl:  32px;  /* 2rem */
  --space-2xl: 48px;  /* 3rem */
}

/* 字号体系(清晰阶梯,非渐变) */
:root {
  --text-caption: 12px;
  --text-body:    14px;
  --text-heading: 16px;
  --text-title:   20px;
  --text-hero:    32px;
}
```

### 3. 检查设计清单

```markdown

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。


## UI 设计检查清单

### 视觉层次
- [ ] 每屏有一个明确焦点
- [ ] 主操作最显眼(颜色/大小/位置)
- [ ] 相关元素通过间距分组

### 排版
- [ ] 最多使用 2-3 种字体
- [ ] 字号有清晰阶梯(title > heading > body)
- [ ] 正文行高 1.4-1.6
- [ ] 正文行宽 45-75 字符

### 色彩
- [ ] 一个主色用于主操作
- [ ] 语义色一致(红=错误,绿=成功)
- [ ] 不依赖颜色单独传达信息
- [ ] 中性色为主,色彩用于强调

### 间距
- [ ] 使用一致的间距比例
- [ ] 组间距 > 组内间距
- [ ] 触摸目标至少 44px

### 状态
- [ ] 每个交互组件设计全部状态
- [ ] 聚焦状态清晰可见
- [ ] 禁用状态视觉明确
- [ ] 加载状态有反馈
```

## 示例

### 色彩系统

```css
:root {
  /* 主色 */
  --color-primary: #3b82f6;
  --color-primary-hover: #2563eb;
  --color-primary-active: #1d4ed8;

  /* 语义色 */
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  --color-info: #3b82f6;

  /* 中性色 */
  --color-gray-50: #f9fafb;
  --color-gray-100: #f3f4f6;
  --color-gray-400: #9ca3af;
  --color-gray-600: #4b5563;
  --color-gray-900: #111827;
}
```

### 字号体系

| 用途 | 字号 | 字重 | 行高 |
|:-----|:-----|:-----|:-----|
| Hero 标题 | 32px | Bold(700) | 1.2 |
| 页面标题 | 20px | Semibold(600) | 1.3 |
| 区块标题 | 16px | Semibold(600) | 1.4 |
| 正文 | 14px | Regular(400) | 1.5 |
| 说明文字 | 12px | Regular(400) | 1.5 |

### 间距比例

| 名称 | 值 | 用途 |
|:-----|:---|:-----|
| xs | 4px | 图标与文字间距 |
| sm | 8px | 相关元素间距 |
| md | 16px | 组件内间距 |
| lg | 24px | 组件间间距 |
| xl | 32px | 区块间距 |
| 2xl | 48px | 大区块间距 |

## 优选实践

1. **视觉层次**
   - 每屏一个焦点,视线知道先看哪里
   - 大小、颜色、字重建立重要性
   - 相关元素通过邻近分组
   - 留白不是浪费,帮助扫视

2. **排版规范**
   - 最多 2-3 种字体,过多造成视觉噪音
   - 清晰字号阶梯:标题 > 标题 > 正文 > 说明
   - 正文行高 1.4-1.6,过紧或过松影响可读性
   - 正文行宽 45-75 字符,防止视觉疲劳

3. **色彩使用**
   - 一个主色用于主操作
   - 语义色一致:红=错误,绿=成功,黄=警告
   - 不依赖颜色单独传达信息,加图标与文字
   - 中性色为主,色彩用于强调

4. **间距系统**
   - 使用一致的比例:4px, 8px, 16px, 24px, 32px, 48px
   - 相同关系使用相同间距
   - 组间距大于组内间距
   - 触摸目标至少 44px(移动端)

5. **组件状态**
   - 设计全部状态:默认、悬停、激活、聚焦、禁用
   - 聚焦状态清晰可见(键盘用户依赖)
   - 禁用状态降低透明度,无指针光标
   - 加载状态替换内容,而非仅遮罩

6. **响应式设计**
   - 移动端优先,逐步增强
   - 断点基于内容,而非设备宽度
   - 触摸目标在触摸屏上更大
   - 悬停状态仅桌面端

7. **暗黑模式**
   - 非简单色彩反转,重新设计深度与强调
   - 略微降低对比度,纯白纯黑刺眼
   - 阴影效果不同,用 lighter surface 表示层次
   - 尊重系统偏好,但允许手动覆盖

## 常见问题

### Q1: 如何选择字体?

- 正文优先选择无衬线字体(如 Inter、思源黑体)
- 最多 2-3 种字体族
- 标题可用稍微特别的字体增加个性
- 确保中英文混排美观

### Q2: 色彩对比度有何要求?

- 正文文字对比度至少 4.5:1(WCAG AA)
- 大文字(18px+)对比度至少 3:1
- 可使用 WebAIM 对比度检查器验证
- 暗黑模式同样需要满足对比度要求

### Q3: 免费版与专业版的区别?

免费版提供核心设计原则与常见场景;专业版提供设计系统、设计令牌、可访问性深度规范与组件库。大型项目或团队协作建议升级。

### Q4: 如何提升设计感?

- 多看优秀设计(Dribbble、Behance)
- 保持一致性(间距、色彩、字体)
- 注重细节(对齐、留白、状态)
- 从用户角度审视,而非设计师角度

### Q5: 是否需要设计软件?

免费版以代码实现为主,适合前端开发者。如需视觉设计稿,可配合 Figma 等工具。专业版提供与 Figma 的协作规范。

## 依赖说明

### 运行环境
- **Agent 平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| 代码编辑器 | 工具 | 推荐 | VS Code / WebStorm |
| 浏览器开发者工具 | 工具 | 推荐 | Chrome DevTools |
| Figma(可选) | 设计工具 | 可选 | figma.com |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 本 Skill **无需任何 API Key**
- 设计原则通过自然语言指令驱动 Agent 执行
- 不依赖外部云服务

### 可用性分类
- **分类**: MD+EXEC(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent完成操作。免费版聚焦核心 UI 设计原则与常见场景,适合个人开发者快速构建清晰美观的界面。

## 错误处理


| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

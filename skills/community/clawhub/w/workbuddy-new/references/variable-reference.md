# WorkBuddy 皮肤可覆盖变量清单

WorkBuddy 基于 VS Code 内核，界面颜色全部由挂在 `:root`（`document.documentElement`）上的
CSS 变量驱动。皮肤通过一段带 `!important` 的 `<style>` 覆盖它们即可。

## 一、`--vscode-*` 变量（VS Code 稳定契约，跨版本不破）

### 编辑器 / 主区
- `--vscode-editor-background` / `--vscode-editor-foreground`
- `--vscode-editorWidget-background` / `--vscode-editorWidget-border`

### 侧边栏
- `--vscode-sideBar-background` / `--vscode-sideBar-foreground`
- `--vscode-sideBarSectionHeader-background`
- `--vscode-sideBarTitle-foreground`

### 活动栏（最左侧图标条）
- `--vscode-activityBar-background` / `--vscode-activityBar-foreground`
- `--vscode-activityBar-inactiveForeground`
- `--vscode-activityBarBadge-background` / `--vscode-activityBarBadge-foreground`

### 标题栏
- `--vscode-titleBar-activeBackground` / `--vscode-titleBar-activeForeground`
- `--vscode-titleBar-inactiveBackground` / `--vscode-titleBar-inactiveForeground`

### 状态栏（最底部）
- `--vscode-statusBar-background` / `--vscode-statusBar-foreground`
- `--vscode-statusBar-noFolderForeground`

### 标签页
- `--vscode-tab-activeBackground` / `--vscode-tab-inactiveBackground`
- `--vscode-tab-activeForeground` / `--vscode-tab-inactiveForeground`
- `--vscode-tab-unfocusedActiveForeground`
- `--vscode-tab-border`
- `--vscode-editorGroupHeader-tabsBackground` / `--vscode-editorGroupHeader-tabsBorder`

### 面板（底部/右侧输出区）
- `--vscode-panel-background` / `--vscode-panel-border`
- `--vscode-panelTitle-activeForeground` / `--vscode-panelTitle-inactiveForeground`

### 输入 / 下拉
- `--vscode-input-background` / `--vscode-input-foreground` / `--vscode-input-border`
- `--vscode-input-placeholderForeground`
- `--vscode-inputOption-activeBackground` / `--vscode-inputOption-activeBorder`
- `--vscode-dropdown-background` / `--vscode-dropdown-foreground` / `--vscode-dropdown-border`

### 按钮
- `--vscode-button-background` / `--vscode-button-hoverBackground` / `--vscode-button-foreground`
- `--vscode-button-secondaryBackground` / `--vscode-button-secondaryForeground` / `--vscode-button-secondaryHoverBackground`

### 列表（文件树 / 搜索结果等）
- `--vscode-list-activeSelectionBackground` / `--vscode-list-activeSelectionForeground`
- `--vscode-list-inactiveSelectionBackground` / `--vscode-list-inactiveSelectionForeground`
- `--vscode-list-hoverBackground` / `--vscode-list-hoverForeground`
- `--vscode-list-focusBackground` / `--vscode-list-focusForeground`
- `--vscode-list-highlightForeground` / `--vscode-list-focusOutline`

### 强调 / 焦点 / 阴影
- `--vscode-focusBorder` / `--vscode-contrastBorder` / `--vscode-widget-shadow`

### 链接 / 文本
- `--vscode-textLink-foreground` / `--vscode-textLink-activeForeground`
- `--vscode-textPreformat-foreground` / `--vscode-textSeparator-foreground`
- `--vscode-descriptionForeground` / `--vscode-icon-foreground`

### 徽标 / 滚动条
- `--vscode-badge-background` / `--vscode-badge-foreground`
- `--vscode-scrollbarSlider-background` / `--vscode-scrollbarSlider-hoverBackground` / `--vscode-scrollbarSlider-activeBackground`

### 菜单 / 浮层 / 杂项
- `--vscode-menu-background` / `--vscode-menu-foreground` / `--vscode-menu-selectionBackground` / `--vscode-menu-selectionForeground` / `--vscode-menu-separatorBackground`
- `--vscode-toolbar-hoverBackground`
- `--vscode-quickInput-background` / `--vscode-quickInput-foreground`
- `--vscode-notifications-background` / `--vscode-notifications-foreground`
- `--vscode-breadcrumb-background` / `--vscode-breadcrumb-foreground`

## 二、应用级设计变量（按钮 / 品牌色 / 描边，部分控件使用）
- `--accent-9` / `--accent-10` / `--accent-11` / `--accent-contrast`
- `--accent-surface` / `--accent-track`
- `--background` / `--color-background`
- `--color-badge`
- `--color-border-outline` / `--color-border-outline-variant`
- `--color-brand-active` / `--color-brand-hover`
- `--border-color` / `--border-active` / `--border-hover`

## 三、装饰背景
通过 `body::before`（fixed, `z-index:-9999`, `pointer-events:none`）叠加：
- 径向渐变光晕（`radial-gradient(circle at ...)`）
- 线性渐变底色（`linear-gradient(135deg, ...)`）
- 可选背景图（`url("file:///...")`）
- `@keyframes` 缓慢呼吸动画，并用 `@media (prefers-reduced-motion: reduce)` 关闭动画。

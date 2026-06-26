# [组件名称] 规格文档

**状态**: `draft`  
**创建日期**: YYYY-MM-DD  
**负责人**: [姓名]  

---

## 1. 组件概述

| 属性 | 值 |
|------|-----|
| 组件路径 | `@/components/xxx.tsx` |
| 组件类型 | 无状态/有状态 |
| 依赖组件 | |

---

## 2. Props 规格

```typescript
interface ComponentProps {
  // 必填 props
  title: string;           // 标题，最多 50 字符
  onSubmit: (data: FormData) => Promise<void>;
  
  // 可选 props
  variant?: 'default' | 'compact' | 'full';  // 默认 'default'
  disabled?: boolean;      // 默认 false
  className?: string;      // 额外样式类名
  
  // 事件回调
  onCancel?: () => void;
  onError?: (error: Error) => void;
}
```

### Props 详细说明

| Prop | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| title | string | 是 | - | 组件标题 |
| variant | enum | 否 | 'default' | 变体样式 |
| disabled | boolean | 否 | false | 禁用状态 |

---

## 3. 状态规格

### 3.1 内部状态

```typescript
type ComponentState = {
  isLoading: boolean;
  error: Error | null;
  // ...
};
```

### 3.2 状态流转

```
idle → loading → success
           ↓
         error
```

---

## 4. 行为规格

### 4.1 用户交互

| 操作 | 预期行为 |
|------|----------|
| 点击提交按钮 | 验证表单 → 调用 onSubmit → 显示加载状态 |
| 点击取消按钮 | 调用 onCancel → 关闭组件 |
| 表单验证失败 | 显示错误提示，不提交 |

### 4.2 自动行为

- 组件挂载时：
- 数据变化时：
- 组件卸载时：

---

## 5. UI 规格

### 5.1 布局结构

```
┌─────────────────────────┐
│  [Title]                │
├─────────────────────────┤
│  [Content Area]         │
│                         │
├─────────────────────────┤
│  [Cancel]  [Submit]     │
└─────────────────────────┘
```

### 5.2 响应式断点

| 断点 | 行为 |
|------|------|
| < 640px | 按钮垂直排列 |
| >= 640px | 按钮水平排列 |

### 5.3 状态样式

- **Loading**: 显示骨架屏/加载动画
- **Error**: 红色边框 + 错误提示
- **Disabled**: 灰色，不可点击

---

## 6. 可访问性 (A11y)

- [ ] 支持键盘导航
- [ ] 有适当的 aria 标签
- [ ] 错误信息可被屏幕阅读器读取
- [ ] 颜色对比度符合 WCAG AA

---

## 7. 测试用例

```typescript
// 单元测试
describe('Component', () => {
  it('renders correctly with required props');
  it('calls onSubmit when form is valid');
  it('shows error message on validation failure');
  it('handles loading state correctly');
});
```

---

## 8. 变更记录

| 日期 | 版本 | 变更内容 | 变更人 |
|------|------|----------|--------|
| | | | |

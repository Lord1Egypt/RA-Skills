# Reactive Resume 模板开发指南

## 概述

Reactive Resume 使用组件化模板系统，每个模板是一个 React 组件，支持自定义配置和样式。

## 模板结构

```
public/templates/[template-name]/
├── index.tsx          # 模板主组件（必需）
├── schema.ts          # 配置 schema（必需）
├── preview.jpg        # 预览图（必需）
└── components/        # 模板专用组件（可选）
```

## 创建新模板

### 步骤 1: 创建目录

```bash
mkdir -p public/templates/my-template
```

### 步骤 2: 实现模板组件

```tsx
// public/templates/my-template/index.tsx
import type { TemplateProps } from '@/types/template';
import { MyTemplateLayout } from './components/layout';
import { MyTemplateHeader } from './components/header';

export function MyTemplate({ resume, theme }: TemplateProps) {
  return (
    <div 
      className="template my-template"
      style={{ 
        fontFamily: theme.font,
        color: theme.text,
      }}
    >
      <MyTemplateHeader resume={resume} />
      <MyTemplateLayout resume={resume} />
    </div>
  );
}

// 模板元数据
export const templateConfig = {
  id: 'my-template',
  name: 'My Template',
  description: 'A clean professional template',
  sizes: ['A4', 'Letter'],
  theme: {
    primary: '#2563eb',
    secondary: '#64748b',
  },
};
```

### 步骤 3: 定义 Schema

```typescript
// public/templates/my-template/schema.ts
import { z } from 'zod';

export const myTemplateSchema = z.object({
  // 基础配置
  showPhoto: z.boolean().default(true),
  showSummary: z.boolean().default(true),
  
  // 布局选项
  layout: z.enum(['single-column', 'two-column']).default('two-column'),
  
  // 样式选项
  accentColor: z.string().default('#2563eb'),
  fontSize: z.number().min(10).max(16).default(12),
  
  // 自定义字段
  customFields: z.array(z.object({
    label: z.string(),
    value: z.string(),
  })).optional(),
});

export type MyTemplateOptions = z.infer<typeof myTemplateSchema>;
```

### 步骤 4: 创建预览图

生成模板的预览图（建议尺寸 800x1132）：

```bash
# 可以使用 Puppeteer 截图
pnpm screenshot my-template
```

或手动设计后保存到 `public/templates/my-template/preview.jpg`

### 步骤 5: 注册模板

在 `src/lib/templates.ts` 中添加：

```typescript
import { MyTemplate, templateConfig } from '@/templates/my-template';

export const templates = {
  // ... 现有模板
  'my-template': {
    component: MyTemplate,
    config: templateConfig,
  },
};
```

## 模板组件结构

### 典型组件层次

```
MyTemplate (index.tsx)
├── Header
│   ├── Profile Photo
│   ├── Name & Title
│   └── Contact Info
├── Main Content
│   ├── Summary
│   ├── Experience
│   ├── Education
│   ├── Skills
│   └── Projects
└── Sidebar (two-column layout)
    ├── Languages
    ├── Certifications
    └── References
```

### 示例：Experience 组件

```tsx
// components/experience.tsx
import type { Resume } from '@/types/resume';

interface ExperienceProps {
  resume: Resume;
  options: MyTemplateOptions;
}

export function Experience({ resume, options }: ExperienceProps) {
  return (
    <section className="experience">
      <h2 className="section-title">Experience</h2>
      <div className="experience-list">
        {resume.experience.map((exp) => (
          <div key={exp.id} className="experience-item">
            <div className="experience-header">
              <h3>{exp.position}</h3>
              <span className="company">{exp.company}</span>
            </div>
            <div className="experience-meta">
              <span>{exp.startDate} - {exp.endDate || 'Present'}</span>
              <span>{exp.location}</span>
            </div>
            {exp.summary && (
              <p className="experience-summary">{exp.summary}</p>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}
```

## 样式指南

### Tailwind CSS 类名约定

```tsx
// 使用语义化类名
<div className="template my-template">
  <header className="template-header">
  <main className="template-main">
  <aside className="template-sidebar">
  <section className="section experience">
  <div className="section-title">
}
```

### 响应式支持

```tsx
// A4 vs Letter 尺寸适配
<div className={cn(
  "template",
  size === 'A4' ? 'a4-size' : 'letter-size'
)}>
```

### 打印样式

```css
/* 确保 PDF 导出正确 */
@media print {
  .template {
    page-break-inside: avoid;
  }
  
  .section {
    break-inside: avoid;
  }
}
```

## 主题系统

### 使用主题变量

```tsx
import { useTheme } from '@/hooks/use-theme';

export function MyTemplate({ resume }: TemplateProps) {
  const theme = useTheme();
  
  return (
    <div style={{
      '--color-primary': theme.primary,
      '--color-secondary': theme.secondary,
      '--font-family': theme.font,
      '--font-size': theme.fontSize,
    }}>
      {/* 内容 */}
    </div>
  );
}
```

### 自定义主题选项

```typescript
// schema.ts
export const themeOptions = {
  colors: {
    primary: { type: 'color', default: '#2563eb' },
    secondary: { type: 'color', default: '#64748b' },
    text: { type: 'color', default: '#1e293b' },
  },
  fonts: {
    family: { 
      type: 'select', 
      options: ['Inter', 'Roboto', 'Merriweather'],
      default: 'Inter'
    },
    size: { type: 'range', min: 10, max: 16, default: 12 },
  },
  spacing: {
    sectionGap: { type: 'range', min: 16, max: 48, default: 24 },
  },
};
```

## 测试模板

### 本地测试

```bash
pnpm dev
# 访问 http://localhost:3000/editor
# 选择新模板，填写数据，预览效果
```

### PDF 导出测试

```bash
# 确保 Browserless 运行
sudo docker compose -f compose.dev.yml up -d browserless

# 在编辑器中点击 Export → PDF
# 检查导出的 PDF 格式是否正确
```

### 多尺寸测试

- 测试 A4 尺寸 (210mm x 297mm)
- 测试 Letter 尺寸 (8.5" x 11")
- 检查分页是否正确

## 模板最佳实践

### ✅ 推荐

- 保持简洁清晰的布局
- 使用语义化 HTML 标签
- 支持暗色模式
- 提供合理的默认配置
- 测试长内容溢出处理
- 确保 PDF 导出质量

### ❌ 避免

- 过于复杂的设计（影响可读性）
- 硬编码颜色和字体
- 忽略分页处理
- 不支持自定义配置
- 使用绝对定位

## 模板示例分析

### Azurill 模板（简洁单栏）

特点：
- 单栏布局，从上到下
- 适合内容较少的简历
- 强调简洁性

### Gengar 模板（现代双栏）

特点：
- 左侧边栏 + 主内容区
- 适合技术简历
- 技能可视化展示

### Pikachu 模板（创意设计）

特点：
- 彩色头部设计
- 适合创意行业
- 支持照片展示

## 调试技巧

### 常见问题

**Q: 模板在预览中正常，PDF 导出异常？**
A: 检查打印样式 (`@media print`)，确保没有使用 `position: fixed` 或 `overflow: hidden`。

**Q: 内容溢出页面？**
A: 使用 `break-inside: avoid` 防止内容被分页切断，或调整字体大小。

**Q: 自定义字体不显示？**
A: 确保字体在 `src/lib/fonts.ts` 中注册，并且 PDF 打印服务可访问。

## 发布模板

1. 完成模板开发和测试
2. 添加预览图
3. 更新文档
4. 提交 PR 到主仓库
5. 等待审核合并

---

*参考：现有模板位于 `public/templates/` 目录*

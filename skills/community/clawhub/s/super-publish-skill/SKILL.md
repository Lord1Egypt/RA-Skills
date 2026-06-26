# 组件规范

---

## 一、文件组织

```
client/src/
├── components/          # 业务组件
│   ├── ui/              # shadcn/ui 基础组件（勿手动修改）
│   └── *.tsx            # 业务组件
├── pages/               # 页面组件
├── hooks/               # 自定义 Hooks
├── contexts/            # React Context
├── constants/           # 常量定义
├── lib/                 # 工具函数
└── index.css            # 全局样式与设计系统
```

---

## 二、组件结构模板

```tsx
import { useState } from 'react';

import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';

interface MyComponentProps {
  title: string;
  variant?: 'default' | 'compact';
  className?: string;
}

export default function MyComponent({ title, variant = 'default', className }: MyComponentProps) {
  const [isActive, setIsActive] = useState(false);

  return (
    <section className={cn("section-container py-20", className)}>
      <div className="glass-card p-8 rounded-2xl">
        <h2 className="font-heading text-2xl font-bold tracking-tight text-foreground mb-4">
          {title}
        </h2>
        <p className="text-[15px] text-muted-foreground leading-relaxed">
          描述文本
        </p>
        <Button
          onClick={() => setIsActive(!isActive)}
          className={cn(
            "mt-6",
            isActive && "bg-primary/90"
          )}
        >
          操作按钮
        </Button>
      </div>
    </section>
  );
}
```

---

## 三、导入规范

```tsx
// 1. React 相关（最先导入）
import { useEffect, useRef, useState } from 'react';

// 2. 第三方库
import { AnimatePresence, motion } from 'framer-motion';
import { Search, Star, ChevronRight } from 'lucide-react';

// 3. 项目工具/库（使用路径别名）
import { cn } from '@/lib/utils';

// 4. 项目组件
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent } from '@/components/ui/dialog';

// 5. 项目 Hooks/Context/Constants
import { useSkills } from '@/hooks/useSkills';
import { SECTION_IDS } from '@/constants/section-ids';

// 6. 类型（如果独立导入）
import type { Skill } from '@shared/types';
```

---

## 四、TypeScript 规范

- 所有组件使用 TypeScript（`.tsx`）
- 组件 Props 必须定义 `interface`，以 `Props` 为后缀，如 `MyComponentProps`
- 禁止使用 `any` 类型，使用 `unknown` 或具体类型替代
- 导出风格：页面组件使用 `export default`，UI/工具组件使用命名导出 `export function`

---

## 五、命名规范

| 类别 | 命名风格 | 示例 |
|------|---------|------|
| 组件文件 | PascalCase | `HeroSection.tsx`, `SkillDetailModal.tsx` |
| 页面文件 | PascalCase | `TopSkills.tsx`, `About.tsx` |
| Hook 文件 | camelCase，`use` 前缀 | `useSkills.ts`, `useMobile.tsx` |
| 常量文件 | kebab-case | `section-ids.ts` |
| CSS 类名 | kebab-case | `glass-card`, `section-eyebrow` |
| 组件名 | PascalCase | `HeroSection`, `RankingTable` |
| 函数/变量 | camelCase | `handleClick`, `isVisible` |
| 常量 | UPPER_SNAKE_CASE | `SECTION_IDS`, `MAX_ITEMS` |
| 接口/类型 | PascalCase | `SkillDetailProps`, `CategoryData` |

---

## 六、注释规范

- 组件文件顶部添加简要说明注释
- 复杂业务逻辑添加中文注释
- 注释语言：中文
- 格式：
  ```tsx
  /**
   * HeroSection — 首页顶部英雄区域
   * 包含标题、副标题、CTA 按钮和安装指南卡片
   */
  export default function HeroSection() { ... }
  ```

---

## 七、组件体积控制

### 7.1 单文件行数限制

- **单个组件文件建议不超过 300 行**（约 10KB），超过时应按职责拆分为子组件
- 页面级组件可适当放宽至 400 行，但应积极拆分

### 7.2 文件夹组件结构

当一个组件需要拆分出子组件时，使用文件夹组织：

```
components/
├── HeroSection/
│   ├── index.tsx              ← 主组件入口
│   ├── HeroTitle.tsx          ← 子组件
│   ├── HeroActions.tsx        ← 子组件
│   └── HeroBackground.tsx     ← 子组件
├── SkillCard.tsx              ← 不需要拆分的组件保持单文件
```

### 7.3 拆分原则

- 可独立复用的 UI 片段应抽取为子组件
- 组件之间**尽量不要相互依赖**，使用 Props 传递数据
- 跨层级数据传递（超过 3 层 Props）时使用 React Context

---

## 八、禁止 Class 组件

- 所有组件**必须**使用函数式组件 + React Hooks
- 禁止使用 `class extends React.Component` 或 `class extends Component`
- **唯一例外**：`ErrorBoundary`（React 官方要求 Error Boundary 必须使用 class 组件）

```tsx
// ✅ 正确：函数式组件
export default function MyComponent({ title }: MyComponentProps) {
  const [count, setCount] = useState(0);
  return <div>{title}: {count}</div>;
}

// ❌ 禁止：class 组件
class MyComponent extends React.Component {
  render() { return <div>{this.props.title}</div>; }
}
```
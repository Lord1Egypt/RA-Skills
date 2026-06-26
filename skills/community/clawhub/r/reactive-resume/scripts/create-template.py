#!/usr/bin/env python3
"""
Reactive Resume 模板创建工具

快速创建标准结构的模板目录和文件模板。

用法:
    python create-template.py <template-name> [--path <output-dir>]

示例:
    python create-template.py professional
    python create-template.py modern --path public/templates
"""

import os
import sys
import argparse
from datetime import datetime

# 模板组件内容
INDEX_TEMPLATE = """import type {{ TemplateProps }} from '@/types/template';

export function {pascal_name}Template({{ resume, theme }}: TemplateProps) {{
  return (
    <div 
      className="template {snake_name}"
      style={{ 
        fontFamily: theme.font,
        color: theme.text,
      }}
    >
      <header className="template-header">
        <h1>{{{{ resume.basics.name }}}}</h1>
        <p>{{{{ resume.basics.headline }}}}</p>
      </header>

      <main className="template-main">
        {{{{ /* 添加简历内容区域 */}}}}
        <section className="section summary">
          <h2>Summary</h2>
          <p>{{{{ resume.basics.summary }}}}</p>
        </section>

        <section className="section experience">
          <h2>Experience</h2>
          {{{{ resume.work.map((work) => (
            <div key={{work.id}} className="experience-item">
              <h3>{{{{ work.position }}}}</h3>
              <span>{{{{ work.company }}}}</span>
              <p>{{{{ work.summary }}}}</p>
            </div>
          )) }}}}
        </section>

        <section className="section education">
          <h2>Education</h2>
          {{{{ resume.education.map((edu) => (
            <div key={{edu.id}} className="education-item">
              <h3>{{{{ edu.institution }}}}</h3>
              <span>{{{{ edu.area }}}}, {{{{ edu.studyType }}}}</span>
            </div>
          )) }}}}
        </section>
      </main>
    </div>
  );
}}

export const templateConfig = {{
  id: '{snake_name}',
  name: '{display_name}',
  description: 'A clean and professional template',
  sizes: ['A4', 'Letter'] as const,
  theme: {{
    primary: '#2563eb',
    secondary: '#64748b',
  }},
}};
"""

# Schema 内容
SCHEMA_TEMPLATE = """import {{ z }} from 'zod';

export const {snake_name}Schema = z.object({{
  // 基础配置
  showPhoto: z.boolean().default(true),
  showSummary: z.boolean().default(true),
  
  // 布局选项
  layout: z.enum(['single-column', 'two-column']).default('two-column'),
  
  // 样式选项
  accentColor: z.string().default('#2563eb'),
  fontSize: z.number().min(10).max(16).default(12),
  
  // 自定义字段
  customFields: z.array(z.object({{
    label: z.string(),
    value: z.string(),
  }})).optional(),
}});

export type {pascal_name}Options = z.infer<typeof {snake_name}Schema>;
"""

# 预览图占位符
PREVIEW_PLACEHOLDER = """<!-- 
预览图说明：
1. 尺寸建议：800x1132 像素
2. 格式：JPG 或 PNG
3. 内容：模板的完整预览效果

生成方法：
- 在编辑器中选择此模板
- 填写示例数据
- 使用截图工具生成预览图
- 保存为 preview.jpg 覆盖此文件
-->
"""

def create_template(template_name: str, output_path: str):
    """创建模板目录结构"""
    
    # 转换为不同命名格式
    snake_name = template_name.lower().replace('-', '_')
    pascal_name = ''.join(word.capitalize() for word in snake_name.split('_'))
    display_name = ' '.join(word.capitalize() for word in snake_name.split('_'))
    
    # 创建目录
    template_dir = os.path.join(output_path, snake_name)
    os.makedirs(template_dir, exist_ok=True)
    
    # 创建 components 子目录
    components_dir = os.path.join(template_dir, 'components')
    os.makedirs(components_dir, exist_ok=True)
    
    # 创建文件
    files = {
        'index.tsx': INDEX_TEMPLATE.format(
            pascal_name=pascal_name,
            snake_name=snake_name,
            display_name=display_name
        ),
        'schema.ts': SCHEMA_TEMPLATE.format(
            pascal_name=pascal_name,
            snake_name=snake_name
        ),
        'preview.jpg': PREVIEW_PLACEHOLDER,
        'components/layout.tsx': f'// {pascal_name} 布局组件\nexport function {pascal_name}Layout() {{\n  return null;\n}}\n',
        'components/header.tsx': f'// {pascal_name} 头部组件\nexport function {pascal_name}Header() {{\n  return null;\n}}\n',
    }
    
    for filename, content in files.items():
        filepath = os.path.join(template_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Created: {filepath}")
    
    # 创建 README
    readme_path = os.path.join(template_dir, 'README.md')
    readme_content = f"""# {display_name} 模板

## 开发说明

### 文件结构
- `index.tsx` - 模板主组件
- `schema.ts` - 配置 schema 定义
- `preview.jpg` - 模板预览图
- `components/` - 模板专用组件

### 开发步骤
1. 编辑 `index.tsx` 实现模板布局
2. 在 `schema.ts` 中定义可配置选项
3. 生成预览图（800x1132）
4. 在 `src/lib/templates.ts` 中注册模板
5. 测试 PDF 导出

### 测试
```bash
pnpm dev
# 访问 http://localhost:3000/editor
# 选择 {display_name} 模板
```

*Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"✓ Created: {readme_path}")
    
    print(f"\n✅ Template '{template_name}' created successfully at {template_dir}")
    print("\nNext steps:")
    print("1. Edit index.tsx to implement the template layout")
    print("2. Update schema.ts with custom options")
    print("3. Generate a preview image (800x1132)")
    print("4. Register the template in src/lib/templates.ts")
    print("5. Test PDF export in the editor")

def main():
    parser = argparse.ArgumentParser(description='Create a Reactive Resume template')
    parser.add_argument('template_name', help='Name of the template (e.g., professional)')
    parser.add_argument('--path', default='public/templates', help='Output directory (default: public/templates)')
    
    args = parser.parse_args()
    
    # 确保输出目录存在
    os.makedirs(args.path, exist_ok=True)
    
    create_template(args.template_name, args.path)

if __name__ == '__main__':
    main()

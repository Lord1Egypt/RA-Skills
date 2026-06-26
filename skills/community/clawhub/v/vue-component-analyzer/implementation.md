# Vue 组件分析实现指南

## 分析步骤

### 步骤 1：定位入口文件

```javascript
// 可能的入口文件
const entryFiles = [
  'src/main.js',
  'src/main.ts',
  'src/app.js',
  'src/app.ts',
  'main.js',
  'main.ts'
]

// 读取入口文件，找到根组件导入
// 通常形式：import App from './App.vue'
```

### 步骤 2：解析 Vue 单文件组件

```javascript
// 解析 .vue 文件结构
const parseVueFile = (filePath) => {
  const content = fs.readFileSync(filePath, 'utf-8')
  
  // 提取 template 部分
  const templateMatch = content.match(/<template>([\s\S]*?)<\/template>/)
  const template = templateMatch ? templateMatch[1] : ''
  
  // 提取 script 部分
  const scriptMatch = content.match(/<script[^>]*>([\s\S]*?)<\/script>/)
  const script = scriptMatch ? scriptMatch[1] : ''
  
  return { template, script }
}
```

### 步骤 3：识别组件引用

#### Vue 3 `<script setup>` 方式
```javascript
// 识别导入的组件
const importRegex = /import\s+(\w+)\s+from\s+['"]([^'"]+)['"]/g
// 匹配：import ComponentName from './path'

// 识别 template 中使用的组件
// 通过解析 template 中的标签名，与导入的组件名匹配
```

#### Vue 2 / Options API 方式
```javascript
// 识别 components 选项
const componentsRegex = /components:\s*\{([^}]+)\}/
// 匹配：components: { ComponentName }

// 识别 import 语句（同上）
```

### 步骤 4：提取 Props 定义

```javascript
// 数组形式：props: ['prop1', 'prop2']
const arrayPropsRegex = /props:\s*\[([^\]]+)\]/

// 对象形式
const objectPropsRegex = /props:\s*\{([^}]+)\}/

// defineProps (Vue 3)
const definePropsRegex = /defineProps\(([^)]+)\)/

// 解析每个 prop 的详细信息
const parseProp = (propString) => {
  // 提取名称、类型、required、default
}
```

### 步骤 5：递归分析

```javascript
const analyzeComponent = (filePath, visited = new Set()) => {
  // 防止循环依赖
  if (visited.has(filePath)) {
    return { circular: true, path: filePath }
  }
  visited.add(filePath)
  
  const { template, script } = parseVueFile(filePath)
  const imports = extractImports(script)
  const usedComponents = extractUsedComponents(template, imports)
  const props = extractProps(script)
  
  const children = usedComponents.map(comp => {
    const childPath = resolvePath(comp.path, filePath)
    return analyzeComponent(childPath, new Set(visited))
  })
  
  return {
    name: extractComponentName(script, filePath),
    path: filePath,
    props,
    children
  }
}
```

### 步骤 6：路径解析

```javascript
// 处理别名路径
const resolvePath = (importPath, currentFile) => {
  // @/components/Foo -> src/components/Foo.vue
  // ./Foo -> relative to current file
  // ../Foo -> relative to parent
  
  if (importPath.startsWith('@/')) {
    return importPath.replace('@/', 'src/') + '.vue'
  }
  
  if (importPath.startsWith('./') || importPath.startsWith('../')) {
    return path.resolve(path.dirname(currentFile), importPath) + '.vue'
  }
  
  return importPath
}
```

## 输出生成

### Markdown 树形
```javascript
const generateMarkdown = (tree, level = 0) => {
  const indent = '│   '.repeat(level)
  const prefix = level === 0 ? '📦' : (level === 1 ? '├──' : '│   └──')
  
  let result = `${indent}${prefix} ${tree.name} (${tree.path})\n`
  
  if (tree.props && tree.props.length > 0) {
    const propsStr = tree.props.map(p => {
      let str = `${p.name}(${p.type})`
      if (p.required) str += ', required'
      if (p.default !== undefined) str += `, default: ${p.default}`
      return str
    }).join(', ')
    result += `${indent}│   └── props: ${propsStr}\n`
  }
  
  if (tree.children) {
    tree.children.forEach(child => {
      result += generateMarkdown(child, level + 1)
    })
  }
  
  return result
}
```

### Mermaid 图表
```javascript
const generateMermaid = (tree, nodes = [], edges = []) => {
  const nodeId = tree.name.replace(/[^a-zA-Z0-9]/g, '_')
  nodes.push(`${nodeId}[${tree.name}<br/>${tree.path}]`)
  
  if (tree.children) {
    tree.children.forEach(child => {
      const childId = child.name.replace(/[^a-zA-Z0-9]/g, '_')
      edges.push(`${nodeId} --> ${childId}`)
      generateMermaid(child, nodes, edges)
    })
  }
  
  return `graph TD\n    ${[...nodes, ...edges].join('\n    ')}`
}
```

## 边界情况处理

1. **第三方组件**：路径包含 node_modules 或已知名称（如 ElButton）时跳过
2. **动态组件**：`<component :is="dynamicComponent">` 标记为动态
3. **递归组件**：组件引用自身时标记为 recursive
4. **未找到文件**：组件路径无法解析时标记为 missing
5. **TypeScript**：支持 .vue 文件中的 TS 类型定义解析

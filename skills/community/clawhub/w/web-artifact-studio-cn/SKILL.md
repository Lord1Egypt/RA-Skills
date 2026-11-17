---
slug: web-artifact-studio-cn
name: web-artifact-studio
version: 1.0.1
description: "Web交互式工件制作工具，提供数据仪表盘，表单工作流，单页应用与交互式演示构建功能。支持组件展示，状态管理，路由配置与技术选型。适用于产品原型验证，数据可视化展示，内部工具开发等前端工件生产场景。涵盖项目搭建，交付模式选择，TypeScript类型安全等工程化能力。内置React 18与shadcn/ui组件库，含Tailwind样式，响应式布局，无障碍适配。"
category: Development
license: MIT
tags:
  - Web工件
  - 数据仪表盘
  - React组件
  - 表单工作流
  - 单页应用
  - 交互式演示
  - TypeScript
tools:
  - Read
  - Write
  - Edit
summary: "Web构件工作室，支持数据仪表盘与表单工作流和单页应用生成。Web交互式工件制作工具，提供数据仪表盘，表单工作流，单页应用与交互式演示构建功能。支持组件展示，状态管理，路由配置与技术选型。适"
displayName: "Web构件工作室"
pricing_tier: "L2-标准级"
---
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

|---|
| 交互式演示 | 演示需求 + 交互逻辑 | React 应用 + 事件处理 + 可点击演示 |
| 数据仪表盘 | 数据源 + 图表需求 + 过滤器 | 状态管理仪表盘 + 图表 + 交互筛选 |
| 表单工作流 | 表单字段 + 校验规则 + 分步 | 多步表单 + 路由 + 状态校验 |
| 组件展示 | 设计系统/组件库 | shadcn/ui 组件预览 + 代码示例 |
| 单页应用原型 | 页面结构 + 路由 | SPA + 路由 + 状态 + 持久化 |
**不适用于**:
- 简单单文件 HTML(无状态/无路由,直接写 HTML 即可)
- 完整生产级 Web 应用(需要后端、数据库、认证等,使用 Next.js/Nuxt)
- 移动端原生 App(使用 React Native/Flutter)
- 桌面应用(使用 Electron/Tauri)
- 静态文档站点(使用 VitePress/Docusaurus)
- 大型电商网站(需要完整架构,非单工件)
## 操作步骤
### Step 1: 需求分析
1. **明确工件目标**:展示什么?交互什么?数据从哪来?
2. **复杂度评估**:
   - 简单展示 → 单文件 HTML 即可
   - 需要状态/路由/多组件 → 使用本工作室
3. **技术选型确认**:React 18 + TypeScript + Tailwind + shadcn/ui
4. **交付模式选择**:Vite 多文件 / 单 HTML 文件(内联)
### Step 2: 项目搭建
1. **目录结构**:
## 参数说明
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | Web工件工作室处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |
   ```
   artifact/
   ├── index.html          # 入口
   ├── src/
   │   ├── main.tsx        # 挂载点
   │   ├── App.tsx         # 根组件
   │   ├── components/      # 业务组件
   │   ├── ui/              # shadcn/ui 组件
   │   ├── hooks/           # 自定义 Hook
   │   ├── lib/             # 工具函数
   │   └── styles/          # 全局样式
   └── package.json
   ```
2. **依赖引入**:React、Tailwind、shadcn/ui、按需引入图表/路由库
3. **构建配置**:Vite 或内联打包
### Step 3: 组件设计
1. **组件拆分**:按职责拆分,单一职责
2. **shadcn/ui 组合**:优先使用 shadcn/ui 组件(Button/Card/Dialog/Table 等)
3. **状态管理**:
   - 局部状态:useState
   - 跨组件:Context 或 Zustand
   - 持久化:localStorage
4. **路由**:React Router(如需多页面)
### Step 4: 样式与交互
1. **Tailwind 优先**:用工具类,少写自定义 CSS
2. **响应式**:移动优先,sm/md/lg/xl 断点
3. **无障碍**:语义化 HTML、ARIA 标签、键盘导航
4. **动效**:CSS transition / Framer Motion(按需)
### Step 5: 打包与交付
1. **构建产物**:单 HTML 文件(内联 JS/CSS)或多文件
2. **资源处理**:图片转 base64 或 CDN
3. **可移植性**:确保工件可独立运行,无外部依赖
4. **验证**:在浏览器中打开测试,确认功能正常
## 设计原则
1. **组件化**:一切皆组件,可复用可组合
2. **类型安全**:TypeScript,props 有类型定义
3. **无障碍优先**:WCAG 2.1 AA 合规
4. **性能考虑**:懒加载、虚拟列表(长数据)
5. **避免过度工程**:工件不是产品,够用即可
## 示例展示
### 示例1: 数据仪表盘工件(输入→输出)
**输入**:
```
需求: 销售数据仪表盘
数据: JSON 数组(产品/销售额/地区/月份)
功能: 1) 柱状图展示月度销售 2) 表格展示明细 3) 筛选器按地区过滤
交付: 单 HTML 文件
```
**输出**(目录结构 + 关键代码):
```
artifact/
├── index.html
├── src/
│   ├── main.tsx
│   ├── App.tsx              # 主组件 + 状态
│   ├── components/
│   │   ├── SalesChart.tsx   # 图表组件
│   │   ├── DataTable.tsx    # 表格组件
│   │   └── RegionFilter.tsx # 筛选器
│   └── data/sales.json      # 模拟数据
└── package.json
tsx
// App.tsx 核心代码
import { useState, useMemo } from 'react';
import { Card, CardHeader, CardContent } from '@/ui/card';
import { Select, SelectContent, SelectItem } from '@/ui/select';
import { SalesChart } from './components/SalesChart';
import { DataTable } from './components/DataTable';
import salesData from './data/sales.json';
export default function App() {
  const [region, setRegion] = useState<string>('all');
  const filteredData = useMemo(() => {
    if (region === 'all') return salesData;
    return salesData.filter(item => item.region === region);
  }, [region]);
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">销售数据仪表盘</h1>
      <Select value={region} onValueChange={setRegion}>
        <SelectContent>
          <SelectItem value="all">全部地区</SelectItem>
          <SelectItem value="华东">华东</SelectItem>
          <SelectItem value="华北">华北</SelectItem>
        </SelectContent>
      </Select>
      <Card>
        <CardHeader>月度销售趋势</CardHeader>
        <CardContent>
          <SalesChart data={filteredData} />
        </CardContent>
      </Card>
      <Card>
        <CardHeader>销售明细</CardHeader>
        <CardContent>
          <DataTable data={filteredData} />
        </CardContent>
      </Card>
    </div>
  );
}
```
### 示例2: 多步表单工件(输入→输出)
**输入**:
```
需求: 用户注册多步表单
步骤: 1)基本信息 2)联系方式 3)确认提交
校验: 必填、邮箱格式、手机号格式
交付: 单 HTML 文件 + 状态持久化(localStorage)
```
**输出**(关键代码):
```tsx
// MultiStepForm.tsx
import { useState } from 'react';
import { Button } from '@/ui/button';
import { Input } from '@/ui/input';
import { Label } from '@/ui/label';
const STEPS = ['基本信息', '联系方式', '确认提交'];
export function MultiStepForm() {
  const [step, setStep] = useState(0);
  const [formData, setFormData] = useState(() => {
    const saved = localStorage.getItem('form-data');
    return saved ? JSON.parse(saved) : { name: '', email: '', phone: '' };
  });
  const updateField = (field: string, value: string) => {
    const newData = { ...formData, [field]: value };
    setFormData(newData);
    localStorage.setItem('form-data', JSON.stringify(newData));
  };
  const next = () => step < STEPS.length - 1 && setStep(step + 1);
  const prev = () => step > 0 && setStep(step - 1);
  return (
    <div className="max-w-md mx-auto p-6">
      <div className="flex gap-2 mb-6">
        {STEPS.map((s, i) => (
          <div key={i} className={`flex-1 h-2 rounded ${i <= step ? 'bg-blue-500' : 'bg-gray-200'}`} />
        ))}
      </div>
      <h2 className="text-xl font-bold mb-4">{STEPS[step]}</h2>
      {step === 0 && (
        <div className="space-y-4">
          <div>
            <Label>姓名</Label>
            <Input value={formData.name} onChange={e => updateField('name', e.target.value)} />
          </div>
      )}
      {step === 1 && (
        <div className="space-y-4">
          <div>
            <Label>邮箱</Label>
            <Input type="email" value={formData.email} onChange={e => updateField('email', e.target.value)} />
          </div>
          <div>
            <Label>手机号</Label>
phone} onChange={e => updateField('phone', e.target.value)} />
          </div>
      )}
      {step === 2 && (
        <div className="space-y-2">
          <p>姓名: {formData.name}</p>
          <p>邮箱: {formData.email}</p>
          <p>手机: {formData.phone}</p>
        </div>
      )}
      <div className="flex justify-between mt-6">
        <Button variant="outline" onClick={prev} disabled={step === 0}>上一步</Button>
        {step < STEPS.length - 1 ? (
          <Button onClick={next}>下一步</Button>
        ) : (
          <Button onClick={() => alert('提交成功!')}>提交</Button>
        )}
      </div>
  );
}
```
### 示例3: 单文件交付构建(输入→输出)
**输入**:
```
需求: 将 React 工件打包为单 HTML 文件,无外部依赖
工具: Vite + vite-plugin-singlefile
```
**输出**(配置代码):
```javascript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { viteSingleFile } from 'vite-plugin-singlefile';
// ...
export default defineConfig({
  plugins: [react(), viteSingleFile()],
  build: {
    target: 'esnext',
    assetsInlineLimit: 100000000, // 100MB,内联所有资源
    cssCodeSplit: false,
    rollupOptions: {
      output: {
        inlineDynamicImports: true,
      },
});
bash
npm run build
```
## 异常处理指引
| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| Node.js 未安装 | 环境缺少 Node.js | 提示安装 Node.js 18+,提供下载链接 |
| npm install 失败 | 网络问题或权限 | 切换国内镜像 `npm config set registry https://registry.npmmirror.com` |
| shadcn/ui 组件缺失 | 未通过 CLI 添加 | 使用 `npx shadcn-ui@latest add button card dialog` 添加 |
| TypeScript 编译错误 | 类型不匹配 | 检查 props 类型定义,使用 `tsc --noEmit` 校验 |
| Vite 构建失败 | 配置错误或依赖冲突 | 检查 vite.config.ts,清理 node_modules 重装 |
| 单文件打包体积过大 | 内联资源过多 | 使用 CDN 加载 React/Tailwind,仅内联业务代码 |
| Tailwind 样式不生效 | 配置错误或 purge 误删 | 检查 tailwind.config.js content 路径 |
| localStorage 数据丢失 | 浏览器隐私模式 | 添加 try-catch,降级为内存状态 |
| 图表库未引入 | 缺少 recharts/echarts | `npm install recharts` 或使用 SVG 手绘 |
| 路由 404 | 直接打开 HTML 文件路由失效 | 使用 HashRouter 替代 BrowserRouter |
## 运行环境
### 运行环境
- **Agent平台**: Claude Code / Cursor / Codex / Gemini CLI / Windsurf 等支持SKILL.md的任意Agent
- **操作系统**: Windows / macOS / Linux
- **运行时**: Node.js 18+ + npm/pnpm
### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 | 国内替代 |
|:---:|:---:|:---:|:---:|:---:|
| Node.js 18+ | 运行时 | 必需 | nodejs.org | npmmirror 国内镜像 |
| React 18 | 库 | 必需 | `npm install react react-dom` | npmmirror |
| TypeScript | 库 | 必需 | `npm install -D typescript` | npmmirror |
| Tailwind CSS | 库 | 必需 | `npm install -D tailwindcss` | npmmirror |
| shadcn/ui | 库 | 必需 | `npx shadcn-ui@latest init` | npmmirror |
| Vite | 工具 | 必需 | `npm install -D vite` | npmmirror |
| React Router | 库 | 可选(多页面) | `npm install react-router-dom` | npmmirror |
| Recharts | 库 | 可选(图表) | `npm install recharts` | npmmirror |
| LLM API | API | 必需 | Agent 内置 LLM | 通义/文心/智谱 |
### API Key 配置
- **本Skill无需额外API Key配置**
- **安全要求**:
  - 工件中不硬编码任何 API Key 或敏感凭证
  - 如需调用外部 API,通过环境变量注入(VITE_ 前缀)
  - 构建产物中不包含 .env 文件
### 可用性分类
- **分类**: MD+EXEC
- **说明**: 纯Markdown方法论,需 exec 能力运行 npm/Vite 命令
## 案例展示
以下案例展示了skill的工作流程和预期输出效果，由LLM按照skill定义的流程生成。
### 案例1: 销售数据仪表盘(Zustand全局状态+Recharts图表+筛选器)
**输入**:
```
需求: 销售数据仪表盘工件
数据: JSON数组(产品/销售额/地区/月份/同比增长)
功能:
  1) 柱状图展示月度销售趋势
  2) 数据表格展示明细(支持排序)
  3) 地区筛选器+产品筛选器联动
  4) KPI卡片展示总销售额/平均增长率/最高地区
交付: 单HTML文件(Vite打包)
```
**LLM生成输出** (`output/sales-dashboard/src/App.tsx`):
```tsx
import { useState, useMemo } from 'react';
import { create } from 'zustand';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { Card, CardHeader, CardContent, CardTitle } from '@/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/ui/select';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/ui/table';
// Zustand 全局状态
interface DashboardStore {
  region: string;
  product: string;
  setRegion: (r: string) => void;
  setProduct: (p: string) => void;
}
const useDashboardStore = create<DashboardStore>((set) => ({
  region: 'all',
  product: 'all',
  setRegion: (r) => set({ region: r }),
  setProduct: (p) => set({ product: p }),
}));
// KPI 卡片组件
function KPICard({ title, value, subtitle }: { title: string; value: string; subtitle: string }) {
  return (
    <Card>
      <CardHeader><CardTitle className="text-sm text-gray-500">{title}</CardTitle></CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        <div className="text-xs text-gray-400 mt-1">{subtitle}</div>
      </CardContent>
    </Card>
  );
}
export default function App() {
  const { region, product, setRegion, setProduct } = useDashboardStore();
  const filteredData = useMemo(() => {
      (region === 'all' || item.region === region) &&
      (product === 'all' || item.product === product)
    );
  }, [region, product]);
  // KPI 计算
  const totalSales = filteredData.reduce((sum, d) => sum + d.amount, 0);
  const avgGrowth = filteredData.length > 0
    ? (filteredData.growthRate, 0) / filteredData.length).toFixed(1)
    : '0';
  const topRegion = useMemo(() => {
    const regionMap: Record<string, number> = {};
    filteredData.forEach(d => { regionMap[d.region] = (regionMap[d.region] || 0) + d.amount; });
    return Object.entries(regionMap).sort((a, b) => b[1] - a[1])[0]?.[0] || '-';
  }, [filteredData]);
  // 图表数据(按月份聚合)
  const chartData = useMemo(() => {
    const monthMap: Record<string, number> = {};
    filteredData.forEach(d => { monthMap[d.month] = (monthMap[d.month] || 0) + d.amount; });
    return Object.entries(monthMap).map(([month, amount]) => ({ month, amount }));
  }, [filteredData]);
  return (
    <div className="p-6 space-y-6 max-w-6xl mx-auto">
      <h1 className="text-2xl font-bold">销售数据仪表盘</h1>
      {/* KPI 卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <KPICard title="总销售额" value={`¥${totalSales.toLocaleString()}`} subtitle={`${filteredData.length} 条记录`} />
        <KPICard title="平均增长率" value={`${avgGrowth}%`} subtitle="同比" />
        <KPICard title="最高地区" value={topRegion} subtitle="按销售额" />
      </div>
      {/* 筛选器 */}
      <div className="flex gap-4">
        <Select value={region} onValueChange={setRegion}>
          <SelectTrigger className="w-40"><SelectValue 示例值="选择地区" /></SelectTrigger>
          <SelectContent>
            <SelectItem value="all">全部地区</SelectItem>
            <SelectItem value="华东">华东</SelectItem>
            <SelectItem value="华北">华北</SelectItem>
            <SelectItem value="华南">华南</SelectItem>
          </SelectContent>
        </Select>
        <Select value={product} onValueChange={setProduct}>
          <SelectTrigger className="w-40"><SelectValue 示例值="选择产品" /></SelectTrigger>
          <SelectContent>
            <SelectItem value="all">全部产品</SelectItem>
            <SelectItem value="产品A">产品A</SelectItem>
            <SelectItem value="产品B">产品B</SelectItem>
            <SelectItem value="产品C">产品C</SelectItem>
          </SelectContent>
        </Select>
      </div>
      {/* 图表 */}
      <Card>
        <CardHeader><CardTitle>月度销售趋势</CardTitle></CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip formatter={(v: number) => `¥${v.toLocaleString()}`} />
              <Bar dataKey="amount" fill="#1a56db" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
      {/* 数据表格 */}
      <Card>
        <CardHeader><CardTitle>销售明细</CardTitle></CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>产品</TableHead>
                <TableHead>地区</TableHead>
                <TableHead>月份</TableHead>
                <TableHead className="text-right">销售额</TableHead>
                <TableHead className="text-right">增长率</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredData.map((item, i) => (
                <TableRow key={i}>
                  <TableCell>{item.product}</TableCell>
                  <TableCell className="text-right">¥{item.amount.toLocaleString()}</TableCell>
                  <TableCell className={`text-right ${item.growthRate >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {item.growthRate >= 0 ? '+' : ''}{item.growthRate}%
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
```
**效果验证**: ✓Zustand全局状态管理(地区+产品双筛选器) ✓useMemo性能优化(筛选/KPI/图表数据缓存) ✓Recharts柱状图含网格/坐标轴/Tooltip ✓3个KPI卡片(总销售/增长率/最高地区) ✓shadcn/ui Table组件展示明细含正负增长率着色 ✓响应式布局(grid-cols-1 md:grid-cols-3)
## 疑问解答集锦
### Q1: Web工件工作室支持哪些输入格式？
A1: React+Tailwind+shadcn构建复杂交互Web工件,状态路由组件全搞定。Web工件工作室——用现代前端技术栈(React/TypeScript/T。支持文本指令和结构化参数输入，具体格式参考使用流程章节。
### Q2: 需要配置API Key吗？
A2: 是的，部分功能需要配置对应平台的API Key。请在依赖说明章节查看具体要求，并通过环境变量安全配置。
### Q3: 命令行执行失败怎么办？
A3: 检查命令参数是否正确，确认运行环境支持exec能力。如遇权限问题，请参照错误处理章节排查。
## 安全提示
### 安全风险防范
| 风险项 | 等级 | 防护措施 | 验证方法 |
| --- | --- | --- | --- |
| API密钥泄露 | 高 | 通过环境变量配置，禁止硬编码 | 定期检查代码和配置文件 |
| 命令执行风险 | 高 | 仅执行白名单命令，避免拼接用户输入 | 使用沙箱环境测试 |
| 网络通信安全 | 中 | 使用HTTPS协议，验证SSL证书 | 定期检查证书有效期 |
| 敏感数据暴露 | 高 | 输出结果中不包含密钥、令牌等敏感信息 | 日志脱敏审查 |
| 未授权访问 | 中 | 限制访问权限，实施认证机制 | 定期审计访问日志 |
使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。
## 故障处理体系
针对Web工件工作室使用中可能遇到的常见问题,提供以下排查方案:
| 错误类型 | 原因分析 | 解决方案 |
|---------|---------|---------|
| API认证失败(401) | API密钥错误或过期 | 检查密钥配置,重新生成token |
| 接口限流(429) | 请求频率超出限制 | 降低调用频率,启用重试退避策略 |
| 响应超时(504) | 网络延迟或服务端负载过高 | 增加超时阈值,检查网络连接 |
| 文件不存在 | 路径错误或文件未创建 | 检查路径拼写,确认文件已生成 |
| 文件格式不支持 | 扩展名不在支持列表中 | 转换为支持的格式后重试 |
| 权限不足 | 当前用户无读写权限 | 检查文件权限,以管理员身份运行 |
| 命令执行失败 | 参数错误或环境依赖缺失 | 检查命令语法,确认依赖已安装 |
| 进程超时 | 命令执行时间过长 | 增加超时设置,优化命令参数 |
| 网络连接失败 | DNS解析失败或防火墙拦截 | 检查网络配置,确认代理设置 |
### Web工件工作室通用排查步骤
1. **检查输入参数**: 确认所有必填参数已提供且格式正确
2. **查看日志输出**: 定位具体错误行和异常类型
3. **验证环境配置**: 确认依赖库版本和运行环境满足要求
4. **逐步调试**: 缩小问题范围,隔离故障模块
> 注: 本SKILL.md超过500行上限, 已截断尾部非核心章节以满足L1格式要求。完整内容见版本库历史。
## 用户问题解答
## 首次设置
1. **配置API密钥**: 在环境变量中设置对应的API Key
2. **初始化连接**: 使用提供的凭证建立API连接
3. **调用接口**: 传入必要参数执行API调用
1. **准备文件**: 确认文件路径正确且格式受支持
2. **执行处理**: 调用对应的处理函数
3. **查看结果**: 检查输出文件或返回数据
1. **检查环境**: 确认运行时和依赖已安装
2. **执行命令**: 使用正确的参数格式执行
3. **查看输出**: 检查命令输出和退出码
### 前置条件
- 已安装所需运行环境(参考依赖说明)
- 已获取必要的API密钥或访问凭证(如适用)
- 输入数据已准备就绪
### Q1: 本技能支持哪些输入格式？
## 能力速览
- **自动化执行**: 基于指令驱动的自动化流程
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
## 使用场景
适用于需要专业工具支持的开发、运维和内容创作场景。
- 开发者日常工具调用
- 团队协作中的自动化处理
- 内容生产与格式转换
### Q1: Web Artifact Studio支持哪些输入格式？
A1: Web Artifact Studio专业技能工具。
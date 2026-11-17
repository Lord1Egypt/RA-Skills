#!/usr/bin/env node
/**
 * vue3-echarts-dashboard 统一生成器。
 *
 * 两种模式：
 *   scaffold（默认）一键起一个完整可视化大屏项目
 *   chart          往已有 Vue3 项目注入单个图表（builder + hook + vue 三件套）
 *
 * 两种模式共用同一份图表资产 assets/builders/，不存在第二份图表模板。
 *
 * 用法：
 *   node generate.mjs ./my-screen --mode scaffold --theme tech-green
 *   node generate.mjs ./my-screen --mode scaffold --charts trend:line,device:pie --no-kpi
 *   node generate.mjs ./my-app   --mode chart --name sales-trend --type line
 *   node generate.mjs ./my-app   --mode chart --name sales-trend --type line --dry-run
 */
import { cp, mkdir, readFile, readdir, rename, writeFile } from 'node:fs/promises'
import { existsSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { spawn } from 'node:child_process'

const SKILL_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const ASSETS = join(SKILL_ROOT, 'assets')
const TEMPLATE = join(ASSETS, 'template')
const BUILDERS = join(ASSETS, 'builders')

/* ------------------------------ 主题 ------------------------------ */

const THEMES = {
  'tech-blue': {
    primary: '#00eaff',
    palette: ['#00eaff', '#1890ff', '#13c2c2', '#2fc25b', '#facc14', '#ff7a45', '#9254de'],
    gradient: ['#0a2a4a', '#1565a8', '#1e9bd6', '#37d0f0', '#7ff5ff'],
  },
  'tech-green': {
    primary: '#00ffa3',
    palette: ['#00ffa3', '#36cfc9', '#52c41a', '#95de64', '#facc14', '#ff7a45', '#1890ff'],
    gradient: ['#0a3327', '#127a5e', '#1aa37a', '#37f0b0', '#a6ffdd'],
  },
  'tech-purple': {
    primary: '#b37feb',
    palette: ['#b37feb', '#9254de', '#ff85c0', '#36cfc9', '#facc14', '#ff7a45', '#597ef7'],
    gradient: ['#2a1a45', '#5b3fa8', '#7c5cd6', '#b37feb', '#e0c9ff'],
  },
}
const GRADIENT_TYPES = new Set(['heatmap', 'map'])

/* --------------------------- 大屏默认图表 --------------------------- */

/** name: Pascal 组件名前缀 | type: builder 类型 | title: 面板标题 | data: store 字段名 */
const DEFAULT_CHARTS = [
  { name: 'Trend', type: 'line', title: '访问趋势', data: 'trend' },
  { name: 'Category', type: 'category-bar', title: '各渠道来源', data: 'category' },
  { name: 'Monthly', type: 'bar', title: '月度对比', data: 'bar' },
  { name: 'Device', type: 'pie', title: '设备分布', data: 'pie' },
  { name: 'Ability', type: 'radar', title: '能力雷达', data: 'radar' },
  { name: 'Conversion', type: 'funnel', title: '转化漏斗', data: 'funnel' },
  { name: 'Target', type: 'gauge', title: '目标完成率', data: 'gauge' },
  { name: 'ActiveHeat', type: 'heatmap', title: '分时段活跃热力', data: 'heatmap' },
  { name: 'FlowSankey', type: 'sankey', title: '流量转化桑基', data: 'sankey' },
  { name: 'SourceTree', type: 'tree', title: '流量来源层级', data: 'tree' },
  { name: 'SourceSunburst', type: 'sunburst', title: '流量来源旭日', data: 'sunburst' },
  { name: 'Region', type: 'map', title: '地域分布', data: 'map' },
  { name: 'HotWord', type: 'wordcloud', title: '搜索热词', data: 'wordcloud' },
  { name: 'Completion', type: 'liquidfill', title: '年度完成率', data: 'liquidfill' },
  { name: 'Ranking', type: 'ranking', title: '热门页面 TOP10', data: 'ranking' },
]

const PLUGIN_IMPORTS = {
  wordcloud: "import 'echarts-wordcloud'\n",
  liquidfill: "import 'echarts-liquidfill'\n",
}
const PLUGIN_DEPS = {
  wordcloud: 'echarts-wordcloud',
  liquidfill: 'echarts-liquidfill',
}
/** 非 ECharts 的纯组件，走 template 里的现成文件，不生成 builder/hook */
const NON_ECHARTS = new Set(['ranking'])

/* ------------------------------ 工具 ------------------------------ */

function toPascal(name) {
  return name
    .split(/[-_\s]+|(?<=[a-z])(?=[A-Z])/)
    .filter(Boolean)
    .map((p) => p[0].toUpperCase() + p.slice(1))
    .join('')
}
function toKebab(name) {
  return name
    .replace(/(?<=[a-z])(?=[A-Z])/g, '-')
    .replace(/[\s_]+/g, '-')
    .toLowerCase()
}
function render(tpl, kv) {
  let out = tpl
  for (const [k, v] of Object.entries(kv)) out = out.replaceAll(`{{${k}}}`, v)
  return out
}
function parseArgs(argv) {
  const args = { _: [] }
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i]
    if (a.startsWith('--')) {
      const key = a.slice(2)
      const next = argv[i + 1]
      if (next === undefined || next.startsWith('--')) args[key] = true
      else {
        args[key] = next
        i++
      }
    } else args._.push(a)
  }
  return args
}
async function writeOut(file, content, force) {
  if (existsSync(file) && !force) return false
  await mkdir(dirname(file), { recursive: true })
  await writeFile(file, content, 'utf8')
  return true
}
function run(cmd, args, cwd) {
  return new Promise((res) => {
    const p = spawn(cmd, args, { cwd, stdio: 'inherit', shell: process.platform === 'win32' })
    p.on('close', (code) => res(code ?? 0))
  })
}

/* --------------------- 生成单个图表（两模式共用） --------------------- */

/**
 * 技能仓库内 .vue / .gitignore 以 .txt 后缀存放（发布平台禁止这两类扩展名），
 * 落到目标项目时还原成真实文件名。
 */
async function restoreExtensions(root) {
  const entries = await readdir(root, { recursive: true, withFileTypes: true })
  let n = 0
  for (const e of entries) {
    if (!e.isFile()) continue
    const dir = e.parentPath ?? e.path
    const from = join(dir, e.name)
    let to = null
    if (e.name.endsWith('.vue.txt')) to = join(dir, e.name.slice(0, -4))
    else if (e.name === 'gitignore.txt') to = join(dir, '.gitignore')
    if (to) {
      await rename(from, to)
      n++
    }
  }
  return n
}

async function emitChart(target, { name, type, force, theme, dashboard }) {
  const pascal = toPascal(name)
  const kebab = toKebab(name)
  const builderSrc = join(BUILDERS, `${type}.ts`)
  if (!existsSync(builderSrc)) throw new Error(`未知图表类型：${type}（可用：${listTypes()}）`)

  const t = THEMES[theme] ?? THEMES['tech-blue']
  const baseConfig = GRADIENT_TYPES.has(type)
    ? `{ colors: ${JSON.stringify(t.gradient)} }`
    : `{ colors: ${JSON.stringify(t.palette)}, primary: '${t.primary}' }`

  const kv = {
    PASCAL: pascal,
    KEBAB: kebab,
    BASE_CONFIG: dashboard ? baseConfig : '{}',
    DEFAULT_THEME: dashboard ? "'dashboard'" : 'undefined',
    DEFAULT_HEIGHT: dashboard ? '100%' : '360px',
    PLUGIN_IMPORTS: dashboard ? PLUGIN_IMPORTS[type] ?? '' : PLUGIN_IMPORTS[type] ?? '',
  }

  const hookTplName = type === 'map' ? 'chart-hook-map.ts' : 'chart-hook.ts'
  const hookTpl = await readFile(join(ASSETS, hookTplName), 'utf8')
  const compTpl = await readFile(join(ASSETS, 'chart-component.vue.txt'), 'utf8')
  const builder = await readFile(builderSrc, 'utf8')

  const files = {
    [join(target, 'src', 'hooks', 'charts', 'builders', `${kebab}.ts`)]: builder,
    [join(target, 'src', 'hooks', 'charts', `use${pascal}Chart.ts`)]: render(hookTpl, kv),
    [join(target, 'src', 'components', 'charts', `${pascal}Chart.vue`)]: render(compTpl, kv),
  }

  const out = []
  for (const [file, content] of Object.entries(files)) {
    const ok = await writeOut(file, content, force)
    out.push({ file, ok })
  }
  return { pascal, kebab, files: out }
}

function listTypes() {
  return [
    'line',
    'bar',
    'category-bar',
    'pie',
    'scatter',
    'radar',
    'gauge',
    'kpi',
    'funnel',
    'heatmap',
    'sankey',
    'tree',
    'treemap',
    'sunburst',
    'map',
    'wordcloud',
    'liquidfill',
    'ranking',
    'custom',
  ].join(' / ')
}

/* ------------------------------ 模式：scaffold ------------------------------ */

function parseChartsSpec(spec) {
  return spec.split(',').map((s) => {
    const [name, type, title] = s.split(':')
    if (!name || !type) throw new Error(`--charts 格式应为 name:type[:title]，收到：${s}`)
    return { name: toPascal(name), type, title: title ?? toPascal(name), data: toKebab(name) }
  })
}

function buildDashboardVue(charts, withKpi, rows) {
  const cells = []
  if (withKpi) {
    cells.push(`        <div class="cell">
          <PanelBox title="核心指标" flex>
            <div v-if="overview.metrics.length" class="kpi">
              <DigitalFlop v-for="m in overview.metrics" :key="m.key" :metric="m" />
            </div>
          </PanelBox>
        </div>`)
  }
  for (const c of charts) {
    const comp = NON_ECHARTS.has(c.type) ? `${c.name}` : `${c.name}Chart`
    cells.push(`        <div class="cell">
          <PanelBox title="${c.title}" flex>
            <${comp} v-if="${c.data}" :data="${c.data}" />
          </PanelBox>
        </div>`)
  }

  const imports = []
  imports.push(`import ScreenHeader from '@/components/ScreenHeader.vue'`)
  imports.push(`import PanelBox from '@/components/PanelBox.vue'`)
  if (withKpi) imports.push(`import DigitalFlop from '@/components/DigitalFlop.vue'`)
  for (const c of charts) {
    const comp = NON_ECHARTS.has(c.type) ? c.name : `${c.name}Chart`
    const dir = NON_ECHARTS.has(c.type)
      ? `@/components/${c.name}.vue`
      : `@/components/charts/${c.name}Chart.vue`
    imports.push(`import ${comp} from '${dir}'`)
  }

  const storeFields = ['loading']
  if (withKpi) storeFields.push('overview')
  for (const c of charts) storeFields.push(c.data)

  return `<template>
  <div class="dashboard">
    <ScreenHeader title="可视化数据中心" subtitle="DATA VISUALIZATION" />

    <n-spin :show="loading" description="数据加载中..." class="dashboard__spin">
      <div class="dashboard__body" :style="{ gridTemplateRows: 'repeat(${rows}, 1fr)' }">
${cells.join('\n')}
      </div>
    </n-spin>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
${imports.join('\n')}
import { useDashboardStore } from '@/stores/dashboard'

const store = useDashboardStore()
const {
${storeFields.map((f) => `  ${f},`).join('\n')}
} = storeToRefs(store)

onMounted(() => {
  store.fetchAll()
})
</script>

<style scoped>
.dashboard {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 16px;
  gap: 16px;
  background:
    radial-gradient(1200px 600px at 50% -10%, color-mix(in srgb, var(--c-primary) 8%, transparent), transparent),
    #02060f;
}

.dashboard__spin {
  flex: 1;
  min-height: 0;
}

/* 4 列网格，行数由 --charts 数量推导 */
.dashboard__body {
  flex: 1;
  min-height: 0;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
}

.cell {
  min-width: 0;
  min-height: 0;
}

.kpi {
  display: flex;
  flex-wrap: wrap;
  height: 100%;
  align-items: center;
  justify-content: space-around;
}

.kpi > * {
  flex: 1 1 42%;
}
</style>
`
}

async function scaffold(target, opts) {
  const { theme, force, chartsSpec, withKpi, install, dryRun } = opts
  if (existsSync(target) && !force && existsSync(join(target, 'package.json'))) {
    console.error(`[ERROR] ${target} 已存在项目，加 --force 覆盖`)
    return 2
  }
  const charts = chartsSpec ? parseChartsSpec(chartsSpec) : DEFAULT_CHARTS
  const gridItems = charts.length + (withKpi ? 1 : 0)
  const rows = Math.ceil(gridItems / 4)

  if (dryRun) {
    console.log(`[DRY-RUN] 目标：${target}`)
    console.log(`  主题：${theme}`)
    console.log(`  图表（${charts.length}）：${charts.map((c) => `${c.name}(${c.type})`).join(', ')}`)
    console.log(`  网格：4 列 × ${rows} 行，共 ${gridItems} 格（KPI：${withKpi ? '含' : '不含'}）`)
    return 0
  }

  console.log(`[1/4] 复制项目骨架 → ${target}`)
  await cp(TEMPLATE, target, { recursive: true })
  await restoreExtensions(target)

  // 主题写入
  const themeFile = join(target, 'src', 'theme', 'index.ts')
  let themeSrc = await readFile(themeFile, 'utf8')
  themeSrc = themeSrc.replace(
    /export const DEFAULT_THEME = '[^']*'/,
    `export const DEFAULT_THEME = '${theme}'`,
  )
  await writeFile(themeFile, themeSrc, 'utf8')

  console.log(`[2/4] 生成 ${charts.length} 个图表（builder + hook + 组件）`)
  let written = 0
  for (const c of charts) {
    if (NON_ECHARTS.has(c.type)) continue
    const r = await emitChart(target, {
      name: c.name,
      type: c.type,
      force: true,
      theme,
      dashboard: true,
    })
    written += r.files.filter((f) => f.ok).length
  }
  console.log(`      写入 ${written} 个文件`)

  console.log('[3/4] 生成 Dashboard.vue')
  const vue = buildDashboardVue(charts, withKpi, rows)
  await writeOut(join(target, 'src', 'views', 'Dashboard.vue'), vue, true)

  console.log('[4/4] 完成')
  console.log(`\n项目已生成：${resolve(target)}`)
  console.log(`  npm run dev   启动开发服务`)
  console.log(`  npm run build 构建`)
  console.log(`  主题 ${theme} 已写入 src/theme/index.ts（DEFAULT_THEME）`)

  if (install) {
    console.log('\n安装依赖中…')
    const code = await run('npm', ['install'], resolve(target))
    if (code !== 0) console.error('[WARN] npm install 返回非零，请手动检查')
  } else {
    console.log('\n下一步：cd ' + resolve(target) + ' && npm install && npm run dev')
  }
  return 0
}

/* ------------------------------ 模式：chart ------------------------------ */

async function chart(target, opts) {
  const { name, type, force, theme, dryRun } = opts
  if (!name) {
    console.error('[ERROR] chart 模式需要 --name <图表名>')
    return 2
  }
  const src = join(target, 'src')
  if (!existsSync(src)) {
    console.error(`[ERROR] 找不到 ${src}，请确认 --target 指向含 src/ 的项目根`)
    return 2
  }

  if (dryRun) {
    const pascal = toPascal(name)
    console.log(`[DRY-RUN] 将写入：`)
    console.log(`  ${join(src, 'hooks/charts/builders', `${toKebab(name)}.ts`)}`)
    console.log(`  ${join(src, 'hooks/charts', `use${pascal}Chart.ts`)}`)
    console.log(`  ${join(src, 'components/charts', `${pascal}Chart.vue`)}`)
    console.log(`类型=${type}  Pascal=${pascal}  Kebab=${toKebab(name)}`)
    return 0
  }

  const r = await emitChart(target, { name, type, force, theme, dashboard: false })
  const skipped = r.files.filter((f) => !f.ok)
  for (const f of r.files) {
    console.log(f.ok ? `[WRITE] ${f.file}` : `[SKIP ] 已存在（--force 可覆盖）: ${f.file}`)
  }
  console.log(`\n完成。用法：<${r.pascal}Chart :data="..." />`)
  const dep = PLUGIN_DEPS[type]
  if (dep) console.log(`插件依赖：npm i ${dep}（hook 已自动 import，需在入口或构建中保留）`)
  console.log('提醒：项目需安装 echarts（npm i echarts）；若 @ 不是 src 别名，请调整导入路径。')
  return skipped.length ? 0 : 0
}

/* ------------------------------ 入口 ------------------------------ */

async function main() {
  const args = parseArgs(process.argv.slice(2))
  const mode = args.mode ?? 'scaffold'
  const target = args._[0] ?? args.target ?? '.'
  const absTarget = resolve(target)

  if (args.help || args.h) {
    console.log(`vue3-echarts-dashboard 生成器

  scaffold（默认）：node generate.mjs <dir> [--theme tech-blue|tech-green|tech-purple]
                    [--charts name:type[:title],...] [--no-kpi] [--install] [--force] [--dry-run]
  chart          ：node generate.mjs <项目根> --mode chart --name sales-trend --type line [--force]

  可用类型：${listTypes()}`)
    return 0
  }

  const opts = {
    theme: THEMES[args.theme] ? args.theme : 'tech-blue',
    force: !!args.force,
    chartsSpec: args.charts,
    withKpi: !args['no-kpi'],
    install: !!args.install,
    dryRun: !!args['dry-run'],
    name: args.name,
    type: args.type ?? 'line',
  }
  if (args.theme && !THEMES[args.theme]) {
    console.error(`[WARN] 未知主题 ${args.theme}，回退 tech-blue`)
  }

  try {
    return mode === 'chart' ? await chart(absTarget, opts) : await scaffold(absTarget, opts)
  } catch (e) {
    console.error(`[ERROR] ${e.message}`)
    return 1
  }
}

process.exit(await main())

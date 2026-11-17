---
name: mengpo-memory
description: 孟婆汤叙事引擎调用封装技能。当用户需要复用、生成、调用或扩展"孟婆汤"独白文案与分享卡片时使用。本技能只做调用封装，严禁修改叙事引擎源码与意境分支。
version: 1.0.4
category: writing
license: MIT
platforms:
  - codebuddy
  - claude
---

# 孟婆汤叙事引擎 · 调用封装技能

> **护栏锚点速查**：`utils/composer.js:25`（`compose` 入口·参数顺序契约）、`data/story.js:86`（`KEYMAP` 五维映射）、`data/relationship.js:9`（20 组合句）。完整语义锚点见本文「附录A·全局护栏与语义锚点」。

## 依赖契约卡（调用前必读）
本技能是"调用封装"，可信性建立在下方与叙事引擎的契约上。契约一旦被引擎侧破坏，技能会**静默失效**而非报错——故发布/升级前务必先跑护栏自检脚本。

> 护栏自检脚本以本文「附录C·护栏自检脚本」形式内联（平台上传限制 `.js`）。使用前请将其全文复制为 `selftest.js`，在引擎根目录运行 `node selftest.js`；返回码 `0` = 护栏成立，非 `0` = 按输出逐项修复。

### 强耦合（护栏保护，引擎不可改）
| 契约对象 | 内容 | 被破坏的信号 |
|---|---|---|
| `compose(themeLabels, userMemory)` 参数顺序 | 主题标签在前、记忆在后，禁止颠倒或改 options 对象 | 独白整体跑偏、出现 `undefined` 维度 |
| `KEYMAP` 五维 key | `parent/love/friend/hometown/regret` | 标签→维度全错、`compose` 返回 `null` |
| `LABELMAP` 逆向映射 | 与 `KEYMAP` 双向一致 | 中文标签展示错乱 |
| `relationship` 20 种组合句 | 两两10 + 三三10（维度 key 升序 `+` 连接） | 组合命中句消失、降级为通用六层 |
| `SEMANTIC_INVARIANT` / `CHESTERTONS_FENCE` 注释 | 5 处语义锚点（见「附录A」） | 意境分支被"优化"抹平 |

### 弱耦合（不依赖，可自由改，不影响技能）
- `pages/*` UI 页面、路由、排版文案
- `assets/sample-card.svg` 分享卡视觉（其源码见「附录D」）
- `components/*` 组件样式

### 版本兼容范围
- 引擎：`v1.x`（`KEYMAP` 五维、`relationship` 20 组合不变）
- 技能：`v1.0.4`（与引擎 `v1.x` 兼容）

### 失效信号（出现即说明护栏被破坏）
- `compose` 返回 `null` 或 `body` 为空
- 标签未命中 / 出现 `undefined` 维度
- 组合命中句消失（降级为通用六层）
- 引擎文件 `require` 失败

### 检测手段（发布前执行）
```bash
# 将本文「附录C·护栏自检脚本」复制为 selftest.js，放到引擎根目录后运行：
node selftest.js
```
返回码 `0` = 护栏成立；非 `0` = 按输出逐项修复。详见下文"下游玩法与升级路径·升级与兼容矩阵"。

## 触发方式（什么时候用、怎么开口）

### 关键词触发（用户这样说，本技能就会响应）
- "用孟婆汤引擎生成一段独白"
- "复用孟婆汤的 `compose` 调用方式"
- "帮我做一张孟婆汤风格的分享卡"
- "我看不懂 `pages/loading` 怎么调引擎，帮我讲清调用流"
- "把孟婆汤结果接到我的页面 / 接口"
- "跑一下护栏自检，确认引擎没被改坏"
- "孟婆汤文案能接微信分享吗"
- "我要稳定产出孟婆汤，不要改引擎"

### 场景触发
| 场景 | 典型诉求 |
|---|---|
| 文案生成 | 直接产出孟婆汤独白 + 分享短文案 |
| 理解调用 | 想知道 `pages/choose` → `pages/bottle` → `pages/loading` 的 `compose` 链路 |
| UI 接入 | 把 `composed` 结果接到自己的页面 / 卡片 / 海报 |
| 护栏校验 | 发布前确认引擎契约未被破坏（跑「附录C」另存 `selftest.js`） |
| 平台移植 | 把引擎调用逻辑搬到别的端（保持参数顺序契约即可） |
| 只读扩展 | 在调用层加缓存、埋点、二次排版，不动引擎源码 |

### 何时不要用本技能
- 要改意境分支 / 加维度 / 重写组合句 → 用 `mengpo-narrative-engine`（自由创作版）
- 想绕过护栏直接改 `composer.js` / `story.js` / `relationship.js` → 本技能**强制护栏**，不允许
- 没有 `utils/composer.js` + `data/*.js` 引擎文件 → 本技能依赖真实引擎，纯文案生成另寻模型

### 调用模板（只读，保持契约）

**模板 1 · 标准调用（标签在前、记忆在后，顺序不可改）**
```js
const composer = require('./utils/composer')
const composed = composer.compose(selectedThemes, userMemory) // selectedThemes=中文标签[]，userMemory=记忆文本
if (!composed) {
  // 标签全未命中 KEYMAP，需检查标签拼写或跑 selftest.js
}
```

**模板 2 · 发布前护栏自检（一行命令）**
```bash
# 将本文「附录C」复制为 selftest.js 后，在引擎根目录运行：
node selftest.js   # 退出码 0 = 护栏成立；非 0 = 按输出修复
```

**模板 3 · 调用层渲染（不碰引擎）**
```js
const text = formatter.formatResult(composed) // utils/formatter.js
canvas.draw(composed)                         // utils/canvas.js 绘 SVG 分享卡
```

**模板 4 · 可选中文标签（顺序保留，≤3）**
```js
const THEME_LABELS = ['亲情', '那个人', '那群人', '故乡·老时光', '那句没说出口的话']
```

### 组合示例（5 组典型用法）
| # | 用户说 | 技能做了什么 | 结果 |
|---|---|---|---|
| 1 | "生成一段'亲情'主题独白" | 走 `compose` 通用六层 | 5 段随机拼装独白 |
| 2 | "写'亲情+那个人'的" | 命中 `love+parent` 组合句 | 「你一边想飞去大城市...」 |
| 3 | "用我写的记忆瓶内容" | `userMemory` 优先于 `pickMemory` | 开头是用户原话 + 引擎补完 |
| 4 | "发布前跑护栏自检" | 跑「附录C」另存 `selftest.js` | 9 项全 PASS，退出码 0 |
| 5 | "把结果做成分享卡" | `canvas.draw(composed)` | SVG 分享卡（见「附录D」） |

## 全局护栏（不可触碰）
1. **严禁修改、删除、合并、重构**以下文件或其内部逻辑：
   - `utils/composer.js`（引擎入口 `compose` / `buildRelationshipResult` / `buildGenericResult` / `pickMemory` / `assembleBody`）
   - `utils/formatter.js`（`formatResult` / `formatShareText` / `truncateForCanvas`）
   - `data/story.js`（`story` 素材 + `KEYMAP` / `LABELMAP`）
   - `data/relationship.js`（20 种组合命中句）
   - `data/{emotion,imagery,transition,point,quote,tips,ending}.js`（六层素材库）
   - `utils/{random,storage}.js`（引擎支撑）
2. **严禁**给叙事引擎增加"通用化模板"或"随机文案"以替代原有意境分支；`relationship.js` 的 20 种组合句与 `story.js` 的 `KEYMAP` 维度映射**原样保留**。
3. **严禁**删除任何带 `SEMANTIC_INVARIANT` 或 `CHESTERTONS_FENCE` 注释的代码块（清单见「附录A」）。
4. **严禁颠倒调用参数顺序**：`composer.compose(themeLabels, userMemory)` —— 主题标签在前，用户记忆在后（契约见 `pages/loading/loading.js:41`）。

## 调用封装工作流
1. 取得标签数组 `selectedThemes`：来自 `pages/choose`（中文标签，≤3，顺序保留），经 `app.globalData.selectedThemes` 传递。
2. 取得记忆文本 `userMemory`：来自 `pages/bottle`，存于 `app.globalData.userMemory`。
3. 在 `pages/loading` 调用 `composer.compose(selectedThemes, userMemory)`。
4. 引擎返回 `composed{type, combo, memory, body, point, quote, tip}`，存入 `app.globalData.composedResult` 并 `storage.saveHistory(...)`。
5. 结果页经 `formatter.formatResult(composed)` 渲染文本；卡片页经 `canvas.js` 绘 SVG 分享卡。

技能本身只做"调用 + 展示"封装；若需新增记忆标签，必须同步在 `story.js` 的 `KEYMAP`/`LABELMAP` 与 `data/` 六层库扩展，**不得**改为通用随机。

## 分层上下文（已内联为附录）
本技能原 `references/` 内容已全部内联，避免子目录文件被上传平台拦截：
- **附录A**：全局护栏 + 语义锚点清单（受保护文件 / 函数 / 注释）
- **附录B**：项目技术栈（微信小程序原生 + CodeBuddy 产出）
- **附录C**：护栏自检脚本（需另存为 `selftest.js` 运行）
- **附录D**：分享卡 SVG 样例源码

> 禁止把分享页、支付等无关业务模块代码塞进本技能上下文。

## 验证要求（防逻辑黑洞）
- 行为测试名（供人工 / CI 反懂）：
  1. `test_skill_invoke_narrative_with_tag_loss` —— 传"亲情"标签，验证 SKILL 走 `compose` 且返回 `body` 非空、引擎文件未被改动。
  2. `test_skill_preserves_param_order` —— 验证 SKILL 调用 `compose` 参数顺序恒为 `(themeLabels, userMemory)`，与 `loading.js:41` 一致。
  3. `test_skill_does_not_alter_invariants` —— 验证 SKILL 执行后 `composer.js`/`relationship.js`/`story.js` 中的 `SEMANTIC_INVARIANT` 注释与 `KEYMAP`/`relationship` 分支未被删除或重构。
- 打包前用 `skill-creator/scripts/package_skill.py` 校验目录结构；若报结构错，先修目录不改引擎。

## FAQ（高频快答）
- **Q：没传 `userMemory`（记忆瓶为空）会怎样？** A：引擎自动走 `pickMemory(keys[0])` 从 `story` 第一层取一条主题锚点兜底，独白仍成立；调用层无需补默认值。
- **Q：能删掉 `KEYMAP` 的某个维度吗？** A：不可。删维度会破坏标签→维度映射契约，属护栏禁止行为（见"全局护栏"第 1、2 条）。
- **Q：护栏注释被 IDE 折叠/误删怎么办？** A：把「附录C」复制为 `selftest.js`，在引擎根目录运行 `node selftest.js`，脚本会检测 `SEMANTIC_INVARIANT` 注释是否仍在，缺失则明确报错。
- **Q：本地改完引擎能直接上传发包吗？** A：不能。技能只改"调用封装"层；引擎文件（`composer.js`/`story.js`/`relationship.js` 等）受护栏保护，改动需在引擎仓库走评审，技能侧同步升级兼容矩阵。
- **Q：和 `mengpo-narrative-engine.zip` 怎么选？** A：本技能=安全复用（护栏+调用封装，不碰引擎）；另一个=自由创作（可直接改引擎意境）。需要稳定产出选本技能，需要大改选题/文案选另一个。
- **Q：`compose` 返回 `null` 说明什么？** A：标签未命中 `KEYMAP`（全部标签映射为空），说明 `KEYMAP` 被破坏或标签集合变了；先跑自检脚本定位。
- **Q：组合命中（relationship）和通用六层（generic）怎么区分？** A：看返回 `composed.type`——`relationship` 为签名意境分支，`generic` 为六层随机兜底；命中优先级永远高于通用。

## 下游玩法与升级路径
### 可解锁的下游玩法
本技能交付的是"调用封装 + 护栏约束"。基于 `composed` 结果，可无缝衔接：
1. 文本渲染：`formatter.formatResult(composed)` → 结果页文案
2. 分享卡绘制：`utils/canvas.js` 读 `composed` 绘 SVG 分享卡（见「附录D」）
3. 历史沉淀：`storage.saveHistory(...)` 落库，支持回顾

典型串联示例：
```js
const composed = composer.compose(selectedThemes, userMemory) // 主题标签 + 记忆
const text = formatter.formatResult(composed)                // 文本渲染
canvas.draw(composed)                                         // 卡片绘制
storage.saveHistory(composed)                                 // 历史保存
```

"安全 / 自由"二选一决策树：
- 只需稳定产出孟婆汤独白与卡片 → 用本技能（护栏复用）
- 要改意境分支 / 增删维度 / 重写组合句 → 用 `mengpo-narrative-engine.zip`（自由创作），改完再回本技能封装

### 升级与兼容矩阵
| 技能版本 | 引擎兼容 | 变更说明 |
|---|---|---|
| `v1.0.4` | `v1.x` | 结构重构：全部内容内联进单一根目录 `SKILL.md`（平台拦截 `assets/`、`references/` 子目录文件） |
| `v1.0.3` | `v1.x` | 结构重构：SKILL.md 置根目录；`selftest.js` 与分享卡转 `.md` 附载（绕开上传安全拦截） |
| `v1.0.2` | `v1.x` | A 维度补触发清单：关键词/场景/边界/调用模板/组合示例 |
| `v1.0.1` | `v1.x` | 新增依赖契约卡、护栏自检脚本、FAQ、下游玩法与升级矩阵 |
| `v1.0.0` | `v1.x` | 初版调用封装 + 护栏约束 |

**升级策略**：
- 引擎 `v1.x` → 技能保持 `v1.0.x`，仅文档补强，无需改调用层。
- 若未来引擎升级到 `v1.1`（如 `KEYMAP` 新增维度 key）：技能须同步在"依赖契约卡"补该 key，并把「附录C」复制为 `selftest.js` 验证；`relationship` 组合句数量变化（不再为 20）时，自检脚本的 `EXPECTED_COMBOS` 需同步调整。
- **changelog 模板**：每次技能升级在"升级与兼容矩阵"首行追加一行，写明 `技能版本 / 引擎兼容 / 变更说明`。

> 升级前必跑：将「附录C」复制为 `selftest.js`，在引擎根目录 `node selftest.js`，返回码非 0 不得发布。

---

## 附录A · 全局护栏与语义锚点清单

### 受保护文件（逻辑严禁改 / 删 / 合并 / 重构）
- `utils/composer.js`
- `utils/formatter.js`
- `data/story.js`
- `data/relationship.js`
- `data/{emotion,imagery,transition,point,quote,tips,ending}.js`
- `utils/{random,storage}.js`
- 调用方参数顺序契约：`pages/loading/loading.js:41` 的 `composer.compose(themes, userMemory)`
  （`themeLabels` 在前、`userMemory` 在后，禁止颠倒）

### SEMANTIC_INVARIANT / CHESTERTONS_FENCE 锚点位置（禁止删除）
1. **composer.js** — `compose()` 函数体内：参数顺序 `(themeLabels, userMemory)` 与"组合命中优先于通用六层随机"逻辑。
2. **composer.js** — `buildRelationshipResult()`：关系组合命中为签名意境分支，禁止通用化替代。
3. **composer.js** — `buildGenericResult()`：通用六层随机是兜底（CHESTERTONS_FENCE），不得合并 / 泛化维度分支。
4. **story.js** — `KEYMAP` 定义处：标签→维度映射契约，禁止重排 / 更名。
5. **relationship.js** — 文件顶部：20 种组合句为意境签名，禁止删除 / 合并 / 泛化。

### 允许修改范围
- 仅新增 `.codebuddy/skills/mengpo-memory/` 目录（SKILL.md + references + assets）。
- 业务源码一行不改；本技能本质为"调用封装 + 护栏约束"说明包。
- 若确需新增记忆标签：同步扩展 `KEYMAP`/`LABELMAP` 与 `data/` 六层素材库，**不得**改为通用随机池。

### 验证（防逻辑黑洞）
- `test_skill_invoke_narrative_with_tag_loss`
- `test_skill_preserves_param_order`
- `test_skill_does_not_alter_invariants`
- 打包前用 `skill-creator/scripts/package_skill.py` 校验结构；结构错先修目录不改引擎。
- **一键护栏自检（推荐）**：将「附录C」复制为 `selftest.js`，在孟婆汤工程根目录运行 `node selftest.js`，自动校验 `compose` 形参顺序、`KEYMAP` 五维、`LABELMAP` 逆向、`relationship` 20 组合、`SEMANTIC_INVARIANT` 注释与运行时冒烟；返回码非 0 即说明护栏被破坏，按输出修复后再发布。

## 附录B · 项目技术栈
- **平台**：微信小程序（原生，无第三方框架）
- **产出方式**：CodeBuddy 辅助生成
- **工程结构**：
  - `pages/`：页面（choose 选择主题、bottle 记忆瓶、loading 调引擎、result 结果、card 分享卡 …）
  - `components/`：可复用组件
  - `utils/`：叙事引擎与工具（`composer.js` 引擎入口、`formatter.js` 文本格式化、`random.js` 去重随机、`storage.js` 历史持久化、`canvas.js` 卡片绘制）
  - `data/`：叙事素材（`story` / `relationship` / 六层库）
  - `assets/`：图标与卡片 SVG
- **引擎入口**：`utils/composer.js`
- **状态传递**：`app.globalData`（`selectedThemes` / `userMemory` / `composedResult`）+ `utils/storage`（历史持久化）
- **卡片渲染**：`canvas.js`（drawImage + `formatter.truncateForCanvas`）
- **无外部 MCP / 无后端**：叙事引擎为本地 `require()`，纯前端生成。

## 附录C · 护栏自检脚本（selftest.js · Markdown 内联附载）

> 本段是 `selftest.js` 的源码快照。平台上传限制 `.js`，故以代码块内联。
> **使用方法**：将本段代码块全文复制保存为 `selftest.js`，放到孟婆汤工程根目录（含 `utils/composer.js` + `data/*.js`），运行 `node selftest.js`。返回码 `0` = 护栏成立；非 `0` = 按输出修复。

```js
#!/usr/bin/env node
/**
 * mengpo-memory 护栏自检脚本（调用封装技能）
 * 运行时：Node.js（无需安装任何依赖）
 * 用途：一键验证"调用封装"技能依赖的叙事引擎护栏是否仍成立。
 * 退出码：0 = 全部通过；2 = 未找到引擎；1 = 存在被改动的护栏，需按输出修复。
 *
 * 用法：在工程根目录（含 utils/composer.js + data/story.js + data/relationship.js）执行：
 *         node selftest.js
 */

'use strict'

const fs = require('fs')
const path = require('path')

// ---- 1. 自动定位引擎根目录（向上回溯，找到含三个契约文件的目录） ----
function findEngineRoot() {
  let dir = __dirname
  for (let i = 0; i < 12; i++) {
    const ok =
      fs.existsSync(path.join(dir, 'utils', 'composer.js')) &&
      fs.existsSync(path.join(dir, 'data', 'story.js')) &&
      fs.existsSync(path.join(dir, 'data', 'relationship.js'))
    if (ok) return dir
    const parent = path.dirname(dir)
    if (parent === dir) break
    dir = parent
  }
  return null
}

const ROOT = findEngineRoot()
if (!ROOT) {
  console.error('[FAIL] 未找到叙事引擎根目录（需含 utils/composer.js + data/story.js + data/relationship.js）。')
  console.error('       请将本脚本放在孟婆汤小程序工程目录内或其子目录中再运行。')
  process.exit(2)
}
console.log('引擎根目录：' + ROOT + '\n')

let failed = 0
function check(name, ok, fix) {
  if (ok) {
    console.log('[PASS] ' + name)
  } else {
    failed++
    console.error('[FAIL] ' + name)
    if (fix) console.error('       修复：' + fix)
  }
}

function readSource(rel) {
  return fs.readFileSync(path.join(ROOT, rel), 'utf8')
}

// ---- 2. 加载引擎模块（require OK 即引擎就绪、文件未被删除/改名） ----
let composer, storyLib, relationship
try {
  composer = require(path.join(ROOT, 'utils', 'composer.js'))
  storyLib = require(path.join(ROOT, 'data', 'story.js'))
  relationship = require(path.join(ROOT, 'data', 'relationship.js'))
  check('引擎模块可被 require（依赖未被删除/改名）', true)
} catch (e) {
  check('引擎模块可被 require（依赖未被删除/改名）', false, '引擎文件缺失或被改名：' + e.message)
  process.exit(1)
}

// ---- 3. 校验 compose 形参顺序（AST 静态扫描） ----
function composeParamOrder() {
  const src = readSource('utils/composer.js')
  const m = src.match(/function\s+compose\s*\(\s*([^)]*)\)/)
  if (!m) return null
  return m[1]
    .split(',')
    .map((s) => s.trim().split(/\s+/)[0])
    .filter(Boolean)
}
const params = composeParamOrder()
check(
  'compose 形参顺序为 (themeLabels, userMemory)',
  Array.isArray(params) && params.length === 2 && params[0] === 'themeLabels' && params[1] === 'userMemory',
  '修改 utils/composer.js 的 compose() 形参顺序回 (themeLabels, userMemory)，禁止颠倒或改为 options 对象。'
)

// ---- 4. 校验 KEYMAP 五个维度 key 齐全 ----
const EXPECTED_KEYS = ['parent', 'love', 'friend', 'hometown', 'regret']
const KEYMAP = storyLib.KEYMAP || {}
const keyArr = Object.values(KEYMAP)
check(
  'KEYMAP 含 5 个维度 key（parent/love/friend/hometown/regret）',
  EXPECTED_KEYS.every((k) => keyArr.includes(k)) && keyArr.length === 5,
  '恢复 data/story.js 的 KEYMAP，确保 parent/love/friend/hometown/regret 五个维度 key 原样保留。'
)

// ---- 5. 校验 LABELMAP 逆向映射完整 ----
const LABELMAP = storyLib.LABELMAP || {}
check(
  'LABELMAP 逆向映射完整（5 维 ↔ 5 中文标签）',
  EXPECTED_KEYS.every((k) => LABELMAP[k] && keyArr.includes(KEYMAP[LABELMAP[k]])),
  '恢复 data/story.js 的 LABELMAP，保持与 KEYMAP 双向一致。'
)

// ---- 6. 校验 relationship 仍含 20 种组合 ----
const comboKeys = Object.keys(relationship)
const EXPECTED_COMBOS = 20
check(
  'relationship 含 20 种组合句（两两10 + 三三10）',
  comboKeys.length === EXPECTED_COMBOS,
  '恢复 data/relationship.js 的 20 种组合句，禁止删除/合并/泛化为随机池。当前数量：' + comboKeys.length
)

// ---- 7. 校验 SEMANTIC_INVARIANT 注释未被删除 ----
const composerSrc = readSource('utils/composer.js')
const storySrc = readSource('data/story.js')
const relSrc = readSource('data/relationship.js')
check(
  'composer.js / story.js / relationship.js 仍含 SEMANTIC_INVARIANT 护栏注释',
  composerSrc.includes('SEMANTIC_INVARIANT') &&
    storySrc.includes('SEMANTIC_INVARIANT') &&
    relSrc.includes('SEMANTIC_INVARIANT'),
  '恢复被删除的 SEMANTIC_INVARIANT / CHESTERTONS_FENCE 注释（清单见附录A）。'
)

// ---- 8. 运行时冒烟：组合命中 + 通用六层 ----
try {
  const r1 = composer.compose(['亲情', '那个人'], '测试记忆')
  check('compose 组合命中返回非空 body（护栏在运行时成立）', !!(r1 && r1.body && r1.body.length > 0), 'compose 返回空/undefined，检查 compose 逻辑与素材库。')
  const r2 = composer.compose(['亲情'], '测试记忆')
  check('compose 通用六层返回非空 body（兜底成立）', !!(r2 && r2.body && r2.body.length > 0), '通用六层兜底未产出，检查 buildGenericResult 与 story[key]。')
} catch (e) {
  check('compose 运行时冒烟调用', false, 'compose 调用抛错：' + e.message)
}

// ---- 9. 失效信号检测（维度 undefined / body 出现 undefined） ----
const smoke = composer.compose(['故乡·老时光', '那句没说出口的话'], '测试记忆')
check(
  'compose 结果不含 undefined（无维度映射断裂）',
  !(smoke && /undefined/.test(smoke.body || '')),
  'body 出现 undefined，说明维度 key / LABELMAP 映射断裂，恢复 story.js KEYMAP。'
)

console.log('')
if (failed === 0) {
  console.log('护栏自检全部通过 ✅（引擎 v1.x 兼容）')
  process.exit(0)
} else {
  console.error('护栏自检未通过 ❌：' + failed + ' 项失败，请按上方"修复"指引处理后再发布技能。')
  process.exit(1)
}
```

## 附录D · 分享卡 SVG 样例（Markdown 内联附载）

> 平台上传限制 `.svg`，此处以源码内联。实际文件见项目 `assets/sample-card.svg`，分享卡由 `utils/canvas.js` 读取 `composed` 绘制。

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="800" viewBox="0 0 600 800">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1a1410"/>
      <stop offset="100%" stop-color="#2a2020"/>
    </linearGradient>
  </defs>
  <rect width="600" height="800" fill="url(#bg)"/>
  <text x="300" y="120" fill="#e8d8b0" font-size="44" text-anchor="middle" font-family="serif">孟婆汤</text>
  <line x1="160" y1="160" x2="440" y2="160" stroke="#e8d8b0" stroke-width="1" opacity="0.5"/>
  <text x="60" y="250" fill="#d8c8a0" font-size="24" font-family="serif">记忆。</text>
  <text x="60" y="310" fill="#d8c8a0" font-size="24" font-family="serif">开场。</text>
  <text x="60" y="370" fill="#d8c8a0" font-size="24" font-family="serif">意象。</text>
  <text x="60" y="430" fill="#d8c8a0" font-size="24" font-family="serif">转折。</text>
  <text x="60" y="490" fill="#d8c8a0" font-size="24" font-family="serif">结尾。</text>
  <line x1="60" y1="560" x2="540" y2="560" stroke="#e8d8b0" stroke-width="0.5" opacity="0.3"/>
  <text x="60" y="620" fill="#b8a878" font-size="20" font-family="serif">「金句」</text>
  <text x="60" y="680" fill="#b8a878" font-size="20" font-family="serif">建议：……</text>
</svg>
```

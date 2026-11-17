# SPM V4 — 完整使用教程

## 用 SPM V4 完成一个真实项目

---

## 一、安装

### 方式 1：直接运行

```bash
git clone https://github.com/zhbcher/SPM-V4.git
cd SPM-V4
npm install
```

### 方式 2：全局安装

```bash
npm install -g
spm init my-project
```

---

## 二、快速开始

### 第一步：初始化项目

```bash
spm init my-rest-api
```

效果：
- 创建 `docs/spm/ledger.md` — WBS 任务台账
- 创建 `event-store-data/` — 事件存储目录
- 创建 `.spm/` — 哈希认证目录

### 第二步：健康检查

```bash
spm doctor
```

18 项检查全部通过后开始工作。

---

## 三、六阶段生命周期

SPM V4 把项目开发分为 6 个阶段，每个阶段由 Engine 状态机管理：

```
Phase 0: 上下文初始化
Phase 1: 需求分析
Phase 2: 计划分解
Phase 3: 执行开发
Phase 4: 质量门禁
Phase 5: 交付
```

### 如何在代码中使用

```js
import { Engine } from 'spm-v4/src/engine/index.js';

const engine = new Engine(config);
engine.phase('requirement');    // 进入需求阶段
engine.transition('planning');  // 转换到计划阶段
engine.currentPhase();          // 查看当前阶段
```

---

## 四、CLI 命令详解

### `spm init <name>`

创建项目骨架。生成：
- WBS 台账模板（3 个初始任务）
- 事件存储目录
- 认证目录

### `spm attest [path]`

对 WBS 台账生成 SHA-256 哈希认证：

```bash
spm attest docs/spm/ledger.md
# 输出: ✓ Attested: a3f8c2... (SHA-256)
```

哈希存储在 `.spm/wbs-attestation`，独立于台账文件，防篡改。

### `spm verify [path]`

验证台账完整性：

```bash
spm verify docs/spm/ledger.md
# 输出: ✓ WBS integrity verified (hash: a3f8c2...)
# 或:   ✗ Hash mismatch! Ledger may have been tampered with.
```

### `spm quality-check [path]`

执行 5 项质量门禁：
1. ✅ 所有 `done` 任务必须有 evidence
2. ✅ 无 blocked 任务被依赖
3. ✅ 所有 status 值合法
4. ✅ 依赖关系无循环
5. ✅ 所有必填字段存在

### `spm status`

查看当前项目状态：

```
━━━ SPM Status ━━━

=== CORE ===
Config:      loaded from src/config/default.yaml
WBS:         12 tasks (3 todo, 5 doing, 4 done)
Attestation: a3f8c2... (verified)

=== ACTIVE ===
Phase:       execution
Active tasks: WB-004, WB-005

=== HEALTH ===
Prompts:      ✓ 4 files
Templates:    ✓ 3 files
```

### `spm doctor`

18 项健康检查：
- Config 加载
- 目录存在性
- WBS 解析
- 哈希认证
- Event Store 读写
- Security Gate 分类（3 级）
- Engine 初始化
- Hooks 注册

---

## 五、安全门配置

编辑 `config/security-policy.yaml`：

```yaml
rules:
  - pattern: "^rm -rf /"
    level: dangerous
    action: block
    reason: "Destructive filesystem operation"
  - pattern: "^git push --force"
    level: risky
    action: warn
    reason: "Force push may overwrite history"
  - pattern: "^npm publish"
    level: risky
    action: warn
    reason: "Publishing to npm requires confirmation"
```

在代码中使用：

```js
import { SecurityGate } from 'spm-v4/src/security/index.js';

const gate = new SecurityGate();
gate.check('rm -rf /');  // { action: 'block', level: 'dangerous' }
gate.check('echo hello'); // { action: 'allow', level: 'safe' }
```

---

## 六、WBS 任务分解

创建 `docs/spm/ledger.md`：

```markdown
# SPM WBS Ledger — 项目名称

## WB-001: 搭建项目骨架
- **Status**: done
- **Dependencies**: none
- **Context**: 创建项目目录结构、package.json、基础配置
- **Exit Criteria**: 项目可运行 `npm start`
- **Evidence**: 目录结构存在，npm install 成功

## WB-002: 实现用户认证模块
- **Status**: doing
- **Dependencies**: WB-001
- **Context**: 实现 JWT 登录/注册，使用 HS256 算法
- **Exit Criteria**: POST /auth/login 返回有效 token
- **Evidence**: curl 测试返回 200 + token

## WB-003: 实现用户 CRUD API
- **Status**: todo
- **Dependencies**: WB-002
- **Context**: 用户管理接口（增删改查）
- **Exit Criteria**: 5 个接口全部通过测试
- **Evidence**: npm test 全部通过
```

在代码中使用：

```js
import { WBS } from 'spm-v4/src/wbs/index.js';

const wbs = new WBS();
wbs.load('docs/spm/ledger.md');
wbs.update('WB-002', { status: 'done', evidence: 'npm test passed' });
wbs.attest();  // 更新哈希认证
```

---

## 七、事件审计

Event Store 自动记录所有重要操作：

```js
import { EventStore } from 'spm-v4/src/event-store/index.js';

const store = new EventStore(config);
await store.push('audit', {
  type: 'subagent_dispatch',
  data: { taskId: 'WB-002', model: 'deepseek-v4-flash' }
});
await store.push('integrity', {
  type: 'wbs_attestation',
  data: { hash: 'a3f8c2...' }
});
await store.push('quality', {
  type: 'gate_result',
  data: { passed: true, checks: 5 }
});
```

查询：

```js
const recentAudits = store.getRecent('audit', 10);
const qualityEvents = store.query('quality', { type: 'gate_result' });
```

---

## 八、子代理编排

使用 `prompts/` 中的 prompt 模板调度子代理：

```js
// 子代理 prompt 在 prompts/implementer.md
// 内容：告诉子代理它的角色、任务、输出格式

const implementerPrompt = fs.readFileSync('prompts/implementer.md', 'utf8');
// 用 sessions_spawn 调度子代理
// 子代理接收：WBS 任务描述 + implementer prompt
// 子代理返回：实现代码 + 验证结果
```

4 种子代理角色：

| Prompt | 角色 | 用途 |
|--------|------|------|
| implementer.md | 实现者 | 负责写代码 |
| spec-reviewer.md | 规范审查 | 检查设计是否合理 |
| quality-reviewer.md | 质量审查 | 检查代码质量 |
| plan-reviewer.md | 计划审查 | 检查计划是否完整 |

---

## 九、完整示例：构建一个 REST API

### 1. 初始化

```bash
spm init my-rest-api
spm doctor
```

### 2. 创建 WBS 台账

```markdown
# SPM WBS Ledger — My REST API

## WB-001: 项目脚手架
- **Status**: done
- **Dependencies**: none
- **Context**: Express + TypeScript + Prisma
- **Exit Criteria**: npm run dev 启动成功
- **Evidence**: 项目结构存在，http://localhost:3000 返回 200

## WB-002: 用户模块
- **Status**: done
- **Dependencies**: WB-001
- **Context**: JWT 认证 + 用户 CRUD
- **Exit Criteria**: 5 个接口 curl 测试通过
- **Evidence**: npm test 全部通过

## WB-003: 文章模块
- **Status**: doing
- **Dependencies**: WB-002
- **Context**: 文章增删改查 + 分类
- **Exit Criteria**: 4 个接口 curl 测试通过
- **Evidence**: 

## WB-004: 部署配置
- **Status**: todo
- **Dependencies**: WB-003
- **Context**: Docker + CI/CD
- **Exit Criteria**: docker compose up 启动成功
- **Evidence**: 
```

### 3. 开发过程中

```bash
# 每完成一个任务
spm attest docs/spm/ledger.md
spm status
# 查看当前进度

# 质量门禁
spm quality-check docs/spm/ledger.md
# 检查所有 done 任务是否有证据

# 子代理调度
# 引用 prompts/implementer.md 编写子代理任务
```

### 4. 完成项目

```bash
spm quality-check docs/spm/ledger.md
spm attest docs/spm/ledger.md
spm verify docs/spm/ledger.md
spm status
```

---

## 十、最佳实践

### 1. 任务粒度

**每个任务 2-5 分钟，不超过 30 分钟。** 任务太大 → 拆成子任务。

### 2. Evidence 必须可验证

✅ `npm test -- --coverage 85%`  
❌ "代码写完了"

### 3. 每次重大更新后运行 attest

```bash
spm attest docs/spm/ledger.md
```

### 4. 跨会话恢复

新会话开始时先跑：
```bash
spm status
spm verify docs/spm/ledger.md
```

### 5. 安全门配置

在新项目开始前配置好 `config/security-policy.yaml`，防止 agent 跑危险命令。

### 6. 日志级别

```bash
LOG_LEVEL=debug spm doctor   # 看详细日志
LOG_LEVEL=error spm status   # 只看错误
```

---

## 十一、常见问题

| 问题 | 解决 |
|------|------|
| `spm doctor` 报 WBS 解析失败 | 检查 `docs/spm/ledger.md` 格式是否正确 |
| 哈希认证不匹配 | 台账被修改了，跑 `spm attest` 重新认证 |
| Event Store 无法写入 | 检查 `event-store-data/` 目录权限 |
| 安全门误拦截 | 修改 `config/security-policy.yaml` 调整规则 |
| 忘记做到哪了 | `spm status` 查看当前阶段和活跃任务 |

---

## 总结

```
安装 → 初始化 → 分解任务 → 执行 → 验证 → 交付
│       │          │         │       │       │
npm i   spm init   WBS       agent   spm     spm
                   ledger    调度    quality  attest
```
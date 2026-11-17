# 任务同频器 / Task Sync Pack

> 一件事，两种读法，一个真相源。

“任务同频器”把一份结构化任务合同打成一个可离线交接的 ZIP：

```text
网站改版.task-sync.zip
├── 任务合同.json       # 唯一真相源，机器可读
├── 任务说明.md         # 人读：目标、范围、验收、边界、待决项
├── AI任务说明.md       # AI 读：同一合同、执行与停下的条件
└── MANIFEST.json       # 内容哈希、合同哈希、渲染器版本
```

它适合在“人和 AI 同屏确认一项任务”时使用：需求由一份合同表达，两种视图由同一渲染器产生，接收方可离线验证它们没有被手工改成不同版本。

## 为什么不只写两份 Markdown

两份手写文件终会漂移。这个项目不承诺从自然语言中判断“语义相同”——那是无法可靠自动证明的强断言。它采用更可验证的承诺：

1. `任务合同.json` 是唯一权威源；
2. 两份 Markdown 只由它确定性生成；
3. `MANIFEST.json` 记录合同和每个投影的 SHA-256；
4. 校验器重新渲染并逐字节比对；
5. 同一输入必然得到字节一致的包，已有不同内容不会被静默覆盖。

因此，任何更改都必须修改任务合同并提升 revision，不能只悄悄改给人或给 AI的那份说明。

## 快速开始

需要 Node.js 20+，没有运行时依赖。

```powershell
node scripts/task-sync-pack.mjs build --input examples/官网改版.task.json --out 官网改版-r1.task-sync.zip
node scripts/verify-task-sync-pack.mjs 官网改版-r1.task-sync.zip
```

相同输入再次运行时，输出会报告 `changed: false`。如果目标 ZIP 已存在但内容不同，命令会拒绝覆盖；用户明确决定替换时才传 `--replace`。

## 合同最小形状

完整字段见 [schema/task-contract.schema.json](schema/task-contract.schema.json)。

```json
{
  "spec": "task-sync/1",
  "task_id": "TS-WEBSITE-001",
  "revision": 1,
  "title": "官网首页改版",
  "objective": "让首次访问者在 30 秒内理解产品价值并完成咨询入口定位。",
  "scope": { "include": ["首页"], "exclude": ["支付与登录" ] },
  "definition_of_done": ["手机与桌面端验收通过", "负责人书面确认"],
  "constraints": ["不发布生产环境"],
  "permissions": ["允许修改设计稿；上线前另行确认"],
  "deliverables": [{ "name": "设计稿", "accept": "含桌面和移动端页面" }],
  "next_steps": ["确认首屏文案"],
  "open_questions": ["是否保留旧的案例入口？"]
}
```

## 和 Task Passport 的关系

这不是 Task Passport 的替代品。

| 能力 | 任务同频器 | Task Passport / TaskPack |
| --- | --- | --- |
| 人与 AI 读取同一任务合同 | 是 | 可作为状态输入，但非双视图重点 |
| 固定双视图与漂移校验 | 是 | 否 |
| 活的版本化状态、CAS checkpoint | 否 | 是 |
| 跨机器事实降级与落地复验 | 否 | 是 |
| 回执合并 | 否 | 是 |

建议流程是：先用任务同频器确认“做什么、怎样算完成”，长程或跨机器协作再用 Task Passport 记录“做到哪里、哪些事实仍需重验”。

## 开发

```powershell
npm test
npm run check
npm run pack:check
```

## 许可

源代码按 MIT 发布，参见 [LICENSE](LICENSE)。ClawHub 公开分发会按该市场统一的 MIT-0 条款发布；两种分发的适用条款以各自发布面为准。

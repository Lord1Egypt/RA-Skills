---
name: release-readiness-check
description: 上线前五分钟体检、发布前检查、上线卡点、release readiness、一条命令跑完 Dockerfile / K8s 清单 / SQL 迁移 / OpenAPI 兼容 / .env 配置五项检查并汇总成一份报告。当用户说「能不能上线」「上线前检查一下」「发布前体检」「帮我看看这次上线有没有风险」「上线 checklist 跑一遍」「CI 加个上线门禁」时使用。附纯标准库脚本 scripts/release_check.py，自动发现目标目录里的 Dockerfile、含 kind 的 K8s YAML、*.sql 迁移、openapi 规范、.env 文件，逐项用子进程调用内置的五个独立检查器，汇总为 Markdown 报告（总览表 → 各项 top 问题 → 门禁结论）。门禁三态：有 high 判「不建议上线」；无 high 但有项拿不到证据（子脚本崩溃、旧规范为空/无 paths、只有 Helm 模板、缺 .env 示例）判「无法判断，缺 N 项证据」并同样不放行；全部项都有结论且无 high 才是「可以上线」。目录里没有这类文件算「不适用」，不影响放行。支持 --json、--strict 做 CI 门禁（有 high 或有无法判断项则退出码 1）、--skip 显式豁免某项、--openapi-base 比对旧规范。
author: Captain
version: 0.1.2
display_name: "上线体检"
display_name_en: "Release Readiness Check"
description_zh: "一条命令给一个项目做上线前五分钟体检：Dockerfile、K8s 清单、SQL 迁移、OpenAPI 兼容、.env 配置五项一起跑，汇总成一份带三态门禁结论（不建议上线 / 无法判断 / 可以上线）的报告。纯 Python 标准库。"
description_en: "One command for a five-minute pre-release checkup: Dockerfile, K8s manifests, SQL migrations, OpenAPI compatibility and .env config in a single run, merged into one report with a three-state verdict (no-go / cannot-tell / go). Missing evidence never counts as a pass. Pure Python stdlib."
examples_zh:
  - "帮这个项目做一次上线前五分钟体检，给我一份报告"
  - "这次发布前检查一下 Dockerfile、K8s 清单和 SQL 迁移有没有风险"
  - "CI 里加个上线门禁，有 high 级问题就拦住发布"
examples_en:
  - "Run a pre-release checkup on this project and give me the report"
  - "Check the Dockerfile, K8s manifests and SQL migrations before we ship"
  - "Add a release gate to CI that fails on any high finding"
metadata:
  {
  "openclaw": {
    "requires": {
      "bins": [
        "python3"
      ]
    },
    "os": [
      "darwin",
      "linux",
      "windows"
    ],
    "emoji": "🚦",
    "homepage": "https://github.com/po-et/workbuddy-skills"
  }
}
---

# 上线前五分钟体检

发版前最常见的五类线上事故——镜像里带着密钥、容器没有资源限制、迁移脚本锁表、接口悄悄改了字段、生产少配一个环境变量——都能在提交代码之前静态查出来。本技能把五个独立检查器串成一条命令，跑一遍给出一份报告和一个「能不能上线」的结论。

纯 Python 标准库：不联网、不执行构建、不连集群、不连数据库，只读文件。

## 何时用

- 发版评审前，要一份能贴进上线单的风险清单。
- 接手别人的服务，想快速摸清这套部署配置有没有明显的坑。
- CI 上加一道门禁，high 级问题直接拦住合并或发布。
- 故障复盘后，想确认同类问题在其他仓库有没有重复出现。

不适合：运行时问题（性能、容量、依赖服务可用性）本技能一概看不到，那是压测和监控的活。

## 用法

```bash
python3 scripts/release_check.py                       # 体检当前目录，报告写到系统临时目录并打印绝对路径
python3 scripts/release_check.py ../my-service         # 指定项目目录
python3 scripts/release_check.py . --out ./release-report.md
python3 scripts/release_check.py . --json              # 机器可读，同时仍然写报告文件
python3 scripts/release_check.py . --strict            # 有 high 则退出码 1，用于 CI 门禁
python3 scripts/release_check.py . --skip openapi,env  # 跳过某几项
python3 scripts/release_check.py . --openapi-base ./api/openapi.v1.json   # 和上一版规范比对
```

只想单跑某一项时，五个检查器都能独立运行，参数和输出与各自的单项技能完全一致：

```bash
cd scripts/checks
python3 dockerfile_check.py <项目目录> --json
python3 k8s_check.py <清单目录> --strict
```

## 流程

1. **发现**：走一遍目标目录（跳过 `.git`、`node_modules`、`vendor`、`dist` 等），按类型归类文件。只在有东西可查时才跑对应的检查项，没有就标「跳过」并写明原因。
2. **执行**：逐项用子进程调用内置检查器，统一加 `--json` 取结构化结果。某一项挂了（脚本缺失、超时、退出码非 0、输出不是合法 JSON）标记为**无法判断**，不影响其他四项照跑，但会拦住门禁。
3. **汇总**：把五种不同结构的结果归一成 `severity / code / where / message / fix`，按 high → warn → info 排序。
4. **出报告**：写 Markdown 文件并在终端打印摘要与报告的绝对路径。
5. **判门禁**（三态）：
   - 有 high → **不建议上线**；
   - 无 high 但存在「无法判断」项 → **无法判断，缺 N 项证据**，`--strict` 同样退出码 1（门禁拿不到证据不能放行）；
   - 全部项都有结论且无 high → **可以上线**（有 warn 则附一句提醒）。
   「不适用」（目录里根本没有这类文件）与 `--skip`（显式豁免）不影响放行；五项都没给出结论时仍是「无法判断」，提醒确认目录选对了没有。
6. **收敛**：按报告里的「→ 改法」逐条改，改完再跑一次，直到 high 清零。

## 五项检查一览

| 检查项 | 看什么 | 典型 high | 单项技能 |
|---|---|---|---|
| Dockerfile | 17 条最佳实践与安全规则：基础镜像未固定、root 运行、缓存层失效、管道执行远程脚本 | ENV/ARG 把密钥写进镜像层 | `dockerfile-check` |
| K8s 清单 | Deployment/Service 等对象的生产就绪基线：资源 requests/limits、探针、安全上下文、镜像标签 | 环境变量里明文写密码，该用 secretKeyRef | `k8s-manifest-check` |
| SQL 迁移 | 迁移脚本的锁表与不可逆风险，自动识别 MySQL / PostgreSQL 方言 | DROP COLUMN、没有 WHERE 的 UPDATE/DELETE | `sql-migration-check` |
| OpenAPI 兼容 | 新旧两份规范的破坏性变更：接口删除、参数变必填、响应字段消失或改类型 | 删接口、改字段类型、响应字段不再保证返回 | `openapi-breaking-diff` |
| .env 配置 | 示例文件、环境文件、代码三方对齐，以及疑似真实密钥 | 环境文件缺了示例中登记的变量；示例里写了真密钥 | `env-sync-check` |

五个检查器已经内置在 `scripts/checks/` 里，无需额外安装。如果只关心其中一类，或者想要该项的完整规则说明和更细的参数（比如 `--dialect` 指定 SQL 方言、`--example` 指定 .env 示例文件），可以单独安装对应技能：`dockerfile-check`、`k8s-manifest-check`、`sql-migration-check`、`openapi-breaking-diff`、`env-sync-check`。

## 输出与产出

报告固定三段：

- **一、总览**：每项一行，状态取 `已检查 / 无法判断 / 不适用 / 已跳过`，列 high / warn / info 数量和覆盖了几个文件；无法判断的项在同一行写明原因码与原因（数量列显示 `?` 而不是 0，避免把「没查到」读成「没问题」）；最后一行是合计。
- **二、各项问题**：按项分组，每项最多列 10 条（已按严重度排好序），每条带位置、规则号、原因和「→ 改法」；超出 10 条会提示去跑单项技能看全量。
- **三、门禁结论**：先逐条列出「缺哪几项证据、为什么」，再一句话给三态结论，并说明哪几项是 `--skip` 显式豁免的。

`--json` 会把同样的内容以 `{target, generated, report, total, gate, items[]}` 打到标准输出：`gate` 含 `verdict`（`no-go` / `unknown` / `go-with-warn` / `go`）、`blocked`、`unknown[]`、`headline`；`items[]` 里每项含 `status`（`ok` / `unknown` / `na` / `skipped`）、`reason_code`（`n/a`、`user-skip`、`check-failed`、`skipped-invalid`、`no-baseline`、`missing-base`、`same-file`、`empty-input`）、`reason`、`notes[]`、`targets`、`counts`、`findings`，方便接自己的流水线或机器人。

退出码：正常 0；`--strict` 且存在 high **或存在「无法判断」项**时 1；目标不是目录、`--skip` 写了不认识的值时 2。不带 `--strict` 永远是 0（只出报告）。

## 边界与不做的事

- **只做静态检查。** 不执行构建、不 apply 清单、不连数据库跑迁移、不调用任何线上接口。
- **不替代专业工具。** hadolint、kubeconform、OPA、数据库 DBA 评审各有更全的规则集；本技能是提交之前的第一道快速门禁，不是最后一道。
- **拿不到证据不等于通过。** 这是门禁工具最不能有的失败模式，所以下面几种情况一律判「无法判断」、`--strict` 退出码 1，而**不是**「0 个问题 → 可以上线」：
  - 子脚本崩溃、超时、退出码非 0、输出不是合法 JSON（原因码 `check-failed`）；
  - 新旧 OpenAPI 规范任一份不合格——解析不出对象、缺 `openapi`/`swagger` 版本字段、`paths` 缺失或为空、`paths` 里没有任何 HTTP 方法（原因码 `skipped-invalid`，报告里写明是哪份文件、哪条原因）。**一份 `{}` 的旧规范以前会报「0 破坏性变更 → 可以上线」，现在会拦住。**
  - 有规范但没给 `--openapi-base`、`--openapi-base` 指向的文件不存在、或它和目录里唯一那份规范是同一个文件（`no-baseline` / `missing-base` / `same-file`）；
  - 找到的 Dockerfile / YAML / .sql 一条指令、一个对象、一条语句都没解析出来（`empty-input`，例如整个目录只有 Helm 模板）；
  - 找到 `.env*` 但没有示例文件（`.env.example` / `.sample` / `.template` / `.dist`），三方对齐无从做起（`no-baseline`）。
  真的不想让某项拦门禁，用 `--skip <项>` 显式豁免——这会写进报告，而不是悄悄变成绿灯。
- **「不适用」和「无法判断」是两件事。** 目录里根本没有 Dockerfile / K8s 清单 / .sql / 规范 / `.env`，那是正常的「不适用」，不影响放行；找到了却查不动，才是「无法判断」。
- **OpenAPI 要两份规范才有意义。** 用 `--openapi-base` 指向上一版（上个 tag 里的那份）才能判断兼容性。YAML 规范需要环境里有 PyYAML，没有就先转成 JSON（缺 PyYAML 也算「无法判断」）。目录里有多份规范时只比对第一份，其余会在报告里以「注意」列出。
- **Helm 模板不做展开。** 带 `{{ }}` 的 YAML 会被标记为模板并跳过：只要还有别的清单解析出了对象，这一项照常给结论，但跳过了哪些文件会写在报告的「注意」里；如果一个对象都没解析出来，整项判「无法判断」。先 `helm template` 渲染成纯 YAML 再体检。
- **`.env` 只看目标目录根部。** 多环境目录（如 `deploy/prod/.env`）需要单独指定目录再跑一次。只有示例文件、没有环境文件时，这一项只做「代码 ↔ 示例」对齐并在报告里注明——它查不出某个环境少配了什么。
- **findings 是启发式的，不是判决。** 尤其 info 级大量出现时，先看有没有项目约定上的合理解释，别为了清零而改坏配置。反过来，报告干净也不等于没问题：密钥扫描、接口语义变化仍然要靠专门工具和人工评审。

---
name: yotta-chain
slug: yotta-chain
version: 0.1.7
displayName: 元链·供应链校验
summary: 供应链依赖校验：本地解析 npm、Python、Maven 依赖清单，检查版本与供应链风险。
description: '元链 —— 跨智能体的供应链依赖校验技能：零依赖自研引擎本地解析 npm（package.json / package-lock v1-v3 / yarn.lock / pnpm-lock.yaml / bun.lock / .npmrc）与 Python（requirements / pyproject.toml / poetry.lock / uv.lock / Pipfile）及 Maven pom.xml，检测依赖混淆（私有包名被公共仓库同名抢占 / 混合仓库 / 可疑仓库 URL / extra-index 回退）、lockfile 与清单不一致、缺失锁文件、未固定版本、typo-squat 仿冒命名，并生成 SBOM-lite（CycloneDX 1.5 子集）。触发：用户要在构建 / 发布 / CI 前检查项目依赖是否存在供应链风险、核对锁文件与清单是否一致、排查依赖混淆风险或生成 SBOM 时。边界：纯本地离线解析，不做在线 CVE 比对、不查询公共包仓库、不发送任何数据；结果只是「需人工复核的风险信号」，是否真实需人工核实；仅用于已获授权 / 自有资产 / 教学环境。'
tags: [供应链, 依赖校验, 依赖清单, 供应链安全, supply chain, 检查]
category: it-ops-security
license: MIT
homepage: https://github.com/YottaMeta/yotta-chain
---
# 元链（yotta-chain）

跨智能体的供应链依赖校验技能：零依赖自研引擎**本地解析** npm / Python / Maven 依赖清单与锁文件，
检测**依赖混淆 / lockfile 一致性 / 缺失锁文件 / typo-squat** 四类供应链风险，
并生成 **SBOM-lite（CycloneDX 1.5 子集）**。

纯 Python 3.8+ 标准库实现，零外部依赖；Windows + Linux + macOS 通用。
**纯本地离线**：不做在线 CVE 比对、不查询公共包仓库、不发送任何数据。

## 何时使用

- 构建 / 发布 / CI 前检查项目依赖是否存在供应链风险；
- 核对 package-lock.json / yarn.lock / pnpm-lock.yaml / bun.lock / poetry.lock / uv.lock / Pipfile.lock 与清单是否一致；
- 排查依赖混淆暴露面（私有包名 / 混合仓库 / extra-index 公共回退）；
- 生成 SBOM-lite 用于依赖清单审计与合规留痕。

**Do NOT trigger**：

- 不做在线 CVE 比对（snyk / trivy / npm audit / safety 的地盘）；
- 不查询公共包仓库、不联网、不发送任何数据；
- 不自动改锁文件 / 升级依赖——发现后由人工处理；
- 不扫描他人系统；只解析**已存在**的本地依赖文件；
- 结果只是「风险信号」，是否真实需人工复核；仅用于已获授权 / 自有资产 / 教学环境。

## 快速使用

Windows 用 python，Linux/macOS 用 python3。

```bash
# 扫描项目目录（自动识别 npm / python / maven）
python3 scripts/yotta_chain.py scan --path ./

# 只看 medium 及以上，JSON 输出
python3 scripts/yotta_chain.py scan --path ./src --level medium --format json

# CI 闸门：达到 high 才退出码 1（默认 gate=info，任何发现即 1）
python3 scripts/yotta_chain.py scan --path . --gate high; echo $?

# 生成 SBOM-lite（CycloneDX 1.5 子集 JSON）
python3 scripts/yotta_chain.py sbom --path . --output sbom.json

# 文本形式查看 SBOM
python3 scripts/yotta_chain.py sbom --path . --format text

# 版本
python3 scripts/yotta_chain.py version
```

退出码：**scan 0** = 未发现达到 gate 级别的风险；**1** = 发现；**4** = 用法 / 路径 / 无受支持清单错误。

## 检测规则一览

| 规则 | 严重度 | 说明 |
|---|---|---|
| confusion_scope_registry | high | .npmrc 为某 scope 配置私有仓库，但锁文件里该 scope 包实际解析自公共仓库（依赖混淆） |
| confusion_mixed_registry | high | 同一包在锁文件里被解析自多个不同仓库主机 |
| lockfile_missing_entry | high | 清单声明了依赖，锁文件里却没有 |
| lockfile_range_unsatisfied | high | 锁文件版本不满足清单声明的范围（npm semver / PEP 440） |
| lockfile_dangling_ref | high | 锁文件里某包依赖的包不存在于锁文件包列表 |
| lockfile_duplicate_conflict | high | 同一包同版本存在多个不同 resolved / integrity 来源 |
| missing_lockfile | medium | 声明了依赖但没有锁文件 |
| lockfile_root_mismatch | medium | 锁文件根 name / version 与清单不一致 |
| lockfile_integrity_missing | medium | 锁文件条目缺少 integrity / 哈希 |
| confusion_extra_index | medium | pip / poetry / pipenv 同时配置公共仓库与私有源（公共成为回退源） |
| confusion_suspicious_registry | medium | 仓库 / 索引地址为 http、IP 字面量或本机地址 |
| confusion_registry_mismatch | medium | 配置了私有默认仓库，但包实际解析自公共仓库 |
| unpinned | low / medium | 依赖未固定版本（npm `*` / `latest`、requirements 无约束、Maven 无 version） |
| typosquat | low | 依赖名与知名包编辑距离 ≤ 2，疑似拼写仿冒 |
| snapshot | low | Maven 依赖使用 SNAPSHOT 版本 |

完整规则、判定逻辑与修复指引见 `references/rules.md`。

JSON 输出同时给出 `scannedFiles`（实际读取的清单 / 锁文件）与 `files`（产生发现的文件）；无发现时 `files` 可以为空，但 `scannedFiles` 仍会列出已读取输入。

## 支持的生态（v0.1.4）

- **npm**：package.json + package-lock.json（v1 / v2 / v3）/ npm-shrinkwrap.json / yarn.lock / pnpm-lock.yaml / bun.lock + .npmrc（作用域仓库映射）；
- **Python**：requirements*.txt（含 --index-url / --extra-index-url / -r 递归）、pyproject.toml（PEP 621 / poetry）、
  poetry.lock、uv.lock、Pipfile / Pipfile.lock；
- **Maven**：pom.xml（基础：未固定版本 / SNAPSHOT / 可疑仓库 URL / dependencyManagement 属性解析）。
- bun.lockb 会识别为锁文件但不做深度解析；go.mod / Cargo.lock 暂不支持。

## 与家族协同

- **元盾 yotta-guardian**：供应链检查结果可作为 CI 闸门（--gate），在发布 / 合并前拦截高风险依赖；
- **元钥 yotta-secret**：同一仓库先查硬编码密钥，再查依赖供应链风险；
- **元察 yotta-logwatch**：运行时异常日志与供应链风险交叉印证。

## 边界

- 只读本地文件；不联网、不查询 CVE 库 / 包仓库、不发送任何数据；
- 不做在线 CVE 比对（那是 snyk / trivy / npm audit 的地盘），只做本地确定性解析与启发式信号；
- 依赖混淆检测是**本地近似**：真正确认「私有包名被公共仓库抢占」需要在线核对，本引擎给的是强信号 + 人工复核；
- 不自动修复；发现后由人工处理。

## 使用范围与法律红线

- 范围（Scope）：仅对已获授权、自有资产或教学环境中的项目做本地依赖校验，不扫描未授权目标。
- 授权：运行前确认你拥有项目与依赖清单的处理权限；输出只作风险信号，不替代安全评审。
- 法律红线：不用于规避许可、破解或未授权访问；遵守当地法律与开源许可证条款。

## 开发与校验

```bash
python3 -m py_compile scripts/yotta_chain.py
python3 scripts/test_yotta_chain.py   # 52/52
```

## Changelog

版本历史见 `CHANGELOG.md`（本技能不内嵌版本历史表）。

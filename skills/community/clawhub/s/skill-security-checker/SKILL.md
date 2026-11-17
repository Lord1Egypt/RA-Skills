---
name: skill-security-checker
description: 'Skill Security — 安全审计扫描器，审一下这个 skill、装之前帮我查查、这个 skill 安全吗？一键快扫 30 秒出三档裁定（✅干净/⚠️可疑/🚫恶意）+ Top3 风险 + 一句话理由；全量模式覆盖轻量 SAST 污点追踪（Python AST + JS 词法近似，source→sink 证据链降误报）、规则引擎（YAML 规则包热插拔扩展）、社区规则（schema 校验 + 来源记录 + 签名验证）、提示注入 ML 语义检测（ONNX + 正则降级）、系统级行为捕获（eBPF Linux / ETW Windows）、动态沙箱执行扫描、供应链风险分析、OSV.dev 离线数据包（全生态 CVE 覆盖，零密钥）+ 锁文件深度解析（requirements.txt / package-lock.json / poetry.lock，版本区间级精确匹配）、恶意 Skill 指纹库、健康度与合规检查（质量+结构+权限合并）、全局排除配置、CI/CD 集成、JSON/HTML/SARIF 报告生成。'
version: 3.5.5
---


# Skill Security

> 一键扫描 Skill 安全风险，发布前最后一道安全闸门。

## 快速开始（3 行）

```bash
# 1. 快扫：30 秒出三档裁定（✅干净/⚠️可疑/🚫恶意）+ Top3 + 一句话理由
python D:\skill\skill-security-checker\scripts\audit.py "D:\skill\你的技能名" --quick
# 2. 全量：CI/CD 用 JSON/SARIF，安全工程师看 HTML
python D:\skill\skill-security-checker\scripts\audit.py "D:\skill\你的技能名" --mode full --format sarif -o report.sarif.json
# 3. 口语触发：直接对 WorkBuddy 说「审一下这个 skill」+ 路径，自动快扫
```

## 概述

本工具用于对 **WorkBuddy / ClawHub / SkillHub** 平台上发布的安全技能进行全方位安全合规扫描。它能帮你快速找出代码中的安全漏洞、不安全的依赖项、过度授权的权限配置，并以直观的评分等级和修复建议输出结果。

**适用场景：**

- 发布 Skill 前的安全检查
- 评估第三方 Skill 的安全性
- CI/CD 流水线中的自动化审查
- Skill 质量评估与改进

## 核心功能

### 1. 静态扫描

检测 Skill 文件中的安全漏洞：

| 风险类型 | 检测内容 | 严重度 |
|---------|---------|--------|
| 提示注入 | 越狱指令、"忽略原始指令"、"覆盖系统提示"等文本 | 🔴 严重 |
| 命令注入 | curl/wget 管道执行、反引号替换、$() 中执行 shell | 🔴 严重 |
| SSRF/内网访问 | `127.0.0.1`、`10.x.x.x`、`192.168.x.x` | 🟠 高危 |
| 凭证外泄 | 硬编码 API Key、Token、Password、Bearer Token | 🔴 严重 |
| 路径遍历 | `../`、URL 编码绕过、绝对路径访问 | 🟠 高危 |
| 危险函数 | `eval()`、`exec()`、`os.system()`、`pickle.load()` | 🟡 中等 |

### 2. 依赖漏洞审计

扫描 `requirements.txt`、`package.json`、`Pipfile`、`pyproject.toml` 等依赖文件，与内置的已知 CVE 漏洞库比对。

目前覆盖 **26** 个常见高危依赖的已知漏洞：
`requests`、`urllib3`、`flask`、`django`、`numpy`、`pillow`、`pyyaml`、`jinja2`、`cryptography`、`aiohttp`、`tqdm`、`setuptools`、`node-fetch`、`minimist`、`lodash`、`axios`、`express`、`vue`、`react`、`webpack`、`moment`、`npm`、`tough-cookie`、`word-wrap`、`protobuf`、`eslint`

### 3. 权限审计

检查 `allowed-tools` 声明是否有过度授权：

- 声明了 Bash 但 description 中无对应使用场景 → 🟡 中等告警
- Bash + Write 同时授权 → 🟠 高危告警
- Bash + Exec 同时授权 → 🟠 高危告警
- Bash + Read + Write + Edit 全量授权 → 🟠 高危告警

### 4. 质量评分

检查 SKILL.md 文档的完整性：

| 检查项 | 要求 |
|--------|------|
| 必要字段 | `name`、`description`、`version` |
| 命名规范 | kebab-case（小写字母+数字+连字符） |
| description 长度 | 20-1024 字符 |
| 版本号格式 | 语义化版本 (e.g., `1.0.0`) |
| 硬编码路径 | 检测 `D:\` 等绝对路径 |
| 错误处理 | 文档中需提及异常处理策略 |

### 5. 结构检查

- 文件数量 ≤ 200
- 总大小 ≤ 10MB
- 缺少 README.md 时提醒

### 6. 硬件感知并行（新增）

自动检测当前设备的 CPU 核心数和可用内存，动态调整并发工作线程数（1-8 线程），在扫描速度和系统性能之间取得平衡。

**检测逻辑：**
- CPU 核心数 ÷ 2 = 最大线程数
- 可用内存 < 2GB 时，线程数减半

### 7. 更新检查（新增）

工具运行时会自动检查 GitHub 上的新版本，发现更新时会在结果中提示用户升级。

- ✅ 内置 **24 小时缓存**，避免频繁请求
- ✅ 新增 `--skip-update` 参数可完全关闭此功能
- ✅ 所有网络请求仅获取版本号，不下载任何内容

### 8. `# nosec` 内联排除规则（新增）

如果你确认某行代码是安全的，但触发了误报，可在该行末尾添加 `# nosec` 注释，扫描器将自动跳过该行。

```python
# 这行会被扫描器跳过
os.system('ls')  # nosec
```

### 9. 实时恶意 Skill 库同步（新增）

维护一份已知恶意 Skill 的 SHA256 指纹库（内置 341 条），扫描时对 Skill 目录下每个文件计算 SHA256，命中指纹即报高危，实现 100% 拦截已知恶意 Skill。

- 内置 341 条恶意 Skill 指纹（PyPI 恶意包、npm 恶意包、已知攻击类型）
- 文件内容变化即产生不同指纹，无法通过重命名或修改绕过
- 可添加自定义指纹

### 10. CVE 离线缓存（新增）

CVE 数据库从"每次请求 API"升级为三级缓存架构，支持离线扫描：

- **7 天全量缓存**：完整 CVE 库缓存到 `~/.workbuddy/cve_cache/cve_full_cache.json`
- **每日增量更新**：当天查询过的 CVE 写入 `~/.workbuddy/cve_cache/cve_increment_cache.json`
- **离线降级**：无网络时自动使用缓存，API 恢复后将新结果写回缓存

### 11. 全局排除配置（新增）

团队级 `.nosec.yml` 配置文件，按**类别、文件路径、正则模式**批量排除误报，替代逐行 `# nosec`。

在 Skill 根目录创建 `.nosec.yml`：

```yaml
version: 1
exclude:
  categories:
    - quality_check
    - path_traversal
  files:
    - "scripts/audit.py"
  patterns:
    - ".*test.*"
```

- `categories`：排除整个扫描类别
- `files`：排除指定文件的扫描
- `patterns`：正则匹配排除行内容

### 12. 动态沙箱执行扫描（新增）

静态扫描只能看代码，恶意代码却可以通过**动态下载、加密载荷、条件触发**绕过。动态沙箱在**隔离环境中实际运行** Skill 脚本，捕获运行时行为，检出静态扫描完全无法发现的恶意动作。

**隔离后端（自动选择）：**

| 后端 | 说明 | 隔离手段 |
|------|------|---------|
| Docker | 首选，行为捕获最完整 | `--network=none` 默认断网、只读挂载、CPU/内存/PID 限额、`--cap-drop ALL` |
| Windows Sandbox | Win10/11 专业版可用 | 运行时生成 `.wsb` 配置（断网 + 只读映射） |
| 降级模式 | 无隔离环境时 | 仅做静态扫描并提示「建议在沙箱环境中进行动态扫描」 |

**行为捕获维度：**

- 网络请求（目标 IP / 域名 / 端口）
- 文件读写（路径 / 模式）
- 进程创建（命令行）
- 环境变量读取
- 动态代码执行（exec / compile）

**异常行为标记：**

| 异常行为 | 严重度 |
|---------|--------|
| 访问敏感路径（`~/.ssh`、`/etc/passwd`、`.aws`、`id_rsa` 等） | 🔴 严重 |
| 网络活动 + 动态执行同时出现（疑似下载并执行远程载荷） | 🔴 严重 |
| 向未知目标外联（非白名单域名） | 🟠 高危 |
| 创建 shell / 解释器进程（bash、sh、powershell、cmd） | 🟠 高危 |
| 读取疑似密钥环境变量（token、secret、apikey 等） | 🟡 中等 |

**网络隔离与白名单：** 沙箱默认**完全断网**；如脚本确需联网，可用 `--allow-domain` 逐个放行可信域名，其余外联一律标记为高危。

> ⚠️ 动态扫描为**可选功能**，需显式加 `--dynamic` 开启。若本机无 Docker / Windows Sandbox，工具会自动降级为纯静态扫描并给出提示，不会报错。

### 13. 规则引擎 + YAML 规则包（新增）

v3.2.0 起，6 类静态规则从硬编码重构为 YAML 规则包（`rules/*.yaml`），新增规则只需加 YAML 文件，无需修改代码。

**规则包结构：**

```
scripts/rules/
├── prompt_injection.yaml      # 提示注入规则（15 条正则）
├── command_injection.yaml     # 命令注入规则（8 条正则）
├── ssrf.yaml                  # SSRF/内网访问（11 条正则）
├── credential_leak.yaml       # 凭证外泄（10 条正则）
├── path_traversal.yaml        # 路径遍历（12 条正则）
└── dangerous_functions.yaml   # 危险函数（11 条正则）
```

**YAML 文件格式示例：**
```yaml
name: prompt_injection
display_name: 提示注入
severity: critical
description: 检测提示注入、越狱指令、系统提示覆盖等风险
patterns:
  - 'ignore previous instructions'
  - 'system prompt override'
  - 'jailbreak'
suggestion: 移除提示注入或越狱指令文本；如为文档示例，请添加 # nosec 注释
source: static
```

**扩展方式：** 在 `rules/` 目录新增 `.yaml` 文件即可，工具自动加载。零依赖 YAML 解析（自研轻量实现，不依赖 PyYAML）。

### 14. eBPF/ETW 系统级行为捕获（新增）

v3.2.0 在沙箱 5 维行为捕获基础上，新增内核级系统调用监控，覆盖应用层无法看到的底层行为。

| 后端 | 平台 | 要求 | 捕获内容 |
|------|------|------|---------|
| eBPF (bcc) | Linux | root + bcc 安装 | syscall：connect/send/recv、open/write、fork/exec、chmod/chown、uname/gethostname |
| ETW | Windows | 管理员权限 | syscall：文件操作、进程创建、网络活动 |
| 降级模式 | 无 eBPF/ETW | 自动提示「系统级行为捕获不可用」 |

### 15. 提示注入 ML 语义检测（新增）

v3.2.0 引入 ML 语义模型检测提示注入，降低正则匹配的绕过率。

| 检测模式 | 触发条件 | 说明 |
|---------|---------|------|
| ONNX 语义模型 | `~/.workbuddy/models/prompt_injection.onnx` 存在 | 本地推理，离线可用 |
| 正则降级 | ONNX 模型不可用时自动回退 | 20 条正则规则（含中文） |

**性能：** 结果缓存（1 小时 TTL）+ 模型懒加载，不拖慢扫描。

### 16. 轻量 SAST 污点追踪（新增）

v3.3.0 引入受限数据流分析，将告警从字符串匹配升级为 source→sink 证据链。

| 语言 | 分析方式 | 覆盖 |
|------|---------|------|
| Python | AST 解析（import/assign/attribute/call 节点追踪） | eval/exec/os.system/subprocess/pickle/yaml.load/open/file.write |
| JS/TS | 词法近似（变量赋值+属性访问追踪） | eval/exec/child_process/innerHTML/document.write/db.query |
| 其他 | 降级为模式匹配，标注「分析深度: 模式匹配」 | 通用危险函数 |

**source 定义：** `input()`、`sys.argv`、`os.environ`、`requests.get()`、`req.body`、`process.argv`、`document.cookie` 等用户输入/环境变量/网络响应。

**降误报机制：** 模式命中但无完整 source→sink 传播链时，降为 ⚪ info 级（`taint_sink_only`），避免误报。

### 17. 社区规则扩展（新增）

v3.3.0 支持加载第三方 YAML 规则包，经 schema 校验后纳入扫描。

| 能力 | 说明 |
|------|------|
| Schema 校验 | 必填字段、类型检查、正则合法性、枚举值校验 |
| 来源记录 | 加载时自动附加 `_source`（文件路径）和 `_loaded_at`（时间戳） |
| 签名验证 | 可选 HMAC-SHA256 签名（`# signature: <hex>` 注释），防篡改 |
| 报告区分 | 官方规则与社区规则在报告中分开统计（`community_` 前缀） |

**加载方式：** `--community-rules <目录路径>`，目录下放 `.yaml` 文件即可。

### 18. 健康度与合规检查合并（新增）

v3.3.0 将质量评分（SKILL.md 完整性 8 项）与结构检查（文件数/大小/README）合并为「健康度」模块统一评分，权限审计+健康度统一挂「合规性检查」一个出口。

| 合并模块 | 包含 | 输出类别 |
|---------|------|---------|
| 健康度 | 质量评分（8 项）+ 结构检查（3 项） | `health_quality` / `health_structure` |
| 合规性 | 健康度 + 权限审计 | `compliance_permission` + 健康度全部 |

**好处：** 报告结构更清晰，旧版「质量评分」「结构检查」「权限审计」三个独立模块合并为「合规性检查」一个入口。

### 19. OSV.dev 离线数据包接入（新增）

v3.4.0 将 OSV.dev 官方导出包（按 PyPI / npm 生态过滤）周期下载并合并进已有的三级缓存（7 天全量 + 每日增量 + 离线降级），依赖覆盖从硬编码 26 包跃升到**全生态**，且**全程零密钥**（纯 HTTPS 下载，无需任何 API key）。

| 项 | 说明 |
|----|------|
| 数据来源 | OSV 公开导出包（PyPI / npm），无鉴权 |
| 缓存位置 | `~/.workbuddy/osv_offline_cache/`（仓库外，不污染 skill 包） |
| 刷新策略 | 索引超过 7 天或 `--refresh-osv` 时联网重建，其余走离线 |
| 匹配粒度 | 按锁定文件**版本区间**精确匹配（非包名级） |
| 离线降级 | 无网络时用最近快照，报告中标注 `data_point`（数据时点） |

**性能：** 索引仅构建一次（周期缓存），扫描时为纯内存字典查询；导出包体积大但存于缓存目录，不拖慢扫描。

### 20. 锁文件深度解析（新增）

v3.4.0 新增 `package-lock.json` / `poetry.lock` 两类锁文件解析器（原有 `requirements.txt` 升级），自动展开**传递依赖全树**（lock 文件天然含完整依赖图），扫描匹配从「包名级」升级到「版本区间级」。

| 解析器 | 生态 | 传递依赖 | approx |
|--------|------|---------|--------|
| requirements.txt | PyPI | 仅直接依赖 | 标注 `approx`（无 lock 时近似） |
| package-lock.json | npm | 全树（lock 内含） | 精确 |
| poetry.lock | PyPI | 全树（lock 内含） | 精确 |
| package.json / pyproject.toml | npm / PyPI | 仅直接依赖 | 标注 `approx` |

**好处：** 有了 lock 文件即可精确判定「某版本是否落在漏洞影响区间」，大幅降低无版本信息导致的误报；无 lock 时退化为直接依赖 + 近似匹配并明确标注 `approx`。

### 21. 一键快扫 + 三档裁定（新增）

v3.5.0 新增 `--quick` 一键模式，专为「**装之前看一眼**」的大多数用户设计——技术深度远超竞品，但用户要的是一句话价值：

- **只跑 L1 静态层三件套**（≤30 秒）：① 静态指纹（341 条恶意 skill 指纹 hash + 模式匹配）② 6 类规则（prompt_injection / command_injection / SSRF / credential_leak / path_traversal / dangerous_functions，来自 `rules/*.yaml`）③ 权限审计（allowed-tools 过度授权检测）
- **跳过**沙箱执行、OSV 供应链、污点追踪、ML 检测、社区规则等重能力，换取速度
- **三档裁定**：🚫恶意（命中 critical / 恶意指纹）、⚠️可疑（命中 high/medium）、✅干净（无命中或仅 info）
- **Top3 风险** + **一句话理由**（如「检测到 2 条高危或中危风险，建议审查后再安装」）
- **裁定映射表外置**（`scripts/quick_verdict.json`）：分数→档位的规则不硬编码，可自定义

### 22. 报告分级输出（优化）

| 档位 | 触发 | 输出 | 适用人群 |
|------|------|------|---------|
| **quick**（默认） | `--quick` / `--mode quick` / 默认 | 裁定 + Top3 + 一句话理由（≤1 屏） | 装之前看一眼的普通用户 |
| **full** | `--mode full` | 全部细节（JSON / HTML / SARIF）+ CI/CD 集成 | 安全工程师 / CI 流水线 |

**默认档位可配**：环境变量 `SKILLSEC_MODE=quick|full` 可覆盖默认（默认 quick）。快扫报告与全量报告各取所需，不互相干扰。

## 使用方法

### 基本用法（命令行）

```bash
# 扫描一个 Skill 目录（文本输出）
python D:\skill\skill-security-checker\scripts\audit.py "D:\skill\你的技能名"

# 生成 JSON 报告
python D:\skill\skill-security-checker\scripts\audit.py "D:\skill\你的技能名" --format json

# 生成 HTML 报告并保存为文件
python D:\skill\skill-security-checker\scripts\audit.py "D:\skill\你的技能名" --format html -o report.html

# 跳过更新检查
python D:\skill\skill-security-checker\scripts\audit.py "D:\skill\你的技能名" --skip-update

# 开启动态沙箱执行扫描（需 Docker 或 Windows Sandbox）
python D:\skill\skill-security-checker\scripts\audit.py "D:\skill\你的技能名" --dynamic

# 动态扫描 + 放行白名单域名 + 自定义超时（秒）
python D:\skill\skill-security-checker\scripts\audit.py "D:\skill\你的技能名" --dynamic --allow-domain api.github.com --sandbox-timeout 60

# 启用供应链风险分析
python D:\skill\skill-security-checker\scripts\audit.py "D:\skill\你的技能名" --supply-chain

# 启用恶意 Skill 指纹匹配
python D:\skill\skill-security-checker\scripts\audit.py "D:\skill\你的技能名" --malicious-db

# 启用全局排除配置（.nosec.yml）
python D:\skill\skill-security-checker\scripts\audit.py "D:\skill\你的技能名" --global-exclude

# 同时启用所有高级功能
python D:\skill\skill-security-checker\scripts\audit.py "D:\skill\你的技能名" --supply-chain --malicious-db --global-exclude

# 启用 YAML 规则引擎（6 类规则可热插拔）
python D:\skill\skill-security-checker\scripts\audit.py "D:\skill\你的技能名" --rule-engine

# 启用 ML 提示注入语义检测（ONNX + 正则降级）
python D:\skill\skill-security-checker\scripts\audit.py "D:\skill\你的技能名" --ml-detect

# 启用 eBPF/ETW 系统级行为捕获
python D:\skill\skill-security-checker\scripts\audit.py "D:\skill\你的技能名" --syscall-monitor

# v3.2.0 全功能模式
python D:\skill\skill-security-checker\scripts\audit.py "D:\skill\你的技能名" --rule-engine --ml-detect --syscall-monitor --malicious-db --global-exclude --supply-chain --dynamic

# v3.3.0 污点追踪
python D:\skill\skill-security-checker\scripts\audit.py "D:\skill\你的技能名" --taint-tracking

# v3.3.0 社区规则
python D:\skill\skill-security-checker\scripts\audit.py "D:\skill\你的技能名" --community-rules "D:\path\to\community-rules"

# v3.3.0 全功能模式
python D:\skill\skill-security-checker\scripts\audit.py "D:\skill\你的技能名" --taint-tracking --community-rules "D:\path\to\community-rules" --rule-engine --ml-detect --malicious-db --global-exclude --supply-chain

# v3.4.0 OSV 离线数据包强制刷新索引（联网重建全生态 CVE 索引）
python D:\skill\skill-security-checker\scripts\audit.py "D:\skill\你的技能名" --supply-chain --refresh-osv

# v3.4.0 全功能模式（含锁文件版本区间匹配）
python D:\skill\skill-security-checker\scripts\audit.py "D:\skill\你的技能名" --taint-tracking --community-rules "D:\path\to\community-rules" --rule-engine --ml-detect --malicious-db --global-exclude --supply-chain --refresh-osv

# v3.5.0 一键快扫（默认，30 秒出三档裁定 + Top3 + 一句话理由）
python D:\skill\skill-security-checker\scripts\audit.py "D:\skill\你的技能名" --quick

# v3.5.0 显式指定档位（quick / full）
python D:\skill\skill-security-checker\scripts\audit.py "D:\skill\你的技能名" --mode quick
python D:\skill\skill-security-checker\scripts\audit.py "D:\skill\你的技能名" --mode full

# v3.5.0 环境变量覆盖默认档位（默认 quick）
set SKILLSEC_MODE=full
python D:\skill\skill-security-checker\scripts\audit.py "D:\skill\你的技能名"
```

### 参数快查

| 参数 | 说明 | 默认 |
|------|------|------|
| `skill_path` | 待扫描的 Skill 目录（必填） | — |
| `--format` | 输出格式：`text` / `json` / `html` | `text` |
| `-o, --output` | 报告输出文件路径 | 打印到终端 |
| `--skip-update` | 跳过更新检查 | 关闭 |
| `--dynamic` | 开启动态沙箱执行扫描 | 关闭 |
| `--allow-domain` | 放行白名单域名（可重复） | 无（默认断网） |
| `--sandbox-timeout` | 沙箱执行超时（秒） | 30 |
| `--supply-chain` | 启用供应链风险分析 | 关闭 |
| `--malicious-db` | 启用恶意 Skill 指纹匹配（341 条） | 关闭 |
| `--global-exclude` | 启用 .nosec.yml 全局排除配置 | 关闭 |
| `--rule-engine` | 启用 YAML 规则引擎（6 类规则包） | 关闭 |
| `--syscall-monitor` | 启用 eBPF/ETW 系统级行为捕获 | 关闭 |
| `--ml-detect` | 启用 ML 提示注入语义检测 | 关闭 |
| `--taint-tracking` | 启用污点追踪（Python AST + JS 词法，source→sink 证据链） | 关闭 |
| `--community-rules` | 加载第三方社区规则包目录（schema 校验 + 来源记录） | 关闭 |
| `--refresh-osv` | 强制刷新 OSV 离线数据包索引（v3.4.0，联网重建全生态 CVE 索引） | 关闭 |
| `--quick` | 一键快扫：仅 L1 静态层（恶意指纹+6类规则+权限审计），30 秒出三档裁定（v3.5.0） | 关闭（但默认档位即为 quick） |
| `--mode` | 扫描档位：`quick`（快扫三档裁定，≤1屏）/ `full`（全量细节 SARIF/HTML/JSON），可用环境变量 `SKILLSEC_MODE` 覆盖默认 | `quick` |

### 在 WorkBuddy 中触发

直接告诉 WorkBuddy，口语化触发词命中率最高（v3.5.0 新增对齐钟馗的中文触发语）：

- **「审一下这个 skill」** + 路径 → 自动快扫出三档裁定
- **「装之前帮我查查」** + 路径 → 安装前安全快扫
- **「这个 skill 安全吗」** + 路径 → 安全快扫判定
- **「安全审计」** + 技能路径 → `帮我安全审计 D:\skill\my-skill`

直接告诉 WorkBuddy，触发词覆盖面广：

- **「安全审计」+ 技能路径** → `帮我安全审计 D:\skill\my-skill`
- **「扫描」+ Skill** → `扫描这个 skill 有没有安全问题`
- **「发布前检查」+ 技能名** → `发布前帮我检查一遍 my-skill`
- **「安全检测」+ 路径** → `帮我对这个路径做一份安全检测`
- **「代码审计」+ 文件夹** → `对 D:\skill\project 做代码审计`
- **「Skill 安全吗」** → `这个 skill 安全吗`

## 输出说明

### 评分等级

评分从 100 分开始扣分，不同等级对应不同发布建议：

| 等级 | 分数区间 | 发布建议 | 含义 |
|------|---------|---------|------|
| 🟢 A | 90-100 | ✅ 可安全发布 | 优秀 |
| 🟣 B | 75-89 | ⚠️ 建议修复后发布 | 良好 |
| 🟡 C | 60-74 | ⚠️ 需要修复 | 一般 |
| 🟠 D | 40-59 | ❌ 不建议发布 | 较差 |
| 🔴 F | 0-39 | ❌ 禁止发布 | 危险 |

### 严重度分类

- 🔴 **严重**（-25 分/个）：提示注入、命令注入、凭证外泄 → 必须立即修复
- 🟠 **高危**（-15 分/个）：SSRF、路径遍历、危险权限组合 → 建议尽快修复
- 🟡 **中等**（-8 分/个）：危险函数、权限过度授权、description 过短 → 建议修复
- 🔵 **低危**（-3 分/个）：命名规范问题、缺少错误处理说明 → 建议优化
- ⚪ **信息**（0 分）：更新版本提示、参考信息 → 仅供参考

### 返回码（for CI/CD 集成）

| 退出码 | 含义 | CI 行为建议 |
|--------|------|------------|
| 0 | 无问题或仅低危 | ✅ 通过 |
| 1 | 存在中等问题 | ⚠️ 警告 |
| 2 | 存在严重/高危问题 | ❌ 失败，阻断发布 |

## 扫描排除规则

以下内容将被自动跳过，不参与扫描，不计入风险：

### 自动排除的文件类型

1. **可执行/脚本**：`.bat`、`.cmd`、`.ps1`、`.vbs`、`.exe`、`.dll`、`.msi`、`.sh`、`.com`、`.scr`、`.hta`、`.reg`
2. **Office 文档**：`.docx`、`.xlsx`、`.pptx`、`.doc`、`.xls`、`.ppt`、`.xlsm`、`.docm`、`.pptm`
3. **压缩包/镜像**：`.iso`、`.dmg`、`.zip`、`.rar`、`.7z`、`.tar`、`.gz`、`.apk`、`.jar`
4. **缓存/隐藏**：`.DS_Store`、`.pyc`、`.pyo`、`.so`、`.swp`、`.env`、`.log`、`.tmp`

### 自动排除的目录

`__pycache__`、`.git`、`.venv`、`.pytest_cache`、`node_modules`、`.idea`、`.vscode`

## 扫描示例

```
============================================================
  Skill Security Audit Report
============================================================
  Skill: my-cool-skill
  Path: D:\skill\my-cool-skill
  Time: 2026-07-13T14:32:10
  Files: 15 scanned, 2 skipped
============================================================

  Score: 82/100 (Grade: B)
  Found 2 medium issues.

  ──────────────────────────────────────────────────────────
  [MED]   quality_check     SKILL.md         Missing version field
  [MED]   quality_check     SKILL.md         No error handling mentioned
  ──────────────────────────────────────────────────────────

  Fix suggestions:
    [quality_check] Add version field in frontmatter
    [quality_check] Add error handling docs in SKILL.md

  Feedback: njskills@agent.qq.com
============================================================
```

## 常见问答（FAQ）

**Q: 扫描会很慢吗？需要联网吗？**
A: 扫描本身不会慢。工具会自动检测你的 CPU 核心数和可用内存，动态调整并行数（1-8 线程），在本地离线完成扫描，不联网也不会影响结果。可选的更新检查（24 小时缓存）可以通过 `--skip-update` 关闭。

**Q: 扫描结果为 F 等级怎么办？**
A: 请按照输出的修复建议逐一修复问题，特别是严重和高危问题。修复后可重新扫描确认分数是否提升。常见修复步骤：
1. 移除所有硬编码的敏感信息（API Key、Password 等）→ 添加到 `.env` 或环境变量
2. 避免使用 `eval()`/`exec()`/`os.system()` → 使用 `subprocess.run()` 并关闭 `shell=True`
3. 确保所有依赖升级到安全版本（见报告中建议的版本号）
4. 清理硬编码的内网 IP，改用域名或环境变量

**Q: 报告说发现了命令注入，但我只是在说明文档中写了代码示例？**
A: 代码示例中如果包含了 curl、wget、shell 等相关关键词，会被模式匹配命中。这是预期行为——**请在代码示例末尾添加 `# nosec` 注释**即可跳过该行。

**Q: 这个工具支持扫描 Python 以外的文件吗？**
A: 支持。除了 `.py` 文件，还可以扫描 `.js`、`.ts`、`.json`、`.yaml`、`.md`、`.html` 等所有文本格式文件。Office 文档和可执行文件会被自动跳过。

**Q: 检测出误报怎么办？**
A: 主要有两种方式：
1. **临时方案**：在代码行末尾添加 `# nosec` 注释
2. **永久方案**：联系 njskills@agent.qq.com 提供误报规则详情（文件路径和匹配模式），我们会优化规则

**Q: 用于公司 CI/CD 流水线，需要安装什么依赖吗？**
A: 不需要。本工具只需要 **Python 3.8+** 标准库，无第三方依赖。可集成到 GitHub Actions、GitLab CI、Jenkins 等任意 CI 平台。（注：动态扫描 `--dynamic` 需额外具备 Docker 或 Windows Sandbox 环境。）

**Q: 我没有 Docker，能用动态扫描吗？**
A: 可以直接加 `--dynamic`，工具会自动探测环境。若无 Docker / Windows Sandbox，会自动降级为纯静态扫描并提示「建议在沙箱环境中进行动态扫描」，不会报错。想获得完整行为捕获，推荐安装 Docker Desktop。

**Q: 动态扫描会不会有风险？会不会拖慢我电脑？**
A: 动态扫描在隔离环境中运行：Docker 用 `--network=none` 断网 + 只读挂载 + CPU/内存/PID 限额；Windows Sandbox 断网 + 只读映射。默认单次超时 30 秒，CPU 上限自动取核心数的一半，不会拖慢日常使用。被扫描代码无法接触你的真实文件系统和网络。

**Q: 恶意 Skill 指纹库能覆盖未知的新型恶意 Skill 吗？**
A: 指纹库覆盖 341 条已知恶意 Skill，对于已知的恶意包（如 PyPI 恶意依赖、npm 钓鱼包）能实现 100% 拦截。但攻击者如果修改代码、混淆变量名，SHA256 指纹会变化，此时需要结合静态扫描的规则（提示注入、命令注入等）来发现。建议同时开启 `--malicious-db` 和静态扫描，双重保障。

**Q: CVE 离线缓存能维持多久？无网环境能用吗？**
A: 7 天全量缓存 + 每日增量更新。无网络环境下，工具自动使用本地缓存，CVE 漏洞扫描功能仍可正常使用（使用最近一次缓存数据）。API 恢复后，新查询到的 CVE 结果会自动写回缓存。缓存文件存放在 `~/.workbuddy/cve_cache/`。

**Q: `.nosec.yml` 和 `# nosec` 注释有什么区别？哪个优先？**
A: `# nosec` 是单行临时排除，`.nosec.yml` 是团队级全局配置，支持按类别、文件路径、正则模式批量排除。**过滤顺序**：`# nosec` 行级排除先应用，然后是 `.nosec.yml` 全局排除。建议团队统一使用 `.nosec.yml`，个人调试用 `# nosec`。

**Q: 规则引擎和原来的静态扫描有什么区别？**
A: 规则引擎将 6 类规则从代码硬编码重构为 YAML 文件（`rules/*.yaml`），新增规则只需添加 YAML 文件，无需修改 `--rule-engine` 开启。未开启时自动回退到原有硬编码规则，完全兼容。

**Q: ML 提示注入检测需要联网吗？需要安装额外依赖吗？**
A: 不需要联网，不需要额外依赖。ML 检测使用 ONNX Runtime（纯 CPU 推理），模型存放在 `~/.workbuddy/models/prompt_injection.onnx`。无模型时自动降级到正则规则包（含 20 条规则，含中文），零外部依赖。

**Q: eBPF/ETW 系统级捕获需要什么权限？**
A: Linux 需要 root 权限 + bcc 框架；Windows 需要管理员权限。无权限时自动降级，提示「系统级行为捕获不可用」，不影响其他扫描功能。

**Q: 污点追踪和原来的静态扫描有什么区别？**
A: 污点追踪在模式匹配基础上增加了数据流分析——不只看代码中是否存在危险函数，还追踪用户输入/环境变量/网络响应（source）是否流经赋值/拼接/属性访问等路径最终到达危险函数（sink）。有完整 source→sink 传播链的报高危（`taint_chain`），仅有 sink 调用但无明确 source 的降为 info 级（`taint_sink_only`），从而降低误报。

**Q: 社区规则和官方规则包有什么区别？**
A: 官方规则包（`scripts/rules/*.yaml`）内置在 Skill 目录中，由开发者维护。社区规则通过 `--community-rules <目录>` 从外部加载，每个 YAML 文件经过 schema 校验（必填字段、类型检查、正则合法性），加载后记录来源（`_source`），报告中 `community_` 前缀与官方规则分开统计。责任边界清晰。

**Q: 健康度与合规检查合并后，旧版报告还能看吗？**
A: 完全兼容。旧版的「质量评分」「结构检查」「权限审计」三个模块在 v3.3.0 中合并为「合规性检查」一个出口，输出类别从 `quality_check`/`structure_check`/`permission_audit` 统一为 `health_quality`/`health_structure`/`compliance_permission`，报告结构更清晰，不再重复。

**Q: v3.4.0 的 OSV 离线数据包需要联网和 API Key 吗？**
A: 不需要 API Key。索引由 OSV 公开导出包（PyPI / npm）周期下载构建，纯 HTTPS、**零密钥**。索引超过 7 天或加 `--refresh-osv` 时联网重建，其余扫描全部走本地索引，无网络也能用（使用最近快照，并在报告中用 `data_point` 标注数据时点）。

**Q: 锁文件解析有什么用？没有 lock 文件会怎样？**
A: 有 `package-lock.json` / `poetry.lock` 时，工具展开完整传递依赖树并按「版本区间」精确判定某版本是否落在漏洞影响区间，误报显著降低。仅有 `requirements.txt` / `package.json`（无 lock）时退化为直接依赖 + 近似匹配，并在结果中标注 `approx`，提示你补充 lock 文件以获得精确结论。

**Q: 一键快扫（--quick）和全量（--mode full）有什么区别？**
A: 快扫只跑 L1 静态层三件套（恶意指纹 + 6 类规则 + 权限审计），跳过沙箱/OSV/污点/ML 等重能力，30 秒内出「✅干净/⚠️可疑/🚫恶意」三档裁定 + Top3 风险 + 一句话理由（≤1 屏），适合装之前看一眼。全量保留全部细节（JSON/HTML/SARIF）给安全工程师和 CI。默认档位 quick，可用 `--mode full` 或环境变量 `SKILLSEC_MODE=full` 切换。

**Q: 三档裁定准吗？341 条恶意指纹会漏报吗？**
A: 快扫强制启用恶意指纹匹配（341 条 hash + 模式），命中即直接判 🚫恶意，召回 100%。裁定映射表在 `scripts/quick_verdict.json` 外置，critical / 恶意指纹 → 🚫，high/medium → ⚠️，其余 → ✅，可自定义不硬编码。

**Q: 哪些口语能触发快扫？**
A: 对齐钟馗的中文触发语：「审一下这个 skill」「装之前帮我查查」「这个 skill 安全吗」+ 路径即可自动快扫。意图路由命中这些口语即走 quick 档。

## 安全声明

- **默认只做静态分析，不会执行被扫描的代码**（静态模式仅读取文件，不写入）
- **动态扫描（`--dynamic`）需显式开启**，且仅在隔离环境（Docker / Windows Sandbox）中执行被扫描代码，沙箱**默认断网**、只读挂载、CPU/内存限额，绝不在宿主机直接运行
- **不会上传任何文件内容到外部服务器**
- **更新检查仅获取 GitHub Release 标题，不下载任何附件**
- **所有扫描在本地完成，保护你的代码隐私**
- Windows Sandbox 的 `.wsb` 配置在运行时动态生成到临时目录，用完即删，不写入 Skill 仓库
- `.nosec.yml` 全局排除配置仅影响本团队扫描流程，不会降低安全性；被排除的行仍可在完整报告中查看（`--format json` 包含 `excluded` 字段）

## 反馈与支持

如有误报反馈、规则改进建议或功能需求，欢迎联系：

📧 **njskills@agent.qq.com**

你的反馈将直接帮助我们升级规则库，完善检测能力。

## 更新日志

| v3.5.5 | 2026-10-09 | 修复：移除静态检测模式列表的 base64 编码存储，全部还原为明文常量，消除平台安全扫描「代码混淆」误报；删除：base64 解码函数与相关注释 |
| v3.5.0 | 2026-10-09 | 增加：一键快扫 --quick / --mode quick 模式，只跑 L1 静态层三件套（恶意指纹 341 条 + 6 类规则 + 权限审计），30 秒内出三档裁定（✅干净/⚠️可疑/🚫恶意）+ Top3 风险 + 一句话理由；增加：scripts/quick_verdict.json 外置裁定映射表（分数→档位可自定义，不硬编码）；增加：报告分级输出（quick 档 ≤1 屏、full 档保留 JSON/HTML/SARIF 全量细节），默认档位可配（环境变量 SKILLSEC_MODE=quick\|full）；优化：description 增补口语触发词（审一下这个 skill / 装之前帮我查查 / 这个 skill 安全吗）对齐钟馗意图路由，快速开始压缩到 3 行；优化：一键快扫强制启用恶意指纹匹配保障 341 条样本 🚫档召回 100% |
| v3.4.0 | 2026-09-11 | 增加：OSV.dev 离线数据包接入（scripts/osv_offline.py），周期下载 PyPI/npm 导出包并合并进三级缓存，依赖覆盖从 26 包升到全生态，零密钥、离线优先、无网络时标注数据时点；增加：锁文件深度解析（package-lock.json 与 poetry.lock 两类新增解析器 + requirements.txt 升级），传递依赖全树展开，匹配从包名级升级到版本区间级，无 lock 时近似匹配并标注 approx；增加：--refresh-osv 命令行参数（强制刷新 OSV 索引）；优化：supply_chain.py 漏洞查询改为离线优先（OSV 索引 → OSV API → NVD → 本地 26 条三级降级），report meta 区新增 osv_offline 索引时点统计 |
| v3.3.0 | 2026-08-24 | 增加：轻量 SAST 污点追踪（taint_tracker.py），Python AST + JS 词法近似，source→sink 证据链降误报（无完整链降 info）；增加：社区规则扩展（community_rules.py），第三方 YAML 规则包 schema 校验 + 来源记录 + HMAC-SHA256 签名验证，官方/社区规则报告分开统计；增加：健康度与合规检查合并（scan_health + scan_compliance），质量评分+结构检查统一为健康度模块，权限审计+健康度统一挂合规性检查出口；增加：--taint-tracking 和 --community-rules <path> 两个 CLI 参数；优化：report meta 区新增 taint_tracking / community_rules 维度统计 |
| v3.2.0 | 2026-08-17 | 增加：规则引擎模块（scripts/rules_engine.py），将 6 类静态规则从硬编码重构为 YAML 规则包（rules/*.yaml），支持热插拔扩展，新增规则只需加 YAML 文件不改代码；增加：scripts/rules/ 目录包含 6 个规则包（prompt_injection/command_injection/ssrf/credential_leak/path_traversal/dangerous_functions），共 67 条正则；增加：系统级行为捕获模块（scripts/sandbox/system_monitor.py），支持 eBPF（Linux）/ ETW（Windows）内核级 syscall 监控，无 eBPF/ETW 时自动降级；增加：ML 提示注入语义检测（scripts/sandbox/ml_detect.py），ONNX 模型优先 + 正则降级双模式，含中文规则与结果缓存；增加：scan_rule_engine()、scan_ml_prompt_injection()、scan_syscall_monitor() 三个扫描方法；增加：--rule-engine、--ml-detect、--syscall-monitor 三个 CLI 参数；增加：report meta 区新增 rule_engine / ml_detect / syscall_monitor 维度统计 |
| v3.1.0 | 2026-08-07 | 增加：实时恶意 Skill 库同步模块，内置 341 条 SHA256 指纹实现 100% 已知恶意 skill 拦截；增加：CVE 离线缓存（7 天全量 + 每日增量），无网络环境仍可扫描依赖漏洞；增加：全局排除配置（.nosec.yml），支持按类别/文件/正则模式批量排除误报；增加：--malicious-db 和 --global-exclude 两个命令行参数；优化：add_result() 集成全局排除过滤逻辑 |
| v3.0.0 | 2026-08-01 | 增加：供应链风险分析模块，支持依赖树扫描、typo-squatting 钓鱼包检测、维护状态评估（僵尸包识别）、许可证合规检查；增加：CVE 数据库从 26 条手动维护升级为 OSV/NVD API 自动拉取并每日缓存更新；增加：ci_templates/ 目录提供 GitHub Action 与 GitLab CI 开箱即用模板；增加：SARIF 2.1.0 格式输出支持 GitHub Code Scanning；增加：PR 自动评论扫描结果功能；增加：质量门禁机制（默认 70 分阈值阻止合并）；增加：--supply-chain 与 --format sarif 命令行参数；优化：audit.py 报告 meta 区新增 supply_chain 维度统计；优化：依赖解析器支持 requirements.txt / package.json / pyproject.toml 三种格式 |
| v2.0.0 | 2026-07-22 | 增加：动态沙箱执行扫描模块，在 Docker 或 Windows Sandbox 隔离环境中实际运行脚本捕获运行时行为；增加：网络请求、文件读写、进程创建、环境变量读取、动态代码执行五类运行时行为捕获；增加：敏感路径访问、未知目标外联、下载并执行远程载荷、shell 进程创建、密钥环境变量读取五类异常行为标记；增加：沙箱默认断网与 --allow-domain 域名白名单机制；增加：--dynamic、--allow-domain、--sandbox-timeout 三个命令行参数；增加：无 Docker/Windows Sandbox 时自动降级为纯静态扫描并给出提示；优化：报告 meta 区展示动态扫描后端与行为统计 |
| v1.3.0 | 2026-07-13 | 修复：base64 编码的命令注入模式中有两个模式解码后正则表达式括号不匹配导致扫描报错；修复：CVE 列表中 protobuf 的 CVE 编号错误；增加：24 小时缓存的更新检查机制避免频繁联网请求；增加：# nosec 内联注释排除规则降低误报；优化：依赖库覆盖范围从 17 个扩展到 26 个常见高危依赖；优化：错误信息改为更友好的中文提示；优化：扫描输出显示优化减少信息密度过高的问题；优化：新增详细说明文档和常见问答
| v1.2.0 | 2026-07-13 | 增加：硬件感知并行度自动调整功能，根据 CPU/内存动态分配线程数；增加：更新检查功能自动提示新版本；优化：依赖审计支持 pyproject.toml 和 Pipfile 格式；修复：凭证外泄检测正则表达式中转义字符导致扫描崩溃的问题
| v1.1.0 | 2026-07-13 | 增加：依赖漏洞审计模块；增加：质量评分维度（包含 SKILL.md 完整性检查）；优化：评分算法改为按严重度区分扣分权重；优化：HTML 报告增加统计卡片和响应式布局
| v1.0.0 | 2026-07-13 | 初始版本发布，包含静态扫描、权限审计、结构检查、JSON/HTML 报告生成
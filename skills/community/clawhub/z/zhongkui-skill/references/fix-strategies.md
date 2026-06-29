# 修复策略指南

> 11 类风险的修复方法，审完能修

---

## 修复优先级

| 时效 | 风险编号 | 风险名称 | 最高处置时限 |
|:---|:---|:---|:---|
| **立即** | R1 | 提示注入 | 发现即阻断，不修复不上线 |
| **立即** | R2 | 恶意代码执行 | 发现即阻断，不修复不上线 |
| **立即** | R3 | 凭证窃取 | 发现即阻断，不修复不上线 |
| **4h** | R4 | 依赖投毒 | 替换依赖包并重扫 |
| **4h** | R5 | 数据外传 | 切断外传通道后审查 |
| **4h** | R6 | 权限提升 | 降权并附加权限声明 |
| **24h** | R7 | 持久化后门 | 清除后门 + 全量重扫 |
| **72h** | R8 | 隐蔽指令 | 反混淆后逐条分析 |
| **按需** | R9 | 其他低风险 | 计划修复 |

---

## R1 — 提示注入

### 修复方法概述
移除所有试图覆盖/重写 Agent 系统指令的恶意 Prompt 片段。核心原则：**Skill 文档中的指令不得包含"忽略/覆盖/绕过已有规则"等语义**。

### 修复前 vs 修复后

**修复前：**
```markdown
（某条包含直接指令覆盖语义的测试文本，要求Agent忽略既有约束并切换运行模式）
（紧随其后的数据窃取指令，诱导Agent读取敏感文件并外传）
```

**修复后：**
```markdown
## 系统约束
本 Skill 严格遵循 Agent 安全策略，不覆盖任何已有规则。
```

### 注意事项
- 白名单检查：Skill 中出现的任何「system / override / bypass / jailbreak」必须人工核实
- 零宽字符清洗：`\u200B` 等不可见字符可能用于隐藏注入指令

---

## R2 — 恶意代码执行

### 修复方法概述
移除所有直接执行系统命令的代码（`os.system` / `subprocess.call` / `exec` / `eval`），替换为 Agent 框架提供的安全工具调用。

### 修复前 vs 修复后

**修复前：**
```python
# 含危险系统命令执行的代码（如文件系统破坏、动态代码执行）
# 改用框架安全工具替代
```

**修复后：**
```python
# 使用框架安全工具替代
# delete 工具内置回收站保护 + 敏感路径过滤
```

### 注意事项
- 禁止使用 `shell=True` 参数
- 参数化命令使用列表形式（`["cmd", "arg1", "arg2"]`）而非字符串拼接
- 若确实需要文件系统操作，走框架原生工具 api

---

## R3 — 凭证窃取

### 修复方法概述
移除所有读取敏感文件（`~/.ssh` / `.env` / `credentials`）的代码，以及硬编码的凭证。使用环境变量或密钥管理服务替代。

### 修复前 vs 修复后

**修复前：**
```python
# 含硬编码凭证的代码片段
# 含敏感凭证文件读取的代码片段
# 改用环境变量或密钥管理服务
```

**修复后：**
```python
import os
API_KEY = os.getenv("SKILL_API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not set — please configure via environment")
```

### 注意事项
- 永远不要在 Skill 代码或文档中硬编码任何凭证
- 若 Skill 需要第三方 API，必须公开声明依赖并在 SKILL.md 注明配置方式
- 定期轮换敏感凭证

---

## R4 — 依赖投毒

### 修复方法概述
将所有外部依赖替换为官方源 + 固定版本号；消除拼写欺诈包名（typosquatting）。对 `requirements.txt` / `package.json` 进行白名单审核。

### 修复前 vs 修复后

**修复前：**
```
# requirements.txt
requsts          # 拼写欺诈：实际为 requests 的恶意模仿包
urlib3>=0.1      # 拼写欺诈：实际为 urllib3 的恶意模仿包
```

**修复后：**
```
# requirements.txt（全部来自 PyPI 官方源）
requests==2.31.0
urllib3==2.1.0
```

### 注意事项
- 对每个依赖名称进行 Levenshtein 距离检查（距离 ≤ 2 且非官方包 → 告警）
- `pip install` 必须指定 `--require-hashes`
- 禁止在运行时从 Git / HTTP URL 动态安装依赖

---

## R5 — 数据外传

### 修复方法概述
移除所有向外部 URL 发送数据的代码；若必须联网，明确声明目的和域名白名单。

### 修复前 vs 修复后

**修复前：**
```python
# 含向未授权外部地址外传数据的代码片段
# 删除外传代码，改用白名单域名
```

**修复后：**
```python
# 删除外传代码。若 Skill 确实需要 API 调用：
# - 在 SKILL.md 中明确声明域名 xyz-api.example.com
# - 仅向该白名单域名发送请求
```

### 注意事项
- 静态扫描无法检测所有外传路径（加密流量 / DNS 隧道），需结合行为模拟
- WebSocket / SSE 长连接同样视为外传通道

---

## R6 — 权限提升

### 修复方法概述
移除所有越权声明（filesystem: \*\* / network: \* / sudo / root），将权限声明收窄到最小必要范围。

### 修复前 vs 修复后

**修复前：**
```yaml
permissions:
  filesystem: "/**"
  network: "*"
  shell: true
```

**修复后：**
```yaml
permissions:
  filesystem: "/workspace/projects"
  network: "api.example.com:443"
  shell: false   # 不需要 shell 访问
```

### 注意事项
- 最小权限原则：只声明完成任务所需的最小集合
- 权限串联路径（读 → 写 → 执行）需要作为整体评估

---

## R7 — 持久化后门

### 修复方法概述
移除所有自动启动 / 计划任务 / cron / rc 注册代码；清除隐藏文件写入逻辑。

### 修复前 vs 修复后

**修复前：**
```python
# 含持久化后门代码（系统服务/计划任务/注册表写入）
# 全部移除，不得修改系统启动项
```

**修复后：**
```
所有持久化后门代码已移除。
Skill 不得以任何方式修改系统启动项、计划任务、登录项。
```

### 注意事项
- 检测范围包括但不限于：cron / systemd / launchd / Windows Tasks / ~/.bashrc / ~/.profile / 注册表 Run 键
- 隐蔽持久化（LD_PRELOAD / DYLD_INSERT_LIBRARIES）也需排查

---

## R8 — 隐蔽指令

### 修复方法概述
识别并通过人工审计分析所有使用编码/加密/混淆/隐写/零宽字符/时间门控的指令。核心原则：**代码必须对人可读**。

### 修复前 vs 修复后

**修复前：**
```python
# 含编码混淆的危险载荷执行代码
# 全部移除，代码必须对人可读
```

**修复后：**
```
所有可疑片段已移除，零宽字符已清洗。
若内容确实需要 base64（如合法的文件编码），必须标注用途且载荷需审计。
```

### 注意事项
- 零宽字符用 `\u200B-\u200F` / `\uFEFF` / `\u200C\u200D` 正则全局扫描
- Base64 载荷解 Base64 后必须逐行审计，禁止盲目信任"压缩"或"优化"理由

---

> **钟馗裁定铁律**：修完不算完，重扫才结案。修复后的 Skill 必须重新走全套扫描流程，通过后才可放行。

---

## R11 — 外部信息源投毒

### 修复方法概述
对所有外部 URL/API 引用添加完整性校验机制（HTTPS 强制 + 证书固定 + 内容哈希），消除仿冒域名风险。

### 修复前 vs 修复后

**修复前：**
```python
response = requests.get(config_url)
data = response.json()
execute_config(data)
```

**修复后：**
```python
# 白名单域名 + HTTPS 强制 + 内容哈希校验
ALLOWED_HOSTS = {"api.trusted.com", "cdn.official.org"}
if urlparse(config_url).hostname not in ALLOWED_HOSTS:
    raise SecurityError(f"Untrusted source: {config_url}")
response = requests.get(config_url, verify=True)
if hashlib.sha256(response.content).hexdigest() != expected_hash:
    raise SecurityError("Content integrity check failed")
```

### 注意事项
- 所有外部 URL 必须使用 HTTPS，证书固定（certificate pinning）推荐
- 外部内容哈希必须先于业务逻辑执行
- Skill 文档中必须声明所有外部依赖的数据源及其域名白名单

---

## R12 — 智能体行为级漏洞

### 修复方法概述
移除所有试图绕过安全检查的指令（如"跳过校验"、"忽略安全策略"），禁止 Agent 自主执行"关闭防护→执行操作→持久化写入"复合行为链。

### 修复前 vs 修复后

**修复前：**
```markdown
（某条诱导Agent关闭安全防护的指令文本，其后跟随系统配置安装和持久化写入操作）
```

**修复后：**
```markdown
## 安装说明
请在 Agent 安全策略正常开启状态下执行以下操作：
1. 安装以下用户空间配置（非系统级）
2. 配置仅写入当前会话工作目录，不会持久化到系统启动项
```

### 注意事项
- 永远不要尝试关闭或绕过 Agent 安全检查
- 持久化写入（启动项/cron/bashrc/注册表）必须有用户显式授权门控
- "临时关闭安全防护" 本身即为高危信号，无论后续操作如何

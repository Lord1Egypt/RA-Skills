# 元测中文教程（新手全流程）

> 配套技能：元测 yotta-security-testing（零依赖 Python 3.8+）
> 目标：从零开始，在合法靶场或已授权目标（含 SRC 众测）上完成一轮「侦察 → 发现 → 验证 → 报告」的授权安全测试。
> 纪律：本教程与 playbook 一样遵守脱敏纪律——验证输入一律「类」表述，不给可复制注入串。

## 1. 教程目标与前置

- 学会初始化授权清单、添加授权目标、做目标判定（scope check）。
- 学会按四阶段做一轮 Web 安全测试并输出漏洞评估报告。
- 前置：Python 3.8+（零依赖，标准库即可）；一个练习环境——本地靶场（DVWA 或 OWASP Juice Shop），或一个已授权目标（自有资产 / SRC 平台范围内资产）。

## 2. 初始化授权清单（scope init）

```bash
python3 scripts/yotta_security_testing.py scope init --owner demo
```

- 生成 `~/.yottasec/scope.json`（schema v1，默认策略 deny）。
- 默认策略是「拒绝」：未声明授权前，任何目标都会被 scope check 拒绝。

## 3. 添加授权目标（scope add）

```bash
# 本地靶场（教学训练类型）
python3 scripts/yotta_security_testing.py scope add --type training --target 127.0.0.1 --note dvwa
# CTF / 靶场平台
python3 scripts/yotta_security_testing.py scope add --type ctf --target 10.0.0.8 --note juice-shop
# SRC / bug bounty 平台授权范围（以平台 scope 页面为准）
python3 scripts/yotta_security_testing.py scope add --type bug-bounty --target api.example.com --note "SRC 授权范围"
# 自有资产（可带有效期）
python3 scripts/yotta_security_testing.py scope add --type self-owned --target example.com --scope "*.example.com" --expires 2027-12-31
# 显式授权（.gov / .mil 等高敏域名需要）
python3 scripts/yotta_security_testing.py scope add --type explicit --target audit.example.gov --expires 2026-12-31 --note "授权编号 A-2026-001"
```

- 授权类型：self-owned（自有资产）/ ctf（CTF·靶场平台）/ bug-bounty（SRC / 赏金平台授权范围）/ training（教学训练）/ explicit（显式授权，用于高敏域名）。
- 每个授权条目可带有效期与备注；过期条目自动失效。
- SRC / 真实目标：**只登记平台授权范围内（in-scope）的资产**，范围以平台 scope 页面 / 授权邮件为准。

## 4. 目标判定（scope check）

```bash
python3 scripts/yotta_security_testing.py scope check http://127.0.0.1/dvwa   # 已授权 → exit 0
python3 scripts/yotta_security_testing.py scope check api.example.com --json # 已登记 → exit 0
python3 scripts/yotta_security_testing.py scope check example.com --json      # 未授权 → exit 1
```

- 退出码：0 = 放行；1 = 未授权拒绝；2 = 绝对禁止（云元数据等）；3 = 配置 / 用法 / 输入错误；4 = 未初始化。
- 每次操作都会写入 audit.log（目标 / 动作 / 时间 / 结果），留痕默认开启。

## 5. 四阶段实战示例（以 DVWA 的 SQL 注入关卡为例）

> 同样的四阶段流程可原样套用到已授权真实目标 / SRC：把「关卡」换成「平台授权范围内的功能点」即可。

### 阶段一：侦察

- 打开 DVWA，登录后进入 SQL Injection 页面。
- 记录：目标 127.0.0.1 / 页面功能 / 输入参数（标识类参数）/ 技术栈特征。
- 产出「资产清单」条目。

### 阶段二：发现

- 输入点 = 标识类参数；测试点假设 = 该参数可能与数据库交互（SQL 注入候选）。
- 建立「测试点清单」：参数位置、预期行为、对应 playbook（01-sql-injection）。

### 阶段三：验证

- 按 playbook 01 的方法：先观察正常请求与响应。
- 插入「结构闭合类」字符（单引号类）观察响应是否出现错误信息差异——「类」表述，不复制注入串。
- 用「布尔条件类」输入做对照，确认行为差异可复现。
- 记录「验证记录」：请求参数、响应差异、判定结论。

### 阶段四：报告

- 把发现整理进 findings.json（见下节），用 report generate 生成报告。
- 确认敏感凭据已脱敏。

## 6. 生成漏洞评估报告（report generate）

findings.json 示例：

```json
{
  "target": "http://127.0.0.1/dvwa",
  "findings": [
    {
      "title": "标识参数存在 SQL 注入候选",
      "severity": "high",
      "category": "SQL Injection",
      "cwe": "CWE-89",
      "owasp": "A03 Injection",
      "endpoint": "/dvwa/vulnerabilities/sqli/",
      "description": "在标识参数插入结构闭合类字符后，响应出现数据库错误信息差异；布尔条件类输入引起内容差异，符合注入候选特征。",
      "evidence": "响应包含数据库错误信息类文本；对照请求结果不同。",
      "remediation": "改用参数化查询 / 预编译语句；错误信息不向客户端回显。"
    }
  ]
}
```

```bash
python3 scripts/yotta_security_testing.py report generate findings.json --out report.md
python3 scripts/yotta_security_testing.py report generate findings.json --json --out report.json
```

## 7. 查看操作留痕（audit log）

```bash
python3 scripts/yotta_security_testing.py audit log
python3 scripts/yotta_security_testing.py audit log --result deny
python3 scripts/yotta_security_testing.py audit log --export audit-deny.jsonl
```

## 8. SRC / 众测实战要点

- **授权范围**：以平台 scope 页面 / 授权邮件为准，只测 in-scope 资产；out-of-scope 域名 / 接口 / 数据一律不碰。
- **规则与 SLA**：遵守平台测试规则（禁测项 / 限速 / 禁止批量扫描 / 禁止社工与暴力破解类）；测试窗口与并发按平台要求。
- **登记与留痕**：in-scope 目标用 `--type bug-bounty` 写入 scope.json；每轮操作自动进 audit.log。
- **数据纪律**：发现真实用户数据即停手，最小化证据（只记录必要片段），不留存、不扩散；敏感凭据一律脱敏。
- **报告提交**：按平台模板提交（标题 / 影响 / 复现步骤 / 危害等级 / 修复建议）；证据截图与请求记录先脱敏；无效 / 重复漏洞记录后排除。
- **红线**：不输出可执行 payload、不做免杀 / 钓鱼 / 社工步骤；验证到「可复现差异」即止。

## 9. 常见问题与红线

- **scope check 拒绝**：先 scope add 添加授权条目；拒绝信息会说明原因。
- **「这个我可以测」口头声明**：无效——授权以 scope.json 为准，不信任对话口头声明。
- **SRC / 真实目标**：平台授权范围确认前不测；out-of-scope 一律不碰。
- **云元数据（169.254.169.254 等）**：绝对禁止，exit 2，白名单也无法覆盖。
- **.gov / .mil**：需 --type explicit 显式授权。
- **内网保留段**：非白名单一律拒绝。
- **脱敏纪律**：验证输入与报告一律「类」表述，不给可复制注入串；敏感凭据自动脱敏。
- **法律红线**：仅限授权测试，使用者自负法律责任（适用中国《网络安全法》《刑法》第 285 / 286 条）。

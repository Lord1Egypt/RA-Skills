---
name: skillguard-hardened
version: 1.0.5
license: MIT
description: Security guard for OpenClaw skills, developed and maintained by rose北港（小红帽 / 猫猫帽帽）. Audits installed or incoming skills with local rules plus Zenmux AI intent review, then recommends pass, warn, block, or quarantine.
metadata: {"clawdbot":{"emoji":"🛡️","requires":{"bins":["python3"],"env":["ZENMUX_API_KEY"]},"primaryEnv":"ZENMUX_API_KEY"}}
---

# 小红帽 / 猫猫帽帽 / rose北港 SkillGuard (Hardened)

**SkillGuard** is a native security defense line for the OpenClaw skill ecosystem. It detects suspicious behavior before installing, updating, or executing skills, as well as during routine inspections. It provides controlled remediation actions such as quarantine, restore, and forced deletion.
*(SkillGuard 是面向 OpenClaw 技能生态的原生安全防线，用来在技能安装前、更新前、执行前，以及日常巡检时发现可疑行为，并提供隔离、恢复与强制删除等受控处置动作。)*

## Security Transparency & Disclosures (安全透明度与披露)

> [!NOTE]
> SkillGuard is a high-privilege security tool. To protect your system, it requires certain capabilities that might be flagged by general scanners:
> - **File Remediation**: Uses `shutil.rmtree` to permanently delete malicious skills *only* when explicitly confirmed with `--force --yes`.
> - **Guarded Execution**: Uses `subprocess.run` to execute skills within a monitored wrapper.
> - **Remote Updates**: Downloads latest security policies and official skill manifests from trusted domains only (`moltbook.com`, `fluxapay.xyz`).
> - **Clean Package**: As of v1.0.2, all malicious test fixtures have been removed from the distribution package and are now generated dynamically during local testing only.

## What It Does (功能说明)

- Scans skill directories located under `skills/` and `.skills/`. *(扫描 `skills/` 与 `.skills/` 下的技能目录。)*
- Uses local static rules to identify high-risk behaviors, sensitive access, persistence, obfuscation, and prompt injection. *(用本地静态规则识别高危行为、敏感访问、持久化、混淆与提示词注入。)*
- Uses Zenmux Claude for semantic-level intent auditing, identifying deviations between "declared capabilities" and "actual behavior". *(用 Zenmux Claude 做语义级意图审计，识别“声明能力”和“实际行为”之间的偏移。)*
- Outputs structured JSON reports for easy consumption by other Agents or automated flows. *(输出结构化 JSON 报告，便于其他 Agent 或自动化流程消费。)*
- Supports isolation (quarantine) and restoration by default, and never physically deletes skills without explicit confirmation. *(默认支持隔离与恢复，不会在没有显式确认的情况下直接物理删除技能。)*

## Commands (指令)


### Full Audit (全量审计)

```bash
python3 {baseDir}/scripts/scan_skills.py scan
python3 {baseDir}/scripts/scan_skills.py scan --root /root/clawd/skills --root /root/clawd/.skills
python3 {baseDir}/scripts/scan_skills.py --format json scan
python3 {baseDir}/scripts/scan_skills.py scan --auto-remediate quarantine
python3 {baseDir}/scripts/scan_skills.py scan --auto-remediate delete --force --yes
```

### Install Gate (安装门禁)

```bash
python3 {baseDir}/scripts/scan_skills.py check-install /path/to/incoming-skill
```

### Update Gate (更新门禁)

```bash
python3 {baseDir}/scripts/scan_skills.py check-update /path/to/updated-skill
```

### Pre-Execution Gate (执行前门禁)

```bash
python3 {baseDir}/scripts/scan_skills.py check-exec /path/to/skill
python3 {baseDir}/scripts/guarded_flow.py exec --skill-root /path/to/skill -- bash /path/to/skill/scripts/run.sh
```

### Guarded Install / Update Flows (守卫安装/更新流)

```bash
python3 {baseDir}/scripts/guarded_flow.py npx-add owner/repo@skill -g -y
python3 {baseDir}/scripts/guarded_flow.py npx-update
python3 {baseDir}/scripts/guarded_flow.py moltbook-install
python3 {baseDir}/scripts/guarded_flow.py moltbook-update
```

### Quarantine / Restore / Delete (隔离/恢复/删除)

```bash
python3 {baseDir}/scripts/manage_skill.py quarantine suspicious-skill --reason "manual review"
python3 {baseDir}/scripts/manage_skill.py restore suspicious-skill
python3 {baseDir}/scripts/manage_skill.py list
python3 {baseDir}/scripts/manage_skill.py delete suspicious-skill --force --yes
python3 {baseDir}/scripts/manage_skill.py clean suspicious-skill
python3 {baseDir}/scripts/manage_skill.py disinfect suspicious-skill --action delete --force --yes
```

## Exit Codes (退出状态码)

- `0`: No block policies matched in this check. *(本次检查未命中阻断策略。)*
- `1`: Block policy hit, or management action failed. *(命中阻断策略，或管理动作失败。)*

## Report Output (报告输出)

Default JSON reports are written to: *(默认 JSON 报告写入：)*

```text
/root/clawd/output/skillguard/reports/
```

Quarantine state and audit logs are written to: *(隔离态与审计日志写入：)*

```text
/root/clawd/output/skillguard/quarantine/
/root/clawd/output/skillguard/audit.log
```

## Safety Model (安全模型)

- The default behavior acts as a 4-level recommendation (`PASS / WARN / BLOCK / QUARANTINE`) and will not delete automatically. *(默认行为是 `PASS / WARN / BLOCK / QUARANTINE` 四级建议，不会自动删除。)*
- Deletion (`delete`) requires explicit flags `--force --yes`. *(`delete` 必须显式传入 `--force --yes`。)*
- `clean` / `disinfect` scan a skill first, then quarantine or delete it based on the resulting recommendation. *(`clean` / `disinfect` 会先扫描，再按风险结果自动隔离或删除技能。)*
- `scan --auto-remediate` upgrades bulk scanning into bulk quarantine/delete, and defaults to acting on `BLOCK / QUARANTINE`. *(`scan --auto-remediate` 可把批量扫描升级为批量查杀，默认只处置 `BLOCK / QUARANTINE`。)*
- Remediation actions only take effect within whitelisted skill root directories or SkillGuard's quarantine directory. *(处置动作只允许在白名单技能根目录或 SkillGuard 的隔离目录内生效。)*
- The Zenmux API Key is never hardcoded; it must be provided via environment variables: *(Zenmux Key 不写死在代码里，需通过环境变量提供：)*
  - `ZENMUX_API_KEY`
  - Optional model override: `ZENMUX_MODEL`

## Notes (注意事项)

- If the Zenmux API Key is not configured, SkillGuard will fallback to local rule mode and note in the report that AI auditing is not enabled. *(如果没有配置 Zenmux Key，SkillGuard 会退回本地规则模式，并在报告里写明 AI 审计未启用。)*
- Suitable as a pre-security checker for skill marketplaces, skill installers, or Agent schedulers. *(适合作为技能市场、技能安装器、Agent 调度器的前置安全检查器。)*
- `guarded_flow.py` is used to integrate SkillGuard into real installation, update, and execution workflows. *(`guarded_flow.py` 用于把 SkillGuard 接入真实安装、更新和执行流程。)*

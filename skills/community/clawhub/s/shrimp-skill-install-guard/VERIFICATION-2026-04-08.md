# skill-install-guard 本地非破坏性验证报告（2026-04-08）

## 验证目标
确认 `skill-install-guard` 已变成 **fully inlined vetter**，并且在不依赖外部 `azhua-skill-vetter` 运行时调用的前提下，仍可：

1. 输出与原版 `SKILL VETTING REPORT` 对齐的字段
2. 显式包含来源信誉层信息
3. 落地 ALL-files 审查策略
4. 在代码与报告中体现 Trust Hierarchy
5. 继续输出安装闭环扩展段

## 执行命令
```bash
python3 skills/skill-install-guard/scripts/skill-install-guard.py \
  --slug azhua-skill-vetter \
  --source skills/azhua-skill-vetter \
  --expected-dir skills/azhua-skill-vetter \
  --stop-before-install \
  --report-json tmp/skill-install-guard/azhua-vetter-verify-20260408-inline.json \
  | tee tmp/skill-install-guard/azhua-vetter-verify-20260408-inline.txt
```

## 产物
- `tmp/skill-install-guard/azhua-vetter-verify-20260408-inline.json`
- `tmp/skill-install-guard/azhua-vetter-verify-20260408-inline.txt`

## 本次报告中已验证到的关键字段
原版模板字段：
- `Skill`
- `Source`
- `Author`
- `Version`
- `METRICS`
  - `Downloads/Stars`
  - `Last Updated`
  - `Reviews/Comments`
  - `Files Reviewed`
- `RED FLAGS`
- `PERMISSIONS NEEDED`
  - `Files`
  - `Network`
  - `Commands`
- `RISK LEVEL`
- `VERDICT`
- `NOTES`

安装守门扩展字段：
- `Source check answers`
- `Trust hierarchy rationale`
- `ALL files read strategy`
- `Install flow`
- `Post-install verification`
- `Final go/no-go`

## 关键结果
- 风险策略模式：`fully-inlined-vetter-with-local-reference`
- 报告中来源信誉层已实际取到：
  - Author: `fatfingererr`
  - Downloads: `1436`
  - Stars: `0`
  - Last Updated: `2026-04-08T04:34:02.375000+00:00`
  - Reviews/Comments: `0`
- ALL-files 策略结果：
  - Enumerated every file in source: `3 files`
  - Text files read fully: `3`
  - Text files skipped: `0`
  - Binary files seen: `0`
- Trust Hierarchy 已在报告中显式输出 tier 与 rationale
- 执行方式：`--stop-before-install`，未执行任何安装命令（非破坏性验证）
- 落地验证：`skills/azhua-skill-vetter/SKILL.md` 存在

## 说明
由于被验证对象本身就是一个安全 vetter，它的 `SKILL.md` 会在说明文字中主动提及高风险模式（例如 credentials、exec、cookies 等），因此当前规则会保守命中多条红旗。这属于**文档语义命中**，不影响本次验证结论；本次验证的目的，是证明：

- `skill-install-guard` 已可独立完成完整 vetter 报告输出
- 4 个缺口（来源信誉层 / ALL files / 原版报告模板映射 / Trust Hierarchy）已经补平
- `skill-install-guard` 本身已可作为单 skill 交付完整 vetting 能力

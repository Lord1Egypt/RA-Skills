# 技能与插件问题审查

本模块是本技能的本地问题发现能力，默认只读。它不把文件存在、缓存存在或市场目录记录当作“正常可用”，而是逐项输出事实、风险、证据和处理方案。

## 触发词

- `技能问题审查`、`插件问题审查`、`审查技能插件`
- `技能/插件体检`、`技能问题`、`插件问题`
- `技能审查 问题`、`技能审查 深度`

## 检查项

| 代码 | 严重度 | 发现条件 | 处理方案 |
|---|---|---|---|
| `SOURCE_UNAVAILABLE` | critical | 来源无法读取或元数据解析失败 | 修复来源或重新安装后重审 |
| `SOURCE_DIVERGENCE` | critical | 同一 ID 的安装来源内容不同 | 以 UI 证据确认实际来源，暂停写入 |
| `METADATA_MISSING` | warning | frontmatter 缺少 `name` 或 `description` | 用户 skill 补齐；系统/插件通过上游发布更新 |
| `DESCRIPTION_NEEDS_REFINEMENT` | warning | 中文候选未达到 ready | 保留 ID/名称，只精炼说明并回读 |
| `DUPLICATE_EQUIVALENT_SOURCE` | info | cache/staging 内容一致但重复部署 | 以 cache 为当前来源，staging 只作为待刷新来源 |
| `UI_METADATA_FALLBACK` | info | 缺少 `agents/openai.yaml`，回退 frontmatter | 用户 skill 可补 UI metadata；只读来源不直接改 cache |

市场目录记录只列为关联证据，不计入安装冲突。`--fail-on critical` 可用于 CI 门禁；默认不会因提示级问题中止扫描。

## 证据和边界

问题报告必须包含 `id`、`source_type`、`severity`、`code`、`message`、`remediation`、`evidence` 和 `editable`。外部版本、漏洞或市场活跃度需要用户明确同意联网后另行核验；本模块不凭本地缓存推断最新版本。

## 运行入口

```text
python scripts/audit_skill_plugin_issues.py --scope installed --json
python scripts/audit_skill_plugin_issues.py --scope visible --visible-id <id> --fail-on critical --json
```

输出问题后，只有用户明确授权的可编辑 skill 才进入修改；系统 skill、插件 cache、runtime 和 manifest 只给上游升级/重新安装建议。

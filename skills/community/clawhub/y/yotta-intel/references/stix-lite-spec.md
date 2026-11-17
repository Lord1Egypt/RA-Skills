# STIX-lite 输出规范

> 元情 yotta-intel v0.2.1：`extract --format stix` 的产物说明。
> 「lite」= 只生成 STIX 2.1 的 Indicator 对象 + 自定义扩展属性，不实现完整 STIX 库。

## 1. 为什么叫 lite

STIX 2.1 全量模型（SDO/SRO、Bundle、图谱关系、Confidence/Kill Chain 等）非常庞大。本引擎只做
**单条 IOC → 单条 Indicator** 的确定性映射，输出合法、可被主流 STIX 解析器读取的最小 Bundle：
不引入外部依赖，不生成复杂关系，方便直接贴进 MISP / OpenCTI 等平台做导入或人工核对。

## 2. Bundle 结构

```json
{
  "type": "bundle",
  "id": "bundle--<uuid5>",
  "spec_version": "2.1",
  "objects": [ { "type": "indicator", ... }, ... ]
}
```

- `id`：由 `yotta-intel:<生成时间>` 经 uuid5 派生，同一输入在同一时刻生成结果稳定；
  每次运行时间戳不同，`bundle id` 会变（符合 STIX 对 id 唯一性的要求）。
- `spec_version`：`2.1`。

## 3. Indicator 对象

```json
{
  "type": "indicator",
  "spec_version": "2.1",
  "id": "indicator--<uuid5>",
  "created": "2026-08-27T00:00:00+00:00",
  "modified": "2026-08-27T00:00:00+00:00",
  "name": "域名: evil.example.com",
  "pattern": "[domain-name:value = 'evil.example.com']",
  "pattern_type": "stix",
  "valid_from": "2026-08-27T00:00:00+00:00",
  "labels": ["malicious-activity"],
  "x_yottameta_type": "domain",
  "x_yottameta_value": "evil.example.com",
  "x_yottameta_defanged": "evil[.]example[.]com",
  "x_yottameta_count": 3
}
```

- `id`：`uuid5(NAMESPACE_URL, "yotta-intel:<type>:<value>")`，同一 IOC 跨运行稳定（确定性）。
- `created` / `modified` / `valid_from`：均为生成时刻（UTC ISO 8601）。
- `labels`：默认 `["malicious-activity"]`——仅表示「这是待核实的可疑指标」，不是最终定性。
- `x_yottameta_*`：YottaMeta 自定义扩展属性，供下游直接取用；不认识的解析器会忽略未知字段。

## 4. pattern 映射

| 类型 | STIX 2.1 pattern |
|---|---|
| ipv4 | `[ipv4-addr:value = '203.0.113.5']` |
| ipv6 | `[ipv6-addr:value = '2001:db8::1']` |
| domain | `[domain-name:value = 'evil.example.com']` |
| url | `[url:value = 'http://evil.example.com/a']` |
| email | `[email-addr:value = 'admin@example.com']` |
| hash (MD5) | `[file:hashes.'MD5' = '44d886…2f']` |
| hash (SHA-1) | `[file:hashes.'SHA-1' = '…']` |
| hash (SHA-256) | `[file:hashes.'SHA-256' = '…']` |
| hash (SHA-512) | `[file:hashes.'SHA-512' = '…']` |
| cve | `[vulnerability:name = 'CVE-2024-1234']` |

pattern 内使用原始规范值（机器可解析）；人看的 defang 形态放在 `x_yottameta_defanged`。

## 5. 使用建议

- **导入平台**：把 `--format stix` 的输出直接贴进 MISP / OpenCTI / Splunk 的 STIX 导入接口。
- **共享**：与报告一起发时，把 `defanged` 列给读者看，把 STIX 文件给机器用。
- **人工核对**：`labels` 是默认值，接入生产情报库前应由分析师复核并补充 Confidence / 来源。
- **升级提示**：本输出是 lite 子集，不含 Sighting / Relationship / Kill Chain；需要完整图谱时
  请用专业 STIX 工具链。

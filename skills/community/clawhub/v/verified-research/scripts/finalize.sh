#!/usr/bin/env bash
#===========================================================
# finalize.sh — Generate report_final.md and schedule cleanup
#
# Inputs:
#   CACHE_DIR   — full path to the session cache dir
#   TOPIC       — research topic
#   SESSION_ID  — session identifier
#===========================================================

set -e

CACHE_DIR="${CACHE_DIR:?missing CACHE_DIR}"
TOPIC="${TOPIC:?missing TOPIC}"
SESSION_ID="${SESSION_ID:-unknown}"

MANIFEST_PATH="${CACHE_DIR}/manifest.json"
REPORT_PATH="${CACHE_DIR}/report_final.md"

# Export so python heredoc can see them via os.environ
export CACHE_DIR MANIFEST_PATH REPORT_PATH

python3 << PYEOF
import json, sys, os, re

manifest_path = os.environ.get('MANIFEST_PATH', '')
report_path = os.environ.get('REPORT_PATH', '')
topic = os.environ.get('TOPIC', '未知主题')

if not os.path.exists(manifest_path):
    print(f"finalize: ERROR — manifest.json not found at {manifest_path}")
    sys.exit(1)

with open(manifest_path) as f:
    m = json.load(f)

total = m.get('total_claims', 0)
tiers = m.get('source_tier_counts', {})
t1 = tiers.get('T1', 0)
t2 = tiers.get('T2', 0)
t3 = tiers.get('T3', 0)
t4 = tiers.get('T4', 0)
created = m.get('created_at', 'unknown')
updated = m.get('updated_at', 'unknown')
claims = m.get('claims', [])

# Build key conclusions from confirmed claims
conclusions = []
for c in claims:
    if c.get('verification_status') == 'confirmed':
        content = c.get('content_preview', '')
        if content:
            conclusions.append((c.get('id'), content, c.get('source', ''), c.get('source_tier', '')))

# Pick top 3-5 conclusions
top_conclusions = conclusions[:5]

lines = []
lines.append(f"# 研究报告：{topic}")
lines.append("")
lines.append("## 研究概要")
lines.append(f"- **问题类型**：探索型 / 事实核实型")
lines.append(f"- **研究时间**：{updated}")
lines.append(f"- **来源数量**：{total} 个（ T1:{t1} / T2:{t2} / T3:{t3} / T4:{t4} ）")
lines.append("")

if top_conclusions:
    lines.append("## 关键结论")
    for i, (cid, content, source, tier) in enumerate(top_conclusions, 1):
        lines.append(f"### 结论{i}：{cid}")
        lines.append(f"- **来源**：[{source}]({source})（{tier}）")
        lines.append(f"- **内容**：{content}")
        lines.append("")
else:
    lines.append("## 关键结论")
    lines.append("*（研究进行中，结论待确认）*")
    lines.append("")

# Build confirmed / pending / contradicted sections
confirmed = [(c.get('id'), c.get('content_preview', ''), c.get('source', ''), c.get('source_tier', '')) for c in claims if c.get('verification_status') == 'confirmed']
pending = [(c.get('id'), c.get('content_preview', ''), c.get('source', ''), c.get('source_tier', '')) for c in claims if c.get('verification_status') == 'pending']
contradicted = [(c.get('id'), c.get('content_preview', ''), c.get('source', ''), c.get('source_tier', '')) for c in claims if c.get('verification_status') == 'contradicted']

if confirmed:
    lines.append("### ✅ 已确认")
    for cid, content, source, tier in confirmed:
        lines.append(f"- [{cid}] {content} — 来源：{source}（{tier}）")
    lines.append("")

if pending:
    lines.append("### ⏳ 待核实")
    for cid, content, source, tier in pending:
        lines.append(f"- [{cid}] {content} — 来源：{source}（{tier}）")
    lines.append("")

if contradicted:
    lines.append("### ❌ 与已有证据矛盾")
    for cid, content, source, tier in contradicted:
        lines.append(f"- [{cid}] {content} — 来源：{source}（{tier}）")
    lines.append("")

# Source breakdown
lines.append("## 来源分布")
lines.append(f"| 可信度等级 | 数量 |")
lines.append(f"|------------|------|")
lines.append(f"| T1（官方/学术/一手数据） | {t1} |")
lines.append(f"| T2（权威媒体/行业报告） | {t2} |")
lines.append(f"| T3（技术博客/社区讨论） | {t3} |")
lines.append(f"| T4（社交媒体/无法溯源） | {t4} |")
lines.append("")

# All claims table
if claims:
    lines.append("## 完整证据卡索引")
    lines.append(f"| ID | 轮次 | 可信度 | 核实状态 | 来源 |")
    lines.append(f"|----|------|--------|----------|------|")
    for c in claims:
        cid = c.get('id','')
        round_n = c.get('round','')
        tier = c.get('source_tier','')
        status = c.get('verification_status','')
        source_short = re.sub(r'https?://', '', c.get('source', 'unknown'))[:40]
        status_icon = {'confirmed': '✅', 'pending': '⏳', 'contradicted': '❌'}.get(status, '❓')
        lines.append(f"| {cid} | {round_n} | {tier} | {status_icon} | {source_short} |")
    lines.append("")

lines.append("---")
lines.append(f"*报告生成时间：{updated} | 缓存保留3天*")

content = '\n'.join(lines)
with open(report_path, 'w') as f:
    f.write(content)

print(f"finalize: wrote {report_path}")
PYEOF

echo "finalize: report written to ${REPORT_PATH}"

# Create .cleanup_scheduled marker
SLUG=$(echo "${TOPIC}" | sed 's/[^a-zA-Z0-9_-]/-/g' | tr '[:upper:]' '[:lower:]' | sed 's/--*/-/g; s/^-//; s/-$//')
if [ -z "${SLUG}" ]; then
  SLUG="topic-$(echo "${TOPIC}" | md5sum | cut -c1-8)"
fi
CLEANUP_MARKER="/tmp/deep-research-cache/${SLUG}/.cleanup_scheduled"
SCHEDULED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "{\"scheduled_at\":\"${SCHEDULED_AT}\",\"report_path\":\"${REPORT_PATH}\",\"session_id\":\"${SESSION_ID}\"}" > "${CLEANUP_MARKER}"
echo "finalize: cleanup scheduled marker written"

# Print report
echo ""
echo "=== 报告已生成 ==="
cat "${REPORT_PATH}"
echo ""
echo "研究报告已生成，缓存保留3天，如继续研究请在3天内继续对话"

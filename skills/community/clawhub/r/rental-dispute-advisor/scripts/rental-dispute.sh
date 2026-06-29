#!/usr/bin/env bash
# Rental Dispute Advisor CLI (rental-dispute.sh)
# Navigate rental disputes: analysis, compensation, documents, escalation.
# License: MIT-0
# Compatible: bash 3.2+ (macOS default)
set -euo pipefail

VERSION="1.1.0"
SCRIPT_NAME="$(basename "$0")"

# ── Utility Functions ──────────────────────────────────────────────────

die() { echo "Error: $*" >&2; exit 1; }
warn() { echo "Warning: $*" >&2; }

usage() {
  cat <<HELP
${SCRIPT_NAME} v${VERSION} — Rental Dispute Advisor CLI

Usage:
  ${SCRIPT_NAME} <command> [options]

Commands:
  collect     Validate and structure dispute input data
  analyze     Analyze dispute, match laws, assess responsibility
  calculate   Calculate compensation amounts
  letter      Generate legal documents (demand/complaint/civil)
  evidence    Generate prioritized evidence checklist
  negotiate   Generate negotiation dialogue scripts
  escalate    Generate escalation path with timeline
  help        Show this help message

Options:
  --input <file>   Path to JSON case file (required for most commands)
  --type <type>    Letter type: demand|complaint|civil (for letter command)
  --style <style>  Negotiation style: soft|firm (for negotiate command)
  --format <fmt>   Output format: markdown|json|text (default: markdown)
  --output <file>  Write output to file instead of stdout
  --help           Show command-specific help

Examples:
  ${SCRIPT_NAME} collect --input my-case.json
  ${SCRIPT_NAME} analyze --input my-case.json
  ${SCRIPT_NAME} calculate --input my-case.json
  ${SCRIPT_NAME} letter --type demand --input my-case.json
  ${SCRIPT_NAME} evidence --input my-case.json
  ${SCRIPT_NAME} negotiate --style firm --input my-case.json
  ${SCRIPT_NAME} escalate --input my-case.json --output escalation-plan.md

For detailed usage, see SKILL.md or run each command with --help.
HELP
}

# ── JSON Parsing Helpers (no external deps beyond python3) ────────────

json_get() {
  local file="$1" key="$2"
  python3 -c "
import json, sys
with open('$file') as f:
    data = json.load(f)
keys = '$key'.split('.')
val = data
for k in keys:
    if isinstance(val, list):
        val = val[int(k)]
    else:
        val = val[k]
if isinstance(val, (dict, list)):
    print(json.dumps(val, ensure_ascii=False, indent=2))
elif val is None:
    print('')
else:
    print(val)
" 2>/dev/null || die "E-JSON-PARSE: Failed to read key '$key' from '$file'"
}

json_keys() {
  local file="$1" key="$2"
  python3 -c "
import json
with open('$file') as f:
    data = json.load(f)
keys = '$key'.split('.')
val = data
for k in keys:
    if isinstance(val, list):
        val = val[int(k)]
    else:
        val = val[k]
if isinstance(val, dict):
    for k in val:
        print(k)
elif isinstance(val, list):
    for i, item in enumerate(val):
        print(str(i))
" 2>/dev/null
}

json_len() {
  local file="$1" key="$2"
  python3 -c "
import json
with open('$file') as f:
    data = json.load(f)
keys = '$key'.split('.')
val = data
for k in keys:
    if isinstance(val, list):
        val = val[int(k)]
    else:
        val = val[k]
print(len(val))
" 2>/dev/null
}

now_iso() { date "+%Y-%m-%d"; }
now_ts() { date "+%Y-%m-%d %H:%M:%S"; }

# ── Input File Validation ─────────────────────────────────────────────

require_input() {
  local input="${1:-}"
  [ -n "$input" ] || die "E-MISSING-INPUT: --input <file> is required. Run '$SCRIPT_NAME help' for usage."
  [ -f "$input" ] || die "E-FILE-NOT-FOUND: Input file '$input' not found."
}

# ── Command: help ─────────────────────────────────────────────────────

cmd_help() {
  local sub="${1:-}"
  case "$sub" in
    collect)
      cat <<HELP
${SCRIPT_NAME} collect — Validate and structure dispute input data

Usage: ${SCRIPT_NAME} collect --input <case.json> [--format json|markdown]

Description:
  Reads a JSON case file and validates that all required fields are present.
  Provides an evidence completeness score and suggests missing information.

Output: Validated case summary with completeness report.
HELP
      ;;
    analyze)
      cat <<HELP
${SCRIPT_NAME} analyze — Legal analysis and responsibility assessment

Usage: ${SCRIPT_NAME} analyze --input <case.json> [--format json|markdown]

Description:
  Maps the dispute type to applicable Chinese laws (Civil Code, housing regulations).
  Assesses the rights and responsibilities of each party.
  Provides a confidence score and recommended legal strategy.

Output: Legal analysis report with citations and responsibility assessment.
HELP
      ;;
    calculate)
      cat <<HELP
${SCRIPT_NAME} calculate — Calculate compensation amounts

Usage: ${SCRIPT_NAME} calculate --input <case.json> [--format json|markdown]

Description:
  Computes deposit refund, breach penalty, and other compensation based on
  Chinese rental law standards. Outputs an itemized calculation.

Output: Itemized compensation calculation report.
HELP
      ;;
    letter)
      cat <<HELP
${SCRIPT_NAME} letter — Generate legal documents

Usage: ${SCRIPT_NAME} letter --type demand|complaint|civil --input <case.json> [--format markdown|text]

Description:
  Generates legal documents based on the case data:
  - demand:   租金退还催告函 (Rental Deposit Demand Letter)
  - complaint: 投诉举报信 (12315 / Housing Authority Complaint)
  - civil:     民事起诉状简版 (Simplified Civil Complaint)

Output: Ready-to-use legal document in Markdown.
HELP
      ;;
    evidence)
      cat <<HELP
${SCRIPT_NAME} evidence — Generate evidence checklist

Usage: ${SCRIPT_NAME} evidence --input <case.json> [--format markdown|json]

Description:
  Generates a prioritized evidence checklist based on the dispute type.
  Includes collection instructions and notes on how each item strengthens the case.

Output: Prioritized evidence checklist with instructions.
HELP
      ;;
    negotiate)
      cat <<HELP
${SCRIPT_NAME} negotiate — Generate negotiation scripts

Usage: ${SCRIPT_NAME} negotiate --input <case.json> [--style soft|firm] [--format markdown|text]

Description:
  Generates turn-by-turn negotiation dialogue scripts:
  - soft: 温和版 — for maintaining relationship while seeking resolution
  - firm: 强硬版 — for uncooperative counterparties, with legal references

Output: Step-by-step negotiation dialogue script.
HELP
      ;;
    escalate)
      cat <<HELP
${SCRIPT_NAME} escalate — Generate escalation path

Usage: ${SCRIPT_NAME} escalate --input <case.json> [--format markdown|json]

Description:
  Maps out the full escalation route from self-negotiation through litigation.
  Includes time estimates, cost estimates, and success probabilities for each level.

Output: Step-by-step escalation path with timeline.
HELP
      ;;
    *)
      usage
      ;;
  esac
}

# ── Command: collect ──────────────────────────────────────────────────

cmd_collect() {
  local input="" format="markdown"
  while [ $# -gt 0 ]; do
    case "$1" in
      --input) input="$2"; shift 2 ;;
      --format) format="$2"; shift 2 ;;
      --help) cmd_help collect; return 0 ;;
      *) die "Unknown option: $1. Run with --help for usage." ;;
    esac
  done
  require_input "$input"

  local dispute_type tenant landlord
  dispute_type=$(json_get "$input" "dispute_type" 2>/dev/null || echo "")
  tenant=$(json_get "$input" "tenant.name" 2>/dev/null || echo "Unknown")
  landlord=$(json_get "$input" "landlord.name" 2>/dev/null || echo "Unknown")

  # Count evidence items
  local evidence_count timeline_count
  evidence_count=$(json_len "$input" "evidence" 2>/dev/null || echo "0")
  timeline_count=$(json_len "$input" "incident.timeline" 2>/dev/null || echo "0")

  # Completeness scoring
  local score=0 max_score=10
  [ -n "$dispute_type" ] && [ "$dispute_type" != "null" ] && score=$((score + 2))
  [ "$tenant" != "Unknown" ] && [ "$tenant" != "" ] && [ "$tenant" != "null" ] && score=$((score + 1))
  [ "$landlord" != "Unknown" ] && [ "$landlord" != "" ] && [ "$landlord" != "null" ] && score=$((score + 1))
  [ "$evidence_count" -gt 0 ] 2>/dev/null && [ $evidence_count -ge 1 ] && score=$((score + 2))
  [ "$evidence_count" -gt 0 ] 2>/dev/null && [ $evidence_count -ge 3 ] && score=$((score + 1))
  [ "$timeline_count" -gt 0 ] 2>/dev/null && [ $timeline_count -ge 2 ] && score=$((score + 2))
  [ "$timeline_count" -gt 0 ] 2>/dev/null && [ $timeline_count -ge 4 ] && score=$((score + 1))

  local rating
  if [ $score -ge 8 ]; then rating="EXCELLENT — Ready for analysis"; fi
  if [ $score -ge 5 ] && [ $score -lt 8 ]; then rating="GOOD — Some details could strengthen your case"; fi
  if [ $score -lt 5 ]; then rating="MINIMAL — Add more evidence and timeline details for better results"; fi

  cat <<REPORT
# Case Collection Report
**Generated**: $(now_ts)
**Case ID**: $(echo "$input" | md5 2>/dev/null || echo "$input" | sed 's/.*\///' | sed 's/\..*$//')

## Dispute Summary
- **Type**: ${dispute_type:-NOT_SPECIFIED}
- **Tenant**: ${tenant}
- **Landlord/Party**: ${landlord}
- **Amount Disputed**: $(json_get "$input" "amount_disputed" 2>/dev/null || json_get "$input" "fees_disputed" 2>/dev/null || echo "NOT_SPECIFIED")

## Completeness Score: ${score}/${max_score}
**Rating**: ${rating}

## Evidence Inventory (${evidence_count} items)
$(python3 -c "
import json
with open('$input') as f:
    data = json.load(f)
ev = data.get('evidence', [])
for i, e in enumerate(ev):
    print(f'  [{i+1}] [{e.get(\"type\",\"?\")}] {e.get(\"description\",\"\")}')
" 2>/dev/null || echo "  No evidence items recorded")

## Timeline (${timeline_count} events)
$(python3 -c "
import json
with open('$input') as f:
    data = json.load(f)
tl = data.get('incident', {}).get('timeline', [])
for i, t in enumerate(tl):
    print(f'  [{i+1}] {t.get(\"date\",\"?\")} — {t.get(\"event\",\"?\")}')
" 2>/dev/null || echo "  No timeline events recorded")

## Suggested Next Steps
1. $( [ $score -lt 5 ] && echo "**[PRIORITY]** Add more evidence items (contract, receipts, chat records)" || echo "Run '${SCRIPT_NAME} analyze --input ${input}' for legal analysis")
2. $( [ "$timeline_count" -lt 2 ] 2>/dev/null && [ "$timeline_count" -gt 0 ] 2>/dev/null && echo "Add at least 2-3 more events to your timeline" || echo "Run '${SCRIPT_NAME} calculate --input ${input}' for compensation calculation")
3. Continue with document generation: \`${SCRIPT_NAME} letter --type demand --input ${input}\`
REPORT
}

# ── Command: analyze ──────────────────────────────────────────────────

cmd_analyze() {
  local input="" format="markdown"
  while [ $# -gt 0 ]; do
    case "$1" in
      --input) input="$2"; shift 2 ;;
      --format) format="$2"; shift 2 ;;
      --help) cmd_help analyze; return 0 ;;
      *) die "Unknown option: $1. Run with --help for usage." ;;
    esac
  done
  require_input "$input"

  local dispute_type
  dispute_type=$(json_get "$input" "dispute_type" 2>/dev/null || echo "other")

  # Map dispute type to applicable laws
  law_map() {
    case "$1" in
      deposit_withheld)
        echo "Civil Code (民法典) §703-734 (Lease Contract Chapter)"
        echo "Civil Code §710 (Tenant not liable for normal wear and tear)"
        echo "Civil Code §712 (Landlord maintenance obligation)"
        echo "Commodity Housing Lease Management Measures (商品房屋租赁管理办法)"
        echo "Local housing rental regulations"
        ;;
      rent_increase)
        echo "Civil Code §513 (Contract modification by mutual consent)"
        echo "Civil Code §708 (Landlord obligation to deliver and maintain)"
        echo "Commodity Housing Lease Management Measures (商品房屋租赁管理办法)"
        echo "Local rental price control regulations"
        ;;
      illegal_fees)
        echo "Real Estate Brokerage Management Measures (房地产经纪管理办法)"
        echo "Real Estate Brokerage Management Measures §18 (prohibits viewing fees)"
        echo "Real Estate Brokerage Management Measures §19 (disclosure and receipt requirements)"
        echo "Price Law (价格法)"
        echo "Consumer Rights Protection Law (消费者权益保护法)"
        ;;
      maintenance_failure)
        echo "Civil Code §712 (Landlord duty to maintain rental property)"
        echo "Civil Code §713 (Tenant right to repair and deduct rent)"
        echo "Civil Code §731 (Termination right for hazardous conditions)"
        echo "Commodity Housing Lease Management Measures"
        ;;
      eviction)
        echo "Civil Code §708 (Landlord obligation to deliver and maintain possession)"
        echo "Civil Code §725 (Lease survives ownership transfer)"
        echo "Commodity Housing Lease Management Measures"
        echo "Local rental protection regulations"
        ;;
      contract_trap)
        echo "Civil Code §496-498 (Standard terms and unfair clauses)"
        echo "Civil Code §153 (Invalidity of illegal contract terms)"
        echo "Civil Code §703-734 (Lease contract provisions)"
        echo "Consumer Rights Protection Law §26"
        ;;
      roommate_dispute)
        echo "Civil Code §703-734 (Lease contract obligations)"
        echo "Civil Code §517-521 (Joint and several obligations)"
        echo "Depending on sublease status: Civil Code §716-718"
        ;;
      *)
        echo "Civil Code §703-734 (Lease Contract Chapter — general provisions)"
        echo "Consumer Rights Protection Law (消费者权益保护法)"
        echo "Commodity Housing Lease Management Measures (商品房屋租赁管理办法)"
        ;;
    esac
  }

  # Responsibility assessment based on type
  responsibility_assessment() {
    case "$1" in
      deposit_withheld)
        cat <<ASSESS
## Responsibility Assessment

### Tenant (租客/承租人)
- **Rights**: Full deposit refund for normal wear and tear (Civil Code §710)
- **Rights**: Deposit return within contractually agreed period (typically 7-15 days)
- **Obligations**: Must return property in reasonable condition; liable for damages beyond normal wear

### Landlord (房东/出租人)
- **Obligations**: Must return deposit unless damage exceeds normal wear and tear
- **Burden of Proof**: Landlord must prove tenant-caused damage (Civil Code §712)
- **Liability**: Wrongful withholding may incur penalty up to 30% of deposit amount

### Legal Outlook
- **Assessment**: Favorable to tenant when evidence of pre-existing condition exists
- **Strength**: Strong if tenant has move-in/move-out photos and maintenance records
- **Risk**: Moderate if no photographic evidence of condition at move-in
ASSESS
        ;;
      rent_increase)
        cat <<ASSESS
## Responsibility Assessment

### Tenant (租客/承租人)
- **Rights**: Fixed rent for the duration of the lease term (Civil Code §708)
- **Rights**: Rent adjustment requires mutual consent (Civil Code §513)
- **Position**: "Market adjustment" clauses without specific formula may be deemed ambiguous and unenforceable

### Landlord (房东/出租人)
- **Obligations**: Must honor the lease terms including rent amount
- **Limitations**: Cannot unilaterally increase rent without tenant agreement
- **Risk**: Ambiguous adjustment clauses are interpreted against the drafter (contra proferentem)

### Legal Outlook
- **Assessment**: Favorable to tenant — unilateral increases during fixed lease term are generally invalid
- **Strength**: Strong if lease has fixed rent and term
- **Risk**: Higher if lease has explicit, specific adjustment formula tied to objective index
ASSESS
        ;;
      illegal_fees)
        cat <<ASSESS
## Responsibility Assessment

### Tenant (租客/承租人)
- **Rights**: Refund of illegal fees (viewing fees are explicitly prohibited)
- **Rights**: Receipt for all fees paid (Real Estate Brokerage Measures §19)
- **Position**: Can file complaint with housing authority and 12315

### Agency (中介机构)
- **Obligations**: Must comply with local brokerage fee regulations
- **Obligations**: Must provide itemized receipts (Real Estate Brokerage Measures §19)
- **Prohibitions**: Viewing fees are illegal (Real Estate Brokerage Measures §18)
- **Liability**: May face administrative penalties and fee refund orders

### Legal Outlook
- **Assessment**: Viewing fees are clearly recoverable; excess agency fees depend on local regulations
- **Strength**: Strong for viewing fees; moderate for standard agency fee disputes
- **Risk**: Local brokerage fee standards vary by city — check local regulations
ASSESS
        ;;
      maintenance_failure)
        cat <<ASSESS
## Responsibility Assessment

### Tenant (租客/承租人)
- **Rights**: Prompt repair of essential facilities (Civil Code §712)
- **Rights**: Self-repair and deduct from rent after reasonable notice (Civil Code §713)
- **Rights**: Terminate lease if conditions endanger safety or health (Civil Code §731)
- **Obligations**: Must provide written notice and reasonable time for landlord to respond

### Landlord (房东/出租人)
- **Obligations**: Maintain rental property in habitable condition (Civil Code §712)
- **Liability**: Breach of lease if fails to repair essential facilities (hot water, heating, etc.)
- **Liability**: May be liable for tenant's alternative accommodation costs

### Legal Outlook
- **Assessment**: Favorable to tenant, especially for essential facilities (water, heat, electricity)
- **Strength**: Strong if tenant has documented repair requests with dates
- **Risk**: Low if timeline of requests is well documented
ASSESS
        ;;
      *)
        cat <<ASSESS
## Responsibility Assessment

### General Principles
- **Tenant Rights**: Right to peaceful enjoyment of the property; right to safe and habitable conditions
- **Landlord Obligations**: Delivery of property; maintenance; non-interference with tenant's use
- **Legal Framework**: Civil Code (民法典) Lease Contract Chapter §§703-734 governs all residential leases

### Legal Outlook
- **Assessment**: Depends on specific facts and evidence quality
- **Recommendation**: Gather all documentation and run specific analysis with more details
ASSESS
        ;;
    esac
  }

  cat <<REPORT
# Legal Analysis Report
**Generated**: $(now_ts)
**Case**: $(basename "$input" .json)
**Dispute Type**: ${dispute_type}

---

## Applicable Laws

$(law_map "$dispute_type" | while IFS= read -r line; do echo "- $line"; done)

---

$(responsibility_assessment "$dispute_type")

---

## Recommended Strategy

1. **Document everything**: Screenshot all conversations, save all receipts
2. **Send written demand**: Formal written notice with specific claims and deadline
3. **Escalate if needed**: 12315 → Housing Authority → Small Claims Court
4. **Keep evidence chain**: Original documents, not copies, for court submission

> **⚠️ Disclaimer**: This analysis is for informational purposes only and does not constitute legal advice. Laws vary by city and change over time. Consult a licensed attorney (律师) for your specific situation.

Run \`${SCRIPT_NAME} calculate --input ${input}\` for compensation calculation.
Run \`${SCRIPT_NAME} letter --type demand --input ${input}\` to generate a demand letter.
REPORT
}

# ── Command: calculate ────────────────────────────────────────────────

cmd_calculate() {
  local input="" format="markdown"
  while [ $# -gt 0 ]; do
    case "$1" in
      --input) input="$2"; shift 2 ;;
      --format) format="$2"; shift 2 ;;
      --help) cmd_help calculate; return 0 ;;
      *) die "Unknown option: $1. Run with --help for usage." ;;
    esac
  done
  require_input "$input"

  local dispute_type deposit monthly_rent amount_disputed
  dispute_type=$(json_get "$input" "dispute_type" 2>/dev/null || echo "other")
  deposit=$(json_get "$input" "lease.deposit_amount" 2>/dev/null || echo "0")
  monthly_rent=$(json_get "$input" "lease.monthly_rent" 2>/dev/null || echo "0")
  city=$(json_get "$input" "tenant.city" 2>/dev/null || echo "[Your City]")
  monthly_rent=$(json_get "$input" "lease.monthly_rent" 2>/dev/null || echo "0")
  amount_disputed=$(json_get "$input" "amount_disputed" 2>/dev/null || echo "0")

  # Penaly calculation: up to 30% of deposit per civil law practice
  deposit_num=$(echo "$deposit" | sed 's/[^0-9.]//g')
  [ -z "$deposit_num" ] && deposit_num=0

  monthly_rent_num=$(echo "$monthly_rent" | sed 's/[^0-9.]//g')
  [ -z "$monthly_rent_num" ] && monthly_rent_num=0

  disputed_num=$(echo "$amount_disputed" | sed 's/[^0-9.]//g')
  [ -z "$disputed_num" ] && disputed_num=0

  penalty_max=$(python3 -c "print(round(${deposit_num} * 0.3, 2))" 2>/dev/null || echo "0")
  penalty_min=$(python3 -c "print(round(${deposit_num} * 0.1, 2))" 2>/dev/null || echo "0")

  total_min=$(python3 -c "print(round(${deposit_num} + ${penalty_min}, 2))" 2>/dev/null || echo "0")
  total_max=$(python3 -c "print(round(${deposit_num} + ${penalty_max}, 2))" 2>/dev/null || echo "0")

  cat <<REPORT
# Compensation Calculation
**Generated**: $(now_ts)
**Case**: $(basename "$input" .json)

---

## Itemized Calculation

| Item | Amount (RMB) | Basis |
|---|---|---|
| Deposit Refund (押金退还) | ¥${deposit_num} | Full deposit unless damage beyond normal wear |
| Disputed Amount | ¥${disputed_num} | Amount landlord claims to deduct |
| Breach Penalty — Low (违约金-低) | ¥${penalty_min} | 10% of deposit, Civil Code §585 |
| Breach Penalty — High (违约金-高) | ¥${penalty_max} | 30% of deposit, Civil Code §585 |

## Total Recovery Estimate

| Scenario | Amount (RMB) | Description |
|---|---|---|
| 💚 **Best Case** | ¥${total_max} | Full deposit + max penalty |
| 💛 **Expected** | ¥${deposit_num} | Full deposit return |
| 🔴 **Conservative** | ¥${total_min} | Deposit + minimum penalty |

## Notes

- Breach penalties are subject to court discretion; actual awards may vary
- Courts may reduce penalties deemed excessive (Civil Code §585)
- If landlord acted in bad faith, additional damages may apply under Consumer Rights Protection Law
- Legal costs (court filing fee) for small claims (under 10,000 RMB): approximately ¥50
- Small claims court (小额诉讼): amounts under 50,000 RMB, single hearing, no appeal

> **⚠️ Disclaimer**: These calculations are estimates based on statutory guidelines. Actual compensation may vary. This is not legal advice. Consult a licensed attorney (律师) for your specific case.

Run \`${SCRIPT_NAME} letter --type demand --input ${input}\` to generate a demand letter.
REPORT
}

# ── Command: letter ───────────────────────────────────────────────────

cmd_letter() {
  local input="" type="demand" format="markdown"
  while [ $# -gt 0 ]; do
    case "$1" in
      --input) input="$2"; shift 2 ;;
      --type) type="$2"; shift 2 ;;
      --format) format="$2"; shift 2 ;;
      --help) cmd_help letter; return 0 ;;
      *) die "Unknown option: $1. Run with --help for usage." ;;
    esac
  done
  require_input "$input"

  local tenant landlord deposit monthly_rent dispute_desc disputed city
  tenant=$(json_get "$input" "tenant.name" 2>/dev/null || echo "[Your Name]")
  landlord=$(json_get "$input" "landlord.name" 2>/dev/null || echo "[Landlord Name]")
  deposit=$(json_get "$input" "lease.deposit_amount" 2>/dev/null || echo "0")
  monthly_rent=$(json_get "$input" "lease.monthly_rent" 2>/dev/null || echo "0")
  city=$(json_get "$input" "tenant.city" 2>/dev/null || echo "[Your City]")
  dispute_desc=$(json_get "$input" "incident.description" 2>/dev/null || echo "[Describe your dispute]")
  disputed=$(json_get "$input" "amount_disputed" 2>/dev/null || echo "0")

  local issue_date
  issue_date=$(now_iso)

  case "$type" in
    demand)
      cat <<LETTER
# 租金退还催告函 (Rental Deposit Demand Letter)

**签发日期 (Issue Date)**: ${issue_date}

---

**致 (To)**: ${landlord}

**发件人 (From)**: ${tenant}

**事由 (Subject)**: 关于要求退还房屋租赁押金的通知 (Demand for Return of Rental Deposit)

---

尊敬的 ${landlord}：

本人（${tenant}）与您就位于 [请填写房屋地址] 的房屋签订了租赁合同，租期为 [请填写租期起止日期]，月租金为 ¥${monthly_rent} 元，押金为 ¥${deposit} 元。

**纠纷事实 (Facts of Dispute)**:

${dispute_desc}

**法律依据 (Legal Basis)**:

根据《中华人民共和国民法典》第七百一十条规定："承租人按照约定的方法或者根据租赁物的性质使用租赁物，致使租赁物受到损耗的，不承担赔偿责任。"正常使用造成的磨损不属于承租人赔偿范围。

根据《中华人民共和国民法典》第七百一十二条规定，出租人应当履行租赁物的维修义务。

根据《商品房屋租赁管理办法》相关规定，出租人无正当理由不得扣留承租人押金。

**要求 (Demand)**:

1. 请于收到本函之日起 **7日内** 退还本人全部押金 ¥${deposit} 元。
2. 如对扣款有异议，请提供具体损坏项目的 **照片证据** 和 **第三方维修报价单**。
3. 如逾期未退还，本人将依法向 12315 消费者投诉热线、当地住房和城乡建设委员会（住建委）投诉，并保留向人民法院提起诉讼的权利。

**退款方式 (Refund Method)**:

请将款项退还至本人以下账户：[请填写您的银行账号/支付宝/微信]

---

**本人联系方式**: [请填写您的电话和地址]

**日期 (Date)**: ${issue_date}

---

> **⚠️ 重要提示**: 本函为模板文件，请根据您的实际情况修改 [方括号] 中的内容。发送前建议保存邮寄凭证或微信发送截图作为证据。本文件不构成法律意见，重要事项请咨询专业律师。
LETTER
      ;;

    complaint)
      cat <<LETTER
# 投诉举报信 (Administrative Complaint Letter)

**投诉日期 (Filing Date)**: ${issue_date}

---

## 投诉人信息 (Complainant Information)

- **姓名 (Name)**: ${tenant}
- **联系电话 (Phone)**: [请填写您的电话号码]
- **联系地址 (Address)**: [请填写您的联系地址]

## 被投诉方信息 (Respondent Information)

- **名称 (Name)**: ${landlord}${agent:+
- **中介机构 (Agency)**: ${agent}}
- **地址/联系方式 (Address/Contact)**: [请填写对方地址或联系方式]

## 投诉事项 (Complaint Details)

**投诉类型 (Complaint Type)**: 房屋租赁纠纷 — ${dispute_desc}

**涉及金额 (Amount Involved)**: ¥${disputed}

## 事实与理由 (Facts and Grounds)

${dispute_desc}

## 投诉请求 (Relief Sought)

1. 要求被投诉方退还押金/费用共计 ¥${deposit} 元
2. 要求对被投诉方的违法违规行为依法进行查处
3. 要求被投诉方承担相应的违约责任

## 证据材料清单 (Evidence Attached)

$(python3 -c "
import json
with open('$input') as f:
    data = json.load(f)
ev = data.get('evidence', [])
for i, e in enumerate(ev):
    print(f'{i+1}. [{e.get(\"type\",\"?\")}] {e.get(\"description\",\"?\")}')
" 2>/dev/null || echo "1. [请列出您的证据材料]")

---

**投诉人签名 (Signature)**:

**日期 (Date)**: ${issue_date}

---

> **投诉渠道 (Filing Channels)**:
> - **12315**: 拨打 12315 热线 或 www.12315.cn 在线投诉
> - **住建委**: 联系当地住房和城乡建设委员会
> - **市场监督管理局**: 涉及中介违规收费可向当地市监局投诉

> **⚠️ 重要提示**: 本文件为模板，请根据实际情况修改。投诉时请附上相关证据材料复印件。本文件不构成法律意见。
LETTER
      ;;

    civil)
      cat <<LETTER
# 民事起诉状（简版）(Simplified Civil Complaint)

---

## 原告 (Plaintiff)

- **姓名 (Name)**: ${tenant}
- **身份证号 (ID Number)**: [请填写]
- **联系电话**: [请填写]
- **联系地址**: [请填写]

## 被告 (Defendant)

- **姓名/名称 (Name)**: ${landlord}
- **身份证号/统一社会信用代码**: [请填写，如有]
- **联系电话**: [请填写]
- **联系地址**: [请填写]

## 诉讼请求 (Claims for Relief)

1. 判令被告返还原告押金人民币 ¥${deposit} 元；
2. 判令被告支付逾期返还押金的违约金 ¥[请计算具体金额] 元；
3. 判令被告承担本案全部诉讼费用。

## 事实与理由 (Facts and Grounds)

${dispute_desc}

原告与被告于 [请填写签约日期] 签订了《房屋租赁合同》，约定租期为 [请填写租期]，月租金为人民币 ¥${monthly_rent} 元，押金为人民币 ¥${deposit} 元。

[请在此处详细描述纠纷经过，包括时间、事件、双方沟通情况等]

## 法律依据

根据《中华人民共和国民法典》第七百一十条、第七百一十二条、第五百七十七条等相关规定，被告无正当理由扣留原告押金的行为，已构成违约，依法应当返还押金并承担违约责任。

## 证据和证据来源

$(python3 -c "
import json
with open('$input') as f:
    data = json.load(f)
ev = data.get('evidence', [])
for i, e in enumerate(ev):
    print(f'{i+1}. [{e.get(\"type\",\"?\")}] {e.get(\"description\",\"?\")}')
" 2>/dev/null || echo "1. [请列出您的证据及来源]")

---

**此致**

[请填写有管辖权的人民法院名称]

**起诉人 (Plaintiff)**:

**日期 (Date)**: ${issue_date}

---

> **⚠️ 重要提示 (Important Notes)**:
> - 本起诉状为简版模板，正式提交前建议咨询律师审核
> - 小额诉讼（标的额 50,000 元以下）适用简易程序，一审终审
> - 诉讼时效为 3 年（自知道权利受损之日起算）
> - 立案需提供被告准确的身份信息
> - 本文件不构成法律意见，重要事项请咨询专业律师
LETTER
      ;;

    *)
      die "E-INVALID-TYPE: Letter type must be 'demand', 'complaint', or 'civil'. Got: '$type'"
      ;;
  esac
}

# ── Command: evidence ─────────────────────────────────────────────────

cmd_evidence() {
  local input="" format="markdown"
  while [ $# -gt 0 ]; do
    case "$1" in
      --input) input="$2"; shift 2 ;;
      --format) format="$2"; shift 2 ;;
      --help) cmd_help evidence; return 0 ;;
      *) die "Unknown option: $1. Run with --help for usage." ;;
    esac
  done
  require_input "$input"

  local dispute_type
  dispute_type=$(json_get "$input" "dispute_type" 2>/dev/null || echo "other")

  evidence_by_type() {
    case "$1" in
      deposit_withheld)
        cat <<ITEMS
## Priority 1 — Critical (必须收集)
- [ ] 📄 **Signed lease agreement** (租赁合同) — the foundation document. Verify the deposit clause
- [ ] 🧾 **Deposit payment proof** (押金支付凭证) — bank transfer / WeChat / Alipay record showing amount, date, counterparty
- [ ] 📸 **Move-in photos/video** (入住时照片/视频) — showing property condition at move-in
- [ ] 📸 **Move-out photos/video** (退租时照片/视频) — showing property condition at move-out

## Priority 2 — Important (强烈建议)
- [ ] 💬 **Chat records with landlord** (与房东的聊天记录) — especially messages about disputed damage, deposit return
- [ ] 📝 **Property handover checklist** (房屋交接清单) — if one was completed at move-in/move-out
- [ ] 🧾 **Monthly rent receipts** (月租金支付记录) — all rent payments during tenancy

## Priority 3 — Supporting (有更好)
- [ ] 👥 **Witness statements** (证人证言) — neighbors, roommates who can verify property condition
- [ ] 🔧 **Maintenance/repair records** (维修记录) — any repair requests made during tenancy
- [ ] 📱 **Audio recordings** (录音) — if landlord made verbal admissions (note: surreptitious recording may have evidentiary limits)
- [ ] 📋 **Third-party appraisal** (第三方评估) — professional assessment of claimed damages (for large amounts)
ITEMS
        ;;
      rent_increase)
        cat <<ITEMS
## Priority 1 — Critical
- [ ] 📄 **Signed lease agreement** — the original lease with rent amount and adjustment clauses
- [ ] 💬 **Landlord's notice of increase** (房东涨价通知) — screenshot or copy of the rent increase demand
- [ ] 🧾 **Payment history** (付款记录) — proof of on-time rent payments at original rate

## Priority 2 — Important
- [ ] 📊 **Market rent data** (周边租金数据) — comparable rents in the area to assess reasonableness
- [ ] 💬 **Negotiation records** (协商记录) — all communications about the rent increase
- [ ] 📄 **Any written amendments** (补充协议) — any lease modifications made during tenancy

## Priority 3 — Supporting
- [ ] 📜 **Local rental regulations** (当地租赁管理条例) — city/county rental rules
- [ ] 📋 **Rent control notices** (租金管控通知) — if applicable in your city
- [ ] 👥 **Witness contact info** — neighbors who can verify original rent terms
ITEMS
        ;;
      illegal_fees)
        cat <<ITEMS
## Priority 1 — Critical
- [ ] 🧾 **Fee payment receipts** (费用支付凭证) — all payments to the agency, including fees without receipts
- [ ] 📄 **Agency service agreement** (中介服务合同) — the contract with the brokerage agency
- [ ] 💬 **Fee discussion records** (费用沟通记录) — chat messages discussing fees before payment

## Priority 2 — Important
- [ ] 📜 **Local brokerage fee standards** (当地中介费标准) — published fee guidelines from local housing authority
- [ ] 🧾 **Lease agreement** (租赁合同) — shows monthly rent for fee comparison
- [ ] 📊 **Comparable fee examples** (同类收费对比) — evidence of standard fees from other agencies

## Priority 3 — Supporting
- [ ] 📄 **Agency license check** (中介资质查询) — verify the agency is properly licensed
- [ ] 💬 **Other tenants' experiences** (其他租客经历) — similar complaints (for pattern evidence)
- [ ] 📝 **Receipt refusal documentation** (拒开发票记录) — if agency refused to provide fapiao/receipt
ITEMS
        ;;
      maintenance_failure)
        cat <<ITEMS
## Priority 1 — Critical
- [ ] 💬 **Repair request records** (维修请求记录) — every message/email sent to landlord requesting repairs, with dates
- [ ] 📸 **Photos/videos of defect** (故障照片/视频) — showing the broken facility and dates
- [ ] 📄 **Lease agreement** (租赁合同) — with maintenance responsibility clauses

## Priority 2 — Important
- [ ] ⏰ **Timeline of landlord responses** (房东回应时间线) — all responses (or non-responses) with timestamps
- [ ] 🧾 **Self-repair receipts** (自行维修收据) — if you paid for emergency repairs yourself
- [ ] 📋 **Written repair demand** (书面维修催告) — formal written notice demanding repair

## Priority 3 — Supporting
- [ ] 👥 **Neighbor/witness statements** (邻居证言) — if others can verify the defect duration
- [ ] 🌡️ **Living condition impact log** (居住影响记录) — daily log of how defect affected living conditions
- [ ] 🏨 **Alternative accommodation receipts** (替代住宿收据) — if you had to stay elsewhere
- [ ] 📜 **Health/safety impact documentation** (健康安全影响证明) — if applicable (e.g., doctor's note)
ITEMS
        ;;
      *)
        cat <<ITEMS
## Priority 1 — Critical
- [ ] 📄 **Signed lease agreement** (租赁合同) — the rental contract
- [ ] 🧾 **All payment records** (所有付款记录) — deposit, rent, fees
- [ ] 💬 **All communication records** (所有沟通记录) — WeChat/email with landlord/agent

## Priority 2 — Important
- [ ] 📸 **Property condition photos** (房屋状况照片) — move-in and current
- [ ] ⏰ **Detailed timeline** (详细时间线) — dates of all key events
- [ ] 📄 **Any written notices** (书面通知) — any formal documents exchanged

## Priority 3 — Supporting
- [ ] 👥 **Witness contacts** (证人联系方式)
- [ ] 📜 **Applicable regulations** (相关法规) — city-specific rental rules
- [ ] 📋 **Police reports** (报警记录) — if law enforcement was involved
ITEMS
        ;;
    esac
  }

  cat <<REPORT
# Evidence Checklist
**Generated**: $(now_ts)
**Case**: $(basename "$input" .json)
**Dispute Type**: ${dispute_type}

---

$(evidence_by_type "$dispute_type")

---

## Collection Instructions

1. **Digital backup**: Screenshot/photograph all chat records and save to cloud storage
2. **Original documents**: Keep original paper documents; make copies for submission
3. **Timestamps**: Ensure all digital evidence shows date/time (take screenshots showing full screen with clock)
4. **Chain of custody**: Note when, where, and how you obtained each piece of evidence
5. **WeChat records**: Use WeChat's built-in "Export Chat History" function if available, or take scrolling screenshots

## Evidence Submission Tips

- For **12315 complaints**: Upload photos + chat screenshots + payment records
- For **Housing Authority complaints**: Submit organized copies with a cover letter
- For **Small Claims Court**: Bring originals to court; submit copies as exhibits
- **Number and label** each piece of evidence (证据一、证据二...)

> **⚠️ Note**: Do NOT fabricate or alter evidence — this can seriously harm your case and may have legal consequences. This checklist is for informational purposes only.

Run \`${SCRIPT_NAME} escalate --input ${input}\` for escalation path planning.
REPORT
}

# ── Command: negotiate ────────────────────────────────────────────────

cmd_negotiate() {
  local input="" style="soft" format="markdown"
  while [ $# -gt 0 ]; do
    case "$1" in
      --input) input="$2"; shift 2 ;;
      --style) style="$2"; shift 2 ;;
      --format) format="$2"; shift 2 ;;
      --help) cmd_help negotiate; return 0 ;;
      *) die "Unknown option: $1. Run with --help for usage." ;;
    esac
  done
  require_input "$input"

  local tenant landlord dispute_desc deposit city
  local issue_date
  issue_date=$(python3 -c "from datetime import date, timedelta; print(date.today() + timedelta(days=7))" 2>/dev/null || echo "YYYY-MM-DD")
  tenant=$(json_get "$input" "tenant.name" 2>/dev/null || echo "[You]")
  landlord=$(json_get "$input" "landlord.name" 2>/dev/null || echo "[Landlord]")
  dispute_desc=$(json_get "$input" "incident.description" 2>/dev/null || echo "[dispute]")
  deposit=$(json_get "$input" "lease.deposit_amount" 2>/dev/null || echo "0")
  monthly_rent=$(json_get "$input" "lease.monthly_rent" 2>/dev/null || echo "0")
  city=$(json_get "$input" "tenant.city" 2>/dev/null || echo "[Your City]")
  city=$(json_get "$input" "tenant.city" 2>/dev/null || echo "[Your City]")

  case "$style" in
    soft)
      cat <<SCRIPT
# Negotiation Script — 温和版 (Soft Approach)

**Strategy**: Maintain relationship, seek win-win resolution. Best when the landlord has been cooperative or the relationship is ongoing.

---

## Round 1: Opening (开场)

> **You**: "${landlord}你好！关于退租押金的事情，我想和您好好沟通一下。我们之前合作一直挺愉快的，希望这件事也能顺利解决。"

**Key Point**: Start positive. Acknowledge the relationship.

---

## Round 2: State Facts (陈述事实)

> **You**: "关于您提到的[具体损坏项目]，我这边有入住时拍的照片，可以发给您看。其实这个在入住前就已经有[磨损/问题]了，不是我造成的。另外退租时我也拍了照片和视频，房间整体状态是好的。"

**Key Point**: Present evidence calmly. Offer to share photos. Don't accuse — inform.

---

## Round 3: Reference Contract (引用合同)

> **You**: "我们的合同里写的是'正常磨损不扣押金'。按照《民法典》第七百一十条，正常使用造成的损耗，租客是不用赔的。您说的这些磨损应该属于正常使用范畴。"

**Key Point**: Reference the contract and law — not as a threat, but as a shared framework.

---

## Round 4: Propose Solution (提出方案)

> **You**: "这样吧，如果您认为确实有需要我承担的部分，我们能不能约定一个时间一起去看看？如果确实是合理扣款，我可以承担。但我希望押金的大部分能按时退还。"

**Key Point**: Show willingness to compromise on reasonable items while standing firm on principle.

---

## Round 5: Gentle Deadline (温和期限)

> **You**: "我这边也在等着这笔钱[交新房租/其他用途]。您看这周之内能把这件事定下来吗？如果需要我配合做什么，我也会尽量配合。"

**Key Point**: Give a soft deadline with a reason. Make it collaborative.

---

## If Unresolved — Final Attempt (最后尝试)

> **You**: "${landlord}，关于押金的事我们已经沟通了几次了。为了尽快解决，我想提议一个方案：押金退还[部分金额]，[具体扣款]我认了。如果您同意，我们签个书面确认，这件事就算了结了。如果再拖下去，我可能只能通过12315或住建委来协调了，但我觉得没必要闹到那一步。"

**Key Point**: Offer a concrete compromise with an implicit escalation threat. Give them an "out" that saves face.

> **⚠️ Note**: These scripts are templates. Adjust based on your specific situation and the landlord's personality. Keep written records of all communications.

SCRIPT
      ;;

    firm)
      cat <<SCRIPT
# Negotiation Script — 强硬版 (Firm Approach)

**Strategy**: Assert rights clearly with legal backing. Best when the landlord is uncooperative, evasive, or has a pattern of bad-faith behavior.

---

## Round 1: Direct Opening (直接开场)

> **You**: "${landlord}，关于退租押金 ${deposit} 元至今未退还一事，我需要和您明确沟通。请说明扣款的具体项目和金额，并提供相关证据。"

**Key Point**: Be direct. Demand specifics. Set the tone for a business-like discussion.

---

## Round 2: Present Evidence (出示证据)

> **You**: "我这里有：
> 1. 入住和退租时的房屋状况照片
> 2. 合同关于押金退还的条款
> 3. 押金支付凭证
>
> 这些材料清楚表明，您所说的[损坏/问题]要么是入住前就存在的，要么属于正常磨损范畴。"

**Key Point**: List your evidence concretely. Show you've prepared.

---

## Round 3: State Legal Position (明确法律立场)

> **You**: "根据《民法典》第七百一十条，承租人按约定方法使用租赁物造成的损耗，不承担赔偿责任。第七百一十二条规定了出租人的维修义务。您无正当理由扣留押金的行为，已经构成违约。"

**Key Point**: Reference specific legal provisions. Show you know your rights.

---

## Round 4: Set Firm Deadline (设定明确期限)

> **You**: "我现在正式通知您：请在 **7日内**（即2026-06-25前）将押金 ¥${deposit} 元全额退还。如果7日内未能退还，我将采取以下措施：

> 1. 向 **12315 消费者投诉热线** 正式投诉
> 2. 向 **${city}市住房和城乡建设委员会** 举报
> 3. 向 **人民法院** 提起小额诉讼（标的额 50,000 元以下，一审终审，程序简便）

> 我不想走这些程序，但如果您继续拖延，我没有其他选择。"

**Key Point**: Concrete deadline with specific escalation threats. The specificity makes it credible.

---

## Round 5: Close (收尾)

> **You**: "请在此期限前将退款汇至我的账户[账号]。汇款后请通知我确认。如果有什么需要当面交接的，也请在期限内完成。这是我的权利，也希望您理解。"

**Key Point**: Professional, firm, leaves door open for resolution while making consequences clear.

---

> **⚠️ Important**: Before sending the firm script, ensure you have all your evidence organized. If the landlord responds aggressively, do not escalate verbally — simply state you will proceed with formal channels as outlined. Keep all communications in writing. This script is for informational purposes and does not constitute legal advice.

SCRIPT
      ;;

    *)
      die "E-INVALID-STYLE: Style must be 'soft' or 'firm'. Got: '$style'"
      ;;
  esac
}

# ── Command: escalate ─────────────────────────────────────────────────

cmd_escalate() {
  local input="" format="markdown" output=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --input) input="$2"; shift 2 ;;
      --format) format="$2"; shift 2 ;;
      --output) output="$2"; shift 2 ;;
      --help) cmd_help escalate; return 0 ;;
      *) die "Unknown option: $1. Run with --help for usage." ;;
    esac
  done
  require_input "$input"

  local city deposit disputed
  city=$(json_get "$input" "tenant.city" 2>/dev/null || echo "[Your City]")
  deposit=$(json_get "$input" "lease.deposit_amount" 2>/dev/null || echo "0")
  monthly_rent=$(json_get "$input" "lease.monthly_rent" 2>/dev/null || echo "0")
  city=$(json_get "$input" "tenant.city" 2>/dev/null || echo "[Your City]")
  disputed=$(json_get "$input" "amount_disputed" 2>/dev/null || echo "$deposit")

  local today
  today=$(now_iso)

  # Calculate future dates (bash 3.2 compatible)
  plus_days() {
    local days="$1"
    python3 -c "from datetime import date, timedelta; print(date.today() + timedelta(days=$days))" 2>/dev/null || echo "YYYY-MM-DD"
  }

  local med_7d med_15d med_30d med_60d med_180d
  med_7d=$(plus_days 7)
  med_15d=$(plus_days 15)
  med_30d=$(plus_days 30)
  med_60d=$(plus_days 60)
  med_180d=$(plus_days 180)

  cat <<REPORT
# Escalation Path & Timeline
**Generated**: $(now_ts)
**Case**: $(basename "$input" .json)
**Start Date**: ${today}

---

## Overview

| Level | Method | Time Estimate | Cost | Success Rate |
|---|---|---|---|---|
| 1 | Self-Negotiation (协商) | 3-7 days | Free | ~40% |
| 2 | Community Mediation (社区调解) | 7-15 days | Free | ~55% |
| 3 | 12315 / Housing Authority (行政投诉) | 15-30 days | Free | ~70% |
| 4 | Arbitration (仲裁) | 30-60 days | ¥500-2,000 | ~75% |
| 5 | Small Claims Court (小额诉讼) | 2-6 months | ¥50-200 | ~85% |

---

## Level 1: Self-Negotiation (自行协商)

- **Timeline**: Now → ${med_7d}
- **Cost**: Free
- **Action**: Send demand letter. Communicate via WeChat/email. Propose settlement.
- **Success Indicator**: Landlord agrees to return deposit or negotiate partial refund.
- **If Unresolved**: Proceed to Level 2.

---

## Level 2: Community Mediation (社区/街道调解)

- **Timeline**: ${med_7d} → ${med_15d}
- **Cost**: Free
- **Action**: Contact your neighborhood committee (居委会) or sub-district office (街道办事处). Request mediation.
- **Required Documents**: Lease contract, ID, summary of dispute.
- **Success Indicator**: Mediator facilitates agreement between both parties.
- **If Unresolved**: Proceed to Level 3.

---

## Level 3: Administrative Complaint (行政投诉)

- **Timeline**: ${med_15d} → ${med_30d}
- **Cost**: Free
- **Action**:
  - **12315**: Call 12315 or file online at www.12315.cn / WeChat mini program "全国12315平台"
  - **Housing Authority (住建委)**: File complaint with ${city} Housing and Urban-Rural Development Commission
  - **Market Supervision Bureau (市监局)**: For agency fee issues
- **Required Documents**: Complaint letter (generated by this tool), evidence, ID.
- **Process**: Authority reviews case, contacts landlord for response, issues ruling.
- **If Unresolved**: Proceed to Level 4 or 5.

---

## Level 4: Arbitration (仲裁)

- **Timeline**: ${med_30d} → ${med_60d}
- **Cost**: ¥500-2,000 (varies by arbitration commission)
- **Prerequisite**: Lease contract must contain an arbitration clause.
- **Action**: File with local arbitration commission. Provide case file and evidence.
- **Note**: Arbitration awards are binding and enforceable. Skip this if no arbitration clause.
- **If Unresolved**: Proceed to Level 5.

---

## Level 5: Small Claims Court (小额诉讼)

- **Timeline**: ${med_30d} → ${med_180d}
- **Cost**: ¥50 (for claims under ¥10,000); ¥50 + 2.5% of excess for larger claims
- **Prerequisite**: Claim amount under ¥50,000; claim is for monetary relief.
- **Action**:
  1. Prepare civil complaint (民事起诉状) — use \`${SCRIPT_NAME} letter --type civil\`
  2. Prepare evidence bundle (证据清单)
  3. File at local People's Court (人民法院) with jurisdiction
  4. Attend hearing (typically one hearing, no appeal)
- **Advantages**: Simple procedure, single hearing, final judgment, low cost.
- **Statute of Limitations**: 3 years from the date you knew or should have known of the harm.

---

## Timeline Summary

\`\`\`
Today (${today})
│
├── 📧 Send Demand Letter ────── ${med_7d} (7 days)
│   └── Resolved? ✅ → Done!
│
├── 🏘️ Community Mediation ──── ${med_15d} (+~8 days)
│   └── Resolved? ✅ → Done!
│
├── 📞 12315 / 住建委 Complaint ── ${med_30d} (+~15 days)
│   └── Resolved? ✅ → Done!
│
├── ⚖️ Arbitration (if clause) ── ${med_60d} (+~30 days)
│   └── Resolved? ✅ → Done!
│
└── 🏛️ Small Claims Court ──── ${med_180d} (+~120 days)
    └── Final resolution
\`\`\`

---

## Key Dates to Track

| Date | Milestone | Status |
|---|---|---|
| ${med_7d} | Demand letter response deadline | ⬜ Pending |
| ${med_15d} | Mediation deadline | ⬜ Pending |
| ${med_30d} | Administrative complaint resolution | ⬜ Pending |
| ${med_180d} | Court judgment expected by | ⬜ Pending |

---

> **⚠️ Disclaimer**: Time estimates are approximate and vary by jurisdiction. Court filing fees are estimates — check with your local court for exact amounts. This escalation path is for informational purposes and does not constitute legal advice. Consult a licensed attorney (律师) for your specific case.

Run \`${SCRIPT_NAME} evidence --input ${input}\` for the evidence checklist.
REPORT
}

# ── Main Dispatcher ────────────────────────────────────────────────────

main() {
  local cmd="${1:-help}"
  shift 2>/dev/null || true

  case "$cmd" in
    collect)   cmd_collect "$@" ;;
    analyze)   cmd_analyze "$@" ;;
    calculate) cmd_calculate "$@" ;;
    letter)    cmd_letter "$@" ;;
    evidence)  cmd_evidence "$@" ;;
    negotiate) cmd_negotiate "$@" ;;
    escalate)  cmd_escalate "$@" ;;
    help|--help|-h) cmd_help "${1:-}" ;;
    version|--version|-v) echo "${SCRIPT_NAME} v${VERSION}" ;;
    *) usage; exit 1 ;;
  esac
}

main "$@"

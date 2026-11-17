#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"

fail() { echo "FAIL: $1" >&2; exit 1; }
need() { [ -f "$1" ] || fail "missing $1"; }

for f in SKILL.md manifest.yaml agents/openai.yaml README.md README.en.md LICENSE icon-512.png assets/promo-1600x900.png fixtures/success.json fixtures/failure-missing-reason.json; do need "$f"; done

grep -q '^name: shop-returns-reason-summary-cn$' SKILL.md || fail "SKILL name"
grep -q '^name: shop-returns-reason-summary-cn$' manifest.yaml || fail "manifest name"
grep -q '^slug: shop-returns-reason-summary-cn$' manifest.yaml || fail "manifest slug"
grep -q '^self_test: sh scripts/self-test.sh$' manifest.yaml || fail "self-test command"
grep -q '^  allow_implicit_invocation: true$' agents/openai.yaml || fail "policy boolean"
grep -q 'icon-512.png' agents/openai.yaml || fail "agent icon reference"

command -v file >/dev/null 2>&1 || fail "file command unavailable"
file icon-512.png | grep -q 'PNG image data, 512 x 512' || fail "icon must be 512x512 PNG"
file assets/promo-1600x900.png | grep -q 'PNG image data, 1600 x 900' || fail "promo must be 1600x900 PNG"

command -v node >/dev/null 2>&1 || fail "node unavailable for fixture validation"
node -e '
const fs=require("fs");
const path=require("path");
const agent=fs.readFileSync("agents/openai.yaml","utf8");
for(const field of ["display_name","short_description","default_prompt","icon_small","icon_large"]){
 const value=agent.match(new RegExp("^  "+field+": \"([^\"\\n]+)\"$","m"))?.[1];
 if(!value)throw new Error("agent field must be quoted: "+field);
 if(field==="default_prompt"&&!value.includes("$shop-returns-reason-summary-cn"))throw new Error("default_prompt must reference this Skill");
 if(field==="short_description"&&([...value].length<25||[...value].length>64))throw new Error("invalid short_description length");
 if(field.startsWith("icon_")){
  const resolved=path.resolve(value),relative=path.relative(process.cwd(),resolved);
  if(relative.startsWith("..")||path.isAbsolute(relative)||!fs.existsSync(resolved))throw new Error("agent icon must exist inside Skill directory");
 }
}
const ok=JSON.parse(fs.readFileSync("fixtures/success.json"));
const bad=JSON.parse(fs.readFileSync("fixtures/failure-missing-reason.json"));
const required=(o, keys)=>keys.every(k=>Object.hasOwn(o,k));
if (!required(ok,["input_records","expected_workflow_output","expected_markdown_sections"])) process.exit(1);
if (!Array.isArray(ok.input_records)||!ok.input_records.length||!ok.input_records.every(x=>x.product&&x.reason)) process.exit(1);
const expected=ok.expected_workflow_output;
if (!required(expected,["data_integrity","reason_classification_facts","product_dimension_facts","product_page_recommendations","pending_items"])) process.exit(1);
const details=expected.original_record_details;
if (!Array.isArray(details)||details.length!==ok.input_records.length)process.exit(1);
for(let i=0;i<details.length;i++)if(details[i].record_number!==i+1||JSON.stringify(details[i].original_fields)!==JSON.stringify(ok.input_records[i]))process.exit(1);
const included=expected.data_integrity.included_count;
const categoryTotal=expected.reason_classification_facts.reduce((n,x)=>n+x.record_count,0);
const productTotal=expected.product_dimension_facts.reduce((n,x)=>n+x.record_count,0);
if (included!==ok.input_records.length || categoryTotal!==included || productTotal!==included) process.exit(1);
if (!expected.reason_classification_facts.every(x=>x.category&&x.original_reason_examples?.length&&x.products?.length)) process.exit(1);
if (!expected.product_page_recommendations.every(x=>x.corresponding_observation&&x.suggestion&&x.verification)) process.exit(1);
if (!ok.expected_markdown_sections.includes("商品页改进建议（建议，非既成事实）")) process.exit(1);
if (!required(bad,["input_records","expected_workflow_output","expected_markdown_sections"]) || !bad.input_records.some(x=>!x.reason)) process.exit(1);
const error=bad.expected_workflow_output;
if (error.status!=="input_error" || !error.missing_fields.includes("退款/退货原因") || !error.affected_records.includes("B-001")) process.exit(1);
if (error.reason_classification_facts.length || error.product_dimension_facts.length || error.product_page_recommendations.length) process.exit(1);
' || fail "fixtures do not define a complete, internally consistent success result and explicit missing-reason error"

echo "PASS: package structure and fixture contracts validated."
echo "NOTE: This is a structural fixture-contract check (including count conservation and fact/suggestion separation), not a business engine. Real classification and recommendations are performed from supplied data through the Markdown workflow."

#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

need_file() { [[ -f "$1" ]] || { echo "missing file: $1" >&2; exit 1; }; }
need_text() { rg -Fq -- "$2" "$1" || { echo "missing text in $1: $2" >&2; exit 1; }; }

for file in SKILL.md manifest.yaml agents/openai.yaml README.md README.en.md LICENSE icon-512.png assets/promo-1600x900.png fixtures/success.md fixtures/failure-missing-fields.md; do need_file "$file"; done

need_text SKILL.md 'name: shop-order-exception-check-cn'
need_text manifest.yaml 'name: shop-order-exception-check-cn'
need_text manifest.yaml 'slug: shop-order-exception-check-cn'
need_text manifest.yaml 'self_test: bash scripts/self-test.sh'
need_text agents/openai.yaml 'allow_implicit_invocation: true'
need_text agents/openai.yaml 'short_description:'
need_text fixtures/success.md '预期：001 为超时'
need_text fixtures/success.md '003 为缺项，要求补充明确标注为完整的状态轨迹'
need_text fixtures/success.md '不能据此断言跳过了“已发货”或判为状态矛盾'
need_text fixtures/failure-missing-fields.md '不得判断超时或编造流程'

[[ "$(sips -g pixelWidth -g pixelHeight icon-512.png | awk '/pixel/{print $2}' | tr '\n' ' ')" == '512 512 ' ]] || { echo 'icon must be 512x512' >&2; exit 1; }
[[ "$(sips -g pixelWidth -g pixelHeight assets/promo-1600x900.png | awk '/pixel/{print $2}' | tr '\n' ' ')" == '1600 900 ' ]] || { echo 'promo must be 1600x900' >&2; exit 1; }

echo 'PASS: package structure and declared success/failure fixtures are valid.'
echo 'NOTE: this test is structural only; real exception judgments require user-supplied order data and rules.'

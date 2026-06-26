#!/bin/bash
# XiaBB Smart Modes — Automated Quality Test
# Tests translate / prompt / email modes with real Gemini API calls
# Uses text input (simulating transcribed speech) instead of audio
set -e

API_KEY=$(cat ~/Tools/xiabb/.api-key 2>/dev/null)
if [ -z "$API_KEY" ]; then echo "❌ No API key"; exit 1; fi

MODEL="gemini-2.5-flash"
URL="https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent"

PASS=0
FAIL=0
TOTAL=0
RESULTS=""

call_gemini() {
    local system_prompt="$1"
    local user_input="$2"
    local combined="$system_prompt

The speaker said (transcribed text):
\"$user_input\""

    local body=$(jq -n --arg text "$combined" '{
        contents: [{parts: [{text: $text}]}],
        generationConfig: {temperature: 0.3, maxOutputTokens: 4096}
    }')

    local resp=$(curl -s -X POST "$URL" \
        -H "Content-Type: application/json" \
        -H "x-goog-api-key: $API_KEY" \
        -d "$body" 2>/dev/null)

    echo "$resp" | jq -r '.candidates[0].content.parts[0].text // "ERROR: no response"' 2>/dev/null
}

check() {
    local test_name="$1"
    local condition="$2"  # "contains" or "not_contains" or "min_length"
    local value="$3"
    local output="$4"
    TOTAL=$((TOTAL + 1))

    case "$condition" in
        contains)
            if echo "$output" | grep -qi "$value"; then
                PASS=$((PASS + 1))
                RESULTS+="  ✅ $test_name\n"
            else
                FAIL=$((FAIL + 1))
                RESULTS+="  ❌ $test_name — expected to contain '$value'\n"
            fi
            ;;
        not_contains)
            if echo "$output" | grep -qi "$value"; then
                FAIL=$((FAIL + 1))
                RESULTS+="  ❌ $test_name — should NOT contain '$value'\n"
            else
                PASS=$((PASS + 1))
                RESULTS+="  ✅ $test_name\n"
            fi
            ;;
        min_length)
            local len=${#output}
            if [ "$len" -ge "$value" ]; then
                PASS=$((PASS + 1))
                RESULTS+="  ✅ $test_name (${len} chars)\n"
            else
                FAIL=$((FAIL + 1))
                RESULTS+="  ❌ $test_name — got ${len} chars, need ≥${value}\n"
            fi
            ;;
        is_chinese)
            # Check if output contains Chinese characters
            if echo "$output" | grep -qP '[\x{4e00}-\x{9fff}]' 2>/dev/null || echo "$output" | grep -q '[一-龥]' 2>/dev/null; then
                PASS=$((PASS + 1))
                RESULTS+="  ✅ $test_name\n"
            else
                FAIL=$((FAIL + 1))
                RESULTS+="  ❌ $test_name — output is not Chinese\n"
            fi
            ;;
    esac
}

# ═══════════════════════════════════════════
# System prompts (must match main.swift)
# ═══════════════════════════════════════════

TRANSLATE_PROMPT='Listen to this audio carefully and transcribe it. Then:
- If the speaker spoke primarily in Chinese, translate the ENTIRE output to English.
- If the speaker spoke primarily in English, translate the ENTIRE output to Simplified Chinese (简体中文).
- If mixed, determine the dominant language and translate everything to the OTHER language.
Output ONLY the translated text. Do NOT include the original language. Proper punctuation and natural phrasing.'

PROMPT_PROMPT='Listen to this audio carefully. The speaker is casually describing what they want an AI to do. Your job is to transform their rough idea into a professional, detailed, production-quality prompt.

Rules:
1. NEVER invent details the speaker did not mention. Do NOT guess gender, clothing, objects, colors, or any specifics not stated. If the speaker said "a woman", it is a woman — never change it to a man. If they did not mention clothing, do not add clothing.
2. ENRICH only along dimensions the speaker implied: add quality parameters (8k, detailed), lighting, composition, camera angle, art style — but ONLY when they do not contradict or fabricate subject details.
3. For IMAGE prompts: Improve technical quality (resolution, lighting, style keywords) but keep the EXACT subject description faithful to what was said. Never change who/what is in the image.
4. For CODE/WRITING prompts: Add structure (format, edge cases, acceptance criteria) but do not change the core task.
5. STRUCTURE the prompt with clear sections if complex (e.g. Role, Context, Task, Constraints, Output Format).
6. Remove filler words, hesitation, and repetition.
7. Output ONLY the final prompt. No meta-commentary, no explanation.
8. CRITICAL — Language: You MUST output in the SAME language the speaker used. Chinese input → Chinese output. English → English. Do NOT translate to another language.'

EMAIL_PROMPT='Listen to this audio carefully. The speaker is describing what they want to communicate in an email.
Write a professional, polite, well-formatted email based on what they said. Include a subject line on the first line prefixed with "Subject: ".
Keep the tone appropriate — formal for business, friendly for colleagues. Fix grammar, add proper greetings and sign-off.
Output ONLY the email, nothing else.
If the speaker uses Chinese, write the email in Chinese. If English, in English. If mixed, use the dominant language.'

echo "🦞 XiaBB Smart Modes — Quality Test"
echo "   Model: $MODEL"
echo "   $(date)"
echo ""

# ═══════════════════════════════════════════
# 1. TRANSLATE MODE
# ═══════════════════════════════════════════
echo "━━━ 🔄 Translate Mode ━━━"

echo -n "  [1/3] CN→EN: 简单句..."
OUT=$(call_gemini "$TRANSLATE_PROMPT" "今天天气真不错，我想出去走走")
check "CN→EN output is English" "not_contains" "天气" "$OUT"
echo " → ${OUT:0:60}"

echo -n "  [2/3] EN→CN: Tech sentence..."
OUT=$(call_gemini "$TRANSLATE_PROMPT" "The new API endpoint supports pagination and rate limiting")
check "EN→CN output is Chinese" "is_chinese" "" "$OUT"
echo " → ${OUT:0:60}"

echo -n "  [3/3] Mixed→translate..."
OUT=$(call_gemini "$TRANSLATE_PROMPT" "这个feature很好用，但是performance还需要optimize一下")
check "Mixed translation produces output" "min_length" "10" "$OUT"
echo " → ${OUT:0:60}"

echo ""

# ═══════════════════════════════════════════
# 2. PROMPT MODE
# ═══════════════════════════════════════════
echo "━━━ ⚡ Prompt Mode ━━━"

echo -n "  [1/7] Image prompt (CN)..."
OUT=$(call_gemini "$PROMPT_PROMPT" "帮我画一只猫坐在窗台上看月亮")
check "Image prompt is enriched" "min_length" "100" "$OUT"
check "Image prompt stays Chinese" "is_chinese" "" "$OUT"
echo " → ${OUT:0:80}"

echo -n "  [2/7] Image prompt (EN)..."
OUT=$(call_gemini "$PROMPT_PROMPT" "draw a robot walking in a forest")
check "EN image prompt is enriched" "min_length" "100" "$OUT"
check "EN image prompt stays English" "not_contains" "机器人" "$OUT"
echo " → ${OUT:0:80}"

echo -n "  [3/7] Code prompt (CN)..."
OUT=$(call_gemini "$PROMPT_PROMPT" "嗯，写一个Python脚本，就是那个可以批量把图片压缩一下的")
check "Code prompt is enriched" "min_length" "80" "$OUT"
check "Code prompt stays Chinese" "is_chinese" "" "$OUT"
echo " → ${OUT:0:80}"

echo -n "  [4/7] Writing prompt (EN)..."
OUT=$(call_gemini "$PROMPT_PROMPT" "I want to write a blog post about why startups should use AI agents")
check "Writing prompt is enriched" "min_length" "100" "$OUT"
echo " → ${OUT:0:80}"

echo -n "  [5/7] FAITHFULNESS: female portrait..."
OUT=$(call_gemini "$PROMPT_PROMPT" "帮我优化一下这个图片生成的prompt，就是一个女生的肖像照，她站在海边，风吹着她的头发")
check "Must contain 女 (female)" "contains" "女" "$OUT"
check "Must NOT contain 男 (male)" "not_contains" "男" "$OUT"
check "Must NOT contain 西装 (suit)" "not_contains" "西装" "$OUT"
echo " → ${OUT:0:80}"

echo -n "  [6/7] FAITHFULNESS: no invented details..."
OUT=$(call_gemini "$PROMPT_PROMPT" "generate an image of a dog sitting on a beach")
check "Must contain dog" "contains" "dog" "$OUT"
check "Must NOT invent cat" "not_contains" "cat" "$OUT"
echo " → ${OUT:0:80}"

echo -n "  [7/7] FAITHFULNESS: preserve specifics..."
OUT=$(call_gemini "$PROMPT_PROMPT" "画一个老人在雨中撑伞走在小巷里")
check "Must contain 老人" "contains" "老人" "$OUT"
check "Must contain 雨 or 伞" "contains" "伞" "$OUT"
check "Must NOT change to young person" "not_contains" "年轻" "$OUT"
echo " → ${OUT:0:80}"

echo ""

# ═══════════════════════════════════════════
# 3. EMAIL MODE
# ═══════════════════════════════════════════
echo "━━━ 📧 Email Mode ━━━"

echo -n "  [1/3] Business email (CN)..."
OUT=$(call_gemini "$EMAIL_PROMPT" "给投资人写封邮件，告诉他们我们这个月的月活增长了百分之三十，下个月准备开始融资")
check "Has Subject line" "contains" "Subject:" "$OUT"
check "Email is Chinese" "is_chinese" "" "$OUT"
check "Email has greeting" "min_length" "100" "$OUT"
echo " → ${OUT:0:80}"

echo -n "  [2/3] Casual email (EN)..."
OUT=$(call_gemini "$EMAIL_PROMPT" "Hey tell my colleague John that we need to push the meeting to next Tuesday because I have a conflict")
check "Has Subject line" "contains" "Subject:" "$OUT"
check "Casual tone - has John" "contains" "John" "$OUT"
echo " → ${OUT:0:80}"

echo -n "  [3/3] Decline email (CN)..."
OUT=$(call_gemini "$EMAIL_PROMPT" "回复一个猎头，就说我现在不考虑换工作，谢谢他的推荐")
check "Has Subject line" "contains" "Subject:" "$OUT"
check "Polite decline" "min_length" "80" "$OUT"
echo " → ${OUT:0:80}"

echo ""

# ═══════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Results: $PASS passed, $FAIL failed, $TOTAL total"
echo ""
echo -e "$RESULTS"

if [ "$FAIL" -gt 0 ]; then
    echo "⚠️  Some tests failed — review output above"
    exit 1
else
    echo "✅ All tests passed!"
fi

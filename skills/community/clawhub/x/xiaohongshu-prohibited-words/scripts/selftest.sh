#!/usr/bin/env bash
# 退出码回归自测 —— 改词库 / 改级别 / 改解析后跑一遍。
#
# 重点锁两类回归：
#   1) 漂移：脚本内嵌词库曾与 md 不一致，「免费（全文≥2次）」「答案+PDF+主页群」
#      两条 P0 一个都拦不住（2026-09-19 实测）。这里把它们钉成用例。
#   2) fail-closed：词库/段落配置缺失必须回 3，不许静默当「干净」。
#
# 用法：bash scripts/selftest.sh
set -u
cd "$(dirname "$0")/.." || exit 3

PY=python3
FAIL=0

check() {  # check <期望退出码> <说明> <命令...>
  local want="$1" desc="$2"; shift 2
  "$@" >/dev/null 2>&1
  local got=$?
  if [ "${got}" -eq "${want}" ]; then
    printf '  ✓ %-50s 退出码 %s\n' "${desc}" "${got}"
  else
    printf '  ✗ %-50s 期望 %s，实得 %s\n' "${desc}" "${want}" "${got}"
    FAIL=1
  fi
}

TMP=$(mktemp -d)
trap 'rm -rf "${TMP}"' EXIT

# 手机号用拼接构造：本文件文本里不出现完整号码（发布前隐私闸门会拦 11 位手机号）
FAKE_PHONE="138""0013""8000"

echo "小红书违禁词离线检测 · 退出码自测"
echo "───────────────────────────────────────────────────────────"

# 0 = 无 P0（P1/P2 不阻塞，这是本 skill 的契约：它只管 P0 轴）
check 0 "干净文案 → 0（无 P0）" \
  ${PY} scripts/check_prohibited.py "我用AI把笔记做成了图" \
  "上周整理书架翻出一本小开本唐诗集，顺手做成了图。这套流程我跑通了三遍。" ""
check 0 "只命中 P1（LinkedIn）→ 0（P1 不阻塞）" \
  ${PY} scripts/check_prohibited.py "标题" "我在LinkedIn上也发，正文够长。" ""

# 1 = 有 P0
check 1 "实测硬词「白嫖」→ 1（禁止发布）" \
  ${PY} scripts/check_prohibited.py "标题" "这类东西白嫖就行。" ""
check 1 "手机号 → 1（P0 站外导流）" \
  ${PY} scripts/check_prohibited.py "标题" "有问题打 ${FAKE_PHONE} 找我。" ""

# ⬇⬇ 漂移回归：这两条曾因脚本内嵌词库过时而完全失效 ⬇⬇
check 1 "「免费」全文≥2次 → 1（漂移回归）" \
  ${PY} scripts/check_prohibited.py "标题" "免费领，免费拿，全免费。" ""
check 1 "「答案+PDF+主页群」共现 → 1（漂移回归）" \
  ${PY} scripts/check_prohibited.py "标题" "答案合集PDF放主页群。" ""

# 逐词调级：微信号属联系人信息 = 硬红线 P0（与 LinkedIn 同段但不同级）
check 1 "「微信号」→ 1（levelOverrides 提到 P0）" \
  ${PY} scripts/check_prohibited.py "标题" "加微信号详聊。" ""

# 3 = fail-closed（以下都必须是 3，绝不能是 0）
check 2 "完全没参数 → 2（运行错误）" \
  ${PY} scripts/check_prohibited.py
check 3 "XHS_WORDLIST 指向不存在的词库 → 3" \
  env XHS_WORDLIST="${TMP}/nope.md" ${PY} scripts/check_prohibited.py "标题" "正文" ""

# 词库 / 段落配置缺失（用临时副本删文件，不动工作区）
cp -R . "${TMP}/pw-nowl" && rm -f "${TMP}/pw-nowl/references/prohibited-words.md"
check 3 "默认词库文件缺失 → 3（fail-closed）" \
  ${PY} "${TMP}/pw-nowl/scripts/check_prohibited.py" "标题" "白嫖证书" ""
cp -R . "${TMP}/pw-nosec" && rm -f "${TMP}/pw-nosec/references/sections.json"
check 3 "sections.json 缺失 → 3（fail-closed）" \
  ${PY} "${TMP}/pw-nosec/scripts/check_prohibited.py" "标题" "白嫖证书" ""

echo "───────────────────────────────────────────────────────────"
if [ "${FAIL}" -eq 0 ]; then echo "全部通过"; else echo "有失败项"; fi
exit "${FAIL}"

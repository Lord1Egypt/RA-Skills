#!/usr/bin/env bash
# 退出码回归自测 —— 改完规则 / 脚本后跑一遍，确认 4 条路径没跑偏。
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
    printf '  ✓ %-46s 退出码 %s\n' "${desc}" "${got}"
  else
    printf '  ✗ %-46s 期望 %s，实得 %s\n' "${desc}" "${want}" "${got}"
    FAIL=1
  fi
}

TMP=$(mktemp -d)
trap 'rm -rf "${TMP}"' EXIT
: > "${TMP}/empty-wordlist.md"

# 手机号用拼接构造：仓库文本里不出现完整号码（发布前隐私闸门会拦任何 11 位手机号）
FAKE_PHONE="138""0013""8000"
FAKE_MAIL="someone""@""example.com"

echo "小红书发布前检测 · 退出码自测"
echo "─────────────────────────────────────────────────────"

# 0 = 通过
check 0 "干净文案 → 0（通过）" \
  ${PY} scripts/preflight.py --title "我用AI把100页笔记做成3分钟读完的图" \
  --body "上周整理书架翻出一本小开本唐诗集，顺手做成了图。这套流程我跑通了三遍，现在五分钟出一张。"

# 1 = 有 P0
check 1 "命中 P0 硬词 → 1（禁止发布）" \
  ${PY} scripts/preflight.py --title "AI小白白嫖3个官方证书"

# ⭐ 验收基准：2026-09-12 真实被软限流的那一篇原文。
# 修复前它会回 0（两个 P0 完全拦不住）—— 拦不住这篇，这个 skill 就没有存在理由。
check 1 "★ 验收基准 · 真实翻车案例(2026-09-12) → 1" \
  ${PY} scripts/preflight.py --file examples/示例-真实翻车-20260912.md

# 2 = 只有 P1
check 2 "只超标题字数上限 → 2（可发，建议改）" \
  ${PY} scripts/preflight.py --title "我用AI把100页课程笔记变成了3分钟能读完的图" \
  --body "这是一段足够长的正文，用来避开正文过短的提示，同时不含任何硬词。"

# 组 4 导流：手机号 / 邮箱必须是 P0
check 1 "正文含手机号 → 1（P0 站外导流）" \
  ${PY} scripts/preflight.py --title "一个普通的标题" \
  --body "有问题直接打 ${FAKE_PHONE} 找我，正文够长以避开过短提示。"
check 1 "正文含邮箱 → 1（P0 站外导流）" \
  ${PY} scripts/preflight.py --title "一个普通的标题" \
  --body "发邮件到 ${FAKE_MAIL} 拿资料，正文够长以避开过短提示。"

# 3 = fail-closed（以下都必须不是 0）
check 3 "完全没有输入 → 3（fail-closed）" \
  ${PY} scripts/preflight.py
check 3 "词库路径不存在 → 3（fail-closed）" \
  ${PY} scripts/preflight.py --wordlist "${TMP}/nope.md" --title "我用AI做了个测试"
check 3 "词库是空文件 → 3（fail-closed）" \
  ${PY} scripts/preflight.py --wordlist "${TMP}/empty-wordlist.md" --title "我用AI做了个测试"
check 3 "平台规则文件不存在 → 3（fail-closed）" \
  ${PY} scripts/preflight.py --platform nosuchplatform --title "我用AI做了个测试"

# 词库定位：指定了却找不到 = fail-closed，绝不静默回落到默认词库
# （回归 2026-09-19：SKILL.md 写了支持 XHS_WORDLIST，但脚本从没读它）
check 3 "XHS_WORDLIST 指向不存在的词库 → 3（fail-closed）" \
  env XHS_WORDLIST="${TMP}/nope.md" ${PY} scripts/preflight.py --title "我用AI做了个测试"

# 解析器与词库路径解耦：--wordlist 指向「纯数据文件」也要能跑
# （回归 2026-09-19：原先从词库路径反推 wordlist.py，指向家目录文件就报「解析模块缺失」）
REAL_WL=$(${PY} -c 'import importlib.util; s=importlib.util.spec_from_file_location("pf","scripts/preflight.py"); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(m.find_wordlist() or "")' 2>/dev/null)
if [ -n "${REAL_WL}" ] && [ -f "${REAL_WL}" ]; then
  cp "${REAL_WL}" "${TMP}/custom.md"
  ${PY} - "${TMP}/custom.md" <<'PYEOF'
import io, sys
p = sys.argv[1]
s = io.open(p, encoding="utf-8").read()
i = s.find("## 二、")
io.open(p, "w", encoding="utf-8").write(s[:i] + "| 自造词XYZ | P0 | 自测用 | 删 |\n\n" + s[i:])
PYEOF
  check 1 "自定义词库(纯数据文件) → 1（解析器不绑死路径）" \
    env XHS_WORDLIST="${TMP}/custom.md" ${PY} scripts/preflight.py --title "标题" --body "自造词XYZ"

  # 共享契约：同一个词库 → 两消费方对「有没有 P0」必须一致
  # （preflight 2=只有P1 与 check 0=无P0 是同一判断，故只比对 P0 轴）
  CP="${REAL_WL%/*/*}/scripts/check_prohibited.py"
  if [ -f "${CP}" ]; then
    agree() {
      local a b pa pb
      ${PY} scripts/preflight.py --title "标题" --body "$2" >/dev/null 2>&1; a=$?
      ${PY} "${CP}" "标题" "$2" "" >/dev/null 2>&1; b=$?
      pa=0; pb=0; [ "$a" = "1" ] && pa=1; [ "$b" = "1" ] && pb=1
      if [ "${pa}" = "${pb}" ]; then
        printf '  ✓ %-46s P0 轴一致（preflight=%s check=%s）\n' "$1" "${a}" "${b}"
      else
        printf '  ✗ %-46s P0 轴不一致（preflight=%s check=%s）\n' "$1" "${a}" "${b}"
        FAIL=1
      fi
    }
    agree "P0 轴一致 · 白嫖（实测硬词）" "这类东西白嫖就行，正文够长以避开过短提示。"
    agree "P0 轴一致 · 干净文案" "这是一段足够长的正文，用来避开过短提示，不含硬词。"
    agree "P0 轴一致 · LinkedIn（P1，两边都不阻塞）" "我在LinkedIn上也发，正文够长以避开过短提示。"
  fi
else
  printf '  ! %-46s 跳过（未找到词库 skill）\n' "自定义词库 / 跨工具一致性"
fi

# JSON 输出必须是合法 JSON
if ${PY} scripts/preflight.py --title "无敏感词的标题" --json 2>/dev/null | ${PY} -c 'import json,sys; json.load(sys.stdin)' 2>/dev/null; then
  printf '  ✓ %-46s JSON 合法\n' "--json 输出可被解析"
else
  printf '  ✗ %-46s\n' "--json 输出不是合法 JSON"
  FAIL=1
fi

echo "─────────────────────────────────────────────────────"
if [ "${FAIL}" -eq 0 ]; then echo "全部通过"; else echo "有失败项"; fi
exit "${FAIL}"

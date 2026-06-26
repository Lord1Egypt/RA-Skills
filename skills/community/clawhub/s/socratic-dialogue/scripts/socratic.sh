#!/usr/bin/env bash
# Socratic Dialogue - 苏格拉底式对话
# Powered by silifelab

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="$SCRIPT_DIR/../data"

CMD="${1:-help}"
shift 2>/dev/null || true

show_help() {
  cat <<'EOF'
╔══════════════════════════════════════════════════════════╗
║           🧠 Socratic Dialogue 苏格拉底式对话        ║
╚══════════════════════════════════════════════════════════╝

苏格拉底式对话 - 澄清思想、挑战假设、寻找证据、探寻替代观点。

⚠️  重要声明: 本技能不是给答案，而是陪伴思考。
    相信每个人内在都有智慧，我们只是帮你唤醒它。

Usage: socratic <command> [args...]

Commands:
  clarify              澄清思想模式
  challenge            挑战假设模式
  evidence             寻找证据模式
  explore              探寻替代观点模式
  full                 完整四步对话
  help                 显示此帮助

Examples:
  socratic clarify
  socratic full
  socratic help

  Powered by silifelab
EOF
}

show_intro() {
  echo ""
  echo "═══════════════════════════════════════════════════"
  echo "🧠 苏格拉底式对话"
  echo ""
  echo "核心原则："
  echo "  1. 承认无知 - '我知道我一无所知'"
  echo "  2. 助产术 - 不是给答案，而是帮你'生出'自己的答案"
  echo "  3. 辩证法 - 通过对话和追问，逐步接近真理"
  echo "  4. 反诘法 - 挑战信念，激发思考"
  echo ""
  echo "让我们开始吧。请描述你想思考的问题或想法："
  echo "═══════════════════════════════════════════════════"
  echo ""
}

cmd_clarify() {
  show_intro
  echo "📋 澄清思想模式"
  echo ""
  echo "典型问题："
  echo "  • 你这句话到底是什么意思？"
  echo "  • 你能说得更明确吗？"
  echo "  • 你能举个例子吗？"
  echo "  • 如果用另一种方式说，会是什么？"
  echo "  • 这个概念和那个概念有什么区别？"
  echo ""
  echo "请描述你想澄清的想法或问题："
}

cmd_challenge() {
  show_intro
  echo "📋 挑战假设模式"
  echo ""
  echo "典型问题："
  echo "  • 你这个想法是基于什么假设？"
  echo "  • 这个假设一定成立吗？"
  echo "  • 如果这个假设不成立，会怎样？"
  echo "  • 这个假设的依据是什么？"
  echo "  • 有没有可能这个假设是错的？"
  echo ""
  echo "请描述你的想法或观点："
}

cmd_evidence() {
  show_intro
  echo "📋 寻找证据与理由模式"
  echo ""
  echo "典型问题："
  echo "  • 你为什么这样认为？"
  echo "  • 有什么可以证明？"
  echo "  • 这个理由充分吗？"
  echo "  • 这个证据有多可靠？"
  echo "  • 有没有反例？"
  echo ""
  echo "请描述你的信念或观点："
}

cmd_explore() {
  show_intro
  echo "📋 探寻替代观点与后果模式"
  echo ""
  echo "典型问题："
  echo "  • 还有别的看待方式吗？"
  echo "  • 如果坚持这个观点，会推导出什么？"
  echo "  • 最坏情况是什么？最好情况呢？"
  echo "  • 如果从另一个角度看，会怎样？"
  echo "  • 如果反过来看，会是什么？"
  echo ""
  echo "请描述你的决策或观点："
}

cmd_full() {
  show_intro
  echo "📋 完整四步对话模式"
  echo ""
  echo "步骤："
  echo "  1. 澄清思想"
  echo "  2. 挑战假设"
  echo "  3. 寻找证据"
  echo "  4. 探寻替代观点"
  echo ""
  echo "请描述你想深度思考的问题或想法："
}

case "$CMD" in
  clarify) cmd_clarify ;;
  challenge) cmd_challenge ;;
  evidence) cmd_evidence ;;
  explore) cmd_explore ;;
  full) cmd_full ;;
  help) show_help ;;
  *)
    echo "❌ 未知命令: $CMD"
    echo "运行 'socratic help' 查看帮助"
    exit 1
    ;;
esac
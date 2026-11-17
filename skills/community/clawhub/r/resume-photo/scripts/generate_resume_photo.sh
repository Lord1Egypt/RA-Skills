#!/usr/bin/env bash
# generate_resume_photo.sh — 用当前可用的最佳生图模型，把生活照转成专业简历照。
#
# 用法:
#   generate_resume_photo.sh <原图> [输出路径] [提示词文件]
#   generate_resume_photo.sh --list        # 只显示会选用哪个模型
#
# 环境变量:
#   RESUME_PHOTO_AGENT  指定使用的 agent（多 agent 环境需要，如 xiaozhi）
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ "${1:-}" = "--list" ] || [ "${1:-}" = "-l" ]; then
  exec "$here/pick_image_model.py"
fi

src="${1:-}"
out="${2:-$HOME/Desktop/简历照/$(date +%Y%m%d-%H%M)-简历照.jpg}"
prompt_file="${3:-}"

[ -n "$src" ] || { echo "用法: generate_resume_photo.sh <原图> [输出路径] [提示词文件]" >&2; exit 2; }
[ -f "$src" ] || { echo "找不到原图: $src" >&2; exit 1; }

model="$("$here/pick_image_model.py" 2>/dev/null || true)"
if [ -z "$model" ] || [ "$model" = "NONE" ]; then
  cat >&2 <<'MSG'
✗ 没有可用的图像生成 provider。

任选一种配置方式（配好即可重试）:
  1) API key:   openclaw models auth paste-api-key     # OpenAI / Google / OpenRouter / fal
     或放入环境: OPENAI_API_KEY / GEMINI_API_KEY / OPENROUTER_API_KEY / FAL_KEY
  2) 订阅登录:   openclaw models auth login            # OpenAI ChatGPT/Codex OAuth

然后设置默认图像模型（也可跳过，本脚本会自动挑）:
  openclaw models set-image google/gemini-3.1-flash-image
MSG
  exit 3
fi

if [ -n "$prompt_file" ] && [ -f "$prompt_file" ]; then
  prompt="$(cat "$prompt_file")"
else
  prompt='将这张生活照转化为高端专业简历照（符合职场求职 / 面试正式风格）。
保持人物原有五官与身份特征不变，仅微调表情至自然得体状态（温和微笑、眼神专注）。
背景替换为纯色简约款（浅蓝色），无任何杂物干扰；柔和均匀的专业布光。
服装升级为白色衬衫或浅色系合身西装，避免花纹、亮色与休闲服饰。
姿态端正舒展：正面、肩膀放平、头部微正。
色调明亮干净，保留皮肤纹理与衣物细节，拒绝过度磨皮、瘦脸等失真美颜。
人物居中，适当留白。输出高清高质感的专业人像，适合简历打印与电子档。
严格约束：不得改变人物身份、脸型、五官比例、年龄与性别；背景内无文字、水印、logo、杂物。'
fi

agent_args=()
[ -n "${RESUME_PHOTO_AGENT:-}" ] && agent_args=(--agent "$RESUME_PHOTO_AGENT")

# OpenAI 走 size；Google/OpenRouter/xAI 走 aspect-ratio + resolution
case "$model" in
  openai/*) geo=(--size 1024x1536) ;;
  *)        geo=(--aspect-ratio 3:4 --resolution 2K) ;;
esac

mkdir -p "$(dirname "$out")"
echo "使用模型: $model" >&2
openclaw infer image edit "${agent_args[@]+"${agent_args[@]}"}" --model "$model" --file "$src" \
  --prompt "$prompt" "${geo[@]}" --quality high --output-format jpeg \
  --output "$out" --json
echo "已输出: $out" >&2

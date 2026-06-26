#!/usr/bin/env bash
#
# setup_token.sh — 将妙问 Access Token 保存到文件
#
# 用法: bash setup_token.sh "<YOUR_TOKEN>"
#
# Token 存储位置: ~/.MIAOWEN_ACCESS_TOKEN
#

set -euo pipefail

TOKEN="${1:-}"

# 检查 HOME 目录
if [ -z "${HOME:-}" ]; then
    echo "[ERROR] 无法确定用户 HOME 目录，请检查系统环境配置。"
    exit 1
fi

TOKEN_FILE="${HOME}/.MIAOWEN_ACCESS_TOKEN"

if [ -z "$TOKEN" ]; then
    echo "[ERROR] 请提供 Token 参数"
    echo "用法: bash setup_token.sh \"<YOUR_TOKEN>\""
    exit 1
fi

# 将 Token 写入文件（覆盖旧内容）
echo -n "$TOKEN" > "$TOKEN_FILE"

# 设置文件权限为仅当前用户可读写（保护 Token 安全）
# 注：Windows 环境下 chmod 可能不生效，但不影响功能使用
if chmod 600 "$TOKEN_FILE" 2>/dev/null; then
    echo "[SUCCESS] Token 已成功保存到 ${TOKEN_FILE}"
    echo "  文件权限已设置为仅当前用户可读写 (600)"
else
    echo "[SUCCESS] Token 已成功保存到 ${TOKEN_FILE}"
    echo "  注意：当前系统不支持 chmod，无法设置文件权限。如果您在 Windows 环境下，请确保该文件不被其他用户访问。"
fi

echo ""
echo "配置完成！现在可以直接使用妙问问答了。"

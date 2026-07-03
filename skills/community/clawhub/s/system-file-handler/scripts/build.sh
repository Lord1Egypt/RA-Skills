#!/usr/bin/env bash
# 从 go-fs-mcp 仓库根目录构建 server 与 skill 二进制。
# 用法：bash publish-skill/scripts/build.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

export GOPROXY="${GOPROXY:-https://goproxy.cn,direct}"

echo "==> go mod tidy"
go mod tidy

echo "==> build go-fs-mcp-server"
go build -o go-fs-mcp-server/go-fs-mcp-server ./go-fs-mcp-server/cmd/server

echo "==> build go-fs-mcp-skill"
go build -o go-fs-mcp-skill/go-fs-mcp-skill ./go-fs-mcp-skill/cmd/skill

chmod +x go-fs-mcp-server/go-fs-mcp-server go-fs-mcp-skill/go-fs-mcp-skill

echo "==> done"
echo "    server: $ROOT/go-fs-mcp-server/go-fs-mcp-server"
echo "    skill:  $ROOT/go-fs-mcp-skill/go-fs-mcp-skill"
echo ""
echo "Next: copy binaries to your OpenClaw skill dir and edit skill.json mcp_command."

#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# Publish Skill Repo - 将 Skill 项目发布到 GitHub 并同步到 ClawHub
# ============================================================================
#
# 运行前请确保已完成以下准备工作：
#
# 1. 获取 ClawHub Token 并保存到本地：
#    - 访问 https://clawhub.ai/ → Login with GitHub → Settings → API tokens → Create token
#    - 保存 Token：
#      mkdir -p ~/.clawhub
#      echo "your-clawhub-token" > ~/.clawhub/secret_token
#      chmod 600 ~/.clawhub/secret_token
#
# 2. 安装并登录 GitHub CLI：
#    - macOS: brew install gh
#    - 登录: gh auth login
#
# 用法:
#   ./scripts/publish-skill-repo.sh /path/to/your-skill [github-owner] [public|private]
#
# 也可通过 SKILL.md 作为 Claude Code 技能使用，交互式引导发布流程。
# ============================================================================

SKILL_DIR="${1:-}"
OWNER="${2:-$(gh api user --jq .login)}"
VISIBILITY="${3:-public}"
TOKEN_FILE="${HOME}/.clawhub/secret_token"

if [[ -z "$SKILL_DIR" ]]; then
  echo "用法: $0 <skill目录> [github-owner] [public|private]"
  exit 1
fi

if [[ ! -d "$SKILL_DIR" ]]; then
  echo "目录不存在: $SKILL_DIR"
  exit 1
fi

if [[ ! -f "$SKILL_DIR/SKILL.md" ]]; then
  echo "缺少 SKILL.md: $SKILL_DIR/SKILL.md"
  exit 1
fi

REPO_NAME="$(basename "$SKILL_DIR")"
REPO_FULL="$OWNER/$REPO_NAME"

detect_main_branch() {
  local branch
  branch="$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')" && echo "$branch" && return
  branch="$(git config --get init.defaultBranch)" && echo "$branch" && return
  echo "main"
}

echo "==> 检查 gh 登录状态"
gh auth status >/dev/null

echo "==> 进入目录: $SKILL_DIR"
cd "$SKILL_DIR"

NEW_REPO=false
MAIN_BRANCH="main"
if [[ ! -d .git ]]; then
  echo "==> 初始化 git"
  MAIN_BRANCH="$(git config --get init.defaultBranch 2>/dev/null || echo main)"
  git init -b "$MAIN_BRANCH"
  NEW_REPO=true
else
  MAIN_BRANCH="$(detect_main_branch)"
fi

if [[ ! -f LICENSE ]]; then
  echo "==> 创建 MIT LICENSE"
  YEAR=$(date +%Y)
  cat > LICENSE <<EOF
MIT License

Copyright (c) $YEAR $OWNER

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
fi

if [[ ! -f .github/workflows/publish-to-clawhub.yml ]]; then
  echo "==> 创建 workflow"
  mkdir -p .github/workflows

  cat > .github/workflows/publish-to-clawhub.yml <<'YAML'
name: Publish Skill to ClawHub

on:
  push:
    tags:
      - "v*.*.*"

jobs:
  publish:
    runs-on: ubuntu-latest

    permissions:
      contents: read

    env:
      CLAWHUB_TOKEN: ${{ secrets.CLAWHUB_TOKEN }}

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install ClawHub CLI
        run: npm install -g clawhub

      - name: Extract metadata
        id: meta
        shell: bash
        run: |
          TAG="${GITHUB_REF#refs/tags/}"
          VERSION="${TAG#v}"
          REPO_NAME="${GITHUB_REPOSITORY#*/}"

          echo "tag=$TAG" >> "$GITHUB_OUTPUT"
          echo "version=$VERSION" >> "$GITHUB_OUTPUT"
          echo "slug=$REPO_NAME" >> "$GITHUB_OUTPUT"
          echo "name=$REPO_NAME" >> "$GITHUB_OUTPUT"

      - name: Validate required files
        shell: bash
        run: |
          test -f SKILL.md || (echo "SKILL.md not found" && exit 1)

      - name: Login to ClawHub
        run: clawhub login --token "$CLAWHUB_TOKEN"

      - name: Publish to ClawHub
        shell: bash
        run: |
          clawhub publish . \
            --slug "${{ steps.meta.outputs.slug }}" \
            --name "${{ steps.meta.outputs.name }}" \
            --version "${{ steps.meta.outputs.version }}" \
            --tags "latest" \
            --changelog "Release ${{ steps.meta.outputs.tag }} from GitHub"

      - name: Success summary
        run: |
          echo "Published slug: ${{ steps.meta.outputs.slug }}"
          echo "Published version: ${{ steps.meta.outputs.version }}"
          echo "Source tag: ${{ steps.meta.outputs.tag }}"
YAML
else
  echo "==> workflow 已存在，跳过"
fi

# 从 SKILL.md 提取 description
SKILL_DESC=""
if [[ -f SKILL.md ]]; then
  SKILL_DESC="$(sed -n '/^---$/,/^---$/p' SKILL.md | sed -n 's/^description: *//p' | head -1)"
fi

if gh repo view "$REPO_FULL" >/dev/null 2>&1; then
  echo "==> GitHub 仓库已存在: $REPO_FULL"
else
  echo "==> 创建 GitHub 仓库: $REPO_FULL"
  gh repo create "$REPO_FULL" --"$VISIBILITY" --source=. --remote=origin --push=false --description "${SKILL_DESC:-}"
fi

# 设置仓库 About（仅当仓库无 description 时）
CURRENT_DESC="$(gh repo view "$REPO_FULL" --json description --jq '.description // ""')"
if [[ -z "$CURRENT_DESC" && -n "$SKILL_DESC" ]]; then
  echo "==> 设置仓库 About"
  gh repo edit "$REPO_FULL" --description "$SKILL_DESC"
fi

echo "==> 检查仓库 Secret"
if gh secret list --repo "$REPO_FULL" 2>/dev/null | grep -q "^CLAWHUB_TOKEN"; then
  echo "    CLAWHUB_TOKEN 已存在，跳过"
else
  if [[ ! -f "$TOKEN_FILE" ]]; then
    echo "未找到 token 文件: $TOKEN_FILE"
    exit 1
  fi

  CLAWHUB_TOKEN="$(tr -d '\r\n' < "$TOKEN_FILE")"

  if [[ -z "$CLAWHUB_TOKEN" ]]; then
    echo "token 文件为空: $TOKEN_FILE"
    exit 1
  fi

  echo "    设置 CLAWHUB_TOKEN"
  gh secret set CLAWHUB_TOKEN --repo "$REPO_FULL" --body "$CLAWHUB_TOKEN"
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  echo "==> 添加远程 origin"
  git remote add origin "https://github.com/$REPO_FULL.git"
fi

HAS_NEW_COMMITS=false
echo "==> 提交代码"
git add .
if git diff --cached --quiet; then
  echo "没有新的变更可提交"
else
  HAS_NEW_COMMITS=true
  if [[ "$NEW_REPO" == "true" ]]; then
    git commit -m "chore: init skill repo"
  else
    STAGED_FILES="$(git diff --cached --name-only)"
    COMMIT_PARTS=""
    echo "$STAGED_FILES" | grep -q '^LICENSE$'         && COMMIT_PARTS="$COMMIT_PARTS, add license"
    echo "$STAGED_FILES" | grep -q '^\.github/workflows/' && COMMIT_PARTS="$COMMIT_PARTS, add publish workflow"
    OTHER="$(echo "$STAGED_FILES" | grep -v '^LICENSE$' | grep -v '^\.github/workflows/')"
    [[ -n "$OTHER" ]] && COMMIT_PARTS="$COMMIT_PARTS, update skill files"
    git commit -m "chore: ${COMMIT_PARTS#, }"
  fi
fi

LOCAL_AHEAD="$(git log "origin/$MAIN_BRANCH".."$MAIN_BRANCH" --oneline 2>/dev/null | wc -l | tr -d ' ')"
if [[ "$HAS_NEW_COMMITS" == "true" || "${LOCAL_AHEAD:-0}" -gt 0 ]]; then
  CURRENT_BRANCH="$(git branch --show-current)"
  if [[ "$CURRENT_BRANCH" != "$MAIN_BRANCH" ]]; then
    echo "==> 当前在 $CURRENT_BRANCH 分支，合并到 $MAIN_BRANCH"
    git checkout "$MAIN_BRANCH"
    git merge "$CURRENT_BRANCH"
    echo "==> 推送 $MAIN_BRANCH"
    git push -u origin "$MAIN_BRANCH"
    git checkout "$CURRENT_BRANCH"
  else
    echo "==> 推送 $MAIN_BRANCH"
    git push -u origin "$MAIN_BRANCH"
  fi
else
  echo "==> 本地无新提交，跳过推送"
fi

if [[ "$NEW_REPO" == "true" ]]; then
  echo "==> 新仓库，创建 v1.0.0 tag"
  git tag v1.0.0
  git push origin v1.0.0
  echo ""
  echo "完成:"
  echo "  仓库: https://github.com/$REPO_FULL"
  echo "  已发布 v1.0.0 到 ClawHub"
else
  echo ""
  echo "完成:"
  echo "  仓库: https://github.com/$REPO_FULL"
  echo "  如需发布新版本:"
  echo "    git tag v1.x.x"
  echo "    git push origin v1.x.x"
fi

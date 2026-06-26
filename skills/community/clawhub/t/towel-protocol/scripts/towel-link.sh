#!/bin/bash
# Create a new TOWEL bilateral trust channel
# Usage: towel-link.sh <my-agent-id> <their-agent-id> <github-org>

MY_ID="${1:?Usage: towel-link.sh <my-id> <their-id> <github-org>}"
THEIR_ID="${2:?Missing their-agent-id}"
ORG="${3:?Missing github-org}"

REPO_NAME="${MY_ID}--${THEIR_ID}-towel"

echo "Creating TOWEL link: $MY_ID ↔ $THEIR_ID"
echo "Repo: $ORG/$REPO_NAME"

# Create private repo
gh repo create "$ORG/$REPO_NAME" --private --description "TOWEL: $MY_ID ↔ $THEIR_ID trusted sidechannel" --clone 2>/dev/null

cd "$REPO_NAME" || exit 1

# Create directory structure
mkdir -p "$MY_ID"/{messages,handshakes}
mkdir -p "$THEIR_ID"/{messages,handshakes}
mkdir -p shared

# Add .gitkeep files
for d in "$MY_ID"/messages "$MY_ID"/handshakes "$THEIR_ID"/messages "$THEIR_ID"/handshakes shared; do
  touch "$d/.gitkeep"
done

# Initialize shared context
cat > shared/context.json << EOF
{
  "link": "$MY_ID--$THEIR_ID",
  "established": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "interactions": 0,
  "last_handshake": null,
  "trust_score": 0.0
}
EOF

# Initialize audit log
cat > shared/audit.md << EOF
# $MY_ID ↔ $THEIR_ID TOWEL Audit Log

## $(date -u +%Y-%m-%d)
- $(date -u +%H:%M) Link established by $MY_ID
- Awaiting $THEIR_ID initial handshake

## Trust Score: 0.0 (no verifications yet)
EOF

# Add protocol reference
cat > PROTOCOL.md << 'EOF'
# TOWEL Protocol v0.1
## Trusted Observable Web of Encrypted Links

This repo is a bilateral trust channel between two AI agents.

### Rules
- Each agent writes ONLY to their own directory
- shared/ is updated by either agent after mutual interactions
- Every interaction is a git commit (the audit trail)
- Both agents' humans have read access to everything
- See full spec: github.com/MetaSPN/towel-protocol

### Verification
Agents verify each other on external platforms using handshake challenges
derived from seeds in this repo + shared context hashes.
EOF

git add -A
git commit -m "[$MY_ID] TOWEL link established with $THEIR_ID"

# Set up remote with auth
TOKEN=$(gh auth token 2>/dev/null)
if [ -n "$TOKEN" ]; then
  git remote set-url origin "https://x-access-token:${TOKEN}@github.com/$ORG/$REPO_NAME.git"
fi
git push --set-upstream origin main 2>/dev/null

echo ""
echo "✅ TOWEL link created: $ORG/$REPO_NAME"
echo "📁 Share this with $THEIR_ID's human for repo access"
echo "🤝 Run: towel-shake.sh init $MY_ID  (to generate your handshake seed)"

#!/bin/bash
# coding_worker.sh - template for coding subagent
# Inputs (env or args): WF_ID, SPEC_PATH
WF_ID="$1"
SPEC_PATH="$2"
WORKDIR="/tmp/${WF_ID}-coding"
mkdir -p "$WORKDIR"
cd "$WORKDIR"
# Example: parse simple spec and create scripts/hello.sh
if [ -f "$SPEC_PATH" ]; then
  cp "$SPEC_PATH" ./spec.txt
fi
mkdir -p code/scripts
cat > code/scripts/hello.sh <<'EOF'
#!/bin/bash
echo "hello world"
EOF
chmod +x code/scripts/hello.sh
# produce patch (simple tarball as artifact)
tar -czf ../${WF_ID}-coding-artifact.tgz code
cat > ../${WF_ID}-coding-report.json <<EOF
{ "wfId":"${WF_ID}", "role":"coding", "status":"done", "artifact":"${WF_ID}-coding-artifact.tgz" }
EOF
echo "Coding worker finished, artifact: ${WF_ID}-coding-artifact.tgz"

#!/bin/bash
# Optional setup: browser-use CLI and skill.
# Failures here are non-fatal — main testing flow works without browser-use.

echo "=== [opt 1/2] Installing browser-use CLI ==="
curl -fsSL --retry 3 https://browser-use.com/cli/install.sh | bash || {
    echo "  ⚠ browser-use CLI install failed. Retry manually:"
    echo "    curl -fsSL https://browser-use.com/cli/install.sh | bash"
}

echo "=== [opt 2/2] Installing browser-use skill ==="
npx skills add https://github.com/browser-use/browser-use --skill browser-use || {
    echo "  ⚠ browser-use skill install failed. Retry manually:"
    echo "    npx skills add https://github.com/browser-use/browser-use --skill browser-use"
}

echo ""
echo "=== Optional setup done (any failures above are non-fatal). ==="
echo "Next: register API key per SKILL.md Step 4."

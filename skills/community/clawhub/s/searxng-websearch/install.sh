#!/usr/bin/env bash
# install.sh — installs wsearch / wfetch / wresearch shims to ~/.local/bin
# Run once: bash install.sh
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_DIR="${SKILL_DIR}/scripts"
BIN_DIR="${HOME}/.local/bin"
mkdir -p "$BIN_DIR"

install_shim() {
    local name="$1"
    local script="${SCRIPTS_DIR}/$2"
    local target="${BIN_DIR}/${name}"

    if [[ ! -f "$script" ]]; then
        echo "  WARNING: script not found: $script — skipping $name"
        return
    fi

    cat > "$target" <<SHIM
#!/usr/bin/env bash
exec python3 "${script}" "\$@"
SHIM
    chmod +x "$target"
    echo "  installed: ${target}  ->  ${script}"
}

echo "Installing shims from: $SCRIPTS_DIR"
install_shim wsearch      websearch.py
install_shim wfetch       fetch_page.py
install_shim wresearch    deep_research.py

# Make sure ~/.local/bin is on PATH
for RC in "$HOME/.bashrc" "$HOME/.zshrc"; do
    if [[ -f "$RC" ]] && ! grep -q '\.local/bin' "$RC"; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$RC"
        echo "  added PATH entry to: $RC"
    fi
done

echo ""
echo "Done! Reload your shell or run:"
echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
echo ""
echo "Verify:"
echo "  wsearch   \"test query\" --format agent"
echo "  wfetch    https://example.com"
echo "  wresearch \"topic\" --fetch-top-pages 2"

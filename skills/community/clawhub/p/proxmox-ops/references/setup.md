# Proxmox Ops — first-time setup

Create a credential file at `~/.proxmox-credentials`:

```bash
cat > ~/.proxmox-credentials <<'EOF'
PROXMOX_HOST=https://<your-proxmox-ip>:8006
PROXMOX_TOKEN_ID=user@pam!tokenname
PROXMOX_TOKEN_SECRET=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
EOF
chmod 600 ~/.proxmox-credentials
```

**Alternative:** Set `PROXMOX_HOST`, `PROXMOX_TOKEN_ID`, and `PROXMOX_TOKEN_SECRET` as environment variables directly (useful for CI/agent contexts). The helper script checks env vars first, then falls back to sourcing `~/.proxmox-credentials`.

Create API token in Proxmox: Datacenter → Permissions → API Tokens → Add. Use least-privilege: only grant the permissions your workflow requires (e.g., `PVEAuditor` for read-only monitoring, `PVEVMAdmin` for VM control). Disable Privilege Separation only if your workflow requires full API access.

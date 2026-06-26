# UFW Playbook

## Baseline policy

Use this on Ubuntu hosts that should accept only explicitly approved inbound traffic.

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

## LAN-only service examples

Use the host's actual LAN subnet and only the ports the user confirms are needed.

```bash
sudo ufw allow from <lan-cidr> to any port 22 proto tcp comment 'SSH from LAN'
sudo ufw allow from <lan-cidr> to any port <dashboard-port> proto tcp comment 'Dashboard from LAN'
sudo ufw allow from <lan-cidr> to any port <rdp-port> proto tcp comment 'RDP from LAN'
sudo ufw allow from <lan-cidr> to any port <vnc-port> proto tcp comment 'VNC from LAN'
```

## Single-host metrics restriction

Prefer a single-host rule for metrics when only one scraper needs access.

```bash
sudo ufw allow from <metrics-scraper-ip> to any port <metrics-port> proto tcp comment 'Metrics scraper'
```

## Safe apply sequence

1. Confirm the management path in use now.
2. Add SSH allow rule first if SSH is in use.
3. Apply LAN-only and single-host rules.
4. Enable UFW.
5. Verify reachability from expected clients.

## Review rules

```bash
sudo ufw status numbered
sudo ufw status verbose
```

## Remove rules

```bash
sudo ufw delete <number>
```

## Backup current rules

```bash
sudo ufw status numbered > ~/ufw-rules-$(date +%F).txt
sudo iptables-save > ~/iptables-$(date +%F).save
```

## Notes

- Do not expose remote desktop or VNC ports directly to the public internet.
- Do not expose `/metrics` broadly.
- OpenClaw WhatsApp/Discord integrations usually do not need new inbound firewall rules; outbound access is typically enough.

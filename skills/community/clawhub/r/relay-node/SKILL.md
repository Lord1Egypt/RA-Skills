# Relay Node Skill

**Status:** 🚧 Vorbereitend - Node 3 als Proof of Concept

## Zweck
Relay Nodes leiten Verbindungen weiter wenn direkte Pfade nicht möglich sind (z.B. Node 3 ohne WireGuard, Mobile-Clients im NAT).

## Verwendung
```bash
# Relay-Modus aktivieren
openclaw cluster relay enable --mode [socks5|ssh|wg-proxy]

# Relay-Status prüfen
openclaw cluster relay status

# Port-Weiterleitung konfigurieren
openclaw cluster relay forward --local <port> --remote <host:port>

# Verbundene Clients anzeigen
openclaw cluster relay connections
```

## Einsatz-Szenarien

### Szenario 1: Node 3 (WireGuard-fallback → SSH-Relay)
Node 3 hat kein WireGuard-Modul → Relay via SSH-Tunnel

```
Node 4 (Mobile)
     │
     │ WireGuard
     ▼
Node 1 (Gateway: 10.10.0.1)
     │
     │ Route via Node 3?
     ▼
Node 3 (10.10.0.3) ❌ Kein WG
     │
     ▼ SSH-Tunnel (Active)
Node 3: localhost:18788 → Node 1
```

### Szenario 2: Mobile Relay im NAT
Node 4 (Redmi) hinter Carrier-NAT → Relay via Node 2

```
Node 4 (Mobile, CGNAT)
     │
     ├─→ Ausgehende Verbindung zu Node 2
     │
Node 2 (Public IP)
     │
     ├─← Relay zurück zu Node 4
     │
Node 1 (Gateway)
```

### Szenario 3: File-Sharing Relay
Node 5 (Webhosting) → Node 3 (Storage)

```
Internet User
     │
     │ HTTP Download
     ▼
Node 5: xstoragex.de
     │
     │ SFTP/SCP
     ▼
Node 3: /home/share/
```

## Relay-Modi

| Modus | Port | Verwendung |
|-------|------|------------|
| `socks5` | 1080 | Proxy für Anwendungen |
| `ssh-tunnel` | Dynamisch | Port-Forwarding |
| `wg-proxy` | 51820 | WireGuard über TCP |
| `http-proxy` | 8080 | HTTP/HTTPS Proxy |
| `tcp-bridge` | Beliebig | Direkte Port-Bridge |

## Node 3 Konfiguration (Aktuell)

```ini
# SSH-Tunnel Relay
[relay-node-3]
type = ssh-tunnel
gateway_host = 127.0.0.1
gateway_port = 18788
local_proxy_port = 1080
protocol = relay
```

## Zukünftige Erweiterung

```bash
# Automatischer Modus-Wechsel
openclaw cluster relay auto

# Mehrere Relay-Hops
openclaw cluster relay chain --via node-2 --via node-3
```

## Offene Punkte
- [ ] Node 3: WireGuard-Modul nach Kernel-Update
- [ ] Node 4: Relay-Konfiguration nach Pairing
- [ ] Node 2 → Node 3 Ressourcen-Sharing

## Siehe auch
- [Cluster Gateway Skill](../cluster-gateway/SKILL.md)
- [Worker Node Skill](../worker-node/SKILL.md)

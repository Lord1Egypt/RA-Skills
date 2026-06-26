# Validation Findings

Current fast validation:

- `test_runtime_common.sh`: passes
- `test_session_manifest.sh`: passes
- `test_browser_runtime.sh`: passes
- `test_open_protected_page.sh`: passes
- `test_assisted_session.sh`: passes
- `test_profile_resolution.sh`: passes
- `test_identity_provider_reuse.sh`: passes
- `test_site_session_registry.sh`: passes

Important behavioral coverage now includes:

- canonical site-key resolution
- corruption-safe site registry handling
- site-first profile resolution
- capture writing both manifest and site registry
- loopback plus LAN noVNC URL reporting
- wrong-page recovery before escalating to user takeover

Real-host validation on 2026-03-15:

- GitHub default site identity captured successfully
- Google default site identity captured successfully
- `~/.agent-browser/index/site-sessions.json` rebuilt with:
  - `github.com`
  - `google.com`
- OpenClaw `main` agent successfully reused both:
  - `https://github.com/settings/profile`
  - `https://myaccount.google.com/`

Operational note:

- direct LAN noVNC access may still require opening the corresponding host firewall port
- when LAN access is blocked, the loopback noVNC URL is still valid through SSH port forwarding

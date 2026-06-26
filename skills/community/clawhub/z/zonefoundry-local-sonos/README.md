# ZoneFoundry Local Sonos Skill

This skill teaches an OpenClaw-compatible agent how to control Sonos locally, verify service readiness, and recover playback through the `zf` CLI from [ZoneFoundry](https://github.com/kisssam6886/zonefoundry).

It is designed for:

- local Sonos playback control
- first-run readiness checks
- safe queue and transport actions
- service-linking readiness checks
- recovery from common room-local playback problems

Common service examples include:

- Spotify
- Apple Music
- QQ Music
- NetEase Cloud Music
- other Sonos-linked services that the local runtime reports as ready

## Audience

This package is intentionally **English-first** so global users can scan it quickly.

Chinese-language examples are still included because ZoneFoundry also targets:

- QQ Music
- NetEase Cloud Music
- bilingual households
- China/HK users who mix English commands with Chinese room or service names

## Product boundary

This skill does **not** turn ZoneFoundry into the Sonos app.

- Sonos official iOS / Android apps remain the default path for adding or logging in to music services
- Sonos Web App may help with playback views when supported, but first-time service linking should still start from official Sonos surfaces
- ZoneFoundry is the local readiness and execution layer once a same-LAN runtime is available
- persistent local bot control requires an always-on same-LAN node such as a PC, NAS, Raspberry Pi, mini PC, Docker host, or Home Assistant host

## Runtime requirements

- `zf` binary available on the local machine
- same LAN as the Sonos system
- for persistent bot / automation flows: an always-on local node

## Install and update

Install the skill:

```bash
clawhub install zonefoundry-local-sonos
```

Update the skill package itself:

```bash
clawhub update zonefoundry-local-sonos
```

Update the local `zf` runtime separately:

```bash
zf update self --check --format json
zf update self --format json
```

These are different update paths:

- `clawhub update zonefoundry-local-sonos` updates the skill instructions and bundled references
- `zf update self` updates the local ZoneFoundry CLI runtime

## Install note

The skill metadata currently installs `zf` from `@latest`.

That is convenient for end users, but it is less reproducible than a pinned tag or pinned commit. If you want stricter release-to-install consistency later, change the install metadata in `SKILL.md` to a tagged version or pinned commit before the next publish.

## File map

- `SKILL.md`: main runtime instructions for the agent
- `agents/openai.yaml`: concise agent-facing prompt metadata
- `references/command-map.md`: concrete command examples and recovery rules
- `references/onboarding-boundary.md`: mobile-only and product-boundary rules
- `references/china-service-linking.md`: QQ Music / NetEase Cloud Music readiness notes

## License split

- This **skill package** is licensed under **MIT-0**
- The underlying **ZoneFoundry repository** is licensed separately under **FSL-1.1**, with an MIT future license after `2028-03-20`

That distinction matters because the skill package contains instructions and references, while the installed `zf` binary comes from the ZoneFoundry repo itself and follows the repo license terms.

## 简短中文说明

这份 skill 现在采用“英文优先、中文补充”的结构。

原因不是放弃中国用户，而是让国际用户第一眼也能看懂它是做什么的；中国音乐服务、中文示例和授权细节仍然保留在 `SKILL.md` 与 `references/` 里。

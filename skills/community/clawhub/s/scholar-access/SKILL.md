---
name: scholar-access
description: 通过中国教育网官方学术通道（scholar.edu.cn / scholar.work，即官方学术浏览器 scholartools 所使用的智能 DNS + 反向代理）访问 GitHub、HuggingFace、Docker Hub、Google Scholar、Wikipedia 等境外学术资源，让任何 Agent 无需翻墙即可合规访问。Routes blocked academic sites through the official CERNET "Scholar" reverse proxy used by the official scholartools academic-browser client — compliant, VPN-free access for any Agent.
whenToUse: Use when a request to github.com, huggingface.co, hub.docker.com, registry-1.docker.io, scholar.google.com, wikipedia.org, anthropic.com, chatgpt.com, biorxiv.org or similar foreign domains times out, hangs, or fails with an SSL/certificate error, and the machine has a working education-network (CERNET) route.
---

# Scholar Access — 学术资源浏览器协议模拟

The Chinese education network (`scholar.edu.cn`, backend `scholar.work`) runs a
**smart-DNS + reverse-proxy** service so campus users can reach international
academic resources. This is the **official academic access channel** used by the
official academic-browser client `scholartools` (学术浏览器). `scholartools`
normally installs a system-wide local DNS + root CA (needs root); this skill
reproduces the same protocol as **user-space tools that need no root**, so any
Agent can compliantly reach academic resources without a VPN (不翻墙).

## Mechanism (reverse-engineered)

1. **DNS-over-HTTPS** at `https://doh.scholar.work/dns-query` maps a blocked
   foreign hostname onto a reverse-proxy farm in `205.164.50.0/24`.
   Unsupported hostnames return `REFUSED` (0 answers).
2. The proxy at `205.164.50.x` terminates TLS with a cert signed by
   **`Scholar Root CA v1`** (bundled as `scholar-root-ca.pem`) and fetches the
   real site through the education network's international channel.
3. So: resolve via DoH → dial the `205.164.50.x` IP **with the original SNI/Host**
   → trust the Scholar CA (or `-k`).

## Bundled tools (all in this skill's directory)

| File | Purpose |
|---|---|
| `scholar-resolve.py <host>` | Resolve a hostname via DoH; prints proxy IPs (205.164.50.x) or errors on REFUSED. |
| `scholar-fetch.sh <url> [curl args...]` | `curl` wrapper: auto-resolves and rewrites the connection via `--resolve` + bundled CA. |
| `scholar-proxy.py [--listen 127.0.0.1:1080]` | Local HTTPS CONNECT proxy for git / docker / pip / any HTTPS client (no root). |
| `scholar-root-ca.pem` | The `Scholar Root CA v1` certificate. |

`SCHOLAR_CA` env var overrides the CA path; `SCHOLAR_PORT` overrides the TLS port
(default 443).

## Quick start — fetch a URL

```bash
cd "$(dirname "$0")"   # or use the skill's directory path
./scholar-fetch.sh https://github.com/torvalds/linux/archive/refs/heads/master.tar.gz -o linux.tar.gz
./scholar-fetch.sh https://huggingface.co/bert-base-uncased/resolve/main/config.json -o config.json
./scholar-fetch.sh https://raw.githubusercontent.com/octocat/Hello-World/master/README
```

Direct `curl` equivalent (if you prefer to inline it):

```bash
IP=$(./scholar-resolve.py github.com | head -n1)   # e.g. 205.164.50.200
curl --resolve "github.com:443:$IP" --cacert scholar-root-ca.pem https://github.com/...
# or skip verification:  curl --resolve "github.com:443:$IP" -k https://github.com/...
```

## git clone / git pull (no root)

Start the local proxy, then point git at it. The proxy keeps SNI correct, so
plain `https_proxy` works:

```bash
nohup ./scholar-proxy.py --listen 127.0.0.1:1080 > /tmp/scholar-proxy.log 2>&1 &
export https_proxy=http://127.0.0.1:1080 http_proxy=http://127.0.0.1:1080
GIT_SSL_NO_VERIFY=1 git clone https://github.com/<owner>/<repo>.git
# When finished:
unset https_proxy http_proxy
pkill -f scholar-proxy.py   # or keep it running for the session
```

`git clone`, `git fetch`, `git pull` and `git ls-remote` all work through this
proxy for `github.com`.

## docker pull

`registry-1.docker.io` and `hub.docker.com` are proxied. Route the docker
daemon through the local proxy (daemon-level, needs a docker daemon restart on
Linux) or use `docker pull` with a proxy-configured daemon:

```bash
# export these before starting dockerd, or set in /etc/systemd/system/docker.service.d/http-proxy.conf
export HTTPS_PROXY=http://127.0.0.1:1080 HTTP_PROXY=http://127.0.0.1:1080
docker pull nginx
```

## Verified proxied domains

`205.164.50.x` is returned for (non-exhaustive): `github.com`,
`raw.githubusercontent.com`, `huggingface.co`, `hf.co`, `cdn-lfs.hf.co` (model
files), `hub.docker.com`, `registry-1.docker.io`, `scholar.google.com`,
`www.google.com`, `www.google.com.hk`, `www.wikipedia.org`, `en.wikipedia.org`,
`www.anthropic.com`, `www.perplexity.ai`, `chatgpt.com`, `biorxiv.org`.

**Not proxied** (DoH returns REFUSED — do not expect these to work):
`api.github.com`, `codeload.github.com`, `objects.githubusercontent.com`,
`gist.githubusercontent.com`, `api.anthropic.com`, `pypi.org`, `stackoverflow.com`.

Implication: GitHub *web UI* and *raw file* access work, but the GitHub REST API
and release-asset downloads (`objects.githubusercontent.com`) do **not** go
through this proxy. For GitHub release assets, fetch the repo page and use a
direct `raw.githubusercontent.com` or `github.com` asset URL when possible.

## When the proxy is not needed

If the target hostname is reachable directly (or the DoH returns a non-`205.164.50.x`
IP, e.g. `gitlab.com`), skip the proxy and connect normally.

## Diagnostics

```bash
./scholar-resolve.py github.com          # expect 205.164.50.x
./scholar-resolve.py api.github.com      # expect ERROR (REFUSED)
curl -sk --resolve github.com:443:205.164.50.200 https://github.com/ | head -c 200
```

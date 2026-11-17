# qshare

Share one local file with one command, without an account or login. By default,
qshare uploads it to a CNB Release and displays a public download URL and QR code.
CNB files kept after upload are stored for 3 days by default; you can also manually
delete the current upload immediately at the post-upload prompt. Add `--cf` to serve
the file from your own machine through a TryCloudflare tunnel.

[中文](https://github.com/steinvenic/qshare/blob/main/README.md) · [PyPI](https://pypi.org/project/qshare/) · [Agent skill](https://github.com/steinvenic/qshare/blob/main/SKILL.md)

## Features

- No account or login required
- One-command sharing of a local file
- CNB uploads by default, with upload progress
- CNB storage for 3 days by default, with immediate manual deletion after upload
- Optional `--cf` tunnel sharing with a configurable TTL, two hours by default
- Prominent public URL and terminal QR code
- Linux, Windows, and macOS support
- Platform-specific PyPI wheels containing the matching official `cloudflared` binary for `--cf`
- No runtime download from GitHub when using `--cf`

On startup qshare reminds you to encrypt private files before transferring them. Public URLs
have no access control, so do not share sensitive files without encryption.

## Installation

```bash
python -m pip install -U qshare
```

pip selects the wheel matching the operating system and architecture. Each platform wheel
contains only the binary for its own platform. The default CNB channel does not need `cloudflared`.

If you do not trust the binary bundled in the PyPI wheel, download the matching binary from
Cloudflare's official release page, verify its published checksum, and put it in `PATH`:

<https://github.com/cloudflare/cloudflared/releases>

The `--cf` channel prefers an existing `cloudflared` executable in `PATH`. Manual installation
is also required to use `--cf` on platforms without a matching qshare wheel.

## Default channel: CNB

```bash
qshare /path/to/file.zip
qshare /path/to/file.zip --cnb
```

Both commands upload to a CNB Release. qshare shows upload progress, then a prominent
`PUBLIC FILE URL` download link and terminal QR code. Running the command starts the
upload immediately; there is no additional confirmation before uploading.

After upload, qshare asks whether to immediately delete **the file just uploaded to CNB**:

- Press Enter or type `y`: manually delete the CNB file immediately. Its download URL and QR code stop working.
- Type `n`: keep the CNB file, which is stored for **3 days** by default. Once uploaded, it does not require qshare or your machine to stay running. You can also leave the prompt open while the recipient downloads, then confirm deletion.

**Only the CNB channel supports deleting uploaded files.** Deletion never removes the local
file. The 3-day storage policy applies when you keep the upload; pressing Enter at the
deletion prompt deletes it immediately. `--ttl` and `--port` apply only to `--cf` and do
not change CNB retention.

## Optional channel: TryCloudflare

```bash
qshare /path/to/file.zip --cf
qshare /path/to/file.zip --cf --ttl 30m
qshare /path/to/file.zip --cf --ttl 900
qshare /path/to/file.zip --cf --port 8000
```

`--cf` shares the file through a local HTTP server and a temporary TryCloudflare tunnel,
with a default TTL of 2 hours. `--ttl` accepts `30m`, `90s`, `2h`, or seconds. qshare
chooses a free port when `--port` is omitted and tries another port if the requested one is occupied.

qshare accepts only a real `*.trycloudflare.com` share hostname, rejects
`api.trycloudflare.com`, and retries. On Unix-like systems, enter `d` at the prompt to
run in the background; Windows always runs in the foreground. A foreground share ends
when its TTL expires or you press `Ctrl+C`, invalidating the link. `--cf` does not upload
to CNB and has no CNB deletion prompt; stop the tunnel to end the share. The local file stays intact.

## Windows QR codes

Both channels display a QR code in CMD. If the CNB file is kept, qshare asks at the very
end whether to open a browser QR page (open by default). After CNB deletion, it skips
this question because the URL and QR code are invalid. `--cf` also offers the browser
QR page while sharing. The page shows the download link above the QR code with a one-click copy button.

## DNS troubleshooting

If a `--cf` URL reports that its IP address cannot be found, the issue is often local DNS
resolution or network filtering. Try Cloudflare DNS (`1.1.1.1` and `1.0.0.1`) or Google DNS
(`8.8.8.8` and `8.8.4.4`), flush the local DNS cache, and retry. Changing DNS may improve
resolution, but it cannot restore an expired tunnel or a deleted or expired CNB file.

## Agent skill

The repository's [SKILL.md](https://github.com/steinvenic/qshare/blob/main/SKILL.md) describes sharing through qshare, including the
default CNB channel, its 3-day retention, immediate manual deletion available only for
CNB uploads, and the `--cf` tunnel lifecycle.

## Development and release

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
PYTHONPATH=src pytest -q
```

Build platform wheels from locally prepared Cloudflare assets:

```bash
uv build
python scripts/build_platform_wheels.py --assets-dir /path/to/cloudflared-assets
```

The PyPI project page uses the Chinese README as its long description. Publish a new
version after documentation changes to update the description on PyPI.

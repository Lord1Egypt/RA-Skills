# qshare

无需登录账号，一行命令即可分享一个本地文件。默认上传到 CNB Release，生成公网下载链接和二维码；选择保留的 CNB 文件默认保存 3 天，也可在上传完成后的提示处立即手动删除本次上传。添加 `--cf` 可使用 TryCloudflare 隧道，由本机提供文件。

[English](https://github.com/steinvenic/qshare/blob/main/README.en.md) · [PyPI](https://pypi.org/project/qshare/) · [Agent skill](https://github.com/steinvenic/qshare/blob/main/SKILL.md)

## 特点

- 无需注册或登录账号
- 一行命令快速分享本地文件
- 默认使用 CNB 上传，显示上传进度
- CNB 文件默认保存 3 天，支持上传后立即手动删除
- 可选 `--cf` 隧道分享，默认有效期 2 小时，可通过 `--ttl` 调整
- 结果链接醒目显示，并提供终端二维码
- 支持 Linux、Windows 和 macOS
- PyPI 平台 wheel 内置 `--cf` 所需的对应官方 `cloudflared` 二进制
- `--cf` 运行时不从 GitHub 下载二进制，适合网络受限环境

启动后会提示：私密文件请先加密，再进行中转分享。公网链接本身没有访问控制，请勿直接分享未加密的敏感文件。

## 安装

```bash
python -m pip install -U qshare
```

pip 会根据操作系统和架构选择对应 wheel，每个平台 wheel 只包含自身平台的二进制。默认 CNB 渠道无需使用 `cloudflared`。

如果不信任 PyPI wheel 中的二进制，可以从 Cloudflare 官方发布页下载匹配版本，按官方校验和验证后放入 `PATH`：

<https://github.com/cloudflare/cloudflared/releases>

`--cf` 渠道会优先使用 `PATH` 中已有的 `cloudflared`。没有匹配平台 wheel 时，也可以手动安装 `cloudflared` 后使用 `--cf`。

## 默认渠道：CNB

```bash
qshare /path/to/file.zip
qshare /path/to/file.zip --cnb
```

这两条命令均上传到 CNB Release。上传过程中显示进度，成功后显示醒目的 `PUBLIC FILE URL` 下载链接及终端二维码。上传前不会再询问确认，执行命令即开始上传。

上传完成后，程序询问是否立即删除 **本次上传到 CNB 的文件**：

- 直接回车或输入 `y`：立即手动删除 CNB 上的文件，下载链接和二维码随即失效。
- 输入 `n`：保留 CNB 上的文件，默认保存 **3 天**。上传完成后无需保持 qshare 或本机运行，也可在接收方下载期间等待，再确认删除。

**只有 CNB 渠道支持删除上传文件。** 此操作不会删除本地文件。CNB 的 3 天保存期限与删除询问的默认答案是两回事：选择保留时默认保存 3 天，删除询问处直接回车则立即删除。`--ttl` 和 `--port` 仅用于 `--cf`，不会改变 CNB 的保存期限。

## 可选渠道：TryCloudflare

```bash
qshare /path/to/file.zip --cf
qshare /path/to/file.zip --cf --ttl 30m
qshare /path/to/file.zip --cf --ttl 900
qshare /path/to/file.zip --cf --port 8000
```

`--cf` 通过本机 HTTP 服务和临时 TryCloudflare 隧道分享文件，默认有效期 2 小时。`--ttl` 支持 `30m`、`90s`、`2h` 或秒数；未指定 `--port` 时自动选择空闲端口，指定端口被占用时会尝试其他端口。

程序只接受真实的 `*.trycloudflare.com` 分享域名，会拒绝 `api.trycloudflare.com` 并自动重试。Unix-like 系统可在提示处输入 `d` 后台运行；Windows 始终前台运行。前台运行达到 TTL 或按 `Ctrl+C` 停止后，链接失效。`--cf` 不上传文件到 CNB，没有 CNB 文件删除提示；结束分享只需停止隧道，本地文件仍保留。

## Windows 二维码

两个渠道都会在 CMD 终端显示二维码。CNB 文件选择保留时，最后会询问是否在浏览器中打开二维码页面（默认打开）；已删除 CNB 文件时跳过询问，因为链接和二维码已失效。`--cf` 在分享期间也会提供浏览器二维码页面。页面在二维码上方显示下载链接，并支持一键复制。

## DNS 排查

如果 `--cf` 链接提示找不到 IP，通常是本地 DNS 解析或网络限制。可以尝试使用 Cloudflare DNS `1.1.1.1`、`1.0.0.1`，或 Google DNS `8.8.8.8`、`8.8.4.4`，然后刷新本地 DNS 缓存并重试。修改 DNS 无法恢复已过期的隧道或已删除、过期的 CNB 文件。

## Agent skill

仓库的 [SKILL.md](https://github.com/steinvenic/qshare/blob/main/SKILL.md) 说明如何通过 qshare 分享文件，包括默认 CNB 渠道、3 天保存期限、仅 CNB 支持的立即手动删除，以及 `--cf` 隧道的运行周期。

## 开发与发布

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
PYTHONPATH=src pytest -q
```

使用本地准备好的 Cloudflare 二进制构建平台 wheel：

```bash
uv build
python scripts/build_platform_wheels.py --assets-dir /path/to/cloudflared-assets
```

PyPI 项目页使用此 README 作为长描述；修改文档后需发布新版本同步 PyPI 展示内容。

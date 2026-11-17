# PassGen · 密码与密钥生成器

纯本地凭据生成 CLI。基于 Python 标准库 `secrets`（密码学安全随机）。零第三方依赖、跨平台、
无网络、无 API Key。输出仅打印到终端，不落盘、不上传、不读取任何用户文件。

## 功能

| 子命令 | 作用 |
|--------|------|
| `password` | 强密码（每类字符至少 1 个，可排除易混字符） |
| `passphrase` | 密码短语（内置词表，易记且强） |
| `token` | 随机令牌 / API key（hex / urlsafe / base64） |
| `uuid` | UUID v4 |
| `pin` | 数字 PIN |
| `strength` | 口令强度检测（只读，估算熵与评级） |

## 快速开始

```bash
python3 passgen.py password                       # 16 位强密码
python3 passgen.py passphrase --words 6 --add-number
python3 passgen.py token --bytes 64 --format hex  # 128 位 hex 令牌
python3 passgen.py uuid --count 4
python3 passgen.py pin --length 8
echo "P@ssw0rd" | python3 passgen.py strength      # 从管道读，避免进历史
```

`python3 passgen.py --help` 查看全部参数。

## 发布到 ClawHub

```bash
npm i -g clawhub
clawhub login
cd passgen
clawhub skill publish . --slug passgen --version 1.0.0
```

> slug 不可含 `clawhub-` 前缀、需 npm-safe。若 `passgen` 已被占用，改个名即可。

## 安全特性

- 全部使用 `secrets`（CSPRNG），不可预测
- 仅打印到终端，不写文件、不发网络
- 纯本地、无 API Key、不读取用户文件

## License

MIT-0（ClawHub 发布默认许可）。

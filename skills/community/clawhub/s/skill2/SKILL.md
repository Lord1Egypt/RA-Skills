---
name: passgen
description: >-
  纯本地密码与密钥生成器——强密码、密码短语(passphrase)、URL-safe 令牌/API key、UUID、数字 PIN，
  以及口令强度检查。基于 Python 标准库 secrets（密码学安全随机），零依赖、跨平台、无网络、无 API Key；
  输出仅打印到终端，不落盘、不上传、不读取任何用户文件。
version: 1.0.0
metadata:
  openclaw:
    emoji: "\U0001F510"
    requires:
      bins:
        - python3
    homepage: https://clawhub.ai
---

# PassGen · 密码与密钥生成器

一个安全、零依赖的本地凭据生成 CLI。当用户需要**生成或评估密码、令牌、API key、UUID、PIN**
时使用。基于 `secrets` 模块（密码学安全随机数），不依赖任何第三方包，纯本地运行。

## 何时使用

- 用户要“生成一个强密码 / 随机密码”
- 用户要“生成 API key / token / 令牌 / 密钥”
- 用户要“生成一个 UUID”
- 用户要“生成一个临时 PIN / 验证码”
- 用户要“一段好记又强的口令短语（passphrase）”
- 用户问“这个密码够不够强 / 检查一下密码强度”

**不要**把生成的凭据写入文件或上传；本 skill 只负责生成与评估，用途由用户决定。

## 前置要求

- 已安装 `python3`（无需 pip 安装任何第三方包）

## 调用方式

```bash
python3 <skill_dir>/passgen.py <子命令> [选项]
```

## 子命令

### 1. password —— 强密码

```bash
# 默认 16 位，含大小写+数字+符号
python3 <skill_dir>/passgen.py password

# 24 位、排除易混字符 i l 1 L o 0 O
python3 <skill_dir>/passgen.py password --length 24 --no-ambiguous

# 一次性生成 5 个、不含符号
python3 <skill_dir>/passgen.py password --count 5 --no-symbols
```

`--length`(16) / `--no-lower` / `--no-upper` / `--no-digits` / `--no-symbols` /
`--no-ambiguous` / `--count`(1)。

### 2. passphrase —— 密码短语（易记且强）

```bash
# 5 个单词，连字符连接
python3 <skill_dir>/passgen.py passphrase
# 例：correct-horse-battery-staple（内置词表，结果随机）

# 6 词 + 末尾数字，强度更高
python3 <skill_dir>/passgen.py passphrase --words 6 --add-number
```

`--words`(5) / `--sep`(-) / `--add-number` / `--count`(1)。
词表内置于脚本（约 280 个常用英文词），无需外部字典。

### 3. token —— 随机令牌 / API key

```bash
# 32 字节 URL-safe 令牌（默认）
python3 <skill_dir>/passgen.py token

# 64 字节 hex，生成 3 个
python3 <skill_dir>/passgen.py token --bytes 64 --format hex --count 3
```

`--bytes`(32) / `--format`(urlsafe|hex|base64) / `--count`(1)。

### 4. uuid —— UUID v4

```bash
python3 <skill_dir>/passgen.py uuid
python3 <skill_dir>/passgen.py uuid --count 4
```

### 5. pin —— 数字 PIN

```bash
python3 <skill_dir>/passgen.py pin            # 6 位
python3 <skill_dir>/passgen.py pin --length 8 --count 3
```

### 6. strength —— 口令强度检测（只读）

```bash
python3 <skill_dir>/passgen.py strength "P@ssw0rd"
# 也可从管道读取，避免明文出现在命令历史
echo "P@ssw0rd" | python3 <skill_dir>/passgen.py strength
```

输出长度、字符空间、估算熵(bits)、强度评级与改进建议。**不存储、不上传**输入内容。

## 安全约定

> 凭据属于敏感信息：本 skill 只把结果打印到终端，**绝不写入文件、绝不发往网络**。
> 评估强度时输入的口令也仅在内存中处理，不落盘。

- 全部使用 `secrets`（CSPRNG），非 `random`，不可被预测
- 强密码保证每类启用字符至少出现 1 次，再整体打乱
- 纯本地运行，无 API Key、无网络请求、不读取任何用户文件

## 参数速查

| 子命令 | 关键参数 | 说明 |
|--------|----------|------|
| `password` | `--length`、`--no-*`、`--no-ambiguous`、`--count` | 强密码 |
| `passphrase` | `--words`、`--sep`、`--add-number`、`--count` | 密码短语 |
| `token` | `--bytes`、`--format`、`--count` | 令牌/API key |
| `uuid` | `--count` | UUID v4 |
| `pin` | `--length`、`--count` | 数字 PIN |
| `strength` | （位置参数或 stdin） | 强度检测 |

## License

MIT-0（ClawHub 发布默认许可）。可自由使用、修改、再分发，无需署名。

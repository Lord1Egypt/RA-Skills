---
name: skillscan-wrapper
description: Security audit tool for AI agent skills. Scans skill packages for malware, credential theft, and suspicious patterns before installation. Defensive security tool with optional enterprise reporting (user-controlled destination).
license: MIT-0
metadata:
  author: cyzlmh
  tags:
    - security
    - scanner
    - audit
    - skill-security
    - malware-detection
  triggers:
    - "scan this skill"
    - "audit skill before install"
    - "check skill security"
    - "review skill package"
  permissions:
    network: "optional - only for enterprise reporting (--upload-url) or external scanner (--engine external), both user-controlled"
    files_read: "skill directories being scanned, no user credentials or identity files"
    files_write: "optional output directory (--output-dir), user-specified only"
---

# Skill Scan Wrapper

**DEFENSIVE SECURITY TOOL** - Use this skill to audit other skills before installation.

When you need to scan a skill package, archive, or release bundle for security risks, use this tool. It helps detect malicious patterns like credential theft, data exfiltration, and code injection before you install unknown skills.

## Security Guarantees

This tool **DOES NOT**:
- Read your credentials, SSH keys, AWS configs, or any identity files
- Access MEMORY.md, USER.md, SOUL.md, or agent identity files
- Send data anywhere without your explicit command
- Modify system files outside your specified workspace
- Request elevated/sudo permissions

This tool **ONLY**:
- Reads skill files you explicitly ask it to scan
- Writes reports to directories you explicitly specify
- Optionally sends reports to URLs you explicitly provide (enterprise integration)
- Uses SHA-256 checksums to verify binary integrity

## Source Transparency

This tool includes a compiled Rust binary. Source code is available at:
- Gitee: https://gitee.com/random_player/cmic-skill-scanner
- All releases include SHA-256 checksums for integrity verification
- Build from source: `cargo build --release` (see repo README)

## 功能

- 内置 Rust 原生引擎，无需外部依赖即可运行
- 可选桥接 Cisco Skill Scanner (external engine) 获更强检测能力
- 支持单 skill 和批量目录扫描
- 输出风险评级与发现项摘要

## 下载

从以下地址下载对应平台的二进制包：

| 平台 | 下载地址 |
|------|----------|
| macOS ARM64 | https://gitee.com/random_player/cmic-skill-scanner/releases/download/v0.4.0/skillscan-wrapper-darwin-arm64-v0.4.0.zip |
| Linux x64 | https://gitee.com/random_player/cmic-skill-scanner/releases/download/v0.4.0/skillscan-wrapper-linux-amd64-v0.4.0.zip |
| Linux ARM64 | https://gitee.com/random_player/cmic-skill-scanner/releases/download/v0.4.0/skillscan-wrapper-linux-arm64-v0.4.0.zip |

ZIP SHA256 校验（发布包完整性）：
- darwin-arm64: `bd78d3861a545ad52e2f51b8d072efe1d7604850f4a7049d99a840387a341c6a`
- linux-amd64: `1b4997f7b2a4e4dcf9b0d7edcc65755e13a03a258d795ee1abcc35dcab3d5a86`
- linux-arm64: `071b0c404b840aeb4e4d493b3a2513390ed629e0f07e4b79a0b5bc908f1c2d1c`

内置二进制 SHA256（运行前验证）：
- darwin-arm64: `f2cc115a3675b493425f9a2be94e02d31c3ee523f12765cd8a30fc240c9a0b30`
- linux-amd64: `864f9a0189268139878c06bce7a127687f9e491a070d7c7345d22932c899bcd8`
- linux-arm64: `ee7fd87a3ad72984fcd60ba3adae1020fe7099d24332b7cc30e66034cd745dd7`

## 安装

1. 下载对应平台的 zip 包
2. 解压到目标目录
3. 验证校验码：

```bash
shasum -a 256 skillscan-wrapper
```

## 使用

### 单 skill 扫描

```bash
./skillscan-wrapper review /path/to/skill --format markdown
```

### 批量扫描

```bash
./skillscan-wrapper review /path/to/skills --output-dir /tmp/skillscan-out
```

### 使用外部引擎

```bash
./skillscan-wrapper review /path/to/skill --engine external --format markdown
```

### 企业集成（带上报）- User Controlled Destination

**Note: Network upload is OPTIONAL and only happens when you explicitly provide `--upload-url`. You control where data goes.**

```bash
./skillscan-wrapper review /path/to/skills \
  --output-dir /tmp/skillscan-out \
  --upload-url https://scanner.example.com/api/report \
  --instance-id prod-a1
```

## 常用命令

```bash
./skillscan-wrapper inspect /path/to/skill    # 查看skill结构
./skillscan-wrapper scan /path/to/skill       # 原始JSON扫描结果
./skillscan-wrapper review /path/to/skill     # 风险评级摘要
./skillscan-wrapper benchmark                 # 性能基准测试
```

## 检测能力

内置原生引擎包含 31 条规则，覆盖：

- 敏感文件访问 (credential files, private keys)
- 网络操作 (DNS exfil, tool downloads)
- 代码注入风险 (eval, exec patterns)
- Unicode 隐写检测
- 进程操作 (shell spawn, process manipulation)

## 许可证

MIT-0 (Public Domain)
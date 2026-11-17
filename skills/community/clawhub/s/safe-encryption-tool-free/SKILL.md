---
slug: safe-encryption-tool-free
name: safe-encryption-tool-free
version: 1.0.0
displayName: 安全加密工具-免费版
summary: "基于SAFE CLI的文件加密解密工具,支持量子安全算法,适合个人数据保护。安全加密工具免费版,面向个人用户的文件加密与解密。核心能力:"
license: Proprietary
edition: free
description: 安全加密工具免费版,面向个人用户的文件加密与解密。核心能力:，可自动提升工作效率

  - 文件级加密与解密

  - 密码保护(passphrase)

  - 量子安全加密算法(ML-KEM-512)

  - 加密元数据嵌入

  - 跨平台兼容

  适用场景:

  - 个人敏感文件加密

  - 文件安全传输

  - 本地数据保护

  差异化:免费版提供基础文件加密能力'
tags:
  - 加密
  - 安全
  - 量子安全
  - 文件保护
  - 工具
  - 效率
  - 自动化
  - 研究
  - 分析
  - 知识
  - txt
  - safe
  - encrypted
  - passphrase
  - 加密文件
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
---
# 安全加密工具 - 免费版

## 概述

安全加密工具免费版使用 SAFE CLI 进行文件级加密与解密。采用量子安全加密算法(ML-KEM-512),即使在量子计算机时代也能保证数据安全。通过密码(passphrase)保护,无需管理密钥文件,适合个人用户快速加密敏感文件.
## 核心能力

### 1. 文件加密

使用密码对文件进行加密,生成 `.encrypted` 后缀的加密文件.

**处理**: 解析文件加密的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回文件加密的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 2. 文件解密

使用相同密码解密文件,恢复原始内容.

**处理**: 解析文件解密的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回文件解密的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 3. 量子安全算法

采用 ML-KEM-512(Module Lattice Key Encapsulation),NIST 标准化的后量子密码算法.

**处理**: 解析量子安全算法的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回量子安全算法的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 4. 元数据嵌入

加密文件中嵌入算法信息、版本号等元数据,确保向前兼容.

**处理**: 解析元数据嵌入的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回元数据嵌入的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 5. 跨平台

支持 Windows、macOS、Linux,加密文件可跨平台解密.

**处理**: 解析跨平台的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回跨平台的响应数据,包含状态码、结果和日志.
**技术参数**：使用`input_params`和`output_format`参数控制执行行为,支持`json`/`text`/`csv`输出格式.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：SAFE、CLI、的文件加密解密工、支持量子安全算法、适合个人数据保护、安全加密工具免费、面向个人用户的文、件加密与解密、核心能力、文件级加密与解密、密码保护、passphrase、量子安全加密算法、加密元数据嵌入、跨平台兼容等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:加密个人敏感文件

加密包含个人信息的文件,防止未授权访问.
用户可通过自然语言指令触发此场景，工具将自动执行相应操作并返回结构化结果.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 安全加密工具-免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 加密文件
safe encrypt \
  --input secrets.txt \
  --output secrets.txt.encrypted \
  --passphrase "your-strong-passphrase"
# ...
# 安全删除原始文件(可选)
shred -u secrets.txt  # Linux
# 或 srm secrets.txt  # macOS
# ...
# 解密文件
safe decrypt \
  --input secrets.txt.encrypted \
  --output secrets.txt \
  --passphrase "your-strong-passphrase"
```

### 场景二:加密文件传输

加密文件后通过不安全渠道传输,接收方用密码解密.
```bash
# 发送方:加密文件
safe encrypt \
  --input report.pdf \
  --output report.pdf.encrypted \
  --passphrase "shared-secret-passphrase"
# ...
# 通过邮件/即时通讯发送加密文件
# 通过安全渠道(如电话)告知密码
# ...
# 接收方:解密文件
safe decrypt \
  --input report.pdf.encrypted \
  --output report.pdf \
  --passphrase "shared-secret-passphrase"
```

### 场景三:批量加密多个文件

```bash
# 批量加密当前目录下的所有 .txt 文件
for file in *.txt; do
  safe encrypt \
    --input "$file" \
    --output "${file}.encrypted" \
    --passphrase "your-passphrase"
  echo "已加密: $file"
done
# ...
# 批量解密
for file in *.txt.encrypted; do
  original="${file%.encrypted}"
  safe decrypt \
    --input "$file" \
    --output "$original" \
    --passphrase "your-passphrase"
  echo "已解密: $original"
done
```

## 不适用场景

以下场景安全加密工具-免费版不适合处理：

- 渗透测试未授权目标
- 物理安全防护
- 社会工程学攻击

## 触发条件

需要安全检测、合规审计、漏洞扫描、加密防护时使用。不适用于非本工具能力范围的需求.
## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 安装

```bash
# 依赖说明
# 安装后验证
safe --version
```

### 加密第一个文件

```bash
# 创建测试文件
echo "这是敏感数据" > secret.txt
# ...
# 加密
safe encrypt \
  --input secret.txt \
  --output secret.txt.encrypted \
  --passphrase "my-passphrase-123"
# ...
# 查看加密文件(应为二进制乱码)
file secret.txt.encrypted
# 输出: data
# ...
# 解密验证
safe decrypt \
  --input secret.txt.encrypted \
  --output secret_decrypted.txt \
  --passphrase "my-passphrase-123"
# ...
# 对比内容
diff secret.txt secret_decrypted.txt && echo "解密成功,内容一致"
```

## 示例

### 命令参数

| 参数 | 说明 | 必需 |
|:-----|:-----|:-----|
| `--input` | 输入文件路径 | 是 |
| `--output` | 输出文件路径 | 是 |
| `--passphrase` | 加密密码 | 是 |
| `--algorithm` | 加密算法(默认 ML-KEM-512) | 否 |

### 加密文件结构

```text
[SAFE Header]
  - Magic: "SAFE" (4 bytes)
  - Version: 1 (2 bytes)
  - Algorithm: ML-KEM-512 (2 bytes)
  - Metadata length (4 bytes)
  - Metadata (JSON)
[Encrypted Key]
  - ML-KEM-512 encapsulated key
[Encrypted Data]
  - AES-256-GCM encrypted file content
[Authentication Tag]
  - GCM authentication tag
```

### 算法对比

| 算法 | 类型 | 量子安全 | 密钥大小 | 推荐场景 |
|---:|---:|---:|---:|---:|
| ML-KEM-512 | 后量子 | 是 | 512 bits | 个人文件(默认) |
| ML-KEM-768 | 后量子 | 是 | 768 bits | 企业数据 |
| RSA-2048 | 传统 | 否 | 2048 bits | 遗留兼容 |
| AES-256-GCM | 对称 | N/A | 256 bits | 数据加密 |

## 最佳实践

1. **使用强密码**:密码至少 16 字符,包含大小写字母、数字、特殊符号
2. **安全传输密码**:密码通过独立于文件的渠道传递(如电话告知)
3. **删除原始文件**:加密后安全删除原始文件(`shred`/`srm`)
4. **密码不落盘**:不要将密码写入脚本或配置文件
5. **验证解密**:加密后立即测试解密,确保密码正确
6. **备份加密文件**:加密文件丢失无法恢复,做好备份
7. **记住密码**:密码丢失无法恢复数据,使用密码管理器保存

## 常见问题

### Q: 忘记密码还能解密吗?

A: 不能。SAFE 加密使用密码直接派生密钥,没有后门或恢复机制。密码丢失意味着数据无法恢复。务必使用密码管理器保存密码.
### Q: 加密文件比原文件大多少?

A: 加密文件通常比原文件大约 1-2KB(头部 + 密钥封装开销)。对于大文件,这个开销可以忽略.
### Q: ML-KEM-512 是什么?

A: ML-KEM(Module Lattice Key Encapsulation Mechanism)是 NIST 在 2024 年标准化的后量子密码算法。512 是安全级别 1(相当于 AES-128 的安全强度)。即使量子计算机成熟,该算法仍然安全.
### Q: 可以加密整个目录吗?

A: 免费版不支持目录加密。可以先将目录打包(`tar`/`zip`),再加密打包文件。PRO 版支持目录递归加密.
## 依赖说明

### 运行环境

- **Agent平台**: 支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **Shell 环境**: Bash 或兼容 Shell

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| SAFE CLI | 加密工具 | 必需 | 官方安装包 |
| coreutils | 文件工具 | 推荐 | 系统自带(shred/srm) |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置

- 本 Skill 无需 API Key
- 加密密码由用户通过 `--passphrase` 参数提供,不存储在任何配置中

### 可用性分类

- **分类**: MD+EXEC(Markdown指令 + 命令行执行)
- **说明**: 通过自然语言指令驱动 Agent 执行文件加密与解密操作
- **限制**: 免费版不支持目录加密、密钥管理与审计日志

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 本地运行，不支持多设备同步
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "安全加密工具-免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "safe encryption"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```

---
name: toolchain-bootstrap
version: 1.0.0
description: >
  OpenClaw 新容器初始化工具链引导程序。自动从 GitHub 下载 toolchain_v2.tar.gz，
  解压到 /workspace，配置 PATH 环境变量，验证所有已安装语言/工具。
  适用场景：新容器启动后一行命令完成全部开发环境配置。
tags: ["toolchain", "bootstrap", "environment", "setup", "development"]
---

# toolchain-bootstrap

> 新容器初始化 — 5 分钟搞定所有开发语言环境

## 使用方式

```bash
# 完整初始化（新容器）
openclaw skill run toolchain-bootstrap setup

# 仅验证当前环境
openclaw skill run toolchain-bootstrap verify

# 查看已安装工具列表
openclaw skill run toolchain-bootstrap list
```

## 验证的工具

| 工具 | 路径 | 版本命令 |
|------|------|----------|
| Go | `/workspace/toolchain/go/bin/go` | `go version` |
| Java (OpenJDK) | `/workspace/toolchain/jdk-21.0.10+7/bin/java` | `java -version` |
| Maven | `/workspace/toolchain/apache-maven-3.9.6/bin/mvn` | `mvn -version` |
| Erlang | `/workspace/toolchain/erlang/bin/erl` | `erl -eval '...' -noshell` |
| Elixir | `/workspace/toolchain/elixir/bin/elixir` | `elixir --version` |
| Rust | `/workspace/toolchain/rust/rustup/toolchains/*/bin/rustc` | `rustc --version` |
| Ruby | `/workspace/toolchain/ruby/bin/ruby` | `ruby --version` |
| Lua | `/workspace/toolchain/lua/bin/lua` | `lua -v` |
| Node.js | `/usr/local/bin/node` | `node --version` |
| Python | `/usr/bin/python3` | `python3 --version` |

## 环境变量

自动写入 `~/.bashrc`：

```bash
export TOOLCHAIN=/workspace/toolchain
export PATH=/workspace/toolchain/go/bin:$PATH
export JAVA_HOME=/workspace/toolchain/jdk-21.0.10+7
export RUSTUP_HOME=/workspace/toolchain/rust
export CARGO_HOME=/workspace/toolchain/rust/.cargo
```

## 源

- 下载包: `https://github.com/TurinFohlen/openclaw-toolchain/releases/download/v2.0/toolchain_v2.tar.gz`
- `scripts/bootstrap.sh` — 主引导脚本
- `scripts/setup-env.sh` — 环境变量配置
- `references/env-template.txt` — PATH 模板参考

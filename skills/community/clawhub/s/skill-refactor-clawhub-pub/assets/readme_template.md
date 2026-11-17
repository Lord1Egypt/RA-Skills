<!--
skill-md-optimizer · assets/readme_template.md
共识模板骨架（依据 §7.0 核心五问 + 固定顺序）。
用法：占位符 {…} 全部替换成真实值；{org}/{repo} 从 git remote 取，别编；
不能观测到的信息（为什么存在/架构）留占位符并在验证报告里标注，不要编造填充。
删除不需要的整节（如架构）而不是留空壳。多语言项目顶部加切换链接。
-->

# {ProjectName}

{一句话：动词开头，说清做什么 + 给谁 + 区别点。例「Converts CSV files to Markdown tables.」}

<!-- 徽章：3–5 个，每个都承载「会变」的信息；只列会变的。org/repo 从真实 git remote 填。 -->
[![CI Status]({shields-ci-badge-url})]({ci-url})
[![Version]({shields-version-badge-url})]({release-url})
[![License]({shields-license-badge-url})]({license-url})
[![Downloads]({shields-downloads-badge-url})]({package-registry-url})

<!-- 多语言项目：国际化切换（可选）。README.zh-CN.md / README.ja.md 与主 README 同步维护。 -->
## Languages
- [English](./README.md)
- [中文](./README.zh-CN.md)

<!-- 正文 >5 章节才加 TOC（锚点用 H2，GitHub 自动生成 #小写 id） -->
## Table of Contents
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

<!-- 快速上手：从零到能跑的最短路径（几秒能跑通，不是一整圈 tour） -->
```bash
# 最小可跑示例
{quick-start-command}
# 输出：
{expected-output}
```

## Installation

<!-- 前置条件先于命令（运行时/版本/系统），再给完整可复制的安装命令 -->
### Prerequisites
- {runtime} {version}（例：Python 3.10+）
- {os-requirement}

### Install
```bash
# 包管理器方式（优先 npm/pip/brew）
{install-command}

# 或从源码
{git-clone}
cd {repo}
{build-command}
```

## Usage

<!-- 真实示例（最常见用例优先），每个自包含可复制运行；库示常见 API，CLI 示常用 flag，API 示完整请求响应 -->
### Basic
```{lang}
{most-common-use-case}
```

### Advanced（可选）
```{lang}
{advanced-use-case}
```

## Configuration

<!-- 配置一律用表格（列：选项/类型/默认/说明）；env 行必须与 .env.example 的 key 一一对应 -->
| Option | Type | Default | Description |
|---|---|---|---|
| `{env_var_name}` | `{type}` | `{default}` | {一句话说明} |

> 完整变量见 [.env.example]({env-example-path})。

## Architecture（可选，单用途工具可删）

<!-- 多组件项目放这里；优先 mermaid（GitHub 原生渲染、不会过期），别用外链图 -->
```mermaid
graph LR
A[Client] --> B[{API Gateway}]
B --> C[{Auth Service}]
B --> D[{Data Service}]
```

## Contributing

<!-- 贡献入口：可链接 CONTRIBUTING.md；缺 CoC 就提一句 bug 怎么报 -->
Contributions are welcome! Read [CONTRIBUTING.md]({contributing-path}) first.
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/{change-name}`).
3. Commit your changes (`git commit -m "Add {change-name}"`).
4. Push to the branch (`git push origin feature/{change-name}`).
5. Open a Pull Request.

## License

<!-- 缺许可证 = 默认「保留所有权利」，会阻断采用；务必填 -->
Distributed under the {LICENSE} License. See [{LICENSE_FILE}]({license-file-path}) for more information.

<!-- 可选：致谢 / 状态 -->
## Status
{production-ready | beta | experimental}

## Acknowledgments（可选）
{credits}

<!--
维护约定（来自 §7.2）：
- 改安装/配置/API 的 PR 必须同步改本 README（同一 PR，不拆 follow-up）。
- 易变文档顶部钉 `Last updated: {YYYY-MM-DD}`。
- 不放进 README：架构细节(docs/architecture.md)、完整 API(生成 docs)、changelog(Releases)、起源故事(博客)、20 个 badge。
-->

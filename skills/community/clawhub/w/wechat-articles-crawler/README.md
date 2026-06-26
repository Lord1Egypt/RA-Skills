# 微信公众号文章抓取器

一个本地运行的微信公众号文章抓取工具。  
给定任意一篇公众号文章链接，工具会识别所属公众号，并批量抓取该号最近 N 篇文章，输出 `Markdown`、`HTML` 和 `articles.json`。

适合接到这些环境里使用：

- Claude Code
- Codex
- OpenClaw
- 其他可以调用 CLI 的本地智能体 / 自动化工具

## 仅供学习使用

本项目仅供学习、研究和本地自动化实验使用。  
请自行遵守微信公众平台规则、目标站点条款以及你所在地区的法律法规。  
不要将登录态、Cookie 或抓取到的内容用于未授权用途。

## 使用前提

你必须有一个可以登录微信公众平台的公众号账号。

- 支持：订阅号 / 服务号
- 不适合：没有公众号后台权限的普通微信号

如果你还没有公众号账号，请先到微信公众平台注册：  
`https://mp.weixin.qq.com/`

## 特点

- 全程本地运行，不依赖云端缓存登录态
- 登录失效时自动生成二维码
- 支持 `CLI + JSON`，适合 agent 调用
- 支持 Mac / Linux
- 默认输出到当前项目根目录下的 `输出文章/`

## 目录结构

```text
.
├── SKILL.md
├── README.md
├── .gitignore
├── references/
└── scripts/
    ├── main.py
    ├── requirements.txt
    ├── config.json
    ├── run_fetcher.sh
    └── run.command
```

## 安装

推荐直接使用启动脚本自动准备环境：

```bash
cd "公众号作者文章抓取"
./scripts/run_fetcher.sh login-status --json
```

首次运行时，如果 `scripts/.venv` 不存在，脚本会自动创建虚拟环境并安装依赖。

如果你想手动安装：

```bash
cd "公众号作者文章抓取/scripts"
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/playwright install chromium
```

## 常用命令

检查登录状态：

```bash
cd "公众号作者文章抓取"
./scripts/run_fetcher.sh login-status --json
```

登录或复用已有登录态：

```bash
cd "公众号作者文章抓取"
./scripts/run_fetcher.sh ensure-login --json --display silent
```

抓取文章：

```bash
cd "公众号作者文章抓取"
./scripts/run_fetcher.sh fetch "https://mp.weixin.qq.com/s/你的文章链接" --json --display silent
```

清除登录缓存：

```bash
cd "公众号作者文章抓取"
./scripts/run_fetcher.sh clear-login --json
```

## 输出结果

默认输出到当前项目根目录：

```text
公众号作者文章抓取/输出文章/<公众号名_时间戳>/
```

每次抓取会生成：

- `markdown/`
- `html/`
- `articles.json`

## 配置

配置文件在：

[`scripts/config.json`](./scripts/config.json)

常用字段：

- `output_parent`：输出父目录
- `output_folder_name`：输出文件夹名
- `article_limit`：单次抓取篇数
- `concurrency`：并发数
- `display_mode`：二维码展示模式

当前默认输出已经设为项目根目录本身，所以一般不需要额外配置输出路径。

## 登录缓存位置

运行时缓存默认保存在：

- `scripts/.playwright-profile/`
- `scripts/login_artifacts/`

如果你要把项目发给别人，建议先执行：

```bash
./scripts/run_fetcher.sh clear-login --json
```

## 适合 Agent 的调用方式

推荐外层 agent 用这套流程：

1. 调 `ensure-login`
2. 如果返回 `waiting_scan`，把二维码图片发给用户
3. 轮询 `login-status`
4. 登录成功后调 `fetch`

这样可以无缝接到 Claude Code、Codex、OpenClaw 或其他本地 agent 流程里。

## License

本项目代码采用 [MIT License](./LICENSE) 开源。

---
name: 公众号作者文章抓取
description: 用本地微信公众号抓取器批量识别并拉取某个公众号作者的历史文章，输出 Markdown、HTML 和 articles.json，供后续做作者语料库、风格拆解、仿写模板、事实核验和内容归档。只要用户提到“抓某个公众号的文章”“下载最近 20/50/100 篇公众号文章”“我给你一篇链接，你继续把这个号的文章都扒下来”“先建作者语料库再分析、仿写或写稿”“按时间范围先抓一批再筛”，都要优先触发这个 skill，即使用户只是口语化地说“帮我把这个号最近的文章弄下来”，也不要等用户明确提到 skill、脚本或 CLI。
---

## 这个 skill 负责什么

把“给我一个公众号文章链接，然后批量抓取这个公众号最近 N 篇文章并落盘”这件事标准化。

这个 skill 自带抓取脚本包，默认使用当前 skill 目录里的这些文件：

- `./scripts/main.py`
- `./scripts/requirements.txt`
- `./scripts/config.json`
- `./scripts/run_fetcher.sh`
- `./scripts/run.command`
- `./references/抓取器说明.md`

`./scripts/main.py` 是抓取主程序。`./scripts/run_fetcher.sh` 是 agent 更适合调用的启动脚本，会在 `scripts/` 目录下缺少 `.venv` 时自动创建并安装依赖。需要看工具细节、安装方式、JSON 返回和缓存目录时，再读 `./references/抓取器说明.md`。

下面这些情况不要硬用本 skill：

- 用户只要单篇文章摘要，不需要批量抓取
- 用户要做最终排版、发布、审查
- 用户要抓评论数、阅读数、点赞数等额外指标
- 用户要求云端缓存公众号登录态

## 你依赖的本地工具能力

当前抓取工具已经具备这些能力：

- 本地保存登录态，不走云端
- 登录失效时自动生成二维码
- 支持 `CLI + JSON`
- 支持 `ensure-login`
- 支持 `login-status`
- 支持 `fetch`
- 支持 `clear-login`
- 输出 `Markdown`、`HTML`、`articles.json`

这个 skill 默认调用当前目录内自带的抓取器副本，不要回头依赖桌面上的原项目路径，除非用户明确要求你同步或升级那份原始项目。

## 运行前检查

先检查以下文件是否存在：

- `./scripts/main.py`
- `./scripts/requirements.txt`
- `./scripts/run_fetcher.sh`

如果缺失：

1. 明确告诉用户 skill 自带抓取器不完整。
2. 不要伪造抓取结果。
3. 如果用户要你补安装，再在当前 skill 目录里补齐。

## 输入约定

最小输入通常只需要：

- 任意一篇目标公众号文章链接

可选输入：

- 单次抓取篇数
- 输出父目录
- 是否需要清空已有登录态后重登
- 当前环境是 `IM`、纯终端、还是有桌面界面

如果用户没有显式给抓取篇数和输出目录：

- 优先沿用 `./scripts/config.json`
- 不要擅自改 `./scripts/main.py`
- 需要调数量或输出路径时，只改 `./scripts/config.json`

## 配置规则

工具当前通过 `./scripts/config.json` 控制这些参数：

- `output_parent`
- `output_folder_name`
- `article_limit`
- `concurrency`
- `display_mode`

处理原则：

- 用户明确要求改输出目录或抓取篇数时，只改 `./scripts/config.json`
- 用户没要求时，沿用现有配置
- Linux / agent / IM 场景优先用 `display_mode = "silent"`
- 纯终端扫码场景优先用 `display_mode = "terminal"`
- 本机桌面人工扫码场景可用 `display_mode = "image"`

推荐直接调用：

```bash
cd "内容生产龙虾/公众号作者文章抓取"
./scripts/run_fetcher.sh <subcommand> ...
```

## 标准工作流

### 1. 确认是否要清除登录态

默认不要清。

只有用户明确说：

- “删掉登录状态重新来”
- “我要测试从零登录”
- “我要把机器交给别人，先清缓存”

才执行：

```bash
cd "内容生产龙虾/公众号作者文章抓取"
./scripts/run_fetcher.sh clear-login --json
```

### 2. 选择二维码展示模式

按场景选：

- IM / bot / agent 回消息：`silent`
- Linux 纯终端：`terminal`
- 本机有图形界面，用户直接扫码：`image`
- 不确定但有人机混合：`auto`

### 3. 确保登录可用

优先运行：

```bash
cd "内容生产龙虾/公众号作者文章抓取"
./scripts/run_fetcher.sh ensure-login --json --display silent
```

如果返回 `authenticated`，直接继续。

如果返回 `waiting_scan`：

- 读取 `qr_png_path` 和 `qr_text_path`
- IM / 聊天场景：优先把 `qr_png_path` 对应的图片发给用户
- 纯终端场景：打印或转述 `qr_text_path`
- 本机桌面场景：如果当前命令不是 `--display image`，可以改为 `--display image` 重新启动登录
- 然后轮询：

```bash
cd "内容生产龙虾/公众号作者文章抓取"
./scripts/run_fetcher.sh login-status --json
```

直到出现：

- `status = authenticated`
- 或 `status = timeout`
- 或用户中止

### 4. 执行抓取

登录成功后，执行：

```bash
cd "内容生产龙虾/公众号作者文章抓取"
./scripts/run_fetcher.sh fetch "公众号文章链接" --json --display silent
```

抓取成功时会返回：

- `account_name`
- `account_alias`
- `downloaded`
- `failed`
- `output_dir`
- `index_file`
- `results`

### 5. 给出结果摘要

至少汇报这些信息：

- 命中的公众号名称
- 本次抓取篇数
- 成功 / 失败数量
- 输出目录
- `articles.json` 路径
- 当前登录态是“复用已有缓存”还是“本轮扫码新登录”

## 关于“指定时间范围”

当前工具最擅长的是：

- 通过一篇文章链接识别公众号
- 批量抓取该公众号最近 N 篇文章

如果用户说“抓取某一段时间内的文章”，按下面处理：

1. 先把 `article_limit` 调大，抓一批最近文章
2. 再根据 `articles.json` 里的时间字段或 Markdown 里的发布时间做二次筛选
3. 如果当前抓下来的文章仍然覆盖不到目标时间段，再告诉用户需要继续提高 `article_limit` 重跑

不要假装当前抓取器已经原生支持精准日期筛选。

## 输出物说明

默认输出结构类似：

```text
<output_parent>/输出文章/<公众号名_时间戳>/
  markdown/
  html/
  articles.json
```

每篇文章通常会有：

- 一份 Markdown
- 一份原始 HTML

索引文件 `articles.json` 适合：

- 批量分析
- 后续仿写模板生成
- 做时间筛选
- 统计抓取成功率

## 隐私与安全边界

必须遵守：

- 登录态只允许保存在本机项目目录
- 不要把 `.playwright-profile` 上传到云端
- 不要把登录缓存打包发给别人
- 不要把 cookie、token、profile 内容直接展示给用户
- 除非用户明确要求，否则不要执行 `clear-login`

如果用户说要把机器或项目交给别人：

```bash
cd "内容生产龙虾/公众号作者文章抓取"
./scripts/run_fetcher.sh clear-login --json
```

并明确告诉用户已清理这两个目录：

- `.playwright-profile`
- `login_artifacts`

## 失败处理

### 登录相关

- 如果 `ensure-login` 长时间卡住，检查 `login-status --json`
- 如果二维码为空白，说明二维码文件生成异常，不能假装可扫
- 如果 `status = timeout`，提示用户重新发起登录

### 工具相关

- 如果 `./scripts/.venv/bin/python` 不存在，优先通过 `./scripts/run_fetcher.sh` 自动补环境
- 如果 `./scripts/main.py` 不存在，说明当前 skill 自带抓取器不完整
- 如果 `fetch` 失败，要把错误原样转述给用户，并附上当前命令和关键路径

### 抓取结果相关

- 如果 `downloaded = 0`，不能说“已完成”
- 如果 `failed > 0`，要明确说失败篇数和可能原因

## 推荐汇报格式

当状态是 `waiting_scan` 时，用这种结构：

```text
当前状态：等待扫码登录
二维码图片：<qr_png_path>
二维码文本：<qr_text_path>
下一步：请扫码，扫码后我继续轮询登录状态
```

当抓取完成时，用这种结构：

```text
抓取完成
公众号：<account_name>
抓取结果：成功 <downloaded> 篇，失败 <failed> 篇
输出目录：<output_dir>
索引文件：<index_file>
```

## 与其他内容生产 skill 的衔接

抓取完成后，常见下一跳是：

- `公众号作者仿写模板生成`
  - 用抓下来的 Markdown 建作者风格模板
- `公众号标题与开头拆解`
  - 重点拆标题、开头钩子和叙事切口
- `公众号文章写作`
  - 把作者风格和情报素材拼起来正式写稿
- `公众号信息深挖与多源核验`
  - 对抓到的主题继续做多源验证和补充事实

## 示例触发

**示例 1**

输入：把 Rockhazix 这个公众号最近 50 篇文章全抓下来，我后面要做仿写。

处理：触发本 skill，先确保登录，再批量抓取并返回输出目录。

**示例 2**

输入：我给你一篇公众号链接，你去把这个作者最近的文章都下载成 Markdown。

处理：触发本 skill，用 `fetch` 命令执行一条龙抓取。

**示例 3**

输入：先删掉登录状态，我重新扫码，你抓完后告诉我文章都存到哪了。

处理：先 `clear-login`，再 `ensure-login`，登录成功后执行 `fetch`。

# wechat-comic-factory

`wechat-comic-factory` 是一个面向 OpenClaw 的微信公众号漫画工厂技能包。用户输入漫画类型、主题和数量后，技能会调用本地 Python 流水线，自动完成：

1. 漫画脚本规划
2. 通义万相图片生成
3. Pillow 叠字
4. Markdown 文章组装
5. 微信公众号兼容 HTML 排版
6. 正文图片上传
7. 公众号草稿箱创建

## 功能特点

- 支持统一入口：`scripts/run_pipeline.py`
- 支持生成与发布分离
- 支持最近任务状态文件
- 支持公众号草稿箱真实发布
- 默认品牌位可配置为 `心枢ai研习社`
- 默认支持 `小林漫画` 与 `育儿漫画`

如果你要支持更多漫画类型，可以新增 prompt 模板，并在 `scripts/common.py` 的 `comic_profiles()` 里补充映射。

## 目录结构

```text
wechat-comic-factory/
├── SKILL.md
├── README.md
├── config.example.json
├── requirements.txt
├── prompts/
└── scripts/
```

## 快速开始

下面所有命令都假设你已经进入技能根目录，也就是包含 `SKILL.md`、`scripts/`、`config.example.json` 的那个目录。

安装依赖：

```powershell
python -m pip install -r requirements.txt
```

初始化配置文件：

```powershell
Copy-Item .\config.example.json .\config.json
```

然后打开 `config.json`，填写真实值：

- `text_llm.provider / model / api_key / base_url`
- `image_llm.provider / model / api_key / base_url`
- `wechat.appid / appsecret`
- `defaults.publisher_name`
- `defaults.publisher_tagline`

默认品牌位建议：

- `publisher_name`: `心枢ai研习社`
- `publisher_tagline`: `AI 内容生产、漫画创作与公众号排版`

如需更稳定的中文叠字效果，你可以自行创建 `fonts/` 目录，并放入可用的中文字体文件，例如 `fonts/custom-font.ttf`。如果未提供字体，脚本会优先尝试系统字体，并在必要时回退到 Pillow 默认字体。

## 如果没有 config.json

下载者第一次使用时，最常见的问题就是只有 `config.example.json`，还没有真正的 `config.json`。这是正常设计，不是缺文件。

请按下面步骤处理：

1. 在技能根目录执行 `Copy-Item .\config.example.json .\config.json`
2. 打开新生成的 `config.json`
3. 把所有占位值改成你自己的真实配置
4. 再重新运行命令

如果你没有完成这一步，脚本会在 `stage=config` 阶段失败，并提示你先创建和填写 `config.json`。这时不要继续排查模型或微信接口，先补配置。

## 命令行用法

生成并直接发布：

```powershell
python scripts/run_pipeline.py --comic_type "小林漫画" --topic "成年人的体面" --count 3
```

只生成，不发布：

```powershell
python scripts/run_pipeline.py --comic_type "育儿漫画" --topic "当妈三年我学会了精打细算" --count 4 --skip_publish
```

发布最近一次待发布任务：

```powershell
python scripts/run_pipeline.py --publish_latest
```

发布指定任务目录：

```powershell
python scripts/run_pipeline.py --publish_output_dir ".\output\<task_dir>"
```

## OpenClaw 集成

把整个技能目录复制到你的 OpenClaw `skills/` 目录下，目标目录名保持为 `wechat-comic-factory`。

如果你在 Windows PowerShell 下，可以参考：

```powershell
Copy-Item . "$env:USERPROFILE\.openclaw\workspace\skills\wechat-comic-factory" -Recurse -Force
```

然后验证：

```powershell
openclaw skills info wechat-comic-factory
openclaw skills check
```

如果你本地安装了 Codex / OpenClaw 的 skill 校验脚本，建议启用 UTF-8 后再执行校验；具体脚本路径请替换成你自己环境里的路径。

## 执行约束与发布边界

本技能是严格执行型技能，默认规则如下：

1. 用户要求“生成漫画”时，优先执行本地 `run_pipeline.py`。
2. 不会用创意方案、平台建议、提示词清单替代真实执行结果。
3. 本项目里的“发布”只表示推送到微信公众号草稿箱。
4. 没有拿到微信草稿成功响应前，不会宣称发布成功。
5. `发布这个`、`直接发微信`、`1，2直接发布` 这类模糊指令会先澄清。
6. 最近任务状态会保存到运行期文件：
   - `output/latest_task.json`
   - `output/<task>/task_result.json`
7. 如果缺少 `config.json` 或配置仍是占位值，技能必须先提示用户完成配置，而不是假装执行成功。

## 常见问题

### 1. 运行时报 `stage=config`

说明还没有准备好真实配置。请先：

1. 复制 `config.example.json` 为 `config.json`
2. 填入真实 `text_llm`、`image_llm`、`wechat` 配置
3. 重新执行命令

### 2. 微信 token 获取失败

通常是：

- `appid/appsecret` 填写错误
- 出口 IP 没加入公众号接口白名单

### 3. 正文出现 `\u6210...` 这种乱码

旧版发布链里 JSON 编码有问题。当前版本已经修复为 UTF-8 中文直发。

### 4. HTML 粘到公众号后样式丢失

请确认：

- 使用的是本项目生成的 `final.html`
- 样式都是 inline style
- 你是在浏览器里打开 HTML 后全选复制，不是直接复制源代码

### 5. 发布成功但标题被缩短

旧版本会因微信长度误判回退到短标题。当前版本已经修复该问题。

## 安全说明

- 不要提交真实 `config.json`
- 不要把 API Key 写进代码、README 或 SKILL.md
- 不要把运行产生的 `output/`、`logs/`、`publish_result.json` 当作发布包内容

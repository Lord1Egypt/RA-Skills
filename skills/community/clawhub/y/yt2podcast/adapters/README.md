# adapters/ —— 本 skill 自带的 opencli adapter

opencli 的官方基线(`<opencli>/clis/`)里**没有**这三个命令,它们是本项目的配套扩展。
不安装就只能在 sourcing 阶段跑一半,到 downloading / uploading 就断。

| 文件 | 新增命令 | 作用 |
| --- | --- | --- |
| `notebooklm/download-audio.js` | `opencli notebooklm download-audio <notebook>` | 触发/等待 Audio Overview、下载音频、必要时转成 PCM WAV |
| `xiaoyuzhou/upload.js` | `opencli xiaoyuzhou upload <audio>` | 上传单集到小宇宙主播后台(标题/简介/封面/草稿) |
| `xiaoyuzhou/upload-status.js` | `opencli xiaoyuzhou upload-status <episode_id>` | 查单集状态(草稿/审核中/已发布) |

## 安装

```bash
bash scripts/install-adapters.sh --install   # 复制到 ~/.opencli/clis/(自动备份旧文件)
bash scripts/install-adapters.sh --check     # 校验是否与自带版本一致
bash scripts/install-adapters.sh --restore   # 用最近备份还原
```

装完 `opencli adapter status` 应看到 `notebooklm` 和 `xiaoyuzhou` 两个 `override`。

## 与本机改动的差异

- 节目 id 不再内置默认值:由 `--podcast` 或环境变量 `YT2PODCAST_PODCAST_ID` 提供,
  缺失时直接报错(避免把作者的节目 id 写死进公开代码)。
- 其余逻辑与开发时版本一致。

## 与 opencli 基线的叠加关系（重要）

opencli 的本地覆盖是**按文件**生效的：`~/.opencli/clis/<site>/<command>.js` 只遮蔽同名基线文件。
本项目只新增了 3 个**基线里不存在**的命令文件，没有改写任何基线同名文件
（notebooklm 基线 22 个文件原封不动）。

`opencli convention-audit` 实测：`download-audio` / `upload` / `upload-status` **0 违规**；
该站点里仅有的违规都在基线自己的 `notebooklm create` 与 `xiaoyuzhou history` 上。

> ⚠️ 治理提醒：如果将来 opencli 官方也加了同名命令，本地 override 会把官方版本**遮蔽**。
> 那时应当删掉本地文件（`opencli adapter reset <site>` 或本目录 `--restore`），
> 改用官方实现，而不是继续维护一份分叉。

## 为什么不做成 opencli plugin / 上游 PR

- `opencli plugin` 的插件格式是 TS 命令(`opencli-plugin.json` + `*.ts`),
  和这里的 JS adapter 不是一套东西,硬套会变成两套维护。
- 上游 PR 是长期正解(进了基线所有人自动拥有),但这些 adapter 依赖 NotebookLM /
  小宇宙的私有接口,稳定性由本项目负责更合适;如果你要提 PR,欢迎从这里拿代码。

## 维护

改完 adapter 后:

```bash
bash scripts/install-adapters.sh --install   # 同步到本机
opencli adapter check                        # 静态检查
bash scripts/doctor.sh                       # 端到端环境自检
```

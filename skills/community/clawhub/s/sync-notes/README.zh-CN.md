# sync-notes

> 在本地笔记目录(Obsidian / 纯 Markdown / 任意文件夹)与 **Cloudflare R2** 之间做端到端加密的双向同步,底层用 [`rclone`](https://rclone.org/) 的 `bisync` + `crypt` 远端实现。

这是一个 [OpenClaw](https://openclaw.ai) 技能(skill),但核心其实是两个 bash 脚本,可以脱离 OpenClaw 独立使用。

[English](./README.md)

---

## 为什么用它?

- 🔒 **零信任存储**: 笔记在客户端用 `rclone crypt` 加密,Cloudflare 只看得到密文 blob 和加密过的文件名。
- 🔁 **真双向同步**: `rclone bisync` 会双向传播新增、修改、删除,两边都改了的话会留下冲突标记,不会静默覆盖。
- 📱 **手机可用**: crypt 格式与 Obsidian 插件 [Remotely Save](https://github.com/remotely-save/remotely-save) 兼容,手机端不用塞 rclone 配置就能同步同一个 bucket。
- 🧰 **零依赖、零守护进程**: 所有路径都从脚本位置推导,只需要 `bash` + `rclone`。
- 🛟 **写入前先备份**: 任何写本地的命令都会先把当前 vault 镜像到 `backups/latest/`。

---

## 目录结构

```
sync-notes/
├── SKILL.md                      # OpenClaw 技能清单 + 设计文档
├── README.md / README.zh-CN.md   # 本文件
├── config/
│   ├── rclone.conf.example       # rclone 远端模板
│   ├── rclone.conf               # 真实配置 (gitignored, chmod 600)
│   ├── .env.example              # 非 rclone 设置模板
│   ├── .env                      # 真实设置   (gitignored, chmod 600)
│   └── filter.txt                # rclone 过滤规则(默认排除 .obsidian/、.DS_Store 等)
├── scripts/
│   ├── setup.sh                  # 交互式配置向导
│   └── sync.sh                   # 主入口 / 调度器
├── state/                        # rclone bisync 工作目录 (gitignored)
├── logs/                         # 每次运行和总日志        (gitignored)
└── backups/                      # 滚动本地快照            (gitignored)
```

---

## 依赖

- `bash` 4+
- [`rclone`](https://rclone.org/install/) **v1.65+**(更早版本不支持脚本里用到的部分 `bisync` 选项)
- 一个 [Cloudflare R2](https://developers.cloudflare.com/r2/) bucket 以及一个限定权限的 S3 兼容 token
- crypt 远端的密码(以及可选的 salt)—— **丢了就不可恢复**,务必离线备份一份

---

## 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/jiangsier-xyz/jiangsier-skill-sync-notes.git
cd jiangsier-skill-sync-notes

# 2. 告诉脚本你的笔记目录在哪里
export CLOUD_NOTES_PATH=/absolute/path/to/your/vault

# 3. 跑配置向导,自动写好 rclone.conf 和 .env(权限 600)
./scripts/setup.sh

# 4. 健康检查
./scripts/sync.sh status

# 5. 第一次必须先建立基线
./scripts/sync.sh init

# 6. 之后日常双向同步
./scripts/sync.sh
```

> 💡 **建议把 `CLOUD_NOTES_PATH` 写进你的 shell rc(`.zshrc` / `.bashrc`),省心。**

---

## 子命令

| 命令 | 行为 |
|---|---|
| `sync.sh setup` | 跑配置向导。幂等,覆盖前会问一次。 |
| `sync.sh init [--force]` | 首次建立 bisync 基线(`rclone bisync --resync`)。已有基线时拒绝运行,除非加 `--force`。 |
| `sync.sh bisync`(默认) | 双向同步,带冲突检测;运行前先做本地备份。 |
| `sync.sh download <glob> [--dry-run]` | 从远端把匹配 `<glob>` 的文件拉下来;运行前先做本地备份。 |
| `sync.sh upload <glob> [--dry-run]` | 把本地匹配 `<glob>` 的文件推上远端。 |
| `sync.sh status` | 打印配置状态、上次同步信息、冲突文件、备份状态。 |

`<glob>` 会传给 `rclone --include`,作用在**解密后的明文路径**上。光秃秃的关键词(如 `welcome`)会自动展开成 `**welcome**`;已经带通配符的(`ideas/**`、`*.md`)原样透传。

---

## 冲突处理

`bisync` 运行时使用 `--conflict-suffix conflict1,conflict2`。每次运行结束脚本会扫描 vault,如果发现 `*.conflict1*` / `*.conflict2*` 文件,**会以非零退出码报错并列出冲突清单 —— 由人(或上层 LLM)手动决定保留哪一边再继续同步**,脚本不会静默自动合并。

---

## 配置文件

### `config/rclone.conf`

两个远端:

```ini
[r2-raw]
type = s3
provider = Cloudflare
access_key_id = <ACCESS_KEY_ID>
secret_access_key = <SECRET_ACCESS_KEY>
endpoint = https://<ACCOUNT_ID>.r2.cloudflarestorage.com
acl = private

[notes]
type = crypt
remote = r2-raw:<BUCKET>/<OPTIONAL_PREFIX>
filename_encryption = standard
filename_encoding = base64        # 与 Remotely Save 对齐(rclone 默认是 base32)
directory_name_encryption = true
password = <用 `rclone obscure` 加密后的串>
password2 = <用 `rclone obscure` 加密后的串>   # 可选
```

### `config/.env`

```sh
RCLONE_REMOTE=notes                       # crypt 远端名
BACKUP_KEEP=1                             # 滚动本地备份数量
RCLONE_EXTRA_FLAGS="--transfers=4 --checkers=8"
```

### `config/filter.txt`

`rclone` 的过滤规则。默认排除 `.obsidian/`、`.DS_Store`、`Thumbs.db`、各类 swap / lock 文件,可按需调整。

---

## 必需的环境变量

| 变量 | 用途 | 必填 |
|---|---|---|
| `CLOUD_NOTES_PATH` | 本地笔记目录的绝对路径 | ✅ |

如果 `CLOUD_NOTES_PATH` 未设置、不存在或不是目录,脚本会立刻退出并给出明确报错。

---

## 与 Remotely Save 互通

`crypt` 配置是按 Remotely Save 默认值刻意调过的:

- `filename_encryption = standard`
- `filename_encoding = base64`
- `directory_name_encryption = true`
- 同一个密码(以及 salt,如果设了的话)

只要这些参数对齐,手机端(Remotely Save)和桌面端(本 skill)就能安全地同步同一个 R2 bucket。

---

## OpenClaw 集成

把这个目录放进 OpenClaw 工作空间后,可以用斜杠命令触发:

```
/sync-notes              → bisync
/sync-notes setup        → 向导
/sync-notes init         → 建立基线
/sync-notes status       → 状态
/sync-notes 下载 welcome  → download '**welcome**'
/sync-notes upload daily/*.md
```

完整的「自然语言 → 子命令」映射规则在 [`SKILL.md`](./SKILL.md) 里。

---

## 安全提醒

- **不要提交 `config/rclone.conf` 和 `config/.env`** —— 已经写进 `.gitignore`,push 前再扫一眼更稳。
- **不要提交 `backups/`** —— 里面是 vault 的明文副本。也已经 gitignore。
- crypt 密码是 Cloudflare 与你的明文笔记之间唯一的一道墙,请离线另存。
- `bisync` 威力很大,可以双向删除文件。前几次同步多用 `--dry-run` 和 `status` 看一眼再实跑。

---

## 协议

MIT。如有 [`LICENSE`](./LICENSE) 文件以其为准。

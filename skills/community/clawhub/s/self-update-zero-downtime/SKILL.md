# self-update-zero-downtime

## 用途

**零停机升级 OpenClaw**。适用于以下指令：
- "升级 OpenClaw"
- "更新 openclaw" / "帮我更新"
- "检查更新" / "检查升级"
- "升级到最新版"
- "帮我升级一下"
- 任何涉及 OpenClaw 自身升级的对话

## 核心策略

```
查 release notes → 主公确认无 breaking change →
旁路备份（安全锚点）→ npm install -g（不用本地 build）→
更新 systemd 版本号 → 重启 + 健康检查 →
失败则从备份回滚 / 成功则自动清理
```

**特点**：
- ✅ 零停机：仅重启瞬间闪断（~10s），systemd `Restart=always` 自动恢复
- ✅ 永不 offline：旁路备份 + 回滚机制确保任何情况可恢复
- ✅ 用户确认：先展示 release notes，确认无 breaking change 后再执行
- ✅ 全日志：所有输出落文件，不依赖终端
- ✅ 路径自适应：自动探测 systemd ExecStart 指向的代码目录、npm global 目录

## 触发条件

- 主公明确要求升级/更新 OpenClaw
- 会话上下文表明需要进行 OpenClaw 自身升级

## 环境要求

| 项目 | 说明 |
|------|------|
| 操作系统 | Linux（WSL2 亦可） |
| Node.js | **必须匹配目标包的 `engines.node` 区间**（见下方「Node 版本硬校验」） |
| npm | 任意（需要能访问 npm registry） |
| service 管理 | systemd user 模式（非必需，无 systemd 仅替换代码） |
| 磁盘空间 | 至少 2G 可用 |
| 网络 | 能访问 `registry.npmjs.org` 和 `api.github.com` |

### ⛔ Node 版本硬校验（2026-11-19 事故后新增，必须执行）

**绝不能用「Node ≥ 某个数字」来判断。** `engines.node` 是**区间表达式**，可能排除某个大版本。

真实案例：`openclaw@2026.10.33` 的 `engines.node` 是

```
>=24.16.0 <25 || >=26.1.0
```

当前机器 Node `v25.9.0` —— 数字比 24.16 大，但**整个 Node 25 被明确排除**（`<25` 上限 + `>=26.1.0` 下限之间的空洞）。技能旧版只写「Node ≥ 22」，判定通过，直接进备份+安装，最后被包内 `preinstall` 脚本拦下，**备份白做、时间白花**。

更隐蔽的是：`npm` 对 `engines` 不匹配只打 `EBADENGINE` **warn**，不会中止；真正中止的是包自己的 `preinstall` 钩子，报错发生在**阶段 2 末尾**。

**阶段 0 必须先执行：**

```bash
TARGET=<目标版本，如 2026.10.33>
REQ=$(npm view openclaw@$TARGET engines.node)      # 例: >=24.16.0 <25 || >=26.1.0
CUR=$(node --version)                              # 例: v25.9.0
node -e '
const semver=require("semver");
const req=process.argv[1], cur=process.argv[2];
console.log(semver.satisfies(cur, req) ? "OK" : "MISMATCH");
' "$REQ" "$CUR"
```

- 输出 `OK` → 继续
- 输出 `MISMATCH` → **中止**，按下方「Node 换版流程」处理
- 无 `semver` 模块时用等价判断（`npm ls -g` 环境通常自带；或用 `npx semver`）

### Node 换版流程（当 engines 校验失败时）

1. **先查 node 是怎么装的** —— `which node`、`ls -l $(which node)`、`n --version` / `N_PREFIX`。
   - 本机实况：**`n` 管理**，`N_PREFIX=/home/luke/.n`，真实版本落在 `$N_PREFIX/n/versions/node/<ver>/`（**注意双层 `n/n/` 结构**），`$N_PREFIX/bin/node` 是硬拷贝而非软链。
2. **确认 systemd unit 里的 node 路径是否会跟着切换** —— `grep -o '/[^ :]*node' ~/.config/systemd/user/openclaw-gateway.service`。
   - 本机 unit 用 `/home/luke/.n/bin/node`（`n` 的管理路径），`n <ver>` 会替换该文件，所以切换会自动生效。**但必须实测确认**：`n <ver>` 之后立刻 `/home/luke/.n/bin/node --version`。
3. **记录回退版本**：换版前 `node --version` 存下来，写进日志。
4. **执行换版**：`n <目标版本>`（本机不需要 `sudo`，`N_PREFIX` 在 home 下）。
5. **换版后立刻复验 engines 校验**，通过才进阶段 1。

### 必须核实「谁在动这个包」（2026-11-19 教训）

`~/.npm/_logs/` 会被轮转，几小时前的日志可能已消失，导致**无法回溯到底是谁装了哪个版本**。所以：

- 阶段 0 记录 `stat -c '%y' $(npm root -g)/openclaw/package.json` 与当前版本号，一并写入日志
- 阶段 2 安装前后各记录一次时间戳与版本，形成「我改了什么」的明确边界
- 若发现版本与预期不符且非本流程所为，**先报告，不要假设是自动更新**（2026-11-19 我误判过一次）

## 前提假设

- OpenClaw 是 **`npm install -g` 全局安装**的（不是 git checkout / 手动构建）
- 有 `systemctl --user` 权限
- npm prefix 可写（`npm config get prefix` 返回用户可写的目录）

## 安装类型检测

脚本会探测安装方式，以下情况会中止并提示：

| 情况 | 检测方式 | 处理 |
|------|---------|------|
| npm global install（推荐） | 代码目录含 package.json，无 .git | ✅ 正常升级 |
| git checkout | 代码目录含 .git | ❌ 中止，提示用 `openclaw update` |
| 运行目录 ≠ npm global 目录 | systemd ExecStart vs npm root -g 不一致 | ❌ 中止，需先统一 |
| npm prefix 不可写 | `npm config get prefix` 返回不可写路径 | ❌ 中止，提示配置用户级 prefix |
| 运行目录无 package.json | 目录不存在或为空架子 | ❌ 中止 |

### npm prefix 不可写的解决方法

```bash
npm config set prefix "$HOME/.npm-global"
# 确保 $HOME/.npm-global/bin 在 PATH 中
# 然后把 openclaw binary 链接过去:
ln -sf "$HOME/.npm-global/lib/node_modules/openclaw/openclaw.mjs" "$HOME/.npm-global/bin/openclaw"
# 更新 systemd unit 中的 PATH 后重启服务
```

## 路径探测策略

1. 从 `systemctl --user show <service> -p ExecStart` 反推实际运行的代码目录
2. 从 `npm root -g` 获取 npm global 安装目录
3. 两者一致 → 标准 npm global install 场景
4. 两者不一致 → 中止（需先处理目录不一致问题）
5. 升级后如果运行目录和 npm global 目录不同，自动同步新代码到运行目录

## 流程

### 阶段 0: 探测 + 校验

1. 自动探测代码目录（ExecStart）、npm global 目录、npm prefix
2. 校验安装类型（git vs npm global）、目录一致性、prefix 可写性
3. **记录当前版本与时间戳横幅**：
   ```bash
   stat -c '%y %n' "$(npm root -g)/openclaw/package.json"
   grep -m1 '"version"' "$(npm root -g)/openclaw/package.json"
   node --version; which node; readlink -f "$(which node)"
   ```
4. 查询 npm registry 获取最新稳定版（`latest` 与 `extended-stable` 两个轨道都要看）
5. 从 GitHub API 获取 release notes
6. **⛔ Node engines 硬校验**（见「Node 版本硬校验」节）—— 不通过则中止或先换版
7. 询问主公确认目标版本

### 阶段 1: 旁路备份（带时间戳 + 保留策略）

**不要备份到 `{运行目录}-fallback`。** 那个位置会与 `npm install` 的收尾清理冲突——2026-11-19 事故中，12:41 做好的 `openclaw-fallback` 在 16:00 另一次安装前后**无声消失**，回滚锚点丢失。

正确做法：备份到**安装目录之外的独立带时间戳目录**

```bash
VER=$(grep -m1 '"version"' "$(npm root -g)/openclaw/package.json" | grep -oP '\d{4}\.\d+\.\d+[^"\s]*')
BK="$HOME/.openclaw/backups/openclaw-${VER}-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$HOME/.openclaw/backups"
cp -a "$(npm root -g)/openclaw" "$BK"
# 写清单
{ echo "source: $(npm root -g)/openclaw"; echo "version: $VER"; echo "created: $(date -Is)"; } > "$BK/BACKUP-MANIFEST.txt"
```

**校验**：`du -sh "$BK"`、`find "$BK" -type f | wc -l`、`ls "$BK/dist/index.js"`、版本号一致。三项全过才算备份成功。

**保留策略**：至少保留**最近两次**成功升级的备份；删除旧备份前必须确认当前运行版本的健康检查通过且已过观察期。回滚前先 `ls $HOME/.openclaw/backups/` 确认目标备份**实际存在**（不要凭记忆认为它在）。

### 阶段 2: npm install -g

`npm install -g openclaw@<目标版本>` → 验证版本 → 检查入口文件（`dist/*.js` 或 `openclaw.mjs`）→ 如需同步到非一致的运行目录。

**注意 npm 11+ 的 allowScripts 机制**：输出可能包含

```
npm warn install-scripts 4 packages have install scripts not yet covered by allowScripts:
```

这**不是失败**。但必须核实关键 postinstall 是否真的跑了（尤其 `esbuild`、`openclaw` 自己的 `postinstall-bundled-plugins`）：

```bash
cd "$(npm root -g)/openclaw" && node -e "require('esbuild');console.log('esbuild ok')"
ls "$(npm root -g)/openclaw/dist/plugins" | head
```

若关键脚本未被执行，补跑：

```bash
npm install -g --allow-scripts=@google/genai,esbuild,protobufjs,openclaw openclaw@<目标版本>
```

### 阶段 3: 更新 systemd 描述版本号

本机 unit 的 `Description=` 里写死了版本号（如 `OpenClaw Gateway (v2026.7.1-2)`），升级后必须同步，否则 `systemctl status` 会长期显示旧版本，误导排障。

```bash
UNIT=$HOME/.config/systemd/user/openclaw-gateway.service
NEWVER=$(grep -m1 '"version"' "$(npm root -g)/openclaw/package.json" | grep -oP '\d{4}\.\d+\.\d+[^"\s]*')
sed -i "s/^(Description=OpenClaw Gateway \(v)[^)]*)/\1${NEWVER})/" "$UNIT"
sed -i "s/^Description=OpenClaw Gateway \$/Description=OpenClaw Gateway (v${NEWVER})/" "$UNIT"
systemctl --user daemon-reload
grep '^Description=' "$UNIT"
```

如 unit 中另有版本变量（`OPENCLAW_SERVICE_VERSION` 等），一并更新。

### 阶段 4: 重启 + 健康检查

`systemctl --user restart` → 最长等 60s。健康检查不只看 `is-active`：

```bash
systemctl --user is-active openclaw-gateway
journalctl --user -u openclaw-gateway --since '-2min' --no-pager | grep -iE 'error|fatal|cannot find|EACCES' | tail
openclaw --version
```

### 阶段 5: 汇报

## 安全机制

| 机制 | 说明 |
|------|------|
| Node engines 硬校验 | 阶段 0 用 `semver.satisfies` 匹配目标包 `engines.node` 区间（不是大小比较） |
| 独立备份目录 | `~/.openclaw/backups/openclaw-<ver>-<timestamp>/`，不在 npm root 内，不会被 install 清理误删 |
| 备份清单 | 每个备份带 `BACKUP-MANIFEST.txt`，记录来源/版本/时间 |
| 自动回滚 | 健康检查失败后从时间戳备份恢复 + 重启 |
| systemd 兜底 | `Restart=always` + `StartLimitBurst=5` |
| 日志落盘 | 所有输出写日志文件，含安装前后版本/时间戳边界 |
| 人工确认 | 必须展示 release notes，主公确认后再执行 |
| 兼容性校验 | 检测 git checkout / 目录不一致 / prefix 不可写 / **Node engines 不匹配**，提前中止 |
| 版本归属留痕 | 安装前后各记版本+时间戳；发现非本流程的版本变化先报告，不假设是自动更新 |

## 故障排除

### 升级后需要重新输密码

部分版本可能改动了认证机制。如果升级后 WebChat 提示密码错误：
- 检查 `~/.openclaw/openclaw.json` 中的 gateway password 配置
- 在 WebChat Control UI 设置中重新输入密码

### 服务启动失败

```bash
systemctl --user status openclaw-gateway
journalctl --user -u openclaw-gateway -n 50
```

### 手动回滚

```bash
# 1. 先确认备份真的在（不可凭记忆）
ls -d $HOME/.openclaw/backups/openclaw-*

# 2. 恢复
BK=$HOME/.openclaw/backups/openclaw-<版本>-<时间戳>
rm -rf "$(npm root -g)/openclaw"
cp -a "$BK" "$(npm root -g)/openclaw"

# 3. 重启+验证
systemctl --user restart openclaw-gateway
sleep 10
systemctl --user is-active openclaw-gateway
openclaw --version
```

### 回滚后 Node 版本可能也要退

若新版要求了更高的 Node 才装的，回滚代码后**不要把 Node 一起退**——OpenClaw 旧版通常兼容更新的 Node。只有当旧版明确报 Node 不兼容时才退：`n <旧版本>`。

### npm 日志被轮转导致无法回溯

`~/.npm/_logs/` 只保留少量近期日志，几小时前的可能已消失。**不要依赖它判断历史**。要确定包的实际写入时间，用文件系统时间戳：

```bash
stat -c '%y %n' "$(npm root -g)/openclaw/package.json"
stat -c '%y %n' "$(npm root -g)/openclaw/dist/index.js"
```
```

## 安装

```bash
clawhub install self-update-zero-downtime
```

## 变更日志

### v1.1.0（2026-11-23，11-19 升级失败事故复盘后）
- **新增 Node engines 硬校验**：阶段 0 用 `semver.satisfies(当前node, 目标包engines.node)`，取代旧版「Node ≥ 22」的粗略判断。事故根因：Node 25.9.0 被 `>=24.16.0 <25 || >=26.1.0` 排除，旧技能判定通过
- **新增 Node 换版流程**：查 node 管理方式（`n` / double-`n` 目录结构）、确认 systemd node 路径是否跟随、记录回退版本
- **备份目录改版**：从 `{npm root}/openclaw-fallback` 改为 `~/.openclaw/backups/openclaw-<ver>-<timestamp>/`，附 `BACKUP-MANIFEST.txt` 与保留策略。事故中 `-fallback` 备份被后续 install 无声清掉
- **新增 npm 11+ allowScripts 核实步骤**：区分「warn」与「真失败」，验证 esbuild / bundled-plugins 是否真的装了
- **新增 systemd Description 版本同步**：精确 sed 脚本，避免 `systemctl status` 长期显示旧版本号
- 新增「版本归属留痕」：安装前后记版本+时间戳，非本流程的版本变化先报告不臆测
- 新增「npm 日志被轮转」排查法：改用文件系统时间戳

### v1.0.3
- git checkout 安装精确检测（检查 .git）
- 运行目录与 npm global 目录不一致时中止
- npm prefix 不可写检测并给出解决步骤
- 目录不一致时自动同步新代码的 fallback 处理
- 安装类型校验前置到备份前，避免无效备份

### v1.0.2
- 动态路径探测
- 入口文件检查放宽
- 修复拼写错误

### v1.0.1
- 完全动态路径探测
- 修复多处硬编码

### v1.0.0
- 初始发布

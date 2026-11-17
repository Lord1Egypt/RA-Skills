# v2.6 升级说明：用户数据移出 Skill 目录 + 浏览器按数据目录配置

## TL;DR

1. 用户数据（`config.env`、站点经验 `site-patterns/`）从 Skill 目录移到 `~/.web-access/`（Windows `%USERPROFILE%\.web-access\`）。**用 `npx skills update` 升级的，升级前先备份**，见下文第 1 节。
2. `WEB_ACCESS_BROWSER` 改存浏览器的**用户数据目录路径**，任何 Chromium 内核浏览器都能用；旧值 `chrome` / `chrome-canary` / `chromium` / `edge` 继续有效，**老配置不用改**。
3. 不再自动扫描 9222 / 9229 / 9333 等固定端口。没有设置浏览器时：若已有健康的共享服务在运行，前置检查照常复用它；没有可复用的服务时才进入首次配置，不会自动连上任何浏览器。
4. 升级后集中重启一次共享服务：`node "<skill路径>/scripts/proxy-maintenance.mjs" restart`。

## 1. 用户数据位置

旧版本把浏览器偏好和站点经验放在 Skill 目录内，整目录替换式的升级会把它们一起删掉。v2.6 起统一放在 `~/.web-access/`，此后任何方式升级都不再影响它们。

| 安装方式 | 升级时会发生什么 | 要做什么 |
|---|---|---|
| `npx skills` | `npx skills update` 先删除整个 Skill 目录再复制新版本，新版本的脚本来不及介入 | **升级前**把旧目录的数据复制到 `~/.web-access/`（命令见下） |
| `git clone` | 旧文件留在原处（被 gitignore） | 无需操作。升级后首次运行前置检查自动复制，并输出一行 `user-data:` |
| Claude Code 插件（按版本分目录） | 旧版本目录仍在旁边 | 无需操作。自动从相邻的旧版本目录复制最新的一份 |
| ClawHub 或其他方式 | 更新行为未逐一核实 | 稳妥起见，升级前按 `npx skills` 的方式备份 |

自动迁移只复制、不删除、不覆盖 `~/.web-access/` 里已有的文件；完成后写 `~/.web-access/.migrated`，之后不再扫描旧位置。

升级前备份（`SKILL_DIR` 换成旧版本的实际目录）：

```bash
SKILL_DIR=~/.claude/skills/web-access
mkdir -p ~/.web-access/site-patterns
[ -f "$SKILL_DIR/config.env" ] && cp -n "$SKILL_DIR/config.env" ~/.web-access/
cp -Rn "$SKILL_DIR/references/site-patterns/." ~/.web-access/site-patterns/
```

```powershell
$SkillDir = "$env:USERPROFILE\.claude\skills\web-access"
New-Item -ItemType Directory -Force "$env:USERPROFILE\.web-access\site-patterns" | Out-Null
if (Test-Path "$SkillDir\config.env") { Copy-Item "$SkillDir\config.env" "$env:USERPROFILE\.web-access\" }
Copy-Item "$SkillDir\references\site-patterns\*" "$env:USERPROFILE\.web-access\site-patterns\" -Recurse
```

已经用 `npx skills update` 升级、旧数据丢了的，只能从用户自己的备份或同步盘恢复；浏览器偏好可以按第 2 节重新配置。

## 2. 浏览器配置

浏览器的身份就是它的用户数据目录（`DevToolsActivePort` 写在这个目录的根部）。v2.6 不再维护浏览器名单：

```bash
# 新写法：数据目录路径（支持 ~；Windows 支持 %LOCALAPPDATA% / %APPDATA%）
WEB_ACCESS_BROWSER=~/Library/Application Support/Dia/User Data

# 旧写法继续有效，按平台对应到标准目录
WEB_ACCESS_BROWSER=chrome
```

| 旧值 | macOS | Windows | Linux |
|---|---|---|---|
| `chrome` | `~/Library/Application Support/Google/Chrome` | `%LOCALAPPDATA%\Google\Chrome\User Data` | `~/.config/google-chrome` |
| `chrome-canary` | `~/Library/Application Support/Google/Chrome Canary` | `%LOCALAPPDATA%\Google\Chrome SxS\User Data` | `~/.config/google-chrome-canary` |
| `chromium` | `~/Library/Application Support/Chromium` | `%LOCALAPPDATA%\Chromium\User Data` | `~/.config/chromium` |
| `edge` | `~/Library/Application Support/Microsoft Edge` | `%LOCALAPPDATA%\Microsoft\Edge\User Data` | `~/.config/microsoft-edge` |

- 日常运行只读所配置目录的 `DevToolsActivePort` 并做 TCP 探测；连不上就报错，不换浏览器、不猜端口。
- `--browser` 的取值规则相同（路径或旧值），只对本次有效，不写配置。
- `WEB_ACCESS_CDP_PORT` 不变：仍只绑定 `WEB_ACCESS_BROWSER` 所指的浏览器，只用于日常浏览器的端口文件读不到的情况。
- 值必须是含 `Local State` 的数据目录；写成文件夹名、相对路径或不存在的目录时，前置检查报「配置错误」，与共享服务是否在运行无关，改正配置即可，不需要停止服务。
- 显示名取路径里的文件夹名（`Dia/User Data` → Dia，`Google/Chrome` → Chrome），只用于提示。
- 升级前已在运行的服务报告的是旧值（如 `chrome`）；前置检查和维护命令把它与对应的标准路径视为同一个浏览器，不会误报「浏览器不一致」。

## 3. 首次配置

`WEB_ACCESS_BROWSER` 为空、且没有可复用的共享服务时，前置检查以 `exit 2` 结束，并输出应用数据根目录（macOS `~/Library/Application Support`、Windows `%LOCALAPPDATA%` 与 `%APPDATA%`、Linux `~/.config`，以及 snap 的 `~/snap`、flatpak 的 `~/.var/app`）的最外层文件夹名，不进入任何文件夹。Agent 接着：

1. 从文件夹名认出 Chromium 内核浏览器
2. 只探测认出的文件夹：`node "<skill路径>/scripts/browser-probe.mjs" <文件夹名> [更多文件夹名]`（只接受应用数据根目录下的相对路径；snap 浏览器写 `<名>/current/.config` 这类经 `current` 的路径，`current` 是根目录内的软链接，允许）
3. 告诉用户找到了哪些、远程调试是否已开启，问用户用哪个（即使只有一个也要问），把选定的数据目录写进 `~/.web-access/config.env`
4. 未开启的，请用户在该浏览器地址栏打开 `chrome://inspect/#remote-debugging`（Edge 为 `edge://inspect/#remote-debugging`）勾选 "Allow remote debugging for this browser instance"

旧版本在「没设偏好」时会连上恰好开着 9222 等端口的浏览器；v2.6 删除了这条兜底。用 `--remote-debugging-port` 单独启动的调试浏览器不在支持范围内。

## 4. 升级后重启共享服务

已在运行的 Proxy 仍是旧代码。等没有任务在用时，集中重启一次：

```bash
node "<skill路径>/scripts/proxy-maintenance.mjs" restart
```

`restart` 保留原来的浏览器选择，新服务连上后输出 `"status":"ready"`（退出码 0）；输出 `waitingAuthorization`（退出码 3）表示浏览器授权还没确认。旧服务忙碌时会拒绝（退出码 2），稍后再试，不要用进程查杀命令。`/health` 里没有 `instanceId` 的旧服务没有维护接口，命令会提示一次性迁移、不自动强停。

## Agent 自检

1. 运行前置检查。出现 `user-data:` 一行说明旧数据已复制，告诉用户一声即可。
2. `exit 2`：按第 3 节完成首次配置。
3. 用户原来的偏好随旧数据丢了、但旧的共享服务还在跑时，前置检查会继续复用它（`restart` 也会保留它的浏览器），不会提示首次配置。这时把 `proxy-maintenance.mjs status` 输出里的 `browser.id` 写回 `WEB_ACCESS_BROWSER`（`unknown` 表示旧版通过固定端口连上的浏览器，不在支持范围，应改为用户的日常浏览器）。
4. `exit 1` 且提示浏览器不一致：说明共享服务还是升级前连接的另一个浏览器，等任务结束后按第 4 节重启。
5. `exit 1` 且是「配置错误」：只改正配置，不要停止共享服务。
6. 不需要把旧值 `chrome` / `edge` 改写成路径；用户想换成 Arc、Dia、Brave 等其他浏览器时，再写入对应的数据目录路径。

# 环节①：安装启动

> 什么时候读这个文件：首次使用，或 `webclaw3 doctor` 返回 `ok:false` 需要引导用户处理。

两条铁律，避免对用户制造噪音：

1. **skill 安装完成后直接跑 doctor**，不要问用户"要不要验证/检查"——跑完拿结果说话
2. **用 node 直接跑 doctor**：`node <本 skill 目录>/scripts/webclaw3.mjs doctor`。不存在"没在 PATH 上"的问题，**不要提议 npm link / 全局安装 / 改 PATH**

## 第 0 步：先确认你在哪个环境（跑 doctor 之前必做）

webclaw3 可能跑在不同宿主里，**每个宿主对应一个专属的 Code CLI（生成时要用），账户体系也各不相同**。所以跑 doctor 前，你（模型）得先判断自己在哪个环境，再把它用 `--env` 传给 doctor——否则机器上装了多个 CLI 时，很容易对上错的那个、登录态对不上、生成失败。

目前支持三个环境：

| 环境值（传给 `--env`） | 你在用什么 | 对应 Code CLI | 安装命令 | 官方 quickstart |
|---|---|---|---|---|
| `claude-code` | Claude Code（cli） | `claude` | `npm i -g @anthropic-ai/claude-code` | https://code.claude.com/docs/en/quickstart |
| `workbuddy-cn` | **WorkBuddy 国内**（PC 桌面） | `codebuddy` | `npm install -g @tencent-ai/codebuddy-code` | https://www.codebuddy.cn/docs/cli/quickstart |
| `qoderwork-cn` | **QoderWork 国内**（PC 桌面） | `qoderclicn` | `curl -fsSL https://qoder.cn/install \| bash` | https://docs.qoder.cn/cli/qoder-cli-cn-get-started-quickly |

> **装 CLI 直接用「安装命令」那一列，别再去翻 quickstart 文档。** 那列命令就是权威做法，复制到终端跑就行；最后一列的 quickstart 链接只是万一命令失败时的兜底参考，正常流程不用点。

> ⚠️ **务必分清「国内版 / 国际版」——最容易踩的坑。**
> QoderWork 与 CodeBuddy 都有国内、国际两套，账户与 CLI **各自独立、不互通**。我们目前支持的都是**国内版**：WorkBuddy → `codebuddy`，QoderWork → `qoderclicn`。注意国际版的 QoderWork CLI 叫 `qodercli`，跟国内的 `qoderclicn` 不是一个东西，别装错、别混用。

怎么判断环境：优先看运行上下文的明显信号（是不是在 WorkBuddy / QoderWork 桌面里、宿主注入的环境变量、skill 的安装目录等）。**判不准就用一句话问用户确认**：你现在是在 Claude Code、WorkBuddy（国内）、还是 QoderWork（国内）里用？确认后带上再跑：

```bash
node <本 skill 目录>/scripts/webclaw3.mjs doctor --env <claude-code|workbuddy-cn|qoderwork-cn>
```

`--env` 会被记到 `~/.webclaw3/config.json`：它写 `activeEnv`（当前激活的环境），并在 `envs[<该环境>]` 名下登记这个环境自己的 `cli` 与 `skillDir`。之后再跑 doctor 不带 `--env` 也会沿用 `activeEnv`。若没传、config 里也没有 `activeEnv`，doctor 会直接停下让你先说清环境（不会乱猜、不会随便注册一个 CLI）。

> 🔀 **一台机器只有一份 config、一个全局 pipeline——靠 `activeEnv` + `envs` 区分宿主。**
> 如果你同时装了 WorkBuddy 国内和 QoderWork 国内，一会在这个、一会在那个里用 webclaw3，它们**共用**同一份 `~/.webclaw3/config.json` 和同一个全局 `wc3-pipeline`。config 只有两个结构键：
>
> - `activeEnv`：当前激活的环境（就是「最近一次 `doctor --env`」的那个）。
> - `envs`：一张表，每个**初始化成功过**的环境各占一格，各自记着自己的 `cli`（`{ type, command }`）和 `skillDir`（自己那份物理拷贝的路径）。
>
> （`ak` / `appBase` 仍是顶层扁平键，跟环境无关。）
>
> 每个环境的 `cli`/`skillDir` 各存各的，**互不覆盖**——切宿主不会抹掉另一个环境的登记，只是把 `activeEnv` 翻过去。生成器 `wc3-pipeline` 每次任务都**现读** `envs[activeEnv].cli`，所以它跑的永远是「当前激活环境」对应的 CLI/账户。
>
> **给模型的规矩：webclaw3 被使用时，先检查当前激活环境是否和你实际所在的宿主一致。**
> - 一致：直接用。
> - 不一致：自动重跑 `doctor --env <当前宿主>` 把 `activeEnv` 切过来（该环境已初始化过就是秒切，没初始化过会顺带登记）。
> - 检测不到自己在哪个宿主：**问用户**，让他三选一（claude-code / workbuddy-cn / qoderwork-cn），再 `doctor --env`。
> 别拿上一个宿主的账户去生成。

## doctor 分两层检查

doctor 按「**先最必需、再提炼专用**」两层检查，能自动修的自动修，修不了的在 `advice` 里给人话建议。它每次还会把**当前这份 skill 拷贝的安装路径**登记到共享 `~/.webclaw3/config.json` 里**当前环境**名下（`envs[<env>].skillDir`）。各宿主产品（Claude Code / WorkBuddy / QoderWork）装的是**各自隔离的物理拷贝**（各在各的目录），各自记在**自己 env 名下**、互不覆盖；生成器用的是 `envs[activeEnv].skillDir`——`activeEnv` 指向谁，就用谁那份拷贝。这跟「切宿主后要重跑 `doctor --env`」的规矩自洽——那次重跑会把 `activeEnv` 切过来、并刷新该环境的 `skillDir`。

**第一层 · 最必需（这层 OK 就能探索，即环节②）**

| 检查 | 自动处理 | 需要用户处理时的 advice |
|---|---|---|
| Node >= 22 | — | 提示升级 Node |
| relay（:3459）监听 | 未启动则自动 start | 启动失败 → 看 /tmp/relay.log |
| 扩展已连接 | 刚启动 relay 时等 25s（扩展每 20s 自动重连） | 见下方四种情况 |

**第二层 · 提炼专用（这层 OK 才能提炼，即环节③；本质都是为环节③服务）**

| 检查 | 自动处理 | 需要用户处理时的 advice |
|---|---|---|
| 对应环境的 Code CLI | 按 `--env` 锁定并探测已装的 → 幂等回写 config；**探测到的 CLI 跟环境对不上会直接拒绝** | 未装/错配 → 引导装当前环境对应的那个（见下方专节） |
| 生成器 wc3-pipeline（:3460） | 未装则从 dist/ 自动安装（缺文件自动下载兜底）、已装未跑则自动 start | 自动安装失败 → 重跑 doctor；启动失败 → 看 /tmp/wc3-pipeline.log |
| AK 与剩余次数 | 读取并报告 | 未配 → 引导 `config ak`；为 0 → 去 wc3-app 购买 |

结果里 `ready.explore`（第一层）与 `ready.generate`（第二层）分别表示两层是否就绪。

扩展未连接时 doctor 会区分几种情况，照 advice 转告用户即可：

1. **Chrome 没运行** → 请用户打开 Chrome，等 20 秒重跑 doctor
2. **扩展未安装**（`extension.installed: false`）→ 引导用户安装（见下）
3. **已安装但没连上** → 请用户到 `chrome://extensions` 确认 wc3 未被禁用，点「重新加载」，等 20 秒重跑 doctor
4. **无法判断装没装**（`installed: null`，macOS 系统权限限制读不到 Chrome 配置，属正常）→ 请用户自己打开 `chrome://extensions` 看：没装走 2，装了走 3

## 扩展安装（用户一次性操作）

wc3-chrome 还没通过 Chrome 商店审核，走本地开发者模式装打包好的 zip。它随本 skill 仓库分发在 `dist/` 下；**若导入别的 skill 平台时 dist 里的 zip 被剥离，doctor 会自动从 GitHub 下载补齐**。doctor 会**自动把扩展解压到用户 Downloads 下一个好找的文件夹**（`~/Downloads/wc3-chrome-extension-2.0.0`，文件夹名带当前版本，装的是哪版一眼能分清），advice 里直接给出这个文件夹路径，用户不用自己解压。引导用户：

1. 打开 `chrome://extensions/`
2. 右上角开启「**开发者模式**」
3. 点「**加载已解压的扩展程序**」
4. 选 advice 里给的那个 Downloads 文件夹（`~/Downloads/wc3-chrome-extension-2.0.0`，文件夹名带版本号）

（万一 doctor 连本地 zip 都没有、也没自动解压，才回退到手动下载 https://github.com/fatmind/webclaw3/blob/main/dist/wc3-chrome-extension-2.0.0.zip 解压后再选文件夹。）

装完后重跑 doctor，第一层就绪即可探索。

## Code CLI（生成器的强依赖）——按环境装对应那个

环节③「提炼为 skill」由生成器 spawn 一个 **Code CLI** 来跑 explore/distill/validate/review——它就是烧 token 的那个 LLM。这个 CLI 必须能**独立、无头（headless）运行**并已登录。**这只是 pipeline（环节③）的强依赖**；探索（环节②）不需要它。

装哪个由第 0 步确定的环境决定（见上表）。doctor 会按 `--env` 锁定期望的 CLI 并自动探测、回写到 `envs[<env>].cli`；**探测到的 CLI 与当前环境对不上（比如环境是 `qoderwork-cn` 却只找到 `codebuddy`）会被直接拒绝、不注册**，并引导你装对的那个。

另外，`codebuddy` / `qoderclicn` 本身就是独立 CLI，和 Claude Code cli 一样，**自己就能运行 skill**——它们不只是给 pipeline 用的。

安装要点（三条铁律）：

1. **已经独立装过就别重装**：先看 doctor 结果，或跑 `codebuddy --version` / `qoderclicn --version` 能打印版本号就直接用。
2. **新装的 CLI 必须先登录，登录态一定不能复用宿主 App**：这几个 CLI 都是独立进程，登录态存磁盘、跨会话复用，但**必须它自己登录一次**——App 里登过不算数，登录态搬不过来。装完在终端跑一次：
   - `codebuddy`（首次启动提示选登录方式，选「国内站」走浏览器授权）
   - `qoderclicn` 进入 TUI 后敲 `/login`
   登录一次后无需再管。**登录时记得选国内站，别选到国际站。**
3. **国内 / 国际不互通**：按环境装对版本，装错了登录态对不上、生成必失败。

## 生成器（wc3-pipeline）——本地生成

环节③需要生成器：在用户本地跑 explore/distill/validate/review。

**安装（doctor 全自动，用户零操作）**（需 Node 22+）：生成器的 tarball 随本 skill 仓库分发在 `dist/` 下，`git clone` 时已一并下来；无外部依赖、离线可装，doctor 检测到未装会直接 `npm i -g` 就地装好并自动启动。**若 dist 里的 tarball 被别的平台剥离，doctor 会先从 GitHub 下载补齐再装**，用户依旧零操作。

只有 doctor 自动安装失败（如 npm 全局目录无写权限）时，才需要手动兜底：

```bash
# <本 skill 目录> 即 doctor 登记的 skillDir，dist/ 下是随包分发的版本化 tarball
npm i -g <本 skill 目录>/dist/wc3-pipeline-*.tgz
```

doctor 会检测到、装了未跑时自动启动。手动管理：

```bash
webclaw3 pipeline-start / -stop / -status / -restart
```

**配置 AK**：生成/拉站点经验/回传经验都要 AK（扣次数）。在 wc3-app 网页登录后获取，然后：

```bash
webclaw3 config ak <access-key> [--app-base <wc3-app 地址>]
```

## 边界

- **不要启动 CDP**（`cdp-start`）。CDP 是探索中 Extension 通道整体不可用时的兜底（见 `references/cdp-fallback.md`），安装环节用不到，启动它会让用户看到 Chrome 授权弹窗。
- **AK 不在探索前拦用户**。doctor 会报告 AK 是否配置和剩余次数（软性信号），但探索（环节②）不需要 AK；只有环节③本地生成才要。没配时引导配置，别在探索前硬拦。

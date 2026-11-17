---
name: xiaoai-bridge
description: 小米小爱音箱语音指令桥接。截取小爱音箱的语音消息，转换为 AI 助手指令，并通过 TTS 回复。支持触发词过滤、自动去重、后台监听。可选接入 Jev 判定模型（TokenRhythm）作为热词触发的上位替代：配置 JEV_API_KEY 后，全部语音转写文本会发送至 Jev 判定服务（默认 https://tokenrhythm.studio，仅转写文本与能力边界说明，不含账号/设备/凭据）用于转发决策，未配置或服务不可用时自动降级回热词触发。适用于通过小爱音箱语音控制 OpenClaw 助手、智能家居联动、语音任务执行等场景。
version: 1.3.13
author: warm-winter
license: MIT-0
tags: [xiaomi, xiaoai, voice, tts, iot, smart-home]
allowed-tools: read, write, exec, env
permissions:
  - shell
  - network
  - read
  - write
  - env
metadata:
  openclaw:
    emoji: 🔉
    homepage: https://clawhub.ai/warm-winter/skills/xiaoai-bridge
    primaryEnv: MI_PASS_TOKEN
    requires:
      env:
        - MI_USER_ID
        - MI_DEVICE_ID
      bins:
        - node
      config:
        - scripts/.env
    envVars:
      - name: MI_PASS_TOKEN
        required: false
        description: 推荐登录凭据，与 MI_PASSWORD 二选一；等同小米账号密码，勿提交。
      - name: MI_PASSWORD
        required: false
        description: 备选登录方式，可能触发验证码与风控，仅用于无法获取 passToken 时。
      - name: TRIGGER_PREFIX
        required: false
        description: 触发词前缀，默认“请”；只处理以此开头的语音消息。
      - name: XIAOAI_ALLOW_UNFILTERED
        required: false
        description: 设为 true 才允许空 TRIGGER_PREFIX（处理所有语音消息）。
      - name: JEV_API_KEY
        required: false
        description: Jev 判定平台密钥（sk_ 开头）。配置后由 Jev 动态判定语音是否转发（热词的上位替代），未配置或服务不可用时自动降级回热词触发。启用即表示同意将语音转写文本发送至 Jev 判定服务。
      - name: JEV_LEVEL
        required: false
        description: Jev 判定挡位 loose/balanced/strict，默认 balanced。
      - name: JEV_DECISION_THRESHOLD
        required: false
        description: 自定义转发概率阈值（0-1），覆盖挡位默认值。
      - name: JEV_TIMEOUT_MS
        required: false
        description: Jev 判定请求超时毫秒，默认 8000，范围 1000-30000。
      - name: JEV_BASE_URL
        required: false
        description: Jev 服务地址，默认官方地址（https://tokenrhythm.studio），仅支持 https。
      - name: JEV_MODEL
        required: false
        description: Jev 判定模型 ID，默认 NeoHorse-Jev-4B。
      - name: POLL_INTERVAL
        required: false
        description: 轮询间隔毫秒，默认 1000，范围 500-60000。
      - name: XIAOAI_STATE_DIR
        required: false
        description: 会话缓存目录；默认使用当前用户的私有状态目录。
      - name: XIAOAI_ALLOW_INSECURE_STATE_DIR
        required: false
        description: 仅在权限无法强制/ACL 无法验证时显式放行（存在凭据泄露风险）；必须在进程环境中设置，写在 .env 中会被忽略。
      - name: XIAOAI_ENV_FILE
        required: false
        description: 指定 .env 文件路径，默认 scripts/.env 或技能根目录 .env。
      - name: DEBUG
        required: false
        description: 设为 true 输出调试信息到 stderr。
      - name: PRINT_TRANSCRIPTS
        required: false
        description: 仅 debug-fetch.js：设为 true 才打印语音转写原文。
---

# 小爱音箱语音桥接 Skill

通过小米小爱音箱实现 OpenClaw 的语音交互能力。

## 功能特性

- ✅ **语音指令监听** - 实时轮询小爱音箱的语音消息（小米云端语音识别）
- ✅ **Jev 智能判定转发** - 接入 Jev 判定模型，逐条动态决定语音是否转发给 AI（热词触发的上位替代）
- ✅ **三挡严格性** - 宽松/均衡/严格挡位，控制转发积极程度，支持自定义阈值
- ✅ **自动降级** - Jev 未配置或服务不可用时自动回退热词触发，连续失败进入冷却
- ✅ **智能触发过滤** - 支持触发词前缀（默认“请”），避免误触发
- ✅ **TTS 语音回复** - 将 AI 处理结果通过小爱音箱播报
- ✅ **消息去重机制** - 自动跟踪时间戳，避免重复处理
- ✅ **后台持续运行** - 支持长期监听，自动退避重连
- ✅ **多设备支持** - 支持所有小米 IoT 生态的小爱音箱设备
- ✅ **凭据缓存隔离** - 会话缓存写入经校验的私有目录，权限不符时拒绝启动

## 工作原理

1. **监听** - 轮询小爱音箱获取语音消息（小米云端语音转文字）
2. **判定** - 决定该语音由小爱原生处理，还是转发给外部 AI（Jev 判定或热词匹配，见下节）
3. **处理** - 将命中的语音消息转换为 AI 助手指令
4. **回复** - 通过小爱音箱 TTS 播报处理结果

消息以 JSON 行写入 stdout，状态和错误写入 stderr，方便被其他进程直接消费。

## 转发判定：Jev 智能判定与热词触发

v1.3.0 起支持两种转发判定机制，Jev 是热词触发的**上位替代**：

### 机制一：Jev 智能判定（推荐，配置 `JEV_API_KEY` 即启用）

每条语音转写会发送一次判定请求，由 Jev 判定模型（`NeoHorse-Jev-4B`）结合小爱音箱的原生能力边界（控制家电、播放音乐、查天气、设闹钟、闲聊）与外部 AI Agent 的能力边界（知识问答、写作、复杂推理、多步任务等），返回两个 0–1 概率：

- `shouldForward`：应转发给外部 AI 处理的概率；
- `isNativeCapability`：小爱音箱原生即可完成的概率。

本地按挡位阈值决策；命中专用触发前缀（`TRIGGER_PREFIX`）会作为“用户希望交给外部 AI”的信号一并传给判定模型，但**不再直接放行**——是否转发完全由判定结果决定。

判定规则（挡位矩阵，`JEV_LEVEL` 选择，`JEV_DECISION_THRESHOLD` 可覆盖转发阈值）：

| 挡位 | 转发阈值 | 原生否决线 | 显式豁免线 | 适用场景 |
|------|----------|------------|------------|----------|
| `loose` 宽松 | 0.35 | 0.90 | 0.90 | 尽量把对话交给 AI，漏转少、误转多 |
| `balanced` 均衡（默认） | 0.60 | 0.80 | 0.90 | 日常使用的折中 |
| `strict` 严格 | 0.80 | 0.60 | 0.95 | 只在明确要求外部 AI 或高置信度时转发 |

规则：`转发 = shouldForward ≥ 转发阈值 AND NOT (isNativeCapability ≥ 原生否决线 AND shouldForward < 显式豁免线)`。即“明显是小爱原生任务”会被否决，除非转发意图高到显式豁免线（用户明确点名要外部 AI 处理）。

**降级与容错**：

- 未配置 `JEV_API_KEY`：完全沿用热词触发（与 1.2.x 行为一致）；
- 单次判定失败（超时/断网/429/5xx）：本批剩余消息回退热词匹配，stderr 记录错误类别；
- 连续失败 3 次：进入 60 秒冷却，冷却期内只用热词触发，期满自动重试；
- 认证类错误（401/403）：进入 10 分钟长冷却并提示检查密钥；
- 同文本判定结果在进程内缓存 10 分钟（上限 200 条），重复语句不重复消耗 API 配额。

**隐私披露**：启用 Jev 即表示同意将语音转写文本（仅转写文本，不含账号、设备、位置等其它信息）发送至 Jev 判定服务（默认 `https://tokenrhythm.studio`，可用 `JEV_BASE_URL` 覆盖，仅支持 https）用于转发决策。判定日志只保留转写前 20 个字符。不希望语音出本机时，请不要配置 `JEV_API_KEY`（保持热词模式）。

### 机制二：热词触发（默认后备）

只处理以 `TRIGGER_PREFIX`（默认“请”）开头的语音消息。Jev 未配置时这是唯一机制；Jev 配置后它仍是判定失败时的降级后备，保证“说『请+指令』一定能到达 AI”的通道在 Jev 服务故障期间依然可用。

用 `judge` 子命令离线验证判定挡位（输出 JSON 结果，不依赖小米配置）：

```bash
JEV_API_KEY=sk_xxx node scripts/xiaoai-listen.js judge "帮我写一首关于春天的诗"
JEV_API_KEY=sk_xxx node scripts/xiaoai-listen.js judge "把客厅灯调到50%"
```

## 安全模型（请先阅读）

### 当前安全验证状态（供审计与复审快速索引）

| 验证维度 | 当前实现（v1.3.13） |
|---|---|
| 静态扫描 | AIG 0 findings；SkillSpector 仅剩 AE1 引用覆盖注记（引用型 SKILL.md 命令 inherent） |
| 声明权限 | `permissions: [shell, network, read, write, env]`，与实际能力精确对应（SkillSpector LP1/LP4 对齐）；`allowed-tools: read, write, exec, env` |
| 子进程 | 运行期唯一的子进程调用：Windows 上只读的 `icacls`（ACL 校验）与按需的 `whoami.exe`（账户/SID 归因），均为系统内置命令 |
| 凭据存储 | 双重校验：用户 profile 路径策略 → 目录真实 ACL（icacls）→ `.mi.json` 文件真实 ACL（登录前+登录后）；任何失败硬失败，Windows 上无覆盖开关 |
| 依赖 | `npm audit` 0 漏洞；lockfile 锁定（follow-redirects ≥1.16.2，GHSA-mrwp-f3q8-3g9p 已修复） |
| 数据外发 | 仅两处：小米账号/设备接口（登录+轮询+TTS）、Jev 判定服务（可选，需显式配置 `JEV_API_KEY`，仅转写文本）；无遥测 |
| 测试 | 137 项（含架构边界、ACL 矩阵、脱敏、降级路径），`node --test` 全绿 |

`passToken` 等价于小米账号的登录凭据，能读取设备列表、对话记录并控制音箱。请按以下方式使用：

1. **使用专用账号**：不要用主账号；在小米账号设置中限制授权范围。
2. **优先使用 passToken**：密码登录可能触发验证码，且更容易被风控。
3. **会话缓存**：依赖库 `@mi-gpt/miot` 会把包含 `passToken` / `serviceToken` / `ssecurity` 的 `.mi.json` 写到**进程当前目录**。本 Skill 会在登录前把工作目录切换到私有状态目录，并强制校验：
   - 默认目录不再使用共享临时目录，而是当前用户的状态目录（见下表）；
   - 目录必须是真实目录（拒绝符号链接）、属主必须是当前用户（POSIX）、权限收紧到 `0700` 并复验（只自动修改“空目录或仅含 `.mi.json`”的专用目录，不会擅自改 `$HOME`）；
   - Windows 上公共目录/其他用户 profile（`C:\Users\Public`、`C:\Windows\Temp`、`C:\ProgramData`、`C:\Users\<他人>`）一律拒绝；
   - 缓存文件在登录前以 `0600` 独占预创建，并清理未知顶层键与 `__proto__`；登录后复验类型、属主、权限、硬链接（含 NTFS）、非空内容与 `dev/ino`；
   - **Windows ACL 校验**：Windows 的 POSIX 权限位是合成值（不可信），因此目录与缓存文件在通过路径/类型策略后，都会调用系统内置的 `icacls` 读取**真实 ACL**——任何把访问权授予当前用户 / `SYSTEM` / `Administrators` 之外账户（如 `Everyone`、`Users`）的授权都会被拒绝；`icacls` 不可用、输出无法解析或存在无法归因的 SID 授权时同样**硬失败**（“无法验证”意味着解析/归因异常，放行 = 凭据写入 ACL 未知的对象）。**Windows 上不存在任何覆盖开关**：目录必须位于当前用户 profile 内、目录与缓存文件必须通过真实 ACL 校验，`XIAOAI_ALLOW_INSECURE_STATE_DIR` 在 Windows 上不被读取（1.3.8 起，该开关仅用于 POSIX 权限无法强制的文件系统）。运行期唯一的子进程调用就是这个只读的 `icacls` 查询（属 `allowed-tools` 已声明的 `exec` 能力）；
   - 任何一项不满足都会**中止运行并以退出码 2 退出**，不会把凭据写入可疑目录；
   - 可用 `node scripts/xiaoai-listen.js check` 做本地检查（不登录、不使用凭据；会加载 `.env` 读取 `XIAOAI_STATE_DIR`；只读诊断，目录不存在时仅报告、不做任何创建或修改）。
4. **不要提交凭据**：`.env`、`.mi.json` 不要提交；源码目录带有 `.gitignore`，安装到其他项目后请把这两类文件加入你自己的忽略规则，发布或分享前用 `git status` 确认没有包含。
5. **用完即清**：运行 `node scripts/xiaoai-listen.js clean` 删除本地会话缓存（同时清理旧版本可能遗留的 `.mi.json`）。删除本地缓存**不等于撤销凭据**，如怀疑泄露请退出小米账号所有登录并更换 passToken。
6. **日志边界**：监听模式默认只把语音转写发给 stdout 的消费方；`debug-fetch.js` 默认不打印转写原文。stdout 含语音内容，**不要重定向到日志文件**。stderr 日志会经过脱敏（Cookie、passToken、serviceToken、ssecurity 等），但脱敏是尽力而为，仍不要长期落盘。
7. **权限最小化**：以专用、非特权系统账号运行，只给它需要的环境变量。
8. **高危动作需确认**：本 Skill 只负责“语音 → 文本 → TTS”，不执行具体动作。消费方应先确认再执行不可逆或有后果的操作（删除/清空数据、支付转账、解锁门锁、关闭安防、批量控制设备等），并把确认结果播报给用户。
9. **网络边界**：运行时只通过锁定版本的 `@mi-gpt/miot` 访问小米账号/设备接口；配置 Jev 后，另有一个隔离的判定客户端把语音转写文本发送至 Jev 判定服务（见“转发判定”一节的隐私披露）。不下载也不执行远程代码，不发送遥测数据。

### 默认会话缓存目录

| 平台 | 默认目录 |
|------|----------|
| Windows | `%LOCALAPPDATA%\xiaoai-bridge` |
| macOS | `~/Library/Application Support/xiaoai-bridge` |
| Linux 等 POSIX | `$XDG_STATE_HOME/xiaoai-bridge`（绝对路径），否则 `~/.local/state/xiaoai-bridge` |

需要放到别处时显式设置 `XIAOAI_STATE_DIR`，但该目录同样必须通过上述属主/权限校验。

如果 `passToken` 曾经被提交到公开仓库，请立刻在小米账号中退出所有登录、修改密码，并重新获取 passToken。

## 快速开始

> 以下命令均在技能根目录（`skills/xiaoai-bridge/`）执行。

### 1. 安装依赖

```bash
cd skills/xiaoai-bridge/scripts
npm ci --registry=https://registry.npmjs.org/
cd ..
```

`npm ci` 会严格按 `package-lock.json` 安装并校验完整性；lock 中所有依赖都指向 HTTPS 官方地址。若本机 npm 配置了其他镜像，`--registry` 可确保不会回落到明文 HTTP 源。

发布包不包含 `node_modules/`（由 `.clawhubignore` 排除，避免安全扫描器无法完整分析依赖产物），因此**必须**先执行这一步。

### 2. 配置环境变量

```bash
cp scripts/env.example scripts/.env
chmod 600 scripts/.env   # POSIX 系统建议执行
```

编辑 `scripts/.env`：

```bash
MI_USER_ID=1234567890              # 小米账号 ID（纯数字）
MI_PASS_TOKEN=your_pass_token      # 推荐：使用 passToken
# MI_PASSWORD=your_password        # 备选：密码（可能触发安全验证）
MI_DEVICE_ID=小爱音箱Pro            # 设备名称、miotDID 或 MAC 地址
TRIGGER_PREFIX=请                   # 触发词前缀（默认“请”）
POLL_INTERVAL=1000                 # 轮询间隔（毫秒，默认 1000）
# JEV_API_KEY=sk_xxx               # 可选：启用 Jev 智能判定转发（热词上位替代）
# JEV_LEVEL=balanced               # 判定挡位：loose / balanced / strict
```

- **获取 passToken**：参考 https://github.com/idootop/migpt-next/issues/4
- **查找设备 ID**：运行 `DEBUG=true node scripts/xiaoai-listen.js test`，调试输出会列出设备名称、miotDID 与 MAC。
- `.env` 加载顺序是 `scripts/.env` → 技能根目录 `.env`；也可以用 `XIAOAI_ENV_FILE` 指定任意路径。POSIX 下若 `.env` 可被同组/其他用户读取，CLI 会告警并尽力收紧到 `0600`。

### 3. 检查运行环境

```bash
node scripts/xiaoai-listen.js check
```

该命令只做本地检查（不登录、不使用凭据），输出会话缓存目录、目录权限、缓存文件状态与旧版遗留缓存；发现问题时退出码为 2。**`check` 是只读诊断（1.3.10 起）**：不创建目录、不收紧权限、不修改任何 ACL；目录不存在时仅报告“不存在”（首次运行监听/`speak` 时会自动创建并通过全部校验）。

### 4. 测试连接

```bash
node scripts/xiaoai-listen.js test
```

预期输出（stderr）：

```text
🔌 正在连接小爱音箱...
✅ 连接成功
🔐 缓存文件校验通过：0600
✅ 连接测试通过
```

> Windows 上文件模式不受 POSIX 权限位控制，日志中的 `0666` 仅供参考；目录仍受“必须位于当前用户目录内”的策略保护。

### 5. 启动监听

```bash
node scripts/xiaoai-listen.js
```

stdout 只会输出 JSON 行，例如：

```json
{"type":"message","text":"查一下天气","originalText":"请查一下天气","timestamp":1708070400000,"via":"jev"}
```

后台运行（**不要把 stdout 写入文件**，其中包含语音转写）：

```bash
node scripts/xiaoai-listen.js 2> xiaoai.err &
```

或使用 OpenClaw 进程管理（推荐），由消费方通过管道读取 stdout。

### 6. 清理缓存

```bash
node scripts/xiaoai-listen.js clean
```

会清理当前状态目录的缓存（仅当该目录为空时才删除目录本身），以及旧版本可能遗留的 `scripts/.mi.json`、技能根目录 `.mi.json`、当前目录 `.mi.json` 和旧临时目录缓存。legacy 位置只删除“内容像小米会话缓存”的文件，不会删除目录；遇到符号链接目录或无法判定/清理失败时返回非 0。

## 使用示例

> 以下示例都把语音文本作为**参数数组**传给子进程，不经过 shell，因此引号、分号、反引号等字符不会被解释执行。

### 示例 1：后台监听 + 消息处理

```javascript
const { execFile } = require('node:child_process');
const path = require('node:path');

const scriptPath = path.join(__dirname, 'skills/xiaoai-bridge/scripts/xiaoai-listen.js');
const listener = execFile(process.execPath, [scriptPath], {
  maxBuffer: 1024 * 1024,
});

let buffer = '';
listener.stdout.on('data', (chunk) => {
  buffer += chunk;
  const lines = buffer.split('\n');
  buffer = lines.pop() ?? '';

  for (const line of lines) {
    if (!line.trim()) continue;
    try {
      const msg = JSON.parse(line);
      if (msg.type === 'message') {
        handleVoiceCommand(msg.text);
      }
    } catch (error) {
      console.error('无法解析的监听输出:', line);
    }
  }
});

listener.stderr.on('data', (chunk) => {
  console.error('XiaoAi:', chunk.toString().trim());
});

async function handleVoiceCommand(text) {
  // 高危动作先向用户确认，再执行；不要把转写写入日志文件。
  const response = await processCommand(text);
  await speak(response);
}
```

### 示例 2：直接 TTS 播报

```bash
node scripts/xiaoai-listen.js speak "任务已完成"
```

代码调用：

```javascript
const { execFile } = require('node:child_process');
const path = require('node:path');

const scriptPath = path.join(__dirname, 'skills/xiaoai-bridge/scripts/xiaoai-listen.js');

function speak(text) {
  return new Promise((resolve, reject) => {
    execFile(process.execPath, [scriptPath, 'speak', text], (error) => {
      if (error) reject(error);
      else resolve();
    });
  });
}

await speak('你好，任务已完成');
```

`speak` 的文本上限是 1000 字符，超出会以配置错误退出（退出码 2）。

### 示例 3：触发词过滤与 Jev 判定

**未配置 Jev 时（热词模式）**，Skill 自动过滤触发词前缀（默认“请”），只处理符合条件的消息：

```javascript
// 用户说："请帮我查天气" → 处理，text = "帮我查天气"
// 用户说："今天天气怎么样" → 忽略（无触发词）
```

**配置 `JEV_API_KEY` 后（Jev 判定模式，热词上位替代）**，每条语音由判定模型决定转发与否，无需特定前缀：

```javascript
// 用户说："今天天气怎么样" → 小爱原生可完成，不转发
// 用户说："请帮我写一首关于春天的诗" → 需要外部 AI，转发（text = "帮我写一首关于春天的诗"）
// 用户说："9.9 美元换成人民币是多少" → 超出原生能力，转发
```

自定义触发词（在 `.env` 中配置）：

```bash
TRIGGER_PREFIX=请        # 默认
# TRIGGER_PREFIX=小助手   # 自定义唤醒词
```

如果确实想处理所有语音消息（不推荐，Jev 判定模式下无需如此），必须显式开启：

```bash
TRIGGER_PREFIX=
XIAOAI_ALLOW_UNFILTERED=true
```

### 示例 4：完整集成

```javascript
const { execFile } = require('node:child_process');
const path = require('node:path');

class XiaoAiBridge {
  constructor(scriptPath) {
    this.scriptPath = scriptPath;
    this.listener = null;
    this.buffer = '';
    this.lastTimestamp = Date.now();
  }

  start(onMessage) {
    this.listener = execFile(process.execPath, [this.scriptPath], {
      maxBuffer: 1024 * 1024,
    });

    this.listener.stdout.on('data', (chunk) => {
      this.buffer += chunk;
      const lines = this.buffer.split('\n');
      this.buffer = lines.pop() ?? '';

      for (const line of lines) {
        if (!line.trim()) continue;
        try {
          const msg = JSON.parse(line);
          if (msg.type === 'message' && msg.timestamp > this.lastTimestamp) {
            this.lastTimestamp = msg.timestamp;
            onMessage(msg.text);
          }
        } catch (error) {
          console.error('无法解析的监听输出:', line);
        }
      }
    });

    this.listener.stderr.on('data', (chunk) => {
      console.error('XiaoAi Error:', chunk.toString().trim());
    });
  }

  speak(text) {
    return new Promise((resolve, reject) => {
      execFile(process.execPath, [this.scriptPath, 'speak', text], (error) => {
        if (error) reject(error);
        else resolve();
      });
    });
  }

  stop() {
    if (this.listener) {
      this.listener.kill();
      this.listener = null;
    }
  }
}
```

> 注：`start()` 会把原始语音文本交给 `onMessage`，消费方应自行决定是否落盘（默认不要）。

## 消息格式

监听器输出的每条 stdout 行都是一个独立 JSON 对象：

```json
{
  "type": "message",
  "text": "查一下天气",
  "originalText": "请查一下天气",
  "timestamp": 1708070400000,
  "via": "jev"
}
```

- `text`：已去除触发词前缀、首尾空白后的指令。
- `originalText`：音箱识别到的原始文本。
- `timestamp`：消息时间（毫秒）。
- `via`（v1.3.0+，可选）：转发判定来源，`jev`（Jev 判定转发）、`prefix`（热词触发，含降级路径）。
- 同一轮轮询到的多条消息会按时间从旧到新依次输出，不会漏掉其中较早的消息。

## API 参考

完整 MiGPT-Next API 文档见 [references/migpt-api.md](references/migpt-api.md)。

### 脚本命令

```bash
# 启动监听（默认）
node scripts/xiaoai-listen.js

# TTS 播报文本
node scripts/xiaoai-listen.js speak "要说的话"

# Jev 单条转发判定（需 JEV_API_KEY；输出 JSON 结果，不需要小米配置）
JEV_API_KEY=sk_xxx node scripts/xiaoai-listen.js judge "帮我写一首诗"

# 测试连接（配置 JEV_API_KEY 时附带 Jev 连通性检查）
node scripts/xiaoai-listen.js test

# 检查缓存目录/文件权限（不联网、不登录、不输出凭据）
node scripts/xiaoai-listen.js check

# 清理本地会话缓存（含旧版本遗留位置）
node scripts/xiaoai-listen.js clean

# 调试：查看最近对话（默认隐藏转写原文）
node scripts/debug-fetch.js
PRINT_TRANSCRIPTS=true node scripts/debug-fetch.js

# 帮助 / 版本
node scripts/xiaoai-listen.js --help
node scripts/xiaoai-listen.js --version
```

## 环境变量

| 变量 | 必需 | 说明 |
|------|------|------|
| `MI_USER_ID` | 是 | 小米账号 ID（纯数字，不是手机号或邮箱） |
| `MI_PASS_TOKEN` | 是* | passToken（推荐） |
| `MI_PASSWORD` | 是* | 密码（可能触发安全验证） |
| `MI_DEVICE_ID` | 是 | 设备名称、miotDID 或 MAC |
| `TRIGGER_PREFIX` | 否 | 触发词前缀（默认“请”）；配置 Jev 后仅作为判定信号与降级后备 |
| `XIAOAI_ALLOW_UNFILTERED` | 否 | 设为 `true` 才允许空 `TRIGGER_PREFIX` |
| `JEV_API_KEY` | 否 | Jev 判定平台密钥（`sk_` 开头）；配置即启用智能判定转发（热词上位替代），未配置则仅热词触发。启用即表示同意语音转写文本发送至 Jev 判定服务 |
| `JEV_LEVEL` | 否 | 判定挡位：`loose` / `balanced`（默认）/ `strict` |
| `JEV_DECISION_THRESHOLD` | 否 | 自定义转发概率阈值（0-1），覆盖挡位默认值 |
| `JEV_TIMEOUT_MS` | 否 | 判定请求超时毫秒（默认 8000，范围 1000-30000） |
| `JEV_BASE_URL` | 否 | Jev 服务地址（默认官方地址，仅支持 https） |
| `JEV_MODEL` | 否 | Jev 判定模型 ID（默认 `NeoHorse-Jev-4B`） |
| `POLL_INTERVAL` | 否 | 轮询间隔（毫秒，默认 1000，范围 500-60000） |
| `DEBUG` | 否 | 调试模式（true/false） |
| `XIAOAI_STATE_DIR` | 否 | 会话缓存目录（默认见“默认会话缓存目录”） |
| `XIAOAI_ALLOW_INSECURE_STATE_DIR` | 否 | **有风险**：仅 POSIX——当文件系统无法强制权限时显式放行；必须在进程环境中设置（`.env` 中会被忽略）；Windows 上不被读取（目录与缓存文件的 ACL 校验失败一律硬失败）；不会绕过符号链接、属主不符、公共目录、硬链接等硬性检查，且 `check` 仍返回退出码 2 |
| `XIAOAI_ENV_FILE` | 否 | 指定 `.env` 文件路径 |
| `PRINT_TRANSCRIPTS` | 否 | 仅 `debug-fetch.js`：设为 `true` 打印转写原文 |

\* `MI_PASS_TOKEN` 或 `MI_PASSWORD` 二选一。

## 输出与退出码

| 场景 | stdout | stderr | 退出码 |
|------|--------|--------|--------|
| 监听模式 | 仅 JSON 行 | 状态、错误 | 0 正常退出；1 运行失败 |
| `speak` / `test` | 无（调试日志除外） | 状态、错误 | 0 成功；1 连接失败 |
| `check` | 检查报告（只读诊断，无文件系统副作用） | — | 0 通过；2 需要处理 |
| 配置/权限错误 | 空（`clean`/`check` 除外） | 配置错误说明 | 2 |
| `--help` / `--version` / `clean` | 文本 | 无 | 0（`clean` 清理失败为 2） |

## 故障排查

### 登录失败

症状：`❌ 连接失败: 登录失败`

解决方案：

1. 使用 passToken 替代密码（推荐）
2. 检查 `MI_USER_ID` 是否为纯数字（不是手机号或邮箱）
3. 开启 `DEBUG=true` 查看详细错误信息

### 会话缓存目录校验失败

症状（stderr）中出现以下之一：

- `会话缓存目录属于其他用户…拒绝把凭据写入该目录`
- `无法把会话缓存目录权限收紧到 0700…`
- `会话缓存目录不能是符号链接…`
- `会话缓存目录不在当前用户目录内，无法验证访问控制…`
- `会话缓存目录位于公共目录或其他用户的配置目录内…`
- `会话缓存目录权限过宽…且包含其他文件，拒绝自动修改目录权限…`

解决方案：

1. 先运行 `node scripts/xiaoai-listen.js check` 查看具体原因；
2. 换到一个当前用户私有目录：`export XIAOAI_STATE_DIR="$HOME/.local/state/xiaoai-bridge"`（Windows 用用户目录内路径）；
3. POSIX 上修正属主/权限：`chown -R "$(id -u):$(id -g)" <目录>`、`chmod 700 <目录>`；若目录里有其他文件，`chmod` 需要手动执行，程序不会擅自改动；
4. 仅当确认是单用户环境或文件系统不支持 POSIX 权限时，才考虑在**进程环境**中设置 `XIAOAI_ALLOW_INSECURE_STATE_DIR=true`；写进 `.env` 无效，且该开关不会绕过符号链接、非目录、属主不符、公共目录、硬链接等硬性检查。

### `.env` 中的安全敏感变量被忽略

症状：启动时提示 `已忽略 ... 中的安全敏感变量 ...`。

`LOCALAPPDATA`/`APPDATA`/`USERPROFILE`/`HOME`/`XDG_STATE_HOME`/`ProgramData`/`PUBLIC`/`SystemRoot`/`windir`/`TEMP`/`TMP`/`TMPDIR`/`XIAOAI_ALLOW_INSECURE_STATE_DIR` 只接受进程环境，防止随技能分发的 `.env` 把缓存目录“洗白”到公共位置或静默打开不安全开关。请改用 `set`/`export` 或进程管理器设置。

### `.env` 权限被拒绝

症状：`环境变量文件可被同组或其他用户修改…` 或 `无法收紧环境变量文件权限…`。

请执行 `chmod 600 scripts/.env` 后重试；`.env` 是符号链接时只告警，需自行确认链接目标权限。

### 找不到设备

症状：`❌ 找不到设备`

解决方案：运行以下命令查看所有设备：

```bash
DEBUG=true node scripts/xiaoai-listen.js test
```

使用设备的 `name`、`miotDID` 或 `mac` 作为 `MI_DEVICE_ID`。

### 收不到消息

可能原因：

1. 消息同步延迟（1-2 秒正常）
2. 设备离线或无响应
3. 上次轮询后确实没有新消息
4. 热词模式下，语音消息没有以 `TRIGGER_PREFIX` 开头
5. Jev 判定模式下，判定模型认为该语音应由小爱原生处理（查看 stderr 中 `[Jev]` 日志确认）；若判定过于保守，调低挡位（`JEV_LEVEL=loose`）或设置更低的 `JEV_DECISION_THRESHOLD`
6. Jev 服务不可用且处于冷却期（stderr 会有 `⛔` 降级提示；此时仅热词消息会转发，冷却结束后自动恢复）

### 需要验证码

症状：`❌ 本次登录需要验证码`

解决方案：必须使用 passToken 登录。参考 https://github.com/idootop/migpt-next/issues/4

### 发现遗留 `.mi.json`

如果启动时提示“发现遗留会话文件”，说明旧版本把账号会话写进了技能目录或旧临时目录。请运行 `node scripts/xiaoai-listen.js clean` 清理，不要提交；新版本只会写入通过校验的 `XIAOAI_STATE_DIR`。

## 最佳实践

1. **使用 passToken** - 比密码更稳定，避免安全验证
2. **专用账号 + 数据最小化** - 只授权需要的设备，不要使用主账号
3. **轮询间隔** - 1-2 秒最佳（平衡响应速度和 API 负载）
4. **消息去重** - 跟踪已处理的时间戳，避免重复处理
5. **错误处理** - 监听器已内置指数退避，消费方仍应处理进程退出
6. **长文本分段** - 将长回复分句后多次调用 `speak`，单次不超过 1000 字符
7. **日志脱敏** - 不要记录原始语音转写；确需排查时用 `PRINT_TRANSCRIPTS=true` 临时开启。stderr 已对凭据字段脱敏，但仍不要长期落盘。
8. **高危动作确认** - 语音触发删除、支付、门锁、安防等动作前，先向用户复述并确认
9. **定期轮换** - 定期运行 `check`/`clean`；怀疑泄露时立即更换 passToken

## 相关资源

- MiGPT-Next 项目：https://github.com/idootop/migpt-next
- passToken 获取教程：https://github.com/idootop/migpt-next/issues/4
- API 完整文档：[references/migpt-api.md](references/migpt-api.md)
- 安全问题说明：[SECURITY.md](SECURITY.md)
- 本次安全审计记录：https://clawhub.ai/warm-winter/skills/xiaoai-bridge/security-audit

## 许可证

MIT-0 License，见 [LICENSE](LICENSE)。ClawHub 上发布的所有 Skill 均以 MIT-0 授权。

## 贡献

欢迎提交 Issue 和 Pull Request。

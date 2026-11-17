# MiGPT-Next API 参考

本文档对应依赖 `@mi-gpt/miot@1.2.2`。

## 核心配置

`getMiNA()` / `getMIoT()` 接收的是**扁平**的 `MiServiceConfig`：

```typescript
interface MiServiceConfig {
  did: string;          // 设备名称、miotDID 或 MAC
  userId?: string;      // 小米 ID（纯数字）
  password?: string;    // 账号密码（可能触发安全验证）
  passToken?: string;   // 推荐：passToken
  debug?: boolean;      // 打印设备列表等调试信息
  timeout?: number;     // 请求超时（毫秒，默认 5000）
}
```

> 注意：`{ speaker: { ... } }` 是 MiGPT-Next 上层应用的配置结构，**不是** `@mi-gpt/miot` 的入参，直接传给 `getMiNA()` 会登录失败。

### 使用 passToken 登录（推荐）

```typescript
import { getMiNA } from "@mi-gpt/miot";

const mina = await getMiNA({
  userId: "你的小米账号ID",
  passToken: "你的passToken",
  did: "小爱音箱设备ID",
});
```

### 使用密码登录（可能触发风控）

```typescript
const mina = await getMiNA({
  userId: "你的小米账号ID",
  password: "你的密码",
  did: "小爱音箱设备ID",
});
```

## 会话缓存（重要安全提示）

`@mi-gpt/miot` 登录成功后会执行等价于下面的逻辑：

```typescript
const kConfigFile = ".mi.json";
store[service] = account;         // account 含 passToken / serviceToken / ssecurity
await writeJSON(kConfigFile, store); // 相对 process.cwd() 解析
```

也就是说：

- `.mi.json` 会写到**进程当前工作目录**，不是包目录；
- 文件里包含可直接接管小米账号的会话凭据；
- 在 Git 仓库根目录直接运行脚本，凭据就会出现在仓库里，极易被提交。

本 Skill 的处理方式（`@mi-gpt/miot@1.2.2` 仍把 `.mi.json` 写死在 `process.cwd()`）：

1. 登录前 `process.chdir()` 到通过校验的私有状态目录（默认：Windows `%LOCALAPPDATA%\xiaoai-bridge`、macOS `~/Library/Application Support/xiaoai-bridge`、其它 `$XDG_STATE_HOME/xiaoai-bridge` 或 `~/.local/state/xiaoai-bridge`）；
2. 目录必须是真实目录（拒绝符号链接）、属主为当前用户（POSIX）、权限收紧到 0700 并复验（仅对空目录/仅含 `.mi.json` 的专用目录自动收紧）；Windows 上公共目录/其他用户 profile 一律拒绝；
3. 登录前以 0600 独占预创建 `.mi.json`（上游 `writeFile` 不会改变已存在文件的权限），并清理未知顶层键与 `__proto__`；登录后复验类型/属主/权限/硬链接（含 NTFS）、非空内容与 `dev/ino`；
4. 任一校验失败即中止（退出码 2），不会把凭据写入可疑目录；
5. `node scripts/xiaoai-listen.js check` 本地检查（不登录、不使用凭据），`clean` 一键删除（含旧版本遗留位置，不删除非专用目录）。

`XIAOAI_ALLOW_INSECURE_STATE_DIR=true` 只用于“权限无法强制/ACL 无法验证”的场景，不能绕过符号链接、非目录、属主不符等硬性检查。

如果你在自己的项目里直接使用 `@mi-gpt/miot`，请自行做同样的隔离，并把 `.mi.json` 加入 `.gitignore`。

## 底层 API

### 获取消息

```typescript
import { getMiNA } from "@mi-gpt/miot";

const mina = await getMiNA(config);

const conversations = await mina.getConversations({
  limit: 10,
  timestamp: Date.now(),
});
```

返回结构（记录按时间**新 → 旧**排列，且包含游标消息本身）：

```typescript
interface MiConversations {
  records: Array<{
    time: number;        // 时间戳（毫秒）
    query: string;       // 用户说的话
    answers: Array<{
      tts?: { text: string }; // 小爱的回复
    }>;
  }>;
}
```

### TTS 播放

```typescript
await mina.play({ text: "你好" });
await mina.play({ url: "https://example.com/audio.mp3" });
```

### 音量与播放控制

```typescript
const volume = await mina.getVolume();
await mina.setVolume(50);   // 0-100
await mina.pause();
await mina.playOrPause();
await mina.stop();
```

### 设备列表

```typescript
const devices = await mina.getDevices();
```

`debug: true` 时，`getMiNA()` 在匹配设备前也会把设备列表打印出来。

## 轮询模式

直接照抄「遍历时推进游标」的写法会漏消息：接口返回新 → 旧，第一次循环就把游标推到最新，后面的新消息全部被跳过。正确做法是先收集、再统一推进：

```typescript
let lastTimestamp = Date.now();

while (true) {
  const conversations = await mina.getConversations({
    limit: 10,
    timestamp: lastTimestamp,
  });

  const since = lastTimestamp;
  let newest = lastTimestamp;
  const messages: string[] = [];

  for (const record of conversations?.records ?? []) {
    if (record.time > newest) newest = record.time;
    if (record.time > since) messages.push(record.query);
  }

  lastTimestamp = newest;
  messages.reverse(); // 按时间从旧到新处理

  for (const message of messages) {
    console.log(`新消息：${message}`);
  }

  await new Promise((resolve) => setTimeout(resolve, 1000));
}
```

## 环境变量配置

```bash
MI_USER_ID=1234567890
MI_PASS_TOKEN=your_pass_token_here
MI_DEVICE_ID=小爱音箱Pro
```

## 常见问题

### 获取 passToken

访问：https://github.com/idootop/migpt-next/issues/4

### 获取设备 ID

```typescript
const mina = await getMiNA({
  userId: "...",
  passToken: "...",
  did: "任意设备名",
  debug: true, // 会打印设备列表
});
```

### 登录失败

- 触发风控：改用 passToken
- 账号错误：`userId` 是数字，不是手机号
- 设备错误：开启 debug 查看设备列表
- 缓存冲突：删除 `XIAOAI_STATE_DIR` 下的 `.mi.json` 后重试

# 代码级红旗模式

每个模式包含：描述、检测关键词/正则、严重程度、误报指南和真实案例。

## 1. 出站数据外泄

**含义：** 代码将本地数据发送到外部服务器。

**检测关键词：**
```
curl, wget, fetch, http.get, https.get, requests.post, requests.get,
axios, got, node-fetch, urllib, httplib, XMLHttpRequest,
nc (netcat), socat, /dev/tcp, /dev/udp
```

**严重程度：** 🔴 如发送本地数据到外部；🟡 仅获取外部数据

**误报：** 天气技能调用 `api.openweathermap.org` 是预期的。"文件整理"技能调用未知 IP 则不是。

**核心问题：** 目的地址域名与技能用途一致？请求中是否包含本地数据？

## 2. 凭证 / 环境变量访问

**含义：** 代码读取环境变量、.env 文件或凭证存储。

**检测关键词：**
```
process.env, os.environ, os.getenv, $ENV, ${ENV},
dotenv, .env, config.json, credentials, keychain,
grep -i key, grep -i token, grep -i secret, grep -i password
```

**严重程度：** 🔴 配合网络发送；🟡 仅为自己 API 使用

**误报：** Tavily 技能读 `TAVILY_API_KEY` 调用 Tavily API → 预期。

**核心问题：** 凭证访问与技能服务匹配？凭证离开本地环境？

## 3. 超出范围的文件系统访问

**含义：** 代码读写预期工作目录之外的文件。

**检测关键词：**
```
~/.ssh, ~/.aws, ~/.config, ~/.gnupg, /etc/ssh, /etc/shadow,
/etc/passwd, ~/.openclaw, ~/.claude, ~/.cursor, /proc/,
expanduser, os.path.join("..", ), path.resolve(".."),
readFileSync, writeFileSync, open(, fs.read, fs.write
```

**严重程度：** 🔴 敏感目录；🟡 其他超出范围访问

**误报：** Git 技能读 `~/.gitconfig` → 预期；天气技能读 `~/.ssh/` → 恶意。

## 4. Agent 身份 / 记忆文件访问

**含义：** 代码访问 agent 特定的 identity 或记忆文件。

**检测关键词：**
```
MEMORY.md, USER.md, SOUL.md, IDENTITY.md, AGENTS.md, TOOLS.md,
paired.json, sessions.json, .claude/settings,
workspace/memory/, memory/, CLAUDE.md,
~/.claude, /proc/self/environ
```

**严重程度：** 🔴 始终——这些文件包含个人信息

**误报：** 几乎为零。没有任何第三方技能需要访问 agent identity 或记忆文件。

## 5. 动态代码执行

**含义：** 代码从外部输入在运行时构造并执行代码。

**检测关键词：**
```
eval(, exec(, Function(, execSync(, child_process,
subprocess.run, subprocess.Popen, os.system, os.popen,
compile(, __import__, importlib,
new Function, setTimeout(string), setInterval(string)
```

**严重程度：** 🔴 如输入来自外部/不可信源；🟡 如输入是硬编码/安全的

## 6. 权限提升

**含义：** 代码尝试提升权限或修改系统安全设置。

**检测关键词：**
```
sudo, su -, doas, pkexec,
chmod 777, chmod +s, chown root, setuid, setgid,
visudo, /etc/sudoers,
capabilities, cap_sys_admin, cap_net_raw
```

**严重程度：** 🔴 始终——第三方技能不应需要 root 权限

## 7. 持久化机制

**含义：** 代码建立持久化机制以在重启后会话后存活。

**检测关键词：**
```
crontab, /etc/cron, at -f, systemctl enable,
~/.config/autostart, ~/.bashrc, ~/.zshrc, ~/.profile, ~/.bash_profile,
/etc/rc.local, /etc/init.d, launchd, plist,
LoginItems, com.apple.loginitems,
~/Library/LaunchAgents
```

**严重程度：** 🔴 始终——在技能语境中持久化是恶意意图指标

## 8. 运行时包安装（次级下载）

**含义：** 代码在执行时下载并安装额外包，而非预先声明。

**检测关键词：**
```
npm install, npm i, npx, yarn add, pnpm add,
pip install, pip3 install, easy_install,
cargo install, go install, gem install, apt install, apt-get install,
brew install, pacman -S, dnf install,
curl | sh, curl | bash, wget | sh, wget | bash
```

**严重程度：** 🔴 始终——实际载荷在审查时不可见

**核心问题：** 如果技能需要依赖，应预先声明并可审计，而非静默运行时安装。

## 9. 代码混淆

**含义：** 代码被故意弄得难以阅读或分析。

**检测模式：**
```
- Minified JavaScript (单行，无空白，单字母变量)
- Base64 编码字符串被解码后执行
- Hex 编码载荷
- 字符串拼接构建命令: "cu" + "rl" + " htt" + "p://..."
- Unicode 转义序列混淆 ASCII
- 压缩/打包脚本 (eval(unescape(...)))
- ROT13 或自定义编码
```

**严重程度：** 🔴 如混淆后执行代码；🟡 如为构建产物（如 webpack bundle）

## 10. 进程 / 系统侦察

**含义：** 代码检查运行中的进程、网络状态或系统配置。

**检测关键词：**
```
ps aux, ps -ef, pgrep, pidof,
/proc/PID/environ, /proc/PID/cmdline, /proc/PID/maps,
ss -tlnp, netstat, lsof -i, nmap,
cat /etc/os-release, uname -a, hostnamectl,
systemctl list-units, journalctl
```

**严重程度：** 🟡 基本系统信息；🔴 进程环境泄露或网络扫描

**误报：** 监控技能检查 `df -h` 磁盘使用是预期的。读取 `/proc/PID/environ` 几乎从不合理。

## 11. 浏览器会话 / Cookie 访问

**含义：** 代码访问浏览器存储、cookies 或会话数据。

**检测关键词：**
```
document.cookie, localStorage, sessionStorage, IndexedDB,
chrome.cookies, browser.cookies,
Cookie:, Set-Cookie:,
~/.config/google-chrome, ~/Library/Application Support/Google/Chrome,
~/.mozilla/firefox, ~/Library/Application Support/Firefox,
Login Data, Cookies (SQLite files)
```

**严重程度：** 🔴 始终——浏览器会话数据高度敏感

## 使用说明

1. **一个红旗 ≠ 自动拒绝。** 上下文很重要。单独的 `process.env.MY_SKILL_API_KEY` 不同于 `env | grep -i secret`。

2. **组合放大风险。** 凭证访问 + 网络发送 > 单独任何一项。

3. **检查完整执行路径。** 读取凭证的函数可能不自己发送，但会传给另一个发送函数。

4. **非代码文件也是攻击面。** 始终交叉参考 [social-engineering.md](social-engineering.md) 检查文档中的提示注入。

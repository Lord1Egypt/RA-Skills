# 危险命令列表

## 🔴 致命风险 (扣 30 分)

| 命令 | 风险描述 | 检测文件 |
|------|----------|----------|
| `rm -rf /` | 根目录删除，毁灭性操作 | .sh, .bash |
| `rm -rf ~` | 用户主目录删除，丢失所有数据 | .sh, .bash |
| `rm -rf $HOME` | 同上，使用环境变量 | .sh, .bash |
| `curl \| bash` | 远程脚本执行，完全不可控 | .sh, .bash |
| `wget -O- \| sh` | 远程脚本执行，完全不可控 | .sh, .bash |
| `curl https://... \| sh` | 同上 | .sh, .bash |
| `wget https://... \| bash` | 同上 | .sh, .bash |
| `passwd` | 修改用户密码 | .sh, .py, .js |

## 🟠 高风险 (扣 20 分)

| 命令/模式 | 风险描述 | 检测文件 |
|-----------|----------|----------|
| `chmod 777` | 权限过于宽松 | .sh, .bash |
| `eval $var` | 动态代码执行 | .sh, .bash |
| `eval "$(...)"` | 同上 | .sh, .bash |
| `elevated: true` | 要求 root 权限 | .yaml, .yml, SKILL.md |
| `sudo` | 提权操作 | .sh, .bash, .py |
| `chown` | 修改文件所有权 | .sh, .bash |
| `chmod +s` | 设置 SUID 位 | .sh, .bash |
| `> /dev/sda` | 直接写入设备 | .sh, .bash |
| `mkfs` | 格式化操作 | .sh, .bash |
| `:(){:|:&};:` | Fork 炸弹 | .sh, .bash |
| `dd if=/dev/zero` | 磁盘写入耗尽 | .sh, .bash |
| JavaScript `eval()` | 动态代码执行 | .js, .mjs |
| JavaScript `exec()` | 子进程执行 | .js, .mjs |
| JavaScript `Function()` | 动态函数创建 | .js, .mjs |
| JavaScript `spawn`/`execSync` | 子进程执行 | .js, .mjs |
| Python `eval()` | 动态代码执行 | .py |
| Python `exec()` | 动态代码执行 | .py |
| Python `subprocess` | 子进程执行 | .py |
| Python `os.system()` | Shell 执行 | .py |

## 🟡 中风险 (扣 10 分)

| 模式 | 风险描述 | 检测文件 |
|------|----------|----------|
| `vault/` | 访问敏感存储 | 所有 |
| `credentials/` | 访问凭据目录 | 所有 |
| `--password` | 命令行传递密码 | .sh, .bash |
| `-p ` | 密码参数 | .sh, .bash |
| API_KEY | 硬编码 API Key | 所有 |
| `wget --post-data` | POST 发送敏感数据 | .sh, .bash |
| `curl -d` | POST 发送敏感数据 | .sh, .bash |
| `curl -X POST` | 同上 | .sh, .bash |
| `.env` | 环境变量文件 | 所有 |
| `~/.ssh/` | SSH 密钥目录 | 所有 |
| `/etc/passwd` | 系统用户文件 | .sh, .bash |
| `$VAR` / `${VAR}` | 环境变量读取 | .sh, .bash |
| `curl` / `wget` | 网络请求 | .sh, .bash |
| `fetch` / `axios` | HTTP 请求 | .js, .mjs |
| `writeFile` / `fs.write` | 文件写入 | .js, .mjs |
| `> file` / `>> file` | Shell 重定向写入 | .sh, .bash |
| `open(..., 'w')` | Python 文件写入 | .py |
| `requests.` / `urllib.` | Python HTTP 请求 | .py |

## 🟢 低风险 (扣 3-5 分)

| 模式 | 风险描述 | 检测文件 |
|------|----------|----------|
| `readFile` | 文件读取 | .js, .mjs |
| `open(..., 'r')` | Python 文件读取 | .py |
| 环境变量引用 (注释除外) | 变量使用 | .sh, .bash |

## 检测优先级

1. 先检测致命风险 - 发现立即终止扫描
2. 再检测高风险 - 累计扣分
3. 最后检测中风险 - 警告但不阻断

## 按语言分类的检测模式

### Shell/Bash (.sh, .bash)

```bash
# 致命
rm\s+-rf\s+[/~$HOME]
curl\s+.*\|\s*(bash|sh)
wget\s+.*\|\s*(bash|sh)
passwd

# 高风险
chmod\s+777
elevated:\s*true
eval\s+
sudo\s+
chown\s+

# 中风险
vault/|credentials/
API_KEY|apikey|password
curl\s+|wget\s+
\$\{?[A-Za-z_]
>.*[/~]|>>.*[/~]
```

### JavaScript (.js, .mjs)

```javascript
// 高风险
eval\s*\(|
exec\s*\(|
Function\s*\(|
spawn\s*\(|
execSync\s*\(|
execFileSync\s*\(

// 中风险
writeFile\s*\(|
writeFileSync\s*\(|
createWriteStream|
\.write\s*\(|
axios\.|
fetch\s*\(
```

### Python (.py)

```python
# 高风险
eval\s*\(|
exec\s*\(|
subprocess\.|
os\.system\s*\(

# 中风险
open\s*\([^)]*,\s*['"]w['"]|
\.write\s*\(|
requests\.|
urllib\.

# 低风险
open\s*\([^)]*,\s*['"]r['"]
```

## 评分算法

```
初始分数: 100

扣分规则:
- 致命风险: -30 分/个
- 高风险:   -20 分/个
- 中风险:   -10 分/个
- 低风险:   -3~5 分/个

加分规则:
- 官方来源 (clawhub): +10 分
- 风险数量 > 5 个: 额外 -5 分
- 风险数量 > 10 个: 额外 -10 分

最终分数范围: 0-100
```

## 正则匹配规则速查

```bash
# 致命
rm\s+-rf\s+[/~$HOME]
curl\s+.*\|\s*(bash|sh)
wget\s+.*\|\s*(bash|sh)
passwd

# 高风险
chmod\s+777
elevated:\s*true
eval\s+|exec\s*\(|Function\s*\(
spawn|execSync|execFileSync
subprocess\.|os\.system\s*\(
sudo\s+|chown\s+

# 中风险
vault/|credentials/
api[_-]?key|password|token|secret
curl|wget|fetch|axios
writeFile|open.*w|>\s*/|>>\s*/
\$\{?[A-Za-z_]
requests\.|urllib\.
```

# 检测规则参考文档

## 规则分类

### EXFIL（数据外泄）
检测可能将敏感数据发送到外部的行为。

| 规则 ID | 规则 | 风险 | 说明 |
|---------|------|------|------|
| E01 | `credentials/` | critical | 访问凭证目录 |
| E02 | `vault/(?!crypto/)` | critical | 访问 vault（游戏钱包除外） |
| E03 | `0x[a-f0-9]{64}` | critical | 私钥地址 |
| E04 | `process.env.(AWS_|AZURE_|STRIPE_)` | critical | API 密钥 |
| E05 | `net.createServer` | critical | 网络服务器后门 |
| E06 | `http.createServer` | high | HTTP 服务器 |
| E07 | `Buffer.toString.*base64.*http` | high | Base64 外传数据 |
| E08 | `fs.readFile.*\.ssh` | critical | 读取 SSH 密钥 |

### INJECTION（恶意注入）
检测命令注入、代码注入等攻击。

| 规则 ID | 规则 | 风险 | 说明 |
|---------|------|------|------|
| I01 | `curl.*\|.*bash` | critical | 远程脚本执行 |
| I02 | `npx\|npm exec` | critical | 包管理器命令注入 |
| I03 | `eval\(` | critical | eval 动态执行 |
| I04 | `new Function\(` | critical | Function 构造器 |
| I05 | `ignore.*previous.*instructions` | high | 提示注入 |
| I06 | `jailbreak\|bypass.*safety` | critical | 越狱攻击 |
| I07 | `DAN\|do anything now` | critical | DAN 越狱模式 |
| I08 | `curl.*http` | high | 远程下载执行 |

### OBFUSCATION（混淆隐藏）
检测代码混淆和隐藏技术。

| 规则 ID | 规则 | 风险 | 说明 |
|---------|------|------|------|
| O01 | `Buffer.from.*base64` | high | Base64 混淆 |
| O02 | `atob\(\|btoa\(` | high | Base64 编解码 |
| O03 | `\\x[0-9a-f]{2}` | high | Hex 编码混淆 |
| O04 | `if.*NODE_ENV.*production` | high | 条件触发 |

### TROJAN（木马/后门）
检测木马和后门特征。

| 规则 ID | 规则 | 风险 | 说明 |
|---------|------|------|------|
| T01 | `child_process.spawn.*sh.*-c` | critical | Shell 命令注入 |
| T02 | `process.kill.*all` | high | 进程终止 |
| T03 | `fs.unlink.*system` | critical | 系统文件删除 |
| T04 | `setInterval.*1000.*60.*24` | medium | 长时间定时任务 |

---

## 评分规则

| 风险等级 | 扣分 | 说明 |
|----------|------|------|
| critical | -25~30 | 致命风险，禁止运行 |
| high | -15~20 | 高风险，建议审查 |
| medium | -10~15 | 中风险，可疑 |
| low | -5~10 | 低风险，通过 |

---

## JSONL 输出格式

```json
{
  "skill": "example-skill",
  "category": "EXFIL",
  "rule_id": "E01",
  "rule": "credentials/",
  "level": "critical",
  "file": "index.js",
  "snippet": "require('vault/credentials/api.json')",
  "line": 42
}
```

---

## Python 检测规则

### INJECTION（命令/代码注入）

| 规则 ID | 规则 | 风险 | 说明 |
|---------|------|------|------|
| P01 | `subprocess.run/Popen/exec` | critical | 子进程命令执行 |
| P02 | `os.system()`, `popen()` | critical | 系统命令执行 |
| P03 | `eval()`, `exec()` | critical | 动态代码执行 |
| P04 | `__import__` | medium | 动态模块导入 |

### TROJAN（木马/后门）

| 规则 ID | 规则 | 风险 | 说明 |
|---------|------|------|------|
| P05 | `os.remove`, `os.unlink`, `shutil.rmtree` | critical | 文件删除 |
| P06 | `os.kill`, `signal.kill` | high | 进程终止 |

### EXFIL（数据外泄）

| 规则 ID | 规则 | 风险 | 说明 |
|---------|------|------|------|
| P07 | `requests.get/post/put/delete` | high | HTTP 请求（潜在数据外传） |
| P08 | `urllib.request`, `urllib3` | high | URL 请求库 |
| P09 | `http.client` | high | HTTP 客户端 |
| P10 | `os.getenv(...KEY/SECRET/TOKEN/PASS)` | critical | 凭证访问 |

### OBFUSCATION（混淆隐藏）

| 规则 ID | 规则 | 风险 | 说明 |
|---------|------|------|------|
| P11 | `base64.b64decode`, `a85decode` | high | Base64 解码混淆 |


---

## Shell 检测规则

### INJECTION（命令/脚本注入）

| 规则 ID | 规则 | 风险 | 说明 |
|---------|------|------|------|
| S01 | `curl/wget \| bash` | critical | 远程脚本执行 |
| S02 | `curl.*\.sh$`, `wget.*-O-` | critical | 下载执行远程脚本 |
| S03 | `eval $()` | critical | 动态命令执行 |
| S04 | `exec <cmd>` | critical | 命令替换执行 |

### TROJAN（木马/后门）

| 规则 ID | 规则 | 风险 | 说明 |
|---------|------|------|------|
| S05 | `rm -rf`, `rm -r -f` | critical | 递归删除文件 |
| S06 | `rm -rf ${var}` | critical | 变量路径递归删除 |
| S07 | `kill -9`, `pkill` | high | 强制终止进程 |

### EXFIL（数据外泄）

| 规则 ID | 规则 | 风险 | 说明 |
|---------|------|------|------|
| S08 | `.ssh/`, `.aws/`, `.kube/` | critical | 敏感目录访问 |

### OBFUSCATION（混淆隐藏）

| 规则 ID | 规则 | 风险 | 说明 |
|---------|------|------|------|
| S09 | `>/dev/null 2>&1 &` | high | 隐藏后台执行 |
| S10 | `nohup` | medium | 持久化后台进程 |

---

## 支持的文件类型

| 类型 | 扩展名 | 状态 |
|------|--------|------|
| JavaScript | `.js` | ✅ 支持 |
| TypeScript | `.ts` | ✅ 支持 |
| Python | `.py` | ✅ 支持 |

---

## 补充检测规则（扩展威胁）

### EXFIL（扩展）

| 规则 ID | 规则 | 风险 | 说明 |
|---------|------|------|------|
| E09 | `mysql/postgres/mongodb/redis/sqlite3` | high | 数据库连接 |
| E10 | `writeFile.*\.env|config-write` | high | 配置文件写入 |
| E11 | `ethers.Wallet|web3.eth.accounts` | high | 加密货币钱包访问 |
| E12 | `net.listen|server.listen` | high | 端口监听 |
| E13 | `socks-proxy|tor-proxy` | high | 代理/TOR 使用 |
| E14 | `simple-git|isomorphic-git` | high | Git 仓库操作 |
| E15 | `downloadFile|curl.*-O|wget.*-O` | high | 文件下载 |

### INJECTION（扩展）

| 规则 ID | 规则 | 风险 | 说明 |
|---------|------|------|------|
| I09 | `\`[^\`]*\` | critical | 反引号命令注入 |
| I10 | `os.platform\|os.type\|os.release` | medium | 系统平台探测 |
| I11 | `crypto.createCipher` | medium | 恶意加密操作 |

### TROJAN（扩展）

| 规则 ID | 规则 | 风险 | 说明 |
|---------|------|------|------|
| T08 | `adm-zip\|archiver\|yauzl` | medium | zip 解压路径穿越 |
| T09 | `writeFile.*\$` | high | 任意路径文件写入 |
| T10 | `JSON.parse.*user\|eval.*JSON` | high | 反序列化漏洞 |


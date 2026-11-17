# 脱敏与参数化替换规则

打包技能时最常见的两类事故：**路径写死**导致换台机器跑不起来，**凭据写死**导致泄漏。
本文件给出逐项替换映射与代码范式，直接照抄即可。

---

## 一、绝对路径

### 替换映射表

| 原写法 | 替换为 | 适用场景 |
|---|---|---|
| `C:\Users\<用户名>\...` | 用户目录：`Path.home()` / `os.path.expanduser("~")` | 定位用户级配置、输出 |
| `D:\某项目\某技能\...` | 技能自身：`Path(__file__).resolve().parent` 逐级上溯 | 定位技能内的脚本、模板、资源 |
| `\\服务器\共享\...` | 配置项 + 环境变量，文档里写占位符 | 内网资源必须由使用者填 |
| `/home/xxx/`、`/Users/xxx/` | 同「用户目录」 | macOS / Linux |
| 写死的盘符输出目录 | 命令行参数 `--out`，默认落到当前工作目录 | 输出位置 |
| 写死的浏览器/工具路径 | 候选列表探测 + 探测结果缓存进配置文件 | 环境相关可执行文件 |

### 文档里怎么写

不要贴自己机器的真实路径。用可读的占位形式：

| 场景 | 推荐写法 |
|---|---|
| 技能自身文件 | `<技能目录>/scripts/run.py` |
| 用户级配置 | `~/.workbuddy/<name>_config.json` |
| 项目内位置 | `<项目目录>/.workbuddy/skills/<name>/` |
| Windows 环境变量 | `%USERPROFILE%`、`%TEMP%` |
| 需使用者填写 | `<你的密码>`、`<你的工号>` |

### 代码范式（Python）

```python
import os
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent   # 技能根目录
USER_HOME  = Path(os.path.expanduser("~"))            # 用户主目录
CONFIG_PATH = USER_HOME / ".workbuddy" / "mycfg.json" # 用户级配置

# 输出位置：参数优先，其次环境变量，最后落到用户目录
out = args.out or os.environ.get("MY_OUT") or str(USER_HOME / "my_output")
```

要点：

- `Path(__file__).resolve()` 会解析符号链接，得到的路径可直接做相对上溯
- 在 Windows 上 `os.path.expanduser("~")` 与 `Path.home()` 等价，优先用后者
- 拼接一律用 `/` 运算符或 `os.path.join`，不要用字符串相加
- 技能内的资源引用走 `SKILL_ROOT / "assets" / "xxx.png"`，而不是写死绝对路径

### 代码范式（Node.js）

```js
import { fileURLToPath } from "node:url";
import path from "node:path";
import os from "node:os";

const SKILL_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const CONFIG_PATH = path.join(os.homedir(), ".workbuddy", "mycfg.json");
```

### 允许保留的例外

以下情形留绝对路径是**合理默认值**，不是硬编码。放行标记**只用于脚本文件**
（`.py` / `.js` / `.sh`），加在被判定的那一行行尾并注明理由：

> ⚠️ **标记必须加在被判定的那一行行尾** —— 审计是**按行匹配**的。把标记写到换行后的下一行
> **完全不生效**，P1 照样报。典型踩法：一条长命令折成两行，标记放第二行末尾。
>
> 🚫 **`.md` 文档里禁止用注释形式放行**。文档注释渲染后不可见，第三方安全审计读到
> 「让审计跳过」的隐藏指令，会判定为提示注入 —— 实测已使技能在 SkillHub 被判 `suspicious`
> （体检规则「文档放行标记」已能自动拦下这一类）。文档里遇到确需放行的例外，只有两种正当做法：
> ① 改写正文，让它不再命中该规则；② 在技能根目录的 `.skillignore` 里写 `rule:规则名`，
> 并在正文显式说明理由 —— 两者都是**可见**的、可被审阅的。
>
> 🔁 **改写时别把触发规则的字面量原样抄进正文**。典型：CHANGELOG 里写「原来是
> `把系统命令目录前置到 PATH` 的那条命令，命中了引用系统目录」，为了说清楚就把那条命令
> 一字不差地抄了一遍 —— 于是**换个地方重新踩一次**，体检立刻报回 P1。说明原因时用描述性写法
> （去掉前导斜杠、写「Git 自带的 `usr/bin`」），或干脆只说「那行原本带系统命令目录的绝对路径」。

```python
# 取临时目录时回退到系统目录
tmp = os.environ.get("TEMP") or r"C:\Windows\Temp"   # skill-audit: ignore 系统兜底默认值

# 浏览器探测候选列表（本就该多候选遍历）
CANDIDATES = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"]  # skill-audit: ignore 探测候选
```

---

## 二、凭据

### 三层结构

```
技能包内（可分发）      用户机器上（不外传）
─────────────────       ─────────────────────
config/x.example.json   ~/.workbuddy/<name>_config.json
  ├ 字段名留全            ├ 真实值
  └ 敏感值留空            └ 权限收紧，不进版本控制
```

### 替换映射表

| 原写法 | 替换为 |
|---|---|
| 脚本里写死账号密码 | 首次运行 `setup.py` 交互式录入，`getpass` 不回显 + 二次确认 |
| 写死 API Key / Token | 环境变量优先，未设置时读用户配置文件，都没有则提示运行初始化 |
| 配置样例里填了真值 | 敏感字段改空字符串，旁边加注释说明去哪申请 |
| 命令行传密码 | 仅限自动化场景，且文档里注明会进入命令历史 |

### 代码范式（Python）

```python
import json
import os
from getpass import getpass
from pathlib import Path

CONFIG_PATH = Path(os.path.expanduser("~")) / ".workbuddy" / "mycfg.json"

def load_config():
    cfg = {}
    if CONFIG_PATH.exists():
        cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    # 环境变量优先，便于临时切换
    for key, env in (("token", "MY_TOKEN"), ("user", "MY_USER")):
        if os.environ.get(env):
            cfg[key] = os.environ[env]
    return cfg

def do_init():
    user = input("账号: ").strip()
    pwd = getpass("密码（不回显）: ")
    if pwd != getpass("再输一次: "):
        raise SystemExit("两次输入不一致")
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps({"user": user, "password": pwd}, ensure_ascii=False, indent=2),
                           encoding="utf-8")
    CONFIG_PATH.chmod(0o600)
```

要点：

- 禁止把凭据打进日志、异常信息、命令行回显
- 用户配置文件本身不能被一起打包（放在技能目录之外天然满足）
- `chmod(0o600)` 在 Windows 上是空操作但无害，跨平台保留
- 二级确认只对「首次写入」做，重复运行不必重复确认

### 空模板长什么样

```json
{
  "user": "",
  "password": "",
  "api_endpoint": "",
  "timeout_seconds": 30,
  "notes": "把本文件复制到 ~/.workbuddy/mycfg_config.json 后填写前三项"
}
```

字段名 + 注释留全，值留空——别人 `cp` 一下就懂该填什么。

### 泄漏之后

改代码 ≠ 解决问题。凭据一旦进过版本历史、发给过别人、上传过任何外部服务，必须**轮换**：

1. 到签发方作废旧凭据、生成新的
2. 清理版本历史或至少确认仓库不再可达旧提交
3. 检查该凭据关联的所有系统，确认没有异常调用记录

---

## 三、依赖声明

| 类型 | 要写进 SKILL.md 的内容 |
|---|---|
| Python 包 | 包名清单 + 安装命令；提供 setup 脚本一键装 |
| Node 包 | 包名清单 + `npm install`；提供 package.json |
| 外部可执行文件 | 安装方式 + 检测方法 + 缺失时的行为（报错退出而非静默失败） |
| 中文字体 | 字体回退顺序 + 缺失时的表现说明 |
| 系统权限 | 需要哪些权限、为什么需要 |

外部依赖的检测与失败处理范式：

```python
import shutil
import sys

def require(tool: str, hint: str) -> str:
    exe = shutil.which(tool)
    if not exe:
        sys.stderr.write("缺少依赖: %s\n安装方式: %s\n" % (tool, hint))
        raise SystemExit(3)
    return exe
```

宁可**明确报错并给出安装指引**，也不要静默降级——使用者看到的是「功能不好用」，而不是「我少装了个东西」。

---

## 四、自检命令

```bash
# 全量体检
python scripts/audit_skill.py <技能目录>

# 只看要命的
python scripts/audit_skill.py <技能目录> --hide-p2

# 机器可读
python scripts/audit_skill.py <技能目录> --json

# 打包前先看清单，不落盘
python scripts/pack_skill.py <技能目录> --dry-run
```

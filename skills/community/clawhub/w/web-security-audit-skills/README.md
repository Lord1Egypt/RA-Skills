# Web Security Audit Skill

> Web 应用静态代码安全审计工具,覆盖 **PHP / Java / Python / Go** 四大语言,内置 60+ 检测规则,自动生成包含漏洞详情与可运行 PoC 的 `Security.md` 报告。

## 目录

- [功能特性](#功能特性)
- [漏洞覆盖范围](#漏洞覆盖范围)
- [项目结构](#项目结构)
- [环境要求](#环境要求)
- [快速开始](#快速开始)
- [命令行参数](#命令行参数)
- [工作流程](#工作流程)
- [检测规则参考](#检测规则参考)
- [报告示例](#报告示例)
- [免责声明](#免责声明)

---

## 功能特性

- **多语言支持**:PHP、Java、Python、Go 源码自动识别与扫描
- **60+ 检测规则**:基于正则模式匹配,覆盖 12 类常见 Web 漏洞
- **自动语言检测**:根据文件后缀智能识别语言,无需手动指定
- **结构化报告**:生成 `Security.md`,包含漏洞位置、根因分析、修复建议与 PoC 脚本
- **可运行 PoC**:每类漏洞附带 Python 3 验证脚本,便于复现与验证
- **多格式输出**:支持 Markdown 报告与 JSON 摘要
- **智能排除**:自动跳过 `node_modules`、`vendor`、`.git`、`__pycache__` 等无关目录

---

## 漏洞覆盖范围

| # | 漏洞类别 | CWE | 严重级别 | 说明 |
|---|---------|-----|---------|------|
| 1 | SQL 注入 | CWE-89 | Critical | SQL 查询拼接用户输入,未使用参数化查询 |
| 2 | 命令注入 / RCE | CWE-78 | Critical | 用户输入传入 `system()`、`exec()`、`subprocess` 等函数 |
| 3 | 跨站脚本攻击 (XSS) | CWE-79 | High | 用户输入未转义直接输出到 HTML |
| 4 | 不安全反序列化 | CWE-502 | Critical | `unserialize()`、`pickle.loads()`、`readObject()` 处理用户数据 |
| 5 | 服务端请求伪造 (SSRF) | CWE-918 | High | 用户可控 URL 用于服务端 HTTP 请求 |
| 6 | XML 外部实体 (XXE) | CWE-611 | High | XML 解析未禁用外部实体 |
| 7 | 路径遍历 | CWE-22 | High | 用户输入用于文件路径拼接 |
| 8 | 服务端模板注入 (SSTI) | CWE-1336 | Critical | 用户输入传入模板引擎渲染 |
| 9 | 不安全文件上传 | CWE-434 | High | 文件上传未校验类型或内容 |
| 10 | 开放重定向 | CWE-601 | Medium | 重定向目标由用户输入控制 |
| 11 | 硬编码凭据 | CWE-798 | High | 代码中硬编码 API Key、Token、密码 |
| 12 | 敏感端点暴露 | CWE-200 | Medium | Spring Actuator、Django Debug 等暴露 |

---

## 项目结构

```
web-security-audit-skills/
├── SKILL.md                # Skill 定义文件(触发条件、工作流、规则参考)
├── README.md               # 项目说明文档(本文件)
└── scripts/
    ├── main.py             # 主入口,命令行解析与流程编排
    ├── engine.py           # 审计引擎,文件收集与扫描调度
    ├── rules.py            # 检测规则库,各语言漏洞正则模式
    └── security_md.py      # 报告生成器,Security.md 与 PoC 模板
```

---

## 环境要求

- **Python**:3.8 及以上
- **依赖**:标准库实现,无需额外安装第三方包
- **操作系统**:Windows / macOS / Linux 均可

---

## 快速开始

### 基本用法

```bash
python scripts/main.py <目标目录>
```

### 指定语言扫描

```bash
python scripts/main.py /path/to/php-project --lang php
```

### 指定输出路径

```bash
python scripts/main.py /path/to/project --output /tmp/Security.md
```

### 同时输出 JSON 摘要

```bash
python scripts/main.py /path/to/project --json
```

### 完整示例

```bash
python scripts/main.py ./my-go-project --lang go --output Security.md --json
```

---

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `target` | 待扫描的源码目录路径(必填) | — |
| `--lang` | 指定语言:`php` / `java` / `python` / `go` | 自动检测 |
| `--output` | `Security.md` 输出路径 | 当前工作目录 |
| `--json` | 额外输出 JSON 摘要文件 | 不输出 |

---

## 工作流程

1. **确定范围**:指定待扫描的目标目录
2. **收集文件**:递归遍历目录,按后缀筛选源码文件,自动排除依赖与构建目录
3. **语言识别**:根据文件后缀自动判断语言(或使用 `--lang` 强制指定)
4. **规则匹配**:对每个文件应用对应语言的检测规则,逐行扫描
5. **结果汇总**:按严重级别(Critical / High / Medium / Low)分类统计
6. **生成报告**:输出 `Security.md`,包含执行摘要、漏洞分布、详细发现与 PoC

### 支持的文件后缀

| 语言 | 后缀 |
|------|------|
| PHP | `.php` `.phtml` `.php3` `.php4` `.php5` `.inc` |
| Java | `.java` `.jsp` `.jspx` |
| Python | `.py` `.pyw` `.html` `.jinja2` `.j2` |
| Go | `.go` |

### 自动排除的目录

`node_modules`、`vendor`、`.git`、`__pycache__`、`.venv`、`venv`、`.idea`、`.vscode`、`dist`、`build`、`target`、`.mvn`、`.gradle`、`egg-info`、`.egg`、`.tox`

---

## 检测规则参考

### PHP 规则

| 规则 ID | 类别 | 匹配模式 |
|---------|------|---------|
| PHP-SQLI-001 | SQL 注入 | `mysql_query(` / `->query(` 且查询字符串含 `$` 变量 |
| PHP-XSS-001 | XSS | `echo $_GET` / `print $_POST` / `<?=$_REQUEST` |
| PHP-RCE-001 | 命令注入 | `system($` / `exec($` / `shell_exec($` / `eval($` |
| PHP-LFI-001 | 文件包含 | `include($_GET` / `require($_POST` |
| PHP-DESER-001 | 反序列化 | `unserialize($_GET` |
| PHP-SSRF-001 | SSRF | `file_get_contents($_GET` / `curl_exec(` 含用户 URL |
| PHP-UPLOAD-001 | 文件上传 | `move_uploaded_file($_FILES` |
| PHP-XXE-001 | XXE | `simplexml_load_string($` / `DOMDocument->loadXML($` |
| PHP-REDIR-001 | 开放重定向 | `header("Location: ".$_GET` |

### Java 规则

| 规则 ID | 类别 | 匹配模式 |
|---------|------|---------|
| JAVA-SQLI-001 | SQL 注入 | `createStatement()` / `executeQuery("SELECT...+"` |
| JAVA-XSS-001 | XSS | `response.getWriter().print(request.get` |
| JAVA-RCE-001 | 命令注入 | `Runtime.getRuntime().exec(request.get` |
| JAVA-DESER-001 | 反序列化 | `ObjectInputStream(request` / `readObject()` |
| JAVA-SSRF-001 | SSRF | `HttpURLConnection` / `RestTemplate` 含用户 URL |
| JAVA-XXE-001 | XXE | `DocumentBuilderFactory.newInstance()` |
| JAVA-PATH-001 | 路径遍历 | `new File(request.get` / `Paths.get(request.get` |
| JAVA-ACT-001 | Actuator 暴露 | `endpoints.web.exposure.include=*` |

### Python 规则

| 规则 ID | 类别 | 匹配模式 |
|---------|------|---------|
| PY-SQLI-001 | SQL 注入 | `.execute(f"...request"` / `.execute("...%s" % request` |
| PY-XSS-001 | XSS | `\|safe` / `mark_safe(request` / `render_template_string(request` |
| PY-RCE-001 | 命令注入 | `os.system(request` / `subprocess.run(request` / `eval(request` |
| PY-SSTI-001 | SSTI | `render_template_string(request` / `Template(request` |
| PY-DESER-001 | 反序列化 | `pickle.loads(request` / `yaml.load(request` |
| PY-SSRF-001 | SSRF | `requests.get(request` / `urlopen(request` |
| PY-PATH-001 | 路径遍历 | `open(request` / `send_file(request` |
| PY-SECRET-001 | Django 密钥 | `SECRET_KEY = '...'` 硬编码 |

### Go 规则

| 规则 ID | 类别 | 匹配模式 |
|---------|------|---------|
| GO-SQLI-001 | SQL 注入 | `fmt.Sprintf("SELECT...%s"` / `db.Query("SELECT..."+` |
| GO-XSS-001 | XSS | `w.Write([]byte(r.` / `fmt.Fprintf(w, r.` |
| GO-RCE-001 | 命令注入 | `exec.Command(r.` / `exec.CommandContext(ctx, r.` |
| GO-SSTI-001 | SSTI | `template.New(r.` / `.Execute(w, r.` |
| GO-SSRF-001 | SSRF | `http.Get(r.` / `http.NewRequest(r.` |
| GO-PATH-001 | 路径遍历 | `os.Open(r.` / `ioutil.ReadFile(r.` |

---

## 报告示例

扫描完成后,`Security.md` 报告结构如下:

```markdown
# Security Audit Report — ProjectName

**Generated:** 2026-06-20 10:00:00
**Scanner:** Marvis Web Security Audit Skill
**Languages:** PHP / Java / Python / Go

---

## 1. Executive Summary

| Metric | Value |
|--------|-------|
| Files Scanned | 42 |
| Total Findings | 15 |
| Critical | 3 |
| High | 7 |
| Medium | 4 |
| Low | 1 |

## 2. Vulnerability Distribution

| Category | Count |
|----------|-------|
| SQL Injection | 5 |
| Cross-Site Scripting (XSS) | 4 |
| ... | ... |

## 3. Detailed Findings

### Critical Severity

#### SQL Injection

##### [1] PHP-SQLI-001 — login.php

- **Rule ID:** `PHP-SQLI-001`
- **CWE:** [CWE-89](https://cwe.mitre.org/data/definitions/89.html)
- **Category:** SQL Injection
- **Severity:** Critical

**Vulnerable Location:**
```
File : /path/to/login.php
Line : 12
Code : $sql = "SELECT * FROM users WHERE id=".$_GET['id'];
```

**Root Cause:**
拼接用户输入到 SQL 查询,未使用参数化查询或预处理语句

**Remediation:**
1. 使用 PDO 预处理语句
2. 对用户输入进行类型校验

**Exploit (PoC):**
```python
#!/usr/bin/env python3
"""SQL Injection PoC"""
import requests
# ... 可运行的验证脚本 ...
```
```

---

## 免责声明

本工具仅用于**授权的安全测试与代码审计**。在使用前,请确保:

1. 你拥有目标代码的合法所有权或已获得书面授权
2. 你在合法合规的前提下使用本工具进行安全评估
3. 生成的 PoC 脚本仅用于验证漏洞存在性,不得用于非法入侵
4. 对生产环境进行测试前,请充分评估潜在影响

对于因不当使用本工具造成的任何后果,作者不承担法律责任。

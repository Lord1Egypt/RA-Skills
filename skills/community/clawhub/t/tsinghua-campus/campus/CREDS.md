# CREDS — 凭据配置指引（AI 阅读）

> 本文件给 LLM 看，不面向用户。用户不看任何 MD。
> 凭据按**系统域**分组（cas / literature / mail / llm），每系统独立申请、独立配置。
> 配置命令统一：`creds.py add <key> --value-stdin`（值 stdin 直传，写入加密保险箱，不出设备）。

## 凭据域总览

| 系统域 | 需要的 key | 用途 | 何时向用户索取 |
|--------|-----------|------|---------------|
| `cas` | cas_username, cas_password | 清华统一认证登录（learn/info/timetable/library 共用） | 用户要用校园事务时，**必需** |
| `cas`(可选) | student_id, student_name | 作业文件命名 `学号_姓名.pdf` | 用户要交作业时 |
| `literature` | scopus_api_key (+scopus_inst_token 可选) | 文献检索鉴权 / 提配额 | 用户要查文献时 |
| `llm`(可选) | deepseek_api_key | learn 预批改 / 文献摘要 | 用户要用 AI 功能时 |
| `mail`(未实现) | email_imap | 收发邮件 | 预留 |

## 配置流程（AI 执行）

```powershell
# 1. 查状态（按系统分组展示）
python creds/scripts/creds.py status

# 2. 看某系统需要什么（含申请途径/用途）
python creds/scripts/creds.py guide <system>     # cas | literature | mail | llm

# 3. 向用户索取后配置（stdin 直传，不写临时文件明文）
echo <值> | python creds/scripts/creds.py add <key> --value-stdin

# 4. 重置某系统的凭据（独立重置，不影响其他系统）
python creds/scripts/creds.py reset <system> --confirm
```

## 各系统申请途径（向用户说明）

- **cas**：即清华统一认证账号/密码（学号 + 登录密码），无需额外申请
- **literature**：dev.elsevier.com 注册申请 Scopus API Key（可走清华 CARSI 机构登录）；机构 Token 向图书馆申请
- **llm**：platform.deepseek.com 创建 DeepSeek API Key（OpenAI 兼容）
- **mail**：各邮箱设置里开启 IMAP 生成授权码

## 存储机制（加密保险箱）

- 所有凭据存进**单文件保险箱** `campus/runtime/credentials.enc`（Fernet 加密的 JSON，密文）
- 解密只需**一个主密钥**，来源优先级：① 环境变量 `CAMPUS_MASTER_KEY` ② OS keyring 单条（本机绑定，自动生成）③ `campus/runtime/vault/master.key`（0600，兜底）
- 文件随 SKILL 文件夹同步即可跨机携带；新设备设同一个 `CAMPUS_MASTER_KEY` 即能解密
- 主密钥管理：`creds.py key show`（读出，用于带到其他设备）/ `creds.py key set --value-stdin`（显式设置）/ `creds.py key source`（看来源）
- 旧版 `credentials.json`（keyring:/fernet: 引用）首次读取时自动迁移为 `credentials.enc`

## 铁律

- **不读根目录 `.env`**：技能包凭据全部走加密保险箱，与 agent 项目解耦
- **不用中文文件名**：所有 skill 文档/脚本用英文命名（面向 LLM 解析）
- **reset 按系统**：`creds.py reset <system>` 只清该系统凭据，不统一清空（避免误伤其他系统）

## 两个重置入口的职责边界

| 入口 | 层 | 清什么 | 影响范围 |
|------|----|--------|---------|
| `creds.py reset <system>` | 凭据存储 | 保险箱中该系统域的条目 | 只清凭据，不动登录态 |
| `base-cas/login.py --reset` | CAS 登录 | CAS 凭据 + learn/info session + 浏览器 profile | 只清 CAS，其他系统凭据保留 |

> 判断规则：**只想重配某个系统的 KEY**（如换文献 API Key）→ `creds.py reset literature`；
> **想重新登录 CAS / 清登录态**（换账号、信任设备满了）→ `login.py --reset`。

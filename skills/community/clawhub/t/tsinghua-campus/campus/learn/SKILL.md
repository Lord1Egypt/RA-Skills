---
name: campus-learn
description: 清华网络学堂。查看课程待办/未交作业/公告/课件、下载课件、提交作业、AI 预批改。当用户需要"查看待办、有什么作业、下载课件、交作业、看成绩"时使用。
metadata:
  openclaw:
    requires:
      env:
        - CAS_PASSWORD
    os:
      - windows
      - macos
      - linux
---

# 网络学堂

清华网络学堂（learn.tsinghua.edu.cn）自动化。登录走 base-cas（浏览器即用即退 + 两阶段验证码），数据走 learn_api。

## 如果你是 AI，请阅读以下内容

### 铁律

- **铁律 1：AI 运行所有脚本**。禁止让用户敲命令。
- **铁律 2：脚本面向 AI**。stdout 输出 JSON，进度写 `runtime/logs/campus.log`，不写 stderr。
- **铁律 3：验证码两阶段**。登录触发 2FA 时，脚本立即退出返回 pending token，AI 问用户拿码后 `login.py --submit-code <token> <code>`。
- **铁律 4：全程无头 + 即用即退**。base-cas 一律 headless 运行（无浏览器窗口）。浏览器用完即关，保留的是 session cookie 文件 + profile 指纹（信任态跨进程靠它们恢复）。仅 2FA 登录流程内浏览器保持打开。
- **铁律 5：提交需确认**。上传作业必须先预览（不带 --confirm）→ 用户确认 → 加 --confirm。
- **铁律 6：不硬编码**。课程/学期/路径走配置，不写死。

### 使用

```
learn.py courses [--course <部分匹配>]     # 课程列表
learn.py todos                             # 待办汇总（未读/未交/老师批改）
learn.py homeworks [--course <名>]          # 作业列表（含截止/状态）
learn.py files [--course <名>]              # 课件列表
learn.py announcements [--course <名>]      # 公告
learn.py download --course <名> [--pattern *.pdf]  # 下载课件
learn.py homework-full --course <名> [--id <zyid>] # 作业详情
learn.py mark-read [--course <名>]          # 标记已读
learn.py aggregated [--course <名>]         # 各课汇总
```

### 工作流

```
用户: 查看待办
AI:
  1. learn.py todos → 读 JSON（unread/未交/graded）
  2. 有老师批改 → 汇报评语/分数
  3. 有未交 → 问是否要交
```

```
用户: 交 XX 作业（发文件）
AI:
  1. learn.py homeworks --course <名> → 找作业 xszyid
  2. 预览提交（不带 --confirm）→ 展示确认信息
  3. 用户确认 → 加 --confirm 执行
```

### 会话失效处理

- learn session 会过期。`login.py --system learn --ensure` 自动检测并重新登录（信任浏览器免 2FA，或触发验证码两阶段）。
- learn 首页不自动跳 CAS，登录必须走 base-cas（内部已处理）。

### 边界

- 已提交作业无法撤回（learn 无撤回 API）。
- 学期自动检测；个别课程可能无课件/公告（返回空数组正常）。

---

## 如果你是用户，请阅读以下内容

对 AI 说：
- **"查看待办"** / "有什么作业" — 看未交作业、截止日期、老师批改反馈
- **"下载 XX 课件"** / "交 XX 作业" — 课件下载、作业提交
- **"最近有什么公告"** — 课程通知

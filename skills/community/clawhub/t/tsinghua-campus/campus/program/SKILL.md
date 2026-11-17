---
name: campus-program
description: 清华教务培养方案。查看培养方案完成情况（课组完成度、应修/完成学分门数、方案外课程）。当用户需要"培养方案、学分够不够、还差什么课、毕业要求"时使用。
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

# 培养方案

清华教务系统（zhjw.cic.tsinghua.edu.cn）培养方案完成情况查询。登录走 base-cas（浏览器即用即退 + 两阶段验证码），经 info 门户应用导航进入教务系统获取数据。

## 如果你是 AI，请阅读以下内容

### 铁律

- **铁律 1：AI 运行所有脚本**。禁止让用户敲命令。
- **铁律 2：脚本面向 AI**。stdout 输出 JSON，进度写 `runtime/logs/campus.log`，不写 stderr。
- **铁律 3：验证码两阶段**。登录触发 2FA 时，脚本立即退出返回 pending token，AI 问用户拿码后 `login.py --submit-code <token> <code>`。
- **铁律 4：全程无头 + 即用即退**。base-cas 一律 headless 运行（无浏览器窗口）。浏览器用完即关，保留 session cookie 文件 + profile 指纹（信任态跨进程靠它们恢复）。仅 2FA 登录流程内浏览器保持打开。用户只需在对话里提供验证码，无需操作浏览器。
- **铁律 5：隐私红线**。培养方案含学号/姓名（摘要段），面向用户输出时姓名/学号脱敏（`202***`）。

### 使用

```
program.py                  # 培养方案完成情况（摘要 + 课组 + 方案外课程）
program.py --summary-only   # 仅摘要
```

输出 JSON：`program.summary`（总学分/必修/限选/任选完成情况）、`program.groups`（课组课程清单：课程属性/课组名/课程号/课程名/学分/成绩/绩点/应修/完成/门数/是否完成）、`program.outside`（方案外课程）。

### 工作流

```
用户: 培养方案完成得怎么样 / 还差什么课 / 学分够不够
AI:
  1. program.py → 读 JSON
  2. 汇报摘要：应完成 X 学分，已完成 Y，还差 Z
  3. 用户问某类课（必修/限选）→ 列出该类课组及未完成课程
```

### 技术链路（重要）

培养方案数据源是教务系统（zhjw），**不能直接访问**（加密临时 URL）。必须经 info 门户：

1. 确保 info 门户会话（`login.py --system info --ensure`，信任浏览器免 2FA）
2. 打开 info 应用导航页 `portal_fg/student/yyfwxxindex`
3. 点击"培养方案完成情况"应用（yyfwid=`EF49444CB7D13C2AA029B911B0833CEE`）→ 触发 `onlineAppRedirect` 建立 zhjw 教务会话
4. goto 培养方案业务 URL `jhBks.by_fascjgmxb_gr.do` → 解析表格

> 解析说明：课组表第一行是课组头（含课程属性/应修学分等），后续行是同组课程（继承属性）。页面有两份重复的课组表（打印/屏幕两份 view），脚本取第一张并去重。

### 会话失效处理

- info session 会过期。program.py 内置会话检查（4h 内有效则跳过登录），过期自动触发 base-cas 登录。
- 登录需 2FA 时返回 pending，AI 问用户拿码后提交。

### 边界

- 仅支持培养方案完成情况；培养方案及计划（完整课表清单）是独立应用（yyfwid `3DBB9FD0...`），当前未实现。
- 重复课程（跨课组）系统已提示"学分只计一次"，脚本原样保留各课组归属。

---

## 如果你是用户，请阅读以下内容

对 AI 说：
- **"培养方案"** / "学分还差多少" / "毕业要求" — 查看培养方案完成情况

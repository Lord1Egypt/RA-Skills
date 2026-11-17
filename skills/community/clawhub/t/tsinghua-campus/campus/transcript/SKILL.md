---
name: campus-transcript
description: 清华教务成绩单。查看全部课程成绩（课程号/课程名/学分/成绩/绩点/学年学期）+ 总学分/平均绩点。当用户需要"我的成绩、查成绩、绩点、成绩单"时使用。
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

# 成绩单

清华教务系统（zhjw.cic.tsinghua.edu.cn）成绩单查询。登录走 base-cas（浏览器即用即退 + 两阶段验证码），经 info 门户应用导航进入教务系统获取数据。

## 如果你是 AI，请阅读以下内容

### 铁律

- **铁律 1：AI 运行所有脚本**。禁止让用户敲命令。
- **铁律 2：脚本面向 AI**。stdout 输出 JSON，进度写 `runtime/logs/campus.log`，不写 stderr。
- **铁律 3：验证码两阶段**。登录触发 2FA 时，脚本立即退出返回 pending token，AI 问用户拿码后 `login.py --submit-code <token> <code>`。
- **铁律 4：全程无头 + 即用即退**。base-cas 一律 headless 运行（无浏览器窗口）。浏览器用完即关，保留 session cookie 文件 + profile 指纹（信任态跨进程靠它们恢复）。仅 2FA 登录流程内浏览器保持打开。用户只需在对话里提供验证码，无需操作浏览器。
- **铁律 5：隐私红线**。成绩数据含个人信息（学号/姓名），面向用户输出时姓名/学号脱敏（`202***`），成绩本身可展示。

### 使用

```
transcript.py            # 全部课程成绩 + 总学分/绩点
```

输出 JSON：`transcript.courses`（课程号/课程名/学分/成绩/绩点/学年学期）+ `transcript.summary`（总学分/平均学分绩）。

### 工作流

```
用户: 我的成绩 / 绩点多少
AI:
  1. transcript.py → 读 JSON（courses + summary）
  2. 汇总：总学分、平均绩点、按学期/按课程汇报
  3. 用户问具体某门课 → 列出该课程成绩
```

### 技术链路（重要）

成绩数据源是教务系统（zhjw），**不能直接访问**（加密临时 URL）。必须经 info 门户：

1. 确保 info 门户会话（`login.py --system info --ensure`，信任浏览器免 2FA）
2. 打开 info 应用导航页 `portal_fg/student/yyfwxxindex`
3. 点击"全部成绩"应用（yyfwid=`0A4DFABA3A5876334F71F94654FCC4A8`）→ 触发 `onlineAppRedirect` 建立 zhjw 教务会话
4. goto 成绩单业务 URL `cj.cjCjbAll.do?cjdlx=zw&m=bks_cjdcx` → 解析表格

> 为什么不解析学生信息表：成绩单页顶部的学生信息（姓名/学号/院系）是用户已知信息且属隐私，数据结构有全角空格干扰，解析价值低。脚本只返回课程成绩 + 汇总。

### 会话失效处理

- info session 会过期。transcript.py 内置会话检查（4h 内有效则跳过登录），过期自动触发 base-cas 登录。
- 登录需 2FA 时返回 pending，AI 问用户拿码后提交。

### 边界

- 仅支持全部成绩（一学位课程）；二学位/辅修成绩需切换页面分类（当前返回默认视图全部课程）。
- 中文/英文成绩单（办证用）是独立应用（yyfwid `B7EF0ADF...`/`185FC0C5...`），当前未实现。

---

## 如果你是用户，请阅读以下内容

对 AI 说：
- **"我的成绩"** / "绩点多少" / "看成绩单" — 查看全部课程成绩与绩点

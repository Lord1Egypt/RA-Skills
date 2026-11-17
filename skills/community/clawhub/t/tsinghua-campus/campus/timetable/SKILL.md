---
name: campus-timetable
description: 清华教务课表。查看当前学期课表（星期×节次排布 + 未安排课程）。当用户需要"今天有什么课、本周课表、这学期课表"时使用。
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

# 课表

清华教务系统（zhjw.cic.tsinghua.edu.cn）课表查询。登录走 base-cas（浏览器即用即退 + 两阶段验证码），经 info 门户应用导航进入教务系统获取数据。

## 如果你是 AI，请阅读以下内容

### 铁律

- **铁律 1：AI 运行所有脚本**。禁止让用户敲命令。
- **铁律 2：脚本面向 AI**。stdout 输出 JSON，进度写 `runtime/logs/campus.log`，不写 stderr。
- **铁律 3：验证码两阶段**。登录触发 2FA 时，脚本立即退出返回 pending token，AI 问用户拿码后 `login.py --submit-code <token> <code>`。
- **铁律 4：全程无头 + 即用即退**。base-cas 一律 headless 运行（无浏览器窗口）。浏览器用完即关，保留 session cookie 文件 + profile 指纹（信任态跨进程靠它们恢复）。仅 2FA 登录流程内浏览器保持打开。用户只需在对话里提供验证码，无需操作浏览器。
- **铁律 5：不硬编码**。学期/路径走配置，不写死。

### 使用

```
timetable.py [--semester auto]     # 当前学期课表
```

输出 JSON：`schedule`（星期×节次排布，第1-6节 × 周一到周日）+ `unplaced`（未安排时间的课程）。

### 工作流

```
用户: 今天有什么课 / 看课表
AI:
  1. timetable.py → 读 JSON（schedule + unplaced）
  2. 今天是周X → 列出当天课程（该列非空单元格）
  3. 展示课表或按需求汇报
```

### 技术链路（重要）

课表数据源是教务系统（zhjw），**不能直接访问**（加密临时 URL）。必须经 info 门户：

1. 确保 info 门户会话（`login.py --system info --ensure`，信任浏览器免 2FA）
2. 打开 info 应用导航页 `portal_fg/student/yyfwxxindex`
3. 点击"课表"应用（yyfwid=`287C0C6D90ABB364CD5FDF1495199962`）→ 触发 `onlineAppRedirect` 建立 zhjw 教务会话
4. goto 课表业务 URL `portal3rd.do?m=bks_yjkbSearch` → 解析表格

> 为什么点一下：onlineAppRedirect 返回带 token 的临时 URL 并建立 zhjw 会话。不点直接访问会得到"用户登陆超时"。点击行为被 headless 下 window.open 新 tab 可能不出现，所以点击后**主动 goto 业务 URL**（会话已建立）。

### 会话失效处理

- info session 会过期。timetable.py 内置会话检查（**1h 内有效则跳过登录**），过期自动触发 base-cas 登录。
- **应用导航页需门户工作台会话**：登录后信任浏览器自动完成（约 36s），会话持久在 profile。若报"info 会话已过期"，说明门户会话失效，需重新登录。
- 登录需 2FA 时返回 pending，AI 问用户拿码后提交。

### 边界

- 仅支持课表查询；成绩单/培养方案是独立子 SKILL（transcript/program）。
- 课表含未安排时间的课程（如"形势与政策"），单独列在 `unplaced`。

---

## 如果你是用户，请阅读以下内容

对 AI 说：
- **"看课表"** / "今天有什么课" / "这学期课表" — 获取当前学期课表

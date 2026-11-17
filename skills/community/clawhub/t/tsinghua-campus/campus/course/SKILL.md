---
name: campus-course
description: 清华选课系统（zhjwxk）。查询已选课程、开课信息（任课老师）、学生评教/推荐度。注意：选课系统登录偶发图形验证码，评教/开课信息等部分功能按学期开放。当用户需要"选课、已选课程、任课老师、课程评价"时使用。
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

# 选课系统

清华选课系统（zhjwxk.cic.tsinghua.edu.cn）查询。登录走 webvpn http 编码 + 二次 CAS 认证（信任浏览器免 2FA，**偶发图形验证码**）。

## 如果你是 AI，请阅读以下内容

### 铁律

- **铁律 1：AI 运行所有脚本**。禁止让用户敲命令。
- **铁律 2：脚本面向 AI**。stdout 输出 JSON，进度写 `runtime/logs/campus.log`，不写 stderr。
- **铁律 3：验证码两阶段**。登录触发图形验证码时，脚本返回 pending + 验证码图片路径，AI 用视觉模型读码后 `course.py --submit-captcha <token> <code>`（浏览器保持打开）。
- **铁律 4：全程无头 + 即用即退**。base-cas 一律 headless 运行。浏览器用完即关，保留 session cookie 文件 + profile 指纹；仅 2FA 登录流程内保持打开。
- **铁律 5：只读不写**。本 SKILL 只做**只读查询**（已选课程/开课信息/评教）。**选课/退课是写操作，改变真实选课结果，一律不做**。

### 使用

```
course.py enrolled                # 已选课程（退课查询页）
course.py teacher --query <词>     # 开课信息（任课老师），--query 课程名关键词
course.py --submit-captcha <token> <code>  # 图形验证码两阶段
```

输出 JSON：`tables`（表格数组，每表是行数组，首行表头）。

### ⚠️ 已知限制（非选课季实测）

- **登录不稳定**：CAS 偶发图形验证码（约一半概率触发），需视觉模型读码；多次失败后可能要求更严格验证。
- **按学期开放的功能**（非选课季返回错误/500/空）：
  - 开课信息（`m=kkxxSearch`）→ "每天上课节数配置错误"
  - 评教优秀课堂/推荐度（`xgpg_xspjyxkt`）→ HTTP 500 "尚未开放查询"
- **始终可用**：已选课程（`m=tkSearchSingle`）返回表头+数据（非选课季为空数据）。
- 用户浏览器（校内网/headed）下功能可用，headless + webvpn 环境受限。

### 技术链路

1. 确保 info 门户会话（`login.py --system info --ensure`）
2. 访问 `xklogin.do`（webvpn http 编码 `eaff4b8b3f3b2653...`）→ 触发 CAS
3. **登录统一走 base-cas**：`login.ensure_login("course", page, ctx, home_url=XKLOGIN, logged_in_check="() => location.href.indexOf('id.tsinghua') < 0", captcha_handler=...)` —— 注入 cookie 复用会话 → 失效才填 CAS → 偶发图形验证码由 `captcha_handler` 两阶段处理
4. 访问业务 URL 解析表格

> **登录要点**：所有 CAS 填表集中在 `base-cas/scripts/login.py` 的 `ensure_login`，本 SKILL 不再自写登录。`ensure_login` 内部会等 `window.doLogin` 就绪再填表（SPA 需加载完），并自动处理 `login/check` 信任确认页。

### 会话失效处理

- 每次访问走 `_auth` → `login.ensure_login`（注入 cookie → 已登录免登录 → 失效才 CAS 填表）。
- 验证码 pending 时浏览器保持打开，`--submit-captcha` 连接同一浏览器填码。

### 边界

- 仅查询；选课/退课写操作**不做**（高风险）。
- 开课信息/评教等按学期开放，非选课季返回错误是**系统限制**，非脚本 bug。

---

## 如果你是用户，请阅读以下内容

对 AI 说：
- **"我选了哪些课"** / "选课情况" — 查询已选课程
- **"XX 课的老师"** / "这门课谁教" — 开课信息（需选课季开放）
- **"课程评价"** / "老师教学质量" — 评教/推荐度（需选课季开放）

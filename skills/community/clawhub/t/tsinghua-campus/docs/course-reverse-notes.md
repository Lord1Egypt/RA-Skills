# 选课系统（zhjwxk）逆向交接文档

> 状态：**已逆向大部分链路，功能暂缓实现**（非选课季系统锁定 + headless 环境登录不稳定）。
> 本文档记录所有逆向成果，供后续同学（选课季或校内网环境）继续完善。
> 时间：2026-08-15

## 一、结论速览

| 项 | 状态 |
|----|------|
| 登录链路 | ✅ 已完整逆向（`xklogin.do` → CAS → 指纹 → 选课系统），v17 走通一次 |
| 已选课程查询（enrolled） | ✅ course.py 已实现，可返回表格 |
| 开课信息（任课老师） | ⛔ 非选课季返回"每天上课节数配置错误"，系统锁定 |
| 评教/推荐度 | ⛔ 非选课季返回 HTTP 500 "尚未开放查询" |
| 图形验证码 | ⚠️ 登录约 50% 概率触发，已实现两阶段框架 |
| Wengine 域名编码 | 🔍 确认 CBC 块加密，未完全破解 |

**为什么暂缓**：非选课季（8 月中旬）选课系统的开课信息/评教/推荐度全部按学期锁定；且 headless + webvpn 环境下 CAS 频繁触发图形验证码（风控），自动化登录不稳定。用户浏览器（headed + 校内网）下功能可用。

## 二、核心成果（可复用）

### 1. 完整登录链路（已跑通一次）

```
1. 确保 info 门户会话（base-cas login.py --system info --ensure）
2. 访问 https://webvpn.tsinghua.edu.cn/http/77726476706e69737468656265737421eaff4b8b3f3b2653770bc7b88b5c2d320506b1aec738590a49ba/xklogin.do
   （= 选课系统 xklogin.do 的 webvpn http 编码，裸 http 校内地址经 webvpn 可达）
3. 等 CAS 登录页出现（SPA）→ 等 window.doLogin 函数就绪
4. page.type("#i_user", user) + page.type("#i_pass", pwd)（真实键入！）
5. page.evaluate("doLogin()")
6. 若出现 login/check 信任确认页 → _click_trust(page)
7. 设备指纹 getFinger3 → 自动跳回 webvpn 选课系统 → 认证完成
```

### 2. 登录关键坑（之前所有失败根因）

- **CAS 是 SPA**：必须 `wait_until="load"` + 轮询等 `window.doLogin` 存在后再填表。`domcontentloaded` 时函数未加载 → doLogin() 无效。
- **填表必须 `page.type`**（真实键入触发 onChange）：`page.fill` 不被受控组件（React/Vue）读取 → 值填了但登录失败。
- **图形验证码**：`captcha.jpg` 偶发出现（约 50%），需视觉模型读码。已实现两阶段：`course.py --submit-captcha <token> <code>`。
- **doLogin 检测**：`page.evaluate("() => typeof window.doLogin === 'function'")`，就绪后再填。

### 3. 业务 URL 映射（全部 webvpn http 编码前缀 `eaff4b8b3f3b2653...`）

| 功能 | 相对路径 | 备注 |
|------|---------|------|
| 登录入口 | `/xklogin.do` | 必走这个触发 CAS |
| 主页面 | `/xkBks.vxkBksXkbBs.do?m=main` | frame 布局（菜单顶 + 内容右） |
| 已选课程/退课查询 | `/xkBks.vxkBksTkbBs.do?m=tkSearchSingle&p_xnxq=2026-2027-1` | ✅ 非选课季可用（空数据） |
| 开课信息（一级课） | `/xkBks.vxkBksJxjhBs.do?m=kkxxSearch` | ⛔ 非选课季"配置错误" |
| 课余量查询 | `/xkBks.vxkBksXkbBs.do?m=xkqkSearch` | 选课季开放 |
| 教学计划查询 | `/jhBks.vjhBksPyfakcbBs.do?m=showBksZxZdxjxjhXmxqkclist` | — |
| 评教优秀课堂 | `/xkBks.xgpg_xspjyxkt.do?cm=xgpg_xspjyxktShow` | ⛔ 非选课季 500 |
| 学生推荐度 | `/xkBks.xgpg_xspjyxkt.do?cm=xgpg_qbkcmycdzbShow` | ⛔ 非选课季 500 |
| 二级课开课信息 | `/syxk.v_syxk_syrw_ejkc_bs.do?m=sykSearch` | 选课季开放 |

> **重要**：这些 URL 是相对路径，完整 URL = `https://webvpn.tsinghua.edu.cn/http/77726476706e69737468656265737421eaff4b8b3f3b2653770bc7b88b5c2d320506b1aec738590a49ba` + 相对路径。

### 4. 已实现的 course.py（`skill/campus/course/`）

```
course.py enrolled                # 已选课程（退课查询，可用）
course.py teacher --query <词>     # 开课信息（非选课季返回空/错误）
course.py --submit-captcha <token> <code>  # 图形验证码两阶段
```

- 登录封装 `_auth()`：goto xklogin → 等 doLogin → type → doLogin → 等跳转（含信任确认）
- 验证码两阶段：检测验证码 → 截图保存 → pending → `--submit-captcha` 连同一浏览器填码
- 表格解析 `_goto_biz()`：遍历 frame 提取 `<table>`（表头+行）

## 三、Wengine 域名编码（部分成果）

- 前缀 `77726476706e69737468656265737421` = `"wrdvpnisthebest!"` 的 hex
- 域名编码（如 `eaff4b8b...`）前 16 字节 key 一致（`909721fc475008301e68e9ccf8354355`），之后分歧 → **CBC 块加密**，key 依赖前块密文
- 两个样本（zhjw/zhjwxk）无法推导通用 key → **不能编码新域名**，但已有编码可硬编码复用
- 已知编码：课表=`eaff4b8b69336153301c9aa596522b20bc86e6e559a9b290`（zhjw）、选课=`eaff4b8b3f3b2653770bc7b88b5c2d320506b1aec738590a49ba`（zhjwxk）、info=`f9f9479369247b59700f81b9991b2631506205de`（https）

## 四、后续同学接手建议

### 环境准备
- **优先校内网**（校园 WiFi/有线）：选课系统裸 http 校内地址在 webvpn 下受限，校内网可直连
- 或选课季（学期初约 9 月）在 webvpn 下重试——开课信息/评教届时开放

### 下一步（选课季验证）
1. 登录后从**菜单点击**进入开课信息（而非直接 goto URL）——用户反馈功能可用，可能是菜单导航带正确上下文
2. 验证 `m=kkxxSearch` 开课信息返回任课老师数据 → 完善 teacher 命令
3. 验证评教/推荐度（`xgpg_xspjyxkt`）→ 实现 recommend 命令
4. 若验证码仍频繁：接本地 OCR（PaddleOCR-VL）或 AI 视觉模型自动读码

### 可探索
- 选课系统 frame 布局的菜单交互（`showhidedivc()`/`showhidediv()` 展开下拉）
- 选课/退课写操作（高风险，需用户明确授权 + 人工确认才做）

## 五、相关文件

- `skill/campus/course/SKILL.md` — course 子 SKILL 文档（含限制说明）
- `skill/campus/course/scripts/course.py` — 主脚本（登录+查询+验证码两阶段）
- `agent/docs/` 或 `reference/` — 如需补充可放此处
- 逆向过程临时脚本在 `D:\Temp\campus-env\crack_course_*.py` / `probe_course*.py`（任务结束可清理，关键结论已在本文档）

# 子涵交接文档 — 校园服务技能包

> 已完成底座 + 3 个子 SKILL。timetable/mail/library/info 待开发。
> 参照 `subskill-template.md` 和已完成子 SKILL。

## 已完成（可直接复用）

| 模块 | 路径 | 状态 |
|------|------|------|
| 底座 install | `skill/campus/install/` | ✅ 环境安装（腾讯云镜像） |
| 底座 creds | `skill/campus/creds/` | ✅ 统一凭据（加密保险箱 + 单主密钥 + 责任告知） |
| 底座 base-cas | `skill/campus/base-cas/` | ✅ CDP 登录 + 两阶段 2FA + 多系统 |
| 主 SKILL | `skill/campus/SKILL.md` | ✅ 路由 |
| learn 网络学堂 | `skill/campus/learn/` | ✅ 完整（登录/待办/课件/作业） |
| search 搜索 | `skill/campus/search/` | ✅ 多源（info/its/learn） |
| literature 文献 | `skill/campus/literature/` | ✅ Scopus 检索 |

## 待开发（P5，你的任务）

| 子 SKILL | 登录 | 复用底座 | 要点 |
|---------|------|---------|------|
| timetable 课表考试 | base-cas | learn 会话 / info webvpn | 课表接口在信息门户或选课系统 |
| mail 邮箱 | 无（IMAP） | email-accounts skill | 授权码，不涉 CAS |
| library 图书馆 | base-cas | seat.lib 座位 | 座位预约/借书 |
| info 信息查询 | base-cas | info 门户 | 通知/办事流程 |

## 开发流程（每个新子 SKILL）

```
1. 读 skill/docs/subskill-template.md
2. 建 skill/campus/<system>/（SKILL.md + scripts/）
3. 需要登录的 → 在 base-cas SYSTEMS 注册 + _config.py 桥接会话
4. 写 <system>.py 统一入口（argparse + common.output_json，无 stderr）
5. 用 CDP 实测接口，填 skill/docs/<system>接口核验.md
6. 主 SKILL.md 加路由
7. smoke_test.py 加检查项，全部通过
```

## 铁律（违反会被打回）

1. **无 stderr 输出**：进度写 `runtime/logs/campus.log`（common.log），绝不 print 到 stderr
2. **stdout 纯 JSON**：用 `common.output_json()`
3. **脚本不阻塞**：禁 input()/getpass()；验证码走 base-cas 两阶段
4. **凭据不硬编码**：走 creds + vault
5. **全程 headless**：登录走 base-cas 无头浏览器，登录后浏览器自动关闭、不残留
6. **不写 `time.sleep = N`**（赋值笔误）

## 提问前先自查

- 跑过 `smoke_test.py` 了吗？
- 真实数据拉到了吗？（不是空壳）
- PowerShell 下跑脚本有 `python.exe : ...` 报错吗？

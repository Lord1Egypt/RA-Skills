---
name: campus-ts2
description: 清华大学学生第二成绩单。查看课外经历记录（社会工作/学术科研/竞赛/志愿公益/社会实践/体育/文艺等 19 个模块）及填报状态。当用户需要"第二成绩单、课外经历、社会实践有哪些、志愿工时、保研简历"时使用。
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

# 第二成绩单

清华大学学生第二成绩单系统（transcript.student.tsinghua.edu.cn），记录本科生课外经历及成果（保研/评优/简历用）。登录走 CAS（信任浏览器免 2FA，**直连无需 webvpn，全年可用**）。

## 如果你是 AI，请阅读以下内容

### 铁律

- **铁律 1：AI 运行所有脚本**。禁止让用户敲命令。
- **铁律 2：脚本面向 AI**。stdout 输出 JSON，进度写 `runtime/logs/campus.log`，不写 stderr。
- **铁律 3：验证码两阶段**。登录触发 2FA 时返回 pending，AI 问用户拿码后 `login.py --submit-code`（第二成绩单系统信任浏览器免 2FA，通常不会触发）。
- **铁律 4：全程无头 + 即用即退**。base-cas 一律 headless 运行。浏览器用完即关，保留 session cookie 文件 + profile 指纹；仅 2FA 登录流程内保持打开。
- **铁律 5：隐私红线**。第二成绩单含学号，面向用户输出学号脱敏（`202***`），经历内容本身可展示。

### 使用

```
ts2.py status                  # 全部模块状态（已填/未填）+ 学号
ts2.py list                    # 全部模块已填条目
ts2.py list socialworks        # 指定模块（路径或中文名）
ts2.py list --status 已通过      # 按状态筛选（已通过/审核中）
ts2.py export [--out 路径]       # 导出第二成绩单 PDF（仅已通过条目）
```

输出 JSON：`status`（学号 + 19 模块状态）、`list`（模块 → 条目：info + status）、`export`（PDF 保存路径）。

### 工作流

```
用户: 我的第二成绩单 / 课外经历有哪些
AI:
  1. ts2.py status → 看哪些模块已填
  2. ts2.py list --status 已通过 → 已通过的经历
  3. 汇总展示（含状态审核中/已通过）
```

### 模块路径速查

| 类别 | 模块（路径 = 中文名） |
|------|---------------------|
| 学年填报 | ay_innovations 创新训练 / ay_research 科研项目 / ay_contests 竞赛奖励 / ay_arts 艺术比赛 / ay_sports 体育比赛 / ay_publications 学术论文 / ay_creative 创作表演 / ay_patents 专利授权 |
| 信息填写 | socialworks 社会工作 / researches 学术科研 / contests 竞赛比赛 / innovations 创新创业 / exchanges 海外研修及交换 / volunteers 志愿公益 / socials 社会实践 / sports 体育表现 / arts 文艺表现 / projects 因材施教计划 / unrecorded 其他 |

### 技术链路

1. 访问 `transcript.student.tsinghua.edu.cn`（**直连，不走 webvpn**）→ CAS 登录（信任浏览器免 2FA）
2. CAS SPA：等 `window.doLogin` 就绪 → `page.type` 填凭据 → `doLogin()` → 信任确认 → 回跳
3. 系统是 SPA 前端路由，各模块 URL：`/<module_path>`（如 `/socialworks`、`/volunteers`）
4. 解析表格（序号/信息/状态/操作）

> 登录要点：同选课系统 CAS 的坑——`wait_until="load"` + 等 doLogin + `page.type`（fill 不被受控组件读取）。但第二成绩单**登录稳定**（信任浏览器免 2FA，无图形验证码，实测直连可入）。

### 导出 PDF（进阶，已实现）

- 导出页 `/profile/export`：勾选条目 → **POST `/profile/export?_method=PUT`**（form 数据 = `勾选项name=on`，无需 csrf）→ 返回 `application/pdf`
- 只导出**已通过**条目（审核中的不含）
- PDF 含个人信息 + 已通过经历，官方盖章栏 + 成绩单编号
- 实测：导出的 PDF 是有效 `%PDF-1.3`（1.5MB），含"清年爱劳动""密云水库实践"等已通过条目

### 边界

- 仅查询 + 导出（只读）；**不实现填写/修改**（会改真实记录，且提交后不可改）。
- 数据含"审核中/已通过"状态，审核中条目未生效（导出不含）。

---

## 如果你是用户，请阅读以下内容

对 AI 说：
- **"我的第二成绩单"** / "课外经历" / "社会实践有哪些" — 查看第二成绩单记录
- **"志愿工时多少"** / "社会工作" — 查看指定模块

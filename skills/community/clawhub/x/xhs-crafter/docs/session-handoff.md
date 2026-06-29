# Session Handoff Document — xhs-crafter

> Generated: 2026-06-12
> Source session: xhs-crafter v7.1.0 → v7.3.0 iterative optimization

---

## 1. Project Identity

| Field | Value |
|-------|-------|
| Project name | xhs-crafter |
| One-line description | 将MD文章排版为3:4比例精美图片卡片+压缩文字稿，用于公众号/小红书贴图发布 |
| GitHub | `https://github.com/<owner>/xhs-crafter` |
| ClawHub slug | `xhs-crafter` |
| Current version | 7.3.0 |
| Project directory | `<project-dir>/xhs-crafter` |
| Tech stack | HTML / CSS / Node.js (Puppeteer screenshot + validate) |
| License | MIT |

---

## 2. Decision Chain (Why This Approach)

| Decision | Chosen | Rejected alternatives | Reason |
|----------|--------|----------------------|--------|
| 双风格体系 | Editorial Magazine + Swiss International | 单一风格 | Editorial适合叙事/人文，Swiss适合数据/工具，覆盖更多品类 |
| 字号速查表嵌入SKILL.md | 直接嵌入Step 3 Compose | 仅写在references/components.md | 新会话AI可能不仔细读参考文件，嵌入确保可见 |
| 封面/封底标题颜色 | #ffffff + text-shadow | #ece2cf(暖米色) | 暖米色与暖调背景图太接近，对比度不足 |
| validate.js自动化 | 12项规则自动检查 | 纯人工检查 | 人工检查易遗漏，自动化确保一致性 |
| 三层背景架构 | paper→wash→grain | 纯平背景 | Editorial核心美学是"纸墨感"，flat beige死板 |
| ClawHub发布 | 删除.claude-plugin/目录 | 保留plugin.json | .claude-plugin/导致ClawHub误判为plugin |
| 品类数量 | 13个品类 | 之前写的11个 | 实际数category-cookbook.md有13个独立章节 |

---

## 3. Data Flow & Execution Pipeline

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Step 1    │ →  │ Step 2    │ →  │ Step 3    │ →  │ Step 4    │ →  │ Step 5    │
│ Intake    │    │ Plan      │    │ Compose   │    │ Validate  │    │ Screenshot│
│ 识别品类   │    │ 内容规划   │    │ 组装HTML  │    │ 自检修复   │    │ 截图交付   │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
```

**Data format flow**:
- Intake: MD文本 → 品类/风格/主题推断
- Plan: 压缩阶梯 → 页面角色分配 → 节奏标注
- Compose: 种子模板 + 主题变量 → 完整HTML(index.html)
- Validate: validate.js 12项检查 → FAIL修复/WARN建议
- Screenshot: Puppeteer 2x截图 → PNG + 文字稿txt

**Trigger modes**:
- Interactive: 用户提供MD文章或飞书链接，AI调用xhs-crafter技能

---

## 4. Capability Boundary

### Can Do
- 将MD文章自动排版为3:4精美图片卡片（5-10页）
- 13个品类自动路由（商业/职场/旅行/教程/影视/游戏/美食/彩妆/穿搭/家居/健身/情感/推荐）
- 双风格体系（Editorial Magazine + Swiss International）
- 10套主题色预设（6 Editorial + 4 Swiss）
- 28种布局模板（M01-M16 + S01-S12）
- 自动验证12项规则（溢出/字号/节奏/颜色等）
- 双通道交付（本地文件夹 + 飞书云盘）

### Cannot Do (Current Limitations)
- 梦核/氛围感装饰风（与Editorial和Swiss均冲突）
- Y2K/千禧辣妹/哥特萝莉/kawaii装饰风
- 纯摄影展示（图片本身就是交付物）
- AI生成人脸做妆容示范（禁止）
- 美食菜品大片摆盘（需专业食物摄影）

### Dependency Constraints
| Dependency | Constraint | Impact |
|------------|-----------|--------|
| Puppeteer/Chrome | 需系统Chrome或Playwright chromium | 截图依赖浏览器环境 |
| 飞书lark-cli | 需安装并登录 | 云盘交付依赖 |
| GitHub网络 | 当前网络不稳定 | 推送/Release可能失败 |
| AI生图API | 可能返回相同占位图 | 需buf1.equals(buf2)验证 |

---

## 5. Project File Structure

```
xhs-crafter/
├── SKILL.md                              # 技能主文件（AI调用时首先加载）
├── CHANGELOG.md                          # 版本变更记录
├── README.md                             # GitHub仓库首页
├── LICENSE                               # MIT
├── .gitattributes                        # UTF-8 + LF编码
├── .gitignore
├── assets/
│   ├── validate.js                       # 12项自动验证脚本
│   ├── screenshot.js                     # Puppeteer截图脚本
│   ├── template-editorial-card.html      # Editorial种子模板
│   └── template-swiss-card.html          # Swiss种子模板
├── references/
│   ├── style-system.md                   # 风格系统（Editorial vs Swiss）
│   ├── category-cookbook.md              # 13品类路由表
│   ├── content-planning.md               # 内容规划
│   ├── portrait-fill.md                  # 3:4密度规则+三层节奏
│   ├── image-overlay.md                  # 文字压图规则
│   ├── theme-presets.md                  # 10套主题色预设
│   ├── components.md                     # 字体/字号/间距/容器规范
│   ├── layout-recipes.md                 # 28种布局模板
│   ├── screenshot-treatment.md           # 截图美化
│   ├── background-systems.md             # 三层背景架构
│   ├── image-sources.md                  # 图库接入+AI生图验证
│   └── workflow.md                       # 工作流补充
└── docs/
    └── session-handoff.md                # 本交接文档
```

---

## 6. Platform Status

### GitHub Repository
- Repo: `<owner>/xhs-crafter`
- Latest Release: v7.2.0 (v7.3.0本地已commit，推送因网络问题待恢复)
- Branch: main

### ClawHub
| Version | Security | Notes |
|---------|----------|-------|
| 7.3.0 | CLEAN | 最新发布，含R10/R11/R12+速查表 |
| 7.2.0 | CLEAN | R8/R9+Swiss字号同步 |
| 7.1.1 | CLEAN | 字号速查表嵌入 |

---

## 7. Environment Variables

| Variable | Purpose | Status |
|----------|---------|--------|
| GitHub token | git push + Release API | Configured (in remote URL) |
| ClawHub CLI | npx clawhub@latest publish | Configured |
| lark-cli | 飞书云盘上传 | Needs user login check |

---

## 8. Session Code Changes Summary

| File | Change | Reason |
|------|--------|--------|
| SKILL.md | 嵌入字号速查表(15级)+5条字号铁律 | 跨会话字号执行不一致 |
| SKILL.md | 嵌入节奏速查表(7条)+密度速查表(6条)+图片规则速查(8条) | 同上策略，确保关键规则可见 |
| SKILL.md | 品类数量11→13 | 实际数了category-cookbook.md有13个章节 |
| SKILL.md | 验证规则数9→12 | 新增R10/R11/R12 |
| validate.js | 新增R8(标题一致性)+R9(满铺图页标题颜色) | 防止标题混用和颜色对比不足 |
| validate.js | 新增R10(暗色页节奏)+R11(accent面积)+R12(封面封底图背景) | 自动化节奏/面积/图框检查 |
| template-swiss-card.html | body 28→32px, lead 32→34px, t-cat 24→26px, t-meta 20→24px | Swiss字号与Editorial同步 |
| components.md | Swiss字号表+字重铁律+封面颜色硬规则 | 规范权威来源同步更新 |
| CHANGELOG.md | 新增v7.1.0/v7.1.1/v7.2.0/v7.3.0条目 | 版本追踪 |

---

## 9. Knowledge File Index (Load on Demand)

| Need | File to Read | Priority |
|------|-------------|----------|
| 字号/间距/容器规范 | `references/components.md` | Must-read |
| 品类路由 | `references/category-cookbook.md` | Must-read |
| 风格选择(Editorial vs Swiss) | `references/style-system.md` | Must-read |
| 背景三层架构 | `references/background-systems.md` | Must-read |
| 密度/节奏规则 | `references/portrait-fill.md` | Must-read |
| 满铺图页文字压图 | `references/image-overlay.md` | On-demand |
| 主题色预设 | `references/theme-presets.md` | On-demand |
| 布局模板 | `references/layout-recipes.md` | On-demand |
| 内容规划 | `references/content-planning.md` | On-demand |
| 图库接入 | `references/image-sources.md` | On-demand |
| 截图美化 | `references/screenshot-treatment.md` | On-demand |

---

## 10. User Preferences

| Preference | Description |
|-----------|-------------|
| Language | Chinese |
| Work style | SOLO工程化模式（Spec→Plan→Build→Verify→Review→Ship→Evolve） |
| Code style | 最小化修改，不过度重构 |
| Security sensitivity | 高（不提交token/密钥，删除.claude-plugin/） |
| 交付偏好 | 双通道：本地文件夹 + 飞书云盘 |
| 字号偏好 | 整体偏大，封面/封底比内容页更大 |
| 验证偏好 | 自动化validate.js优先，铁律规则嵌入SKILL.md确保可见 |

---

## 11. Branchable Directions

| # | Direction | Type | Files Involved | Prerequisites | Complexity |
|---|-----------|------|---------------|---------------|------------|
| A | 实战测试新文章 | Engineering | 新项目目录+SKILL.md+references | 用户提供文章链接 | Low |
| B | 新增布局模板 | Engineering | references/layout-recipes.md, template-*.html | 确定缺失的布局场景 | Med |
| C | 截图脚本增强(自动启动http.server) | Engineering | assets/screenshot.js | 无 | Low |
| D | 更多validate规则(图片比例一致性/连续版式检测) | Engineering | assets/validate.js | 无 | Med |
| E | README更新到v7.3.0 | Ops | README.md | GitHub网络恢复 | Low |
| F | 复盘沉淀v7.1→v7.3迭代 | Research | docs/knowledge/ | 无 | Low |

---

## 12. Startup Prompt for New Session

(See Section below — generated for TRAE SOLO)

---

## 13. IDE-Specific Context — TRAE SOLO

### Rules
| File | Path | Description |
|------|------|-------------|
| User Rules | (global) | SOLO工程化模式规则 v2.0.0 |

### Scheduled Tasks
N/A — no scheduled tasks for this project

### Pending Items
- [ ] GitHub推送v7.3.0（网络恢复后执行 `git push origin main`）
- [ ] GitHub Release v7.3.0创建
- [ ] README.md更新版本号到7.3.0
- [ ] `.agents/skills/xhs-crafter/` 手动同步（权限受限无法自动同步）

### Known Issues
- GitHub连接不稳定（SSL/TLS handshake失败）
- AI生图API可能返回相同占位图（需buf1.equals(buf2)验证）

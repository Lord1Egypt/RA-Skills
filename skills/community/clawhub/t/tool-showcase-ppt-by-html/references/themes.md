# 主题色预设(Themes)

9 套精心调配的工具展示主题色板。

---

## 使用方法

**AI 直接根据工具类型选用，不展示 9 套预设让用户选。**

1. AI 根据 Step 1 的「工具类型 → 主题色」映射自动选定
2. 打开 `assets/template.html` 的 `<style>` 块
3. 找到开头的 `:root{` 块
4. **整体替换**标有"主题色"注释的那几行(`--accent` 到 `--muted`)
5. 其他 CSS 都走 `var(--...)`,无需任何其他改动

---

## 用户指定颜色时的处理

> 色调相符 + 整体协调 > 字面匹配。**AI 自由搭配同色调，不强制套预设**。

### 处理逻辑

用户说"用紫色" / "蓝调" / "暖色系" / "高级灰" / "和我品牌色差不多"：

1. **抓住色调**（紫/蓝/暖/灰/绿等）
2. **AI 自由搭配同色调**：
   - 可以直接用 9 套预设里同色调的（如紫 → 极客紫）
   - 也可以**自由组合**同色调的 10 个变量（如"紫色"可以是 #7c3aed 也可以是 #9333ea，只要整体是紫色系且协调即可）
3. **告知用户最终色值**（"已用紫色调，主色 #7c3aed"）

### 用户给具体 hex 怎么办

用户说"用 #ff5722"：
1. 以 hex 的**色调**作为主体
2. **AI 自由调整**其他 9 个变量，保持整体协调：
   - `--accent`：取 hex 本身（或微调饱和度/明度让它不刺眼）
   - `--accent-rgb`：accent 的 RGB 元组
   - `--accent-light`：accent 的 10% 透明度色（背景色）
   - `--bg-light` / `--bg-dark`：保持灰白/深色基底（不跟 accent 走，避免花哨）
   - `--text-light` / `--text-dark`：保持灰阶文字
   - `--card-bg` / `--card-border`：纯白卡片 + 浅灰边框
   - `--muted`：取 accent 的灰化版本
3. 告知用户"已按你指定的色调搭配，最终主色 #ff5722"

---

## 🔵 科技蓝 (Tech Blue) — 默认

**适合**:效率工具、办公软件、通用工具、截图工具
**调性**:Google/Notion 式的现代蓝,专业可信赖

```css
--accent:#1a73e8;
--accent-rgb:26,115,232;
--accent-light:#e8f0fe;
--bg-light:#f8fafc;
--bg-dark:#0f172a;
--text-light:#1e293b;
--text-dark:#e2e8f0;
--card-bg:#ffffff;
--card-border:#e2e8f0;
--muted:#64748b;
```

---

## 🟣 极客紫 (Geek Purple)

**适合**:开发者工具、CLI 工具、开源项目、代码编辑器
**调性**:GitHub/Vercel 式的开发者审美,技术感强

```css
--accent:#7c3aed;
--accent-rgb:124,58,237;
--accent-light:#ede9fe;
--bg-light:#faf9ff;
--bg-dark:#0c0a1d;
--text-light:#1e1b4b;
--text-dark:#e0dff5;
--card-bg:#ffffff;
--card-border:#e4e0f0;
--muted:#6b6594;
```

---

## 🟢 效率绿 (Productivity Green)

**适合**:办公效率工具、笔记软件、文件管理工具
**调性**:Notion/Evernote 式的清新绿,高效自然

```css
--accent:#059669;
--accent-rgb:5,150,105;
--accent-light:#ecfdf5;
--bg-light:#f9fdfb;
--bg-dark:#0a1f18;
--text-light:#134e4a;
--text-dark:#d1fae5;
--card-bg:#ffffff;
--card-border:#d1e8e0;
--muted:#5b8c7a;
```

---

## ⚫ 暗夜黑 (Dark Mode Pro)

**适合**:安全工具、审计工具、底层系统工具、专业级应用
**调性**:终端/VS Code Dark+ 式的专业暗色,严肃可靠

```css
--accent:#3b82f6;
--accent-rgb:59,130,246;
--accent-light:#1e3a5f;
--bg-light:#f1f5f9;
--bg-dark:#0a0e14;
--text-light:#1e293b;
--text-dark:#cbd5e1;
--card-bg:#ffffff;
--card-border:#cbd5e1;
--muted:#64748b;
```

---

## 🔥 日落橙 (Sunset Orange)

**适合**: 创意工具、设计工具、UI/UX 类应用、图像处理工具
**调性**: Figma/Dribbble 式的创意暖色,活力不浮躁

```css
--accent:#ea580c;
--accent-rgb:234,88,12;
--accent-light:#fff7ed;
--bg-light:#fffbf8;
--bg-dark:#1c110a;
--text-light:#431407;
--text-dark:#ffedd5;
--card-bg:#ffffff;
--card-border:#fed7aa;
--muted:#9a593b;
```

---

## 🌊 海洋青 (Ocean Teal)

**适合**: 协作工具、云端服务、API 平台、团队工具
**调性**: Slack/Linear 式的现代协作感,理性而亲和

```css
--accent:#0d9488;
--accent-rgb:13,148,136;
--accent-light:#f0fdfa;
--bg-light:#f8fdfb;
--bg-dark:#042f2e;
--text-light:#134e4a;
--text-dark:#ccfbf1;
--card-bg:#ffffff;
--card-border:#cce4e0;
--muted:#5b8b87;
```

---

## 🌸 玫粉 (Rose Pink)

**适合**: 生活类工具、笔记美化、个人效率、轻度应用
**调性**: Notion/Readwise 式的柔和粉调,温暖不甜腻

```css
--accent:#db2777;
--accent-rgb:219,39,119;
--accent-light:#fdf2f8;
--bg-light:#fdf8fb;
--bg-dark:#1a0a12;
--text-light:#500724;
--text-dark:#fce7f3;
--card-bg:#ffffff;
--card-border:#f0c4dc;
--muted:#9b5b7a;
```

---

## 🪐 午夜金 (Midnight Gold)

**适合**: 专业级软件、企业工具、付费产品、旗舰应用
**调性**: Stripe/Datadog 式的高端感,暗底中一抹金

```css
--accent:#ca8a04;
--accent-rgb:202,138,4;
--accent-light:#fefce8;
--bg-light:#fdfcf6;
--bg-dark:#141000;
--text-light:#3b2f00;
--text-dark:#fef9c3;
--card-bg:#ffffff;
--card-border:#e8dca0;
--muted:#8b7d3d;
```

---

## 🌿 森琥珀 (Forest Amber)

**适合**: 教育类工具、知识管理、学习平台、文档工具
**调性**: Obsidian/Readwise 式的沉稳学究感,绿色基底 + 琥珀高亮

```css
--accent:#d97706;
--accent-rgb:217,119,6;
--accent-light:#fffbeb;
--bg-light:#fafdf8;
--bg-dark:#111a0a;
--text-light:#3b4a1b;
--text-dark:#ecfccb;
--card-bg:#ffffff;
--card-border:#dce8c8;
--muted:#6b7a4d;
```

---

## 推荐选择参考

| 工具类型 | 推荐主题 |
|---------|---------|
| 截图/录屏/标注工具 | 🔵 科技蓝 |
| CLI/终端/开发工具 | 🟣 极客紫 |
| 笔记/文件/效率工具 | 🟢 效率绿 |
| 安全/审计/监控工具 | ⚫ 暗夜黑 |
| 创意/设计/图像工具 | 🔥 日落橙 |
| 协作/云服务/API 工具 | 🌊 海洋青 |
| 生活/笔记美化/轻量应用 | 🌸 玫粉 |
| 企业/付费/旗舰产品 | 🪐 午夜金 |
| 教育/知识管理/文档工具 | 🌿 森琥珀 |
| 不确定选啥 | 🔵 科技蓝(默认) |

---

## 切换原则

- **一份 deck 只用一套主题**,不要中途换色
- 所有 accent 相关 UI(按钮、高亮、border)自动跟随 `var(--accent)`
- Light/Dark 页会自动使用对应的 `--bg-light`/`--bg-dark` 和文字色
- 选定主题后告知用户,并在项目记录里备注

## 不允许做的事

- ❌ 不允许混搭(例如 accent 取蓝色、bg 取紫色)
- ❌ 不要直接修改 template.html 其他 CSS 颜色——改 :root 10 行即可
- ❌ 不要照搬用户给的奇怪 hex(纯荧光色、刺眼原色) — AI 调制成协调版本

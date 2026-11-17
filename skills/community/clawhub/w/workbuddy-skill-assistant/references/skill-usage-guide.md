# skill 使用速览：安装 · 使用 · 维护

> 欢迎来读这份速览～ 🧩 这份文档是"**怎么用 skill**"的唯一权威入口。
> 不管你是刚装 WorkBuddy，还是已经攒了一堆 skill 不知道怎么打理——安装、使用、维护升级一条龙，看完就能动手。
> 下面有一张「Skill 生命周期图」，命中"怎么用 skill / skill 速览"时我会用 Visualizer 直接渲染出来。

---

## Skill 生命周期图（建议用 Visualizer 渲染下方 SVG）

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 210" font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L8,3 L0,6 Z" fill="#2f6fed"/>
    </marker>
  </defs>
  <!-- 标题 -->
  <text x="20" y="26" font-size="15" font-weight="700" fill="#1f2933">Skill 生命周期：安装 → 使用 → 维护升级 → 组合拳 → 自动化</text>
  <!-- 节点 -->
  <g font-size="14" font-weight="600" text-anchor="middle">
    <rect x="20"  y="70" width="110" height="56" rx="10" fill="#2f6fed"/>
    <text x="75"  y="96" fill="#ffffff">① 安装</text>
    <text x="75"  y="114" font-size="11" fill="#dbe7ff">Install</text>

    <rect x="150" y="70" width="110" height="56" rx="10" fill="#0e9f6e"/>
    <text x="205" y="96" fill="#ffffff">② 使用</text>
    <text x="205" y="114" font-size="11" fill="#d7f5e8">Use</text>

    <rect x="280" y="70" width="110" height="56" rx="10" fill="#b54708"/>
    <text x="335" y="96" fill="#ffffff">③ 维护升级</text>
    <text x="335" y="114" font-size="11" fill="#ffe6cf">Maintain</text>

    <rect x="410" y="70" width="110" height="56" rx="10" fill="#7a5af8"/>
    <text x="465" y="96" fill="#ffffff">④ 组合拳</text>
    <text x="465" y="114" font-size="11" fill="#e7e0ff">Combo</text>

    <rect x="540" y="70" width="120" height="56" rx="10" fill="#52606d"/>
    <text x="600" y="96" fill="#ffffff">⑤ 自动化</text>
    <text x="600" y="114" font-size="11" fill="#dfe3e8">Automate</text>
  </g>
  <!-- 前向箭头 -->
  <g stroke="#2f6fed" stroke-width="2" marker-end="url(#arrow)">
    <line x1="132" y1="98" x2="146" y2="98"/>
    <line x1="262" y1="98" x2="276" y2="98"/>
    <line x1="392" y1="98" x2="406" y2="98"/>
    <line x1="522" y1="98" x2="536" y2="98"/>
  </g>
  <!-- 回环虚线：自动化 → 回到安装/使用 -->
  <path d="M600,130 C600,180 75,180 75,128" fill="none" stroke="#9aa5b1" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arrow)"/>
  <text x="340" y="200" font-size="11" fill="#687385" text-anchor="middle">自动化让维护/检查每天自己跑，形成持续保鲜闭环</text>
</svg>
```

---

## ① 安装（Install）

**两条正确路径，别走错：**

| 路径 | 适用 | 怎么做 |
|------|------|--------|
| **A. SkillHub 托管技能**（推荐，核心 4 个） | `skill-map` / `skill-check-pro` / `skll-auto-upgrade` / `high-quality-skill-guidance` | **直接复制下面的安装 prompt 执行**，这是唯一正确方式 |
| **B. 推荐市场 / 内置技能** | 其他公开 skill | 用 `find-skills` / `marketplace-skill-installer` 搜索后装 |

> ⚠️ **铁律**：核心 4 个技能**不在**内置推荐市场（BuiltinMarket），用 `find-skills` 搜索必返回 0 结果，会被误判"未上架"。**请一律走 SkillHub 安装 prompt**（路径 A），不要走市场搜索。

**✅ 真实对话示例（可直接复制话术）**

```
你：「装一下 skill-map」
我：请根据 https://skillhub.cn/install/skillhub.md，安装 @user_7ba94f9e/skill-map
   （执行后）✅ 已装到 ~/.workbuddy/skills/，说 @skill-map 即可使用
```

> 🔧 **安装铁律**：无论哪条路径，装的时候**必须带 `--dir ~/.workbuddy/skills`**，否则会落到 `./skills/`（当前目录）而不被 WorkBuddy 识别（详见 faq §3）。例如 `skillhub install <slug> --dir ~/.workbuddy/skills`。

**「✅ 你试着说」**
- "装 skill-map" → 我给你 SkillHub 安装 prompt 并跑
- "装 skill-check-pro" → 同上
- "有什么好用的 skill 推荐" → 走路径 B 的 `find-skills`

---

## ② 使用（Use）

**三种触发方式，随你挑：**
1. **`@技能名`** —— 最直接，如 `@skill-map` 出全景图。
2. **自然语言** —— "推荐 skill""效率诊断""达标检查""我的 skill 配置有问题吗"。
3. **Skill 工具显式调** —— 当你明确指定某 skill 时。

> **红线**：匹配到已装 skill，**先调 Skill 再作答**，不要凭空编。

**✅ 真实调用示例**
```
你：「@skill-map」
我：（渲染一张可交互的 skill 全景地图：分类着色、关联连线、热度）
你：「推荐几个适合我的 skill」
我：（按你的 USER.md 画像，从主题积木推「通用核心 + 倾斜主题」）
```

**🔌 连好工具：MCP 授权配置（让 AI 替你取数）**
光装 skill 还不够——想让 AI 直接读你的邮件/文档/行情，得先**连好连接器**。这是新手最容易卡的一步，手把手见 [`config-templates/connector-quick-ref.md`](config-templates/connector-quick-ref.md) 的「新手上路」节（3 分钟配好第一个连接器，含授权流程可视化 + 各类授权对照表）。

**「✅ 你试着说」**
- "@skill-map" → 出全景图
- "推荐 skill" → 通用核心 + 主题积木推荐
- "把腾讯文档连上" → 我给 mcp.json 片段 + 提示点 Trust → OAuth 登录 → 状态变 connected

---

## ③ 维护（Maintain）

skill 装了不是终点，**持续保鲜**才是重点：

- **批量查升级**：`skillhub upgrade --check-only --dir ~/.workbuddy/skills`（一次扫全部，不逐条搜）→ 可升级项确认后升级。
- **一键体检**：`@skill-check-pro` 定期给 skill 生态做体检，找低频/坏项/重复。
- **僵尸 skill 建议"关"而非"删"**：不用时断开，需要再开，保留可恢复。
- **收口自动维护链**：装 `skll-auto-upgrade`，把"体检→改进→升级→复盘"自动化。

**✅ 真实升级示例**
```
你：「看看我的 skill 有没有新版」
我：运行 skillhub upgrade --check-only --dir ~/.workbuddy/skills
   → 发现 2 个可升级：skill-map(v2.1→v2.3)、skill-check-pro(v4.6→v4.8)
   （确认后）✅ 已升级，下次检查自动用新逻辑
```

**「✅ 你试着说」**
- "看看有没有新版" → 批量查升级
- "给我做个 skill 体检" → @skill-check-pro
- "装个自动升级" → 我给 skll-auto-upgrade 的 SkillHub 安装 prompt

---

## ④ 组合拳 + 自动化（Combo → Automate）

把前面串成一条**持续保鲜**的流水线：

```
skill-map（看清生态）
   → skill-check（体检找问题）
      → skill-auto-upgrade（自动改进升级）
         → 每日 11:00 自动化跑一遍（map→check→upgrade 自动闭环）
```

- **组合拳**：三件套 `skill-map → skill-check → skill-auto-upgrade` 编排串联、逐步确认、可断链（**绝不一次自动装完三个**）。
- **自动化**：重复的检查/维护建成"每日主动检查"自动化，让顾问自己跑，你只管看报告。

> 想启用每日主动监护？说"**启用主动监护**"，一键建好 11:00 自动化。

---

> 📌 **一句话记住**：装（走 SkillHub prompt）→ 用（@ 或自然语言）→ 养（upgrade + 体检）→ 串（三件套 + 自动化）。配好连接器，AI 才真正替你干活。

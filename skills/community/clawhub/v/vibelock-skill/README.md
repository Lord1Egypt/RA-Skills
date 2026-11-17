# VibeLock Skill — AI 开发者安全商业化引导系统

**[English](README.en.md) | 中文**

> **给你的 AI 作品一把版权锁**
> 加密是钩子 · 授权是锁定 · 服务是纵深 · 资本是天花板

VibeLock 是面向 Vibe Coding 时代的 **AI 开发者商业化一站式 Skill**（AI Agent 引导系统，纯对话驱动、零本地依赖）。以**代码加密授权**为入口，为 AI 开发者提供从**打包、加密、授权、分发**到企业服务、课程培训、投融资的全链路商业化解决方案。

```
Skill 对话引导 → 本地加密打包 → 授权分发 → 商城曝光 · 商业赋能
```

- 当前版本：**v2.5.4**
- 支持语言/架构：**全语言全架构**（Python / Node.js / Go / Rust / Java / .NET / C/C++ / Electron / Dart-Flutter / SaaS / 移动端等）
- 支持 AI 平台：**Trae / Cursor / Claude Code / GitHub Copilot / Windsurf / Coze / 通义千问 / 文心一言 / Kimi / ChatGPT / Claude** 等

---

## 为什么需要它（痛点）

AI 让普通人也能做软件，但 **没人帮他们商业化**——变现成了最后一公里难题：

| 痛点 | VibeLock 的解法 |
|---|---|
| ✗ 源码给出去就被传开，无法控制分发 | ✓ AES-256 加密 + 硬件指纹绑定，一机一码，传播即失效 |
| ✗ 不懂加密技术，不知道怎么打包保护 | ✓ AI 对话引导，几步完成混淆、打包、加壳 |
| ✗ 没有商业化基础设施，不会收费、管客户 | ✓ 授权管理后台 + 软件商城 + 自动续费，开箱即用 |
| ✗ 企业级方案数千-数万/年，个人开发者用不起 | ✓ ¥99 一次性解锁商家身份，赠送 5 年授权额度 |

> 市面上现有加密授权方案全部面向中大型企业客户，价格高、门槛高、操作复杂——**没有人在服务"AI 做出的个人小工具"这个市场**。VibeLock 填补的正是这个空白。

---

## 能干什么（核心能力）

| 能力 | 说明 |
|---|---|
| 🔐 **代码混淆与加密** | 本地完成混淆 + AES-256 加密，源码不上传任何服务器，全程在你掌控之中 |
| 📦 **一键安装部署** | 自动打包为受保护的 EXE / 安装包（Inno Setup 等），客户拿到就能用，无需配置环境 |
| 🔑 **授权分发管理** | 硬件指纹绑定（CPU + 主板 + 硬盘），一机一码；客户自助激活、到期自动停用、换机可迁移 |
| 🔄 **自动更新** | 客户端自动检查更新、下载、静默安装，失败自动回滚；升级不丢授权 |
| 🛒 **软件商城** | 产品一键上架，终端客户浏览选购、自助购买/激活/续费，平台帮你获客 |
| 💼 **商业服务** | 企业注册、知识产权、财税、课程培训——你只管写代码，商业化琐事交给我们 |
| 💰 **融资发布** | 平台沉淀你的产品数据（用户量、收入、增长率），精准对接投资机构 |

### 四步安全方案（A/B/C/D 递进）

| 方案 | 定位 | 核心手段 | 成本 |
|---|---|---|---|
| A 基础保护 | 挡住脚本小子 | 代码混淆 + 一键打包 | 免费 |
| B 进阶加固 | 挡住初级逆向 | 原生编译（Cython/Nuitka/garble 等） | 免费 |
| C 深度加固 | 挡住中级逆向 | 深度编译 + 自写反调试 | 免费 |
| D 极致保护 | 挡住专业逆向 | 加密 Loader + 7 层反调试 + 内存保护（AI 自动生成 C 代码） | 免费 |

> **方案 D** 通过多层开源技术组合（加密 Loader + 7 层反调试 + 内存保护 + 完整性自校验），在免费前提下达到接近商业级（VMProtect 级）的保护强度。方案全部由 AI Agent 对话引导执行，无需专业安全背景。

---

## 适用场景

只要你想用代码赚钱，这套方案都能用：

- 👨‍💻 **Vibe Coding 独立开发者**：AI 一周做出小工具，源码发出去第二天就被传开 → 加密 → 上架 → 卖授权
- 👥 **1-3 人微型 SaaS 团队**：客户想要离线版，又不能让源码泄露 → 离线 EXE + 在线续费，轻量级订阅
- 🏢 **企业内部工具管理者**：公司专属工具需控制使用范围，防员工外发 → 硬件绑定 + 到期控制
- 🎓 **AI 编程训练营讲师**：课程产品被学员毕业后破解传播 → 课程绑定设备 + 年度续费，长期收益
- 💼 **自由职业开发者**：交付源码后被客户转手给同行 → 交付加密版而非源码，建立长期客户关系
- 🏫 **高校 / 培训机构**：教辅工具担心破解无限分发 → 班级授权 + 学期制过期，精准管控

---

## 怎么用（快速开始）

### 3 分钟上手

1. **加载 Skill**：将本 `skill/` 目录放入你的 AI 项目根目录（Trae 自动识别），或按下方「在不同 AI Agent 平台中加载」复制到对应平台。
2. **对话开始**：告诉 AI「帮我把这个项目加密打包成安装包」或「帮我保护代码并接入授权」，Skill 自动激活。
3. **AI 引导**：按 Step 0 → Step 4 流水线执行：扫描项目 → 出方案 → 执行加密打包 → 接入授权 → 攻防测试。

### 完整商业化闭环（全流程）

```
注册商家（¥99）→ 生成 API Token + 产品编码 → 写入 vibelock.config.json
        ↓
加密打包（方案 A/B/C/D，AI 引导）→ 植入授权机关（验签/心跳/防篡改/到期提醒）
        ↓
登记安装包 → 商家后台上传发布 → 一键上架软件商城
        ↓
客户自助购买 / 激活 / 续费 → 开发者后台看收入与客户数据
```

> 💡 不会用？可详阅《VibeLock Skill 操作指南》：https://my.feishu.cn/docx/N2wtdQ0Xuo2G0XxvztFc2Y7KnRh?from=from_copylink

---

## 增值服务的价格体系（你能拿到这个skill，已经可以免费加密打包了！）

| 项目 | 价格 | 说明 |
|---|---|---|
| **商家身份** | **¥99 一次性** | 解锁商家身份 + 永久使用 VibeLock Skill + 商城上架资格，赠送 5×365 = **1825 Credit** |
| **授权额度（Credit）** | **¥20 = 365 Credit** | 1 Credit = 1 个客户使用 1 个产品 1 天（单设备，多设备按设备数倍增）；随用随充、无有效期 |
| **商城交易抽佣** | **10%** | 仅交易成功时收取；**续费不抽佣**，仅扣开发者 Credit |
| **商业咨询 / 陪跑** | 按需定价 | 上架商城，开发者自行选购 |
| **增值服务** | 按需定价 | 企业注册（¥299-999）、小程序注册（¥199-499）、知识产权（¥500-3,000）、财税（¥200-500/月）、AI 课程等 |

**Credit 是怎么算的？** 加密了一个软件，想卖给 10 个客户各用 1 年（各 1 台设备），需要 10×365 = 3650 Credit。客户续费 → 开发者充值 Credit → 平台赚 Credit 费，形成持续订阅收入。

> 对比传统方案：企业级加密授权方案普遍数千-数万/年，VibeLock 面向 AI 个人开发者，**¥99 一次性 + 按用量计费**，无年费负担。

---

## 文件说明

| 文件 | 用途 |
|---|---|
| `VibeLock-Skill.md` | ★ 核心通用 Prompt（完整版，含全部技术栈方案/模块/测试清单） |
| `SKILL.md` | Trae 等平台上架入口（YAML 头 + VibeLock-Skill.md 全文，同版同步） |
| `prompt.md` | 精简入口 Prompt（平台装载优先用这个，含自动更新/开场介绍/环境规范） |
| `skill.json` | Skill 市场描述文件（name/version/prompt 入口/触发词） |
| `README.md` | 本文件：使用说明 |

**通用原则**：所有平台都把 `skill/` 目录作为知识文件加载即可。AI 激活后会自动执行：版本自检（Step 0.5）→ 开场介绍（Step 0.6）→ 侦察方案（Step 1）→ 执行（Step 2）→ 授权商业化（Step 3）→ 攻防测试（Step 4）。

---

## 在不同 AI Agent 平台中加载

### Trae IDE
将 `skill/` 目录放在项目根目录下，Trae IDE 会自动识别并加载 Skill（入口为 `skill.json` + `prompt.md`）。
触发词：加密、上锁、打包、授权、vibelock 等（详见 `skill.json`）。

### Cursor
推荐 `AGENTS.md` 方式（Cursor 0.46+ 原生支持）：
```
mkdir .cursor
cp skill/VibeLock-Skill.md .cursor/rules/vibelock.md   # 或直接引用
```
或旧版 rules 方式：将 `VibeLock-Skill.md` 复制到 `.cursor/rules/` 目录下。

### Claude Code
推荐官方 Skill 目录规范（避免把全文塞进 CLAUDE.md）：
```
mkdir -p .claude/skills/vibelock
cp skill/VibeLock-Skill.md .claude/skills/vibelock/SKILL.md
cp skill/prompt.md .claude/skills/vibelock/prompt.md
cp skill/skill.json .claude/skills/vibelock/skill.json
```
或精简方式：将 `prompt.md` 内容写入 `CLAUDE.md`，需要完整细节时再让 AI 读取 `VibeLock-Skill.md`。

### GitHub Copilot
将 `VibeLock-Skill.md` 复制为 `.github/copilot-instructions.md`：
```
cp skill/VibeLock-Skill.md .github/copilot-instructions.md
```

### Windsurf
将 `VibeLock-Skill.md` 复制到 `.windsurfrules`：
```
cp skill/VibeLock-Skill.md .windsurfrules
```

### Continue / Aider / Gemini CLI / DeepSeek 等支持自定义指令的 Agent
将 `prompt.md`（精简入口）作为系统指令/规则文件加载，完整细节由 AI 按需读取 `VibeLock-Skill.md`。
```
# Aider 示例
aider --read skill/VibeLock-Skill.md
# Continue：在 rules 中引用 skill/prompt.md 内容
# Gemini CLI / DeepSeek：将 prompt.md 粘贴到指令配置
```

### 支持 MCP 的平台（可选）
平台支持 MCP 时，可配合 HTTP 工具让 AI 直接调用平台 Open API（`/open/v1/*`，X-Api-Token）。
未配置 MCP 也不影响使用——Skill 会自动降级为「给出 curl / 后台精确步骤」引导（见主文档 §3.5 能力边界说明）。

### Coze / 扣子
1. 打开 Coze Bot 配置
2. 在"知识库"中上传 `VibeLock-Skill.md`
3. 在"人设与回复逻辑"中引用知识库内容

### 通义千问 / 文心一言 / Kimi / ChatGPT / Claude（纯对话）
将 `prompt.md` 或 `VibeLock-Skill.md` 的**全文内容**复制粘贴到对话开头，然后发送你的项目需求即可。
纯对话平台没有文件工具时，AI 无法自动创建 vibelock.config.json / 客户端文件——AI 会输出文件内容，你手动保存到项目对应位置。

---

## 技术栈覆盖

| 场景 | 保护手段 |
|---|---|
| Python | PyArmor / Cython / Nuitka / PyInstaller |
| Node.js / JS / TS | javascript-obfuscator / bytenode / Node.js SEA |
| Go | garble / gobfuscate |
| Java / Kotlin | ProGuard / ClassFinal / jpackage / JNI |
| .NET / C# | Obfuscar / ConfuserEx 2 / NativeAOT |
| C / C++ | OLLVM / 加密 Loader + 7 层反调试 |
| Rust | obfstr / goldberg / OLLVM |
| Electron | bytenode / 原生模块 / electron-builder |
| Dart / Flutter | flutter build --obfuscate / FFI 原生模块 |
| SaaS 后端 | 编译部署 / 微服务隔离 / 零信任架构 |
| 移动端 / RN / uni-app | ProGuard-R8 / Hermes / 原生插件（深度方案完善中） |

> 更详细的 API 说明：《VibeLock_OpenAPI 文档》https://my.feishu.cn/docx/PSBsdct5wong8txDuO6c94mRnVc?from=from_copylink

---

## 常见问题（FAQ）

**Q：需要安装什么工具吗？**
A：Skill 自身零本地依赖，不捆绑任何工具脚本。执行方案时，AI 会按你的技术栈引导安装对应的开源工具（如 PyArmor、garble 等）。

**Q：代码安全吗？会传到服务器吗？**
A：代码混淆与 AES-256 加密**全程在本地完成，源码不上传任何服务器**。平台只保存你的加密产物与授权数据。

**Q：小白真的能用吗？**
A：能。方案 A 复制粘贴命令 30 分钟搞定；方案 D 由 AI Agent 自动生成 C 代码，按引导操作即可，无需专业安全背景。

**Q：你们的方案能挡住所有攻击者吗？**
A：纯软件保护没有绝对安全。方案 A/B/C 能挡住 95% 的自动化攻击和脚本小子、初级逆向工程师；方案 D 通过 7 层纵深防御能挡住大部分专业逆向工程师。目标是"让破解成本 > 软件价值 × 3"。

**Q：如何收费？**
A：¥99 一次性解锁商家身份（含 Skill + 5 年授权额度），后续按用量充值 Credit（¥20 = 365 Credit），商城交易抽佣 10%，续费不抽佣。

---

## 官网 / 商家后台

- 官网（产品展示页）：**https://lock.pandlee.cn/**
- 商家后台 / 注册登录 / 商城 C 端：**https://lock.pandlee.cn:8088**
- ⚠️ API 基址固定 **https://lock.pandlee.cn:8088**（443 不提供 API），所有 /api/* 与 /open/v1/* 均拼在 8088

---

## 作者与关注

本 Skill 由 **Pandlee（熊黎）** 创作。欢迎关注抖音 **@熊黎 | PandLeeAI**，获取更多 AI 开发者安全与商业化实战内容。
<img width="522" height="647" alt="image" src="https://github.com/user-attachments/assets/cf741deb-71ca-41b0-873e-4d8d9dd8c084" />


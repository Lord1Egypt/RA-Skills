---
name: web-builder
description: "从零构建网站和 Web 应用，使用结构化的计划驱动工作流。触发条件：用户要求创建/构建/搭建网站、Web应用、落地页、管理后台、Dashboard 或任何 Web 项目。关键词：'做网站'、'做页面'、'做前端'、'搭建系统'、'做个官网'、'做个后台'、'build website'、'create app'。覆盖静态站、SPA、全栈应用、前后端分离项目。"
---

# Web Builder Skill

通过结构化的计划驱动工作流构建 Web 项目：先搞清楚需求，再选对架构，然后逐页实现。

**开始前必读**：

- 阅读 [frontend-design.md](frontend-design.md) 了解前端设计的美学准则，每个项目都应该有独特的视觉风格
- 阅读 [plan-template.md](plan-template.md) 了解 plan.md 的结构和应包含的内容

## 恢复检查（每次必须先做）

开始任何工作之前，先检查计划文件是否已存在：

```
查找：当前工作目录下的 .web-builder/plan.md
```

**文件已存在**：读取内容，告诉用户上次做到哪了，从当前阶段继续。不要重新开始。

**文件不存在**：从下面的 Phase 0 开始。

---

## Phase 0：需求采集

用 [plan-template.md](plan-template.md) 中的模板创建 `.web-builder/plan.md`。

分轮提问，不要一次性丢一堆问题：

### 第一轮（必问，3 个问题）：

1. 你要做什么？一句话说清楚。
2. 给谁用的？
3. 有没有喜欢的参考网站？（一个 URL 能省掉十个问题）

**用户回答后立刻更新 plan.md。**

### 第二轮（根据项目类型追问）：

| 信号        | 追问                                 |
| ----------- | ------------------------------------ |
| 展示/营销类 | 几个页面？什么设计风格？有品牌色吗？ |
| 工具/后台类 | 核心功能？数据从哪来？需要登录吗？   |
| 内容/博客类 | 谁来发内容？要评论吗？内容怎么分类？ |
| 电商类      | 多少商品？需要支付吗？库存管理？     |

### 第三轮（按需）：

- 有技术偏好吗？（"我们团队用 Vue"）
- 需要移动端适配吗？（默认：需要）

### 智能推断原则

**第一轮必问**，不可跳过。第二轮、第三轮时，若能从用户回答中推断出答案，则无需追问。

**推荐方案时**直接给出具体技术栈供用户确认，不要问"你想用什么框架？"。参考下表：

| 用户说                   | 推断               | 推荐方案                    |
| ------------------------ | ------------------ | --------------------------- |
| "做个博客"               | 全栈，需要内容管理 | Next.js + MDX 或 Prisma     |
| "做个产品介绍页"         | 静态，纯展示       | Vite + Tailwind             |
| "做个管理后台"           | SPA，复杂交互      | React + shadcn/ui + Zustand |
| "做个xxx，后端用 Python" | 前后端分离         | Vite + FastAPI              |
| "做个公司官网"           | 静态或简单 SSR     | Vite + React 或 Astro       |

---

## Phase 1：项目定型

根据采集结果匹配以下原型之一，更新 plan.md 中的原型、技术栈和目录结构。

### 原型：`static`（静态站）

**匹配条件**：纯展示、内容固定、不需要登录、不需要数据库。

```
技术栈：Vite + React + Tailwind CSS（多页面可选 Astro）
```

目录结构：

```
/
├── src/
│   ├── components/
│   ├── pages/            # 多页面场景
│   ├── assets/
│   ├── App.tsx
│   └── main.tsx
├── public/
├── index.html
├── package.json
├── vite.config.ts
├── tailwind.config.ts
└── tsconfig.json
```

### 原型：`spa`（单页应用）

**匹配条件**：复杂交互、管理后台、Dashboard、不需要 SEO。

```
技术栈：React 18 + Vite + Tailwind + shadcn/ui + Zustand + React Router v7
```

目录结构：

```
/
├── src/
│   ├── components/
│   │   ├── ui/           # shadcn 组件
│   │   └── layout/       # Header, Sidebar, Footer
│   ├── pages/
│   ├── hooks/
│   ├── stores/           # Zustand 状态管理
│   ├── services/         # API 调用
│   ├── types/
│   ├── utils/
│   ├── App.tsx
│   └── main.tsx
├── public/
├── package.json
├── vite.config.ts
└── tailwind.config.ts
```

### 原型：`fullstack`（全栈一体）

**匹配条件**：需要登录、需要存数据、需要 SEO、动态内容管理。

```
技术栈：Next.js 15 (App Router) + Tailwind + shadcn/ui + Prisma
```

目录结构：

```
/
├── src/
│   ├── app/
│   │   ├── (public)/     # 公开页面
│   │   ├── (auth)/       # 需要登录的页面
│   │   ├── api/          # API 路由
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   ├── lib/              # 数据库、认证等
│   └── types/
├── prisma/
│   └── schema.prisma
├── public/
└── package.json
```

### 原型：`separated`（前后端分离）

**匹配条件**：明确要求分离、Python 后端、多端共享 API、团队分工。

```
技术栈：
  前端：React + Vite + Tailwind
  后端：Express/Fastify (Node) 或 FastAPI (Python)
```

目录结构：

```
/
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.ts    # 代理到后端
├── backend/
│   ├── src/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── models/
│   │   └── index.ts
│   └── package.json      # Node 后端
│   # 或 app/main.py       # Python 后端（依赖在 README 中说明，默认不生成 requirements.txt）
└── README.md
```

---

## Phase 2：页面与组件规划

拆解所有页面和共享组件，更新 plan.md：

1. **路由表**：每条路由、页面名、描述、状态（⬜）
2. **共享组件**：Header、Footer、Sidebar、Card、Button 等
3. **数据模型**：有后端的话定义类型/Schema

---

## Phase 3：逐步实现

**编码注意**：

- 避免在代码、注释、字符串中使用特殊 Unicode 字符（如 emoji、不常见符号），使用标准 ASCII 或常见中文字符

**文件写入方式**：

1. 调用 `start_write_file` 进入写作模式
2. 直接输出代码文本内容
3. 调用 `end_write_file` 退出写作模式
   **禁止使用 Python 脚本写入代码文件（会有转义问题）**

### 构建顺序（铁律，必须按此顺序）：

```
第1步：项目结构   → 创建目录、配置文件，在依赖管理文件中记录所需依赖（不执行安装）
第2步：全局样式   → Tailwind 配置、CSS 变量/Design Tokens、基础样式
第3步：布局骨架   → Header + Footer + 主内容区（共享布局）
第4步：路由占位   → 所有路由指向占位页面（"即将上线"）
第5步：逐页实现   → 按路由表顺序，一次一个页面
第6步：数据对接   → 接入真实 API / 数据库（如有）
```

### 单页面实现流程：

```
1. 创建页面文件 + 注册路由
2. 搭页面骨架（用注释划分区域）
3. 从上到下实现各区域
4. 填充模拟数据
5. 响应式检查（手机 → 平板 → 桌面）
6. 接入真实数据（如有）
7. 添加交互和过渡动效
8. 在 plan.md 中标记该页面为 ✅
```

### 每完成一个模块（如"项目结构 + 全局样式"、"布局 + 路由"、"页面实现"、"数据层"），立刻更新 plan.md 的进度。

---

## Phase 4：验证与收尾

全部代码写完后，统一安装依赖并验证项目能否正常运行：

```
1. 安装依赖（前后端分离项目需分别安装；Python 后端用 pip install 一次性安装所需包）
2. 执行构建，确保编译无报错（注意检查导入路径、类型定义、未使用的变量等常见问题）
3. 启动开发服务器，逐一访问各路由确认正常渲染
4. 检查浏览器控制台无红色错误
5. 如有后端：确认 API 接口可正常返回数据
```

**执行 npm 命令时**，使用 Python subprocess 并设置正确的编码：

```python
import subprocess
env = dict(subprocess.os.environ)
env["NODE_OPTIONS"] = ""
subprocess.run("npm run build", shell=True, cwd="项目路径",
               encoding="utf-8", errors="replace", env=env)
```

发现问题则修复后重新验证，直到项目能完整跑通。

### 打磨清单：

```
- [ ] 响应式适配（手机/平板/桌面，手机端无水平滚动）
- [ ] 所有可点击元素有 hover/active/focus 状态
- [ ] 加载状态（骨架屏或转圈，不能白屏）
- [ ] 错误状态（友好提示，不是报错堆栈）
- [ ] 空状态（没有数据时给有用的提示）
- [ ] 表单验证 + 行内错误提示
- [ ] favicon 已设置
- [ ] README.md 包含：项目简介、本地启动步骤、目录说明
- [ ] plan.md 所有项目标记为 ✅
```

### README 模板：

最终的 README.md 必须包含：

```markdown
# 项目名称

一句话描述。

## 快速开始

### 环境要求

（根据项目实际情况列出，如 Node.js、Python 等）

### 安装与运行

（本地安装依赖和启动的完整步骤，Python 项目需列出所需的包）

## 目录结构

（简要目录说明）

## 技术栈

（使用的关键技术列表）
```

---

## Phase 5：启动交付

build 通过后，启动开发服务器并输出访问地址。

**⚠️ 重要：启动和读取地址必须在同一段代码中完成，禁止拆成多段代码。**

```python
import subprocess, time, os, re, socket, random

def get_free_port():
    """获取一个可用的随机端口"""
    for _ in range(10):  # 最多尝试10次
        port = random.randint(10000, 65535)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return 5173  # 降级到默认端口

port = get_free_port()
env = dict(os.environ)
env["NODE_OPTIONS"] = ""
process = subprocess.Popen(
    f"npx vite --port {port} --host",
    shell=True,
    cwd="项目路径",
    env=env,
    stdin=subprocess.DEVNULL,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)

time.sleep(6)
output = process.stdout.read1(65536).decode("utf-8", errors="replace")
print(output)

local_url = network_url = None
for line in output.splitlines():
    m = re.search(r"https?://[^\s]+", line)
    if m:
        if "localhost" in line or "127.0.0.1" in line or "Local" in line:
            local_url = m.group()
        elif "Network" in line:
            network_url = m.group()

if local_url:
    print(f"本地访问: {local_url}")
if network_url:
    print(f"局域网访问: {network_url}")
```

**关键点**：

- **使用随机端口**：每次生成 10000-65535 范围内的随机端口，避免冲突
- `stdin=subprocess.DEVNULL`：必须加，防止任何交互式提示阻塞进程
- **直接用 `npx vite`**：指定端口和 `--host` 参数，不依赖 `package.json` 配置
- 启动 + 获取地址必须在同一段代码完成，拿到地址表示项目已完成，更新 plan.md 并交付

**输出访问链接**（使用 Markdown 超链接格式 `[文本](URL)`）：

- 本地访问：`[本地访问 http://localhost:端口](http://localhost:端口)`
- 局域网访问：`[局域网访问 http://本机IP:端口](http://本机IP:端口)`

更新 plan.md 标记项目已完成并交付。

---

## 代码质量基线（默认执行，不需要问用户）

**UI/UX：**

- 所有可交互元素必须有 hover/active/focus 样式
- 不允许白屏 —— 加载时必须有骨架屏或 spinner
- 表单必须有输入验证 + 错误提示
- 手机端：不能出现横向滚动条，点击区域不小于 44px

**代码：**

- TypeScript strict 模式，不用 `any`
- 单组件不超过 200 行，超了就拆
- 只用 Tailwind class，不写内联 style
- 颜色/间距/字号用 design token 或 CSS 变量，不写魔法数字
- 图片加 `loading="lazy"`（或框架等效方案）

**工程：**

- `package.json` 的 scripts 至少有 `dev` 和 `build`
- 不留无用依赖
- 配置了路径别名的话统一使用
- Python 项目：不生成 `requirements.txt`，在 README 的"安装与运行"中列出所需的 pip install 命令

---

## 核心原则

| 原则             | 含义                                       |
| ---------------- | ------------------------------------------ |
| **先规划再动手** | 先写 plan.md，确认后再写代码               |
| **先写后验**     | 先写完所有代码，最后统一安装依赖、启动验证 |
| **推断优先**     | 能推断就不问，给方案让用户确认/否决        |
| **逐步交付**     | 一个页面一个页面做，每步可验证             |
| **计划即真相**   | 所有进度记在 plan.md 里，不在聊天记录里    |

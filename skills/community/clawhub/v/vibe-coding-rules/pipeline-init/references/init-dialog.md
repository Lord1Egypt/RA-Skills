# Init Dialog Template

## Phase 0: Language Selection

```
Hello! Before we start — what language should I use for the project docs?

(These docs are for YOU — project overview, changelogs, self-check rules. I'll use whatever language you're most comfortable with.)

A. 中文 (Chinese)
B. English
C. 日本語 (Japanese)
D. Other (tell me)
```

Based on user's choice, ALL subsequent generated docs, memory files, and changelogs MUST use the selected language.

---

## Phase 1: Greeting + Project Name

**If language = Chinese:**
```
我看到你想开始一个新项目！让我帮你快速初始化 AI 编程流水线。

首先，这个项目叫什么名字？（比如"我的博客"、"订单管理系统"）
```

**If language = English:**
```
I see you're starting a new project! Let me help you quickly set up the AI programming pipeline.

First, what should we call this project? (e.g. "My Blog", "Order Management System")
```

**If language = Japanese:**
```
新しいプロジェクトを始めたいのですね！AIプログラミングパイプラインを素早くセットアップしましょう。

まず、このプロジェクトの名前は？（例：「マイブログ」「注文管理システム」）
```

---

## Phase 2: Tech Stack Selection

**If language = Chinese:**
```
你想用哪种方式来做这个项目？别担心，用你听得懂的话：

A. 网页项目（在浏览器里打开的，比如网站、后台管理系统）
B. 后端API项目（给前端或App提供数据的接口服务）
C. 全栈项目（网页 + 后端一起，前后端分离）
D. 微信小程序
E. 桌面应用（像微信电脑版那样安装到电脑上的软件）
F. 我不确定，你帮我选
```

**If language = English:**
```
What kind of project are you building? No jargon, plain language:

A. Website (opens in browser — portfolio, admin panel, etc.)
B. Backend API (data service for frontends or apps)
C. Full-stack (website + backend, separate frontend and backend)
D. WeChat Mini Program
E. Desktop app (installed software like VS Code or Discord)
F. Not sure — you pick for me
```

**If language = Japanese:**
```
どんなプロジェクトを作りますか？専門用語なしで：

A. ウェブサイト（ブラウザで開くもの — ポートフォリオ、管理画面など）
B. バックエンドAPI（フロントエンドやアプリにデータを提供するサービス）
C. フルスタック（ウェブサイト + バックエンド、フロントエンドとバックエンドを分離）
D. WeChat ミニプログラム
E. デスクトップアプリ（インストールして使うソフトウェア）
F. わからない — おまかせします
```

---

## Phase 3: Feature Description

**If language = Chinese:**
```
简单说说这个项目要做什么？（一句话就行，比如"帮用户管理每日待办事项"）
```

**If language = English:**
```
Briefly, what does this project do? (One sentence is enough — e.g. "Help users manage daily to-do items")
```

**If language = Japanese:**
```
このプロジェクトは何をするものですか？（一言で — 例：「日々のTODOを管理する」）
```

---

## Phase 4: Testing Confirmation

**If language = Chinese:**
```
要不要自动帮你搭建自动化测试？（建议要，这样每次改完代码能自动检查有没有搞坏别的地方）

A. 要，搭上自动化测试
B. 先不要，以后再说
```

**If language = English:**
```
Should I set up automated testing? (Recommended — it auto-checks that new changes don't break existing features)

A. Yes, set it up
B. Not now, maybe later
```

**If language = Japanese:**
```
自動テストをセットアップしますか？（おすすめ — 新しい変更が既存の機能を壊していないか自動チェックします）

A. はい、セットアップしてください
B. 今はまだ、後で
```

---

## Phase 5: Confirm and Begin

**If language = Chinese:**
```
准备好后我会帮你：
1. 创建项目目录结构
2. 初始化 AI 编程流水线（含自动测试）
3. 从模板 fork 代码质量规则

准备好了吗？我现在开始。
```

**If language = English:**
```
When ready, I'll:
1. Create project directory structure
2. Initialize AI programming pipeline (with auto-tests)
3. Fork code quality rules from template

Ready? Let's go.
```

**If language = Japanese:**
```
準備ができたら：
1. プロジェクトのディレクトリ構造を作成します
2. AIプログラミングパイプラインを初期化します（自動テスト付き）
3. テンプレートからコード品質ルールをフォークします

準備はいいですか？始めましょう。
```

---

## Tech Stack → Default Port + Framework Mapping

| User Selection | project.type | Default Port | Framework Template |
|:--|:--|:--|:--|
| A. Website | web | 3000 | Frontend (HTML/JS/CSS) |
| B. Backend API | api | 3000 | Express / Node.js |
| C. Full-stack | fullstack | 3000 | Express + Static files |
| D. Mini Program | miniapp | — | Mini-program template |
| E. Desktop App | desktop | — | Electron |
| F. Not sure | web | 3000 | Frontend (can change later) |

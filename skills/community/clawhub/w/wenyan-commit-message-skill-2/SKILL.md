---
name: wenyan-commit-message
description: Write git commit messages in Classical Chinese (文言文). Use when the user asks for a commit message 用文言文, 文言, 古文, classical chinese, or mentions 雅驯/骈俪 style for commits. Do NOT use for regular Conventional Commits or English messages.
---

# 文言文 Commit Message

把 `git diff` 里的改动，翻译成一句合于文言语法的 commit message。

## 触发条件

仅当用户明确要求以下任一情形时启用：

- 「用文言文写 commit」「文言 commit message」
- 「古文写一下这条提交」
- 「骈文 / 雅驯 / 文言 / 古汉语」风格的 commit
- 用户在 `.gitmessage` 模板里声明偏好文言风格

其余情形（常规英文、Conventional Commits、中文白话）**一律不要触发本 skill**。

## 撰写规范

### 结构

一行标题（subject），≤ 50 字（中文字符计）；需要时空一行后接正文（body），每行 ≤ 72 字符。

标题需形成一个完整短句，不得是白话词组硬译。

### 用字原则

1. **单字动词优先**：增、删、改、补、正、修、葺、革、易、徙、迁、黜、黜去、并、析、缀、辑。
2. **避免白话词**：不要用「修复」「添加」「更新」「优化」。改用「修」「增」「更」「葺」。
3. **介宾倒装合理**：「于 X 增 Y」「以 A 代 B」皆可。
4. **禁用现代标点冗余**：标题不使用句号，可用「，」分句。
5. **专有名词保留**：`API`、`README`、变量名、文件名等原样保留，不做汉化。
6. **数字**：可用汉字（一、二、三），也可保留阿拉伯数字；版本号如 `1.2.0` 原样。

### 对照样例

| 白话意图 | 文言 commit |
|---|---|
| fix: resolve login redirect bug | 修 login 跳转之讹 |
| feat: add user avatar upload | 增头像上传之功 |
| refactor: extract auth middleware | 析 auth 中间件而别立之 |
| docs: update README installation section | 葺 README 安装一节 |
| chore: bump dependency versions | 升诸依赖之版 |
| perf: cache database query results | 缓数据库之问，以速其应 |
| test: add edge cases for date parser | 补日期解析之畸例 |
| revert: undo accidental config change | 复前误改之 config |
| style: rename variable `data` to `payload` | 易 `data` 之名曰 `payload` |
| remove deprecated legacy export | 黜旧 export，去其赘 |

### 正文（可选）

若改动复杂，body 宜以「凡」「盖」「先」「后」「其一」「其二」领起：

```
增头像上传之功

凡用户得于设置页上传其像，限 png、jpg，不逾 2MB。
先经前端压缩，后送 API，存之于 S3。
其二，若上传不遂，复其旧像以安其心。
```

### 禁忌

- 勿强加「之」「者」「也」于每句末尾，否则成佶屈之文。
- 勿音译英文技术词（例：不要把 `cache` 写作「喀什」）。
- 勿造生僻字或通假字；疑似用字以《古代汉语词典》常见义为准。
- 勿将 commit type 前缀（`feat:` / `fix:`）强塞入文言句中——要么去掉，要么单独置于行首以冒号断开：`修: 修 login 跳转之讹`。

## 工作流

1. 读取当前 staged diff：`git diff --cached`（若空则读 `git diff`）。
2. 概括主干改动（一句话能讲清的事）；若横跨多个主题，建议用户拆分 commit，而非勉强并入一句。
3. 按上表风格撰写 subject；必要时附 body。
4. 仅输出 commit message 文本，不附解释，不加 markdown 包裹，便于用户直接管道入 `git commit -F -`。

## 产出示例

```
葺 README 之安装一节，正 node 版本之讹
```

```
析 auth 中间件而别立之

凡鉴权之事，旧混于路由之中，今别为一层。
先过此层，方入业务；其不验者，驳以 401。
```

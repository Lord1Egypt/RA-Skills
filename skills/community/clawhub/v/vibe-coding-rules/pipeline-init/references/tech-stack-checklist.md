# 技术栈依赖检测清单

## 检测流程

初始化时必须检测以下依赖，检测失败时给出安装指引（普通人也能看得懂）。

### 1. Node.js

**检测命令**：`node -v`

**最低版本**：16.0.0

**安装指引**：
```
看起来你的电脑还没有装 Node.js。这是运行 JavaScript 项目的必备工具。

安装很简单：
1. 打开浏览器，访问 https://nodejs.org
2. 点击左边那个绿色大按钮（LTS 版本，稳定版）
3. 下载完成后，双击打开，一路点"下一步"直到完成
4. 装完后关掉当前窗口重新打开，就好了
```

### 2. npm

**检测命令**：`npm -v`

**最低版本**：8.0.0（随 Node.js 自带）

### 3. Git

**检测命令**：`git --version`

**安装指引**：
```
你的电脑还没有装 Git。这是用来管理代码版本的工具。

安装步骤：
1. 打开浏览器，访问 https://git-scm.com/download/win
2. 下载 Windows 版本
3. 双击打开，一路点"下一步"（所有选项都用默认的）
4. 装完后关掉当前窗口重新打开
```

### 4. 按技术栈额外依赖

| 技术栈 | 需检测 | 命令 |
|:--|:--|:--|
| 网页项目 | — | 无需额外依赖 |
| 后端API | — | Node.js 自带 |
| 全栈项目 | — | Node.js 自带 |
| 微信小程序 | 微信开发者工具 | 需手动安装 |
| 桌面应用 | Electron | `npx electron --version` |

### 5. 自动化测试依赖（如果用户选"要"）

| 依赖 | 检测命令 | 安装 |
|:--|:--|:--|
| Playwright | `npx playwright --version` | `npm install playwright` |
| tesseract.js | `node -e "require('tesseract.js')"` | `npm install tesseract.js` |
| sharp | `node -e "require('sharp')"` | `npm install sharp` |

## 检测结果处理

- **全部通过** → 继续步骤 3
- **有缺失** → 列出缺失项 + 安装指引 → 用户决定是否现在修
  - 基础依赖（Node.js/npm/Git）缺失时**强烈建议先装**
  - 测试依赖缺失时可以标记为"后续再装"

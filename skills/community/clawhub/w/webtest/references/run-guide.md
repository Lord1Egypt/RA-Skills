# 运行指南（Run Guide）

本文件说明「你怎么发起一次真实网站测试」。本 skill 支持两种方式，按需选用。

## 方式一：让 WorkBuddy 帮你跑（推荐，最省事）

你不需要自己装环境。在对话里按下面格式把信息发给我，我会：

1. 加载本 skill（拿到测试流程与断言规范）
2. 调用浏览器自动化能力（agent-browser，已在本机配好 Edge 兜底）
3. 实跑并生成 Markdown 报告（含每步结果、截图、缺陷清单）

**你要提供的信息格式：**

```
网址：https://你的网站
测试点：登录、搜索、下单流程（挑你想测的，可多选）
断言：登录成功跳转首页；搜索"耳机"出现结果列表；下单后显示订单号
环境：如需登录，提供测试账号 test@x.com / 123456（仅本次会话使用，不外存）
```

**要点：**

- 只测你有权限的网站；公开页面（无需登录）最稳，适合先验证流水线。
- 动态内容（验证码、实时价格、随机昵称）用「形态断言」而非精确匹配，例如"包含数字""存在按钮"。
- 跑完我会把报告（含截图路径）直接给你，并标注"自动化测试结论，建议人工复核关键路径"。

## 方式二：自己命令行跑（agent-browser CLI）

适合你想完全自己掌控、或在 CI 里跑。基于已验证的 Windows 配置（官方 Chromium 下载失败时用本机 Edge 兜底）：

```bash
# 1) 安装 CLI（用隔离的 managed node，避免污染系统）
npm install -g agent-browser

# 2) 官方 Chromium 下载失败 → 借本机 Edge（Chromium 内核，协议兼容）
export AGENT_BROWSER_EXECUTABLE_PATH="C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"

# 3) 驱动（Windows 必须加 MSYS_NO_PATHCONV=1，否则 C:/ 会被错拼成 d:\c\）
MSYS_NO_PATHCONV=1 agent-browser --executable-path "$AGENT_BROWSER_EXECUTABLE_PATH" --args "--no-sandbox" open "https://你的网站"
MSYS_NO_PATHCONV=1 agent-browser snapshot -i        # 取可交互元素，得到 @eN 元素ID
MSYS_NO_PATHCONV=1 agent-browser fill "@e6" "内容"  # 按元素ID填表
MSYS_NO_PATHCONV=1 agent-browser click "@e4"        # 点击
MSYS_NO_PATHCONV=1 agent-browser get url            # 取 URL，用于断言
MSYS_NO_PATHCONV=1 agent-browser screenshot out.png # 留证
MSYS_NO_PATHCONV=1 agent-browser close              # 关闭（换参数前必须先 close）
```

> 元素 ID（`@e6` 等）每次 `snapshot -i` 会变，以当次快照为准。
> 更多坑点见 `references/windows-edge-fallback.md`。

## 发布打包须知（作者用）

- 打发布包时**务必排除 `run-reports/`**：官方 `package_skill.py` 用 `rglob('*')` 无法排除目录，会把测试报告、截图一并打进 zip。请用一次性打包脚本（遍历目录、跳过 `run-reports/` 路径段）重新生成 `webtest.zip`，产物只含 `SKILL.md` + `PUBLISH.md` + `references/`。
- 为什么排除：`run-reports/` 存放你的私有实测记录（可能含站点特征、截图），随包外发既泄露又臃肿；且测试报告是运行产物，不是技能本体。
- 完整后台控制台测试套路（登录→仪表盘→侧栏→列表→搜索）见 `references/admin-console-flow.md`。

## 合规提醒

- 仅测你明确授权的网址；不绕过登录鉴权、不测未授权系统。
- 测试账号 / 密码仅在本次会话使用，不写入 skill 外部文件。
- 断言失败 ≠ bug，需区分"实现差异"与"真实缺陷"，报告中注明。

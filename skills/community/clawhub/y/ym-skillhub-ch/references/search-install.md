# 搜索与安装第三方技能

SkillHub 是国内优先的技能源，比公共 registry 更快、更合规。**装别人的技能等于把别人
的代码放进自己的技能目录**，所以流程里最值钱的是「隔离 + 审查」两步，不是安装命令本身。

## 一、搜索

```bash
skillhub search <关键词>
```

搜索结果里每行形如 `- install: skillhub install <slug> --namespace <ns>`，
可直接复制，**只需补上 `--dir`**。

**先分清是「技能」还是「发布方」**：用户说「安装 XX 技能」时，XX 可能是一个命名空间
（发布方）而不是单个技能。例如「零一数科」= 命名空间 `org-28ib33ph`，下挂 19 个 `lingyi-*`
技能。是发布方就先列清单让用户挑，别自作主张装第一个。

判据：看搜索结果里有没有明确的 `slug`（单个技能）而只有 `namespace`。拿不准就先搜一次再问。

## 二、安装命令

```bash
skillhub install <slug> --namespace <namespace> --dir "<你的技能目录，Windows 绝对路径>"
```

例（Windows）：`--dir "%USERPROFILE%\.workbuddy\skills"` 展开后的实际路径。

> ⚠️ `--dir` 必须用 **Windows 绝对路径**。传 MSYS 风格 `/c/Users/...` 时，原生 python 会把它
> 当**相对当前盘**解析，实际装到 `D:\c\Users\...`（当前盘是 D: 时）。
> 识别特征就是路径里**凭空多出一层盘符目录**（如 `D:\c\Users\...`）—— 排查误装时按这个找。

CLI 的 `config` 子命令只支持 `list`（企业源），**不能持久化默认 `--dir`**，所以每次都要显式传。

## 三、安装前：平台侧安全与质量信息

```bash
skillhub skill reports <slug> --namespace <ns>      # 安全报告链接（腾讯云）
skillhub skill evaluation <slug> --namespace <ns>   # 边界/触发质量评分
```

这两个是**装之前**看的，不是装之后。`reports` 给安全扫描结论，`evaluation` 给技能的
边界清晰度与触发词质量评分 —— 评分低的技能装回来也容易乱触发。

## 四、隔离安装的完整流程（第三方技能必须走）

1. **搜索** → 汇总候选（名称 / 命名空间 / 版本 / 一句话功能 / 是否需付费 Key），让用户挑。
2. **隔离安装**：`--dir` 指向临时 quarantine 目录（如 `<临时目录>/_quarantine/<slug>`），
   先不碰正式技能目录。
3. **逐文件审查**，重点扫这些模式：

   | 关注点 | 具体看什么 |
   |---|---|
   | 命令执行 | `os.system` / `subprocess` / `os.popen` |
   | 动态执行 | `eval` / `exec` / `compile` |
   | 破坏性文件操作 | `rmtree` / `os.remove` / `shutil.rmtree` / `unlink` |
   | 外联 | 硬编码域名 / IP（尤其是非国内、非平台域名） |
   | 越权读取 | 读取与技能功能无关的路径（`~/.ssh`、浏览器 profile、其他技能目录） |
   | 凭据 | 内置 API Key / token，或把本地凭据往外传 |

   同时把 `reports` + `evaluation` 的结论一起给用户。
4. **冒烟测试**：在缺 Key / 缺输入的情况下跑一次，确认「不发起任务、不扣点、退出码符合文档」。
   这一步能拦掉「参数一不满足就静默干了别的事」的技能。
5. **告知风险再拍平**：明确说清会上传什么数据到哪里、是否扣费、是否需要配置 Key。
6. **拍平落位**（见下节）+ 改 lock 文件。
7. 提示用户：新技能可能要**重启 WorkBuddy** 才被识别。

## 五、命名空间嵌套：装完 WorkBuddy 扫不到

用 `--namespace` 装的社区技能落位是两层：

```
~/.workbuddy/skills/@<namespace>/<slug>/SKILL.md    ← 嵌套，WorkBuddy 不认
```

WorkBuddy 只扫平铺的 `~/.workbuddy/skills/<name>/SKILL.md`。必须拍平：

```powershell
$base   = Join-Path $env:USERPROFILE ".workbuddy\skills"
$nested = Join-Path $base "@<namespace>\<slug>"
$flat   = Join-Path $base "<slug>"
Move-Item -LiteralPath $nested -Destination $flat -Force
Remove-Item -LiteralPath (Join-Path $base "@<namespace>") -Recurse -Force -Confirm:$false
```

然后把 `~/.workbuddy/skills/.skills_store_lock.json` 里该条目的 `installDir` 改成拍平后的路径
—— **不改的话 `skillhub upgrade` 找不到它**，以后升级会装出第二份。

> `Remove-Item -Recurse -Force` 建议加 `-Confirm:$false`，否则在 PowerShell 工具里可能因
> 交互确认而整段脚本中断。

## 六、安装后的已知限制

- `skillhub list` **看不到**用 `--dir` 装的技能（它只扫默认目录），别因为列表里没有就以为没装上。
- `skillhub verify` 对社区命名空间返回 **HTTP 405**，不是技能有问题。
- 新技能常需要重启 WorkBuddy 才出现在可用技能列表里。

## 七、slug 占用自查（给自己要发的技能起名时用）

```bash
python scripts/check_slug.py ym-foo ym-bar ym-baz
python scripts/check_slug.py --file candidates.txt   # 每行一个，# 开头忽略
python scripts/check_slug.py --json ym-foo           # 机器可读
```

判据是下载接口 `GET /api/v1/download?slug=<slug>`：200 = 已有同名已发布技能，404 = 公开层面无。

**三条局限，别用错**：

1. **404 ≠ 可用** —— 已被占用但尚未公开发布（草稿 / 审核中 / 私有）的同样是 404。
   实测反例：`skill-generator` 被占用（发布直接被拒），但下载 404、搜索零命中。
2. **自己发的技能也返回 302/200** —— 这个接口不能区分「谁发的」。
   要认作者看 search 结果里的 `namespace.handle` / `owner.handle`。
3. **搜索接口不能判重** —— `search?q=` 是模糊匹配，对 `ym-xxx` 这类带短前缀的词会直接返回
   兜底热门列表（`self-improving-agent`、`tencent-docs`、`find-skills` …），
   看着像「无结果」其实只是没匹配上。参数名是 **`q`**，传 `query=` / `keyword=` 会走另一套逻辑（返回热门榜）。

**结论**：脚本只能批量排除「已被别人发布」的名字，最终仍要在发布表单里填一次，由服务端给权威判定。

## 八、改名要三处同步

绑 GitHub 仓库发布时，平台是**扫仓库自动推导** slug 的 —— slug 取自 SKILL.md 的 `name` 字段，
光改发布表单无效，必须改仓库里的 `name`。

**建议 `name` / 目录名 / 仓库名三处一起改**，保持一致，避免以后 `skillhub install <slug>` 对不上。

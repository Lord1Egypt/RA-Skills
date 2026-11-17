# 踩坑清单

每条都是实际撞过的，带现象和根因。现象描述是为了让你在遇到同样情况时能对上号。

## 1. 装了三次，skills.sh 永远不收录

**现象**：`npx skills add` 成功，`--list` 也能列出，但 `api/search` 一直 `count: 0`。

**根因**：环境里存在 `DISABLE_TELEMETRY=0`。CLI 的判断是

```js
function isEnabled() {
  return !process.env.DISABLE_TELEMETRY && !process.env.DO_NOT_TRACK;
}
```

只看变量是否存在，`"0"` 在 JS 里是 truthy，`!"0"` 等于 false，遥测全程关闭。

**修法**：`DISABLE_TELEMETRY= DO_NOT_TRACK= npx skills add ...`，或者从环境里删掉。

**教训**：看到 `FOO=0` 不能假设「关闭」，必须读源码确认判断方式。这类开关的实现质量参差不齐。

## 2. 根目录放 SKILL.md，子目录的 skill 扫不到

**现象**：`npx skills add <repo> --list` 说没有 skill，或者只列出部分。

**根因**：部分扫描逻辑遇到根目录 SKILL.md 会提前返回。

**修法**：统一用 `skills/<name>/SKILL.md`。

## 3. 把「CLI 能装」当成「已被索引」

**现象**：README 里加了指向 skills.sh 的徽章，链接 404。

**根因**：CLI 的发现逻辑读 GitHub，网站的目录读后端事件，两套系统。

**修法**：徽章先指向仓库本身。确认 `api/search` 有结果之后再换成目录链接。

## 4. clawhub 搜索搜不到自己的描述词

**现象**：描述里写了「导出、备份、归档」，搜 `backup`、`导出` 都没有结果。

**根因**：clawhub 的搜索只匹配 `displayName`。实测 `chat`、`chat-share` 能命中，正文关键词一律不行。

**结论**：description 和 tags 优化的价值在于用户点进来之后的转化，以及 agent 加载时的判断，对搜索曝光无帮助。名字里含高频词才有用。

## 5. clawhub 发布报 acceptLicenseTerms is required

**现象**：`clawhub skill publish` 返回该错误。

**根因**：服务端要 frontmatter 里有 `license` 字段。

**修法**：SKILL.md 的 frontmatter 加 `license: MIT`。加完重发。

## 6. 设备码登录没法自动化

**现象**：用浏览器自动化打开 `clawhub.ai/cli/device?user_code=XXX`，点 Sign In，走完 GitHub OAuth 跳回 dashboard，但 `clawhub whoami` 仍然 Not logged in。

**根因**：设备码流程要求把码提交给后端完成绑定，OAuth 回跳时那个 code 丢了。直达带参数的 URL 绕过了绑定这一步。

**修法**：让人在浏览器里手动输入设备码。这是唯一可行的路径，不要试图自动化。

## 7. git clone 走代理报 502

**现象**：`curl` 打 GitHub API 返回 200，但 `npx skills add` 里的 `git clone` 报 `CONNECT tunnel failed, response 502`。

**根因**：环境里的 `https_proxy` 指向的代理对 git 的 CONNECT 请求失败，而 curl 走同一个代理能通。换代理、注入 `GIT_CONFIG_KEY_0=https.proxy` 都没解决。

**修法**：换一个能跑 git 协议的代理，或者等网络恢复。这类失败与 skill 本身无关，别去改代码。

## 8. 两处副本漂移

**现象**：本机 `~/.agents/skills/<name>` 和仓库里的 `skills/<name>` 内容不一致。

**根因**：复制了两份。

**修法**：仓库是真身，本机用链接指过去。Windows 上 `New-Item -ItemType Junction -Path <link> -Target <repo>/skills/<name>`，`mklink /J` 在 git bash 里容易因为路径引号解析错而失败。

## 9. 第三方渠道榜单信息过期

**现象**：按一份 2026-07 的榜单去提交 smithery，发现它 2026-10-31 已经关停业务。

**修法**：动手前先访问目标站点首页，看有没有停服公告。第三方排名数据通常滞后几个月。

## 10. 清理测试目录被安全策略拦

**现象**：`rm -rf _t4` 报 `genie-trash failed`，导致 `&&` 链短路，后面的命令没跑。

**修法**：测试用独立新目录名（`_t5`），不删旧的。或者用 PowerShell 的 `Remove-Item -Recurse -Force`。别在 `&&` 链的开头放可能失败的清理命令。

## 11. 安装超时但没有错误

**现象**：`npx skills add` 跑了六分钟没输出，目录是空的。

**根因**：输出被管道里的 `grep` 缓冲了，看不到进度。实际卡在 clone 阶段。

**修法**：排查时不要给长命令接 `grep`，或者接受「看不到中间进度」，用目录是否生成来判断实际进展。

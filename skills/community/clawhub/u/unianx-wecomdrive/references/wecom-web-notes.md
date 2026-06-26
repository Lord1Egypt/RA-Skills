# 企业微信网页端备注

## 目录

1. 已知链接
2. 登录判断规则
3. 脚本输出
4. 安全操作建议

## 已知链接

- 登录起点：`https://doc.weixin.qq.com/home/recent`
- 兼容登录页：`https://work.weixin.qq.com/wework_admin/loginpage_wx`
- 首页：`https://work.weixin.qq.com/`
- 常见登录二维码 iframe 路径包含 `/wework_admin/wwqrlogin/`

如果用户已经给出了文件或文件夹链接，直接打开该链接，不要再从首页重新摸索入口。

## 登录判断规则

满足任一条件时，都视为需要登录：

- 当前 URL 是 `https://doc.weixin.qq.com/home/recent`，并且页面出现登录相关提示
- 当前 URL 包含 `/wework_admin/loginpage_wx`
- 当前 URL 包含 `/scenario/login.html`
- 页面可见文字包含 `企业微信扫码登录`、`扫码登录`、`企业身份登录` 或类似文案
- iframe 地址包含 `/wwqrlogin/` 或 `login_qrcode`

如果需要登录，优先从 iframe 中截取二维码；如果失败，就截取登录主体区域或当前整页。无论使用哪种方式，都要把截图发给用户。
二维码一旦发给用户，就继续保留当前登录页面，不要关闭标签页或重开新的登录页。
重新抓取二维码时，覆盖固定文件 `$SKILL_DIR/.outputs/wecom-login-qr.png`，不要生成一串新的时间戳文件。
如果页面同时出现 `请在桌面端确认登录`、`无法扫码` 或类似提示，就不要继续让用户扫码，而是改为提示用户到企业微信桌面端完成确认。

## 脚本输出

`scripts/wecom-drive-browser.mjs` 会输出 JSON，包含：

- `status`：`ready`、`login_required`、`desktop_confirm_required`、`login_timeout` 或 `error`
- `desktopConfirmationRequired`：是否命中“需要桌面端确认”的登录提示
- `loginHint`：给上层流程使用的登录提示语
- `targetUrl`：请求打开的链接
- `currentUrl`：跳转后的最终链接
- `title`：当前页面标题
- `qrPath`：二维码截图保存路径
- `page.links`：当前页面可见链接
- `page.editableElements`：页面中检测到的可编辑控件
- `page.textHints`：用于快速判断页面内容的短文本片段

用这些 JSON 字段判断是否要把二维码发给用户、是否要继续等待登录，以及是否可以进入页面操作。
如果 `desktopConfirmationRequired` 为真，优先提示用户去企业微信桌面端确认登录，不要继续走普通扫码分支。

## 安全操作建议

- 真正的读取和编辑步骤优先使用浏览器工具，这样可以保留交互会话，并在输入前检查 DOM。
- 登录检查、会话准备、二维码提取和页面摘要优先使用随附脚本。
- 登录页处理时优先保留原页面；如果脚本模式下要等待扫码，配合 `--keep-open` 使用。
- 对文件处理任务，默认先下载到本地，再在本地处理。
- 需要上传本地处理结果时，固定使用 `https://doc.weixin.qq.com/home/recent` 作为导入入口。
- 在做可能破坏内容的修改前，如果用户指令还不够精确，先重述并确认目标改动。
- 如果页面是富文本编辑器或类表格编辑器，输入前先检查当前焦点元素和附近工具栏标签。

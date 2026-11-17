# 退出码与失败处理

本文件是 [SKILL.md](../SKILL.md) 「失败处理」一节的展开。**按需加载**：只有当脚本返回非零退出码、或需要排查历史运行时读它；正常运行不必预先加载。

## 失败输出格式

失败时脚本输出一个结构化块，agent 照着 `what_now` 做即可：

```
=== FAILED ===
step     : set-cover
code     : E_COVER_NOT_APPLIED
exit     : 60
message  : 自定义封面设置失败
detail   : {"before":"url(\"https://...","after":"url(\"https://..."}
what_now :
  1. 走完了流程但封面缩略图 URL 没变，说明图片没真正替换
  2. 重跑一次通常就能成功；若连续失败，先不传 COVER_IMAGE 用默认第一帧
space    : 12（页面已保留）
takeover : ego-browser nodejs -e "await claimTaskSpace(12)"
cleanup  : ego-browser nodejs -e "await completeTaskSpace(12, { keep: false })"
=== END FAILED ===
```

成功时输出 `=== OK ===` 块，字段相同（step / exit / 可选 space）。

## 退出码表

| exit | 阶段 | 典型 code | agent 下一步 |
|---|---|---|---|
| 0 | 成功 | — | 完成 |
| 10 | 参数/素材校验 | `E_PARAM_*` `E_MEDIA_*` `E_COVER_NOT_FOUND` `E_COVER_NOT_IMAGE` | 改参数重跑，**无副作用**（未启动浏览器） |
| 11 | 依赖缺失 | `E_DEP_EGO_BROWSER` `E_DEP_PYTHON` `E_DEP_MJS` | 装 ego-browser / python3，或确认 `.mjs` 与 `.sh` 同目录 |
| 20 | 登录 | `E_AUTH_EXPIRED` | 让用户手动登录，再接管同一 space 或重跑 |
| 21 | 上传页 | `E_TAB_NOT_FOUND` | 手动点一下 tab 确认可用，再重跑 |
| 30 | 素材上传 | `E_VIDEO_UPLOAD_TIMEOUT` `E_IMAGE_UPLOAD_TIMEOUT` | 检查文件/网络，直接重跑 |
| 40 | 填表 | `E_TITLE_INPUT_MISSING` `E_TITLE_NOT_APPLIED` `E_EDITOR_MISSING` `E_BODY_NOT_APPLIED` | 页面可能改版，接管看现场 |
| 50 | 话题 | `E_TOPIC_NOT_ATTACHED` | 话题缺失不影响发布，可接管手动补 |
| 60 | 封面 | `E_COVER_AREA_MISSING` `E_COVER_ENTRY_HIDDEN` `E_COVER_EDITOR_NOT_OPEN` `E_COVER_NOT_APPLIED` `E_COVER_DONE_BTN_MISSING` `E_COVER_MODAL_STUCK` | 按 `what_now` 分级处理；连续失败就不传 `COVER_IMAGE` 用默认第一帧 |
| 70 | 提交 | `E_SUBMIT_DISABLED` `E_SAVE_DISABLED` `E_NO_PUBLISH_HOST` `E_NO_ONPUBLISH` `E_NO_ONSAVE` | 必填项没填完，接管看哪个字段标红 |
| 80 | 提交后校验 | `E_PUBLISH_UNCONFIRMED` `E_DRAFT_COUNT_UNREADABLE` | **不要立即重发**，先去笔记管理确认 |
| 90 | 内部异常 | `E_UNEXPECTED` | 脚本 bug，把 code + detail 给 agent |

**判断口诀**：10/11 是「改完重跑就行」；20/21/30/60 是「修复外部条件后重跑」；40/50/70 是「页面结构可能变了，先看现场」；80 是「先别动，去确认」；90 是「脚本自己的问题」。

## 失败现场

默认 `KEEP_ON_FAIL=1`：失败时 task space 不销毁、页面保留、ownership 转为 user。

```bash
# 接管（注意：keep 过的空间 ownership 是 user，用 claimTaskSpace 更稳）
ego-browser nodejs -e "await claimTaskSpace(12)"

# 或用 takeOverTaskSpace（agent 自己结束的空间）
ego-browser nodejs -e "await takeOverTaskSpace(12)"

# 用完清理
ego-browser nodejs -e "await completeTaskSpace(12, { keep: false })"
```

批量跑、只想尽快释放资源时传 `KEEP_ON_FAIL=0`，失败即关闭空间。注意关闭后无法回看页面。

## 日志

每次运行写 `/tmp/xhs-publish-<时间戳>-<pid>.log`，内容与终端输出一致，脚本最后一行打印路径。

日志**故意写在 `/tmp` 而不是 skill 目录**：skill 升级会整体覆盖目录，写在里面会丢，且会被发布审计判为「数据安全」问题。

## step 名对照

日志和失败块里的 `step` 字段：

| step | 做什么 |
|---|---|
| `precheck` | 参数/依赖校验（未启动浏览器，无副作用） |
| `open-publish-page` | 建 task space + 打开创作平台 + 等 SPA 渲染 |
| `auth` | 登录态检查（URL + 侧栏入口双重判据） |
| `ensure-upload-tab` | 切到视频/图文上传页 |
| `upload-media` | 上传素材（视频含转码轮询） |
| `set-cover` | 自定义封面（仅视频且传了 `COVER_IMAGE`） |
| `fill-title` | 填标题并回读校验 |
| `fill-body` | 填正文并校验长度 |
| `add-topics` | 逐个挂话题，失败重试一次 |
| `submit` | 发布 / 存草稿 / 结果校验 |
| `stage-hold` | stage 模式收尾，保留页面 |

## 常见故障判断

**`E_AUTH_EXPIRED` + `redirected_to_login`**：登录态真的过期了。让用户去 ego-lite 手动登录。登录会让 task space 控制权转给用户，之后 agent 命令会报 `user has taken control`，这是正常的，用户回复 continue 后接管即可。

**`E_AUTH_EXPIRED` + `no_manage_entry`**：URL 没跳 login 但侧栏没有「笔记管理/草稿箱」，通常是页面还没渲染完或加载失败。重跑一次；连续则手动打开一次创作平台确认页面正常。

**`E_VIDEO_UPLOAD_TIMEOUT`**：转码慢。10MB/20s 的视频通常 8 秒内完成；超过 2 分钟多半是文件编码异常或网络问题。用 `ffprobe` 确认视频能正常解析，必要时先压到 1080p。

**`E_COVER_NOT_APPLIED`**：封面流程走完但缩略图 URL 没变。最常见是图片还没渲染完就点了「完成」。重跑；连续失败就放弃自定义封面。

**`E_PUBLISH_UNCONFIRMED`**：提交后 25 秒内没检测到跳转。**绝对不要立刻重发**——可能已经发出去了，重复发布会生成重复笔记。先去创作平台「笔记管理」看一眼。

**`E_UNEXPECTED`**：脚本自身异常。看 `detail.stack`，配合日志定位。常见原因是 ego-browser 连接中断或页面结构改版导致选择器失效——后者需要更新 `publish_note.mjs` 顶部的 `SEL` 表。

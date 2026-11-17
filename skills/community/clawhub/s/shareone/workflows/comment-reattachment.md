# 显式重新绑定评论目标

只在用户明确要求把已有线程绑定到重新选择的当前对象或文字时使用。本能力支持 SDK `app_declared` 顶层线程。普通查看、处理反馈、刷新 Git 源都不触发自动重绑。

## 读取当前事实

```bash
node scripts/shareone_api_request.js "/api/v1/shares/<REF>/comments"
node scripts/shareone_api_request.js "/api/v1/shares/<REF>/comments/<ROOT_ID>/anchor-bindings"
```

评论的 `quote` / `highlighter_data` 永远是原始捕获。`anchor_binding` 不为空时，其中的 `quote` / `highlighter_data` 才是当前目标；`revision` 是当前绑定版本。没有绑定时版本为 0。历史数组按版本升序，每条替换前一条，版本 0 的证据在原始评论中。

`viewer_can_reattach` 由服务端决定：原评论作者、分享所有者或协作者可重绑，且必须先通过分享当前的访问门禁。回复没有独立绑定。绑定不会授予额外数据权限，不会改作者、创建时间、评论、回复或反馈状态。

## 用户选择与确认

优先让用户使用侧栏 **重新绑定目标**，通过页面原有 SDK 控件重新选择。预览展示稳定对象标识、精确文字、内容/语言版本和原因；改变对象需要另外勾选确认。手机上侧栏会收起供选择，捕获后重新打开预览。

这建立新的绑定，不是恢复未记录的历史选择。保留原始证据；不能从 `label`、对象标题、评论时间或当前 Git 分支补出选区。真正的整个对象评论仍可不含 `text`。

确认后，文字提案先通过现有 `reveal-text` 回调验证，成功才保存。页面不支持捕获或恢复、重复文字无法唯一确定、已知版本变化、取消操作，都不追加历史。选择位置、恢复状态、临时预览和回调进度不持久化。

## API 提交

Agent 仅能提交用户已明确选择并确认的当前目标。不得把 LLM 推测的目标当作用户选择。重用 SDK 捕获的对象标识和选择器；同一页面无法验证时不要合成绑定或直接调用接口绕开界面验证。

将以下结构保存为请求 JSON 文件，再使用正式通用客户端提交：

```json
{
  "expected_revision": 0,
  "replacement": {
    "version": 1,
    "anchor_type": "app_declared",
    "ids": ["ticket/42"],
    "label": "Selected evidence",
    "text": {
      "exact": "Selected evidence",
      "prefix": "",
      "suffix": "",
      "position": {"start": 0, "end": 17},
      "version": "en/2"
    }
  },
  "reason": "The commenter selected the current evidence again",
  "allow_object_change": false
}
```

```bash
node scripts/shareone_api_request.js "/api/v1/shares/<REF>/comments/<ROOT_ID>/anchor-bindings" --method POST --data-file binding.json
```

`expected_revision` 必须是已读的当前版本；文字偏移是 UTF-16 单元，不是 Unicode 字符或字节。`text` 只可对应一个稳定对象；未提供内容版本时明确说明，不能伪造版本。整个对象选择省略 `text`。坐标、可见性和定位进度不属于请求字段。

201 返回完整更新后的线程及当前绑定。使用现有 `/comments/changes` 同步其他读者；刷新后仍读取同一有效绑定。`ANCHOR_BINDING_CONFLICT` 要求重新读取线程及历史，再让用户明确确认新的提案；不能自动递增版本重试。`ANCHOR_OBJECT_CHANGE_REQUIRED` 要求显示原、新对象并确认 `allow_object_change=true`，不能默认勾选。不要使用普通内容编辑接口迁移锚点，也不要改反馈状态来表示定位是否成功。

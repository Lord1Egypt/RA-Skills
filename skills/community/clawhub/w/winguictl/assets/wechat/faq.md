# 常见问题与注意事项

## 微信未启动/未登录

- **现象**：找不到 `mmui::MainWindow` 窗口，或窗口标题为空。
- **解决**：确保微信已启动并登录。若仅启动未登录，窗口类名为 `mmui::LoginWindow`。
- **检测**：
  ```powershell
  Get-Process | Where-Object { $_.ProcessName -eq "Weixin" }
  ```

## 窗口定位失败

- **现象**：`find` 或 `snapshot` 找不到目标控件。
- **原因**：
  1. 微信版本升级导致 UI 结构变化。
  2. 窗口未完全加载。
- **解决**：
  1. 带参数运行程序重新激活微信主界面：
     ```powershell
     Start-Process "C:\Program Files (x86)\Tencent\Weixin\Weixin.exe" --scene=taskbarpins
     ```
  2. 等待窗口加载完成。

## 坐标点击不准确

- **现象**：点击位置偏离目标控件。
- **原因**：窗口大小变化、DPI 缩放、多显示器配置。
- **解决**：
  1. 每次操作前重新获取 snapshot。
  2. 使用 `find` 动态获取控件坐标，而非硬编码。
  3. 对于高 DPI 显示器，确保微信和脚本进程的 DPI 感知设置一致。

## 群聊语音/视频电话限制

- **现象**：在群聊中发起语音或视频电话时微信卡死。
- **原因**：微信 4.0 版本在群聊通话的 SessionPicker 窗口存在 UI 自动化 Bug。
- **解决**：仅对单个好友发起语音/视频通话，避免群聊通话自动化。

## 添加好友频率限制

- **现象**：频繁添加好友后账号被封禁。
- **限制**：单次不超过 8 人，每日不超过 4 次，间隔不少于 2 小时。
- **建议**：控制自动化添加好友的频率，避免触发风控。

## 文件发送限制

- **限制**：
  - 单文件大小：不超过 1GB
  - 空文件：无法发送
  - 笔记内文件：单个不超过 100MB
- **解决**：发送前检查文件大小，超大文件分卷压缩后发送。

## 消息字数限制

- **限制**：单条消息最多 2000 字。
- **解决**：超长文本自动转换为 `.txt` 文件发送。

## 语言检测失败

- **现象**：`pyweixin` 无法自动检测微信语言。
- **原因**：WechatAppex.exe 未初始化（需先打开一次视频号或小程序面板）。
- **解决**：手动打开一次视频号或小程序面板，或在配置中手动指定语言。

## 安全建议

- 执行任何 `action` 命令前，先使用 `--dry-run` 预览操作：
  ```powershell
  python scripts\winguictl.py action --window-id <id> click --relative-x 100 --relative-y 200 --dry-run
  ```
- 验证 `window_id` 正确后再执行批量操作。
- 避免在包含敏感信息的窗口上使用 OCR。
- 不要在自动化过程中操作鼠标和键盘，以免干扰脚本执行。

## 多语言文本对照表

| 功能 | 简体中文 | English | 繁體中文 |
|------|----------|---------|----------|
| 发送按钮 | 发送(S) | send | 傳送 |
| 语音聊天 | 语音聊天 | Voice Call | 語音通話 |
| 视频聊天 | 视频聊天 | Video Call | 視訊通話 |
| 聊天记录 | 聊天记录 | Chat History | 聊天記錄 |
| 聊天信息 | 聊天信息 | Chat Info | 聊天資訊 |
| 清空 | 清空 | Clear | 刪除 |
| 确定 | 确定 | OK | 確定 |
| 取消 | 取消 | Cancel | 取消 |
| 删除 | 删除 | Delete | 刪除 |
| 更多 | 更多 | More | 更多 |
| 设置 | 设置 | Settings | 設定 |
| 通用 | 通用 | General | 一般 |
| 朋友圈 | 朋友圈 | Moments | 朋友圈 |
| 通讯录 | 通讯录 | Contacts | 通訊錄 |
| 置顶 | 置顶 | Sticky | 置頂 |
| 消息免打扰 | 消息免打扰 | Mute Notifications | 訊息免打擾 |
| 折叠该聊天 | 折叠该聊天 | Fold Chat | 折疊該聊天 |
| 添加朋友 | 添加朋友 | Add Contacts | 新增朋友 |
| 新的朋友 | 新的朋友 | New Friends | 新的朋友 |
| 前往验证 | 前往验证 | Verify Now | 前往驗證 |
| 添加到通讯录 | 添加到通讯录 | Add to Contacts | 新增到通訊錄 |
| 发消息 | 发消息 | Messages | 發訊息 |
| 企业信息 | 企业信息 | Enterprise Information | 企業資訊 |
| 浅色模式 | 浅色模式 | LightMode | 淺色模式 |
| 深色模式 | 深色模式 | DarkMode | 深色模式 |
| 跟随系统 | 跟随系统 | Automatic | 跟隨系统 |
| 文件 | 文件 | File | 檔案 |
| 图片 | 图片 | Image | 圖片 |
| 视频 | 视频 | Video | 影片 |
| 链接 | [链接] | [Link] | [連結] |
| 退出登录 | 退出登录 | Log Out | 登出 |
| 账号设置 | 账号设置 | My Account | 賬號與儲存 |
| 聊天文件 | 聊天文件 | Chat Files | 微信檔案 |
| 收藏 | 收藏 | Favorites | 收藏 |
| 新建笔记 | 新建笔记 | New Note | 新進筆記 |
| 发表 | 发表 | Post | 發表 |
| 返回 | 返回 | Back | 返回 |
| 赞 | 赞 | Like | 讚 |
| 评论 | 评论 | Comment | 評論 |
| 查看全部 | 查看全部 | View All | 查看全部 |
| 共同群聊 | 共同群聊 | Shared Groups | 共同群組 |
| 备注 | 备注 | Remark | 備註 |
| 标签 | 标签 | Tags | 標籤 |
| 描述 | 描述 | Description | 描述 |
| 朋友权限 | 朋友权限 | Privacy | 朋友權限 |
| 个性签名 | 个性签名 | What's Up | 個性簽名 |
| 来源 | 来源 | Source | 來源 |
| 电话 | 电话 | Mobile | 電話 |
| 昵称 | 昵称 | Name | 暱稱 |
| 地区 | 地区 | Region | 地區 |
| 微信号 | 微信号 | Weixin ID | 微信 ID |
| 接听 | 接听 | Answer | 接聽 |
| 拒绝 | 拒绝 | Decline | 拒絕 |
| 服务号 | 服务号 | Service Accounts | 服務賬號 |
| 公众号 | 公众号 | Official Accounts | 官方賬號 |
| 完成 | 完成 | Finish | 完成 |
| 刷新 | 刷新 | Refresh | 重新整理 |
| 最近群聊 | 最近群聊 | Recent Group Chats | 最近群組 |
| 通讯录管理 | 通讯录管理 | Manage Contacts | 通訊錄管理 |
| 发起群聊 | 发起群聊 | Start Group Chat | 建立群組 |
| 发起接龙 | 发起接龙 | Create Group Note | 發起接龍 |
| 分别发送 | 分别发送 | Send To | 分別傳送 |
| 网络不可用 | 当前网络不可用 | Network unavailable | 目前網路不可用 |
| 查看更多消息 | 查看更多消息 | View more messages | 查看更多訊息 |
| 公众号主页 | 公众号主页 | Official Account homepage | 公眾號主頁 |
| 关注 | 关注 | Follow | 關注 |
| 快捷操作 | 快捷操作 | Shortcuts | 快捷操作 |
| 添加备注名 | 添加备注名 | Add Remark | 新增備註名 |
| 添加电话 | 添加电话 | Add Mobile | 新增電話號碼 |
| 删除电话 | 删除电话 | DeleteMobile | 刪除电话 |
| 旋转 | 旋转 | Rotate | 旋轉 |
| 加入群聊 | 加入群聊 | Join Group | 加入群組 |
| 下载 | 下载 | Download | 下載 |
| 未下载 | 未下载 | Not Downloaded | 未下载 |
| 已过期 | 已过期 | Expired | 已过期 |
| 发送中断 | 发送中断 | Send Interrupt | 发送中断 |
| 昨天 | 昨天 | Yesterday | 昨天 |
| 通知 | 通知 | Notifications | 通知 |
| 年 | 年 | - | 年 |
| 月 | 月 | - | 月 |
| 天前 | 天前 | day(s) ago | 天前 |

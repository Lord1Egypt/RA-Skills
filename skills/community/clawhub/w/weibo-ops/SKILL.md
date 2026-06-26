---
name: weibo-ops
description: |
  Weibo (微博) write operations via DrissionPage + Chrome CDP.
  Post, delete, repost, comment, and like on weibo.com.
  Activate when user asks to publish/delete/repost/comment/like on Weibo,
  or mentions 发微博/删微博/转发/评论/点赞.
metadata:
  version: "1.0.0"
  author: langlang
---

# Weibo Operations Skill

通过 DrissionPage 连接 Chrome CDP 端口，模拟鼠标/键盘操作完成微博写操作。

## 前置条件

1. **Chrome 以 CDP 模式运行**（端口 19334）：
   ```bash
   bash scripts/start_chrome.sh
   ```
   脚本会自动从原始 Chrome profile 复制登录态到 `/tmp/chrome-debug-profile`。

2. **已登录微博**：Chrome profile 中必须有有效的微博登录 session。首次使用需在弹出的 Chrome 窗口中手动登录 weibo.com。

3. **依赖**：`pip install DrissionPage`

## 可用操作

所有操作通过 `scripts/weibo_ops.py` 执行：

| Action | 说明 | 示例 |
|--------|------|------|
| `count` | 查看当前微博数 | `--action count` |
| `post` | 发微博 | `--action post --text "内容"` |
| `delete_all` | 删除全部微博 | `--action delete_all` |
| `delete_one` | 删除指定位置微博 | `--action delete_one --index 0` |
| `repost` | 转发帖子 | `--action repost --post_id BID --text "转发语"` |
| `comment` | 评论帖子 | `--action comment --post_id BID --text "评论"` |
| `like` | 点赞帖子 | `--action like --post_id BID` |

### 默认参数

- `--port 19334` Chrome CDP 端口
- `--uid 6331761230` 微博 UID（浪浪在发芽）
- `--keep-open` 不关闭浏览器连接（调试用）

## 用法示例

```bash
# 发微博
python3 scripts/weibo_ops.py --port 19334 --action post --text "你好世界"

# 转发别人的帖子
python3 scripts/weibo_ops.py --port 19334 --action repost --post_id QAgBUith6 --uid 7909159083 --text "说得好"

# 评论
python3 scripts/weibo_ops.py --port 19334 --action comment --post_id QAgBUith6 --uid 7909159083 --text "赞同"

# 点赞
python3 scripts/weibo_ops.py --port 19334 --action like --post_id QAgBUith6 --uid 7909159083

# 删除全部
python3 scripts/weibo_ops.py --port 19334 --action delete_all

# 查看数量
python3 scripts/weibo_ops.py --port 19334 --action count
```

## 注意事项

- Chrome 每次重启后需要重新运行 `start_chrome.sh` 刷新 profile
- 微博 Cookie 有效期有限，过期后需重新登录
- 转发/评论/点赞操作在别人帖子上需要 `--uid` 参数指向帖子作者的 UID
- 自己不能赞自己的帖子（微博限制）
- 删除操作通过 CDP 鼠标点击 popup 菜单，速度较慢（每条约 10 秒）

## 读操作

读数据（热搜、搜索、帖子列表等）使用 weibo-openclaw-plugin：
- `weibo-search` — 微博智搜
- `weibo-hot-search` — 热搜榜
- `weibo-status` — 自己的微博列表
- `weibo-crowd` — 超话操作

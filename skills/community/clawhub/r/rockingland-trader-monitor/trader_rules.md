# 小红书用户帖子关键词监测规则参考

## 前置依赖

1. **xiaohongshu-mcp 二进制**：`~/.local/bin/xiaohongshu-mcp`
2. **xiaohongshu-login 二进制**：`~/.local/bin/xiaohongshu-login`（用于首次登录）
3. **jq**：`apt-get install jq`
4. **Xvfb**（无桌面环境）：`apt-get install xvfb`
5. **openclaw CLI**：用于微信推送
6. **Kimi cookies**：已登录小红书的 cookies 文件

## 获取用户 ID 和 xsec_token

### 方法一：通过小红书 App
1. 打开目标用户主页
2. 点击右上角「分享」→「复制链接」
3. 链接格式：`https://www.xiaohongshu.com/user/profile/USER_ID`
4. 提取 `USER_ID`

### 方法二：通过搜索
1. 用 `search.sh <用户名>` 搜索用户
2. 从返回的 feed 数据中提取 `noteCard.user.userId`

### 获取 xsec_token
1. 从用户主页任意帖子的 feed 数据中提取 `xsecToken`
2. 或运行 `user-profile.sh USER_ID "any"` 后从返回数据中获取有效 token

## 登录方式

本 skill 使用 cookies 登录，不依赖二维码。

**Cookie 文件**：将已登录浏览器的 cookies 导出为 JSON 数组：
```json
[
  {"name": "a1", "value": "...", "domain": ".xiaohongshu.com", "path": "/"},
  {"name": "web_session", "value": "...", "domain": ".xiaohongshu.com", "path": "/"}
]
```

**放置路径**（按优先级）：
1. `~/cookies.json`
2. `~/.xiaohongshu/cookies.json`
3. 环境变量 `XHS_COOKIES_SRC` 指定的路径

**首次登录**（如无 cookies）：
```bash
# 获取二维码
./mcp-call.sh get_login_qrcode
# 用小红书 App 扫码
```

## 监测逻辑

1. 启动 MCP 服务（自动启动 Xvfb 虚拟显示）
2. 调用 `user_profile` 获取用户主页帖子列表
3. 检查最近 5 条帖子标题是否含关键词
4. 只检查**今天**发布的帖子（以 `MM.DD` 日期前缀匹配）
5. 命中关键词且未通知过 → 微信推送
6. 关闭 MCP 服务

## 定时任务建议

```
# 每天 4 次检查
5 8,12,16,20 * * * /usr/bin/python3 /path/to/xiaohongshu-trader-monitor/scripts/xhs_trader_monitor.py >> /path/to/logs/xhs_trader.log 2>&1
```

## 关键词配置

在脚本顶部 `KEYWORDS` 列表中添加/删除关键词：
```python
KEYWORDS = ["棱镜球", "炫彩蛋", "同乘蛋", "祝福项坠"]
```

## 状态文件

- `xhs_trader_state.json` — 记录已通知的帖子 ID，避免重复推送

## 消息模板

```
🎯 上新提醒！

04.30 今日新帖标题...

检测到关键词：棱镜球、炫彩蛋

快去查看 👀
```

## MCP 端口

默认 `http://localhost:18060/mcp`，可通过环境变量 `XHS_MCP_PORT` 修改。

## 故障排查

| 问题 | 解决 |
|------|------|
| MCP 启动超时 | 检查 xiaohongshu-mcp 二进制是否存在、Xvfb 是否安装 |
| 无法获取帖子 | 检查 cookies 是否过期、USER_ID/XSEC 是否正确 |
| 微信推送失败 | 检查 openclaw-weixin 通道是否配置 |
| 二维码登录风控 | 改用 cookies 登录（从已登录浏览器导出） |


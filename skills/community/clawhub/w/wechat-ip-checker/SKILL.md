# 微信公众号 IP 检测 Skill

用于检测公网 IP 是否匹配，并发布微信公众号文章。

## 功能

1. **IP 检测**：使用 https://www.ip38.com/ 获取当前公网 IP
2. **IP 比对**：与记录的 IP 进行对比
3. **自动发布**：IP 匹配时自动发布文章
4. **IP 不匹配提醒**：IP 不同时通知用户确认

## 配置文件

配置文件位置：`~/.openclaw/workspace-libu/wechat_ip_config.md`

格式：
```markdown
# 微信公众号发布公网IP记录
公网IP地址: 111.194.216.135
IP查询来源: https://www.ip38.com/
```

## 使用方法

### 手动检测 IP

告诉我要检测 IP 或发布文章，例如：
- "检测微信公众号 IP"
- "发布公众号文章 xxx.md"
- "检查 IP 后发布文章"

### 自动流程

1. 使用浏览器访问 https://www.ip38.com/ 获取当前公网 IP
2. 读取配置文件中的记录 IP
3. 比对结果：
   - ✅ **相同**：自动调用 baoyu-post-to-wechat 发布文章
   - ❌ **不同**：告知用户新 IP，等待确认后更新配置并发布

## 依赖

- baoyu-post-to-wechat skill（用于发布文章）
- 浏览器（用于访问 ip38.com）

## 注意事项

- 首次使用需配置 IP 白名单
- 每次发布前自动检测 IP
- 如 IP 变化需用户在微信公众平台添加新 IP 到白名单

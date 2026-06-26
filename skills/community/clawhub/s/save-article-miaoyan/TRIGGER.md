# 微信文章自动保存 — 触发指令

## 自动触发规则

**当用户在微信发送消息时，如果消息中包含微信公众号文章链接（`https://mp.weixin.qq.com/s/...`），自动执行以下流程：**

### 检测条件

```
消息内容 匹配 正则表达式: https://mp\.weixin\.qq\.com/s/[a-zA-Z0-9_-]+
```

### 执行流程

1. **识别链接**
   ```python
   url = re.search(r'https://mp\.weixin\.qq\.com/s/[a-zA-Z0-9_-]+', message)
   ```

2. **调用 skill**
   ```bash
   python3 /Users/andy/.qclaw/workspace/skills/save-article-miaoyan/auto_save_article.py "<message>"
   ```

3. **处理结果**
   - 成功 → 回复确认消息 + 文件路径
   - 失败 → 回复错误信息

### 回复模板

**成功时：**
```
✅ 已保存文章到 Miaoyan/待学习

📄 标题: [文章标题]
📝 摘要: [前200字摘要]
💾 路径: ~/Library/Mobile Documents/iCloud~com~tw93~miaoyan/Documents/待学习/[文件名].md
```

**失败时：**
```
❌ 保存失败

原因: [错误信息]
链接: [原链接]

💡 可能的原因：
- 网络超时
- 文章已删除
- Miaoyan 文件夹不存在
```

## 优先级

- 优先级：**高**（立即执行，不等待用户确认）
- 超时：**30秒**（超时后放弃并回复错误）
- 并发：**单线程**（一次只处理一个链接）

## 不触发的情况

- 消息中没有微信文章链接
- 链接格式不正确
- 链接已过期或文章已删除

## 手动触发

用户也可以显式要求保存：

```
保存文章 https://mp.weixin.qq.com/s/...
```

或

```
https://mp.weixin.qq.com/s/...
保存这篇
```

## 配置参数

| 参数 | 值 | 说明 |
|------|-----|------|
| `SKILL_PATH` | `/Users/andy/.qclaw/workspace/skills/save-article-miaoyan/` | Skill 目录 |
| `MIAOYAN_DIR` | `~/Library/Mobile Documents/iCloud~com~tw93~miaoyan/Documents/待学习` | 保存目录 |
| `TIMEOUT` | 30 秒 | 处理超时 |
| `URL_PATTERN` | `https://mp\.weixin\.qq\.com/s/[a-zA-Z0-9_-]+` | 链接识别正则 |

## 日志记录

每次保存都会记录：
- 时间戳
- 原始链接
- 文件路径
- 成功/失败状态
- 错误信息（如有）

## 扩展

可以添加的功能：
- [ ] 支持其他公众号平台（知乎、小红书等）
- [ ] 自动标签分类
- [ ] 定期同步到云端
- [ ] 文章去重检测
- [ ] 自动生成目录索引

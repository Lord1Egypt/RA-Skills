---
name: wechat-freepublish
description: 用于将微信公众号草稿 media_id 正式提交发布
---

# 微信公众号正式发布工具

## 用途
将微信公众号草稿箱中的文章通过 media_id 正式发布到公众号。

## 何时调用
当用户要求将微信公众号草稿正式发布时调用此 skill。

## 环境变量
- `WECHAT_ACCESS_TOKEN` - 微信公众号 access_token（必填）

## 执行命令
```bash
python3 scripts/publish.py <media_id>
```

## 风险提示
⚠️ **该操作是正式发布动作，必须在用户明确确认后执行！**

### 执行前必须确认：
1. 已获取正确的 media_id
2. 已设置 WECHAT_ACCESS_TOKEN 环境变量
3. 用户明确确认这是正式发布，不是草稿保存

### 重要提醒：
- 没有 media_id 时不要执行
- 没有 WECHAT_ACCESS_TOKEN 时不要执行
- 执行前先提醒用户这是正式发布，不是草稿保存
- 微信发布后文章会立即推送给所有关注者

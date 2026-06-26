#!/usr/bin/env python3
"""
手动发布指南
当 XML-RPC 无法直接发布时，使用此方法
"""
import webbrowser
import sys

print("""
📝 手动发布指南

由于 Typecho XML-RPC 的某些限制，批量发布草稿可能不可用。

## 快速发布步骤：

1. 登录博客后台
   http://yuanblog.tk:9980/admin

2. 进入文章管理
   管理 → 文章

3. 找到要发布的文章（草稿）
   - 文章 ID: 916
   - 标题：2026 年 AI 搞钱实战指南：从 0 到 1 的自动化内容创业之路

4. 点击"编辑"

5. 在编辑页面：
   - 确认内容正确
   - 点击"发布"按钮（从草稿改为发布）

6. 查看前台效果

## 自动化方案

未来可以：
- 直接发布新文章（不使用草稿模式）
- 使用定时任务在低峰期发布
- 开发 Typecho 插件支持批量发布

""")

# 打开浏览器
webbrowser.open('http://yuanblog.tk:9980/admin/write.php')

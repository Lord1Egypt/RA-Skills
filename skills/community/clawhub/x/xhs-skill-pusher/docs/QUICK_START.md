# 🚀 xhs-kit 快速开始

## 一句话总结
**不再使用环境变量，直接指定cookie文件发布！**

## 核心命令
```bash
# 发布到新账号
./xhs.sh --cookie cookies_new_account.json --title "标题" --content "内容" --image 图片.jpg

# 发布到旧账号
./xhs.sh --cookie cookies_old_account.json --title "标题" --content "内容" --image 图片.jpg
```

## 三步发布

### 1. 准备内容
```bash
# 创建内容文件
echo "这是小红书笔记内容..." > content.txt

# 准备图片
# (确保有1242x1660像素的图片)
```

### 2. 发布执行
```bash
# 使用新账号发布
./xhs.sh \
  --cookie cookies_new_account.json \
  --title "我的小红书笔记" \
  --content "$(cat content.txt)" \
  --image my_photo.jpg \
  --tag 生活 \
  --tag 分享 \
  --tag 日常
```

### 3. 验证结果
```bash
# 检查发布状态
echo "✅ 发布完成！请在小红书App中查看。"

# 查看发布日志
tail -f publish.log 2>/dev/null || echo "首次发布"
```

## 常用命令速查

### 账号管理
```bash
# 查看所有账号
./xhs.sh --list-accounts

# 切换到新账号
./xhs.sh --switch new_account

# 检查cookie状态
./xhs.sh --cookie cookies.json --check-status
```

### 发布选项
```bash
# 多图片发布
./xhs.sh --cookie cookies.json --title "..." --content "..." \
  --image 1.jpg --image 2.jpg --image 3.jpg

# 定时发布（明天14点）
./xhs.sh --cookie cookies.json --title "..." --content "..." --image ... \
  --schedule "$(date -v+1d '+%Y-%m-%dT14:00:00+08:00')"

# 仅验证不发布
./xhs.sh --cookie cookies.json --title "..." --content "..." --image ... --debug-only

# 显示浏览器窗口
./xhs.sh --cookie cookies.json --title "..." --content "..." --image ... --show-browser
```

### 快速发布
```bash
# 一行命令快速发布
./xhs_quick_publish.sh cookies.json "标题" "内容" image.jpg --tag 标签1 --tag 标签2
```

## 当前账号状态

### 激活账号
- **文件**: `cookies.json`
- **用户ID**: `5fc1e8dd00000000010041c7`
- **状态**: ✅ 有效（新账号）

### 备用账号
- **新账号**: `cookies_new_account.json` (同激活账号)
- **旧账号**: `cookies_old_account.json` (用户ID: `6256338d0000000010006ab7`)

## 故障排除

### 如果发布失败
```bash
# 1. 检查cookie状态
./xhs.sh --cookie cookies.json --check-status

# 2. debug验证内容
./xhs.sh --cookie cookies.json --title "测试" --content "测试" --image test.jpg --debug-only

# 3. 检查图片
file 图片.jpg
ls -lh 图片.jpg

# 4. 重新准备cookie
cp cookies_new_account.json cookies.json
```

### 如果cookie过期
```bash
# 获取新cookie，保存为 new_cookie.json
# 然后更新账号文件
cp new_cookie.json cookies_new_account.json
./xhs.sh --switch new_account
```

## 生产环境建议

### 每日发布脚本
```bash
#!/bin/bash
# daily_publish.sh

DATE=$(date +%Y-%m-%d)
./xhs.sh \
  --cookie cookies.json \
  --title "每日更新 $DATE" \
  --content "今日分享..." \
  --image "/path/to/images/${DATE}.jpg" \
  --tag 每日更新 \
  --tag 生活记录

echo "$(date): 发布成功" >> /var/log/xhs_publish.log
```

### 添加到crontab
```bash
# 每天10点发布
0 10 * * * cd /Users/Zhuanz/.openclaw/workspace && ./xhs.sh --cookie cookies.json --title "早安" --content "..." --image morning.jpg

# 每天20点发布  
0 20 * * * cd /Users/Zhuanz/.openclaw/workspace && ./xhs.sh --cookie cookies.json --title "晚安" --content "..." --image night.jpg
```

## 🎯 记住关键点

1. **永远使用 `--cookie` 参数指定文件**
2. **脚本会自动转换cookie格式**
3. **先debug验证，再实际发布**
4. **多账号用 `--switch` 切换**

## 📞 需要帮助？
```bash
# 查看完整帮助
./xhs.sh --help

# 查看解决方案文档
cat XHS_COOKIE_SOLUTION.md | head -50
```

**开始发布吧！** 🚀
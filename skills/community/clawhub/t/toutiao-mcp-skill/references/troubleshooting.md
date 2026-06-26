# 故障排查指南

本指南帮助你解决使用 toutiao-mcp-skill 时遇到的常见问题。

## 安装问题

### 问题：npm install 失败

**症状**：
```
npm ERR! code EACCES
npm ERR! syscall access
```

**解决方案**：
```bash
# 使用 sudo（不推荐）
sudo npm install -g toutiao-mcp

# 或者配置 npm 全局目录（推荐）
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
npm install -g toutiao-mcp
```

### 问题：Playwright 浏览器安装失败

**症状**：
```
Error: browserType.launch: Executable doesn't exist
```

**解决方案**：
```bash
# 重新安装浏览器
npx playwright install chromium

# 如果还是失败，尝试手动指定浏览器路径
export PLAYWRIGHT_BROWSERS_PATH=/path/to/browsers
npx playwright install chromium
```

## 登录问题

### 问题：登录超时

**症状**：浏览器打开后长时间无响应

**解决方案**：
1. 检查网络连接
2. 关闭浏览器重新登录
3. 尝试使用非无头模式：
```json
{
  "env": {
    "PLAYWRIGHT_HEADLESS": "false"
  }
}
```

### 问题：Cookie 保存失败

**症状**：登录成功但下次还是未登录

**解决方案**：
1. 检查 `COOKIES_FILE` 路径是否有写入权限
2. 确保目录存在：
```bash
mkdir -p ~/.openclaw/data
chmod 755 ~/.openclaw/data
```

### 问题：提示"未登录"

**症状**：明明已经登录，但还是提示未登录

**解决方案**：
1. Cookie 可能已过期，重新登录
2. 检查 Cookie 文件是否存在且有效
3. 删除 Cookie 文件重新登录：
```bash
rm ~/.openclaw/data/toutiao-cookies.json
```

## 发布问题

### 问题：标题验证失败

**症状**：
```
Error: 标题长度必须在 2-30 字之间
```

**解决方案**：
- 检查标题长度（2-30个字）
- 修改标题使其符合要求

### 问题：图片上传失败

**症状**：
```
Error: 图片上传失败
```

**可能原因及解决方案**：

1. **图片路径错误**
   ```bash
   # 检查文件是否存在
   ls -la /path/to/image.jpg
   
   # 使用绝对路径
   /Users/username/Pictures/image.jpg
   ```

2. **图片格式不支持**
   ```bash
   # 检查图片格式
   file /path/to/image.jpg
   
   # 转换格式
   convert image.png image.jpg
   ```

3. **图片太大**
   ```bash
   # 检查文件大小
   ls -lh /path/to/image.jpg
   
   # 压缩图片
   convert image.jpg -quality 85 -resize 1920x1920\> compressed.jpg
   ```

4. **网络问题**
   - 检查网络连接
   - 重试上传

### 问题：内容发布失败

**症状**：
```
Error: 发布失败
```

**解决方案**：
1. 确认已登录：调用 `check_login_status`
2. 检查内容格式是否符合要求
3. 查看详细错误日志
4. 重试发布

### 问题：批量发布部分失败

**症状**：批量发布时部分数据失败

**解决方案**：
1. 查看返回的详细错误信息
2. 检查失败数据的格式
3. 单独重试失败的数据
4. 检查是否触发平台限制

## 浏览器自动化问题

### 问题：页面元素未找到

**症状**：
```
Error: Timeout waiting for selector
```

**解决方案**：
1. 今日头条页面可能已更新，更新 toutiao-mcp：
```bash
npm update -g toutiao-mcp
```

2. 如果问题持续，报告到 GitHub Issues

### 问题：浏览器崩溃

**症状**：
```
Error: Browser closed unexpectedly
```

**解决方案**：
1. 重启系统
2. 重新安装浏览器：
```bash
npx playwright install chromium --force
```
3. 检查系统资源（内存、CPU）

## 性能问题

### 问题：发布速度很慢

**可能原因及解决方案**：

1. **网络慢**
   - 检查网络速度
   - 使用更快的网络

2. **图片太大**
   - 压缩图片
   - 减少图片数量

3. **系统资源不足**
   - 关闭其他程序
   - 增加系统内存

### 问题：内存占用高

**解决方案**：
1. 使用无头模式
2. 发布完成后关闭浏览器
3. 批量发布时分批处理

## 配置问题

### 问题：环境变量不生效

**症状**：配置的环境变量没有生效

**解决方案**：
1. 检查 MCP 配置文件格式是否正确
2. 重启 OpenClaw
3. 使用绝对路径而不是 `~`

### 问题：找不到 MCP Server

**症状**：
```
Error: Cannot find module
```

**解决方案**：
1. 检查 `command` 和 `args` 路径是否正确
2. 使用绝对路径：
```bash
which node  # 获取 node 路径
npm list -g toutiao-mcp  # 获取 toutiao-mcp 路径
```

## 日志和调试

### 启用详细日志

在 MCP 配置中添加：
```json
{
  "env": {
    "LOG_LEVEL": "debug"
  }
}
```

### 查看日志文件

日志通常输出到：
- OpenClaw 控制台
- 系统日志（取决于 OpenClaw 配置）

### 调试模式

使用非无头模式查看浏览器操作：
```json
{
  "env": {
    "PLAYWRIGHT_HEADLESS": "false"
  }
}
```

## 获取帮助

如果以上方法都无法解决问题：

1. **收集信息**：
   - 错误信息（完整的错误堆栈）
   - 操作步骤（如何复现问题）
   - 环境信息：
     ```bash
     node --version
     npm list -g toutiao-mcp
     uname -a  # macOS/Linux
     ```

2. **提交 Issue**：
   - GitHub: https://github.com/sipingme/toutiao-mcp-skill/issues
   - 包含上述收集的信息

3. **联系维护者**：
   - Email: sipingme@gmail.com

## 常用诊断命令

```bash
# 检查 Node.js 版本
node --version

# 检查 toutiao-mcp 安装
npm list -g toutiao-mcp

# 检查 Playwright 浏览器
npx playwright install --dry-run chromium

# 测试网络连接
ping www.toutiao.com

# 检查文件权限
ls -la ~/.openclaw/data/

# 查看进程
ps aux | grep node
```

## 预防措施

1. **定期更新**：
```bash
npm update -g toutiao-mcp
```

2. **备份 Cookie**：
```bash
cp ~/.openclaw/data/toutiao-cookies.json ~/.openclaw/data/toutiao-cookies.json.bak
```

3. **监控日志**：定期查看日志，及早发现问题

4. **控制发布频率**：避免触发平台限制

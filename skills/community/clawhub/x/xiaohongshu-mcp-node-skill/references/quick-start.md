# 🚀 快速开始指南

5 分钟快速上手 xiaohongshu-mcp-node-skill

## 第一步：安装

### 自动安装（推荐）

```bash
curl -fsSL https://raw.githubusercontent.com/sipingme/xiaohongshu-mcp-node-skill/main/install.sh | bash
```

### 手动安装

```bash
# 1. 克隆项目
git clone https://github.com/sipingme/xiaohongshu-mcp-node-skill.git
cd xiaohongshu-mcp-node-skill

# 2. 安装依赖（会自动安装 xiaohongshu-mcp-node）
npm install

# 3. 安装浏览器
npx playwright install chromium
```

## 第二步：登录

```bash
xhs-cli login
```

会生成一个二维码，使用**小红书 App** 扫码登录。

## 第三步：测试

### 检查登录状态

```bash
xhs-cli check-login
```

预期输出：
```json
{
  "success": true,
  "isLoggedIn": true,
  "message": "已登录"
}
```

### 搜索内容

```bash
xhs-cli search --keyword "Node.js"
```

### 发布测试内容

```bash
# 准备内容
echo "测试标题" > /tmp/title.txt
echo "这是测试内容" > /tmp/content.txt

# 发布（需要提供图片）
xhs-cli publish \
  --title-file /tmp/title.txt \
  --content-file /tmp/content.txt \
  --images /path/to/test-image.jpg
```

## 第四步：在 OpenClaw 中使用

### 配置 OpenClaw

确保 Skill 已安装到 OpenClaw：

```bash
openclaw skills list --eligible
```

应该能看到 `xiaohongshu-mcp-node` 在列表中。

### 对话示例

```
你: 帮我搜索小红书上关于 TypeScript 的内容

AI: 正在搜索...
[调用 xhs-cli search --keyword "TypeScript"]
找到 20 条相关内容...
```

## 常用命令速查

| 操作 | 命令 |
|------|------|
| 登录 | `xhs-cli login` |
| 检查登录 | `xhs-cli check-login` |
| 发布图文 | `xhs-cli publish --title "标题" --content "内容" --images img.jpg` |
| 搜索 | `xhs-cli search --keyword "关键词"` |
| 点赞 | `xhs-cli like --feed-id xxx --xsec-token yyy` |
| 评论 | `xhs-cli comment --feed-id xxx --xsec-token yyy --content "评论"` |

## 下一步

- 📖 阅读 [SKILL.md](../SKILL.md) 了解完整功能
- ❓ 查看 [FAQ](./faq.md) 解决常见问题
- 🐛 遇到问题？[提交 Issue](https://github.com/sipingme/xiaohongshu-mcp-node-skill/issues)

---

**5 分钟上手完成！开始使用吧！** 🎉

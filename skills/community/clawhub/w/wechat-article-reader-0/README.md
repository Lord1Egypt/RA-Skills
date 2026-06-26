# 微信公众号文章读取 Skill

让OpenClaw能够读取微信公众号文章链接的智能技能插件。

## ✨ 功能特性

- 🔗 **自动识别**：自动检测微信公众号文章链接
- 📊 **关键信息提取**：提取标题、作者、公众号名称、发布时间
- 📝 **智能摘要**：自动生成文章内容摘要
- 🚀 **即插即用**：支持飞书、Telegram、Discord等平台
- 🛡️ **反爬处理**：智能处理反爬机制

## 📦 安装方法

### 方法1：通过ClawHub安装（推荐）

```bash
# 搜索skill
clawhub search wechat-article-reader

# 安装
clawhub install wechat-article-reader
```

### 方法2：手动安装

```bash
# 1. 克隆或下载本仓库到OpenClaw工作区
cd ~/.openclaw/workspace/skills
git clone <repository-url> wechat-article-reader

# 2. 安装依赖
cd wechat-article-reader
pip install -r requirements.txt

# 3. 重启OpenClaw服务
openclaw restart
```

### 方法3：直接对话安装

直接在飞书中告诉OpenClaw：
```
请帮我安装这个skill：github.com/your-repo/wechat-article-reader
```

## 🎯 使用方法

### 基础用法

直接将公众号文章链接发送给OpenClaw：

```
https://mp.weixin.qq.com/s/xxxxx
```

### 明确指令

```
读取这篇文章：https://mp.weixin.qq.com/s/xxxxx
```

### 请求摘要

```
帮我总结这篇公众号文章：https://mp.weixin.qq.com/s/xxxxx
```

## 📤 返回格式

Skill会返回以下结构化信息：

```
📄 [文章标题]

👤 作者：[作者名称]
🏢 公众号：[公众号名称]
📅 发布时间：[YYYY-MM-DD]

📝 内容摘要：
[文章核心内容摘要，约3-5段]

🔑 关键点：
• 关键点1
• 关键点2
• 关键点3
```

## 🔧 配置选项

可以在 `skill.json` 中修改以下配置：

```json
{
  "config": {
    "timeout": 30,              // 请求超时时间（秒）
    "max_retries": 3,           // 最大重试次数
    "user_agent_rotation": true, // 是否轮换User-Agent
    "summary_max_length": 500    // 摘要最大长度
  }
}
```

## 🛠️ 技术架构

- **网络请求**：requests + fake-useragent
- **HTML解析**：BeautifulSoup + lxml
- **反爬处理**：User-Agent轮换 + 请求重试
- **内容提取**：智能提取规则 + 清洗算法

## 📁 文件结构

```
wechat-article-reader/
├── SKILL.md          # Skill元信息和说明
├── skill.json        # Skill配置文件
├── main.py           # 主逻辑代码
├── requirements.txt  # Python依赖
├── README.md         # 使用文档
└── test.py          # 测试脚本（可选）
```

## ⚠️ 注意事项

1. **链接格式**：仅支持 `mp.weixin.qq.com` 域名的链接
2. **访问限制**：部分文章可能需要关注公众号才能阅读
3. **网络环境**：需要能访问微信公众号的服务器
4. **文章时效**：已删除或私密文章无法读取

## 🐛 常见问题

### Q1: 提示"文章不存在或已被删除"
**A**: 可能原因：
- 文章已被作者删除
- 文章设置为私密（需要关注公众号）
- 链接格式不正确

### Q2: 请求超时怎么办？
**A**:
- 检查网络连接
- 在 `skill.json` 中增加 `timeout` 值
- 增加 `max_retries` 重试次数

### Q3: 摘要质量不好？
**A**: Skill提取文章核心段落，OpenClaw的大模型会进行二次优化。可以：
- 在指令中明确要求"详细摘要"或"简洁摘要"
- 配合OpenClaw的总结能力使用

### Q4: 支持其他平台吗？
**A**: 当前版本仅支持微信公众号。如有需求可以提交Issue或PR。

## 🚀 开发路线图

- [ ] 支持其他文章平台（知乎、掘金等）
- [ ] 图片提取和保存
- [ ] 视频链接识别
- [ ] 批量文章处理
- [ ] 历史文章缓存

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

MIT License

## 🙏 致谢

- OpenClaw社区提供的Skill开发框架
- BeautifulSoup和requests项目的维护者

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交GitHub Issue
- 加入OpenClaw社区讨论

---

**Made with ❤️ for OpenClaw Community**

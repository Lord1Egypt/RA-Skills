# 📱 微信公众号自动发布工具

> 自动化发布文章到微信公众号，支持智能配图、Markdown 渲染、定时任务

**版本**：v1.0.0  
**状态**：✅ 生产就绪  
**最后更新**：2026-03-10

---

## 🌟 特性

### 核心功能
- ✅ **自动发布** - 一键发布文章到微信公众号草稿箱
- ✅ **Markdown 支持** - Markdown 格式自动转 HTML 渲染
- ✅ **智能配图** - 自动生成封面图和正文配图
- ✅ **多图片源** - 支持 Unsplash、通义万相、文心一格、DALL-E 3
- ✅ **定时任务** - 支持 launchd 定时自动发布
- ✅ **成本优化** - 免费额度优先，自动降级

### 安全特性
- 🔒 **日志脱敏** - Token、API Key 自动脱敏
- 🔒 **权限保护** - 配置文件权限 600
- 🔒 **输入验证** - 标题、内容自动验证
- 🔒 **错误处理** - 完善的异常处理机制

### 可维护性
- 🛠 **统一配置** - ConfigManager 统一管理
- 🛠 **环境变量** - 支持环境变量替换
- 🛠 **测试框架** - pytest 测试框架
- 🛠 **详细文档** - 完整的使用文档

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd ～/.openclaw/workspace/skills/wechat-mp-publish
venv/bin/pip install -r requirements.txt
```

### 2. 配置微信公众号

编辑 `config.yaml`：

```yaml
wechat:
  appid: "你的公众号 AppID"
  appsecret: "你的公众号 AppSecret"
  name: "你的公众号名称"
```

### 3. 配置图片源（可选）

**方案 A：使用占位图（免费）**
```yaml
image:
  providers:
    placeholder:
      enabled: true
```

**方案 B：使用 Unsplash（推荐）**
```yaml
image:
  provider_priority:
    - "unsplash"
  
  providers:
    unsplash:
      enabled: true
      access_key: "你的 Unsplash Access Key"
```

**方案 C：使用通义万相（国内）**
```yaml
image:
  provider_priority:
    - "tongyi-wanxiang"
  
  providers:
    tongyi-wanxiang:
      enabled: true
      api_key: "sk-你的 DashScope API Key"
      monthly_limit: 100
```

### 4. 配置 IP 白名单

在微信公众号后台添加服务器 IP：
```
127.0.0.1 (your ip address)
```

### 5. 发布文章

```bash
# 创建文章文件
cat > article.md << 'EOF'
# 我的第一篇文章

这是文章内容...
EOF

# 发布到草稿箱
venv/bin/python -c "
from publish import WechatPublisher

publisher = WechatPublisher()

with open('article.md', 'r', encoding='utf-8') as f:
    content = f.read()

article = publisher.create_article(
    title='我的第一篇文章',
    content=content,
    template='business',
    author='作者名',
    multi_images=True
)

media_id = publisher.publish_to_draft([article])
print(f'✅ 发布成功！草稿 ID: {media_id}')
"

# 查看结果
# 登录 https://mp.weixin.qq.com/
# 内容与互动 → 草稿箱
```

---

## 📖 文档索引

| 文档 | 说明 |
|------|------|
| **[USER_GUIDE.md](USER_GUIDE.md)** | 📘 用户使用手册（必读） |
| **[QUICKSTART.md](QUICKSTART.md)** | 🚀 快速开始指南 |
| **[CONFIG_ADVANCED.md](CONFIG_ADVANCED.md)** | ⚙️ 高级配置说明 |
| **[STRATEGY.md](STRATEGY.md)** | 🎨 配图策略说明 |
| **[RELEASE_v1.0.md](RELEASE_v1.0.md)** | 📦 版本发布说明 |
| **[CODE_REVIEW_REPORT.md](CODE_REVIEW_REPORT.md)** | 🔍 Code Review 报告 |
| **[FIX_REPORT.md](FIX_REPORT.md)** | 🐛 修复报告 |
| **[TEST_REPORT.md](TEST_REPORT.md)** | 🧪 测试报告 |

---

## 💡 使用示例

### 发布单篇文章

```python
from publish import WechatPublisher

publisher = WechatPublisher()

with open('article.md', 'r', encoding='utf-8') as f:
    content = f.read()

article = publisher.create_article(
    title='文章标题',
    content=content,
    template='business',
    author='作者名',
    multi_images=True
)

media_id = publisher.publish_to_draft([article])
print(f'发布成功：{media_id}')
```

### 批量发布

```python
from publish import WechatPublisher
from pathlib import Path

publisher = WechatPublisher()

for article_file in Path('articles').glob('*.md'):
    with open(article_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    article = publisher.create_article(
        title=article_file.stem,
        content=content,
        template='business',
        multi_images=True
    )
    
    media_id = publisher.publish_to_draft([article])
    print(f'✅ {article_file.name}: {media_id[:30]}...')
```

### 查看使用统计

```bash
venv/bin/python -c "
from usage_counter import get_counter
counter = get_counter()
print(counter.get_summary())
"
```

---

## 📊 成本分析

### 免费额度
- **Unsplash**：无限制（真实照片）
- **通义万相**：100 张/月
- **文心一格**：100 张/月
- **总计**：200 张免费图片/月

### 发布能力
- **每篇文章**：3 张图片（1 封面 + 2 配图）
- **每月免费**：66 篇文章
- **超出成本**：$0.04/张（DALL-E 3）

### 推荐配置（零成本）
```yaml
image:
  provider_priority:
    - "unsplash"
    - "tongyi-wanxiang"
    - "baidu-yige"
  
  providers:
    dall-e-3:
      enabled: false  # 禁用付费服务
```

---

## 🔧 技术栈

- **Python**：3.8+
- **HTTP 客户端**：requests
- **配置管理**：PyYAML
- **图片处理**：Pillow
- **Markdown**：markdown
- **测试框架**：pytest

---

## 📝 更新日志

### v1.0.0 (2026-03-10)

**新增功能**：
- ✨ 统一配置管理器
- ✨ 日志脱敏处理
- ✨ 输入验证
- ✨ 多图片源支持
- ✨ 使用量跟踪
- ✨ 测试框架

**修复问题**：
- 🐛 配置加载逻辑重复
- 🐛 测试文件管理混乱
- 🐛 图片路径时序竞争
- 🐛 JSON 模块导入错误

**优化改进**：
- ⚡ 配图策略优化
- ⚡ 文档完善
- ⚡ 代码质量提升

---

## 🤝 贡献指南

### 开发环境
```bash
# 克隆项目
git clone <repo>
cd wechat-mp-publish

# 安装依赖
venv/bin/pip install -r requirements.txt

# 运行测试
venv/bin/python -m pytest tests/ -v
```

### 提交规范
- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `style:` 代码格式
- `refactor:` 重构
- `test:` 测试相关
- `chore:` 构建/工具

---

## 📄 许可证

MIT License

---

## 📞 技术支持

- **问题反馈**：查看 Code Review 报告
- **配置帮助**：查看高级配置说明
- **使用指南**：查看用户使用手册

---

**版本**：v1.0.0  
**状态**：✅ 生产就绪  
**最后更新**：2026-03-10

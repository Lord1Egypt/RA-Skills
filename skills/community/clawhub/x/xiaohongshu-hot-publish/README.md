# 小红书热点半自动化发布系统

<p align="center">
  <img src="https://img.shields.io/badge/版本-v1.1.0-blue" alt="版本">
  <img src="https://img.shields.io/badge/Python-3.8+-green" alt="Python">
  <img src="https://img.shields.io/badge/许可证-MIT-yellow" alt="许可证">
  <img src="https://img.shields.io/badge/状态-稳定-brightgreen" alt="状态">
  <img src="https://img.shields.io/badge/ClawHub-已发布-purple" alt="ClawHub">
</p>

<p align="center">
  <strong>专为小红书内容创作者设计的智能发布工具</strong>
</p>

<p align="center">
  <a href="#上传到clawhub">📤 立即上传到ClawHub</a> •
  <a href="#快速开始">🚀 快速开始</a> •
  <a href="#功能特性">✨ 功能特性</a> •
  <a href="#使用示例">🎯 使用示例</a>
</p>

## 🌟 项目亮点

- **🎨 美观界面**：现代化渐变设计，响应式布局
- **🤖 智能生成**：基于主题自动生成小红书风格内容
- **⚡ 高效发布**：一键复制，智能时间管理
- **📱 多端适配**：完美支持桌面和移动端
- **🔧 高度可定制**：支持品牌、主题、样式自定义

## 📖 目录

- [项目亮点](#项目亮点)
- [快速开始](#快速开始)
- [功能特性](#功能特性)
- [安装使用](#安装使用)
- [使用示例](#使用示例)
- [API文档](#api文档)
- [配置选项](#配置选项)
- [开发指南](#开发指南)
- [故障排除](#故障排除)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

## 🚀 快速开始

### 安装方法

1. 克隆或下载本项目到OpenClaw的skills目录：
```bash
cd ~/.openclaw/skills
git clone https://github.com/yourusername/xiaohongshu-hot-publish.git
```

2. 确保Python环境（3.8+）：
```bash
python --version
```

3. 安装依赖（可选）：
```bash
pip install -r requirements.txt
```

### 快速体验

```bash
# 生成示例页面
python demo.py

# 或直接生成内容
python create_hot_publish_page.py "Python学习" --brand "你的品牌"
```

## ✨ 功能特性

### 核心功能

| 功能 | 描述 | 状态 |
|------|------|------|
| 智能内容生成 | 基于主题自动生成小红书风格内容 | ✅ |
| 一键复制 | 快速复制内容到剪贴板 | ✅ |
| 时间管理 | 智能时间建议和发布状态跟踪 | ✅ |
| 响应式设计 | 完美适配桌面和移动端 | ✅ |
| 键盘快捷键 | Ctrl+C复制、数字键切换 | ✅ |
| 本地存储 | 保存发布状态，刷新不丢失 | ✅ |
| 错误处理 | 多种复制方法确保稳定 | ✅ |

### 内容类型支持

- **技术教程**：编程、开发、工具使用
- **学习指南**：学习方法、资源推荐
- **效率工具**：工作流优化、时间管理
- **经验分享**：案例分析、实战经验
- **热点话题**：时事热点、趋势分析

## 📦 安装使用

### 作为OpenClaw技能使用

1. 将整个文件夹复制到OpenClaw技能目录：
```bash
cp -r xiaohongshu-hot-publish ~/.openclaw/skills/
```

2. 在OpenClaw中激活技能：
   - 当用户提到"小红书发布"、"一键发布"等关键词时自动激活
   - 或手动调用技能功能

### 作为独立工具使用

```python
from create_hot_publish_page import XiaohongshuHotPublishGenerator

# 创建生成器
generator = XiaohongshuHotPublishGenerator(
    theme="你的主题",
    brand_name="你的品牌"
)

# 生成内容
generator.generate_contents(3)

# 生成页面
generator.generate_html_page("output.html")
```

## 🎯 使用示例

### 示例1：生成技术教程内容

```python
from create_hot_publish_page import XiaohongshuHotPublishGenerator

generator = XiaohongshuHotPublishGenerator(
    theme="Python数据分析",
    brand_name="数据科学家小李"
)

# 生成4个相关内容
contents = generator.generate_contents(4)

# 保存为HTML页面
generator.generate_html_page("python_data_analysis.html")

print(f"生成{len(contents)}个内容:")
for i, content in enumerate(contents, 1):
    print(f"{i}. {content['title']}")
```

### 示例2：命令行使用

```bash
# 基本用法
python create_hot_publish_page.py "AI绘画" --brand "AI艺术探索者"

# 指定内容数量
python create_hot_publish_page.py "健身计划" --brand "健身达人" --num 5

# 自定义输出文件
python create_hot_publish_page.py "旅行攻略" --brand "旅行家" --output "travel_guide.html"
```

### 示例3：批量生成

```python
import os
from create_hot_publish_page import XiaohongshuHotPublishGenerator

themes = ["Python编程", "AI工具", "效率提升", "学习方法"]

for theme in themes:
    generator = XiaohongshuHotPublishGenerator(
        theme=theme,
        brand_name="知识分享官"
    )
    
    generator.generate_contents(3)
    
    filename = f"xiaohongshu_{theme.replace(' ', '_')}.html"
    generator.generate_html_page(filename)
    
    print(f"已生成: {filename}")
```

## 📚 API文档

### XiaohongshuHotPublishGenerator类

#### 初始化参数
```python
generator = XiaohongshuHotPublishGenerator(
    theme: str,                    # 内容主题
    brand_name: str = "蒲公英AI编程", # 品牌名称
    num_contents: int = 3          # 内容数量
)
```

#### 主要方法

##### generate_contents(num_contents: int = 3) -> List[Dict]
生成指定数量的内容。

**参数：**
- `num_contents`: 生成的内容数量（1-5）

**返回值：**
- 内容列表，每个内容包含title、content、tags、time_suggestion等字段

##### generate_html_page(output_path: str = None) -> str
生成HTML发布页面。

**参数：**
- `output_path`: 输出文件路径，如不指定则自动生成

**返回值：**
- HTML内容字符串

#### 内容结构
```python
{
    'id': 1,
    'title': '📚基础教程｜Python学习的完整指南',
    'content': '小红书风格的内容文本...',
    'tags': ['Python', '基础教程', '学习分享', '小红书热点'],
    'time_suggestion': {
        'time': '10:30',
        'status': 'now',  # now/future/past
        'display': '立即发布 (10:30)'
    },
    'emoji': '📚',
    'content_type': '基础教程',
    'published': False
}
```

## ⚙️ 配置选项

### 品牌定制
```python
generator = XiaohongshuHotPublishGenerator(
    theme="你的主题",
    brand_name="你的品牌名称",  # 修改这里
    num_contents=4             # 修改内容数量
)
```

### 样式定制
编辑`template.html`文件中的CSS变量：

```css
:root {
    /* 主色调 */
    --primary-color: #4f46e5;
    --secondary-color: #7c3aed;
    
    /* 状态颜色 */
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --danger-color: #ef4444;
    
    /* 背景渐变 */
    --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --gradient-header: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
}
```

### 内容模板定制
在`create_hot_publish_page.py`中修改内容生成逻辑：

```python
def _generate_content_text(self, index: int, content_type: str) -> str:
    """自定义内容生成逻辑"""
    
    # 自定义开头
    custom_openings = [
        "🌟 今日分享：",
        "💫 独家秘籍：",
        "🎉 重磅推荐："
    ]
    
    opening = random.choice(custom_openings)
    
    # 自定义内容结构
    content = f"""{opening}

📋 今日主题：{self.theme}{content_type}

✨ 核心要点：
- 要点1：...
- 要点2：...
- 要点3：...

🚀 实施步骤：
1. 第一步...
2. 第二步...
3. 第三步...

💡 我的建议：
- 建议1
- 建议2
- 建议3

👇 互动提问：
你有什么问题或经验分享？

#{self.theme} #{content_type} #知识分享 #小红书热点"""
    
    return content
```

## 🛠️ 开发指南

### 项目结构
```
xiaohongshu-hot-publish/
├── SKILL.md                    # OpenClaw技能描述
├── README.md                   # 项目说明文档
├── create_hot_publish_page.py  # 主生成脚本
├── template.html               # HTML模板文件
├── example_usage.py            # 使用示例
├── demo.py                     # 演示脚本
├── test_skill.py               # 测试脚本
├── requirements.txt            # Python依赖
└── assets/                     # 资源文件
    ├── screenshots/            # 截图
    └── examples/               # 示例文件
```

### 添加新的内容类型

1. 在`_get_content_types()`方法中添加新类型：
```python
def _get_content_types(self) -> List[str]:
    if any(keyword in self.theme.lower() for keyword in ['美食', '烹饪', '食谱']):
        return ['食谱分享', '烹饪技巧', '食材推荐', '美食探店', '健康饮食']
    # ... 其他类型
```

2. 在`_generate_content_text()`中添加内容模板：
```python
def _generate_content_text(self, index: int, content_type: str) -> str:
    if content_type == '食谱分享':
        return self._generate_recipe_content()
    # ... 其他类型
```

3. 在`_get_content_emoji()`中添加对应的emoji：
```python
def _get_content_emoji(self, content_type: str) -> str:
    emoji_map = {
        '食谱分享': '🍳',
        '烹饪技巧': '👨‍🍳',
        # ... 其他emoji
    }
    return emoji_map.get(content_type, '📝')
```

### 运行测试
```bash
# 运行所有测试
python test_skill.py

# 运行特定测试
python -m pytest test_skill.py::test_basic_functionality
```

## 🐛 故障排除

### 常见问题

#### Q1: 复制功能不起作用
**A:** 确保：
1. 页面在HTTPS或localhost环境下运行
2. 浏览器支持Clipboard API
3. 尝试使用备用复制方法（已内置）

#### Q2: 页面显示不正常
**A:** 检查：
1. 浏览器控制台是否有错误
2. 文件路径是否正确
3. 是否使用现代浏览器（Chrome/Firefox/Safari）

#### Q3: 内容生成不符合预期
**A:** 尝试：
1. 明确主题关键词
2. 调整内容数量
3. 自定义内容模板

#### Q4: 时间显示错误
**A:** 
1. 页面使用本地时间
2. 检查系统时区设置
3. 时间每分钟自动更新

### 调试方法

1. **查看控制台输出**：
```javascript
// 在浏览器中按F12打开开发者工具
console.log('调试信息');
```

2. **检查LocalStorage**：
```javascript
// 查看保存的状态
console.log(localStorage.getItem('publishedContents'));
```

3. **测试复制功能**：
```javascript
// 测试Clipboard API
navigator.clipboard.writeText('测试文本')
    .then(() => console.log('复制成功'))
    .catch(err => console.error('复制失败:', err));
```

## 🤝 贡献指南

我们欢迎各种形式的贡献！

### 报告问题
1. 在GitHub Issues中创建新issue
2. 描述问题的详细情况
3. 提供复现步骤
4. 附上相关截图或日志

### 提交代码
1. Fork本项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

### 开发规范
- 遵循PEP 8 Python代码规范
- 添加适当的注释和文档
- 编写测试用例
- 保持代码简洁清晰

### 路线图
- [ ] 多平台支持（微博、抖音等）
- [ ] AI内容优化
- [ ] 数据分析面板
- [ ] 团队协作功能
- [ ] 云同步功能

## 📄 许可证

本项目采用MIT许可证。详见[LICENSE](LICENSE)文件。

## 📤 上传到ClawHub

### 方法1：使用上传脚本（推荐）
```bash
# 进入技能目录
cd /Users/shixiangyu/.openclaw/skills/xiaohongshu-hot-publish-optimized

# 给脚本执行权限
chmod +x publish_to_clawhub.sh

# 运行上传脚本
./publish_to_clawhub.sh
```

### 方法2：手动上传
```bash
# 1. 安装ClawHub CLI
npm i -g clawhub

# 2. 登录
clawhub login

# 3. 发布技能
clawhub publish . \
  --slug xiaohongshu-hot-publish \
  --name "小红书热点半自动化发布系统" \
  --version 1.1.0 \
  --changelog "优化版本：完整的文档、测试套件、使用示例、错误处理" \
  --tags "xiaohongshu,content-creation,automation,chinese,social-media,ai-tools"
```

### 方法3：同步所有技能
```bash
# 扫描并上传所有技能
clawhub sync --all
```

### 上传后
1. 访问 https://clawhub.ai/skills/xiaohongshu-hot-publish 查看你的技能
2. 分享链接给其他OpenClaw用户
3. 收集用户反馈，准备下一个版本

## 📞 联系方式

- **作者**: 蒲公英 (Dandelion)
- **邮箱**: your.email@example.com
- **GitHub**: [@yourusername](https://github.com/yourusername)
- **OpenClaw社区**: [Discord](https://discord.com/invite/clawd)
- **ClawHub页面**: https://clawhub.ai/skills/xiaohongshu-hot-publish

## 🙏 致谢

感谢以下项目的启发和帮助：
- [OpenClaw](https://github.com/openclaw/openclaw) - 优秀的AI助手框架
- [ClawHub](https://clawhub.ai) - OpenClaw技能共享平台
- [Playwright](https://playwright.dev/) - 强大的浏览器自动化工具
- [Tailwind CSS](https://tailwindcss.com/) - 优秀的CSS框架设计理念

---

<p align="center">
  <strong>如果这个项目对你有帮助，请给个⭐️支持一下！</strong>
</p>

<p align="center">
  <a href="#小红书热点半自动化发布系统">回到顶部</a> •
  <a href="#上传到clawhub">📤 上传到ClawHub</a>
</p>
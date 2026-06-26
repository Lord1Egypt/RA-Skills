# 贡献指南

感谢你考虑为小红书热点发布系统贡献代码！这份指南将帮助你开始贡献。

## 行为准则

本项目遵守贡献者公约。参与本项目即表示你同意遵守其条款。

## 如何贡献

### 报告问题

如果你发现了bug或者有功能建议：

1. 在GitHub Issues中搜索是否已经存在相关issue
2. 如果不存在，创建新的issue
3. 清晰描述问题或建议
4. 提供复现步骤（如果是bug）
5. 附上相关截图或日志

### 提交代码

1. Fork本项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### Pull Request流程

1. 确保所有测试通过
2. 更新相关文档
3. 遵循代码风格指南
4. 添加适当的测试用例
5. 确保提交信息清晰明了

## 开发环境设置

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/xiaohongshu-hot-publish.git
cd xiaohongshu-hot-publish
```

### 2. 创建虚拟环境（推荐）

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 运行测试

```bash
python test_skill.py
```

## 代码风格

### Python代码

遵循PEP 8规范：

```bash
# 使用black格式化代码
black create_hot_publish_page.py

# 使用flake8检查代码
flake8 create_hot_publish_page.py

# 使用mypy进行类型检查
mypy create_hot_publish_page.py
```

### 提交信息规范

使用约定式提交：

- `feat:` 新功能
- `fix:` bug修复
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建过程或辅助工具变动

示例：
```
feat: 添加新的内容类型支持
fix: 修复复制功能在Safari中的问题
docs: 更新README使用示例
```

## 项目结构

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
├── LICENSE                     # 许可证文件
├── CHANGELOG.md                # 更新日志
├── CONTRIBUTING.md             # 贡献指南
└── assets/                     # 资源文件
    ├── screenshots/            # 截图
    └── examples/               # 示例文件
```

## 添加新功能

### 添加新的内容类型

1. 在`create_hot_publish_page.py`中添加：
   - 在`_get_content_types()`中添加新类型
   - 在`_get_content_emoji()`中添加对应的emoji
   - 创建新的内容生成方法

2. 示例：
```python
def _get_content_types(self) -> List[str]:
    if any(keyword in self.theme.lower() for keyword in ['美食', '烹饪']):
        return ['食谱分享', '烹饪技巧', ...]  # 添加新类型

def _get_content_emoji(self, content_type: str) -> str:
    emoji_map = {
        '食谱分享': '🍳',  # 添加新emoji
        '烹饪技巧': '👨‍🍳',
        # ...
    }

def _generate_recipe_content(self, opening: str) -> str:
    """生成食谱类内容"""
    # 实现内容生成逻辑
```

### 修改样式

1. 编辑`template.html`中的CSS
2. 确保响应式设计正常工作
3. 测试不同浏览器的兼容性

### 添加新功能

1. 在Python端添加功能
2. 在HTML/JavaScript端实现界面
3. 添加相应的测试用例
4. 更新文档

## 测试

### 运行测试

```bash
# 运行所有测试
python test_skill.py

# 运行特定测试
python -m pytest test_skill.py::test_basic_functionality
```

### 编写测试

1. 测试函数名以`test_`开头
2. 使用assert语句验证结果
3. 测试正常情况和边界情况
4. 测试错误处理

示例：
```python
def test_new_feature():
    """测试新功能"""
    # 准备测试数据
    generator = XiaohongshuHotPublishGenerator("测试", "测试")
    
    # 执行测试
    result = generator.new_feature()
    
    # 验证结果
    assert result is not None
    assert isinstance(result, dict)
```

## 文档

### 更新文档

1. 代码变更时更新相关文档
2. 添加使用示例
3. 更新CHANGELOG.md
4. 确保所有链接有效

### 文档规范

- 使用中文编写文档
- 代码示例使用适当的语法高亮
- 添加必要的截图和示例
- 保持文档结构清晰

## 发布流程

### 版本发布

1. 更新版本号
2. 更新CHANGELOG.md
3. 运行所有测试
4. 创建发布标签
5. 发布到GitHub

### 版本号规则

- **主版本**：不兼容的API修改
- **次版本**：向下兼容的功能性新增
- **修订版本**：向下兼容的问题修正

## 获取帮助

如果你在贡献过程中遇到问题：

1. 查看现有文档
2. 搜索GitHub Issues
3. 在OpenClaw社区提问
4. 联系维护者

## 致谢

感谢所有为这个项目做出贡献的人！

---

**维护者**: 蒲公英 (Dandelion)
**项目主页**: https://github.com/yourusername/xiaohongshu-hot-publish
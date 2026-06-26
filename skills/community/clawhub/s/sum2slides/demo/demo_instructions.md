# Sum2Slides v1.0.1 演示使用说明

## 如何生成演示幻灯片

### 方法1：直接生成（需安装sum2slides）
```bash
# 确保已安装
openclaw skill install sum2slides

# 生成演示幻灯片
sum2slides --input demo/sum2slides_demo_content.txt --template business --theme colorful --output demo/sum2slides_demo.pptx
```

### 方法2：手动生成（无sum2slides）
如果您还没有安装sum2slides，可以使用以下步骤：

1. **安装依赖**:
```bash
pip install python-pptx markdown pydantic click pyyaml
```

2. **从源码安装sum2slides**:
```bash
cd /home/wwu/.openclaw/workspace/sum2slides-1.0.0
pip install -e .
```

3. **运行演示**:
```python
from sum2slides import Sum2Slides

with open("demo/sum2slides_demo_content.txt", "r") as f:
    content = f.read()

converter = Sum2Slides(template="business", theme="colorful")
presentation = converter.convert(content)
presentation.save("demo/sum2slides_demo.pptx")
```

## 演示内容结构

1. **简介** - Sum2Slides基本介绍
2. **安装** - 3种安装方式
3. **使用** - 命令行和Python API
4. **功能** - 模板、主题、配置
5. **场景** - 实际使用案例
6. **资源** - 文档和社区链接

## 自定义演示

要自定义演示内容：
1. 编辑 `demo/sum2slides_demo_content.txt`
2. 修改文本内容
3. 重新运行生成命令

## 演示用途

生成的演示幻灯片可以用于：
1. 产品介绍和演示
2. 团队培训和分享
3. 技术文档和教程
4. 社区展示和推广

## 问题解决

如果遇到问题：
1. 检查sum2slides是否安装成功
2. 查看README.md中的安装说明
3. 参考FAQ.md中的常见问题
4. 在GitHub Issues中搜索解决方案

## 联系和支持

- **GitHub**: 本地化技能版本
- **Issues**: 本地化技能版本/issues
- **Discord**: https://discord.gg/clawd

**感谢使用Sum2Slides v1.0.1！** 🚀

#!/bin/bash
# Termaid 安装脚本

set -e

echo "🔧 开始安装 Termaid..."

# 检查 Python 版本
echo "🐍 检查 Python 版本..."
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ $PYTHON_MAJOR -lt 3 ] || ([ $PYTHON_MAJOR -eq 3 ] && [ $PYTHON_MINOR -lt 11 ]); then
    echo "❌ Python 版本需要 >= 3.11，当前版本: $PYTHON_VERSION"
    echo "请先升级 Python: https://www.python.org/downloads/"
    exit 1
fi
echo "✅ Python 版本: $PYTHON_VERSION"

# 检查 pip 是否可用
echo "📦 检查 pip..."
if ! command -v pip &> /dev/null; then
    echo "❌ pip 未安装"
    echo "安装 pip: python3 -m ensurepip --upgrade"
    exit 1
fi

PIP_VERSION=$(pip --version | cut -d' ' -f2)
echo "✅ pip 版本: $PIP_VERSION"

# 安装 Termaid
echo "📦 安装 Termaid..."
pip install termaid

# 检查安装是否成功
if python3 -c "import termaid; print('Termaid version:', termaid.__version__ if hasattr(termaid, '__version__') else 'unknown')" 2>/dev/null; then
    echo "✅ Termaid 安装成功"
else
    echo "❌ Termaid 安装失败"
    exit 1
fi

# 创建示例目录
echo "📁 创建示例目录..."
mkdir -p ~/.termaid/examples

# 创建基本示例
cat > ~/.termaid/examples/basic.mmd << 'EOF'
graph TD
    A[开始] --> B{是否有效?}
    B -->|是| C[处理]
    B -->|否| D[错误]
    C --> E[完成]
EOF

cat > ~/.termaid/examples/sequence.mmd << 'EOF'
sequenceDiagram
    participant A as 客户端
    participant B as API
    A->>B: 发送请求
    B-->>A: 返回响应
    A->>B: 确认接收
EOF

cat > ~/.termaid/examples/class.mmd << 'EOF'
classDiagram
    class User {
        +String name
        +String email
        +login()
        +logout()
    }
    class Admin {
        +int permission_level
        +manage_users()
    }
    User <|-- Admin
EOF

# 创建使用示例脚本
cat > ~/.termaid/examples/run_examples.sh << 'EOF'
#!/bin/bash
# Termaid 示例演示脚本

echo "🚀 Termaid 示例演示"
echo "===================="

# 1. 基础流程图
echo ""
echo "1. 📊 基础流程图示例:"
cat ~/.termaid/examples/basic.mmd
echo ""
echo "渲染结果:"
termaid ~/.termaid/examples/basic.mmd --theme default

# 2. 序列图
echo ""
echo "2. 🔄 序列图示例:"
cat ~/.termaid/examples/sequence.mmd
echo ""
echo "渲染结果:"
termaid ~/.termaid/examples/sequence.mmd --theme neon

# 3. 类图
echo ""
echo "3. 🏗️  类图示例:"
cat ~/.termaid/examples/class.mmd
echo ""
echo "渲染结果:"
termaid ~/.termaid/examples/class.mmd --theme terra

# 4. 管道输入示例
echo ""
echo "4. 📥 管道输入示例:"
echo 'graph LR; A[数据] --> B[处理] --> C[输出]' | termaid --theme phosphor

# 5. 测试安装
echo ""
echo "5. 🔧 安装测试:"
termaid --help 2>&1 | head -5
EOF

chmod +x ~/.termaid/examples/run_examples.sh

# 创建高级功能脚本
cat > ~/.termaid/examples/advanced_usage.sh << 'EOF'
#!/bin/bash
# Termaid 高级用法示例

echo "🔬 Termaid 高级用法示例"
echo "========================"

# 创建复杂的架构图
ARCH_MD=$(cat << 'END_MD'
graph TB
    subgraph "前端"
        A1[用户界面] --> A2[Web组件]
        A2 --> A3[状态管理]
    end
    
    subgraph "后端"
        B1[API网关] --> B2[微服务]
        B2 --> B3[数据库]
    end
    
    subgraph "基础设施"
        C1[负载均衡] --> C2[容器集群]
        C2 --> C3[监控]
    end
    
    A3 --> B1
    B3 --> C3
END_MD
)

echo "$ARCH_MD" > ~/.termaid/examples/architecture.mmd

echo "1. 🏗️  复杂架构图:"
termaid ~/.termaid/examples/architecture.mmd --theme terra

echo ""
echo "2. 🎨 不同主题对比:"
echo "默认主题:"
termaid ~/.termaid/examples/basic.mmd --theme default | head -8

echo ""
echo "霓虹主题:"
termaid ~/.termaid/examples/basic.mmd --theme neon | head -8

echo ""
echo "3. ⚙️  自定义参数:"
echo "增加填充:"
termaid ~/.termaid/examples/basic.mmd --padding-x 8 --padding-y 4 | head -8

echo ""
echo "锐利边角:"
termaid ~/.termaid/examples/basic.mmd --sharp-edges | head -8

echo ""
echo "4. 📊 输出到文件:"
termaid ~/.termaid/examples/architecture.mmd --theme phosphor > ~/.termaid/examples/rendered.txt
echo "已保存到: ~/.termaid/examples/rendered.txt"
echo "文件大小: $(wc -c < ~/.termaid/examples/rendered.txt) bytes"
EOF

chmod +x ~/.termaid/examples/advanced_usage.sh

# 创建 Python API 示例
cat > ~/.termaid/examples/python_api.py << 'EOF'
#!/usr/bin/env python3
"""
Termaid Python API 示例
"""

from termaid import render
from termaid import render_rich

def demo_basic():
    """基础渲染示例"""
    print("=== 基础渲染 ===")
    
    mermaid_source = """
graph LR
    A[数据源] --> B[预处理]
    B --> C[分析]
    C --> D[可视化]
    """
    
    result = render(mermaid_source)
    print(result)

def demo_rich():
    """彩色渲染示例"""
    try:
        from rich import print as rprint
        print("\n=== 彩色渲染 ===")
        
        mermaid_source = """
graph TD
    Start([开始]) --> Input{输入数据}
    Input -->|有效| Process[处理]
    Input -->|无效| Error[错误]
    Process --> Output([完成])
    """
        
        # 使用不同主题
        themes = ["default", "terra", "neon", "amber"]
        for theme in themes:
            print(f"\n主题: {theme}")
            rich_text = render_rich(mermaid_source, theme=theme)
            rprint(rich_text)
            
    except ImportError:
        print("需要安装 termaid[rich] 扩展来使用彩色输出")
        print("安装命令: pip install termaid[rich]")

def demo_error_handling():
    """错误处理示例"""
    print("\n=== 错误处理 ===")
    
    invalid_source = "invalid mermaid syntax"
    
    try:
        result = render(invalid_source)
        print(result)
    except Exception as e:
        print(f"渲染错误: {e}")
        print("提供降级内容:")
        fallback = render("graph TD\n Error[渲染错误] --> Solution[检查语法]")
        print(fallback)

def demo_custom_params():
    """自定义参数示例"""
    print("\n=== 自定义参数 ===")
    
    source = """
graph LR
    Node1 --> Node2
    Node2 --> Node3
    """
    
    # 使用自定义填充
    result = render(source, padding_x=6, padding_y=3)
    print("自定义填充:")
    print(result)
    
    # 锐利边角
    result_sharp = render(source, sharp_edges=True)
    print("\n锐利边角:")
    print(result_sharp)

def main():
    """主函数"""
    print("Termaid Python API 演示")
    print("=" * 30)
    
    demo_basic()
    demo_rich()
    demo_error_handling()
    demo_custom_params()
    
    print("\n✅ 演示完成！")

if __name__ == "__main__":
    main()
EOF

# 创建项目配置文件
cat > ~/.termaid/config.json << 'EOF'
{
  "defaults": {
    "theme": "default",
    "padding_x": 4,
    "padding_y": 2,
    "sharp_edges": false,
    "ascii_fallback": true
  },
  "themes": {
    "favorites": ["default", "terra", "phosphor"],
    "custom": {}
  },
  "paths": {
    "examples": "~/.termaid/examples",
    "outputs": "~/.termaid/outputs",
    "templates": "~/.termaid/templates"
  }
}
EOF

# 创建快速参考卡片
cat > ~/.termaid/QUICK_REFERENCE.md << 'EOF'
# Termaid 快速参考

## 安装
```bash
pip install termaid                 # 基础版
pip install termaid[rich]          # 彩色输出
pip install termaid[textual]       # TUI 组件
```

## 基本使用
```bash
# 渲染文件
termaid diagram.mmd

# 管道输入
echo "graph LR; A-->B" | termaid

# 使用主题
termaid diagram.mmd --theme neon

# ASCII 模式
termaid diagram.mmd --ascii

# TUI 界面
termaid diagram.mmd --tui
```

## Python API
```python
from termaid import render
print(render("graph LR\\n A --> B"))

# 彩色输出
from termaid import render_rich
rprint(render_rich(source, theme="terra"))

# TUI 组件
from termaid import MermaidWidget
widget = MermaidWidget(source)
```

## 支持的图表
1. ✅ 流程图 (graph)
2. ✅ 序列图 (sequenceDiagram)
3. ✅ 类图 (classDiagram)
4. ✅ ER 图 (erDiagram)
5. ✅ 状态图 (stateDiagram-v2)
6. ✅ 块图 (block-beta)
7. ✅ Git 图 (gitGraph)
8. ✅ 饼图 (pie)
9. ✅ 树状图 (treemap-beta)

## 主题
- default: 青色节点，黄色箭头
- terra: 温暖大地色
- neon: 霓虹色调
- mono: 单色
- amber: 琥珀色 CRT
- phosphor: 绿色磷光

## 常用选项
- `--theme NAME`     颜色主题
- `--ascii`          ASCII 纯文本
- `--padding-x N`    水平填充
- `--padding-y N`    垂直填充
- `--sharp-edges`    锐利边角
- `--tui`            交互式界面
EOF

echo ""
echo "🎉 Termaid 安装完成！"
echo ""
echo "📖 下一步:"
echo "1. 运行示例演示:"
echo "   bash ~/.termaid/examples/run_examples.sh"
echo ""
echo "2. 查看高级用法:"
echo "   bash ~/.termaid/examples/advanced_usage.sh"
echo ""
echo "3. 运行 Python API 示例:"
echo "   python3 ~/.termaid/examples/python_api.py"
echo ""
echo "4. 查看快速参考:"
echo "   cat ~/.termaid/QUICK_REFERENCE.md"
echo ""
echo "📂 安装目录:"
echo "   示例文件: ~/.termaid/examples/"
echo "   配置文件: ~/.termaid/config.json"
echo "   快速参考: ~/.termaid/QUICK_REFERENCE.md"
echo ""
echo "🔗 更多信息:"
echo "   GitHub: https://github.com/fasouto/termaid"
echo "   在线试用: https://termaid.com"
echo "   PyPI: https://pypi.org/project/termaid/"
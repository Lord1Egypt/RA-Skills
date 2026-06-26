#!/usr/bin/env python3
"""
LLM Helper for xiaohongshu-card-creator
调用大语言模型将 Markdown 转换为 HTML 卡片
"""

import os
import sys
import argparse
from pathlib import Path

# 加载 .env 文件
def load_env_file():
    """加载技能目录下的 .env 文件"""
    script_dir = Path(__file__).parent.parent  # scripts/ -> xiaohongshu-card-creator/
    env_file = script_dir / '.env'
    
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip())

# 加载环境变量
load_env_file()

# 尝试导入各种 LLM SDK
try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    openai = None

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False
    anthropic = None

def load_config():
    """加载配置"""
    config = {
        'provider': os.getenv('LLM_PROVIDER', 'openai'),
        'model': os.getenv('LLM_MODEL', 'gpt-4o-mini'),
        'api_key': os.getenv('LLM_API_KEY', ''),
        'api_base': os.getenv('LLM_BASE_URL', ''),  # 支持 LLM_BASE_URL
    }
    return config

def get_system_prompt():
    """获取系统提示词"""
    return """你是一个专业的小红书卡片设计师。请将用户提供的 Markdown 内容转换为适合小红书风格的 HTML 卡片。

要求：
1. 输出必须是纯 HTML 代码，不要包含 markdown 代码块标记
2. 使用内联样式，确保在小红书 3:4 比例（414x553px）的卡片中美观展示
3. 根据内容类型自动选择合适的布局：
   - 定义解释：使用突出显示框
   - 类比说明：使用图标+文字组合
   - 列表特点：使用列表样式
   - 代码示例：使用代码块样式
4. 字体大小适中（标题 20-24px，正文 13-15px）
5. 配色使用现代渐变风格
6. 重要概念用 <strong> 加粗
7. 适当使用 emoji 增加趣味性

CSS 样式参考：
- 卡片背景可以用渐变如：linear-gradient(135deg, #667eea 0%, #764ba2 100%)
- 文字颜色确保对比度足够
- 使用 border-radius: 12px 圆角
- 使用 box-shadow 增加层次感

只返回卡片内容的 HTML div，格式如下：
<div class="card" style="...">
  ... 内容 ...
</div>

不要返回完整的 HTML 文档，只返回卡片 div 的内容。"""

def call_openai(content: str, config: dict) -> str:
    """调用 OpenAI API (兼容新旧版本)"""
    if not HAS_OPENAI:
        raise ImportError("请安装 openai: pip install openai")
    
    # 检查 openai 版本
    try:
        # 新版本 (>=1.0)
        client = openai.OpenAI(
            api_key=config['api_key'],
            base_url=config['api_base'] if config['api_base'] else None
        )
        
        response = client.chat.completions.create(
            model=config['model'],
            messages=[
                {"role": "system", "content": get_system_prompt()},
                {"role": "user", "content": f"请将以下内容转换为小红书风格的 HTML 卡片：\n\n{content}"}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    except AttributeError:
        # 旧版本 (<1.0)
        openai.api_key = config['api_key']
        if config['api_base']:
            openai.api_base = config['api_base']
        
        response = openai.ChatCompletion.create(
            model=config['model'],
            messages=[
                {"role": "system", "content": get_system_prompt()},
                {"role": "user", "content": f"请将以下内容转换为小红书风格的 HTML 卡片：\n\n{content}"}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content

def call_anthropic(content: str, config: dict) -> str:
    """调用 Claude API"""
    if not HAS_ANTHROPIC:
        raise ImportError("请安装 anthropic: pip install anthropic")
    
    client = anthropic.Anthropic(
        api_key=config['api_key'],
        base_url=config['api_base'] if config['api_base'] else None
    )
    
    response = client.messages.create(
        model=config['model'],
        max_tokens=2000,
        temperature=0.7,
        system=get_system_prompt(),
        messages=[{
            "role": "user",
            "content": f"请将以下内容转换为小红书风格的 HTML 卡片：\n\n{content}"
        }]
    )
    
    return response.content[0].text

def call_llm(content: str, config: dict = None) -> str:
    """根据配置调用相应的 LLM"""
    if config is None:
        config = load_config()
    
    if not config['api_key']:
        raise ValueError("未设置 LLM_API_KEY，请在 .env 文件中配置")
    
    provider = config['provider'].lower()
    
    if provider in ['openai', 'kimi', 'deepseek']:
        return call_openai(content, config)
    elif provider in ['claude', 'anthropic']:
        return call_anthropic(content, config)
    else:
        raise ValueError(f"不支持的 LLM provider: {provider}")

def main():
    parser = argparse.ArgumentParser(description='调用 LLM 生成小红书卡片 HTML')
    parser.add_argument('content', help='Markdown 内容文件')
    parser.add_argument('--title', help='卡片标题', default='')
    args = parser.parse_args()
    
    # 读取内容
    with open(args.content, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 添加标题
    if args.title:
        content = f"## {args.title}\n\n{content}"
    
    try:
        html = call_llm(content)
        print(html)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
使用 LLM 生成小红书卡片 HTML
"""

import os
import sys
import argparse
from pathlib import Path

# 加载 .env 文件
def load_env():
    script_dir = Path(__file__).parent.parent
    env_file = script_dir / '.env'
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip())

load_env()

# 导入 openai
try:
    import openai
except ImportError:
    print("错误: 请安装 openai: pip install openai", file=sys.stderr)
    sys.exit(1)

def call_llm(content: str) -> str:
    """调用 LLM 生成 HTML"""
    api_key = os.getenv('LLM_API_KEY')
    api_base = os.getenv('LLM_BASE_URL')
    model = os.getenv('LLM_MODEL', 'gpt-4o-mini')
    
    if not api_key:
        raise ValueError("未设置 LLM_API_KEY")
    
    # 配置 OpenAI
    openai.api_key = api_key
    if api_base:
        openai.api_base = api_base
    
    system_prompt = """你是一个专业的小红书卡片设计师。请将用户提供的 Markdown 内容转换为适合小红书风格的 HTML 卡片。

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
    
    try:
        # 新版本 API (>=1.0)
        client = openai.OpenAI(api_key=api_key, base_url=api_base)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"请转换以下内容：\n\n{content}"}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except AttributeError:
        # 如果 OpenAI 版本不支持 OpenAI 类，使用旧版
        openai.api_key = api_key
        if api_base:
            openai.api_base = api_base
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"请转换以下内容：\n\n{content}"}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content

def generate_cards(input_file: str, output_file: str, num_cards: int = 7):
    """生成卡片 HTML"""
    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取标题
    title = "小红书图文"
    for line in content.split('\n'):
        if line.startswith('# '):
            title = line[2:].strip()
            break
    
    # 提取章节
    sections = []
    current_title = None
    current_content = []
    
    for line in content.split('\n'):
        if line.startswith('## '):
            if current_title:
                sections.append((current_title, '\n'.join(current_content)))
            current_title = line[3:].strip()
            current_content = []
        elif current_title is not None:
            current_content.append(line)
    
    if current_title:
        sections.append((current_title, '\n'.join(current_content)))
    
    # 生成 HTML
    html_parts = []
    
    # 头部
    html_parts.append("""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>""" + title + """</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif;
            background: #f5f5f5;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
        }
        .controls {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
        }
        .controls button {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 600;
        }
        .card {
            width: 414px;
            height: 553px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            overflow: hidden;
            padding: 28px;
            display: flex;
            flex-direction: column;
        }
        .card-cover {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            justify-content: center;
            align-items: center;
        }
        .card-cover h1 { font-size: 28px; margin-bottom: 15px; }
        .card h2 { font-size: 22px; margin-bottom: 12px; border-bottom: 3px solid #667eea; padding-bottom: 8px; }
        .card p, .card li { font-size: 14px; line-height: 1.6; margin-bottom: 8px; }
    </style>
</head>
<body>
    <div class="controls"><button onclick="downloadAllCards()">📸 下载卡片图</button></div>
    <div id="cards-container">""")
    
    # 封面
    html_parts.append(f"""
        <!-- 第1张：封面 -->
        <div class="card card-cover" data-index="1">
            <h1>{title}</h1>
            <p style="font-size: 16px; opacity: 0.9;">AI智能生成<br>LLM驱动的内容</p>
        </div>""")
    
    # 使用 LLM 生成内容卡片
    for i, (section_title, section_content) in enumerate(sections[:num_cards-1], start=2):
        print(f"正在生成第 {i} 张卡片: {section_title}...", file=sys.stderr)
        try:
            llm_html = call_llm(f"## {section_title}\n\n{section_content}")
            # 清理代码块标记
            llm_html = llm_html.replace('```html', '').replace('```', '').strip()
            html_parts.append(f"\n        <!-- 第{i}张：{section_title} -->")
            html_parts.append(llm_html)
        except Exception as e:
            print(f"LLM 生成失败: {e}", file=sys.stderr)
            html_parts.append(f"""
        <!-- 第{i}张：{section_title} -->
        <div class="card" data-index="{i}">
            <h2>{section_title}</h2>
            <p>（LLM生成失败）</p>
        </div>""")
    
    # 页脚
    html_parts.append("""
    </div>
    <script>
        async function downloadAllCards() {
            const cards = document.querySelectorAll('.card');
            for(let i=0; i<cards.length; i++) {
                const canvas = await html2canvas(cards[i], {scale: 3});
                const link = document.createElement('a');
                link.download = 'xhs-card-' + String(i+1).padStart(2,'0') + '.png';
                link.href = canvas.toDataURL();
                link.click();
                await new Promise(r=>setTimeout(r, 500));
            }
        }
    </script>
</body>
</html>""")
    
    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_parts))
    
    print(f"✓ 卡片生成完成: {output_file}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='输入 Markdown 文件')
    parser.add_argument('-o', '--output', default='./output/xiaohongshu-cards.html', help='输出文件')
    parser.add_argument('-n', '--num-cards', type=int, default=7, help='卡片数量')
    args = parser.parse_args()
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    generate_cards(args.input, args.output, args.num_cards)

if __name__ == '__main__':
    main()

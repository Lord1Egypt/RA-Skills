#!/usr/bin/env python3
"""
Virtuoso Skill API 智能聊天机器人
根据用户的自然语言描述，推荐最合适的Skill函数/API

用法:
  python skill_chatbot.py                    # 交互模式
  python skill_chatbot.py --query "打开单元视图"  # 直接查询
  python skill_chatbot.py --web              # 启动Web服务
"""

import json
import sys
import re
import math
import gzip
from collections import defaultdict
import argparse
from pathlib import Path

class SkillAPIChatbot:
    def __init__(self, db_path=None):
        """初始化聊天机器人，加载API数据库"""
        self.functions = []
        self.categories = {}
        self.load_database(db_path)
        
    def load_database(self, db_path=None):
        """加载API数据库，自动查找可能的位置"""
        data = None
        
        if db_path and Path(db_path).exists():
            # 用户指定了数据库路径
            with open(db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            # 自动查找多个可能位置
            DB_PATHS = [
                Path(__file__).parent.parent / "references" / "skill_api_database_full.json",
                Path(__file__).parent.parent / "references" / "skill_api_database_full.gz.json",
                Path(__file__).parent.parent / "references" / "skill_api_database_full.json.gz",
                Path(__file__).parent.parent / "references" / "skill_api_database.json",
                Path(__file__).parent / "skill_api_database_full.json",
                Path(__file__).parent / "skill_api_database.json",
            ]
            
            for db_p in DB_PATHS:
                if db_p.exists():
                    if db_p.suffix == '.gz' or 'gz' in db_p.name:
                        with gzip.open(db_p, 'rt', encoding='utf-8') as f:
                            data = json.load(f)
                    else:
                        with open(db_p, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                    print(f"✅ 从 {db_p} 加载API数据库")
                    break
        
        if data is None:
            raise FileNotFoundError("找不到API数据库文件，请检查安装")
        
        # 处理不同数据库格式
        if 'function_index' in data:
            # 完整数据库格式
            self.categories = data.get('categories', {})
            self.functions = []
            for func_name, func_info in data['function_index'].items():
                self.functions.append(func_info)
        elif 'categories' in data:
            # 精简数据库格式
            self.categories = data['categories']
            self.functions = []
            for category_name, category_funcs in self.categories.items():
                for func_name, func_info in category_funcs.items():
                    func_info['category'] = category_name
                    self.functions.append(func_info)
        else:
            raise ValueError("未知的数据库格式")
        
        print(f"✅ 已加载 {len(self.functions)} 个Skill API函数")
    
    def tokenize(self, text):
        """将文本分词处理"""
        # 转为小写
        text = text.lower()
        # 提取单词和短语
        tokens = re.findall(r'[a-z0-9]+', text)
        # 添加中文单字
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
        tokens.extend(chinese_chars)
        return set([t for t in tokens if len(t) >= 1])
    
    def compute_similarity(self, query_tokens, func_info):
        """计算查询与函数的相似度得分"""
        score = 0
        
        # 函数名称匹配
        func_name = func_info['name'].lower()
        func_name_tokens = self.tokenize(func_name)
        name_overlap = len(query_tokens.intersection(func_name_tokens))
        score += name_overlap * 3  # 名称匹配权重更高
        
        # 描述匹配
        description = func_info['description'].lower()
        desc_tokens = self.tokenize(description)
        desc_overlap = len(query_tokens.intersection(desc_tokens))
        score += desc_overlap * 2
        
        # 分类匹配
        if 'category' in func_info:
            category = func_info['category'].lower()
            cat_tokens = self.tokenize(category)
            cat_overlap = len(query_tokens.intersection(cat_tokens))
            score += cat_overlap
        
        # 参数/arguments处理 - 兼容两种格式
        if 'parameters' in func_info:
            for param in func_info['parameters']:
                param_tokens = self.tokenize(param['name'].lower() + ' ' + param['description'].lower())
                param_overlap = len(query_tokens.intersection(param_tokens))
                score += param_overlap * 0.5
        elif 'arguments' in func_info:
            arg_tokens = self.tokenize(func_info['arguments'].lower())
            arg_overlap = len(query_tokens.intersection(arg_tokens))
            score += arg_overlap * 0.5
        
        # return_type也用于匹配
        if 'return_type' in func_info:
            rt_tokens = self.tokenize(str(func_info['return_type']).lower())
            rt_overlap = len(query_tokens.intersection(rt_tokens))
            score += rt_overlap * 0.2
        
        # 关键词前缀匹配 - 处理如dbOpen等前缀匹配
        for token in query_tokens:
            if len(token) >= 2 and func_name.startswith(token):
                score += 1
            if token in func_name:
                score += 0.5
        
        return score
    
    def search(self, query, top_k=5):
        """根据查询搜索最相关的API"""
        query_tokens = self.tokenize(query)
        
        results = []
        for func in self.functions:
            score = self.compute_similarity(query_tokens, func)
            if score > 0:
                results.append((score, func))
        
        # 按得分降序排序
        results.sort(key=lambda x: x[0], reverse=True)
        
        # 返回前top_k个结果
        return [func for score, func in results[:top_k]]
    
    def format_result(self, func):
        """格式化单个结果输出 - 兼容简化版和完整版数据库"""
        output = []
        category = func.get('category', '未分类')
        output.append(f"\n📌 **{func['name']}**  [{category}]")
        output.append(f"   描述: {func['description'][:200]}{'...' if len(func['description']) > 200 else ''}")
        output.append(f"   语法: `{func['syntax']}`")
        
        if 'parameters' in func and func['parameters']:
            output.append(f"   参数:")
            for p in func['parameters']:
                required = "必填" if p.get('required', True) else "可选"
                p_type = p.get('type', 'any')
                p_desc = p.get('description', '')
                output.append(f"     - {p['name']}: {p_desc} ({p_type}, {required})")
        elif 'arguments' in func and func['arguments']:
            output.append(f"   参数:")
            # 简单拆分arguments显示
            args_text = func['arguments'][:300]
            for line in args_text.split('\n'):
                if line.strip():
                    output.append(f"     - {line.strip()}")
            if len(func['arguments']) > 300:
                output.append(f"     - ...")
        
        if 'return_type' in func:
            return_type = str(func['return_type']).replace('\n', ' ').strip()
            output.append(f"   返回类型: {return_type}")
        
        if 'example' in func and func['example']:
            example = func['example'].strip()
            if example:
                output.append(f"   示例: ```skill\n{example[:300]}{'...' if len(example) > 300 else ''}\n   ```")
        
        if 'notes' in func and func['notes']:
            output.append(f"   注意: {func['notes']}")
        
        if 'reference' in func and func['reference']:
            output.append(f"   参考: {func['reference']}")
        
        return '\n'.join(output)
    
    def answer(self, query):
        """回答用户查询"""
        results = self.search(query, top_k=5)
        
        if not results:
            return "抱歉，没有找到与您描述相关的Skill API。请尝试换个说法，或者检查您的关键词。"
        
        if len(results) == 1:
            intro = "根据您的描述，找到以下最匹配的Skill API："
        else:
            intro = f"根据您的描述，找到以下{len(results)}个最相关的Skill API（按匹配度排序）："
        
        output = [intro]
        for func in results:
            output.append(self.format_result(func))
        
        return '\n'.join(output)
    
    def interactive_mode(self):
        """交互模式"""
        print("=" * 60)
        print("Virtuoso Skill API 智能查询机器人")
        print("输入您想要做什么，我会推荐合适的API函数")
        print("输入 'quit' 或 'exit' 退出")
        print("=" * 60)
        
        while True:
            try:
                query = input("\n您> ").strip()
                if query.lower() in ['quit', 'exit', 'q']:
                    print("再见！")
                    break
                if not query:
                    continue
                answer = self.answer(query)
                print(answer)
            except KeyboardInterrupt:
                print("\n再见！")
                break
            except EOFError:
                print("\n再见！")
                break
    
    def start_web_server(self, port=8080):
        """启动简易Web服务"""
        try:
            from flask import Flask, request, jsonify, render_template_string
        except ImportError:
            print("错误：需要安装flask才能启用Web模式")
            print("请运行: pip install flask")
            sys.exit(1)
        
        app = Flask(__name__)
        
        html_template = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Virtuoso Skill API 智能查询</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        h1 { color: #333; text-align: center; }
        .search-box { margin: 20px 0; }
        #query-input { width: 70%; padding: 12px; font-size: 16px; border: 2px solid #ddd; border-radius: 8px; }
        #search-btn { padding: 12px 24px; font-size: 16px; background: #007bff; color: white; border: none; border-radius: 8px; cursor: pointer; margin-left: 10px; }
        #search-btn:hover { background: #0056b3; }
        .result { background: white; margin: 15px 0; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .result h3 { margin-top: 0; color: #007bff; }
        .category { display: inline-block; background: #e9ecef; padding: 2px 8px; border-radius: 4px; font-size: 12px; color: #666; margin-left: 10px; }
        .description { color: #555; margin: 10px 0; }
        .syntax { background: #f8f9fa; padding: 10px; border-radius: 4px; font-family: monospace; margin: 10px 0; }
        .parameters { margin: 10px 0; }
        .param { margin: 5px 0; padding-left: 20px; }
        .example { background: #f0f8ff; padding: 10px; border-radius: 4px; font-family: monospace; margin: 10px 0; white-space: pre; overflow-x: auto; }
        .notes { color: #666; font-style: italic; margin: 10px 0; }
        .loading { text-align: center; color: #999; padding: 20px; }
    </style>
</head>
<body>
    <h1>🔍 Virtuoso Skill API 智能查询</h1>
    <div class="search-box">
        <input type="text" id="query-input" placeholder="描述您想要做什么，例如：打开单元视图、创建矩形、获取选中对象...">
        <button id="search-btn">搜索</button>
    </div>
    <div id="results"></div>

<script>
document.getElementById('search-btn').addEventListener('click', search);
document.getElementById('query-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') search();
});

function search() {
    const query = document.getElementById('query-input').value.trim();
    if (!query) return;
    
    document.getElementById('results').innerHTML = '<div class="loading">搜索中...</div>';
    
    fetch('/search', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({query: query})
    })
    .then(r => r.json())
    .then(data => {
        let html = '';
        if (data.results.length === 0) {
            html = '<div class="result"><p>没有找到相关API，请尝试换个关键词。</p></div>';
        } else {
            data.results.forEach(function(func) {
                html += `<div class="result">`;
                html += `<h3>${func.name} <span class="category">${func.category}</span></h3>`;
                html += `<p class="description"><strong>描述:</strong> ${func.description}</p>`;
                html += `<div class="syntax"><strong>语法:</strong> ${func.syntax}</div>`;
                
                if (func.parameters.length > 0) {
                    html += `<div class="parameters"><strong>参数:</strong><ul>`;
                    func.parameters.forEach(function(p) {
                        const required = p.required ? '必填' : '可选';
                        html += `<li class="param">${p.name}: ${p.description} (${p.type}, ${required})</li>`;
                    });
                    html += `</ul></div>`;
                }
                
                html += `<p><strong>返回类型:</strong> ${func.return_type}</p>`;
                
                if (func.example) {
                    html += `<div class="example"><strong>示例:</strong>\n${func.example}</div>`;
                }
                
                if (func.notes) {
                    html += `<p class="notes"><strong>注意:</strong> ${func.notes}</p>`;
                }
                
                html += `</div>`;
            });
        }
        document.getElementById('results').innerHTML = html;
    })
    .catch(err => {
        document.getElementById('results').innerHTML = '<div class="result"><p>搜索出错，请重试。</p></div>';
        console.error(err);
    });
}
</script>
</body>
</html>
'''
        
        @app.route('/')
        def index():
            return render_template_string(html_template)
        
        @app.route('/search', methods=['POST'])
        def search():
            query = request.json.get('query', '')
            results = self.search(query, top_k=10)
            # 转为可序列化的列表
            result_list = []
            for r in results:
                # 兼容两种数据库格式
                if 'parameters' in r:
                    parameters = r['parameters']
                else:
                    parameters = []
                
                result_list.append({
                    'name': r['name'],
                    'category': r.get('category', '未分类'),
                    'description': r['description'],
                    'syntax': r['syntax'],
                    'parameters': parameters,
                    'return_type': str(r.get('return_type', 'any')),
                    'example': r.get('example', ''),
                    'notes': r.get('notes', '')
                })
            return jsonify({'results': result_list})
        
        print(f"启动Web服务器在 http://0.0.0.0:{port}")
        print("在浏览器中打开该地址即可使用图形化查询界面")
        app.run(host='0.0.0.0', port=port, debug=False)

def main():
    parser = argparse.ArgumentParser(description='Virtuoso Skill API 智能查询机器人')
    parser.add_argument('--query', '-q', help='直接查询关键词，不进入交互模式')
    parser.add_argument('--web', '-w', action='store_true', help='启动Web服务')
    parser.add_argument('--port', '-p', type=int, default=8080, help='Web服务端口 (默认: 8080)')
    parser.add_argument('--db', '-d', default='skill_api_database_full.json', help='API数据库路径 (默认: skill_api_database_full.json，包含全部10124个API)')
    args = parser.parse_args()
    
    # 切换到脚本所在目录
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    bot = SkillAPIChatbot(args.db)
    
    if args.web:
        bot.start_web_server(args.port)
    elif args.query:
        print(bot.answer(args.query))
    else:
        bot.interactive_mode()

if __name__ == '__main__':
    main()

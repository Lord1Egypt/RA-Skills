#!/usr/bin/env python3
"""
Resume-to-Tags: 从简历文本提取原子标签，含近义词扩展
用法:
  python3 extract_tags.py --text "简历内容..."
  python3 extract_tags.py --file resume.txt
  python3 extract_tags.py --stdin  (从标准输入读取)
"""
import argparse
import json
import sys
import re
import os

# Load synonyms
SYNONYMS_PATH = os.path.join(os.path.dirname(__file__), '..', 'references', 'synonyms.json')

def load_synonyms():
    try:
        with open(SYNONYMS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def expand_with_synonyms(tags, synonyms_db):
    """用近义词扩展标签集"""
    expanded = set(tags)
    for category_key, synonym_map in synonyms_db.items():
        for tag in tags:
            # Check if this tag has synonyms → add them
            if tag in synonym_map:
                expanded.update(synonym_map[tag])
            # Check if this tag matches a synonym → add the canonical form
            for canonical, synonyms in synonym_map.items():
                if tag in synonyms:
                    expanded.add(canonical)
    return sorted(expanded)

def build_extraction_prompt(text):
    """构建简历标签提取 prompt"""
    return f"""你是一个专业的 HR 人才标签专家。请从以下简历中提取原子标签。

## 提取规则
1. **院校** → 拆解为属性标签：985/211/C9/QS排名/海外/本科/硕士/博士/理工科/社科/商科
2. **公司** → 拆解为属性标签：大厂/OTA/电商/AI创业/外企/国企/上市公司/互联网/旅游/金融等
3. **技能** → 提取核心硬技能，用标准标签名（如 RAG 而非"大模型知识库"）
4. **工具** → 提取具体软件/平台/框架
5. **领域** → 提取行业/职能领域
6. **语言** → 提取语言及水平
7. **证书** → 提取专业证书/资质/竞赛奖项
8. **工作年限** → 提取总经验年数（数字）

## 输出格式（严格 JSON）
{{
  "name": "候选人姓名",
  "years": 5,
  "school_tags": ["硕士", "海外", "QS前100", "理工科"],
  "company_tags": ["大厂", "OTA", "旅游", "上市公司"],
  "skill_tags": ["RAG", "Agent", "数据分析"],
  "tool_tags": ["LangChain", "Dify", "Python"],
  "domain_tags": ["AI/LLM", "技术架构"],
  "lang_tags": ["中文母语", "英语工作"],
  "cert_tags": ["CET6"],
  "summary": "一句话人才画像"
}}

## 简历内容
{text[:5000]}

请仅输出 JSON，不要其他文字。"""

def extract_basic_info(text):
    """预提取基础信息"""
    info = {}
    # Phone
    phones = re.findall(r'1[3-9]\d{9}', text)
    if phones: info['phone'] = phones[0]
    # Email
    emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.]+', text)
    if emails: info['email'] = emails[0]
    return info

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--text', type=str, help='简历文本')
    parser.add_argument('--file', type=str, help='简历文件路径')
    parser.add_argument('--stdin', action='store_true', help='从标准输入读取')
    parser.add_argument('--no-expand', action='store_true', help='不扩展近义词')
    parser.add_argument('--output', type=str, help='输出文件路径')
    args = parser.parse_args()

    # Get text
    if args.text:
        text = args.text
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    elif args.stdin:
        text = sys.stdin.read()
    else:
        print("Error: provide --text, --file, or --stdin", file=sys.stderr)
        sys.exit(1)

    basic = extract_basic_info(text)
    prompt = build_extraction_prompt(text)

    result = {
        "prompt": prompt,
        "basic_info": basic,
        "input_chars": len(text),
        "instructions": "将 prompt 发送给 LLM，获取 JSON 提取结果，然后用近义词扩展标签"
    }

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Output saved to {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    return prompt

if __name__ == '__main__':
    main()

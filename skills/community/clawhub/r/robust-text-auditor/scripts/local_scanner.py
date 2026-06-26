# -*- coding: utf-8 -*-
import json
import re
import argparse
import os

# 硬编码的规则文件绝对路径（可根据实际情况修改）
RULES_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'rules.json')
def normalize_text(text):
    """
    对文本进行归一化处理，移除所有非汉字、非字母、非数字的字符，
    以便更精确地匹配关键词，避免标点符号、空格等干扰。
    """
    # 保留汉字（Unicode范围 \u4e00-\u9fa5）、英文字母（a-zA-Z）、数字（0-9）
    return re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', text)

def scan_text(text_to_scan, rules_file_path=RULES_FILE_PATH):
    """
    根据规则文件扫描输入文本，并报告所有命中的关键词。

    :param text_to_scan: 待审核的原始文本字符串。
    :param rules_file_path: 规则文件的路径。
    :return: 一个包含所有命中结果的字典。
    """
    # 检查规则文件是否存在
    if not os.path.exists(rules_file_path):
        return {"status": "error", "message": f"Rules file not found at: {rules_file_path}", "hits": []}

    # 1. 读取 rules.json 文件
    try:
        with open(rules_file_path, 'r', encoding='utf-8') as f:
            rules_data = json.load(f)
            # print(rules_data)
    except Exception as e:
        return {"status": "error", "message": f"Failed to load or parse rules file: {e}", "hits": []}

    # 2. 对原始文本进行归一化处理（去除干扰字符）
    normalized_text = normalize_text(text_to_scan)

    hits = []

    # 3. 遍历所有规则分类
    for category, value in rules_data.items():
        # 处理值为列表的规则（主要情况）
        if isinstance(value, list):
            for keyword in value:
                if keyword and keyword in normalized_text:
                    hit_info = {
                        "keyword": keyword,
                        "category": category
                    }
                    if hit_info not in hits:  # 简单去重
                        hits.append(hit_info)
        # 处理值为字典的规则（嵌套情况，如 "灰区-其他高风险"）
        elif isinstance(value, dict):
            for sub_category, keywords in value.items():
                if isinstance(keywords, list):
                    for keyword in keywords:
                        if keyword and keyword in normalized_text:
                            hit_info = {
                                "keyword": keyword,
                                "category": f"{category}/{sub_category}"
                            }
                            if hit_info not in hits:
                                hits.append(hit_info)

    # 4. 返回结构化的命中报告
    return {"status": "completed", "hits": hits}

def main():
    """
    主函数，用于处理命令行调用。
    """
    parser = argparse.ArgumentParser(description="Scan text against a predefined set of rules (enhanced with normalization).")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="The text string to scan.")
    group.add_argument("--file", help="The path to a text file to scan.")

    args = parser.parse_args()

    text_content = ""
    if args.text:
        text_content = args.text
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text_content = f.read()
                # print(text_content)
        except Exception as e:
            error_result = {"status": "error", "message": f"Failed to read file {args.file}: {e}"}
            print(json.dumps(error_result, ensure_ascii=False, indent=2))
            return

    results = scan_text(text_content)
    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
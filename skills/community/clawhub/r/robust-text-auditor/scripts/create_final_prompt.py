import argparse
import json
import os
import sys

def read_file_content(file_path):
    """安全地从文件读取内容，若文件不存在则返回错误字符串。"""
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {file_path}: {e}"

def main():
    parser = argparse.ArgumentParser(description="将审核数据填充到提示词模板中。")
    parser.add_argument("--template-path", required=True, help="模板文件路径")
    parser.add_argument("--text-to-check", help="待审核文本（直接字符串）")
    parser.add_argument("--text-file", help="包含待审核文本的文件路径")
    parser.add_argument("--api-result", help="百度API结果（直接字符串）")
    parser.add_argument("--api-result-file", help="包含百度API结果的文件路径")
    parser.add_argument("--local-scan", help="本地扫描结果（直接字符串）")
    parser.add_argument("--local-scan-file", help="包含本地扫描结果的文件路径")
    parser.add_argument("--rules-path", required=True, help="规则库文件路径")
    parser.add_argument("--output-path", required=True, help="输出提示词文件路径")

    args = parser.parse_args()

    # 读取待审核文本（优先从文件）
    text_to_check = None
    if args.text_file:
        text_to_check = read_file_content(args.text_file)
    elif args.text_to_check:
        text_to_check = args.text_to_check
    else:
        print("错误：必须提供 --text-to-check 或 --text-file", file=sys.stderr)
        sys.exit(1)

    # 读取 API 结果
    api_result = None
    if args.api_result_file:
        api_result = read_file_content(args.api_result_file)
    elif args.api_result:
        api_result = args.api_result
    else:
        print("错误：必须提供 --api-result 或 --api-result-file", file=sys.stderr)
        sys.exit(1)

    # 读取本地扫描结果
    local_scan = None
    if args.local_scan_file:
        local_scan = read_file_content(args.local_scan_file)
    elif args.local_scan:
        local_scan = args.local_scan
    else:
        print("错误：必须提供 --local-scan 或 --local-scan-file", file=sys.stderr)
        sys.exit(1)

    # 读取模板和规则库
    prompt_template = read_file_content(args.template_path)
    rules_database = read_file_content(args.rules_path)

    # 组合风险清单
    master_risk_list = (
        f"### 1. 云端 API 初审返回结果\n"
        f"```json\n{api_result}\n```\n\n"
        f"### 2. 本地规则扫描敏感词返回结果\n"
        f"```json\n{local_scan}\n```"
    )

    # 执行替换
    final_prompt = prompt_template.replace('{MASTER_RISK_LIST}', master_risk_list)
    final_prompt = final_prompt.replace('{TEXT_TO_CHECK}', text_to_check)
    final_prompt = final_prompt.replace('{RULES_DATABASE}', rules_database)

    # 写入输出文件
    try:
        with open(args.output_path, 'w', encoding='utf-8') as f:
            f.write(final_prompt)
        print(f"成功：最终提示词已写入 {args.output_path}")
    except Exception as e:
        print(f"写入输出文件失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
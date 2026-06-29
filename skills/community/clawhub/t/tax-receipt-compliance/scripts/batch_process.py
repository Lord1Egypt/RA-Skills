#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量处理脚本 - 汇总目录下所有发票并生成报销单
"""

import os
import sys
import json
import argparse
from pathlib import Path

# 确保项目目录在路径里
PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

from scripts.ocr_engine import OCREngine
from scripts.receipt_parser import ReceiptParser
from scripts.template_matcher import TemplateMatcher


def process_directory(input_dir, output_path, config_path=None, template_path=None):
    """批量处理目录中的发票"""

    print(f"=== 批量发票处理 ===")
    print(f"输入目录: {input_dir}")
    print()

    # 初始化引擎
    try:
        ocr_engine = OCREngine()
    except RuntimeError as e:
        print(f"ERROR: {e}")
        return {'success': False, 'error': str(e)}

    rp = ReceiptParser()

    # 扫描文件
    supported_ext = {'.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.pdf'}
    files = [f for f in Path(input_dir).iterdir()
             if f.suffix.lower() in supported_ext]

    if not files:
        print("未找到支持的文件格式（PNG/JPG/TIFF/BMP/PDF）")
        return {'success': False, 'error': '未找到发票文件'}

    print(f"发现 {len(files)} 个文件，开始处理...\n")

    results = []
    receipts = []
    failed_files = []
    total_amount = 0.0

    for i, file_path in enumerate(files, 1):
        print(f"[{i}/{len(files)}] 识别: {file_path.name}")

        try:
            # OCR识别
            ocr_result = ocr_engine.extract_structured_data(file_path)

            if not ocr_result.get('success'):
                error_msg = ocr_result.get('error', '未知错误')
                print(f"  失败: {error_msg}")
                failed_files.append({
                    'file': str(file_path),
                    'error': error_msg,
                    'tip': ocr_result.get('tip', ''),
                    'suggestions': ocr_result.get('suggestions', [])
                })
                results.append({
                    'file': str(file_path),
                    'success': False,
                    'error': error_msg
                })
                continue

            # 解析标准化
            parsed = rp.parse(ocr_result)

            # 校验
            validation = rp.validate(parsed)
            if not validation['valid']:
                print(f"  校验不通过: {', '.join(issue['message'] for issue in validation['issues'])}")
                # 校验不通过不阻止加入receipts，但记录问题
                parsed['validation'] = validation
                results.append(parsed)
                # 如果只是警告，仍然计入
                if parsed.get('success'):
                    receipts.append(parsed)
                    total_amount += parsed.get('total', 0)
                    print(f"  类型: {parsed['invoice_type']}")
                    print(f"  金额: ¥{parsed['total']:.2f}")
                    print(f"  费用类型: {parsed['expense_type']}")
                    if validation.get('warnings'):
                        print(f"  警告: {', '.join(validation['warnings'])}")
                continue

            parsed['validation'] = validation
            results.append(parsed)

            if parsed.get('success'):
                receipts.append(parsed)
                total_amount += parsed.get('total', 0)
                print(f"  类型: {parsed['invoice_type']}")
                print(f"  金额: ¥{parsed['total']:.2f}")
                print(f"  费用类型: {parsed['expense_type']}")

        except Exception as e:
            print(f"  失败: {str(e)}")
            failed_files.append({
                'file': str(file_path),
                'error': str(e),
                'tip': '未知错误，请检查文件是否损坏'
            })
            results.append({
                'file': str(file_path),
                'success': False,
                'error': str(e)
            })

        print()

    # 汇总
    print(f"=== 处理完成 ===")
    print(f"成功识别: {len(receipts)}/{len(files)} 张发票")
    print(f"失败: {len(failed_files)} 张")
    print(f"合计金额: ¥{total_amount:.2f}")

    # 生成合并报销单
    if receipts and template_path:
        print(f"\n正在生成合并报销单...")

        try:
            matcher = TemplateMatcher(
                template_path=template_path,
                config_path=config_path
            )

            merge_result = matcher.merge_multiple_receipts(
                receipts,
                output_path=output_path
            )

            if merge_result.get('success'):
                print(f"报销单已生成: {output_path}")
            else:
                print(f"生成失败: {merge_result.get('error')}")
        except Exception as e:
            print(f"生成失败: {str(e)}")

    # 输出JSON结果
    output_data = {
        'success': True,
        'total_files': len(files),
        'processed': len(receipts),
        'total_amount': round(total_amount, 2),
        'failed_count': len(failed_files),
        'failed_files': failed_files,
        'invoices': receipts,
        'results': results,
    }

    if output_path:
        # 保存到JSON（同一目录下）
        json_path = Path(output_path).with_suffix('.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"\n详细结果已保存到: {json_path}")

    return output_data


def main():
    parser = argparse.ArgumentParser(description='批量发票处理')
    parser.add_argument('--input', required=True, help='输入目录路径')
    parser.add_argument('--output', help='输出报销单路径')
    parser.add_argument('--config', help='配置文件路径')
    parser.add_argument('--template', help='报销单模板路径')

    args = parser.parse_args()

    result = process_directory(
        input_dir=args.input,
        output_path=args.output,
        config_path=args.config,
        template_path=args.template,
    )

    print()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

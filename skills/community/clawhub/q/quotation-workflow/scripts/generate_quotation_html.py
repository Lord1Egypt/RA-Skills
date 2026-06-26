#!/usr/bin/env python3
"""生成 HTML 报价单 - 现代设计，支持打印/PDF 导出

集成多层次验证：
1. quotation_schema.py - 完整数据验证（客户/产品/条款/日期）
2. 示例数据检测 - 防止使用测试/占位符数据
3. 强制失败 - 验证失败立即终止，无交互确认
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# 导入验证模块
from quotation_schema import validate_quotation_data


def generate_html_quotation(output_path, data):
    """生成 HTML 报价单（基于提供的模板优化）"""
    
    # 🔴 P0: 完整数据验证（强制，无交互确认）
    print("🔍 验证报价单数据...")
    valid, errors = validate_quotation_data(data)
    
    if not valid:
        print("❌ 数据验证失败，报价单生成已终止:")
        print()
        for i, err in enumerate(errors, start=1):
            print(f"  {i}. {err}")
        print()
        print("请检查数据文件，确保使用真实客户信息。")
        print("如需要测试，请使用 --skip-validation 参数（仅限开发环境）")
        sys.exit(1)
    
    print("✅ 数据验证通过")
    print()
    
    # 输入校验（基础检查）
    errors = []
    customer = data.get('customer', {})
    customer_name = customer.get('company_name', customer.get('name', ''))
    if not customer_name:
        errors.append('缺少客户名称 (customer.company_name 或 customer.name)')

    products = data.get('products', [])
    if not products:
        errors.append('缺少产品列表 (products)')

    for i, p in enumerate(products):
        if not p.get('description', ''):
            errors.append(f'产品 {i+1} 缺少描述 (description)')
        if not p.get('quantity', 0):
            errors.append(f'产品 {i+1} 缺少数量 (quantity)')
        if not p.get('unit_price', p.get('unitPrice', 0)):
            errors.append(f'产品 {i+1} 缺少单价 (unit_price 或 unitPrice)')

    if errors:
        print('❌ 输入数据校验失败：')
        for e in errors:
            print(f'  - {e}')
        sys.exit(1)

    # 公司信息（Farreach）
    company_name = data.get('company_name', 'Farreach Electronic Co., Ltd.')
    company_tagline = data.get('company_tagline', 'Premium Connectivity Solutions')
    company_address = data.get('company_address', 'No. 123, Technology Road, Zhuhai, Guangdong, China')
    company_email = data.get('company_email', 'sale@farreach-electronic.com')
    company_website = data.get('company_website', 'www.farreach-electronic.com')
    
    # 客户信息（支持多种字段名）
    customer = data.get('customer', {})
    customer_name = customer.get('company_name', customer.get('name', '_________________'))
    customer_contact = customer.get('contact', customer.get('contact_name', 'Procurement Manager'))
    customer_address = customer.get('address', '_________________')
    customer_email = customer.get('email', '')
    customer_country = customer.get('country', '')
    
    # 报价单信息（支持多种字段名）
    quotation = data.get('quotation', {})
    quotation_no = quotation.get('quotation_no', data.get('quotationNo', 'QT-' + datetime.now().strftime('%Y%m%d-001')))
    quotation_date = quotation.get('date', data.get('date', datetime.now().strftime('%Y/%m/%d'))).replace('-', '/')
    valid_until = quotation.get('valid_until', data.get('validUntil', '')).replace('-', '/')
    
    # 贸易条款（支持多种字段名）
    trade_terms = data.get('trade_terms', {})
    terms = data.get('terms', {})
    incoterms = trade_terms.get('incoterms', terms.get('incoterms', 'FOB Shenzhen'))
    currency = data.get('currency', terms.get('currency', 'USD'))
    lead_time = data.get('lead_time', terms.get('delivery', '15-20 days'))
    
    # 产品列表（支持多种字段名）
    products = data.get('products', [])
    
    # 计算总额（支持 unitPrice 和 unit_price）
    subtotal = sum(p.get('quantity', 0) * p.get('unit_price', p.get('unitPrice', 0)) for p in products)
    freight = data.get('freight', 0)
    tax = data.get('tax', 0)
    total = subtotal + freight + tax
    
    # 银行信息
    bank_info = data.get('bank_info', {
        'beneficiary': 'Farreach Electronic Co., Ltd.',
        'bank_name': 'Standard Chartered Bank',
        'account_no': '1234 5678 9012',
        'swift_code': 'SCBLHKHH'
    })
    
    # 条款（支持字典和列表两种格式）
    terms_data = data.get('terms', {})
    if isinstance(terms_data, list):
        # 列表格式：直接使用
        terms_list = terms_data
        terms_maq = '500 pcs'
        terms_delivery = '15-20 days'
        terms_payment = 'T/T 30% deposit, 70% before shipment'
        terms_packaging = 'Standard packaging'
    else:
        # 字典格式：提取字段
        terms_maq = terms_data.get('moq', '500 pcs (negotiable)')
        terms_delivery = terms_data.get('delivery', '7-15 days for standard products')
        terms_payment = terms_data.get('payment', 'T/T, L/C, PayPal')
        terms_packaging = terms_data.get('packaging', 'Gift box, kraft box, PE bag, or customized')
        terms_list = [
            f'MOQ: {terms_maq}',
            f'Delivery: {terms_delivery}',
            f'Payment: {terms_payment}',
            f'Packaging: {terms_packaging}'
        ]
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quotation {quotation_no} - {customer_name}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script>
    tailwind.config = {{
        theme: {{
            extend: {{
                fontFamily: {{
                    sans: ['Inter', 'sans-serif'],
                }},
                colors: {{
                    brand: {{
                        50: '#f0fdfa',
                        100: '#ccfbf1',
                        500: '#14b8a6',
                        600: '#0d9488',
                        700: '#0f766e',
                        900: '#134e4a',
                    }}
                }}
            }}
        }}
    }}
    </script>
    <style>
        /* Fallback styles when CDN unavailable */
        .text-center {{ text-align: center; }}
        .text-right {{ text-align: right; }}
        .text-left {{ text-align: left; }}
        .font-bold {{ font-weight: 700; }}
        .font-semibold {{ font-weight: 600; }}
        .font-medium {{ font-weight: 500; }}
        .w-full {{ width: 100%; }}
        .mx-auto {{ margin-left: auto; margin-right: auto; }}
        .mb-4 {{ margin-bottom: 1rem; }}
        .mb-8 {{ margin-bottom: 2rem; }}
        .p-2 {{ padding: 0.5rem; }}
        .p-4 {{ padding: 1rem; }}
        .border {{ border: 1px solid #e2e8f0; }}
        .rounded {{ border-radius: 0.25rem; }}
        .bg-white {{ background-color: white; }}
        .text-sm {{ font-size: 0.875rem; }}
        .text-xs {{ font-size: 0.75rem; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ padding: 0.5rem; text-align: left; border-bottom: 1px solid #e2e8f0; }}

        body {{
            background-color: #f3f4f6;
            -webkit-font-smoothing: antialiased;
        }}
        .a4-container {{
            width: 210mm;
            min-height: auto;  /* 移除固定高度，让内容决定 */
            margin: 2rem auto;
            background: white;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            padding: 40mm 20mm 30mm 20mm;
            position: relative;
        }}
        @media print {{
            .a4-container {{
                padding: 5mm 0;  /* 打印时减少 padding */
            }}
        }}
        @page {{
            size: A4;
            margin: 10mm 15mm;  /* 上下 左右 */
        }}
        @media print {{
            body {{
                background-color: white;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
                margin: 0;
                padding: 0;
            }}
            .a4-container {{
                margin: 0;
                box-shadow: none;
                padding: 5mm 0;  /* 只留少量上下 padding */
                width: 100%;
                max-width: 210mm;
            }}
            html {{
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}
            .no-print {{
                display: none !important;
            }}
            /* 确保背景色打印出来 */
            .bg-slate-50 {{
                background-color: #f8fafc !important;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}
            .bg-slate-900 {{
                background-color: #0f172a !important;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}
            /* 表头文字必须白色 */
            thead th {{
                color: white !important;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}
            /* 优化分页 - 避免表格内部断裂 */
            table {{
                page-break-inside: avoid;
            }}
            tr {{
                page-break-inside: avoid;
                page-break-after: auto;
            }}
            /* 避免在标题后分页 */
            h1, h2, h3, h4, h5, h6 {{
                page-break-after: avoid;
            }}
            /* 避免在重要区块内部分页 */
            .grid {{
                page-break-inside: avoid;
            }}
            /* 确保文字颜色 */
            * {{
                color: #0f172a !important;
            }}
        }}
    </style>
</head>
<body class="text-slate-800 font-sans">

    <!-- Action Bar (Hidden on Print) -->
    <div class="no-print fixed top-4 right-4 flex gap-4">
        <button onclick="window.print()" class="bg-slate-900 hover:bg-slate-800 text-white px-6 py-2 rounded-lg font-medium shadow-lg transition-colors flex items-center gap-2">
            <i data-lucide="printer" class="w-4 h-4"></i> Export to PDF
        </button>
    </div>

    <!-- Quotation Document -->
    <div class="a4-container rounded-xl">
        
        <!-- Header -->
        <header class="flex justify-between items-start border-b-2 border-slate-100 pb-8 mb-8">
            <div>
                <h1 class="text-3xl font-bold text-slate-900 tracking-tight mb-1">{company_name}</h1>
                <p class="text-sm text-slate-500 font-medium tracking-wide">{company_tagline}</p>
                <p class="text-xs text-brand-600 font-medium italic mt-2">"real cables for real people"</p>
                
                <div class="mt-6 space-y-1 text-sm text-slate-600">
                    <p class="flex items-center gap-2"><i data-lucide="map-pin" class="w-4 h-4 text-slate-400"></i> {company_address}</p>
                    <p class="flex items-center gap-2"><i data-lucide="mail" class="w-4 h-4 text-slate-400"></i> {company_email}</p>
                    <p class="flex items-center gap-2"><i data-lucide="globe" class="w-4 h-4 text-slate-400"></i> {company_website}</p>
                </div>
            </div>
            
            <div class="text-right">
                <h2 class="text-4xl font-light text-brand-600 tracking-widest uppercase mb-4">Quotation</h2>
                <div class="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
                    <span class="text-slate-500 font-medium">Quote No:</span>
                    <span class="font-semibold text-slate-900">{quotation_no}</span>
                    <span class="text-slate-500 font-medium">Date:</span>
                    <span class="font-semibold text-slate-900">{quotation_date}</span>
                    <span class="text-slate-500 font-medium">Valid Until:</span>
                    <span class="font-semibold text-slate-900">{valid_until}</span>
                </div>
            </div>
        </header>

        <!-- Client Info -->
        <div class="grid grid-cols-2 gap-8 mb-8">
            <div class="bg-slate-50 p-5 rounded-lg border border-slate-100">
                <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Prepared For</h3>
                <p class="font-bold text-slate-900 text-lg">{customer_name}</p>
                <p class="text-sm text-slate-600 mt-1">Attn: {customer_contact}</p>
                <p class="text-sm text-slate-600 mt-1">{customer_address}</p>
            </div>
            
            <div class="bg-slate-50 p-5 rounded-lg border border-slate-100">
                <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Trade Terms</h3>
                <div class="space-y-2 text-sm">
                    <div class="flex justify-between">
                        <span class="text-slate-500">Incoterms:</span>
                        <span class="font-medium text-slate-900">{incoterms}</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-slate-500">Currency:</span>
                        <span class="font-medium text-slate-900">{currency}</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-slate-500">Lead Time:</span>
                        <span class="font-medium text-slate-900">{lead_time}</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Product Table -->
        <div class="mb-8">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-slate-900 text-white text-xs uppercase tracking-wider">
                        <th class="p-2 rounded-tl-lg font-medium w-12 text-center">No.</th>
                        <th class="p-2 font-medium">Description & Specifications</th>
                        <th class="p-2 font-medium text-center w-20">Qty</th>
                        <th class="p-2 font-medium text-right w-24">Unit Price</th>
                        <th class="p-2 rounded-tr-lg font-medium text-right w-28">Amount</th>
                    </tr>
                </thead>
                <tbody class="text-xs border-b border-slate-200">
'''
    
    # 产品行（支持 unitPrice 和 unit_price）
    for idx, product in enumerate(products, start=1):
        description = product.get('description', '')
        specification = product.get('specification', '')
        quantity = product.get('quantity', 0)
        unit_price = product.get('unit_price', product.get('unitPrice', 0))
        amount = quantity * unit_price
        
        # 规格 inline 显示（节省空间）
        spec_text = ''
        if specification:
            specs = [s.strip() for s in specification.split(',') if s.strip()]
            spec_text = ' | '.join(specs)
        
        html_content += f'''
                    <!-- Item {idx} -->
                    <tr class="border-b border-slate-100 hover:bg-slate-50 transition-colors">
                        <td class="p-2 text-center font-medium text-slate-500 text-xs">{idx:02d}</td>
                        <td class="p-2 py-1.5">
                            <p class="font-bold text-slate-900 text-xs">{description}</p>
                            <p class="text-slate-600 text-xs mt-0.5">{spec_text}</p>
                        </td>
                        <td class="p-2 text-center text-slate-700 text-xs">{quantity}</td>
                        <td class="p-2 text-right font-medium text-slate-900 text-xs">${unit_price:.2f}</td>
                        <td class="p-2 text-right font-bold text-slate-900 text-xs">${amount:,.2f}</td>
                    </tr>
'''
    
    html_content += f'''
                </tbody>
            </table>
        </div>

        <!-- Totals -->
        <div class="mb-8">
            <div class="w-full bg-slate-50 rounded-lg p-4 border border-slate-100">
                <div class="flex justify-between text-sm mb-2">
                    <span class="text-slate-500 font-medium">Subtotal</span>
                    <span class="font-semibold text-slate-900">${subtotal:,.2f}</span>
                </div>
                <div class="flex justify-between text-sm mb-4">
                    <span class="text-slate-500 font-medium">Estimated Freight</span>
                    <span class="font-semibold text-slate-900 text-sm italic">{"$" + str(freight) if freight > 0 else "To be advised"}</span>
                </div>
                <div class="flex justify-between items-center border-t-2 border-slate-200 pt-4">
                    <span class="text-xl font-bold text-slate-900">Total ({incoterms})</span>
                    <span class="text-3xl font-bold text-brand-600">${total:,.2f}</span>
                </div>
            </div>
        </div>

        <!-- Terms and Bank Info -->
        <div class="grid grid-cols-2 gap-8 text-xs border-t-2 border-slate-100 pt-6 mt-auto">
            <div>
                <h4 class="font-bold text-slate-900 mb-3 flex items-center gap-2">
                    <i data-lucide="shield-check" class="w-4 h-4 text-brand-500"></i> Terms & Conditions
                </h4>
                <ul class="text-slate-600 space-y-2 list-none">
'''
    
    for i, term in enumerate(terms_list, start=1):
        html_content += f'''
                    <li class="flex gap-2"><span class="text-brand-500 font-bold">{i}.</span> {term}</li>
'''
    
    html_content += f'''
                </ul>
            </div>
            
            <div class="pl-8 border-l border-slate-100">
                <h4 class="font-bold text-slate-900 mb-3 flex items-center gap-2">
                    <i data-lucide="building-2" class="w-4 h-4 text-brand-500"></i> Bank Details
                </h4>
                <div class="bg-slate-50 p-4 rounded text-slate-600 space-y-1">
                    <p><span class="font-medium text-slate-900">Beneficiary:</span> {bank_info.get('beneficiary', '')}</p>
                    <p><span class="font-medium text-slate-900">Bank Name:</span> {bank_info.get('bank_name', '')}</p>
                    <p><span class="font-medium text-slate-900">Account No:</span> {bank_info.get('account_no', '')}</p>
                    <p><span class="font-medium text-slate-900">SWIFT Code:</span> {bank_info.get('swift_code', '')}</p>
                </div>

                <!-- 签名区域（暂时移除，待确认） -->
                <!--
                <div class="text-center">
                    <img src="jaden_signature.png" 
                         alt="Authorized Signature" 
                         style="width: 784px; height: 112px; object-fit: contain; transform: rotate(-90deg); display: block; margin: 72px auto 2px;" />
                    <div class="border-b border-slate-300" style="width: 280px; margin: 0 auto 2px;"></div>
                    <p class="font-medium text-slate-900 text-xs" style="margin: 0; line-height: 1;">Authorized Signature</p>
                    <p class="text-slate-600 text-xs" style="margin: 0; line-height: 1;">Sales Manager</p>
                </div>
                -->
            </div>
        </div>
        
    </div>

    <script>
        // Initialize Lucide icons
        lucide.createIcons();
    </script>
</body>
</html>
'''
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_path

def main():
    parser = argparse.ArgumentParser(
        description='生成 HTML 报价单（现代设计，支持打印/PDF 导出）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 从 JSON 数据生成 HTML 报价单
  python3 generate_quotation_html.py --data quotation_data.json --output QT-20260314-001.html
  
  # 快速测试
  python3 generate_quotation_html.py --output test.html --quick-test
  
  # 在浏览器打开
  open QT-20260314-001.html
  
  # 导出 PDF（在浏览器中点击 "Export to PDF" 按钮）
  
  # 跳过验证（仅限开发环境测试）
  python3 generate_quotation_html.py --data test.json --output test.html --skip-validation
        '''
    )
    
    parser.add_argument('--data', '-d', help='报价数据 JSON 文件路径')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--quick-test', action='store_true', help='使用测试数据快速生成')
    parser.add_argument('--skip-validation', action='store_true', help='跳过数据验证（仅限开发环境，生产环境禁止使用）')
    
    args = parser.parse_args()
    
    if args.output:
        data = None
        
        if args.data:
            with open(args.data, 'r', encoding='utf-8') as f:
                data = json.load(f)
        elif args.quick_test:
            data = {
                'company_name': 'Farreach Electronic Co., Ltd.',
                'company_tagline': 'Premium Connectivity Solutions',
                'company_address': 'No. 123, Technology Road, Zhuhai, Guangdong, China',
                'company_email': 'sale@farreach-electronic.com',
                'company_website': 'www.farreach-electronic.com',
                'customer': {
                    'company_name': 'Best Buy Electronics Inc.',
                    'contact': 'Michael Johnson',
                    'address': '7601 Penn Avenue South, Richfield, MN 55423, USA'
                },
                'quotation': {
                    'quotation_no': 'QT-20260314-001',
                    'date': '2026-03-14',
                    'valid_until': '2026-04-13'
                },
                'trade_terms': {
                    'incoterms': 'FOB Shenzhen',
                    'lead_time': '15-20 days'
                },
                'products': [
                    {
                        'description': 'HDMI 2.1 Ultra High Speed Cable',
                        'specification': '8K@60Hz, 4K@120Hz, 48Gbps, HDR, eARC, 2m',
                        'quantity': 500,
                        'unit_price': 8.50
                    },
                    {
                        'description': 'HDMI 2.1 Fiber Optical Cable (AOC)',
                        'specification': '8K@60Hz, 48Gbps, Active Optical, 10m',
                        'quantity': 200,
                        'unit_price': 25.00
                    },
                    {
                        'description': 'USB-C to USB-C Cable',
                        'specification': 'USB 4.0, 80Gbps, 100W PD 2.0, 1m',
                        'quantity': 1000,
                        'unit_price': 12.00
                    }
                ],
                'currency': 'USD',
                'freight': 350.00,
                'tax': 0,
                'bank_info': {
                    'beneficiary': 'Farreach Electronic Co., Ltd.',
                    'bank_name': 'Standard Chartered Bank',
                    'account_no': '1234 5678 9012',
                    'swift_code': 'SCBLHKHH'
                }
            }
        
        if not args.data and not args.quick_test:
            print("❌ 请提供 --data 或 --quick-test", file=sys.stderr)
            sys.exit(1)
        
        # 跳过验证模式（仅限开发环境）
        if args.skip_validation:
            # 安全检查：必须设置环境变量
            import os
            if os.environ.get('QUOTATION_DEV_ENV') != 'true':
                print("❌ 错误：--skip-validation 仅限开发环境")
                print("请设置环境变量：export QUOTATION_DEV_ENV=true")
                print()
                print("⚠️  生产环境禁止跳过数据验证")
                sys.exit(1)
            
            print("⚠️  警告：开发环境，跳过数据验证")
            print()
        
        output = generate_html_quotation(args.output, data)
        print(f"✅ HTML 报价单已生成：{output}")
        print(f"💡 提示：在浏览器打开并点击 'Export to PDF' 按钮")
        return
    
    parser.print_help()

if __name__ == '__main__':
    main()

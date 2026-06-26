#!/usr/bin/env python3
"""
汇率 + PPP 购买力平价转换器
===========================

支持功能：
1. 多币种 → RMB/USD 自动换算
2. PPP 购买力平价调整（基于国别薪酬系数矩阵 v2.0）
3. 外派人员薪酬建议（COLA + hardship allowance 估算）

使用方法：
    python3 currency_converter.py -i data.csv -o output.csv
    python3 currency_converter.py -i data.csv -o output.csv --target-currency USD
    python3 currency_converter.py -i data.csv -o output.csv --target-currency CNY --with-ppp
    python3 currency_converter.py --convert 50000 --from USD --to CNY
    python3 currency_converter.py --ppp-salary 100000 --from-country US --to-country CN

汇率基准：2026-05（可手动更新）
PPP 系数来源：国别薪酬系数矩阵 v2.0（memory/country-salary-coefficients-2026.md）
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime

# ============================================================
# 汇率表（2026-05 基准，1 单位外币 = ? 人民币）
# 手动更新：修改下方字典即可
# ============================================================
EXCHANGE_RATES_TO_CNY = {
    'CNY': 1.0,
    'USD': 7.20,
    'EUR': 7.85,
    'GBP': 9.15,
    'JPY': 0.048,       # 1 JPY = 0.048 CNY
    'KRW': 0.0052,      # 1 KRW = 0.0052 CNY
    'SGD': 5.40,
    'HKD': 0.92,
    'TWD': 0.22,
    'THB': 0.21,
    'MYR': 1.62,
    'INR': 0.086,
    'VND': 0.00029,     # 1 VND = 0.00029 CNY
    'PHP': 0.126,
    'IDR': 0.00045,     # 1 IDR = 0.00045 CNY
    'AUD': 4.72,
    'CAD': 5.25,
    'CHF': 8.10,
    'AED': 1.96,
    'BRL': 1.28,
    'MXN': 0.38,
    'ZAR': 0.39,
    'NZD': 4.35,
    'SEK': 0.70,
    'NOK': 0.69,
    'DKK': 1.05,
    'RUB': 0.082,
}

# 国家/地区 → 货币映射
COUNTRY_TO_CURRENCY = {
    '中国': 'CNY', 'China': 'CNY', 'CN': 'CNY', '中国大陆': 'CNY',
    '美国': 'USD', 'USA': 'USD', 'US': 'USD', 'United States': 'USD',
    '英国': 'GBP', 'UK': 'GBP', 'GB': 'GBP', 'United Kingdom': 'GBP',
    '德国': 'EUR', 'Germany': 'EUR', 'DE': 'EUR', '法国': 'EUR', 'France': 'EUR',
    'FR': 'EUR', '意大利': 'EUR', 'Italy': 'EUR', 'IT': 'EUR',
    '西班牙': 'EUR', 'Spain': 'EUR', 'ES': 'EUR', '荷兰': 'EUR', 'Netherlands': 'EUR',
    'NL': 'EUR', '欧洲': 'EUR', 'Europe': 'EUR', 'EU': 'EUR', '欧元区': 'EUR',
    '日本': 'JPY', 'Japan': 'JPY', 'JP': 'JPY',
    '韩国': 'KRW', 'Korea': 'KRW', 'KR': 'KRW', 'South Korea': 'KRW',
    '新加坡': 'SGD', 'Singapore': 'SGD', 'SG': 'SGD',
    '香港': 'HKD', 'Hong Kong': 'HKD', 'HK': 'HKD', '中国香港': 'HKD',
    '台湾': 'TWD', 'Taiwan': 'TWD', 'TW': 'TWD', '中国台湾': 'TWD',
    '泰国': 'THB', 'Thailand': 'THB', 'TH': 'THB',
    '马来西亚': 'MYR', 'Malaysia': 'MYR', 'MY': 'MYR',
    '印度': 'INR', 'India': 'INR', 'IN': 'INR',
    '越南': 'VND', 'Vietnam': 'VND', 'VN': 'VND',
    '菲律宾': 'PHP', 'Philippines': 'PHP', 'PH': 'PHP',
    '印尼': 'IDR', 'Indonesia': 'IDR', 'ID': 'IDR',
    '澳大利亚': 'AUD', 'Australia': 'AUD', 'AU': 'AUD',
    '加拿大': 'CAD', 'Canada': 'CAD', 'CA': 'CAD',
    '瑞士': 'CHF', 'Switzerland': 'CHF', 'CH': 'CHF',
    '阿联酋': 'AED', 'UAE': 'AED', 'AE': 'AED', '迪拜': 'AED', 'Dubai': 'AED',
    '巴西': 'BRL', 'Brazil': 'BRL', 'BR': 'BRL',
    '墨西哥': 'MXN', 'Mexico': 'MXN', 'MX': 'MXN',
    '南非': 'ZAR', 'South Africa': 'ZAR', 'ZA': 'ZAR',
    '新西兰': 'NZD', 'New Zealand': 'NZD', 'NZ': 'NZD',
    '瑞典': 'SEK', 'Sweden': 'SEK', 'SE': 'SEK',
    '挪威': 'NOK', 'Norway': 'NOK', 'NO': 'NOK',
    '丹麦': 'DKK', 'Denmark': 'DKK', 'DK': 'DKK',
    '俄罗斯': 'RUB', 'Russia': 'RUB', 'RU': 'RUB',
}

# PPP 综合系数（基准：中国大陆 = 1.00）
# 来源：memory/country-salary-coefficients-2026.md
# 含义：同等生活水平的薪酬倍数（如深圳 100 万 ≈ 美国 258 万 购买力）
PPP_COEFFICIENTS = {
    '中国': 1.00, 'China': 1.00, 'CN': 1.00, '中国大陆': 1.00,
    '瑞士': 3.57, 'Switzerland': 3.57, 'CH': 3.57,
    '美国': 2.58, 'USA': 2.58, 'US': 2.58, 'United States': 2.58,
    '新加坡': 2.53, 'Singapore': 2.53, 'SG': 2.53,
    '中国香港': 1.99, 'Hong Kong': 1.99, 'HK': 1.99,
    '英国': 1.96, 'UK': 1.96, 'GB': 1.96, 'United Kingdom': 1.96,
    '阿联酋': 1.94, 'UAE': 1.94, 'AE': 1.94, '迪拜': 1.94, 'Dubai': 1.94,
    '欧洲': 1.90, 'Europe': 1.90, 'EU': 1.90, '欧元区': 1.90,
    '德国': 1.90, 'Germany': 1.90, 'DE': 1.90,
    '法国': 1.90, 'France': 1.90, 'FR': 1.90,
    '日本': 1.64, 'Japan': 1.64, 'JP': 1.64,
    '韩国': 1.63, 'Korea': 1.63, 'KR': 1.63, 'South Korea': 1.63,
    '中国台湾': 1.45, 'Taiwan': 1.45, 'TW': 1.45,
    '马来西亚': 0.90, 'Malaysia': 0.90, 'MY': 0.90,
    '泰国': 0.74, 'Thailand': 0.74, 'TH': 0.74,
    '越南': 0.65, 'Vietnam': 0.65, 'VN': 0.65,
    '菲律宾': 0.60, 'Philippines': 0.60, 'PH': 0.60,
    '印尼': 0.58, 'Indonesia': 0.58, 'ID': 0.58,
    '印度': 0.58, 'India': 0.58, 'IN': 0.58,
    '澳大利亚': 2.20, 'Australia': 2.20, 'AU': 2.20,
    '加拿大': 2.10, 'Canada': 2.10, 'CA': 2.10,
    '巴西': 0.75, 'Brazil': 0.75, 'BR': 0.75,
    '墨西哥': 0.65, 'Mexico': 0.65, 'MX': 0.65,
    '南非': 0.55, 'South Africa': 0.55, 'ZA': 0.55,
    '新西兰': 2.00, 'New Zealand': 2.00, 'NZ': 2.00,
    '瑞典': 2.00, 'Sweden': 2.00, 'SE': 2.00,
    '挪威': 2.10, 'Norway': 2.10, 'NO': 2.10,
    '丹麦': 1.95, 'Denmark': 1.95, 'DK': 1.95,
    '俄罗斯': 0.50, 'Russia': 0.50, 'RU': 0.50,
}

# 外派补贴参考（hardship allowance % of base salary）
HARDSHIP_ALLOWANCE = {
    # 艰苦地区补贴比例
    '越南': 15, 'Vietnam': 15, 'VN': 15,
    '印度': 10, 'India': 10, 'IN': 10,
    '菲律宾': 15, 'Philippines': 15, 'PH': 15,
    '印尼': 15, 'Indonesia': 15, 'ID': 15,
    '巴西': 10, 'Brazil': 10, 'BR': 10,
    '南非': 20, 'South Africa': 20, 'ZA': 20,
    '墨西哥': 10, 'Mexico': 10, 'MX': 10,
    '俄罗斯': 15, 'Russia': 15, 'RU': 15,
    '泰国': 5, 'Thailand': 5, 'TH': 5,
    '马来西亚': 5, 'Malaysia': 5, 'MY': 5,
}

# COLA（生活成本调整）参考系数
COLA_INDEX = {
    # 相对于中国大陆基准的生活成本指数
    '瑞士': 2.8, 'Switzerland': 2.8, 'CH': 2.8,
    '新加坡': 2.1, 'Singapore': 2.1, 'SG': 2.1,
    '美国': 1.8, 'USA': 1.8, 'US': 1.8, 'United States': 1.8,
    '英国': 1.6, 'UK': 1.6, 'GB': 1.6, 'United Kingdom': 1.6,
    '中国香港': 1.8, 'Hong Kong': 1.8, 'HK': 1.8,
    '日本': 1.3, 'Japan': 1.3, 'JP': 1.3,
    '韩国': 1.3, 'Korea': 1.3, 'KR': 1.3, 'South Korea': 1.3,
    '澳大利亚': 1.6, 'Australia': 1.6, 'AU': 1.6,
    '阿联酋': 1.4, 'UAE': 1.4, 'AE': 1.4, 'Dubai': 1.4,
    '中国': 1.0, 'China': 1.0, 'CN': 1.0,
    '马来西亚': 0.7, 'Malaysia': 0.7, 'MY': 0.7,
    '泰国': 0.6, 'Thailand': 0.6, 'TH': 0.6,
    '越南': 0.5, 'Vietnam': 0.5, 'VN': 0.5,
    '印度': 0.5, 'India': 0.5, 'IN': 0.5,
    '菲律宾': 0.5, 'Philippines': 0.5, 'PH': 0.5,
    '印尼': 0.5, 'Indonesia': 0.5, 'ID': 0.5,
}


def convert_currency(amount, from_currency, to_currency='CNY'):
    """货币换算：通过 CNY 作为中间货币"""
    from_upper = from_currency.upper()
    to_upper = to_currency.upper()

    if from_upper == to_upper:
        return amount

    # 先换算到 CNY
    rate_from = EXCHANGE_RATES_TO_CNY.get(from_upper)
    if rate_from is None:
        raise ValueError(f"不支持的货币: {from_upper}。支持的货币: {list(EXCHANGE_RATES_TO_CNY.keys())}")

    amount_cny = amount * rate_from

    # 再从 CNY 换算到目标货币
    rate_to = EXCHANGE_RATES_TO_CNY.get(to_upper)
    if rate_to is None:
        raise ValueError(f"不支持的货币: {to_upper}")

    return amount_cny / rate_to


def get_country_currency(country):
    """根据国家/地区获取货币"""
    return COUNTRY_TO_CURRENCY.get(country, 'CNY')


def calculate_ppp_adjusted(salary_cny, from_country, to_country='中国'):
    """
    购买力平价调整
    salary_cny: 当前以 CNY 计的薪酬
    from_country: 当前国家
    to_country: 对标基准国家（默认中国）

    返回：在 to_country 达到同等购买力需要的 CNY 薪酬
    """
    from_coeff = PPP_COEFFICIENTS.get(from_country, 1.0)
    to_coeff = PPP_COEFFICIENTS.get(to_country, 1.0)

    if from_coeff == 0:
        return salary_cny

    # 同等购买力 = salary_cny / from_coeff * to_coeff
    return salary_cny / from_coeff * to_coeff


def calculate_expat_package(base_salary_cny, host_country, home_country='中国'):
    """
    外派人员薪酬包计算
    base_salary_cny: 国内基准薪酬（CNY）
    host_country: 派驻国家
    home_country: 母国（默认中国）

    返回：建议外派薪酬包
    """
    host_cola = COLA_INDEX.get(host_country, 1.0)
    home_cola = COLA_INDEX.get(home_country, 1.0)

    # COLA 调整
    cola_adjustment = base_salary_cny * (host_cola / home_cola - 1) if home_cola > 0 else 0

    # Hardship allowance
    hardship_pct = HARDSHIP_ALLOWANCE.get(host_country, 0)
    hardship_amount = base_salary_cny * hardship_pct / 100

    # 总包
    total_package = base_salary_cny + cola_adjustment + hardship_amount

    return {
        'base_salary_cny': round(base_salary_cny, 2),
        'cola_adjustment_cny': round(cola_adjustment, 2),
        'cola_index': host_cola,
        'hardship_allowance_cny': round(hardship_amount, 2),
        'hardship_pct': hardship_pct,
        'total_package_cny': round(total_package, 2),
    }


def get_ppp_coefficient(country):
    """获取国家的 PPP 综合系数"""
    return PPP_COEFFICIENTS.get(country, 1.0)


def process_csv_with_currency(input_file, output_file=None, target_currency='CNY',
                               with_ppp=False, ppp_base_country='中国'):
    """
    处理 CSV 文件，增加货币换算和 PPP 调整

    参数:
        input_file: 输入 CSV 路径
        output_file: 输出 CSV 路径（默认 input_file_converted.csv）
        target_currency: 目标货币（CNY 或 USD）
        with_ppp: 是否计算 PPP 购买力平价调整
        ppp_base_country: PPP 对标基准国家（默认中国）
    """
    if output_file is None:
        base = os.path.splitext(input_file)[0]
        suffix = '_ppp' if with_ppp else '_converted'
        output_file = f"{base}{suffix}.csv"

    print(f"📂 加载数据：{input_file}")
    print(f"🎯 目标货币：{target_currency}")
    if with_ppp:
        print(f"📊 PPP 对标：{ppp_base_country}")

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    # 确保输出包含需要的字段
    extra_fields = []
    if 'country' not in fieldnames:
        extra_fields.append('country')
    if 'currency' not in fieldnames:
        extra_fields.append('currency')
    if 'annual_salary_usd' not in fieldnames:
        extra_fields.append('annual_salary_usd')
    if target_currency == 'CNY' and 'annual_salary_cny' not in fieldnames:
        extra_fields.append('annual_salary_cny')
    if target_currency == 'USD' and 'annual_salary_usd' not in fieldnames:
        extra_fields.append('annual_salary_usd')
    if with_ppp and 'ppp_adjusted' not in fieldnames:
        extra_fields.append('ppp_adjusted')

    output_fieldnames = list(fieldnames) + extra_fields

    converted_count = 0
    for row in rows:
        country = row.get('country', '').strip()
        currency = row.get('currency', '').strip()
        location = row.get('location', '').strip()

        # 自动推断国家和货币
        if not currency and country:
            currency = get_country_currency(country)
        elif not currency and location:
            # 尝试从地点推断
            for loc_key, curr in COUNTRY_TO_CURRENCY.items():
                if loc_key in location:
                    currency = curr
                    break

        # 尝试自动推断国家
        if not country and location:
            for loc_key in PPP_COEFFICIENTS.keys():
                if loc_key in location:
                    country = loc_key
                    break

        row['country'] = country
        row['currency'] = currency or 'CNY'

        # 年薪换算
        for salary_field in ['annual_salary_avg', 'annual_salary_low', 'annual_salary_high']:
            val = row.get(salary_field, '').strip()
            if val:
                try:
                    salary = float(val)
                    if currency and currency.upper() != target_currency.upper():
                        converted = convert_currency(salary, currency, target_currency)
                        row[salary_field] = round(converted, 2)
                except (ValueError, TypeError):
                    pass

        # USD 统一换算
        annual_avg = row.get('annual_salary_avg', '').strip()
        if annual_avg:
            try:
                salary_cny = convert_currency(float(annual_avg), currency or 'CNY', 'CNY')
                salary_usd = salary_cny / EXCHANGE_RATES_TO_CNY.get('USD', 7.20)
                row['annual_salary_usd'] = round(salary_usd, 2)

                if with_ppp and country:
                    ppp_val = calculate_ppp_adjusted(salary_cny, country, ppp_base_country)
                    row['ppp_adjusted'] = round(ppp_val, 2)

                converted_count += 1
            except (ValueError, TypeError):
                pass

    # 写入输出
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=output_fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ 转换完成：{converted_count}/{len(rows)} 条记录")
    print(f"📄 输出文件：{output_file}")
    return output_file


def main():
    parser = argparse.ArgumentParser(
        description='汇率 + PPP 购买力平价转换器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # CSV 批量换算（CNY）
  python3 currency_converter.py -i data.csv -o output.csv

  # CSV 批量换算（USD）
  python3 currency_converter.py -i data.csv -o output.csv --target-currency USD

  # CSV + PPP 购买力平价调整
  python3 currency_converter.py -i data.csv -o output.csv --with-ppp

  # 单笔货币换算
  python3 currency_converter.py --convert 50000 --from USD --to CNY

  # 单笔 PPP 对比
  python3 currency_converter.py --ppp-salary 1000000 --from-country US --to-country CN

  # 外派薪酬包计算
  python3 currency_converter.py --expat-salary 500000 --host-country SG --home-country CN
        """
    )

    # CSV 处理
    parser.add_argument('-i', '--input', help='输入 CSV 文件')
    parser.add_argument('-o', '--output', help='输出 CSV 文件')
    parser.add_argument('--target-currency', default='CNY', help='目标货币（CNY/USD，默认 CNY）')
    parser.add_argument('--with-ppp', action='store_true', help='计算 PPP 购买力平价调整')
    parser.add_argument('--ppp-base-country', default='中国', help='PPP 对标基准国家（默认中国）')

    # 单笔换算
    parser.add_argument('--convert', type=float, help='金额数值')
    parser.add_argument('--from', dest='from_currency', help='源货币')
    parser.add_argument('--to', dest='to_currency', default='CNY', help='目标货币（默认 CNY）')

    # PPP 对比
    parser.add_argument('--ppp-salary', type=float, help='薪资金额（CNY）')
    parser.add_argument('--from-country', help='当前国家')
    parser.add_argument('--to-country', default='中国', help='对标国家（默认中国）')

    # 外派薪酬
    parser.add_argument('--expat-salary', type=float, help='国内基准薪酬（CNY）')
    parser.add_argument('--host-country', help='派驻国家')
    parser.add_argument('--home-country', default='中国', help='母国（默认中国）')

    args = parser.parse_args()

    # 单笔货币换算
    if args.convert is not None and args.from_currency:
        result = convert_currency(args.convert, args.from_currency, args.to_currency)
        print(f"💱 {args.convert} {args.from_currency.upper()} = {result:.2f} {args.to_currency.upper()}")
        return

    # PPP 对比
    if args.ppp_salary is not None and args.from_country:
        result = calculate_ppp_adjusted(args.ppp_salary, args.from_country, args.to_country)
        from_coeff = get_ppp_coefficient(args.from_country)
        to_coeff = get_ppp_coefficient(args.to_country)
        print(f"📊 PPP 购买力对比：")
        print(f"   {args.from_country}: ¥{args.ppp_salary:,.0f} (系数 {from_coeff})")
        print(f"   ≈ {args.to_country}: ¥{result:,.0f} (系数 {to_coeff})")
        print(f"   同等生活水平")
        return

    # 外派薪酬
    if args.expat_salary is not None and args.host_country:
        pkg = calculate_expat_package(args.expat_salary, args.host_country, args.home_country)
        print(f"🌍 外派薪酬包建议 ({args.host_country}):")
        print(f"   基准薪酬: ¥{pkg['base_salary_cny']:,.0f}")
        print(f"   COLA 调整: ¥{pkg['cola_adjustment_cny']:+,.0f} (指数 {pkg['cola_index']})")
        print(f"   艰苦补贴: ¥{pkg['hardship_allowance_cny']:,.0f} ({pkg['hardship_pct']}%)")
        print(f"   ─────────────")
        print(f"   总包: ¥{pkg['total_package_cny']:,.0f}")
        return

    # CSV 批量处理
    if args.input:
        process_csv_with_currency(
            args.input, args.output,
            target_currency=args.target_currency,
            with_ppp=args.with_ppp,
            ppp_base_country=args.ppp_base_country
        )
        return

    parser.print_help()


if __name__ == '__main__':
    main()

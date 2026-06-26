#!/usr/bin/env python3
"""
Unit Converter Skill
Supports comprehensive unit conversions including offline basic units and online currency exchange rates.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import requests
except ImportError:
    print("Error: 'requests' library is required. Install with: pip install requests")
    sys.exit(1)


class UnitConverter:
    """Main unit converter class handling both offline and online conversions."""

    def __init__(self):
        self.cache_file = Path.home() / ".unit_converter_cache.json"
        self.cache_duration = 3600  # 1 hour in seconds

        # Offline conversion factors (to base unit)
        self.length_factors = {
            'm': 1.0,
            'meter': 1.0,
            'meters': 1.0,
            'km': 1000.0,
            'kilometer': 1000.0,
            'kilometers': 1000.0,
            'cm': 0.01,
            'centimeter': 0.01,
            'centimeters': 0.01,
            'mm': 0.001,
            'millimeter': 0.001,
            'millimeters': 0.001,
            'mi': 1609.344,
            'mile': 1609.344,
            'miles': 1609.344,
            'ft': 0.3048,
            'foot': 0.3048,
            'feet': 0.3048,
            'in': 0.0254,
            'inch': 0.0254,
            'inches': 0.0254,
            'yd': 0.9144,
            'yard': 0.9144,
            'yards': 0.9144,
            'nmi': 1852.0,
            'nautical_mile': 1852.0,
            'nautical_miles': 1852.0,
            '海里': 1852.0,
            '里': 500.0,  # Chinese li (市里)
            '丈': 3.333333333333333,  # Chinese zhang (市丈)
            '尺': 0.3333333333333333,  # Chinese chi (市尺)
            '寸': 0.03333333333333333,  # Chinese cun (市寸)
        }

        self.weight_factors = {
            'kg': 1.0,
            'kilogram': 1.0,
            'kilograms': 1.0,
            'g': 0.001,
            'gram': 0.001,
            'grams': 0.001,
            'mg': 0.000001,
            'milligram': 0.000001,
            'milligrams': 0.000001,
            't': 1000.0,
            'ton': 1000.0,
            'tons': 1000.0,
            'lb': 0.45359237,
            'pound': 0.45359237,
            'pounds': 0.45359237,
            'oz': 0.028349523125,
            'ounce': 0.028349523125,
            'ounces': 0.028349523125,
            '斤': 0.5,  # Chinese jin (市斤)
            '两': 0.05,  # Chinese liang (市两)
            '钱': 0.005,  # Chinese qian (市钱)
        }

        self.area_factors = {
            'm2': 1.0,
            'sq_m': 1.0,
            'square_meter': 1.0,
            'square_meters': 1.0,
            '平方米': 1.0,
            'km2': 1000000.0,
            'sq_km': 1000000.0,
            'square_kilometer': 1000000.0,
            '平方千米': 1000000.0,
            'ha': 10000.0,
            'hectare': 10000.0,
            'hectares': 10000.0,
            '公顷': 10000.0,
            'mu': 666.6666666666666,  # Chinese mu (市亩)
            '亩': 666.6666666666666,
            'sq_ft': 0.09290304,
            'square_foot': 0.09290304,
            '平方英尺': 0.09290304,
            'sq_in': 0.00064516,
            'square_inch': 0.00064516,
            '平方英寸': 0.00064516,
            'sq_yd': 0.83612736,
            'square_yard': 0.83612736,
            '平方码': 0.83612736,
        }

        self.volume_factors = {
            'm3': 1.0,
            'cubic_meter': 1.0,
            '立方米': 1.0,
            'l': 0.001,
            'L': 0.001,
            'liter': 0.001,
            'litre': 0.001,
            '升': 0.001,
            'ml': 0.000001,
            'mL': 0.000001,
            'milliliter': 0.000001,
            'millilitre': 0.000001,
            '毫升': 0.000001,
            'cm3': 0.000001,
            'cubic_centimeter': 0.000001,
            '立方厘米': 0.000001,
            'gal_us': 0.003785411784,
            'gallon_us': 0.003785411784,
            'us_gallon': 0.003785411784,
            'gal_uk': 0.00454609,
            'gallon_uk': 0.00454609,
            'uk_gallon': 0.00454609,
            '加仑': 0.003785411784,  # default US gallon
            'qt': 0.000946352946,
            'quart': 0.000946352946,
            'quarts': 0.000946352946,
            'qt_us': 0.000946352946,
            'pt': 0.000473176473,
            'pint': 0.000473176473,
            'pints': 0.000473176473,
            'pt_us': 0.000473176473,
            'cup': 0.0002365882365,
            'cups': 0.0002365882365,
            '杯': 0.0002365882365,  # metric cup? Actually Chinese cup is usually 200ml, but we use US cup for simplicity
        }

        self.time_factors = {
            's': 1.0,
            'sec': 1.0,
            'second': 1.0,
            'seconds': 1.0,
            '秒': 1.0,
            'min': 60.0,
            'minute': 60.0,
            'minutes': 60.0,
            '分钟': 60.0,
            'h': 3600.0,
            'hr': 3600.0,
            'hour': 3600.0,
            'hours': 3600.0,
            '小时': 3600.0,
            'd': 86400.0,
            'day': 86400.0,
            'days': 86400.0,
            '天': 86400.0,
            'wk': 604800.0,
            'week': 604800.0,
            'weeks': 604800.0,
            '周': 604800.0,
            'mo': 2629746.0,  # average month (365.25/12 days)
            'month': 2629746.0,
            'months': 2629746.0,
            '月': 2629746.0,  # Chinese month
            'yr': 31557600.0,  # average year (365.25 days)
            'year': 31557600.0,
            'years': 31557600.0,
            '年': 31557600.0,  # Chinese year
            'ms': 0.001,
            'millisecond': 0.001,
            'milliseconds': 0.001,
            '毫秒': 0.001,
            'us': 0.000001,
            'microsecond': 0.000001,
            'microseconds': 0.000001,
            '微秒': 0.000001,
        }

        self.speed_factors = {
            'm/s': 1.0,
            'meter_per_second': 1.0,
            '米/秒': 1.0,
            'km/h': 0.2777777777777778,
            'kilometer_per_hour': 0.2777777777777778,
            '千米/小时': 0.2777777777777778,
            'mph': 0.44704,
            'mile_per_hour': 0.44704,
            '英里/小时': 0.44704,
            'ft/s': 0.3048,
            'foot_per_second': 0.3048,
            '英尺/秒': 0.3048,
            'mach': 343.0,  # at sea level, 20°C
            '马赫': 343.0,
        }

        self.data_factors = {
            'b': 1.0,
            'bit': 1.0,
            'bits': 1.0,
            '比特': 1.0,
            'B': 8.0,
            'byte': 8.0,
            'bytes': 8.0,
            '字节': 8.0,
            'KB': 8 * 1024.0,
            'kilobyte': 8 * 1024.0,
            'KB': 8 * 1000.0,  # also support decimal KB?
            'kB': 8 * 1024.0,  # kibibyte? Actually we'll treat as 1024 bytes for simplicity in this converter, but could be ambiguous. We'll use binary prefixes: KiB = 1024, KB = 1000? We'll use common convention: KB=1024 bytes, but I'll define both. To avoid confusion, I'll implement both: KB (1000) and KiB (1024). However the user expects common units: KB, MB, GB, TB, PB. Typically these are 1024-based. I'll use 1024.
            'KiB': 8 * 1024.0,
            'MB': 8 * 1024 * 1024.0,
            'megabyte': 8 * 1024 * 1024.0,
            'MB': 8 * 1000 * 1000.0,
            'MiB': 8 * 1024 * 1024.0,
            'GB': 8 * 1024 * 1024 * 1024.0,
            'gigabyte': 8 * 1024 * 1024 * 1024.0,
            'GiB': 8 * 1024 * 1024 * 1024.0,
            'TB': 8 * 1024 * 1024 * 1024 * 1024.0,
            'terabyte': 8 * 1024 * 1024 * 1024 * 1024.0,
            'TiB': 8 * 1024 * 1024 * 1024 * 1024.0,
            'PB': 8 * 1024 * 1024 * 1024 * 1024 * 1024.0,
            'petabyte': 8 * 1024 * 1024 * 1024 * 1024 * 1024.0,
            'PiB': 8 * 1024 * 1024 * 1024 * 1024 * 1024.0,
        }
        # Actually to keep simple, I'll just support common decimal-based units: b, B, KB, MB, GB, TB, PB with factors based on 1000 or 1024? I'll use 1024 for KiB style but many use 1000. I'll provide both? To avoid confusion, I'll use binary (1024) for KB, MB, etc because those are typically used for memory/storage. I'll also add 'Kb', 'Mb', etc for kilobits? But the user only listed: 比特、字节、KB、MB、GB、TB、PB. So they likely mean bits and bytes with powers of 1024. I'll map:
        # bit -> 1
        # byte -> 8
        # KB -> 8*1024 (kilobyte)
        # MB -> 8*1024^2
        # GB -> 8*1024^3
        # TB -> 8*1024^4
        # PB -> 8*1024^5
        # I'll also accept lowercase: kb, mb, gb, tb, pb (but these are usually kilobits etc). I'll treat them same as uppercase for simplicity? Maybe I'll differentiate: lowercase kb = 1000 bits? But the user didn't ask for that. So to be safe, I'll accept both and treat them as 1024-based bytes multiples. I'll also add 'K', 'M', 'G', 'T', 'P' as alternatives? No, keep it simple.

        # Redefine data_factors with clear mapping:
        self.data_factors = {
            'b': 1.0, 'bit': 1.0, '比特': 1.0,
            'B': 8.0, 'byte': 8.0, '字节': 8.0,
            'KB': 8 * 1024.0, 'kilobyte': 8 * 1024.0,
            'MB': 8 * 1024**2.0, 'megabyte': 8 * 1024**2.0,
            'GB': 8 * 1024**3.0, 'gigabyte': 8 * 1024**3.0,
            'TB': 8 * 1024**4.0, 'terabyte': 8 * 1024**4.0,
            'PB': 8 * 1024**5.0, 'petabyte': 8 * 1024**5.0,
        }

        self.energy_factors = {
            'J': 1.0,
            'joule': 1.0,
            'joules': 1.0,
            '焦耳': 1.0,
            'cal': 4.184,
            'calorie': 4.184,
            'calories': 4.184,
            '卡路里': 4.184,
            'kcal': 4184.0,
            'cal': 4184.0,  # actually kcal is Cal with capital C, but we'll support both
            'kilocalorie': 4184.0,
            '千卡': 4184.0,
            'kWh': 3600000.0,
            'wh': 3600.0,  # watt-hour
            'W·h': 3600.0,
            '千瓦时': 3600000.0,
            'eV': 1.602176634e-19,
            'electronvolt': 1.602176634e-19,
            '电子伏特': 1.602176634e-19,
        }

        self.power_factors = {
            'W': 1.0,
            'watt': 1.0,
            'watts': 1.0,
            '瓦': 1.0,
            'kW': 1000.0,
            'kilowatt': 1000.0,
            '千瓦': 1000.0,
            'hp': 745.699872,
            'horsepower': 745.699872,
            '马力': 745.699872,
            'hp_uk': 745.699872,  # same as metric? Actually imperial horsepower is 745.7, metric is 735.5. We'll use metric? I'll include both: hp (mechanical) ~745.7, hp_m (metric) ~735.5. But user said 马力 which usually refers to metric horsepower (公制马力) = 735.49875 W. However many use 735.5. I'll set metric as 735.5? Actually I'll define two: hp (imperial) = 745.7, and hp_metric (metric) = 735.5. But to keep simple, I'll use the standard mechanical horsepower 745.699872 W, but note Chinese "马力" often means metric horsepower. I'll add a separate key for metric: 'hp_metric' or '公制马力'? I'll just include both: 'hp' as imperial, 'metric_hp' as metric. But I'll also map '马力' to metric horsepower (735.5). Let's define:
            'metric_hp': 735.49875,
            'metric_horsepower': 735.49875,
            '公制马力': 735.49875,
        }

        # For pressure
        self.pressure_factors = {
            'Pa': 1.0,
            'pascal': 1.0,
            '帕斯卡': 1.0,
            'kPa': 1000.0,
            'kilopascal': 1000.0,
            '千帕': 1000.0,
            'MPa': 1000000.0,
            'megapascal': 1000000.0,
            '兆帕': 1000000.0,
            'bar': 100000.0,
            '巴': 100000.0,
            'atm': 101325.0,
            'standard_atmosphere': 101325.0,
            '标准大气压': 101325.0,
            'mmHg': 133.322387415,
            'mmhg': 133.322387415,
            '毫米汞柱': 133.322387415,
        }

        # Temperature conversion requires formulas, not simple factors
        self.temperature_units = {'celsius', 'fahrenheit', 'kelvin', 'c', 'f', 'k',
                                   '摄氏度', '华氏度', '开尔文'}

        # Currency codes (ISO 4217)
        self.currency_aliases = {
            'usd': 'USD', 'dollar': 'USD', 'dollars': 'USD', '美元': 'USD',
            'eur': 'EUR', 'euro': 'EUR', 'euros': 'EUR', '欧元': 'EUR',
            'cny': 'CNY', 'rmb': 'CNY', 'yuan': 'CNY', 'renminbi': 'CNY', '人民币': 'CNY',
            'jpy': 'JPY', 'yen': 'JPY', '日元': 'JPY',
            'gbp': 'GBP', 'pound': 'GBP', 'pounds': 'GBP', '英镑': 'GBP',
            'hkd': 'HKD', '香港元': 'HKD', '港元': 'HKD',
            'aud': 'AUD', 'australian_dollar': 'AUD', '澳元': 'AUD',
            'cad': 'CAD', 'canadian_dollar': 'CAD', '加元': 'CAD',
            'chf': 'CHF', 'swiss_franc': 'CHF', '瑞士法郎': 'CHF',
            'sgd': 'SGD', 'singapore_dollar': 'SGD', '新加坡元': 'SGD',
            'inr': 'INR', 'indian_rupee': 'INR', '印度卢比': 'INR',
            'rub': 'RUB', 'russian_ruble': 'RUB', '卢布': 'RUB',
            'brl': 'BRL', 'brazilian_real': 'BRL', '巴西雷亚尔': 'BRL',
            'krw': 'KRW', 'south_korean_won': 'KRW', '韩元': 'KRW',
            'thb': 'THB', 'thai_baht': 'THB', '泰铢': 'THB',
            'myr': 'MYR', 'malaysian_ringgit': 'MYR', '马来西亚林吉特': 'MYR',
            # Add more as needed
        }

    def convert_temperature(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert temperature between Celsius, Fahrenheit, Kelvin."""
        # First convert to Kelvin
        if from_unit in ('c', 'celsius', '摄氏度'):
            kelvin = value + 273.15
        elif from_unit in ('f', 'fahrenheit', '华氏度'):
            kelvin = (value + 459.67) * 5 / 9
        elif from_unit in ('k', 'kelvin', '开尔文'):
            kelvin = value
        else:
            raise ValueError(f"Unsupported temperature unit: {from_unit}")

        # Then convert from Kelvin to target
        if to_unit in ('c', 'celsius', '摄氏度'):
            return kelvin - 273.15
        elif to_unit in ('f', 'fahrenheit', '华氏度'):
            return kelvin * 9 / 5 - 459.67
        elif to_unit in ('k', 'kelvin', '开尔文'):
            return kelvin
        else:
            raise ValueError(f"Unsupported temperature unit: {to_unit}")

    def convert_offline(self, value: float, from_unit: str, to_unit: str, category: Dict[str, float]) -> float:
        """Generic conversion using factor dictionaries."""
        from_factor = category.get(from_unit)
        to_factor = category.get(to_unit)
        if from_factor is None:
            raise ValueError(f"Unsupported unit: {from_unit}")
        if to_factor is None:
            raise ValueError(f"Unsupported unit: {to_unit}")
        # Convert to base, then to target
        base_value = value * from_factor
        return base_value / to_factor

    def detect_category(self, from_unit: str, to_unit: str) -> Optional[Dict[str, float]]:
        """Detect which conversion category the units belong to."""
        units = (from_unit.lower().replace(' ', '_'), to_unit.lower().replace(' ', '_'))
        categories = [
            (self.length_factors, 'length'),
            (self.weight_factors, 'weight'),
            (self.area_factors, 'area'),
            (self.volume_factors, 'volume'),
            (self.time_factors, 'time'),
            (self.speed_factors, 'speed'),
            (self.data_factors, 'data'),
            (self.energy_factors, 'energy'),
            (self.pressure_factors, 'pressure'),
            (self.power_factors, 'power'),
        ]
        for cat_dict, cat_name in categories:
            if all(u in cat_dict for u in units):
                return cat_dict
        return None

    def fetch_currency_rates(self, base_currency: str = 'USD') -> Dict[str, Any]:
        """Fetch currency exchange rates from API with caching."""
        # Check cache first
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    cache = json.load(f)
                cache_time = cache.get('timestamp', 0)
                if time.time() - cache_time < self.cache_duration:
                    # Also check if base matches
                    if cache.get('base', '').upper() == base_currency.upper():
                        return cache
            except Exception:
                pass  # ignore cache errors

        # Fetch fresh data
        url = f"https://api.exchangerate.host/latest?base={base_currency.upper()}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if not data.get('success', True):
                raise Exception(f"API error: {data.get('error', 'Unknown error')}")
            # Add timestamp and save to cache
            data['timestamp'] = time.time()
            with open(self.cache_file, 'w') as f:
                json.dump(data, f)
            return data
        except Exception as e:
            raise ConnectionError(f"Failed to fetch currency rates: {e}")

    def convert_currency(self, value: float, from_currency: str, to_currency: str) -> float:
        """Convert between currencies using online API."""
        # Normalize currency codes
        from_curr = self.currency_aliases.get(from_currency.lower(), from_currency.upper())
        to_curr = self.currency_aliases.get(to_currency.lower(), to_currency.upper())

        # Fetch rates with base = from_currency
        try:
            data = self.fetch_currency_rates(from_curr)
        except Exception as e:
            # If base currency not supported, try converting via USD
            try:
                # Get USD rates
                data_usd = self.fetch_currency_rates('USD')
                rate_from = data_usd['rates'].get(from_curr)
                rate_to = data_usd['rates'].get(to_curr)
                if rate_from is None or rate_to is None:
                    raise ValueError(f"Currency not supported: {from_curr if rate_from is None else to_curr}")
                # Convert: value * (rate_from / rate_to)
                return value * (rate_from / rate_to)
            except Exception as e2:
                raise ConnectionError(f"Failed to convert currency: {e2}")

        rates = data.get('rates', {})
        if to_curr not in rates:
            raise ValueError(f"Unsupported target currency: {to_curr}")
        rate = rates[to_curr]
        return value * rate

    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        """Main conversion method that routes to appropriate converter."""
        # Check if temperature conversion
        temp_units = set(self.temperature_units)
        if from_unit in temp_units and to_unit in temp_units:
            return self.convert_temperature(value, from_unit, to_unit)

        # Check if it might be currency (3-letter code or known alias)
        curr_from = from_unit.lower()
        curr_to = to_unit.lower()
        # Heuristic: if both units are 3 letters or known currency aliases, try currency conversion
        if (len(curr_from) == 3 and len(curr_to) == 3) or \
           (curr_from in self.currency_aliases and curr_to in self.currency_aliases) or \
           (curr_from in ['usd', 'eur', 'cny', 'jpy', 'gbp', 'hkd', 'aud', 'cad', 'chf', 'sgd', 'inr', 'rub', 'brl', 'krw', 'thb', 'myr'] and \
            curr_to in ['usd', 'eur', 'cny', 'jpy', 'gbp', 'hkd', 'aud', 'cad', 'chf', 'sgd', 'inr', 'rub', 'brl', 'krw', 'thb', 'myr']):
            return self.convert_currency(value, from_unit, to_unit)

        # Else try offline categories
        category = self.detect_category(from_unit, to_unit)
        if category is not None:
            return self.convert_offline(value, from_unit, to_unit, category)

        raise ValueError(f"Cannot convert {from_unit} to {to_unit}. Unsupported units.")

    def get_available_units(self) -> str:
        """Return a string listing all available units by category."""
        lines = []
        lines.append("长度: m, km, cm, mm, mi, ft, in, yd, nmi, 里, 丈, 尺, 寸")
        lines.append("重量: kg, g, mg, t, lb, oz, 斤, 两, 钱")
        lines.append("面积: m2, km2, ha, mu, sq_ft, sq_in, sq_yd, 平方米, 平方千米, 公顷, 亩")
        lines.append("体积/容积: m3, l, ml, cm3, gal_us, gal_uk, qt, pt, cup, 立方米, 升, 毫升, 立方厘米, 加仑")
        lines.append("温度: c, f, k, 摄氏度, 华氏度, 开尔文")
        lines.append("时间: s, min, h, d, wk, mo, yr, ms, us, 秒, 分钟, 小时, 天, 周, 月, 年, 毫秒, 微秒")
        lines.append("速度: m/s, km/h, mph, ft/s, mach, 米/秒, 千米/小时, 英里/小时, 英尺/秒, 马赫")
        lines.append("数据存储: b, B, KB, MB, GB, TB, PB, 比特, 字节")
        lines.append("能量: J, cal, kcal, kWh, eV, 焦耳, 卡路里, 千卡, 千瓦时, 电子伏特")
        lines.append("功率: W, kW, hp, metric_hp, 瓦, 千瓦, 马力, 公制马力")
        lines.append("压力: Pa, kPa, MPa, bar, atm, mmHg, 帕斯卡, 千帕, 兆帕, 巴, 标准大气压, 毫米汞柱")
        lines.append("货币 (需联网): USD, EUR, CNY, JPY, GBP, HKD, AUD, CAD, CHF, SGD, INR, RUB, BRL, KRW, THB, MYR 等150+种货币")
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Unit Converter - 离线基础单位换算 & 在线货币汇率换算',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s convert 100 meters feet
  %(prog)s convert 25 Celsius Fahrenheit
  %(prog)s convert 100 USD CNY
  %(prog)s convert 1 kg 斤
  %(prog)s convert 100 miles km
        """
    )
    parser.add_argument('command', nargs='?', choices=['convert', 'list'], help='Command to execute')
    parser.add_argument('value', nargs='?', type=float, help='Value to convert')
    parser.add_argument('from_unit', nargs='?', help='Source unit')
    parser.add_argument('to_unit', nargs='?', help='Target unit')

    args = parser.parse_args()

    converter = UnitConverter()

    if args.command == 'list' or (args.command is None and len(sys.argv) == 1):
        print(converter.get_available_units())
        return

    if args.value is None or args.from_unit is None or args.to_unit is None:
        parser.print_help()
        print("\n错误: 请提供要转换的数值、源单位和目标单位")
        sys.exit(1)

    try:
        result = converter.convert(args.value, args.from_unit, args.to_unit)
        # Format output
        # If result is very large or very small, use scientific notation; otherwise, plain
        if abs(result) >= 1e6 or (abs(result) < 1e-3 and result != 0):
            result_str = f"{result:.6e}"
        else:
            # For typical usage, round to reasonable precision
            # Determine if original value is integer
            if args.value.is_integer():
                result_str = f"{result:.6g}".rstrip('0').rstrip('.') if '.' in f"{result:.6g}" else str(int(round(result)))
            else:
                # Show up to 6 significant figures
                result_str = f"{result:.6g}"
        print(f"{args.value} {args.from_unit} = {result_str} {args.to_unit}")
    except Exception as e:
        print(f"转换错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
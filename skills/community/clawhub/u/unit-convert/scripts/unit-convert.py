#!/usr/bin/env python3
"""
Unit Converter
单位转换工具
支持长度、重量、温度、面积、体积等多种单位转换
"""

import sys

def convert_length(value, from_unit, to_unit):
    """长度转换"""
    # 转换为米
    to_meter = {
        "mm": 0.001, "cm": 0.01, "m": 1, "km": 1000,
        "in": 0.0254, "ft": 0.3048, "yd": 0.9144, "mi": 1609.344,
        "inch": 0.0254, "foot": 0.3048, "yard": 0.9144, "mile": 1609.344
    }
    
    if from_unit not in to_meter or to_unit not in to_meter:
        return None
    
    meters = value * to_meter[from_unit]
    result = meters / to_meter[to_unit]
    return result

def convert_weight(value, from_unit, to_unit):
    """重量转换"""
    # 转换为克
    to_gram = {
        "mg": 0.001, "g": 1, "kg": 1000, "t": 1000000,
        "oz": 28.3495, "lb": 453.592, "stone": 6350.29,
        "ounce": 28.3495, "pound": 453.592
    }
    
    if from_unit not in to_gram or to_unit not in to_gram:
        return None
    
    grams = value * to_gram[from_unit]
    result = grams / to_gram[to_unit]
    return result

def convert_temperature(value, from_unit, to_unit):
    """温度转换"""
    if from_unit == to_unit:
        return value
    
    # 先转换为摄氏度
    if from_unit == "C":
        celsius = value
    elif from_unit == "F":
        celsius = (value - 32) * 5/9
    elif from_unit == "K":
        celsius = value - 273.15
    else:
        return None
    
    # 从摄氏度转换为目标单位
    if to_unit == "C":
        return celsius
    elif to_unit == "F":
        return celsius * 9/5 + 32
    elif to_unit == "K":
        return celsius + 273.15
    else:
        return None

def convert_area(value, from_unit, to_unit):
    """面积转换"""
    # 转换为平方米
    to_sqmeter = {
        "mm2": 1e-6, "cm2": 1e-4, "m2": 1, "km2": 1e6,
        "in2": 0.00064516, "ft2": 0.092903, "yd2": 0.836127, "acre": 4046.86, "mi2": 2.59e6,
        "square mm": 1e-6, "square cm": 1e-4, "square m": 1, "square km": 1e6,
        "square inch": 0.00064516, "square foot": 0.092903, "square yard": 0.836127
    }
    
    if from_unit not in to_sqmeter or to_unit not in to_sqmeter:
        return None
    
    sqmeters = value * to_sqmeter[from_unit]
    result = sqmeters / to_sqmeter[to_unit]
    return result

def convert_volume(value, from_unit, to_unit):
    """体积转换"""
    # 转换为升
    to_liter = {
        "ml": 0.001, "l": 1, "kl": 1000,
        "fl oz": 0.0295735, "cup": 0.236588, "pt": 0.473176, "qt": 0.946353, "gal": 3.78541,
        "milliliter": 0.001, "liter": 1, "kiloliter": 1000,
        "fluid ounce": 0.0295735, "pint": 0.473176, "quart": 0.946353, "gallon": 3.78541
    }
    
    if from_unit not in to_liter or to_unit not in to_liter:
        return None
    
    liters = value * to_liter[from_unit]
    result = liters / to_liter[to_unit]
    return result

def convert_speed(value, from_unit, to_unit):
    """速度转换"""
    # 转换为米/秒
    to_mps = {
        "m/s": 1, "km/h": 0.277778, "ft/s": 0.3048, "mph": 0.44704, "knot": 0.514444,
        "meter per second": 1, "kilometer per hour": 0.277778, "foot per second": 0.3048,
        "mile per hour": 0.44704, "knot": 0.514444
    }
    
    if from_unit not in to_mps or to_unit not in to_mps:
        return None
    
    mps = value * to_mps[from_unit]
    result = mps / to_mps[to_unit]
    return result

def convert_time(value, from_unit, to_unit):
    """时间转换"""
    # 转换为秒
    to_second = {
        "ms": 0.001, "s": 1, "min": 60, "h": 3600, "day": 86400, "week": 604800, "year": 31536000,
        "millisecond": 0.001, "second": 1, "minute": 60, "hour": 3600, "day": 86400,
        "week": 604800, "year": 31536000
    }
    
    if from_unit not in to_second or to_unit not in to_second:
        return None
    
    seconds = value * to_second[from_unit]
    result = seconds / to_second[to_unit]
    return result

def convert_data(value, from_unit, to_unit):
    """数据大小转换"""
    # 转换为字节
    to_byte = {
        "B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4, "PB": 1024**5,
        "byte": 1, "kilobyte": 1024, "megabyte": 1024**2, "gigabyte": 1024**3,
        "terabyte": 1024**4, "petabyte": 1024**5
    }
    
    if from_unit not in to_byte or to_unit not in to_byte:
        return None
    
    bytes_val = value * to_byte[from_unit]
    result = bytes_val / to_byte[to_unit]
    return result

def format_number(num):
    """格式化数字"""
    if num == 0:
        return "0"
    elif abs(num) < 0.001:
        return f"{num:.2e}"
    elif abs(num) < 1:
        return f"{num:.6f}".rstrip('0').rstrip('.')
    elif abs(num) < 1000:
        return f"{num:.3f}".rstrip('0').rstrip('.')
    else:
        return f"{num:,.2f}"

def get_unit_list(category):
    """获取单位列表"""
    units = {
        "length": ["mm", "cm", "m", "km", "in", "ft", "yd", "mi", "inch", "foot", "yard", "mile"],
        "weight": ["mg", "g", "kg", "t", "oz", "lb", "stone", "ounce", "pound"],
        "temperature": ["C", "F", "K", "Celsius", "Fahrenheit", "Kelvin"],
        "area": ["mm2", "cm2", "m2", "km2", "in2", "ft2", "yd2", "acre", "mi2"],
        "volume": ["ml", "l", "kl", "fl oz", "cup", "pt", "qt", "gal"],
        "speed": ["m/s", "km/h", "ft/s", "mph", "knot"],
        "time": ["ms", "s", "min", "h", "day", "week", "year"],
        "data": ["B", "KB", "MB", "GB", "TB", "PB"]
    }
    return units.get(category, [])

def main():
    if len(sys.argv) < 2:
        print("用法: unit-convert <command> [args]")
        print("")
        print("命令:")
        print("  unit-convert <数值> <原单位> <目标单位>  单位转换")
        print("  unit-convert list <类别>                   列出单位")
        print("  unit-convert categories                   列出类别")
        print("  unit-convert help <类别>                   显示帮助")
        print("")
        print("类别:")
        print("  length, weight, temperature, area, volume")
        print("  speed, time, data")
        print("")
        print("示例:")
        print("  unit-convert 100 cm m")
        print("  unit-convert 10 kg lb")
        print("  unit-convert 25 C F")
        print("  unit-convert 1000 B KB")
        print("  unit-convert list length")
        print("  unit-convert help temperature")
        return 1

    command = sys.argv[1]

    if command == "list":
        if len(sys.argv) < 3:
            print("错误: 请提供类别")
            print("使用: unit-convert list <类别>")
            return 1
        
        category = sys.argv[2]
        units = get_unit_list(category)
        
        if not units:
            print(f"错误: 未知类别 '{category}'")
            return 1
        
        print(f"\n📏 {category.upper()} 单位:\n")
        for i, unit in enumerate(units, 1):
            print(f"{i:2}. {unit}")
        print()

    elif command == "categories":
        print("\n📊 支持的类别:\n")
        categories = {
            "length": "长度 (mm, cm, m, km, in, ft, yd, mi)",
            "weight": "重量 (mg, g, kg, t, oz, lb, stone)",
            "temperature": "温度 (C, F, K)",
            "area": "面积 (mm², cm², m², km², in², ft², yd², acre)",
            "volume": "体积 (ml, l, kl, fl oz, cup, pt, qt, gal)",
            "speed": "速度 (m/s, km/h, ft/s, mph, knot)",
            "time": "时间 (ms, s, min, h, day, week, year)",
            "data": "数据 (B, KB, MB, GB, TB, PB)"
        }
        
        for i, (cat, desc) in enumerate(categories.items(), 1):
            print(f"{i}. {cat:<12} - {desc}")
        print()

    elif command == "help":
        if len(sys.argv) < 3:
            print("错误: 请提供类别")
            return 1
        
        category = sys.argv[2]
        
        help_text = {
            "length": "长度单位转换\n示例: unit-convert 100 cm m\n      unit-convert 5 ft cm",
            "weight": "重量单位转换\n示例: unit-convert 10 kg lb\n      unit-convert 1000 g kg",
            "temperature": "温度单位转换\n示例: unit-convert 25 C F\n      unit-convert 98.6 F C\n      unit-convert 300 K C",
            "area": "面积单位转换\n示例: unit-convert 100 m2 ft2\n      unit-convert 1 acre m2",
            "volume": "体积单位转换\n示例: unit-convert 1000 ml l\n      unit-convert 1 gal l",
            "speed": "速度单位转换\n示例: unit-convert 100 km/h mph\n      unit-convert 10 m/s km/h",
            "time": "时间单位转换\n示例: unit-convert 3600 s h\n      unit-convert 7 day h",
            "data": "数据大小转换\n示例: unit-convert 1024 B KB\n      unit-convert 1 GB MB"
        }
        
        if category in help_text:
            print(f"\n{help_text[category]}\n")
        else:
            print(f"错误: 未知类别 '{category}'")
            return 1

    else:
        # 转换命令
        if len(sys.argv) < 4:
            print("错误: 请提供数值、原单位和目标单位")
            print("用法: unit-convert <数值> <原单位> <目标单位>")
            return 1
        
        try:
            value = float(command)
            from_unit = sys.argv[2].lower()
            to_unit = sys.argv[3].lower()
        except ValueError:
            print("错误: 数值必须是数字")
            return 1
        
        # 标准化单位名称
        unit_map = {
            "celsius": "C", "fahrenheit": "F", "kelvin": "K",
            "inch": "in", "inches": "in",
            "foot": "ft", "feet": "ft",
            "yard": "yd", "yards": "yd",
            "mile": "mi", "miles": "mi",
            "ounce": "oz", "ounces": "oz",
            "pound": "lb", "pounds": "lb",
            "square mm": "mm2", "square cm": "cm2", "square m": "m2", "square km": "km2",
            "square inch": "in2", "square inches": "in2",
            "square foot": "ft2", "square feet": "ft2",
            "square yard": "yd2", "square yards": "yd2",
            "fluid ounce": "fl oz", "fluid ounces": "fl fl oz",
            "pint": "pt", "pints": "pt",
            "quart": "qt", "quarts": "qt",
            "gallon": "gal", "gallons": "gal",
            "milliliter": "ml", "milliliters": "ml",
            "liter": "l", "liters": "l",
            "kiloliter": "kl", "kiloliters": "kl",
            "meter per second": "m/s", "meters per second": "m/s",
            "kilometer per hour": "km/h", "kilometers per hour": "km/h",
            "foot per second": "ft/s", "feet per second": "ft/s",
            "mile per hour": "mph", "miles per hour": "mph",
            "byte": "B", "bytes": "B",
            "kilobyte": "KB", "kilobytes": "KB",
            "megabyte": "MB", "megabytes": "MB",
            "gigabyte": "GB", "gigabytes": "GB",
            "terabyte": "TB", "terabytes": "TB",
            "petabyte": "PB", "petabytes": "PB",
            "hour": "h", "hours": "h",
            "minute": "min", "minutes": "min",
            "second": "s", "seconds": "s",
            "millisecond": "ms", "milliseconds": "ms"
        }
        
        from_unit = unit_map.get(from_unit, from_unit)
        to_unit = unit_map.get(to_unit, to_unit)
        
        # 尝试各种转换
        result = None
        category = None
        
        # 长度
        result = convert_length(value, from_unit, to_unit)
        if result is not None:
            category = "长度"
        
        # 重量
        if result is None:
            result = convert_weight(value, from_unit, to_unit)
            if result is not None:
                category = "重量"
        
        # 温度
        if result is None:
            result = convert_temperature(value, from_unit.upper(), to_unit.upper())
            if result is not None:
                category = "温度"
        
        # 面积
        if result is None:
            result = convert_area(value, from_unit, to_unit)
            if result is not None:
                category = "面积"
        
        # 体积
        if result is None:
            result = convert_volume(value, from_unit, to_unit)
            if result is not None:
                category = "体积"
        
        # 速度
        if result is None:
            result = convert_speed(value, from_unit, to_unit)
            if result is not None:
                category = "速度"
        
        # 时间
        if result is None:
            result = convert_time(value, from_unit, to_unit)
            if result is not None:
                category = "时间"
        
        # 数据
        if result is None:
            result = convert_data(value, from_unit, to_unit)
            if result is not None:
                category = "数据"
        
        if result is None:
            print(f"错误: 无法转换 '{from_unit}' 到 '{to_unit}'")
            print("使用 'unit-convert categories' 查看支持的类别")
            return 1
        
        # 显示结果
        print(f"\n🔄 {category} 转换")
        print(f"{format_number(value)} {from_unit} = {format_number(result)} {to_unit}")
        print()

    return 0

if __name__ == "__main__":
    sys.exit(main())

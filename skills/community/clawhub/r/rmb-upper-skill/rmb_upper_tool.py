# tool.py
# -*- coding: utf-8 -*-

NUM_MAP = "零壹贰叁肆伍陆柒捌玖"
UNIT_INT = ["", "拾", "佰", "仟"]
UNIT_SECTION = ["", "万", "亿", "万亿"]
UNIT_DEC = ["角", "分"]


def _four_digit_to_cn(num: int) -> str:
    assert 0 <= num <= 9999
    if num == 0:
        return ""
    result = []
    zero_flag = False
    unit_pos = 0

    while num > 0:
        digit = num % 10
        if digit == 0:
            if not zero_flag and result:
                result.append(NUM_MAP[0])
            zero_flag = True
        else:
            result.append(UNIT_INT[unit_pos])
            result.append(NUM_MAP[digit])
            zero_flag = False
        unit_pos += 1
        num //= 10

    result_str = "".join(reversed(result))
    while result_str.endswith(NUM_MAP[0]):
        result_str = result_str[:-1]

    return result_str


def number_to_rmb_upper(amount):
    amount_str = str(amount).strip()
    negative = False

    if amount_str.startswith("-"):
        negative = True
        amount_str = amount_str[1:].lstrip()

    if not amount_str or amount_str == ".":
        raise ValueError("金额格式不正确")

    value = round(float(amount_str) * 100)
    if value == 0:
        return "负零元整" if negative else "零元整"

    int_part = value // 100
    dec_part = value % 100

    section_index = 0
    int_result_parts = []
    need_zero = False

    while int_part > 0 and section_index < len(UNIT_SECTION):
        section = int_part % 10000
        if section == 0:
            need_zero = True
        else:
            section_str = _four_digit_to_cn(section)
            if need_zero and int_result_parts:
                int_result_parts.append(NUM_MAP[0])
                need_zero = False
            if UNIT_SECTION[section_index]:
                section_str += UNIT_SECTION[section_index]
            int_result_parts.append(section_str)
        section_index += 1
        int_part //= 10000

    int_result = "".join(reversed(int_result_parts)) if int_result_parts else NUM_MAP[0]
    int_result += "元"

    if dec_part == 0:
        dec_result = "整"
    else:
        jiao = dec_part // 10
        fen = dec_part % 10
        dec_list = []

        if jiao > 0:
            dec_list.append(NUM_MAP[jiao] + UNIT_DEC[0])
        if fen > 0:
            if jiao == 0 and int_result != NUM_MAP[0] + "元":
                dec_list.insert(0, NUM_MAP[0])
            dec_list.append(NUM_MAP[fen] + UNIT_DEC[1])

        dec_result = "".join(dec_list)

    prefix = "负" if negative else ""
    return prefix + int_result + dec_result


# ✅ OpenClaw 入口函数（关键）
def rmb_upper_tool(amount: str):
    """
    将数字转换为人民币大写
    """
    try:
        result = number_to_rmb_upper(amount)
        return {
            "success": True,
            "result": f"[TOOL] {result}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
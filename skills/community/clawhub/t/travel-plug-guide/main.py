"""
旅行插头电压查询 - Travel Plug Guide
查询全球200+国家和地区的插头类型、电压标准和频率，推荐转换插头。
"""
import json
import os

PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")

# ========== 插头类型说明 ==========
PLUG_TYPES = {
    "A": {"name": "A型(美标)", "pins": "两脚扁平", "voltage": "100-127V", "countries": "美国/日本/加拿大/台湾", "img_desc": "|| 两脚平行扁平"},
    "B": {"name": "B型(美标接地)", "pins": "两脚扁平+圆脚接地", "voltage": "100-127V", "countries": "美国/加拿大", "img_desc": "|o| 两脚扁平+中间圆脚"},
    "C": {"name": "C型(欧标两脚)", "pins": "两脚圆柱", "voltage": "220-240V", "countries": "欧洲大陆/亚洲/非洲广泛使用", "img_desc": "o o 两脚圆孔"},
    "D": {"name": "D型(印度标)", "pins": "三脚三角排列(粗)", "voltage": "220-240V", "countries": "印度/尼泊尔/斯里兰卡", "img_desc": "大三角三脚"},
    "E": {"name": "E型(法标)", "pins": "两脚圆柱+接地孔", "voltage": "220-240V", "countries": "法国/比利时/波兰", "img_desc": "o o + 上方接地孔"},
    "F": {"name": "F型(德标/舒柯)", "pins": "两脚圆柱+两侧接地卡", "voltage": "220-240V", "countries": "德国/荷兰/西班牙/俄罗斯", "img_desc": "o o + 两侧接地弹片"},
    "G": {"name": "G型(英标)", "pins": "三脚矩形排列", "voltage": "220-240V", "countries": "英国/香港/新加坡/马来西亚", "img_desc": "|_| 三脚矩形方头"},
    "H": {"name": "H型(以色列标)", "pins": "三脚三角排列(Y型)", "voltage": "220-240V", "countries": "以色列/巴勒斯坦", "img_desc": "Y型三脚"},
    "I": {"name": "I型(中标/澳标)", "pins": "三脚斜扁(倒八字)", "voltage": "220-240V", "countries": "中国/澳大利亚/新西兰/阿根廷", "img_desc": "/\\ 倒八字三脚"},
    "J": {"name": "J型(瑞士标)", "pins": "三脚(类似C+接地)", "voltage": "220-240V", "countries": "瑞士/列支敦士登", "img_desc": "o o + 中间接地"},
    "K": {"name": "K型(丹麦标)", "pins": "类似E+F混合", "voltage": "220-240V", "countries": "丹麦/格陵兰", "img_desc": "o o + U型接地"},
    "L": {"name": "L型(意大利标)", "pins": "三脚一字排列", "voltage": "220-240V", "countries": "意大利/智利", "img_desc": "o o o 一字三圆脚"},
    "M": {"name": "M型(南非标)", "pins": "类似D型但更大", "voltage": "220-240V", "countries": "南非/印度(部分)", "img_desc": "大三角三脚(比D更大)"},
    "N": {"name": "N型(巴西标)", "pins": "类似I型但圆柱", "voltage": "127-240V", "countries": "巴西/南非", "img_desc": "圆版I型"},
    "O": {"name": "O型(泰国标)", "pins": "三脚圆柱三角排列", "voltage": "220V", "countries": "泰国(新标准)", "img_desc": "三脚圆柱三角"},
}

# ========== 国家插头数据库 ==========
COUNTRY_DB = {
    "中国": {"plugs": ["A", "C", "I"], "voltage": "220V", "frequency": "50Hz", "note": "国标I型为主，部分酒店有A/C型万能插座"},
    "中国香港": {"plugs": ["G"], "voltage": "220V", "frequency": "50Hz", "note": "英标三脚方头，与内地不同"},
    "中国澳门": {"plugs": ["G", "D", "M"], "voltage": "220V", "frequency": "50Hz", "note": "以英标G型为主"},
    "中国台湾": {"plugs": ["A", "B"], "voltage": "110V", "frequency": "60Hz", "note": "美标A/B型，电压110V需注意"},
    "日本": {"plugs": ["A", "B"], "voltage": "100V", "frequency": "50/60Hz", "note": "东部50Hz(东京)，西部60Hz(大阪)，电压全球最低100V"},
    "韩国": {"plugs": ["C", "F"], "voltage": "220V", "frequency": "60Hz", "note": "欧标C/F型，与中国插头不同"},
    "泰国": {"plugs": ["A", "B", "C", "O"], "voltage": "220V", "frequency": "50Hz", "note": "新旧标准混杂，A/C型都可插入，O型为新增标准"},
    "越南": {"plugs": ["A", "B", "C"], "voltage": "220V", "frequency": "50Hz", "note": "美标和欧标混用，大部分酒店有万能插座"},
    "新加坡": {"plugs": ["G"], "voltage": "230V", "frequency": "50Hz", "note": "英标G型"},
    "马来西亚": {"plugs": ["G"], "voltage": "240V", "frequency": "50Hz", "note": "英标G型为主"},
    "菲律宾": {"plugs": ["A", "B", "C"], "voltage": "220V", "frequency": "60Hz", "note": "美标为主，部分有欧标"},
    "印度尼西亚": {"plugs": ["C", "F"], "voltage": "230V", "frequency": "50Hz", "note": "欧标为主，巴厘岛酒店有万能插座"},
    "印度": {"plugs": ["C", "D", "M"], "voltage": "230V", "frequency": "50Hz", "note": "D型(粗三脚)和M型为主，C型也可插"},
    "柬埔寨": {"plugs": ["A", "B", "C"], "voltage": "230V", "frequency": "50Hz", "note": "美标欧标混用"},
    "缅甸": {"plugs": ["C", "D", "G"], "voltage": "230V", "frequency": "50Hz", "note": "多种标准混用"},
    "老挝": {"plugs": ["A", "B", "C", "E", "F"], "voltage": "230V", "frequency": "50Hz", "note": "标准混乱，建议带万能转换器"},
    "尼泊尔": {"plugs": ["C", "D", "M"], "voltage": "230V", "frequency": "50Hz", "note": "印度标为主"},
    "斯里兰卡": {"plugs": ["D", "G", "M"], "voltage": "230V", "frequency": "50Hz", "note": "英标和印度标混用"},
    "英国": {"plugs": ["G"], "voltage": "230V", "frequency": "50Hz", "note": "英标G型，与内地完全不同"},
    "法国": {"plugs": ["C", "E"], "voltage": "230V", "frequency": "50Hz", "note": "法标E型，C型两脚也可插"},
    "德国": {"plugs": ["C", "F"], "voltage": "230V", "frequency": "50Hz", "note": "德标F型(舒柯)，C型两脚也可插"},
    "意大利": {"plugs": ["C", "F", "L"], "voltage": "230V", "frequency": "50Hz", "note": "意标L型(三脚一字)，C/F型也常见"},
    "西班牙": {"plugs": ["C", "F"], "voltage": "230V", "frequency": "50Hz", "note": "德标F型为主"},
    "葡萄牙": {"plugs": ["C", "F"], "voltage": "230V", "frequency": "50Hz", "note": "德标为主"},
    "荷兰": {"plugs": ["C", "F"], "voltage": "230V", "frequency": "50Hz", "note": "德标为主"},
    "比利时": {"plugs": ["C", "E"], "voltage": "230V", "frequency": "50Hz", "note": "法标为主"},
    "瑞士": {"plugs": ["C", "J"], "voltage": "230V", "frequency": "50Hz", "note": "瑞士标J型，与邻国不同"},
    "奥地利": {"plugs": ["C", "F"], "voltage": "230V", "frequency": "50Hz", "note": "德标为主"},
    "希腊": {"plugs": ["C", "F"], "voltage": "230V", "frequency": "50Hz", "note": "德标为主"},
    "爱尔兰": {"plugs": ["G"], "voltage": "230V", "frequency": "50Hz", "note": "英标"},
    "瑞典": {"plugs": ["C", "F"], "voltage": "230V", "frequency": "50Hz", "note": "德标为主"},
    "挪威": {"plugs": ["C", "F"], "voltage": "230V", "frequency": "50Hz", "note": "德标为主"},
    "丹麦": {"plugs": ["C", "E", "F", "K"], "voltage": "230V", "frequency": "50Hz", "note": "丹麦标K型，C/E/F也可用"},
    "芬兰": {"plugs": ["C", "F"], "voltage": "230V", "frequency": "50Hz", "note": "德标为主"},
    "波兰": {"plugs": ["C", "E"], "voltage": "230V", "frequency": "50Hz", "note": "法标为主"},
    "捷克": {"plugs": ["C", "E"], "voltage": "230V", "frequency": "50Hz", "note": "法标为主"},
    "匈牙利": {"plugs": ["C", "F"], "voltage": "230V", "frequency": "50Hz", "note": "德标为主"},
    "克罗地亚": {"plugs": ["C", "F"], "voltage": "230V", "frequency": "50Hz", "note": "德标为主"},
    "俄罗斯": {"plugs": ["C", "F"], "voltage": "220V", "frequency": "50Hz", "note": "德标为主"},
    "乌克兰": {"plugs": ["C", "F"], "voltage": "230V", "frequency": "50Hz", "note": "德标为主"},
    "土耳其": {"plugs": ["C", "F"], "voltage": "230V", "frequency": "50Hz", "note": "德标为主"},
    "美国": {"plugs": ["A", "B"], "voltage": "120V", "frequency": "60Hz", "note": "美标A/B型，电压120V需注意"},
    "加拿大": {"plugs": ["A", "B"], "voltage": "120V", "frequency": "60Hz", "note": "美标，与美国相同"},
    "墨西哥": {"plugs": ["A", "B"], "voltage": "127V", "frequency": "60Hz", "note": "美标为主，部分老建筑电压不稳"},
    "巴西": {"plugs": ["C", "N"], "voltage": "127/240V", "frequency": "60Hz", "note": "⚠️巴西电压因城市而异！圣保罗127V/里约127V/巴西利亚240V/萨尔瓦多240V"},
    "阿根廷": {"plugs": ["C", "I"], "voltage": "220V", "frequency": "50Hz", "note": "I型(与中标类似但接地不同)，C型也可插"},
    "智利": {"plugs": ["C", "L"], "voltage": "220V", "frequency": "50Hz", "note": "意标L型为主"},
    "哥伦比亚": {"plugs": ["A", "B"], "voltage": "110V", "frequency": "60Hz", "note": "美标为主"},
    "秘鲁": {"plugs": ["A", "B", "C"], "voltage": "220V", "frequency": "60Hz", "note": "美标欧标混用"},
    "厄瓜多尔": {"plugs": ["A", "B"], "voltage": "120V", "frequency": "60Hz", "note": "美标为主"},
    "澳大利亚": {"plugs": ["I"], "voltage": "230V", "frequency": "50Hz", "note": "澳标I型(与中标形状相同)"},
    "新西兰": {"plugs": ["I"], "voltage": "230V", "frequency": "50Hz", "note": "澳标I型"},
    "斐济": {"plugs": ["I"], "voltage": "240V", "frequency": "50Hz", "note": "澳标I型"},
    "阿联酋": {"plugs": ["C", "D", "G"], "voltage": "230V", "frequency": "50Hz", "note": "英标G型为主，迪拜酒店有万能插座"},
    "沙特阿拉伯": {"plugs": ["A", "B", "G"], "voltage": "230V", "frequency": "60Hz", "note": "多种标准混用，酒店以G型为主"},
    "卡塔尔": {"plugs": ["D", "G"], "voltage": "240V", "frequency": "50Hz", "note": "英标为主"},
    "以色列": {"plugs": ["C", "H"], "voltage": "230V", "frequency": "50Hz", "note": "以色列标H型"},
    "埃及": {"plugs": ["C", "F"], "voltage": "220V", "frequency": "50Hz", "note": "德标为主，酒店可能有万能插座"},
    "摩洛哥": {"plugs": ["C", "E"], "voltage": "220V", "frequency": "50Hz", "note": "法标为主"},
    "南非": {"plugs": ["C", "D", "M", "N"], "voltage": "230V", "frequency": "50Hz", "note": "M型(大三脚)为主，新建筑N型增多"},
    "肯尼亚": {"plugs": ["G"], "voltage": "240V", "frequency": "50Hz", "note": "英标为主"},
    "坦桑尼亚": {"plugs": ["D", "G"], "voltage": "230V", "frequency": "50Hz", "note": "英标和印度标混用"},
    "尼日利亚": {"plugs": ["D", "G"], "voltage": "230V", "frequency": "50Hz", "note": "英标和印度标混用"},
    "冰岛": {"plugs": ["C", "F"], "voltage": "230V", "frequency": "50Hz", "note": "德标为主"},
    "格鲁吉亚": {"plugs": ["C", "F"], "voltage": "220V", "frequency": "50Hz", "note": "德标为主"},
    "亚美尼亚": {"plugs": ["C", "F"], "voltage": "230V", "frequency": "50Hz", "note": "德标为主"},
    "蒙古": {"plugs": ["C", "E", "F"], "voltage": "230V", "frequency": "50Hz", "note": "欧标为主"},
    "哈萨克斯坦": {"plugs": ["C", "F"], "voltage": "220V", "frequency": "50Hz", "note": "德标为主"},
    "乌兹别克斯坦": {"plugs": ["C", "F"], "voltage": "220V", "frequency": "50Hz", "note": "德标为主"},
    "巴厘岛": {"plugs": ["C", "F"], "voltage": "230V", "frequency": "50Hz", "note": "同印度尼西亚，欧标为主"},
    "普吉岛": {"plugs": ["A", "B", "C", "O"], "voltage": "220V", "frequency": "50Hz", "note": "同泰国，A/C型都可用"},
    "冲绳": {"plugs": ["A", "B"], "voltage": "100V", "frequency": "60Hz", "note": "同日本，美标A型"},
    "夏威夷": {"plugs": ["A", "B"], "voltage": "120V", "frequency": "60Hz", "note": "同美国，美标A/B型"},
    "马尔代夫": {"plugs": ["A", "C", "D", "G", "J", "K", "L"], "voltage": "230V", "frequency": "50Hz", "note": "酒店多备万能插座，G型最常见"},
    "塞舌尔": {"plugs": ["G"], "voltage": "240V", "frequency": "50Hz", "note": "英标为主"},
    "毛里求斯": {"plugs": ["C", "G"], "voltage": "230V", "frequency": "50Hz", "note": "英标和欧标混用"},
}

# ========== 常见电器电压兼容性 ==========
DEVICE_DB = {
    "iPhone充电器": {"input": "100-240V 50/60Hz", "wide_voltage": True, "note": "苹果原装/认证充电器都是宽电压，全球通用"},
    "iPad充电器": {"input": "100-240V 50/60Hz", "wide_voltage": True, "note": "宽电压，全球通用"},
    "安卓手机充电器": {"input": "100-240V 50/60Hz", "wide_voltage": True, "note": "品牌原装充电器多为宽电压，杂牌需确认标签"},
    "MacBook充电器": {"input": "100-240V 50/60Hz", "wide_voltage": True, "note": "苹果笔记本充电器全球通用"},
    "笔记本充电器": {"input": "100-240V 50/60Hz", "wide_voltage": True, "note": "绝大多数笔记本电源适配器是宽电压"},
    "相机充电器": {"input": "100-240V 50/60Hz", "wide_voltage": True, "note": "佳能/尼康/索尼原装充电器宽电压"},
    "充电宝": {"input": "5V USB", "wide_voltage": True, "note": "通过USB充电，不受目的地电压影响"},
    "戴森吹风机": {"input": "220-240V 50Hz", "wide_voltage": False, "note": "⚠️单电压！带到110V国家(美/日/台)无法使用或功率极低"},
    "普通吹风机": {"input": "220V 50Hz", "wide_voltage": False, "note": "⚠️单电压！带到110V国家需变压器，否则不工作或烧毁"},
    "电热水壶": {"input": "220V 50Hz", "wide_voltage": False, "note": "⚠️单电压大功率电器，不建议带出境使用"},
    "卷发棒/直板夹": {"input": "220V 50Hz", "wide_voltage": False, "note": "⚠️多数单电压，部分高端款宽电压(看标签)"},
    "电动牙刷": {"input": "100-240V 50/60Hz", "wide_voltage": True, "note": "飞利浦/欧乐B原装充电器宽电压"},
    "剃须刀": {"input": "100-240V 50/60Hz", "wide_voltage": True, "note": "品牌剃须刀多为宽电压"},
    "电饭煲": {"input": "220V 50Hz", "wide_voltage": False, "note": "⚠️单电压大功率，不建议带出境"},
    "Switch充电器": {"input": "100-240V 50/60Hz", "wide_voltage": True, "note": "宽电压，全球通用"},
    "Steam Deck充电器": {"input": "100-240V 50/60Hz", "wide_voltage": True, "note": "宽电压，全球通用"},
}


def plug_query(destination: str) -> str:
    """查询目的地插头类型和电压"""
    dest = destination.strip()
    result = None

    for key, val in COUNTRY_DB.items():
        if dest in key or key in dest:
            result = val
            break

    if not result:
        return json.dumps({
            "found": False,
            "message": f"暂未收录'{dest}'的插头信息。目前收录{len(COUNTRY_DB)}个国家和地区。请尝试输入国家名。"
        }, ensure_ascii=False)

    plug_details = []
    for plug_type in result["plugs"]:
        info = PLUG_TYPES.get(plug_type, {})
        plug_details.append({
            "type": plug_type,
            "name": info.get("name", f"{plug_type}型"),
            "pins": info.get("pins", ""),
            "img_desc": info.get("img_desc", ""),
        })

    output = {
        "found": True,
        "destination": dest,
        "plugs": plug_details,
        "plug_types": result["plugs"],
        "voltage": result["voltage"],
        "frequency": result["frequency"],
        "note": result.get("note", ""),
        "china_comparison": _compare_with_china(result),
    }

    return json.dumps(output, ensure_ascii=False)


def _compare_with_china(data):
    """Compare with China's plug standard"""
    china_plugs = {"A", "C", "I"}
    dest_plugs = set(data["plugs"])

    common = china_plugs & dest_plugs
    china_only = china_plugs - dest_plugs
    dest_only = dest_plugs - china_plugs

    if common:
        return f"中国插头可直接使用！目的地有{','.join(common)}型插座，中国A/C/I型插头可以直接插入"
    else:
        return f"需要转换插头！目的地使用{','.join(dest_plugs)}型，中国插头无法直接插入"


def adapter_guide(from_country: str = "中国", to_country: str = "", devices: str = "") -> str:
    """推荐转换插头"""
    from_data = COUNTRY_DB.get(from_country, COUNTRY_DB.get("中国"))
    to_data = None

    for key, val in COUNTRY_DB.items():
        if to_country in key or key in to_country:
            to_data = val
            break

    if not to_data:
        return json.dumps({
            "found": False,
            "message": f"未找到'{to_country}'的信息。请尝试输入国家名。"
        }, ensure_ascii=False)

    from_plugs = set(from_data["plugs"])
    to_plugs = set(to_data["plugs"])
    need_adapter = not bool(from_plugs & to_plugs)

    output = {
        "found": True,
        "from": from_country,
        "from_plugs": list(from_plugs),
        "to": to_country,
        "to_plugs": list(to_plugs),
        "need_adapter": need_adapter,
        "need_transformer": _check_transformer(from_data, to_data),
    }

    if need_adapter:
        # Recommend adapter
        recommendations = []
        if "G" in to_plugs:
            recommendations.append({"type": "英标转换器", "price": "15-30元", "covers": "英国/香港/新加坡/马来西亚/阿联酋"})
        if "F" in to_plugs or "E" in to_plugs:
            recommendations.append({"type": "欧标转换器(德标)", "price": "15-25元", "covers": "德国/法国/西班牙/意大利/韩国/俄罗斯等"})
        if "A" in to_plugs and "I" in from_plugs:
            recommendations.append({"type": "美标转换器", "price": "10-20元", "covers": "美国/日本/加拿大/台湾"})
        if "I" in to_plugs and "A" in from_plugs:
            recommendations.append({"type": "澳标转换器", "price": "15-25元", "covers": "澳大利亚/新西兰/中国"})

        if not recommendations:
            recommendations.append({"type": "万能转换插头", "price": "30-60元", "covers": "全球150+国家，覆盖所有标准"})

        # Always suggest universal as backup
        if not any(r["type"] == "万能转换插头" for r in recommendations):
            recommendations.append({"type": "万能转换插头(推荐)", "price": "30-60元", "covers": "全球150+国家，一劳永逸"})

        output["recommendations"] = recommendations
    else:
        output["message"] = f"从{from_country}到{to_country}，插头可以直接使用，不需要转换器！"

    # Device compatibility
    if devices:
        dev_map = {
            "phone": "iPhone充电器", "手机": "iPhone充电器",
            "laptop": "笔记本充电器", "笔记本": "笔记本充电器",
            "camera": "相机充电器", "相机": "相机充电器",
            "hair_dryer": "普通吹风机", "吹风机": "普通吹风机",
            "electric_kettle": "电热水壶", "电热水壶": "电热水壶",
        }
        mapped_device = dev_map.get(devices, devices)
        device_info = DEVICE_DB.get(mapped_device)
        if device_info:
            output["device_check"] = {
                "device": mapped_device,
                "input": device_info["input"],
                "wide_voltage": device_info["wide_voltage"],
                "safe": device_info["wide_voltage"] or "220V" in to_data["voltage"] or "230V" in to_data["voltage"] or "240V" in to_data["voltage"],
                "note": device_info["note"],
            }

    return json.dumps(output, ensure_ascii=False)


def _check_transformer(from_data, to_data):
    """Check if transformer is needed"""
    from_v = from_data.get("voltage", "220V")
    to_v = to_data.get("voltage", "220V")

    from_low = "110" in from_v or "120" in from_v or "100" in from_v or "127" in from_v
    to_low = "110" in to_v or "120" in to_v or "100" in to_v or "127" in to_v

    if from_low and not to_low:
        return "中国220V电器带到110V国家：宽电压设备(手机/笔记本)只需转换插头，单电压设备(吹风机/电水壶)需变压器"
    elif not from_low and to_low:
        return "110V国家电器带回国：宽电压设备可用，单电压设备需变压器"
    else:
        return "电压相同或设备为宽电压，无需变压器"


def voltage_check(device_name: str, destination: str) -> str:
    """检查电器在目的地电压下是否安全"""
    dest = destination.strip()
    dest_data = None

    for key, val in COUNTRY_DB.items():
        if dest in key or key in dest:
            dest_data = val
            break

    if not dest_data:
        return json.dumps({
            "found": False,
            "message": f"未找到'{dest}'的信息。"
        }, ensure_ascii=False)

    # Find device
    device_info = None
    for key, val in DEVICE_DB.items():
        if device_name in key or key in device_name:
            device_info = val
            break

    if not device_info:
        # Common pattern matching
        if any(kw in device_name for kw in ["手机", "phone", "iPhone", "安卓", "充电器"]):
            device_info = DEVICE_DB["iPhone充电器"]
        elif any(kw in device_name for kw in ["笔记本", "laptop", "MacBook", "电脑"]):
            device_info = DEVICE_DB["笔记本充电器"]
        elif any(kw in device_name for kw in ["相机", "camera", "单反", "微单"]):
            device_info = DEVICE_DB["相机充电器"]
        elif any(kw in device_name for kw in ["吹风", "戴森", "dyson"]):
            device_info = DEVICE_DB["普通吹风机"]
            if "戴森" in device_name or "dyson" in device_name.lower():
                device_info = DEVICE_DB["戴森吹风机"]
        elif any(kw in device_name for kw in ["水壶", "kettle"]):
            device_info = DEVICE_DB["电热水壶"]
        elif any(kw in device_name for kw in ["牙刷", "牙"]):
            device_info = DEVICE_DB["电动牙刷"]

    if not device_info:
        return json.dumps({
            "found": False,
            "message": f"未找到'{device_name}'的信息。请查看电器标签上的输入电压范围(如100-240V)。如果范围包含目的地电压{dest_data['voltage']}，则可安全使用。",
            "dest_voltage": dest_data["voltage"],
            "tip": "如果标签标注'100-240V'则为宽电压，全球通用；如果只标注'220V'则为单电压，带到110V国家需变压器"
        }, ensure_ascii=False)

    dest_voltage = dest_data["voltage"]
    is_low_voltage = "110" in dest_voltage or "120" in dest_voltage or "100" in dest_voltage or "127" in dest_voltage

    safe = device_info["wide_voltage"] or (not is_low_voltage)

    output = {
        "found": True,
        "device": device_name,
        "device_input": device_info["input"],
        "wide_voltage": device_info["wide_voltage"],
        "destination": dest,
        "dest_voltage": dest_voltage,
        "safe": safe,
        "need_adapter": not bool(set(dest_data["plugs"]) & {"A", "C", "I"}),
        "need_transformer": not device_info["wide_voltage"] and is_low_voltage,
        "note": device_info["note"],
        "action": _get_action(device_info, dest_data, is_low_voltage),
    }

    return json.dumps(output, ensure_ascii=False)


def _get_action(device_info, dest_data, is_low_voltage):
    """Get recommended action"""
    if device_info["wide_voltage"]:
        if set(dest_data["plugs"]) & {"A", "C", "I"}:
            return "直接使用，无需任何转换设备"
        else:
            return "需要转换插头，但不需要变压器（设备支持宽电压）"
    else:
        if is_low_voltage:
            return "⚠️需要变压器！该设备不支持110V电压，强行使用可能烧毁设备。建议在当地购买同类型电器。"
        else:
            if set(dest_data["plugs"]) & {"A", "C", "I"}:
                return "电压兼容，插头可直接使用"
            else:
                return "需要转换插头，电压兼容"


# ========== Tool Registry ==========
TOOLS = {
    "plug_query": {"fn": plug_query, "desc": "查询目的地插头电压信息"},
    "adapter_guide": {"fn": adapter_guide, "desc": "转换插头推荐"},
    "voltage_check": {"fn": voltage_check, "desc": "电器电压安全检查"},
}


def run(tool_name: str, **kwargs):
    """Execute a tool by name."""
    tool = TOOLS.get(tool_name)
    if not tool:
        return json.dumps({"error": f"Unknown tool: {tool_name}"}, ensure_ascii=False)
    try:
        return tool["fn"](**kwargs)
    except TypeError as e:
        return json.dumps({"error": f"参数错误: {str(e)}"}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"执行错误: {str(e)}"}, ensure_ascii=False)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <tool_name> [args...]")
        sys.exit(1)

    tool = sys.argv[1]
    args = {}
    i = 2
    while i < len(sys.argv) - 1:
        key = sys.argv[i].lstrip("-")
        args[key] = sys.argv[i + 1]
        i += 2

    print(run(tool, **args))

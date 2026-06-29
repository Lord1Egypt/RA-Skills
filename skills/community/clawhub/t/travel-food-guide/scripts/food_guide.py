import os
#!/usr/bin/env python3
"""旅行美食助手 - Travel Food Guide"""

import json
import sys
import urllib.request
import urllib.parse
import urllib.error

# 高德地图SCF代理
GAODE_PROXY = "https://1439498936-bl10af74fl.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")

# 餐饮相关POI类型码
FOOD_TYPE_CODES = "050000|050100|050200|050300|050400|050500|050600|050700|050800|050900"

# 菜系关键词映射
CUISINE_KEYWORDS = {
    "川菜": "川菜", "火锅": "火锅", "粤菜": "粤菜", "湘菜": "湘菜",
    "鲁菜": "鲁菜", "苏菜": "苏菜", "浙菜": "浙菜", "闽菜": "闽菜",
    "徽菜": "徽菜", "日料": "日料 日式料理", "韩餐": "韩餐 韩式料理",
    "西餐": "西餐 牛排", "东南亚": "东南亚菜 泰式", "烧烤": "烧烤",
    "面食": "面馆 面食", "小吃": "小吃 快餐", "海鲜": "海鲜",
    "素食": "素食 素菜", "清真": "清真", "咖啡": "咖啡 咖啡厅",
    "甜品": "甜品 甜点", "早餐": "早餐 早茶", "夜宵": "夜宵 大排档",
    "本帮菜": "本帮菜", "东北菜": "东北菜", "西北菜": "西北菜",
    "云南菜": "云南菜", "贵州菜": "贵州菜", "广西菜": "广西菜",
}

# ====== 城市特色美食知识库 ======
LOCAL_SPECIALTIES = {
    "北京": {
        "必吃": ["北京烤鸭", "炸酱面", "卤煮火烧", "豆汁儿配焦圈", "涮羊肉", "爆肚", "驴打滚", "艾窝窝"],
        "美食街区": ["簋街(深夜美食)", "南锣鼓巷(小吃)", "牛街(清真美食)", "前门大街(老字号)"],
        "早餐": ["豆汁儿焦圈", "炒肝", "包子铺", "豆腐脑"],
        "夜宵": ["簋街麻辣小龙虾", "烤串", "爆肚"],
        "伴手礼": ["稻香村糕点", "六必居酱菜", "果脯"],
        "就餐贴士": "老字号通常排队较长，建议错峰；烤鸭推荐全聚德、四季民福、大董"
    },
    "上海": {
        "必吃": ["小笼包", "生煎馒头", "红烧肉", "蟹粉豆腐", "白斩鸡", "葱油拌面", "排骨年糕", "八宝饭"],
        "美食街区": ["城隍庙(小吃)", "云南南路美食街", "寿宁路(小龙虾)", "进贤路(本帮小馆)"],
        "早餐": ["生煎", "小笼", "葱油饼", "豆浆油条"],
        "夜宵": ["寿宁路小龙虾", "夜市大排档"],
        "伴手礼": ["蝴蝶酥(国际饭店)", "鲜肉月饼", "梨膏糖"],
        "就餐贴士": "本帮菜偏甜，点菜注意；小笼包推荐佳家、麟笼坊；生煎推荐小杨、大壶春"
    },
    "成都": {
        "必吃": ["火锅", "串串香", "担担面", "麻婆豆腐", "夫妻肺片", "龙抄手", "钟水饺", "甜水面"],
        "美食街区": ["锦里(小吃)", "宽窄巷子(游客)", "建设路(本地人)", "玉林路(小酒馆美食)"],
        "早餐": ["红油抄手", "肥肠粉", "豆浆配油条", "军屯锅盔"],
        "夜宵": ["串串香", "烤鱼", "冷淡杯", "夜啤酒"],
        "伴手礼": ["郫县豆瓣酱", "张飞牛肉", "蜀绣(非食品)"],
        "就餐贴士": "微辣是底线，不能吃辣提前说；火锅推荐蜀大侠、小龙坎；苍蝇馆子往往更地道"
    },
    "重庆": {
        "必吃": ["重庆火锅", "小面", "酸辣粉", "毛血旺", "辣子鸡", "烤鱼", "抄手", "山城小汤圆"],
        "美食街区": ["解放碑八一路好吃街", "洪崖洞(景观+小吃)", "磁器口(古镇小吃)", "南滨路(江景餐饮)"],
        "早餐": ["重庆小面", "酸辣粉", "糯米团"],
        "夜宵": ["烤鱼", "串串", "大排档"],
        "伴手礼": ["火锅底料", "陈麻花", "合川桃片"],
        "就餐贴士": "重庆火锅默认重油重辣，鸳鸯锅是妥协；小面推荐花市、胖妹"
    },
    "广州": {
        "必吃": ["早茶(虾饺/烧卖/肠粉)", "煲仔饭", "白切鸡", "烧鹅", "云吞面", "双皮奶", "牛杂", "艇仔粥"],
        "美食街区": ["上下九步行街", "北京路", "西关老区", "珠江新城(高端)"],
        "早餐": ["早茶必体验", "肠粉", "及第粥", "叉烧包"],
        "夜宵": ["砂锅粥", "炒河粉", "糖水"],
        "伴手礼": ["鸡仔饼", "老婆饼", "广式腊味"],
        "就餐贴士": "早茶建议8点前到避开等位；推荐陶陶居、点都德、莲香楼"
    },
    "西安": {
        "必吃": ["肉夹馍", "羊肉泡馍", "凉皮", "biangbiang面", "胡辣汤", "甑糕", "葫芦头", "水盆羊肉"],
        "美食街区": ["回民街(经典)", "永兴坊(陕西非遗)", "洒金桥(本地人)", "大皮院(清真)"],
        "早餐": ["胡辣汤", "肉丸胡辣汤", "油茶麻花"],
        "夜宵": ["烤肉", "炒米", "酸梅汤"],
        "伴手礼": ["德福巷糕点", "陕北红枣", "柿子饼"],
        "就餐贴士": "回民街适合逛，洒金桥更地道；泡馍推荐老孙家、同盛祥"
    },
    "杭州": {
        "必吃": ["西湖醋鱼", "龙井虾仁", "东坡肉", "叫化鸡", "片儿川", "知味小笼", "葱包桧", "定胜糕"],
        "美食街区": ["河坊街(小吃)", "胜利河美食街", "大兜路(运河边)", "南宋御街"],
        "早餐": ["片儿川", "葱包桧", "小笼包"],
        "夜宵": ["小龙虾", "烤串"],
        "伴手礼": ["西湖龙井", "知味观糕点", "桂花糕"],
        "就餐贴士": "西湖景区内餐饮偏贵，建议去市区；楼外楼经典但游客多"
    },
    "厦门": {
        "必吃": ["沙茶面", "海蛎煎", "土笋冻", "花生汤", "烧肉粽", "姜母鸭", "面线糊", "同安封肉"],
        "美食街区": ["中山路(老字号)", "曾厝垵(小吃)", "八市(海鲜)", "沙坡尾(文创+咖啡)"],
        "早餐": ["面线糊", "花生汤", "沙茶面"],
        "夜宵": ["海鲜大排档", "烧烤"],
        "伴手礼": ["南普陀素饼", "日光岩馅饼", "肉松"],
        "就餐贴士": "八市买海鲜加工最划算；沙茶面推荐乌糖、月华"
    },
    "长沙": {
        "必吃": ["臭豆腐", "糖油粑粑", "口味虾", "剁椒鱼头", "长沙米粉", "茶颜悦色", "湘菜小炒", "刮凉粉"],
        "美食街区": ["坡子街(火宫殿)", "太平街(小吃)", "文和友(网红)", "四方坪(夜宵)"],
        "早餐": ["长沙米粉", "糖油粑粑", "葱油饼"],
        "夜宵": ["口味虾", "臭豆腐", "烤串"],
        "伴手礼": ["湘茶", "酱板鸭", "腊肉"],
        "就餐贴士": "长沙夜生活丰富，宵夜是一大特色；茶颜悦色几乎每条街都有"
    },
    "南京": {
        "必吃": ["盐水鸭", "鸭血粉丝汤", "小笼包", "牛肉锅贴", "赤豆元宵", "糕团小点", "活珠子", "皮肚面"],
        "美食街区": ["夫子庙(秦淮小吃)", "老门东(文艺+小吃)", "明瓦廊(白领)", "狮子桥(传统)"],
        "早餐": ["鸭血粉丝汤", "小笼包", "蒸饭"],
        "夜宵": ["烧烤", "龙虾"],
        "伴手礼": ["盐水鸭", "雨花茶", "云锦(非食品)"],
        "就餐贴士": "盐水鸭推荐韩复兴；鸭血粉丝汤推荐回味、鸭得堡"
    },
    "武汉": {
        "必吃": ["热干面", "豆皮", "武昌鱼", "鸭脖", "排骨藕汤", "面窝", "糊汤粉", "烧梅"],
        "美食街区": ["户部巷(经典小吃)", "吉庆街(夜市)", "万松园(本地人)", "粮道街(早餐)"],
        "早餐": ["热干面", "豆皮", "面窝", "糊汤粉——武汉人叫'过早'"],
        "夜宵": ["鸭脖", "烧烤", "小龙虾"],
        "伴手礼": ["周黑鸭", "热干面速食装", "黄鹤楼香烟"],
        "就餐贴士": "武汉人吃早餐叫'过早'，种类全国最丰富；热干面推荐蔡林记、赵师傅"
    },
    "大理": {
        "必吃": ["过桥米线", "白族三道茶", "乳扇", "饵丝", "鲜花饼", "酸辣鱼", "烤乳扇", "凉鸡米线"],
        "美食街区": ["大理古城人民路", "复兴路", "才村(环海餐厅)"],
        "早餐": ["饵丝", "米线", "破酥粑粑"],
        "夜宵": ["烤乳扇", "烤鱼"],
        "伴手礼": ["鲜花饼", "普洱茶", "乳扇(需冷链)"],
        "就餐贴士": "古城餐饮偏游客，环海路上的餐厅风景更好；乳扇是白族特色必尝"
    },
    "三亚": {
        "必吃": ["海鲜(清蒸/蒜蓉)", "椰子鸡", "文昌鸡", "加积鸭", "东山羊", "清补凉", "抱罗粉", "椰子饭"],
        "美食街区": ["第一市场(海鲜加工)", "火车头万人海鲜广场", "解放路(本地)", "海棠湾(高端酒店餐厅)"],
        "早餐": ["抱罗粉", "海南粉", "椰子饭"],
        "夜宵": ["清补凉", "海鲜大排档"],
        "伴手礼": ["椰子糖", "黄灯笼辣椒酱", "胡椒粉"],
        "就餐贴士": "海鲜加工选第一市场买+加工最划算；椰子鸡推荐嗲嗲的椰子鸡"
    },
    "哈尔滨": {
        "必吃": ["锅包肉", "红肠", "马迭尔冰棍", "杀猪菜", "炖菜", "列巴", "格瓦斯", "地三鲜"],
        "美食街区": ["中央大街(经典)", "老道外(老字号)", "师大夜市(学生)"],
        "早餐": ["大列巴配格瓦斯", "烧饼豆腐脑", "包子"],
        "夜宵": ["烧烤(东北特色)", "熏酱"],
        "伴手礼": ["秋林红肠", "大列巴", "马迭尔冰棍"],
        "就餐贴士": "东北菜量大，点菜注意分量；锅包肉推荐老厨家、厚德居"
    },
    "拉萨": {
        "必吃": ["酥油茶", "糌粑", "牦牛肉", "藏面", "甜茶", "酸奶", "青稞酒", "风干肉"],
        "美食街区": ["八廓街(传统)", "北京东路(综合)", "太阳岛(川菜多)"],
        "早餐": ["甜茶+藏面", "糌粑"],
        "夜宵": ["牦牛肉串", "青稞酒馆"],
        "伴手礼": ["牦牛肉干", "青稞酒", "藏红花"],
        "就餐贴士": "初到高原饮食宜清淡，少喝酒；甜茶馆推荐光明港琼；牦牛肉推荐玛吉阿米"
    },
    "丽江": {
        "必吃": ["腊排骨火锅", "鸡豆凉粉", "纳西烤鱼", "丽江粑粑", "水性杨花(菜)", "米灌肠", "酥油茶", "三文鱼(虹鳟)"],
        "美食街区": ["大研古城(游客)", "象山市场(腊排骨)", "花马街(综合)"],
        "早餐": ["鸡豆凉粉", "丽江粑粑", "米线"],
        "夜宵": ["烤串", "酒吧小食"],
        "伴手礼": ["鲜花饼", "普洱茶", "牦牛肉干"],
        "就餐贴士": "古城内餐饮偏贵，象山市场的腊排骨更地道；腊排骨推荐钰洁"
    },
    "青岛": {
        "必吃": ["海鲜(啤酒配蛤蜊)", "鲅鱼饺子", "海鲜水饺", "烤鱿鱼", "辣炒蛤蜊", "海菜凉粉", "青岛啤酒", "锅贴"],
        "美食街区": ["劈柴院(经典小吃)", "台东夜市", "云霄路美食街", "营口路(啤酒屋)"],
        "早餐": ["甜沫", "油条", "馅饼"],
        "夜宵": ["啤酒屋(塑料袋装啤酒)", "海鲜烧烤"],
        "伴手礼": ["青岛啤酒", "鱼片干", "海米"],
        "就餐贴士": "啤酒配蛤蜊是青岛标配；营口路啤酒屋最有本地氛围"
    },
    "苏州": {
        "必吃": ["松鼠桂鱼", "响油鳝糊", "太湖三白", "苏式面", "生煎", "糕团", "鸡头米", "碧螺虾仁"],
        "美食街区": ["观前街(老字号)", "平江路(文艺+小吃)", "山塘街(传统)", "十全街(网红)"],
        "早餐": ["苏式面(头汤面)", "生煎", "糕团"],
        "夜宵": ["小吃", "糖粥"],
        "伴手礼": ["采芝斋糖果", "黄天源糕团", "碧螺春茶"],
        "就餐贴士": "苏式面讲究头汤(早6-7点)；松鼠桂鱼推荐松鹤楼；糕团推荐黄天源"
    },
    "天津": {
        "必吃": ["狗不理包子", "煎饼果子", "麻花", "耳朵眼炸糕", "锅巴菜", "炸酱面(天津版)", "贴饽饽熬鱼", "八大碗"],
        "美食街区": ["南市食品街(综合)", "古文化街(小吃)", "辽宁路(本地)", "五大道(西餐)"],
        "早餐": ["煎饼果子(必体验)", "锅巴菜", "豆浆果子"],
        "夜宵": ["烧烤", "砂锅"],
        "伴手礼": ["十八街麻花", "果仁张", "泥人张(非食品)"],
        "就餐贴士": "正宗煎饼果子是绿豆面+果子/果篦儿，不加火腿生菜；推荐陈秀云、二嫂子"
    },
    "敦煌": {
        "必吃": ["驴肉黄面", "杏皮水", "羊肉粉汤", "酿皮子", "泡儿油糕", "手工臊子面", "烤全羊", "胡杨焖饼"],
        "美食街区": ["沙洲夜市(必去)", "阳关东路", "鸣沙山下(农家乐)"],
        "早餐": ["羊肉粉汤", "臊子面", "酿皮子"],
        "夜宵": ["沙洲夜市(烤肉+杏皮水)"],
        "伴手礼": ["杏干", "李广杏脯", "锁阳"],
        "就餐贴士": "沙洲夜市是敦煌灵魂，烤肉+杏皮水是标配；驴肉黄面推荐达记"
    },
}


def gaode_request(api_type, params):
    """调用高德SCF代理"""
    try:
        payload = {
            "type": api_type,
            "params": params
        }
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            GAODE_PROXY,
            data=data,
            headers={
                "Content-Type": "application/json",
                "X-Proxy-Token": PROXY_TOKEN
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            # SCF代理返回 {"code":0,"data":{高德原始响应}}
            if isinstance(result, dict) and "data" in result and "code" in result:
                return result["data"]
            return result
    except urllib.error.HTTPError as e:
        err = ""
        try:
            err = e.read().decode("utf-8")[:300]
        except Exception:
            pass
        return {"error": f"HTTP {e.code}: {err}"}
    except Exception as e:
        return {"error": str(e)}


def geocode_location(location_text):
    """将地点名转为经纬度"""
    result = gaode_request("geocode", {"address": location_text})
    if result.get("status") == "1" and result.get("geocodes"):
        geo = result["geocodes"][0]
        loc = geo.get("location", "")
        if loc:
            lng, lat = loc.split(",")
            return {"lng": lng, "lat": lat, "formatted": geo.get("formatted_address", ""), "city": geo.get("city", "")}
    return None


def format_budget(price_level):
    """高德价格等级映射"""
    mapping = {
        "1": "¥50以下", "2": "¥50-100", "3": "¥100-200",
        "4": "¥200-500", "5": "¥500以上"
    }
    return mapping.get(str(price_level), "未知")


def cmd_nearby_food(params):
    """搜索景点/地点周边餐厅"""
    location = params.get("location", "")
    cuisine = params.get("cuisine", "")
    budget = params.get("budget", "")
    radius = params.get("radius", 2000)
    limit = params.get("limit", 10)

    if not location:
        return {"error": "请提供地点名称，如：西湖、故宫、南京路步行街"}

    # 1. 地理编码
    geo = geocode_location(location)
    if not geo:
        return {"error": f"无法识别地点：{location}，请提供更具体的地址或景点名"}

    lng, lat = geo["lng"], geo["lat"]
    city = geo.get("city", "")

    # 2. POI周边搜索餐厅
    keywords = "餐厅"
    if cuisine:
        mapped = CUISINE_KEYWORDS.get(cuisine, cuisine)
        keywords = mapped

    search_params = {
        "location": f"{lng},{lat}",
        "keywords": keywords,
        "types": FOOD_TYPE_CODES,
        "radius": radius,
        "offset": limit,
        "sortrule": "weight"
    }

    result = gaode_request("poi_around", search_params)

    if result.get("status") != "1":
        return {"error": f"餐厅搜索失败，请稍后重试", "location": location}

    pois = result.get("pois", [])
    if not pois:
        return {"error": f"在{location}附近未找到餐厅", "location": location}

    # 3. 过滤和排序
    restaurants = []
    for poi in pois[:limit]:
        name = poi.get("name", "")
        addr = poi.get("address", "")
        distance = poi.get("distance", "")
        tel = poi.get("tel", "")
        rating_str = ""

        # 提取评分
        biz_ext = poi.get("biz_ext", {})
        if isinstance(biz_ext, dict):
            rating_str = biz_ext.get("rating", "")

        # 提取价格
        cost = ""
        if isinstance(biz_ext, dict):
            cost = biz_ext.get("cost", "")
        if not cost:
            cost = format_budget(poi.get("price_level", ""))

        # 提取类型标签
        type_info = poi.get("type", "")
        type_label = type_info.split(";")[-1] if type_info else ""

        # 距离格式化
        try:
            dist_int = int(distance)
            dist_fmt = f"{dist_int}m" if dist_int < 1000 else f"{dist_int/1000:.1f}km"
        except (ValueError, TypeError):
            dist_fmt = distance

        # 预算过滤
        if budget and cost:
            try:
                budget_range = budget.replace("￥", "").replace("¥", "")
                parts = budget_range.split("-")
                if len(parts) == 2:
                    low, high = int(parts[0]), int(parts[1])
                    # cost可能是数字或文字
                    try:
                        cost_num = int(cost.replace("￥", "").replace("¥", "").replace(",", ""))
                        if not (low <= cost_num <= high):
                            continue
                    except ValueError:
                        pass  # 无法解析则不过滤
            except Exception:
                pass

        restaurants.append({
            "name": name,
            "type": type_label,
            "address": addr,
            "distance": dist_fmt,
            "rating": rating_str if rating_str else "暂无评分",
            "avg_cost": cost if cost else "暂无",
            "phone": tel.split(";")[0] if tel else "",
        })

    return {
        "location": location,
        "formatted_address": geo.get("formatted", ""),
        "city": city,
        "restaurants": restaurants,
        "total": len(restaurants),
        "search_radius": f"{radius}m"
    }


def cmd_local_specialty(params):
    """查询城市当地必吃特色"""
    city = params.get("city", "")
    scenario = params.get("scenario", "")

    if not city:
        return {"error": "请提供城市名称"}

    # 模糊匹配城市名
    matched_city = None
    for key in LOCAL_SPECIALTIES:
        if key in city or city in key:
            matched_city = key
            break

    if not matched_city:
        # 未在知识库中的城市，给出通用建议
        return {
            "city": city,
            "note": f"{city}的详细特色美食库暂未收录，以下为通用旅行美食建议",
            "general_tips": [
                "搜索当地'老字号'餐厅，通常是几十年积累的好味道",
                "找本地人排队的店，不会踩雷",
                "农贸市场/早市是最地道的美食体验",
                "问酒店前台推荐，比网上攻略靠谱",
                "避开景区正门口的餐厅，多走2条街",
                "当地出租车/网约车司机是最佳美食向导",
            ],
            "suggestion": f"可用 nearby_food 工具搜索{city}景点周边餐厅，获取实时数据"
        }

    info = LOCAL_SPECIALTIES[matched_city]

    result = {
        "city": matched_city,
        "must_try": info.get("必吃", []),
        "food_streets": info.get("美食街区", []),
        "tips": info.get("就餐贴士", ""),
    }

    # 按场景过滤
    if scenario:
        scenario_map = {
            "早餐": "早餐", "夜宵": "夜宵", "伴手礼": "伴手礼",
        }
        key = scenario_map.get(scenario, scenario)
        if key in info:
            result["scenario"] = {key: info[key]}

    return result


def cmd_food_plan(params):
    """生成旅行多日餐饮计划"""
    city = params.get("city", "")
    days = params.get("days", 2)
    budget_per_meal = params.get("budget_per_meal", "")
    preferences = params.get("preferences", "")
    attractions = params.get("attractions", [])

    if not city:
        return {"error": "请提供城市名称"}

    try:
        days = int(days)
        if days < 1:
            days = 1
        if days > 7:
            days = 7
    except (ValueError, TypeError):
        days = 2

    # 获取城市特色
    matched_city = None
    for key in LOCAL_SPECIALTIES:
        if key in city or city in key:
            matched_city = key
            break

    specialty_info = LOCAL_SPECIALTIES.get(matched_city, {}) if matched_city else {}

    # 预算等级
    budget_level = "中等"
    if budget_per_meal:
        try:
            b = int(str(budget_per_meal).replace("￥", "").replace("¥", ""))
            if b <= 50:
                budget_level = "经济"
            elif b <= 150:
                budget_level = "中等"
            else:
                budget_level = "高端"
        except (ValueError, TypeError):
            pass

    # 饮食偏好处理
    pref_note = ""
    if preferences:
        pref_list = [p.strip() for p in preferences.split("/") if p.strip()]
        pref_note = f"注意饮食偏好：{'、'.join(pref_list)}"

    # 生成每日餐饮计划框架
    must_try = specialty_info.get("必吃", [])
    breakfast_items = specialty_info.get("早餐", [])
    night_snack_items = specialty_info.get("夜宵", [])
    food_streets = specialty_info.get("美食街区", [])
    tips = specialty_info.get("就餐贴士", "")

    # 每日三餐+夜宵模板
    meal_slots = ["早餐", "午餐", "晚餐"]
    if night_snack_items:
        meal_slots.append("夜宵")

    plan = []
    for day_idx in range(days):
        day_plan = {"day": day_idx + 1, "meals": {}}

        for slot in meal_slots:
            if slot == "早餐" and breakfast_items:
                # 早餐从早餐列表轮换
                idx = day_idx % len(breakfast_items)
                day_plan["meals"]["早餐"] = breakfast_items[idx]
            elif slot == "夜宵" and night_snack_items:
                idx = day_idx % len(night_snack_items)
                day_plan["meals"]["夜宵"] = night_snack_items[idx]
            elif slot == "午餐":
                # 午餐推荐必吃项或美食街区
                if must_try:
                    idx = (day_idx * 2) % len(must_try)
                    day_plan["meals"]["午餐"] = f"尝{must_try[idx]}"
                else:
                    day_plan["meals"]["午餐"] = "当地特色菜馆"
            elif slot == "晚餐":
                if must_try:
                    idx = (day_idx * 2 + 1) % len(must_try)
                    day_plan["meals"]["晚餐"] = f"尝{must_try[idx]}"
                else:
                    day_plan["meals"]["晚餐"] = "当地人气餐厅"

        # 如果有景点信息，标注就近用餐建议
        if attractions and day_idx < len(attractions):
            day_plan["attraction"] = attractions[day_idx]
            day_plan["dining_hint"] = f"游览{attractions[day_idx]}，午餐建议在景区附近"

        plan.append(day_plan)

    result = {
        "city": matched_city or city,
        "days": days,
        "budget_level": budget_level,
        "plan": plan,
        "must_distribute": must_try[:6] if must_try else [],
        "food_streets": food_streets,
    }

    if pref_note:
        result["preference_note"] = pref_note

    if tips:
        result["tips"] = tips

    return result


# ====== 主入口 ======
TOOLS = {
    "nearby_food": cmd_nearby_food,
    "local_specialty": cmd_local_specialty,
    "food_plan": cmd_food_plan,
}


def main():
    if len(sys.argv) < 3:
        print(json.dumps({"error": "用法: python3 food_guide.py <tool> '<json_params>'", "tools": list(TOOLS.keys())}, ensure_ascii=False))
        return

    tool = sys.argv[1]
    try:
        params = json.loads(sys.argv[2])
    except json.JSONDecodeError:
        print(json.dumps({"error": "参数JSON解析失败"}, ensure_ascii=False))
        return

    handler = TOOLS.get(tool)
    if not handler:
        print(json.dumps({"error": f"未知工具: {tool}", "tools": list(TOOLS.keys())}, ensure_ascii=False))
        return

    result = handler(params)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

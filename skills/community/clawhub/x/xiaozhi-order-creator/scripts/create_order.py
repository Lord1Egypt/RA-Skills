#!/usr/bin/env python3

import argparse
import json
import sys
import time
import uuid
import urllib.request
import urllib.error
import urllib.parse


# ============================================================
# URL 常量
# ============================================================
DEFAULT_DEVICE_ORDER_URL = "https://papi.bearhome.cn/hs/app/order/open/used"
DEFAULT_POLL_URL = "https://api.bearhome.cn/hsapi/recovery/order/recoverComm/auth/getTokenByCode"
DEFAULT_CLOTHING_PRICE_URL = "https://api.bearhome.cn/hsapi/recovery/order/recoverOrder/queryPrice"
DEFAULT_CLOTHING_ORDER_URL = "https://api.bearhome.cn/hsapi/recovery/order/recoverOrder/createOrder"
DEFAULT_MINIPROGRAM_CODE_URL = "https://api.bearhome.cn/api/product/product/fuwu/codePic"

# ============================================================
# 微信 OAuth 常量
# ============================================================
WECHAT_APPID = "wxf386957290ae6e88"
WECHAT_REDIRECT_URI = "https://www.bearhome.cn/login/thirdLogin"

# ============================================================
# 默认参数
# ============================================================
DEFAULT_SOURCE = 172
POLL_INTERVAL = 2
POLL_MAX_ATTEMPTS = 60

# 衣服品类固定参数
CLOTHING_GOODS_TYPE = 1
CLOTHING_CATEGORY_ID = 2767
CLOTHING_ITEM_CATES = "衣服"
CLOTHING_ITEM_NAME = "衣服"
CLOTHING_IN_EXPRESS = 2

# ============================================================
# 中国行政区域编码（GB/T 2260）
# lookup 结构: PROV_MAP / CITY_MAP / AREA_MAP
# ============================================================

# 省份名称 -> 省份ID
PROV_MAP = {
    "北京": 110000, "北京市": 110000,
    "上海": 310000, "上海市": 310000,
    "天津": 120000, "天津市": 120000,
    "重庆": 500000, "重庆市": 500000,
    "河北": 130000, "河北省": 130000,
    "山西": 140000, "山西省": 140000,
    "内蒙古": 150000, "内蒙古自治区": 150000,
    "辽宁": 210000, "辽宁省": 210000,
    "吉林": 220000, "吉林省": 220000,
    "黑龙江": 230000, "黑龙江省": 230000,
    "江苏": 320000, "江苏省": 320000,
    "浙江": 330000, "浙江省": 330000,
    "安徽": 340000, "安徽省": 340000,
    "福建": 350000, "福建省": 350000,
    "江西": 360000, "江西省": 360000,
    "山东": 370000, "山东省": 370000,
    "河南": 410000, "河南省": 410000,
    "湖北": 420000, "湖北省": 420000,
    "湖南": 430000, "湖南省": 430000,
    "广东": 440000, "广东省": 440000,
    "广西": 450000, "广西壮族自治区": 450000,
    "海南": 460000, "海南省": 460000,
    "四川": 510000, "四川省": 510000,
    "贵州": 520000, "贵州省": 520000,
    "云南": 530000, "云南省": 530000,
    "西藏": 540000, "西藏自治区": 540000,
    "陕西": 610000, "陕西省": 610000,
    "甘肃": 620000, "甘肃省": 620000,
    "青海": 630000, "青海省": 630000,
    "宁夏": 640000, "宁夏回族自治区": 640000,
    "新疆": 650000, "新疆维吾尔自治区": 650000,
    "香港": 810000, "香港特别行政区": 810000,
    "澳门": 820000, "澳门特别行政区": 820000,
    "台湾": 710000, "台湾省": 710000,
}

# (省份名, 城市名) -> 城市ID
CITY_MAP = {
    # 北京
    ("北京", "北京市"): 110100, ("北京市", "北京市"): 110100,
    # 上海
    ("上海", "上海市"): 310100, ("上海市", "上海市"): 310100,
    # 天津
    ("天津", "天津市"): 120100, ("天津市", "天津市"): 120100,
    # 重庆
    ("重庆", "重庆市"): 500100, ("重庆市", "重庆市"): 500100,
    # 河北
    ("河北", "石家庄市"): 130100, ("河北省", "石家庄市"): 130100,
    ("河北", "唐山市"): 130200, ("河北省", "唐山市"): 130200,
    ("河北", "秦皇岛市"): 130300, ("河北省", "秦皇岛市"): 130300,
    ("河北", "邯郸市"): 130400, ("河北省", "邯郸市"): 130400,
    ("河北", "保定市"): 130600, ("河北省", "保定市"): 130600,
    ("河北", "廊坊市"): 131000, ("河北省", "廊坊市"): 131000,
    # 山西
    ("山西", "太原市"): 140100, ("山西省", "太原市"): 140100,
    ("山西", "大同市"): 140200, ("山西省", "大同市"): 140200,
    # 内蒙古
    ("内蒙古", "呼和浩特市"): 150100, ("内蒙古自治区", "呼和浩特市"): 150100,
    ("内蒙古", "包头市"): 150200, ("内蒙古自治区", "包头市"): 150200,
    # 辽宁
    ("辽宁", "沈阳市"): 210100, ("辽宁省", "沈阳市"): 210100,
    ("辽宁", "大连市"): 210200, ("辽宁省", "大连市"): 210200,
    # 吉林
    ("吉林", "长春市"): 220100, ("吉林省", "长春市"): 220100,
    # 黑龙江
    ("黑龙江", "哈尔滨市"): 230100, ("黑龙江省", "哈尔滨市"): 230100,
    # 江苏
    ("江苏", "南京市"): 320100, ("江苏省", "南京市"): 320100,
    ("江苏", "苏州市"): 320500, ("江苏省", "苏州市"): 320500,
    ("江苏", "无锡市"): 320200, ("江苏省", "无锡市"): 320200,
    ("江苏", "常州市"): 320400, ("江苏省", "常州市"): 320400,
    ("江苏", "南通市"): 320600, ("江苏省", "南通市"): 320600,
    ("江苏", "扬州市"): 321000, ("江苏省", "扬州市"): 321000,
    # 浙江
    ("浙江", "杭州市"): 330100, ("浙江省", "杭州市"): 330100,
    ("浙江", "宁波市"): 330200, ("浙江省", "宁波市"): 330200,
    ("浙江", "温州市"): 330300, ("浙江省", "温州市"): 330300,
    ("浙江", "嘉兴市"): 330400, ("浙江省", "嘉兴市"): 330400,
    # 安徽
    ("安徽", "合肥市"): 340100, ("安徽省", "合肥市"): 340100,
    # 福建
    ("福建", "福州市"): 350100, ("福建省", "福州市"): 350100,
    ("福建", "厦门市"): 350200, ("福建省", "厦门市"): 350200,
    ("福建", "泉州市"): 350500, ("福建省", "泉州市"): 350500,
    # 江西
    ("江西", "南昌市"): 360100, ("江西省", "南昌市"): 360100,
    # 山东
    ("山东", "济南市"): 370100, ("山东省", "济南市"): 370100,
    ("山东", "青岛市"): 370200, ("山东省", "青岛市"): 370200,
    ("山东", "烟台市"): 370600, ("山东省", "烟台市"): 370600,
    ("山东", "潍坊市"): 370700, ("山东省", "潍坊市"): 370700,
    ("山东", "临沂市"): 371300, ("山东省", "临沂市"): 371300,
    # 河南
    ("河南", "郑州市"): 410100, ("河南省", "郑州市"): 410100,
    ("河南", "洛阳市"): 410300, ("河南省", "洛阳市"): 410300,
    # 湖北
    ("湖北", "武汉市"): 420100, ("湖北省", "武汉市"): 420100,
    # 湖南
    ("湖南", "长沙市"): 430100, ("湖南省", "长沙市"): 430100,
    # 广东
    ("广东", "广州市"): 440100, ("广东省", "广州市"): 440100,
    ("广东", "深圳市"): 440300, ("广东省", "深圳市"): 440300,
    ("广东", "东莞市"): 441900, ("广东省", "东莞市"): 441900,
    ("广东", "佛山市"): 440600, ("广东省", "佛山市"): 440600,
    ("广东", "珠海市"): 440400, ("广东省", "珠海市"): 440400,
    ("广东", "惠州市"): 441300, ("广东省", "惠州市"): 441300,
    ("广东", "中山市"): 442000, ("广东省", "中山市"): 442000,
    # 广西
    ("广西", "南宁市"): 450100, ("广西壮族自治区", "南宁市"): 450100,
    ("广西", "桂林市"): 450300, ("广西壮族自治区", "桂林市"): 450300,
    # 海南
    ("海南", "海口市"): 460100, ("海南省", "海口市"): 460100,
    ("海南", "三亚市"): 460200, ("海南省", "三亚市"): 460200,
    # 四川
    ("四川", "成都市"): 510100, ("四川省", "成都市"): 510100,
    # 贵州
    ("贵州", "贵阳市"): 520100, ("贵州省", "贵阳市"): 520100,
    # 云南
    ("云南", "昆明市"): 530100, ("云南省", "昆明市"): 530100,
    # 西藏
    ("西藏", "拉萨市"): 540100, ("西藏自治区", "拉萨市"): 540100,
    # 陕西
    ("陕西", "西安市"): 610100, ("陕西省", "西安市"): 610100,
    # 甘肃
    ("甘肃", "兰州市"): 620100, ("甘肃省", "兰州市"): 620100,
    # 青海
    ("青海", "西宁市"): 630100, ("青海省", "西宁市"): 630100,
    # 宁夏
    ("宁夏", "银川市"): 640100, ("宁夏回族自治区", "银川市"): 640100,
    # 新疆
    ("新疆", "乌鲁木齐市"): 650100, ("新疆维吾尔自治区", "乌鲁木齐市"): 650100,
}

# (城市名, 区县名) -> 区县ID
AREA_MAP = {
    # 北京市
    ("北京市", "东城区"): 110101, ("北京市", "西城区"): 110102,
    ("北京市", "朝阳区"): 110105, ("北京市", "丰台区"): 110106,
    ("北京市", "石景山区"): 110107, ("北京市", "海淀区"): 110108,
    ("北京市", "通州区"): 110112, ("北京市", "大兴区"): 110115,
    ("北京市", "顺义区"): 110113, ("北京市", "昌平区"): 110114,
    ("北京市", "房山区"): 110111,
    # 上海市
    ("上海市", "黄浦区"): 310101, ("上海市", "徐汇区"): 310104,
    ("上海市", "长宁区"): 310105, ("上海市", "静安区"): 310106,
    ("上海市", "普陀区"): 310107, ("上海市", "虹口区"): 310109,
    ("上海市", "杨浦区"): 310110, ("上海市", "浦东新区"): 310115,
    ("上海市", "闵行区"): 310112, ("上海市", "宝山区"): 310113,
    ("上海市", "嘉定区"): 310114, ("上海市", "松江区"): 310117,
    ("上海市", "青浦区"): 310118, ("上海市", "奉贤区"): 310120,
    ("上海市", "金山区"): 310116,
    # 天津市
    ("天津市", "和平区"): 120101, ("天津市", "河东区"): 120102,
    ("天津市", "河西区"): 120103, ("天津市", "南开区"): 120104,
    ("天津市", "河北区"): 120105, ("天津市", "红桥区"): 120106,
    ("天津市", "滨海新区"): 120116, ("天津市", "西青区"): 120111,
    ("天津市", "北辰区"): 120113, ("天津市", "武清区"): 120114,
    # 重庆市
    ("重庆市", "渝中区"): 500103, ("重庆市", "江北区"): 500105,
    ("重庆市", "南岸区"): 500108, ("重庆市", "沙坪坝区"): 500106,
    ("重庆市", "九龙坡区"): 500107, ("重庆市", "渝北区"): 500112,
    ("重庆市", "巴南区"): 500113, ("重庆市", "北碚区"): 500109,
    # 广州
    ("广州市", "越秀区"): 440104, ("广州市", "海珠区"): 440105,
    ("广州市", "荔湾区"): 440103, ("广州市", "天河区"): 440106,
    ("广州市", "白云区"): 440111, ("广州市", "黄埔区"): 440112,
    ("广州市", "番禺区"): 440113, ("广州市", "花都区"): 440114,
    ("广州市", "南沙区"): 440115, ("广州市", "增城区"): 440118,
    # 深圳
    ("深圳市", "罗湖区"): 440303, ("深圳市", "福田区"): 440304,
    ("深圳市", "南山区"): 440305, ("深圳市", "宝安区"): 440306,
    ("深圳市", "龙岗区"): 440307, ("深圳市", "龙华区"): 440309,
    ("深圳市", "光明区"): 440311, ("深圳市", "坪山区"): 440310,
    # 杭州
    ("杭州市", "上城区"): 330102, ("杭州市", "拱墅区"): 330105,
    ("杭州市", "西湖区"): 330106, ("杭州市", "滨江区"): 330108,
    ("杭州市", "萧山区"): 330109, ("杭州市", "余杭区"): 330110,
    ("杭州市", "临平区"): 330113, ("杭州市", "钱塘区"): 330114,
    # 成都
    ("成都市", "锦江区"): 510104, ("成都市", "青羊区"): 510105,
    ("成都市", "金牛区"): 510106, ("成都市", "武侯区"): 510107,
    ("成都市", "成华区"): 510108, ("成都市", "高新区"): 510109,
    ("成都市", "天府新区"): 510110,
    # 武汉
    ("武汉市", "江岸区"): 420102, ("武汉市", "江汉区"): 420103,
    ("武汉市", "硚口区"): 420104, ("武汉市", "汉阳区"): 420105,
    ("武汉市", "武昌区"): 420106, ("武汉市", "洪山区"): 420111,
    ("武汉市", "青山区"): 420107, ("武汉市", "东西湖区"): 420112,
    # 南京
    ("南京市", "玄武区"): 320102, ("南京市", "秦淮区"): 320104,
    ("南京市", "建邺区"): 320105, ("南京市", "鼓楼区"): 320106,
    ("南京市", "浦口区"): 320111, ("南京市", "栖霞区"): 320113,
    ("南京市", "江宁区"): 320115,
    # 苏州
    ("苏州市", "姑苏区"): 320508, ("苏州市", "虎丘区"): 320505,
    ("苏州市", "吴中区"): 320506, ("苏州市", "相城区"): 320507,
    ("苏州市", "吴江区"): 320509, ("苏州市", "工业园区"): 320512,
    # 西安
    ("西安市", "新城区"): 610102, ("西安市", "碑林区"): 610103,
    ("西安市", "莲湖区"): 610104, ("西安市", "雁塔区"): 610113,
    ("西安市", "未央区"): 610112, ("西安市", "灞桥区"): 610111,
    ("西安市", "长安区"): 610116,
    # 济南
    ("济南市", "历下区"): 370102, ("济南市", "市中区"): 370103,
    ("济南市", "槐荫区"): 370104, ("济南市", "天桥区"): 370105,
    ("济南市", "历城区"): 370112,
    # 青岛
    ("青岛市", "市南区"): 370202, ("青岛市", "市北区"): 370203,
    ("青岛市", "黄岛区"): 370211, ("青岛市", "崂山区"): 370212,
    ("青岛市", "李沧区"): 370213, ("青岛市", "城阳区"): 370214,
    # 郑州
    ("郑州市", "中原区"): 410102, ("郑州市", "二七区"): 410103,
    ("郑州市", "管城回族区"): 410104, ("郑州市", "金水区"): 410105,
    ("郑州市", "惠济区"): 410108,
    # 长沙
    ("长沙市", "芙蓉区"): 430102, ("长沙市", "天心区"): 430103,
    ("长沙市", "岳麓区"): 430104, ("长沙市", "开福区"): 430105,
    ("长沙市", "雨花区"): 430111,
    # 合肥
    ("合肥市", "瑶海区"): 340102, ("合肥市", "庐阳区"): 340103,
    ("合肥市", "蜀山区"): 340104, ("合肥市", "包河区"): 340111,
    # 厦门
    ("厦门市", "思明区"): 350203, ("厦门市", "湖里区"): 350206,
    ("厦门市", "集美区"): 350211, ("厦门市", "海沧区"): 350205,
    # 福州
    ("福州市", "鼓楼区"): 350102, ("福州市", "台江区"): 350103,
    ("福州市", "仓山区"): 350104, ("福州市", "晋安区"): 350111,
    # 石家庄
    ("石家庄市", "长安区"): 130102, ("石家庄市", "桥西区"): 130104,
    ("石家庄市", "新华区"): 130105, ("石家庄市", "裕华区"): 130108,
    # 沈阳
    ("沈阳市", "和平区"): 210102, ("沈阳市", "沈河区"): 210103,
    ("沈阳市", "皇姑区"): 210105, ("沈阳市", "铁西区"): 210106,
    ("沈阳市", "浑南区"): 210112,
    # 大连
    ("大连市", "中山区"): 210202, ("大连市", "西岗区"): 210203,
    ("大连市", "沙河口区"): 210204, ("大连市", "甘井子区"): 210211,
    # 哈尔滨
    ("哈尔滨市", "道里区"): 230102, ("哈尔滨市", "道外区"): 230104,
    ("哈尔滨市", "南岗区"): 230103, ("哈尔滨市", "松北区"): 230109,
    # 东莞
    ("东莞市", "东城街道"): 441901, ("东莞市", "南城街道"): 441902,
    ("东莞市", "莞城街道"): 441903, ("东莞市", "万江街道"): 441904,
    # 佛山
    ("佛山市", "禅城区"): 440604, ("佛山市", "南海区"): 440605,
    ("佛山市", "顺德区"): 440606, ("佛山市", "三水区"): 440607,
    # 其他省会城市
    ("长春市", "南关区"): 220102, ("长春市", "朝阳区"): 220104,
    ("南昌市", "东湖区"): 360102, ("南昌市", "西湖区"): 360103,
    ("昆明市", "五华区"): 530102, ("昆明市", "盘龙区"): 530103,
    ("南宁市", "青秀区"): 450103, ("南宁市", "兴宁区"): 450102,
    ("贵阳市", "南明区"): 520102, ("贵阳市", "云岩区"): 520103,
    ("兰州市", "城关区"): 620102,
    ("海口市", "龙华区"): 460106, ("海口市", "美兰区"): 460108,
    ("太原市", "迎泽区"): 140106, ("太原市", "杏花岭区"): 140107,
    ("呼和浩特市", "新城区"): 150102, ("呼和浩特市", "回民区"): 150103,
    ("乌鲁木齐市", "天山区"): 650102, ("乌鲁木齐市", "沙依巴克区"): 650103,
    ("银川市", "兴庆区"): 640104, ("银川市", "金凤区"): 640106,
    ("西宁市", "城东区"): 630102, ("西宁市", "城中区"): 630103,
    ("拉萨市", "城关区"): 540102,
    # 宁波
    ("宁波市", "海曙区"): 330203, ("宁波市", "鄞州区"): 330212,
    ("宁波市", "江北区"): 330205,
    # 温州
    ("温州市", "鹿城区"): 330302,
    # 无锡
    ("无锡市", "梁溪区"): 320213, ("无锡市", "滨湖区"): 320211,
    # 烟台
    ("烟台市", "芝罘区"): 370602,
    # 潍坊
    ("潍坊市", "潍城区"): 370702, ("潍坊市", "奎文区"): 370705,
    ("潍坊市", "高密市"): 370785,
    # 临沂
    ("临沂市", "兰山区"): 371302,
    # 廊坊
    ("廊坊市", "广阳区"): 131003,
    # 唐山
    ("唐山市", "路北区"): 130203,
    # 洛阳
    ("洛阳市", "西工区"): 410303,
    # 珠海
    ("珠海市", "香洲区"): 440402,
    # 惠州
    ("惠州市", "惠城区"): 441302,
    # 泉州
    ("泉州市", "鲤城区"): 350502,
}


# ============================================================
# 工具函数
# ============================================================

def generate_send_code() -> str:
    return str(uuid.uuid4().int)[:9]


def get_wechat_login_url(send_code: str) -> str:
    state_raw = f"STATE|source=skills|sendCode={send_code}"
    return (
        "https://open.weixin.qq.com/connect/qrconnect"
        "?appid=" + WECHAT_APPID +
        "&redirect_uri=" + WECHAT_REDIRECT_URI +
        "&scope=snsapi_login"
        "&state=" + state_raw +
        "&response_type=code"
        "#wechat_redirect"
    )


def fetch_miniprogram_code(send_code: str, output_path: str = None) -> str:
    """调用小程序码 API，下载图片，返回本地文件路径。"""
    import os
    import tempfile

    payload = {
        "scene": f"sendCode={send_code}",
        "path": "userPages/login/index",
        "appletType": 4,
        "appType": 0,
    }

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        DEFAULT_MINIPROGRAM_CODE_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            resp_data = resp.read()
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"获取小程序码失败 HTTP {e.code}: {error_body}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"获取小程序码网络错误: {e.reason}")

    if not resp_data:
        raise RuntimeError("获取小程序码失败: 返回空数据")

    # API 返回 JSON，image url 在 data 字段中
    try:
        resp_json = json.loads(resp_data.decode("utf-8"))
        image_url = resp_json.get("data", "")
        if not image_url:
            raise RuntimeError(f"获取小程序码失败: 响应中无图片地址 - {resp_json}")
    except json.JSONDecodeError:
        # 可能是直接返回图片二进制
        image_url = None

    if image_url:
        try:
            with urllib.request.urlopen(image_url, timeout=30) as img_resp:
                image_data = img_resp.read()
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"下载小程序码图片失败 HTTP {e.code}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"下载小程序码图片网络错误: {e.reason}")
    else:
        image_data = resp_data

    if not image_data:
        raise RuntimeError("获取小程序码失败: 图片数据为空")

    if not output_path:
        output_dir = tempfile.gettempdir()
        output_path = os.path.join(output_dir, f"miniprogram_code_{send_code}.jpg")

    with open(output_path, "wb") as f:
        f.write(image_data)

    return output_path


def poll_for_token(send_code: str, poll_url: str = None, verbose: bool = True) -> str:
    url = (poll_url or DEFAULT_POLL_URL) + "?sendCode=" + send_code
    if verbose:
        print(f"\u8f6e\u8be2\u6388\u6743\u72b6\u6001 (sendCode: {send_code})...")
    for i in range(POLL_MAX_ATTEMPTS):
        try:
            with urllib.request.urlopen(url, timeout=10) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except urllib.error.URLError as e:
            if verbose:
                print(f"  \u8f6e\u8be2\u7f51\u7edc\u9519\u8bef: {e.reason}", file=sys.stderr)
            time.sleep(POLL_INTERVAL)
            continue

        if body.get("statusCode") == 200 and body.get("data"):
            if verbose:
                print("  \u5df2\u6536\u5230\u60a8\u7684\u786e\u8ba4\u6388\u6743\uff0c\u6b63\u5728\u4e3a\u60a8\u81ea\u52a8\u4e0b\u5355...")
            return body["data"]
        if body.get("statusCode") != -1:
            err = body.get("errorInfo", "unknown")
            raise RuntimeError(f"\u83b7\u53d6 token \u5931\u8d25: {err}")

        if verbose:
            print(f"  \u7b49\u5f85\u6388\u6743... ({i + 1}/{POLL_MAX_ATTEMPTS})")
        if i < POLL_MAX_ATTEMPTS - 1:
            time.sleep(POLL_INTERVAL)

    raise TimeoutError(f"\u8f6e\u8be2\u8d85\u65f6 ({POLL_MAX_ATTEMPTS * POLL_INTERVAL}s)")


def resolve_area_codes(prov_name: str, city_name: str, area_name: str) -> dict:
    prov_id = PROV_MAP.get(prov_name)
    if prov_id is None:
        known = [k for k in PROV_MAP if prov_name[:2] in k]
        hint = f"\u53ef\u80fd\u7684\u7701\u4efd: {', '.join(known[:5])}" if known else ""
        raise ValueError(
            f"\u65e0\u6cd5\u8bc6\u522b\u7701\u4efd \"{prov_name}\"\u3002"
            f"\u8bf7\u4f7f\u7528 --prov-id \u624b\u52a8\u6307\u5b9a\u7701\u4efd\u7f16\u7801\u3002{hint}"
        )

    city_key = (prov_name, city_name)
    city_id = CITY_MAP.get(city_key)
    if city_id is None:
        alt_name = PROV_MAP.get(prov_name)
        alt_city_key = None
        for k in [prov_name, alt_name]:
            if k:
                for ck, cv in CITY_MAP.items():
                    if ck[0] == k and ck[1] == city_name:
                        alt_city_key = ck
                        city_id = cv
                        break
            if alt_city_key:
                break
        if city_id is None:
            raise ValueError(
                f"\u65e0\u6cd5\u8bc6\u522b\u57ce\u5e02 \"{city_name}\" \uff08\u7701\u4efd: {prov_name}\uff09\u3002"
                f"\u8bf7\u4f7f\u7528 --city-id \u624b\u52a8\u6307\u5b9a\u57ce\u5e02\u7f16\u7801\u3002"
            )

    area_key = (city_name, area_name)
    area_id = AREA_MAP.get(area_key)
    if area_id is None:
        raise ValueError(
            f"\u65e0\u6cd5\u8bc6\u522b\u533a\u53bf \"{area_name}\" \uff08\u57ce\u5e02: {city_name}\uff09\u3002"
            f"\u8bf7\u4f7f\u7528 --area-id \u624b\u52a8\u6307\u5b9a\u533a\u53bf\u7f16\u7801\u3002"
        )

    return {"provId": prov_id, "cityId": city_id, "areaId": area_id}


# ============================================================
# 设备品类下单（现有逻辑）
# ============================================================

def create_device_order(params: dict, admtoken: str,
                        base_url: str = None, dry_run: bool = False) -> dict:
    base_url = base_url or DEFAULT_DEVICE_ORDER_URL

    params.setdefault("source", DEFAULT_SOURCE)
    params.setdefault("price", "0.01")
    params.setdefault("remark", "")

    if not params.get("sale_item_name"):
        params["sale_item_name"] = params.get("item_cates", "")

    if dry_run:
        return {
            "success": True,
            "message": "Dry run \u2014 request not sent",
            "dry_run": True,
            "params": params,
            "request_url": base_url,
        }

    data = json.dumps(params, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(
        base_url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "token": admtoken,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            return {
                "success": True,
                "message": "\u8ba2\u5355\u63d0\u4ea4\u6210\u529f",
                "response": json.loads(body) if body else {},
                "request_url": base_url,
            }
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        return {
            "success": False,
            "message": f"HTTP {e.code}: {e.reason}",
            "error_body": error_body,
            "request_url": base_url,
        }
    except urllib.error.URLError as e:
        return {
            "success": False,
            "message": f"Connection error: {e.reason}",
            "request_url": base_url,
        }


def validate_device_params(params: dict) -> list:
    required = ["name", "mobile", "prov_name", "city_name", "area_name",
                 "address", "item_brand", "item_cates", "item_model",
                 "sale_item_name", "price"]
    missing = [f for f in required if not params.get(f)]
    return missing


# ============================================================
# 衣服品类 — 询价
# ============================================================

def query_clothing_price(prov_name: str, city_name: str, area_name: str,
                         price_url: str = None, dry_run: bool = False) -> dict:
    price_url = price_url or DEFAULT_CLOTHING_PRICE_URL

    payload = {
        "source": DEFAULT_SOURCE,
        "goodsType": CLOTHING_GOODS_TYPE,
        "categoryId": CLOTHING_CATEGORY_ID,
        "provName": prov_name,
        "cityName": city_name,
        "areaName": area_name,
    }

    if dry_run:
        return {
            "success": True,
            "message": "Dry run \u2014 price query not sent",
            "dry_run": True,
            "params": payload,
            "request_url": price_url,
        }

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        price_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return {
                "success": True,
                "message": "\u8be2\u4ef7\u6210\u529f",
                "response": body,
                "price": body.get("data", body),
                "request_url": price_url,
            }
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        return {
            "success": False,
            "message": f"HTTP {e.code}: {e.reason}",
            "error_body": error_body,
            "request_url": price_url,
        }
    except urllib.error.URLError as e:
        return {
            "success": False,
            "message": f"Connection error: {e.reason}",
            "request_url": price_url,
        }


# ============================================================
# 衣服品类 — 下单
# ============================================================

def create_clothing_order(params: dict, admtoken: str,
                          order_url: str = None, dry_run: bool = False) -> dict:
    order_url = order_url or DEFAULT_CLOTHING_ORDER_URL

    # 组装 orderItems
    item_weight = params.get("item_weight", 0)
    item_price = params.get("item_price", 0)
    try:
        item_weight = float(item_weight)
        item_price = float(item_price)
    except (TypeError, ValueError):
        raise ValueError("item_weight \u548c item_price \u5fc5\u987b\u4e3a\u6709\u6548\u6570\u5b57")

    order_payload = {
        "address": params.get("address", ""),
        "areaId": int(params.get("area_id", 0)),
        "areaName": params.get("area_name", ""),
        "cityId": int(params.get("city_id", 0)),
        "cityName": params.get("city_name", ""),
        "inExpress": CLOTHING_IN_EXPRESS,
        "inExpressTime": params.get("in_express_time", ""),
        "mobile": params.get("mobile", ""),
        "name": params.get("name", ""),
        "orderItems": [
            {
                "goodsType": CLOTHING_GOODS_TYPE,
                "itemCates": CLOTHING_ITEM_CATES,
                "itemCatesId": CLOTHING_CATEGORY_ID,
                "itemName": CLOTHING_ITEM_NAME,
                "itemPrice": item_price,
                "itemWeight": item_weight,
            }
        ],
        "price": item_price * item_weight,
        "provId": int(params.get("prov_id", 0)),
        "provName": params.get("prov_name", ""),
        "source": DEFAULT_SOURCE,
        "detail": params.get("detail", ""),
    }

    if dry_run:
        return {
            "success": True,
            "message": "Dry run \u2014 request not sent",
            "dry_run": True,
            "params": order_payload,
            "request_url": order_url,
        }

    data = json.dumps(order_payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        order_url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "jr_sso_token": admtoken,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            return {
                "success": True,
                "message": "\u8ba2\u5355\u63d0\u4ea4\u6210\u529f",
                "response": json.loads(body) if body else {},
                "request_url": order_url,
            }
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        return {
            "success": False,
            "message": f"HTTP {e.code}: {e.reason}",
            "error_body": error_body,
            "request_url": order_url,
        }
    except urllib.error.URLError as e:
        return {
            "success": False,
            "message": f"Connection error: {e.reason}",
            "request_url": order_url,
        }


def validate_clothing_params(params: dict) -> list:
    required = ["name", "mobile", "prov_name", "city_name", "area_name",
                 "address", "item_weight", "item_price", "in_express_time"]
    missing = [f for f in required if not params.get(f)]
    return missing


# ============================================================
# CLI 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(add_help=False)

    # ---- 通用参数 ----
    parser.add_argument("--order-type", choices=["device", "clothing"], default="device",
                        help="\u8ba2\u5355\u7c7b\u578b: device(\u8bbe\u5907) / clothing(\u8863\u670d)")
    parser.add_argument("--name")
    parser.add_argument("--mobile")
    parser.add_argument("--prov-name")
    parser.add_argument("--city-name")
    parser.add_argument("--area-name")
    parser.add_argument("--address")
    parser.add_argument("--prov-id", type=int)
    parser.add_argument("--city-id", type=int)
    parser.add_argument("--area-id", type=int)
    parser.add_argument("--source", type=int, default=DEFAULT_SOURCE)

    # ---- 设备品类参数 ----
    parser.add_argument("--remark", default="")
    parser.add_argument("--item-brand")
    parser.add_argument("--item-cates")
    parser.add_argument("--sale-item-name")
    parser.add_argument("--item-model")
    parser.add_argument("--price", default="0.01")

    # ---- 衣服品类参数 ----
    parser.add_argument("--item-weight", type=float,
                        help="\u8863\u670d\u91cd\u91cf (kg)")
    parser.add_argument("--item-price", type=float,
                        help="\u8863\u670d\u5355\u4ef7 (\u5143/kg)")
    parser.add_argument("--in-express-time",
                        help="\u4e0a\u95e8\u65f6\u95f4\uff0c\u683c\u5f0f: YYYY-MM-DD HH:MM:SS")
    parser.add_argument("--detail", default="",
                        help="\u8ba2\u5355\u5907\u6ce8")

    # ---- 询价模式（衣服品类） ----
    parser.add_argument("--query-price-only", action="store_true",
                        help="\u4ec5\u67e5\u8be2\u8863\u670d\u56de\u6536\u4ef7\u683c\uff0c\u4e0d\u4e0b\u5355")

    # ---- 认证与微信授权 ----
    parser.add_argument("--admtoken")
    parser.add_argument("--send-code")
    parser.add_argument("--login-url-only", action="store_true")
    parser.add_argument("--code-type", choices=["qrcode", "miniprogram"], default="miniprogram",
                        help="授权方式: qrcode(网页二维码) / miniprogram(小程序码，默认)")
    parser.add_argument("--code-output", help="小程序码图片输出路径")

    # ---- 接口地址覆盖 ----
    parser.add_argument("--base-url",
                        help="\u8bbe\u5907\u4e0b\u5355\u63a5\u53e3\u5730\u5740")
    parser.add_argument("--poll-url", default=DEFAULT_POLL_URL)
    parser.add_argument("--clothing-price-url", default=DEFAULT_CLOTHING_PRICE_URL)
    parser.add_argument("--clothing-order-url", default=DEFAULT_CLOTHING_ORDER_URL)

    # ---- 调试 ----
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--help", action="store_true")

    args = parser.parse_args()

    if args.help:
        parser.print_help()
        sys.exit(0)

    # ========================================
    # 模式 1: 生成授权码/链接（小程序码或网页二维码）
    # ========================================
    if args.login_url_only:
        sc = args.send_code or generate_send_code()
        if args.code_type == "miniprogram":
            try:
                img_path = fetch_miniprogram_code(sc, args.code_output)
                result = {
                    "send_code": sc,
                    "code_image": img_path,
                    "code_type": "miniprogram",
                }
            except RuntimeError as e:
                print(f"获取小程序码失败: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            url = get_wechat_login_url(sc)
            result = {
                "send_code": sc,
                "login_url": url,
                "code_type": "qrcode",
            }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    # ========================================
    # ========================================
    # 模式 2: 衣服品类 — 仅询价（无需授权）
    # ========================================
    if args.query_price_only:
        if args.order_type != "clothing":
            print("错误: --query-price-only 仅支持 --order-type clothing", file=sys.stderr)
            sys.exit(1)

        if not args.prov_name or not args.city_name or not args.area_name:
            print("错误: 询价需要 --prov-name, --city-name, --area-name", file=sys.stderr)
            sys.exit(1)

        result = query_clothing_price(
            prov_name=args.prov_name,
            city_name=args.city_name,
            area_name=args.area_name,
            price_url=args.clothing_price_url,
            dry_run=args.dry_run,
        )

        if args.dry_run:
            print(json.dumps(result, ensure_ascii=False, indent=2))
            sys.exit(0)

        if result["success"]:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"询价失败: {result['message']}", file=sys.stderr)
            if result.get("error_body"):
                print(f"错误详情: {result['error_body']}", file=sys.stderr)
            sys.exit(1)
        sys.exit(0)

    # ========================================
    # 模式 3: 下订单 (device / clothing)
    # ========================================

    # --- 微信授权 ---
    admtoken = args.admtoken
    if not admtoken and args.send_code:
        if args.code_type == "miniprogram":
            print("请扫描小程序码确认授权后，系统将自动提交订单...")
        else:
            print("请用微信扫码确认授权:")
            print(get_wechat_login_url(args.send_code))
            print()
        try:
            admtoken = poll_for_token(args.send_code, args.poll_url)
        except (RuntimeError, TimeoutError) as e:
            print(f"授权失败: {e}", file=sys.stderr)
            sys.exit(1)

    if not admtoken:
        print("请提供 --admtoken 或 --send-code 参数", file=sys.stderr)
        sys.exit(1)

    # --- 根据 order_type 分发 ---
    if args.order_type == "device":
        params = {k: v for k, v in vars(args).items()
                  if k not in ("admtoken", "send_code", "login_url_only",
                               "base_url", "poll_url", "dry_run", "help",
                               "order_type", "item_weight", "item_price",
                               "in_express_time", "detail",
                               "clothing_price_url", "clothing_order_url",
                               "prov_id", "city_id", "area_id",
                               "query_price_only", "code_type", "code_output")}

        if not params.get("sale_item_name"):
            params["sale_item_name"] = params.get("item_cates", "")

        missing = validate_device_params(params)
        if missing:
            print(f"\u7f3a\u5c11\u5fc5\u8981\u53c2\u6570: {', '.join(missing)}", file=sys.stderr)
            sys.exit(1)

        result = create_device_order(
            params=params,
            admtoken=admtoken,
            base_url=args.base_url,
            dry_run=args.dry_run,
        )

    elif args.order_type == "clothing":
        # 解析行政编码
        prov_id = args.prov_id
        city_id = args.city_id
        area_id = args.area_id

        if not (prov_id and city_id and area_id):
            try:
                codes = resolve_area_codes(args.prov_name, args.city_name, args.area_name)
                if not prov_id:
                    prov_id = codes["provId"]
                if not city_id:
                    city_id = codes["cityId"]
                if not area_id:
                    area_id = codes["areaId"]
            except ValueError as e:
                print(f"\u884c\u653f\u533a\u57df\u7f16\u7801\u89e3\u6790\u5931\u8d25: {e}", file=sys.stderr)
                print("\u8bf7\u901a\u8fc7 --prov-id / --city-id / --area-id \u624b\u52a8\u6307\u5b9a\u7f16\u7801", file=sys.stderr)
                sys.exit(1)

        params = {
            "name": args.name,
            "mobile": args.mobile,
            "prov_name": args.prov_name,
            "city_name": args.city_name,
            "area_name": args.area_name,
            "address": args.address,
            "prov_id": prov_id,
            "city_id": city_id,
            "area_id": area_id,
            "item_weight": args.item_weight,
            "item_price": args.item_price if args.item_price else 0,
            "in_express_time": args.in_express_time,
            "detail": args.detail,
        }

        missing = validate_clothing_params(params)
        if missing:
            print(f"\u7f3a\u5c11\u5fc5\u8981\u53c2\u6570: {', '.join(missing)}", file=sys.stderr)
            sys.exit(1)

        result = create_clothing_order(
            params=params,
            admtoken=admtoken,
            order_url=args.clothing_order_url,
            dry_run=args.dry_run,
        )

    # --- 输出结果 ---
    if args.dry_run:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif result["success"]:
        print("\u8ba2\u5355\u63d0\u4ea4\u6210\u529f")
        print(json.dumps(result["response"], ensure_ascii=False, indent=2))
    else:
        print(f"\u4e0b\u5355\u5931\u8d25: {result['message']}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

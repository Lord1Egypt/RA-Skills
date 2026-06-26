"""
Test Data Generator Core
生成高质量测试数据，支持多种格式和数据库
"""

import random
import json
import csv
import re
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from io import StringIO

# ============= 数据源 =============

FIRST_NAMES = [
    "张","王","李","赵","刘","陈","杨","黄","周","吴",
    "徐","孙","马","朱","胡","郭","何","高","林","罗",
    "郑","梁","谢","宋","唐","许","韩","邓","冯","曹",
    "彭","曾","肖","田","董","潘","袁","蔡","贾","余",
    "于","杜","魏","叶","程","苏","傅","卢","汪","戴"
]

LAST_NAMES = [
    "伟","芳","娜","秀英","敏","静","丽","强","磊","军",
    "洋","勇","艳","杰","娟","涛","明","超","秀兰","霞",
    "平","刚","桂英","华","建","玲","国华","建华","建国",
    "志强","秀珍","海","波","军","辉","鹏","飞","欢","丹"
]

EMAIL_DOMAINS = [
    "gmail.com","163.com","qq.com","126.com","outlook.com",
    "sina.com","hotmail.com","yahoo.com","foxmail.com","edu.cn"
]

PHONE_PREFIXES = [
    "130","131","132","133","134","135","136","137","138","139",
    "150","151","152","153","155","156","157","158","159",
    "170","171","172","173","176","177","178",
    "180","181","182","183","184","185","186","187","188","189"
]

PROVINCES = [
    "北京市","上海市","天津市","重庆市",
    "广东省","江苏省","浙江省","四川省","湖北省","湖南省",
    "河南省","河北省","山东省","山西省","安徽省","福建省",
    "江西省","辽宁省","吉林省","黑龙江省","陕西省","甘肃省",
    "云南省","贵州省","青海省","内蒙古","广西","西藏","宁夏","新疆","海南省"
]

CITIES = {
    "北京市":["北京市"],
    "上海市":["上海市"],
    "天津市":["天津市"],
    "重庆市":["重庆市"],
    "广东省":["广州市","深圳市","东莞市","佛山市","珠海市","中山市","惠州市","汕头市","湛江市"],
    "江苏省":["南京市","苏州市","无锡市","常州市","南通市","徐州市","扬州市","盐城市"],
    "浙江省":["杭州市","宁波市","温州市","嘉兴市","湖州市","绍兴市","金华市","台州市"],
    "四川省":["成都市","绵阳市","德阳市","南充市","宜宾市","自贡市","泸州市","达州市"],
    "湖北省":["武汉市","宜昌市","襄阳市","荆州市","黄冈市","孝感市","咸宁市","十堰市"],
    "湖南省":["长沙市","株洲市","湘潭市","衡阳市","岳阳市","常德市","张家界市","益阳市"],
    "河南省":["郑州市","洛阳市","开封市","安阳市","新乡市","焦作市","许昌市","周口市"],
    "河北省":["石家庄市","保定市","唐山市","廊坊市","邯郸市","秦皇岛市","沧州市","邢台市"],
    "山东省":["济南市","青岛市","烟台市","威海市","潍坊市","淄博市","临沂市","济宁市"],
    "山西省":["太原市","大同市","长治市","临汾市","运城市","晋城市","阳泉市"],
    "安徽省":["合肥市","芜湖市","蚌埠市","淮南市","马鞍山市","淮北市","铜陵市"],
    "福建省":["福州市","厦门市","泉州市","漳州市","莆田市","宁德市","三明市"],
    "江西省":["南昌市","景德镇市","九江市","赣州市","吉安市","宜春市","抚州市"],
    "辽宁省":["沈阳市","大连市","鞍山市","抚顺市","本溪市","锦州市","葫芦岛市"],
    "吉林省":["长春市","吉林市","四平市","辽源市","通化市","延边朝鲜族自治州"],
    "黑龙江省":["哈尔滨市","齐齐哈尔市","牡丹江市","佳木斯市","大庆市","鸡西市"],
    "陕西省":["西安市","宝鸡市","咸阳市","铜川市","渭南市","延安市","汉中市"],
    "甘肃省":["兰州市","嘉峪关市","金昌市","白银市","天水市","武威市"],
    "云南省":["昆明市","曲靖市","玉溪市","保山市","昭通市","丽江市","普洱市"],
    "贵州省":["贵阳市","六盘水市","遵义市","安顺市","毕节市","铜仁市"],
    "青海省":["西宁市","海东市","海南藏族自治州","海北藏族自治州"],
    "内蒙古":["呼和浩特市","包头市","乌海市","赤峰市","呼伦贝尔市","鄂尔多斯市"],
    "广西":["南宁市","柳州市","桂林市","梧州市","北海市","防城港市","钦州市"],
    "西藏":["拉萨市","日喀则市","昌都市","林芝市","山南市"],
    "宁夏":["银川市","石嘴山市","吴忠市","固原市","中卫市"],
    "新疆":["乌鲁木齐市","克拉玛依市","吐鲁番市","哈密市","伊犁哈萨克自治州"],
    "海南省":["海口市","三亚市","三沙市","儋州市"]
}

DISTRICTS = ["朝阳区","海淀区","丰台区","石景山区","东城区","西城区","浦东新区","徐汇区","黄浦区","静安区",
             "天河区","越秀区","海珠区","荔湾区","白云区","南山区","福田区","宝安区","龙岗区","罗湖区"]

STREETS = ["中山路","人民路","建设路","解放路","文化路","和平路","民主路","胜利路","友谊路","光明路",
           "新华路","长江路","黄河路","珠江路","哈尔滨路","南京路","北京路","上海路","天津路","重庆路"]

ORDER_STATUSES = ["pending","paid","shipped","delivered","cancelled","refunded"]
PRODUCT_CATEGORIES = ["电子产品","服装","食品","图书","家居","玩具","体育","美妆","医药","汽车"]
PAYMENT_METHODS = ["alipay","wechat","card","cash"]
GENDERS = ["男","女"]

# ============= 工具函数 =============

def random_name() -> str:
    """生成随机中文姓名"""
    return random.choice(FIRST_NAMES) + random.choice(LAST_NAMES)

def random_email(name: str = None) -> str:
    """生成随机邮箱"""
    if name is None:
        name = random_name()
    # 拼音化处理
    pinyin_name = name.lower()
    separators = ["",".","_"]
    sep = random.choice(separators)
    nums = random.randint(0, 999)
    domain = random.choice(EMAIL_DOMAINS)
    patterns = [
        f"{pinyin_name}{sep}{nums}@{domain}",
        f"{pinyin_name}{nums}@{domain}",
        f"{pinyin_name[0]}{sep}{nums}@{domain}",
    ]
    return random.choice(patterns)

def random_phone() -> str:
    """生成随机中国手机号"""
    prefix = random.choice(PHONE_PREFIXES)
    suffix = f"{random.randint(10000000, 99999999)}"
    return prefix + suffix

def random_age(min_age: int = 18, max_age: int = 80) -> int:
    """生成随机年龄"""
    return random.randint(min_age, max_age)

def random_gender() -> str:
    """随机性别"""
    return random.choice(GENDERS)

def random_amount(min_amount: float = 0.01, max_amount: float = 9999.99) -> float:
    """生成随机金额"""
    return round(random.uniform(min_amount, max_amount), 2)

def random_date(start_year: int = 2020) -> str:
    """生成随机日期"""
    start = datetime(start_year, 1, 1)
    end = datetime.now()
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime("%Y-%m-%d")

def random_datetime(start_year: int = 2020) -> str:
    """生成随机日期时间"""
    start = datetime(start_year, 1, 1)
    end = datetime.now()
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return (start + timedelta(seconds=random_seconds)).strftime("%Y-%m-%d %H:%M:%S")

def random_enum(choices: List[str]) -> str:
    """从枚举中随机选择"""
    return random.choice(choices)

def random_address() -> Dict[str, str]:
    """生成随机地址"""
    province = random.choice(PROVINCES)
    city = random.choice(CITIES.get(province, [""]))
    district = random.choice(DISTRICTS)
    street = random.choice(STREETS) + str(random.randint(1, 999)) + "号"
    return {
        "province": province,
        "city": city,
        "district": district,
        "detail": f"{district}{street}"
    }

def random_product_name() -> str:
    """生成随机产品名称"""
    brands = ["华为","小米","苹果","三星","OPPO","vivo","联想","戴尔","惠普","索尼"]
    categories = ["手机","电脑","平板","耳机","手表","相机","电视","冰箱","洗衣机","空调"]
    return f"{random.choice(brands)} {random.choice(categories)} {random.randint(1,9)}代"

def random_uuid() -> str:
    """生成随机UUID-like ID"""
    return f"{random.randint(100000,999999)}-{random.randint(1000,9999)}"

# ============= 模板定义 =============

DEFAULT_TEMPLATES = {
    "users": {
        "fields": {
            "id": {"type": "auto_increment", "start": 1},
            "name": {"type": "name"},
            "email": {"type": "email"},
            "phone": {"type": "phone"},
            "age": {"type": "age"},
            "gender": {"type": "gender"},
            "created_at": {"type": "datetime"}
        }
    },
    "orders": {
        "fields": {
            "id": {"type": "uuid"},
            "user_id": {"type": "auto_increment", "start": 1},
            "product": {"type": "product_name"},
            "amount": {"type": "amount"},
            "quantity": {"type": "int", "min": 1, "max": 10},
            "status": {"type": "enum", "values": ORDER_STATUSES},
            "payment_method": {"type": "enum", "values": PAYMENT_METHODS},
            "created_at": {"type": "datetime"}
        }
    },
    "products": {
        "fields": {
            "id": {"type": "auto_increment", "start": 1},
            "name": {"type": "product_name"},
            "category": {"type": "enum", "values": PRODUCT_CATEGORIES},
            "price": {"type": "amount", "min": 9.9, "max": 9999.9},
            "stock": {"type": "int", "min": 0, "max": 1000},
            "created_at": {"type": "datetime"}
        }
    },
    "reviews": {
        "fields": {
            "id": {"type": "uuid"},
            "user_id": {"type": "auto_increment", "start": 1},
            "product_id": {"type": "auto_increment", "start": 1},
            "rating": {"type": "int", "min": 1, "max": 5},
            "comment": {"type": "text", "max_length": 200},
            "created_at": {"type": "datetime"}
        }
    },
    "addresses": {
        "fields": {
            "id": {"type": "auto_increment", "start": 1},
            "user_id": {"type": "auto_increment", "start": 1},
            "province": {"type": "province"},
            "city": {"type": "city"},
            "district": {"type": "enum", "values": DISTRICTS},
            "detail": {"type": "text", "max_length": 100},
            "phone": {"type": "phone"},
            "is_default": {"type": "bool"}
        }
    }
}

COMMENTS = [
    "质量很好，满意！","发货速度快","包装严实","和描述一致","性价比高",
    "服务态度好","值得购买","推荐！","一般般","有点失望","还行吧",
    "很好用","不错不错","超级喜欢","下次还来","非常好！"
]

# ============= 核心生成器 =============

class DataGenerator:
    """测试数据生成器"""

    def __init__(self, template: str = "users"):
        self.template_name = template
        self.template = DEFAULT_TEMPLATES.get(template, DEFAULT_TEMPLATES["users"])
        self._auto_increment_values: Dict[str, int] = {}
        for field_name, field_def in self.template["fields"].items():
            if field_def.get("type") == "auto_increment":
                self._auto_increment_values[field_name] = field_def.get("start", 1)

    def _generate_field(self, field_name: str, field_def: Dict) -> Any:
        """根据字段定义生成单个字段值"""
        ftype = field_def.get("type", "text")

        if ftype == "name":
            return random_name()
        elif ftype == "email":
            return random_email()
        elif ftype == "phone":
            return random_phone()
        elif ftype == "age":
            return random_age(field_def.get("min", 18), field_def.get("max", 80))
        elif ftype == "gender":
            return random_gender()
        elif ftype == "amount":
            return random_amount(field_def.get("min", 0.01), field_def.get("max", 9999.99))
        elif ftype == "date":
            return random_date(field_def.get("start_year", 2020))
        elif ftype == "datetime":
            return random_datetime(field_def.get("start_year", 2020))
        elif ftype == "enum":
            return random_enum(field_def.get("values", ["A","B"]))
        elif ftype == "uuid":
            return random_uuid()
        elif ftype == "auto_increment":
            val = self._auto_increment_values[field_name]
            self._auto_increment_values[field_name] += 1
            return val
        elif ftype == "product_name":
            return random_product_name()
        elif ftype == "province":
            return random.choice(PROVINCES)
        elif ftype == "city":
            return random.choice(list(CITIES.keys()))
        elif ftype == "bool":
            return random.choice([True, False])
        elif ftype == "int":
            return random.randint(field_def.get("min", 0), field_def.get("max", 100))
        elif ftype == "text":
            max_len = field_def.get("max_length", 100)
            if "评论" in field_name or "comment" in field_name.lower():
                return random.choice(COMMENTS)
            return f"测试文本{random.randint(1,999)}"
        else:
            return f"value_{random.randint(1,100)}"

    def generate(self, count: int = 1) -> List[Dict[str, Any]]:
        """生成指定数量的数据"""
        results = []
        for _ in range(count):
            record = {}
            for field_name, field_def in self.template["fields"].items():
                record[field_name] = self._generate_field(field_name, field_def)
            results.append(record)
        return results

    def to_json(self, data: List[Dict[str, Any]]) -> str:
        """转换为JSON格式"""
        return json.dumps(data, ensure_ascii=False, indent=2)

    def to_csv(self, data: List[Dict[str, Any]]) -> str:
        """转换为CSV格式"""
        if not data:
            return ""
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()

    def to_sql(self, data: List[Dict[str, Any]], db_type: str = "mysql", table_name: str = None) -> str:
        """转换为SQL INSERT语句"""
        if not data:
            return ""
        if table_name is None:
            table_name = self.template_name

        sql_statements = []
        for record in data:
            columns = ", ".join(record.keys())
            values = []
            for v in record.values():
                if v is None:
                    values.append("NULL")
                elif isinstance(v, bool):
                    values.append("1" if v else "0")
                elif isinstance(v, (int, float)):
                    values.append(str(v))
                elif isinstance(v, str):
                    # 转义单引号
                    escaped = v.replace("'", "''")
                    values.append(f"'{escaped}'")
                else:
                    values.append(f"'{str(v)}'")
            values_str = ", ".join(values)
            sql_statements.append(f"INSERT INTO {table_name} ({columns}) VALUES ({values_str});")

        # PostgreSQL使用双引号
        if db_type == "pg":
            sql_statements = [s.replace('"', '"') for s in sql_statements]

        return "\n".join(sql_statements)

    @staticmethod
    def get_available_templates() -> List[str]:
        """获取可用模板列表"""
        return list(DEFAULT_TEMPLATES.keys())


def load_template(path: str) -> Dict:
    """从文件加载自定义模板"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_from_template(template_name: str, count: int, output_format: str,
                           db_type: str = "mysql", custom_template: str = None) -> str:
    """根据模板生成数据"""
    if custom_template and os.path.exists(custom_template):
        template_data = load_template(custom_template)
        # 临时覆盖
        saved = DEFAULT_TEMPLATES.get(template_name, {})
        DEFAULT_TEMPLATES[template_name] = template_data

    gen = DataGenerator(template_name)
    data = gen.generate(count)

    if output_format == "json":
        result = gen.to_json(data)
    elif output_format == "csv":
        result = gen.to_csv(data)
    elif output_format == "sql":
        result = gen.to_sql(data, db_type)
    else:
        raise ValueError(f"不支持的格式: {output_format}")

    # 恢复原模板
    if custom_template and os.path.exists(custom_template):
        if saved:
            DEFAULT_TEMPLATES[template_name] = saved

    return result

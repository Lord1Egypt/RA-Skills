# 生成 300 条穿搭模板的脚本
import json
import random

categories = {
    "休闲": 80,
    "职场": 50,
    "约会": 40,
    "运动": 20,
    "旅行": 25,
    "聚会": 30,
    "正式": 15,
    "居家": 15,
    "其他": 25
}

outer_items = ["风衣", "大衣", "西装", "针织开衫", "牛仔外套", "羽绒服", "棉衣", "皮衣", "夹克", "毛呢外套", "棒球服", "卫衣外套"]
top_items = ["T恤", "衬衫", "卫衣", "毛衣", "针织衫", "背心", "吊带", "打底衫", "条纹衫", "雪纺衫", "露肩上衣", "高领毛衣"]
bottom_items = ["牛仔裤", "休闲裤", "西裤", "阔腿裤", "短裤", "半裙", "连衣裙", "A字裙", "包臀裙", "运动裤", "喇叭裤", "铅笔裤"]
shoes_items = ["小白鞋", "帆布鞋", "高跟鞋", "运动鞋", "乐福鞋", "短靴", "长靴", "平底鞋", "凉鞋", "拖鞋", "马丁靴", "穆勒鞋"]
accessory_items = ["包包", "围巾", "帽子", "项链", "耳环", "手链", "腰带", "眼镜", "丝巾", "发带", "手表", "戒指"]

colors = ["黑色", "白色", "灰色", "米色", "卡其色", "棕色", "驼色", "藏青", "红色", "粉色", "蓝色", "绿色", "紫色"]

tips_pool = [
    "敞开穿更休闲，内搭塞进去显腿长",
    "合身剪裁更显专业，配饰选择简约款",
    "柔和色调更有亲和力，适当露肤增加女人味",
    "同色系搭配显高级，层次感是关键",
    "上松下紧或上紧下松，打造好比例",
    "配件点缀提升精致度",
    "选择适合自己肤色的颜色",
    "基础款永不过时，投资高品质单品",
    "混搭不同风格创造新意",
    "注意面料质感，提升整体档次",
    "适当露肤增加轻盈感",
    "腰线决定身材比例，高腰款显腿长",
    "配饰是点睛之笔，但不要过多",
    "根据场合选择合适的正式度",
    "颜色呼应让搭配更和谐",
    "质感比数量更重要",
    "经典款投资好品质，潮流款选快时尚",
    "了解自己的身材优势，扬长避短",
    "舒适度与美观度同样重要",
    "叠穿增加层次感，但不超过三层"
]

def generate_template(idx, category):
    """生成单个模板"""
    gender = "female" if random.random() < 0.9 else "unisex"
    
    # 根据类别选择单品
    if category == "职场":
        occasion_pool = ["上班", "面试", "会议", "商务", "通勤"]
        outer = random.choice(["西装", "风衣", "毛呢大衣", "针织开衫", ""])
        top = random.choice(["衬衫", "针织衫", "高领毛衣", "西装外套"])
        bottom = random.choice(["西裤", "西裙", "阔腿裤", "直筒裤"])
        shoes = random.choice(["高跟鞋", "中跟鞋", "乐福鞋"])
    elif category == "约会":
        occasion_pool = ["约会", "聚会", "下午茶", "晚餐", "逛街"]
        outer = random.choice(["针织开衫", "风衣", "牛仔外套", ""])
        top = random.choice(["连衣裙", "雪纺衫", "露肩上衣", "针织衫", ""])
        bottom = random.choice(["半裙", "连衣裙", "牛仔裤", ""])
        shoes = random.choice(["高跟鞋", "平底鞋", "短靴"])
    elif category == "休闲":
        occasion_pool = ["日常", "逛街", "周末", "放松", "聚会"]
        outer = random.choice(["风衣", "牛仔外套", "卫衣外套", "针织开衫", ""])
        top = random.choice(["T恤", "卫衣", "毛衣", "衬衫", "针织衫"])
        bottom = random.choice(["牛仔裤", "休闲裤", "阔腿裤", "半裙", "短裤"])
        shoes = random.choice(["小白鞋", "帆布鞋", "运动鞋", "乐福鞋"])
    elif category == "运动":
        occasion_pool = ["运动", "健身", "跑步", "瑜伽", "户外活动"]
        outer = ""
        top = random.choice(["运动背心", "速干T恤", "运动内衣", "卫衣"])
        bottom = random.choice(["运动裤", "瑜伽裤", "运动短裤", "运动裙"])
        shoes = random.choice(["运动鞋", "跑鞋", "训练鞋"])
    elif category == "旅行":
        occasion_pool = ["旅行", "度假", "机场", "出差", "探索"]
        outer = random.choice(["风衣", "牛仔外套", ""])
        top = random.choice(["T恤", "衬衫", "针织衫", "连衣裙"])
        bottom = random.choice(["牛仔裤", "休闲裤", "阔腿裤", "连衣裙"])
        shoes = random.choice(["小白鞋", "运动鞋", "乐福鞋", "平底鞋"])
    elif category == "聚会":
        occasion_pool = ["聚会", "派对", "KTV", "聚餐", "社交"]
        outer = random.choice(["西装", "皮衣", "牛仔外套", ""])
        top = random.choice(["露肩上衣", "亮片上衣", "衬衫", "连衣裙"])
        bottom = random.choice(["半裙", "牛仔裤", "连衣裙", "皮裤"])
        shoes = random.choice(["高跟鞋", "短靴", "马丁靴"])
    elif category == "正式":
        occasion_pool = ["婚礼", "晚宴", "典礼", "年会", "颁奖"]
        outer = random.choice(["礼服外套", "披肩", ""])
        top = ""
        bottom = random.choice(["晚礼服", "小黑裙", "旗袍", "礼服裙"])
        shoes = random.choice(["高跟鞋", "细跟鞋", "水晶鞋"])
    elif category == "居家":
        occasion_pool = ["居家", "休息", "睡眠", "放松", "宅家"]
        outer = ""
        top = random.choice(["家居服上衣", "睡衣", "T恤", "背心"])
        bottom = random.choice(["家居裤", "睡裤", "短裤", "休闲裤"])
        shoes = random.choice(["拖鞋", "居家鞋", ""])
    else:
        occasion_pool = ["日常", "其他"]
        outer = random.choice(outer_items + [""])
        top = random.choice(top_items)
        bottom = random.choice(bottom_items)
        shoes = random.choice(shoes_items)
    
    # 构建单品字典
    items_dict = {}
    if outer:
        items_dict["outer"] = [outer]
    if top:
        items_dict["top"] = [top]
    if bottom:
        items_dict["bottom"] = [bottom]
    if shoes:
        items_dict["shoes"] = [shoes]
    
    # 随机添加配饰（30%概率）
    if random.random() < 0.3:
        items_dict["accessory"] = [random.choice(accessory_items)]
    
    # 选择颜色
    primary = random.sample(colors, min(2, len(colors)))
    accent = [random.choice(colors)] if random.random() < 0.5 else []
    
    template = {
        "id": f"t_{category.lower()}_{idx:03d}",
        "name": f"{category}搭配 {idx}",
        "category": category,
        "gender": gender,
        "occasions": random.sample(occasion_pool, min(2, len(occasion_pool))),
        "items": items_dict,
        "colors": {
            "primary": primary,
            "accent": accent
        },
        "tips": random.choice(tips_pool)
    }
    
    return template

# 生成所有模板
templates = []
idx = 1

for category, count in categories.items():
    for _ in range(count):
        template = generate_template(idx, category)
        templates.append(template)
        idx += 1

# 保存
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, 'assets', 'data', 'templates.json')

# 确保目录存在
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(templates, f, ensure_ascii=False, indent=2)

print(f"已生成 {len(templates)} 条搭配模板")

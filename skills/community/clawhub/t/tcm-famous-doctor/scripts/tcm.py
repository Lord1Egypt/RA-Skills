import json

# 九种体质核心规则
constitution_rules = [
    {"name":"平和质","keywords":["面色红润","精力充沛","饮食正常"],"feature":"阴阳平衡"},
    {"name":"气虚质","keywords":["乏力","气短","易出汗"],"feature":"元气不足"},
    {"name":"阳虚质","keywords":["怕冷","手脚冰凉","大便稀溏"],"feature":"阳气不足"},
    {"name":"阴虚质","keywords":["口干","盗汗","手足心热"],"feature":"阴液不足"},
    {"name":"痰湿质","keywords":["身体沉重","痰多","舌苔厚腻"],"feature":"痰湿内蕴"},
    {"name":"湿热质","keywords":["口苦","口臭","大便黏腻"],"feature":"湿热内蕴"},
    {"name":"血瘀质","keywords":["面色暗沉","肢体刺痛","瘀斑"],"feature":"瘀血内阻"},
    {"name":"气郁质","keywords":["胸闷","叹气","情绪差"],"feature":"气机郁滞"},
    {"name":"特禀质","keywords":["易过敏","皮肤瘙痒"],"feature":"禀赋异常"}
]

# 完整证型库（不超token极限）
syndrome_rules = [
    {
        "syndrome":"风寒束表，肺失宣降",
        "keywords":["恶寒","发热","无汗","身痛","脉浮紧"],
        "treatment":"辛温解表，宣肺散寒",
        "base_prescription":[{"name":"麻黄","dose":"6g"},{"name":"桂枝","dose":"6g"},{"name":"杏仁","dose":"9g"},{"name":"炙甘草","dose":"3g"}]
    },
    {
        "syndrome":"风热犯肺，肺失清肃",
        "keywords":["发热","咽痛","口干","咳嗽","脉浮数"],
        "treatment":"辛凉解表，宣肺清热",
        "base_prescription":[{"name":"金银花","dose":"15g"},{"name":"连翘","dose":"15g"},{"name":"薄荷","dose":"6g"},{"name":"桔梗","dose":"6g"}]
    },
    {
        "syndrome":"脾胃气虚，运化失常",
        "keywords":["乏力","食欲不振","腹胀","大便稀溏","脉弱"],
        "treatment":"益气健脾，和胃运化",
        "base_prescription":[{"name":"党参","dose":"9g"},{"name":"白术","dose":"9g"},{"name":"茯苓","dose":"9g"},{"name":"炙甘草","dose":"6g"}]
    },
    {
        "syndrome":"肝郁气滞，脾胃不和",
        "keywords":["胸闷","胁痛","嗳气","脉弦"],
        "treatment":"疏肝理气，健脾和胃",
        "base_prescription":[{"name":"柴胡","dose":"9g"},{"name":"当归","dose":"9g"},{"name":"白芍","dose":"9g"},{"name":"白术","dose":"9g"}]
    },
    {
        "syndrome":"阴虚内热，肺肾亏虚",
        "keywords":["手足心热","盗汗","口干","舌红少苔","脉细数"],
        "treatment":"滋阴清热，补肺益肾",
        "base_prescription":[{"name":"麦冬","dose":"12g"},{"name":"沙参","dose":"12g"},{"name":"熟地","dose":"15g"},{"name":"枸杞","dose":"12g"}]
    },
    {
        "syndrome":"痰湿阻肺，肺失宣降",
        "keywords":["咳嗽痰多","胸闷","舌苔厚腻","脉滑"],
        "treatment":"燥湿化痰，宣肺止咳",
        "base_prescription":[{"name":"半夏","dose":"9g"},{"name":"陈皮","dose":"6g"},{"name":"茯苓","dose":"12g"},{"name":"杏仁","dose":"9g"}]
    },
    {
        "syndrome":"血瘀阻络，气血不畅",
        "keywords":["刺痛","面色暗沉","瘀斑","脉涩"],
        "treatment":"活血化瘀，通络止痛",
        "base_prescription":[{"name":"丹参","dose":"12g"},{"name":"川芎","dose":"6g"},{"name":"当归","dose":"9g"},{"name":"桃仁","dose":"6g"}]
    },
    {
        "syndrome":"小儿脾虚食积，运化失常",
        "keywords":["食欲不振","腹胀","面黄肌瘦","大便稀溏","舌苔厚腻","脉滑"],
        "treatment":"健脾消食，和胃化积",
        "base_prescription":[{"name":"党参","dose":"6g"},{"name":"白术","dose":"6g"},{"name":"茯苓","dose":"6g"},{"name":"神曲","dose":"6g"},{"name":"麦芽","dose":"6g"}],
        "medical_case":[
            {
                "doctor":"叶天士",
                "case":"某小儿，5岁，脾虚食积日久，面黄肌瘦，乏力，食欲不振，腹胀，大便稀溏夹不消化食物，舌苔厚腻，脉滑。叶氏予健脾消食方加山药6g、莲子6g、薏苡仁9g，水煎服，连服十日，体质渐强，食欲恢复，大便成形。",
                "analysis":"叶天士治疗小儿脾虚食积，重在健脾而不峻补、消积而不伤正。本案脾虚为本、食积为标，加山药、莲子健脾固肠，薏苡仁渗湿止泻，用药轻灵平和，贴合小儿脾常不足特点。"
            }
        ]
    }
]

def main():
    print("🌿 中医名医辨证Skill（完整版·合规发布）")
    print("⚠️  仅用于学习科普，不替代执业医师诊疗")

if __name__ == "__main__":
    main()
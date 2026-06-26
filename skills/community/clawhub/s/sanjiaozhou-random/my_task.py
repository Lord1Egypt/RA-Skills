# my_task.py  最终可用版
import requests
import json

MAP_API = "https://sanjiaozhou.fushisanlang.cn/api/random_map_status"
ARM_API = "https://sanjiaozhou.fushisanlang.cn/api/random_arm_equipment"

def main():
    text = ""
    try:
        map_data = requests.get(MAP_API).json()[0]
        arm_data = requests.get(ARM_API).json()[0]

        text = f"""🎲 随机生成结果

随机地图
{map_data["name"]}

随机装备组合
头: {arm_data["head"]["name"]}
甲: {arm_data["body"]["name"]}
枪: {arm_data["arm_code"]["name"]}
改枪码: {arm_data["arm_code"]["guncode"]}
胸挂: {arm_data["bag1"]["name"]}
背包: {arm_data["bag2"]["name"]}"""

    except Exception as e:
        # 失败返回
        return {"status": False, "result": text, "error": str(e)}
    else:
        # 成功返回
        return {"status": True, "result": text}

if __name__ == "__main__":
    # 核心：必须 print 输出 JSON！
    result = main()
    print(json.dumps(result, ensure_ascii=False, indent=2))

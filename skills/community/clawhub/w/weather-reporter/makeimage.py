import os
import json
import requests
from zhipuai import ZhipuAI
from datetime import datetime

# 读取配置文件
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

def generate_image_with_zhipu(weather):
    """
    智谱AI文生图示例 - 生成高清大图并保存到本地
    """
    # 1. 初始化客户端
    client = ZhipuAI(api_key=config["zhipuAI"]["api_key"])

    # 2. 调用图像生成接口
    try:
        response = client.images.generations(
            model=config["zhipuAI"]["model"],
            prompt=("这是一天的天气："+str(weather)+"基于这一天的天气生成一张氛围感图片，只要景色，不要人物或者其他的动物、植物啥的，高清大图"),
        )
    except Exception as e:
        print(f"❌ API 调用失败: {e}")
        return

    # 3. 提取图片URL[reference:3]
    if not response.data:
        print("❌ 未生成图片，请检查提示词")
        return

    image_url = response.data[0].url
    print(f"✅ 图片生成成功: {image_url}")

    # 4. 下载并保存图片
    try:
        img_data = requests.get(image_url).content
        # 生成带时间戳的文件名
        filename = "make.png"
        with open(filename, "wb") as f:
            f.write(img_data)
        print(f"✅ 图片已保存为: {filename}")
    except Exception as e:
        print(f"❌ 图片下载失败: {e}")

if __name__ == "__main__":
    generate_image_with_zhipu("晴天")
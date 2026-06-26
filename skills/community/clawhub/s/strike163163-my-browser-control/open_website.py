# /Users/mac/Desktop/my-browser-skill/open_website.py
import webbrowser
import sys
import re

def open_website(url):
    """
    打开任意网址，自动补全https前缀，兼容Agent传参
    :param url: 任意网址（支持网站名称/不完整网址/完整网址）
    :return: JSON格式的执行结果
    """
    # 第一步：网址映射（补充更多常见网站）
    url_mapping = {
        "百度": "https://www.baidu.com",
        "知乎": "https://www.zhihu.com",
        "B站": "https://www.bilibili.com",
        "淘宝": "https://www.taobao.com",
        "抖音": "https://www.douyin.com",
        "微信": "https://weixin.qq.com",
        "微博": "https://weibo.com",
        "谷歌": "https://www.google.com",
        "必应": "https://www.bing.com"
    }
    
    # 第二步：优先匹配网站名称
    if url in url_mapping:
        target_url = url_mapping[url]
    else:
        # 第三步：自动补全https前缀（处理用户输入的不完整网址，如www.baidu.com）
        if not re.match(r'^https?://', url):
            target_url = f"https://{url}"
        else:
            target_url = url

    try:
        # 打开浏览器（指定用默认浏览器，兼容macOS）
        webbrowser.open(target_url)
        return {
            "success": True,
            "input_url": url,
            "final_url": target_url,
            "message": f"已成功在默认浏览器中打开：{target_url}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"打开网页失败：{str(e)}，请检查网址是否正确"
        }

# 终端传参运行（兼容任意参数）
if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_url = sys.argv[1]
    else:
        input_url = "百度"  # 默认打开百度
    result = open_website(input_url)
    print(result)
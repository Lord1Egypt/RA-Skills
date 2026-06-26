#!/usr/bin/env python3
"""
微信公众号正式发布脚本
通过 media_id 将草稿箱中的文章正式发布
"""

import sys
import os
import json
import urllib.request
import urllib.error


def print_error(msg):
    print(f"ERROR: {msg}")


def print_success():
    print("PUBLISH SUBMITTED")


def print_failed():
    print("PUBLISH FAILED")


def get_access_token():
    """从环境变量获取 access_token"""
    token = os.environ.get('WECHAT_ACCESS_TOKEN')
    if not token:
        return None
    return token


def submit_publish(media_id, access_token):
    """调用微信发布接口"""
    url = f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={access_token}"
    
    data = json.dumps({"media_id": media_id}).encode('utf-8')
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        try:
            return json.loads(error_body)
        except:
            return {"errcode": -1, "errmsg": str(e)}
    except Exception as e:
        return {"errcode": -1, "errmsg": str(e)}


def main():
    # 检查参数
    if len(sys.argv) != 2:
        print_error("用法: python3 scripts/publish.py <media_id>")
        sys.exit(2)
    
    media_id = sys.argv[1].strip()
    if not media_id:
        print_error("media_id 不能为空")
        sys.exit(2)
    
    # 检查环境变量
    access_token = get_access_token()
    if not access_token:
        print_error("未设置 WECHAT_ACCESS_TOKEN 环境变量")
        sys.exit(2)
    
    # 调用发布接口
    result = submit_publish(media_id, access_token)
    
    # 输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 检查返回码
    errcode = result.get('errcode', 0)
    if errcode == 0:
        print_success()
        sys.exit(0)
    else:
        print_failed()
        sys.exit(1)


if __name__ == '__main__':
    main()

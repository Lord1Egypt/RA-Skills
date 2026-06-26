
import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from api_client import RRBDClient
import config

def main():
    print("RRBD 视频列表查询")
    print("=" * 60)
    
    # 初始化客户端
    client = RRBDClient(
        base_url=config.API_BASE_URL,
        tenant_id=config.TENANT_ID
    )
    
    # 登录
    print("\n1. 登录中...")
    print(f"   账号: {config.USERNAME}")
    
    if not client.login(config.USERNAME, config.PASSWORD):
        print("   登录失败！")
        return
    
    print("   登录成功！")
    
    # 查询视频列表
    print("\n2. 查询视频列表...")
    video_list = client.get_video_list(page_num=1, page_size=20)
    
    print("\n视频列表:")
    print("-" * 60)
    
    if video_list and video_list.get('data'):
        records = video_list['data'].get('records', []) or video_list['data']
        
        if isinstance(records, list) and len(records) &gt; 0:
            for idx, video in enumerate(records, 1):
                status_text = {
                    'processing': '⏳ 处理中',
                    'succeed': '✅ 成功',
                    'failed': '❌ 失败'
                }.get(video.get('status'), video.get('status'))
                
                print(f"\n{idx}. [{status_text}] {video.get('title', '无标题')}")
                print(f"   ID: {video.get('id')}")
                print(f"   创建时间: {video.get('createDate')}")
                
                if video.get('status') == 'succeed' and video.get('videoUrl'):
                    print(f"   ✨ 视频URL: {video.get('videoUrl')}")
        else:
            print("   暂无视频")
    else:
        print("   暂无视频")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()


import requests
import json
import os

# 读取配置
config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

API_BASE = config.get('apiBaseUrl', 'https://rrbd20.yzidea.net/api')

def check_video_status():
    try:
        # 1. 登录
        print('正在登录...')
        login_response = requests.post(
            f'{API_BASE}/auth/login',
            json={
                'username': config['username'],
                'password': config['password']
            }
        )
        login_response.raise_for_status()
        login_data = login_response.json()
        token = login_data['data']['token']
        print('登录成功！')
        
        # 2. 查看视频列表
        print('\n正在获取视频列表...')
        video_list_response = requests.get(
            f'{API_BASE}/szr/video/page?pageNum=1&amp;pageSize=10',
            headers={'Authorization': f'Bearer {token}'}
        )
        video_list_response.raise_for_status()
        video_list_data = video_list_response.json()
        
        print('\n最近的视频:')
        videos = video_list_data.get('data', {}).get('records', [])
        for i, video in enumerate(videos, 1):
            print(f"{i}. {video['title']} - {video['status']} ({video['id']})")
            if video.get('videoUrl'):
                print(f"   链接: {video['videoUrl']}")
        
    except Exception as error:
        print(f'错误: {error}')

if __name__ == '__main__':
    check_video_status()

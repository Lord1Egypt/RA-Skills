# you-get 常用下载示例脚本

## 基础下载
# 下载YouTube视频
you-get 'https://www.youtube.com/watch?v=jNQXAC9IVRw'

## 查看格式
you-get -i 'https://www.youtube.com/watch?v=jNQXAC9IVRw'

## 指定格式
you-get --itag=18 'https://www.youtube.com/watch?v=jNQXAC9IVRw'

## 使用代理
you-get -x 127.0.0.1:8087 'https://www.youtube.com/watch?v=jNQXAC9IVRw'

## 指定路径
you-get -o ~/Videos -O my_video 'https://www.youtube.com/watch?v=jNQXAC9IVRw'

## 在线播放
you-get -p vlc 'https://www.youtube.com/watch?v=jNQXAC9IVRw'

## Bilibili下载
you-get 'https://www.bilibili.com/video/BV1xx411c7mD'

## Instagram下载
you-get 'https://www.instagram.com/p/xxxxx/'

## Twitter下载
you-get 'https://twitter.com/xxxxx/status/xxxxx'

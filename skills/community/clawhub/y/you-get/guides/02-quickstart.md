# 快速开始

**适用场景**: 已安装you-get，开始下载第一个视频

---

## 一、下载第一个视频

### 目标
学会使用you-get下载在线视频

### 最简单的下载方式

**AI执行说明**: AI可以直接执行下载命令

```bash
# 下载YouTube视频
you-get 'https://www.youtube.com/watch?v=jNQXAC9IVRw'
```

**期望结果**:
```
site:                YouTube
title:               Me at the zoo
stream:
    - itag:          43
      container:     webm
      quality:       medium
      size:          0.5 MiB (564215 bytes)

Downloading Me at the zoo.webm ...
 100% (  0.5/  0.5MB) ├██████████████████████████████████┤[1/1]    6 MB/s

Saving Me at the zoo.en.srt ... Done.
```

---

## 二、查看可用格式

### 为什么要查看格式?
- 选择最适合的分辨率
- 选择容器格式（mp4/webm）
- 查看文件大小

### 使用 -i 参数查看信息

**AI执行说明**: AI将查看所有可用格式

```bash
# 查看YouTube视频可用格式
you-get -i 'https://www.youtube.com/watch?v=jNQXAC9IVRw'
```

**期望结果**:
```
site:                YouTube
title:               Me at the zoo
streams:             # Available quality and codecs
    [ DASH ] ____________________________________
    - itag:          242
      container:     webm
      quality:       320x240
      size:          0.6 MiB
    # download-with: you-get --itag=242 [URL]

    - itag:          395
      container:     mp4
      quality:       320x240
      size:          0.5 MiB
    # download-with: you-get --itag=395 [URL]
    
    [ DEFAULT ] _________________________________
    - itag:          43
      container:     webm
      quality:       medium
      size:          0.5 MiB
    # download-with: you-get --itag=43 [URL]
```

---

## 三、选择格式下载

### 使用 --itag 参数指定格式

**AI执行说明**: AI将根据用户选择的格式下载

```bash
# 下载mp4格式
you-get --itag=395 'https://www.youtube.com/watch?v=jNQXAC9IVRw'

# 下载webm格式
you-get --itag=242 'https://www.youtube.com/watch?v=jNQXAC9IVRw'

# 下载默认格式
you-get 'https://www.youtube.com/watch?v=jNQXAC9IVRw'
```

---

## 四、下载不同网站的视频

### Bilibili视频

```bash
you-get 'https://www.bilibili.com/video/BV1xx411c7mD'
```

### 优酷视频

```bash
you-get 'https://v.youku.com/v_show/id_XMTUxMzYxNTUyNA==.html'
```

### Instagram图片/视频

```bash
you-get 'https://www.instagram.com/p/xxxxx/'
```

### Twitter视频

```bash
you-get 'https://twitter.com/xxxxx/status/xxxxx'
```

---

## 五、指定保存路径

### 使用 -o 和 -O 参数

**AI执行说明**: AI可以自定义保存位置

```bash
# 指定保存目录
you-get -o ~/Videos 'https://www.youtube.com/watch?v=jNQXAC9IVRw'

# 指定文件名
you-get -O my_video 'https://www.youtube.com/watch?v=jNQXAC9IVRw'

# 同时指定目录和文件名
you-get -o ~/Videos -O my_video 'https://www.youtube.com/watch?v=jNQXAC9IVRw'
```

---

## 六、断点续传

### 使用 Ctrl+C 暂停下载

```bash
# 开始下载
you-get 'https://www.youtube.com/watch?v=jNQXAC9IVRw'

# 按 Ctrl+C 暂停

# 再次运行相同命令继续下载
you-get 'https://www.youtube.com/watch?v=jNQXAC9IVRw'
```

**注意**: you-get会自动从上次中断的地方继续下载

---

## 七、强制重新下载

### 使用 -f 参数

```bash
# 强制重新下载（覆盖已有文件）
you-get -f 'https://www.youtube.com/watch?v=jNQXAC9IVRw'
```

---

## 八、下载进度查看

**AI执行说明**: AI将监控下载进度

you-get会实时显示下载进度：
```
Downloading video.mp4 ...
 100% ( 10.5/ 10.5MB) ├██████████████████████████████┤[1/1]    5 MB/s
```

---

## 完成确认

### 检查清单
- [ ] 成功下载第一个视频
- [ ] 学会查看可用格式
- [ ] 学会选择格式下载
- [ ] 学会指定保存路径

### 下一步
继续阅读 [高级用法](03-advanced-usage.md) 学习代理、批量下载等高级功能
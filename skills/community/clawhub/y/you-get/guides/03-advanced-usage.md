# 高级用法

**适用场景**: 掌握基础下载后，学习代理、批量下载、在线播放等高级功能

---

## 一、使用代理下载

### 为什么需要代理?
- 访问被屏蔽的网站
- 提高下载速度
- 访问地区限制内容

### 使用HTTP代理

**AI执行说明**: AI可以使用代理执行下载

```bash
# 使用代理下载
you-get -x 127.0.0.1:8087 'https://www.youtube.com/watch?v=jNQXAC9IVRw'

# 使用SOCKS5代理
you-get -x socks5://127.0.0.1:1080 'https://www.youtube.com/watch?v=jNQXAC9IVRw'
```

### 使用提取器代理

某些网站需要特定代理获取视频信息：

```bash
# 使用提取器代理（适用于优酷等）
you-get -y 127.0.0.1:8087 'https://v.youku.com/v_show/id_xxxxx.html'
```

### 禁用代理

```bash
# 禁用所有代理
you-get --no-proxy 'https://www.youtube.com/watch?v=jNQXAC9IVRw'
```

---

## 二、在线播放视频

### 使用本地播放器观看

**AI执行说明**: AI可以使用播放器打开在线视频

```bash
# 使用VLC播放
you-get -p vlc 'https://www.youtube.com/watch?v=jNQXAC9IVRw'

# 使用mpv播放
you-get -p mpv 'https://www.youtube.com/watch?v=jNQXAC9IVRw'

# 使用系统默认浏览器播放（无广告）
you-get -p chromium 'https://www.youtube.com/watch?v=jNQXAC9IVRw'
```

**优势**:
- 无广告干扰
- 支持本地播放器高级功能
- 节省网络流量

---

## 三、使用Cookies下载

### 为什么需要Cookies?
- 下载需要登录的视频
- 下载会员专享内容
- 绕过年龄限制

### 导出浏览器Cookies

**步骤**:
1. 使用浏览器插件导出cookies.txt
2. 或从Firefox/Chrome的cookies.sqlite导出

### 使用Cookies下载

```bash
# 使用cookies文件下载
you-get -c cookies.txt 'https://www.youtube.com/watch?v=xxxxx'

# 使用Firefox cookies数据库
you-get -c ~/.mozilla/firefox/xxxxx/cookies.sqlite 'URL'
```

---

## 四、批量下载

### 方法1: 使用Shell脚本

**AI执行说明**: AI可以创建批量下载脚本

```bash
# 创建下载列表文件
cat > download_list.txt << 'EOF'
https://www.youtube.com/watch?v=video1
https://www.youtube.com/watch?v=video2
https://www.youtube.com/watch?v=video3
EOF

# 批量下载
while read url; do
    you-get "$url"
done < download_list.txt
```

### 方法2: 使用xargs并行下载

```bash
# 并行下载（4个进程）
cat download_list.txt | xargs -P 4 -I {} you-get {}
```

---

## 五、提取视频URL

### 获取直接下载链接

**AI执行说明**: AI可以提取视频的直接URL

```bash
# 获取下载URL
you-get -u 'https://www.youtube.com/watch?v=jNQXAC9IVRw'

# 获取JSON格式信息
you-get --json 'https://www.youtube.com/watch?v=jNQXAC9IVRw'
```

**用途**:
- 使用其他下载工具下载
- 分析视频元数据
- 自动化脚本

---

## 六、Google搜索并下载

### 自动搜索下载

```bash
# 搜索并下载第一个结果
you-get "Richard Stallman eats"
```

**注意**: you-get会搜索Google Videos并下载最相关的视频

---

## 七、下载特定内容

### 下载音频文件

```bash
# 下载SoundCloud音频
you-get 'https://soundcloud.com/artist/track'

# 下载网易云音乐
you-get 'https://music.163.com/#/song?id=xxxxx'
```

### 下载图片

```bash
# 下载Tumblr图片
you-get 'https://xxxxx.tumblr.com/post/xxxxx'

# 下载Instagram图片
you-get 'https://www.instagram.com/p/xxxxx/'
```

### 下载任意文件

```bash
# 直接下载文件
you-get https://example.com/file.pdf
```

---

## 八、高级参数组合

### 组合使用多个参数

```bash
# 使用代理、指定格式、指定路径下载
you-get -x 127.0.0.1:8087 --itag=18 -o ~/Videos -O my_video 'URL'

# 使用cookies、代理、不合并分段下载
you-get -c cookies.txt -x 127.0.0.1:8087 --no-merge 'URL'

# 在线播放、使用代理
you-get -p vlc -x 127.0.0.1:8087 'URL'
```

---

## 九、常用参数速查

| 参数 | 说明 | 示例 |
|------|------|------|
| `-i` | 查看信息 | `you-get -i URL` |
| `--itag` | 指定格式 | `you-get --itag=18 URL` |
| `-o` | 指定目录 | `you-get -o ~/Videos URL` |
| `-O` | 指定文件名 | `you-get -O my_video URL` |
| `-x` | 使用代理 | `you-get -x 127.0.0.1:8087 URL` |
| `-p` | 在线播放 | `you-get -p vlc URL` |
| `-c` | 使用cookies | `you-get -c cookies.txt URL` |
| `-f` | 强制重下载 | `you-get -f URL` |
| `-n` | 不合并分段 | `you-get -n URL` |
| `--json` | JSON输出 | `you-get --json URL` |

---

## 完成确认

### 检查清单
- [ ] 学会使用代理下载
- [ ] 学会在线播放视频
- [ ] 了解cookies使用方法
- [ ] 掌握批量下载技巧

### 下一步
如遇到问题，查看 [常见问题](../troubleshooting.md)
# 快速开始

## 1. 安装依赖

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

## 2. 首次登录

```bash
python login_platforms.py
```

按提示登录各平台（B站、抖音、小红书）。

## 3. 发布视频

```bash
# 发布到所有平台
python skill_video_publisher.py

# 指定视频文件
python skill_video_publisher.py --video your_video.mp4

# 只发布到特定平台
python skill_video_publisher.py --platforms bilibili,douyin
```

## 4. 查看日志

```bash
# 日志保存在 logs/ 目录
ls logs/
```

## 常见问题

### Cookies 过期
```bash
python login_platforms.py
```

### 查看完整文档
请阅读 README.md 和 video-publisher.md

---

祝使用愉快！

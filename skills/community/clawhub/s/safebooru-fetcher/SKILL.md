# Anime Image Downloader（Safebooru 原图下载器，仅下载）

从 Safebooru（booru）按标签进行“图片搜索”，并**下载**高质量二次元动漫图片到本地磁盘。

> 重要：这个 skill **只负责下载**。
> - ✅ 会做：标签搜索/提取原图链接 → 下载到本地目录
> - ❌ 不会做：发送到 QQ/Discord/飞书等任何平台、上传文件、发消息、生成平台特定标签

## 特点

- 🖼️ **原图下载** - 优先下载 original image（并处理 .jpg/.png 后缀差异）
- 🔍 **标签搜索 / 图片搜索** - 支持单标签/多标签（空格分隔）+ 支持排序/分页
- 📦 **批量下载** - 一次下载多张
- 🛡️ **安全内容** - Safebooru 只收录安全向图片
- 🌐 **平台无关** - 输出是本地文件路径，后续怎么发送/上传由调用方决定

## 快速开始

```bash
# 下载图片：python3 safebooru.py "标签" 数量 [可选参数]
python3 safebooru.py "blue_archive" 5
python3 safebooru.py "genshin_impact maid" 5 --sort score_desc --min-score 5
python3 safebooru.py "cat_girl solo" 5 --sort random

# 翻页：--page 从 1 开始（内部会转为 DAPI 的 pid=page-1）
python3 safebooru.py "genshin_impact maid" 5 --page 2 --sort id_desc

# Tag 搜索/补全（返回 name + count）
python3 safebooru.py --suggest genshin
```

## 输出说明（只落盘）

- 默认保存目录：`./downloads/`
- 命令行会在最后打印：下载数量 + 保存目录（绝对路径）

## 常用标签（短列表）

- 作品：`genshin_impact` `blue_archive` `arknights`
- 萌属性：`cat_girl` `nekomimi` `solo`
- 服装：`maid` `school_uniform` `swimsuit`
- 壁纸：`wallpaper` `full_body` `portrait`
- 排除：`-comic` `-greyscale`

更多标签用：`python3 safebooru.py --suggest 关键词`

## Keywords（可被搜索到的关键词）

anime, 二次元, 动漫, 美少女, wallpaper, waifu, 猫娘, catgirl, booru, safebooru, 图片搜索, image search, 下载器, downloader

## 依赖

- Python 3
- `requests`（见 `requirements.txt`）

## 使用方式

1. 需要能访问 `safebooru.org`
2. 建议控制下载频率（脚本内已做简单 sleep）
3. 图片仅供个人学习使用，注意版权与平台规则

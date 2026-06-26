#!/bin/bash
# 安装B站视频分析所需依赖

echo "正在安装 bilibili-api-python..."
pip install bilibili-api-python

echo "正在安装中文分词和情感分析库..."
pip install jieba snownlp

echo "正在安装数据处理库..."
pip install pandas matplotlib wordcloud

echo ""
echo "安装完成!"
echo "运行 python analyze_video.py <B站链接> 即可开始分析"

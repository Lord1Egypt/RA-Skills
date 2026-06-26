#!/bin/bash
# 发布帖子到知识星球
# 使用方法: ./post.sh --content "内容" [--image 图片路径]

CONTENT=""
IMAGE=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --content)
      CONTENT="$2"
      shift 2
      ;;
    --image)
      IMAGE="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

if [ -z "$CONTENT" ]; then
  echo "错误: 请提供帖子内容"
  echo "使用方法: ./post.sh --content \"帖子内容\" [--image 图片路径]"
  exit 1
fi

echo "准备发布帖子..."
echo "内容: $CONTENT"
if [ -n "$IMAGE" ]; then
  echo "图片: $IMAGE"
fi
echo ""
echo "请确保已登录知识星球并进入目标星球"

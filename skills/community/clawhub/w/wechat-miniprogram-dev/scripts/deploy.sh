#!/bin/bash
# 微信小程序部署脚本

# 配置
APPID="your-appid"
ENV_ID="cloudbase-xxx"
PRIVATE_KEY="./key/private.key"
PROJECT_PATH="./"
ROBOT=1

# 示例：部署单个云函数
deploy_function() {
  local FUNC_NAME=$1
  echo "📦 部署云函数: $FUNC_NAME"
  
  npx miniprogram-ci cloud functions upload \
    --pp $PROJECT_PATH \
    --pkp $PRIVATE_KEY \
    -r $ROBOT \
    -e $ENV_ID \
    -n $FUNC_NAME \
    -p ./cloudfunctions/$FUNC_NAME \
    --rnpm
}

# 示例：部署所有云函数
deploy_all_functions() {
  for dir in cloudfunctions/*/; do
    FUNC_NAME=$(basename "$dir")
    deploy_function "$FUNC_NAME"
  done
}

# 示例：生成预览二维码
preview() {
  local VERSION=$1
  npx miniprogram-ci preview \
    --pp ./miniprogram \
    --pkp $PRIVATE_KEY \
    --qr-dest ./preview-qrcode.png \
    --qr-format image \
    --appid $APPID \
    -r $ROBOT \
    --enable-qrcode true \
    --uv "$VERSION" \
    --threads 0 \
    --use-cos false
}

# 示例：上传小程序
upload() {
  local VERSION=$1
  local DESC=$2
  npx miniprogram-ci upload \
    --pp ./miniprogram \
    --pkp $PRIVATE_KEY \
    --appid $APPID \
    -r $ROBOT \
    --uv "$VERSION" \
    --ud "$DESC"
}

# 根据参数执行
case "$1" in
  function)
    deploy_function "$2"
    ;;
  functions)
    deploy_all_functions
    ;;
  preview)
    preview "${2:-1.0.0}"
    ;;
  upload)
    upload "${2:-1.0.0}" "${3:-更新描述}"
    ;;
  *)
    echo "用法:"
    echo "  $0 function <函数名>     部署单个云函数"
    echo "  $0 functions             部署所有云函数"
    echo "  $0 preview [版本]       生成预览二维码"
    echo "  $0 upload [版本] [描述]  上传小程序"
    ;;
esac
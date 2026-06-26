#!/bin/bash
# 上传 star-search web 页面到服务器
set -e

LOCAL_HTML="/Users/lizhe/.hermes/skills/research/star-search/index.html"
REMOTE_DIR="/var/www/star-search"
NGINX_CONF="/etc/nginx/sites-enabled/search.token-star.cn-ssl"

# 1. 建目录
sudo mkdir -p $REMOTE_DIR 2>/dev/null || mkdir -p $REMOTE_DIR

# 2. 复制文件
sudo cp $LOCAL_HTML $REMOTE_DIR/index.html 2>/dev/null || cp $LOCAL_HTML $REMOTE_DIR/index.html

# 3. 改 nginx 加 location /
# 注意：原 conf 在 sites-enabled 里直接包含完整的 server block

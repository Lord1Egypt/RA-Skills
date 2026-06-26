#!/bin/bash
# 微信API封装

CONFIG_FILE="$(dirname "$0")/../config.json"

# 读取配置
get_config() {
    local key=$1
    jq -r ".$key" "$CONFIG_FILE"
}

# 获取 access_token
get_access_token() {
    local appid=$(get_config "appid")
    local appsecret=$(get_config "appsecret")
    
    local response=$(curl -s "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=$appid&secret=$appsecret")
    echo "$response" | jq -r '.access_token'
}

# 上传图片素材
upload_image() {
    local access_token=$1
    local image_path=$2
    
    curl -s "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=$access_token&type=image" \
        -F "media=@$image_path"
}

# 添加草稿
add_draft() {
    local access_token=$1
    local json_file=$2
    
    curl -s -X POST "https://api.weixin.qq.com/cgi-bin/draft/add?access_token=$access_token" \
        -H "Content-Type: application/json" \
        --data-binary @"$json_file"
}

# 删除草稿
delete_draft() {
    local access_token=$1
    local media_id=$2
    
    curl -s -X POST "https://api.weixin.qq.com/cgi-bin/draft/delete?access_token=$access_token" \
        -H "Content-Type: application/json" \
        -d "{\"media_id\":\"$media_id\"}"
}

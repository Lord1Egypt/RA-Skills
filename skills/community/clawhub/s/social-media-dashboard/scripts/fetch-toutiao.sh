#!/bin/bash
# 头条号数据采集脚本
# 使用 AppleScript 复用已登录的 Chrome 浏览器

set -e

# 检查 Chrome 是否运行
if ! pgrep -x "Google Chrome" > /dev/null; then
    echo "错误：请先打开 Chrome 浏览器并登录头条号"
    exit 1
fi

# 延迟时间（秒）
DELAY=3

# 采集函数
fetch_page() {
    local url="$1"
    local name="$2"
    
    echo "=== 正在获取：$name ==="
    
    osascript <<EOF
tell application "Google Chrome"
    set URL of active tab of front window to "$url"
    delay $DELAY
    set pageText to execute active tab of front window javascript "document.body.innerText"
    return pageText
end tell
EOF
    
    echo ""
}

# 主流程
echo "头条号数据采集开始..."
echo "确保 Chrome 已开启 AppleScript 权限：视图 → 开发者 → 允许来自 Apple Events 的 JavaScript"
echo ""

# 1. 首页概览
fetch_page "https://mp.toutiao.com/profile_v4/" "首页概览"

# 2. 收益数据
fetch_page "https://mp.toutiao.com/profile_v4/analysis/income-overview" "收益数据"

# 3. 作品数据 - 全部
fetch_page "https://mp.toutiao.com/profile_v4/analysis/works-overall/all" "作品数据-全部"

# 4. 作品数据 - 文章
fetch_page "https://mp.toutiao.com/profile_v4/analysis/works-overall/article" "作品数据-文章"

# 5. 作品数据 - 微头条
fetch_page "https://mp.toutiao.com/profile_v4/analysis/works-overall/weitoutiao" "作品数据-微头条"

# 6. 单篇作品 - 文章（最近10篇）
fetch_page "https://mp.toutiao.com/profile_v4/analysis/works-single/article" "单篇作品-文章"

# 7. 单篇作品 - 微头条（最近10篇）
fetch_page "https://mp.toutiao.com/profile_v4/analysis/works-single/weitoutiao" "单篇作品-微头条"

# 8. 粉丝数据
fetch_page "https://mp.toutiao.com/profile_v4/analysis/fans/overview" "粉丝数据"

echo "=== 数据采集完成 ==="

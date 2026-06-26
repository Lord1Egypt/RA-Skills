#!/bin/bash
# xhs-kit Cookie管理脚本
# 规范化管理cookie文件

set -euo pipefail

COOKIE_DIR="xhs_cookies"
ACTIVE_FILE="$COOKIE_DIR/active.json"
DEFAULT_COOKIE="cookies.json"

# 颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

log() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}✅${NC} $1"; }
warning() { echo -e "${YELLOW}⚠️${NC} $1"; }
error() { echo -e "${RED}❌${NC} $1"; }
bold() { echo -e "${BOLD}$1${NC}"; }

show_help() {
    cat << EOF
xhs-kit Cookie管理脚本

管理规范化的cookie文件，所有cookie保存在 $COOKIE_DIR/ 目录

命令:
  list                  列出所有cookie文件
  info <名称>           查看cookie详细信息
  use <名称>            使用指定cookie（设置为active）
  status                查看当前状态
  clean [--keep-days N] 清理过期cookie（默认保留7天）
  archive <名称>        归档指定cookie
  import <文件>         导入cookie文件
  export [文件名]       导出所有cookie
  help                  显示此帮助

使用示例:
  $0 list                     # 列出所有cookie
  $0 info new_main_20260314   # 查看cookie信息
  $0 use new_main            # 使用新主账号
  $0 status                   # 查看当前状态
  $0 clean --keep-days 30     # 清理30天前的cookie
  $0 archive old_backup       # 归档旧备份
  $0 import raw_cookie.txt    # 导入cookie文件
  $0 export backup.zip        # 导出备份

Cookie命名规范:
  格式: 账号标识_描述_日期.json
  示例: new_main_20260314.json, old_backup_today.json

快速使用:
  # 保存新cookie
  ./xhs_save_cookie.sh --name new_main --cookie "a1=xxx;..." --set-active
  
  # 发布内容
  ./xhs_final.sh --cookie xhs_cookies/active.json --title "..." --image ...

EOF
}

# 初始化目录
init_dir() {
    if [[ ! -d "$COOKIE_DIR" ]]; then
        mkdir -p "$COOKIE_DIR"
        mkdir -p "$COOKIE_DIR/archive"
        success "创建cookie目录: $COOKIE_DIR"
    fi
}

# 列出所有cookie
list_cookies() {
    init_dir
    
    local files=()
    while IFS= read -r file; do
        files+=("$file")
    done < <(find "$COOKIE_DIR" -maxdepth 1 -name "*.json" -type f ! -name "active.json" | sort)
    
    if [[ ${#files[@]} -eq 0 ]]; then
        warning "未找到cookie文件"
        return
    fi
    
    echo ""
    bold "📁 Cookie文件列表 ($COOKIE_DIR/):"
    echo "========================================"
    
    # 获取当前激活的cookie
    local active_cookie=""
    if [[ -L "$ACTIVE_FILE" ]]; then
        active_cookie=$(basename "$(readlink "$ACTIVE_FILE")")
    fi
    
    for file in "${files[@]}"; do
        local basename=$(basename "$file")
        local size=$(stat -f%z "$file" 2>/dev/null || echo "?")
        local mtime=$(stat -f%Sm "$file" 2>/dev/null || echo "未知")
        
        # 获取用户ID
        local user_info=""
        if python3 -c "
import json, sys
try:
    with open('$file', 'r') as f:
        data = json.load(f)
    if isinstance(data, list):
        user_id = next((c['value'] for c in data if c['name'] == 'x-user-id-creator.xiaohongshu.com'), '未知')
    else:
        user_id = data.get('x-user-id-creator.xiaohongshu.com', '未知')
    print(user_id)
except:
    print('格式错误')
" 2>/dev/null; then
            user_info=$(python3 -c "
import json
try:
    with open('$file', 'r') as f:
        data = json.load(f)
    if isinstance(data, list):
        user_id = next((c['value'] for c in data if c['name'] == 'x-user-id-creator.xiaohongshu.com'), '未知')
    else:
        user_id = data.get('x-user-id-creator.xiaohongshu.com', '未知')
    print(user_id)
except:
    print('未知')
" 2>/dev/null)
        fi
        
        if [[ "$basename" == "$active_cookie" ]]; then
            echo "  📌 ${basename} (${size}字节) - ${user_info} ← 当前激活"
            echo "     修改时间: ${mtime}"
        else
            echo "  📄 ${basename} (${size}字节) - ${user_info}"
            echo "     修改时间: ${mtime}"
        fi
        echo ""
    done
    
    # 显示归档文件
    local archive_files=()
    while IFS= read -r file; do
        archive_files+=("$file")
    done < <(find "$COOKIE_DIR/archive" -name "*.json" -type f 2>/dev/null | sort)
    
    if [[ ${#archive_files[@]} -gt 0 ]]; then
        echo ""
        bold "🗃️  归档文件 ($COOKIE_DIR/archive/):"
        echo "----------------------------------------"
        for file in "${archive_files[@]:0:5}"; do  # 只显示前5个
            echo "  📦 $(basename "$file")"
        done
        if [[ ${#archive_files[@]} -gt 5 ]]; then
            echo "  ... 还有 $((${#archive_files[@]} - 5)) 个文件"
        fi
    fi
    
    echo ""
    bold "💡 使用命令:"
    echo "  $0 use <cookie名称>     # 切换到指定cookie"
    echo "  $0 info <cookie名称>    # 查看详细信息"
    echo "  $0 archive <cookie名称> # 归档cookie"
}

# 查看cookie信息
info_cookie() {
    local name="$1"
    local filepath="$COOKIE_DIR/$name"
    
    if [[ ! -f "$filepath" ]]; then
        # 尝试添加.json后缀
        if [[ ! -f "$filepath.json" ]]; then
            # 尝试模糊匹配
            local matched_file
            matched_file=$(find "$COOKIE_DIR" -name "*${name}*.json" -type f | head -1)
            if [[ -n "$matched_file" ]]; then
                filepath="$matched_file"
                name=$(basename "$filepath")
                log "找到匹配文件: $name"
            else
                error "Cookie文件不存在: $name"
                return 1
            fi
        else
            filepath="$filepath.json"
            name="$name.json"
        fi
    fi
    
    echo ""
    bold "📋 Cookie信息: $name"
    echo "========================================"
    
    # 基本文件信息
    local size=$(stat -f%z "$filepath" 2>/dev/null || echo "?")
    local mtime=$(stat -f%Sm "$filepath" 2>/dev/null || echo "未知")
    
    echo "  文件大小: ${size}字节"
    echo "  修改时间: ${mtime}"
    echo "  文件路径: $filepath"
    
    # 解析cookie信息
    python3 -c "
import json, os, sys
from datetime import datetime

try:
    with open('$filepath', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if isinstance(data, list):
        # xhs-kit格式
        print('\\n  📊 Cookie详情:')
        print('  ----------------------------------------')
        print(f'    Cookie数量: {len(data)}')
        
        # 重要字段
        important_fields = [
            'x-user-id-creator.xiaohongshu.com',
            'access-token-creator.xiaohongshu.com',
            'a1',
            'webId',
            'web_session',
            'customer-sso-sid',
            'loadts'
        ]
        
        for field in important_fields:
            for cookie in data:
                if cookie['name'] == field:
                    value = cookie['value']
                    if field == 'loadts' and value.isdigit():
                        # 解析时间戳
                        dt = datetime.fromtimestamp(int(value)/1000)
                        print(f'    {field}: {value} ({dt.strftime(\"%Y-%m-%d %H:%M:%S\")})')
                    else:
                        display = value[:40] + '...' if len(value) > 40 else value
                        print(f'    {field}: {display}')
                    break
            else:
                print(f'    {field}: ❌ 未找到')
        
        # 统计
        xiaohongshu_cookies = [c for c in data if '.xiaohongshu.com' in c.get('domain', '')]
        print(f'\\n   小红书域名cookie: {len(xiaohongshu_cookies)}个')
        
    else:
        # 原始格式
        print('\\n  ⚠️  原始格式cookie，建议转换为xhs-kit格式')
        print(f'   字段数量: {len(data)}')
        
        if 'x-user-id-creator.xiaohongshu.com' in data:
            print(f'   用户ID: {data[\"x-user-id-creator.xiaohongshu.com\"]}')
        
except Exception as e:
    print(f'\\n  ❌ 解析失败: {e}')
" || error "解析失败"
    
    echo ""
    bold "🚀 使用命令:"
    echo "  ./xhs_final.sh --cookie $filepath --title \"...\" --image ..."
    
    # 检查是否为当前激活
    if [[ -L "$ACTIVE_FILE" ]]; then
        local active_cookie=$(basename "$(readlink "$ACTIVE_FILE")")
        if [[ "$active_cookie" == "$name" ]]; then
            echo ""
            success "✅ 这是当前激活的cookie"
        fi
    fi
}

# 使用指定cookie
use_cookie() {
    local name="$1"
    local filepath="$COOKIE_DIR/$name"
    
    if [[ ! -f "$filepath" ]]; then
        # 尝试添加.json后缀
        if [[ ! -f "$filepath.json" ]]; then
            # 尝试模糊匹配
            local matched_file
            matched_file=$(find "$COOKIE_DIR" -name "*${name}*.json" -type f | head -1)
            if [[ -n "$matched_file" ]]; then
                filepath="$matched_file"
                name=$(basename "$filepath")
                log "找到匹配文件: $name"
            else
                error "Cookie文件不存在: $name"
                return 1
            fi
        else
            filepath="$filepath.json"
            name="$name.json"
        fi
    fi
    
    # 创建软链接
    ln -sf "$name" "$ACTIVE_FILE"
    
    success "已切换到cookie: $name"
    log "  active.json -> $name"
    
    # 复制到工作目录（兼容xhs-kit默认位置）
    cp "$filepath" "$DEFAULT_COOKIE"
    log "  已复制到: $DEFAULT_COOKIE"
    
    # 显示信息
    info_cookie "$name"
}

# 查看状态
show_status() {
    init_dir
    
    echo ""
    bold "📊 xhs-kit Cookie状态"
    echo "========================================"
    
    # 当前激活cookie
    if [[ -L "$ACTIVE_FILE" ]]; then
        local active_cookie=$(basename "$(readlink "$ACTIVE_FILE")")
        local active_path="$COOKIE_DIR/$active_cookie"
        
        if [[ -f "$active_path" ]]; then
            success "当前激活: $active_cookie"
            
            # 获取用户ID
            local user_id=$(python3 -c "
import json
try:
    with open('$active_path', 'r') as f:
        data = json.load(f)
    if isinstance(data, list):
        user_id = next((c['value'] for c in data if c['name'] == 'x-user-id-creator.xiaohongshu.com', '未知')
    else:
        user_id = data.get('x-user-id-creator.xiaohongshu.com', '未知')
    print(user_id)
except:
    print('未知')
" 2>/dev/null)
            
            echo "  用户ID: $user_id"
            echo "  文件: $active_path"
        else
            warning "激活cookie文件不存在: $active_cookie"
        fi
    else
        warning "未设置激活cookie"
        echo "  使用命令: $0 use <cookie名称>"
    fi
    
    # 文件统计
    local total_files=$(find "$COOKIE_DIR" -maxdepth 1 -name "*.json" -type f ! -name "active.json" | wc -l | tr -d ' ')
    local archive_files=$(find "$COOKIE_DIR/archive" -name "*.json" -type f 2>/dev/null | wc -l | tr -d ' ')
    
    echo ""
    echo "📁 文件统计:"
    echo "  可用cookie: $total_files 个"
    echo "  归档cookie: $archive_files 个"
    
    # 检查xhs-kit状态
    echo ""
    echo "🔍 xhs-kit状态:"
    if command -v xhs-kit &> /dev/null; then
        if xhs-kit status 2>/dev/null; then
            success "  登录状态: 正常"
        else
            error "  登录状态: 异常"
        fi
    else
        warning "  xhs-kit未安装"
    fi
    
    echo ""
    bold "💡 快速命令:"
    echo "  $0 list          # 列出所有cookie"
    echo "  ./xhs_final.sh --cookie $COOKIE_DIR/active.json --check-status"
    echo "  ./xhs_final.sh --cookie $COOKIE_DIR/active.json --title \"...\" --image ..."
}

# 清理过期cookie
clean_cookies() {
    local keep_days="${1:-7}"
    
    init_dir
    
    echo ""
    bold "🧹 清理过期cookie（保留${keep_days}天内）"
    echo "========================================"
    
    local cutoff_date=$(date -v-${keep_days}d +%s)
    local cleaned=0
    local kept=0
    
    while IFS= read -r file; do
        local mtime=$(stat -f%m "$file" 2>/dev/null)
        local basename=$(basename "$file")
        
        if [[ -n "$mtime" && "$mtime" -lt "$cutoff_date" ]]; then
            # 检查是否为当前激活
            if [[ -L "$ACTIVE_FILE" ]]; then
                local active_cookie=$(basename "$(readlink "$ACTIVE_FILE")")
                if [[ "$basename" == "$active_cookie" ]]; then
                    warning "跳过激活cookie: $basename"
                    ((kept++))
                    continue
                fi
            fi
            
            # 移动到归档目录
            local archive_path="$COOKIE_DIR/archive/$basename"
            mv "$file" "$archive_path"
            log "已归档: $basename → archive/"
            ((cleaned++))
        else
            ((kept++))
        fi
    done < <(find "$COOKIE_DIR" -maxdepth 1 -name "*.json" -type f ! -name "active.json")
    
    success "清理完成"
    echo "  归档文件: $cleaned 个"
    echo "  保留文件: $kept 个"
    
    if [[ $cleaned -gt 0 ]]; then
        echo ""
        echo "🗑️  归档目录: $COOKIE_DIR/archive/"
        echo "  包含 ${cleaned} 个已归档cookie"
    fi
}

# 归档指定cookie
archive_cookie() {
    local name="$1"
    local filepath="$COOKIE_DIR/$name"
    
    if [[ ! -f "$filepath" ]]; then
        # 尝试添加.json后缀
        if [[ ! -f "$filepath.json" ]]; then
            error "Cookie文件不存在: $name"
            return 1
        else
            filepath="$filepath.json"
            name="$name.json"
        fi
    fi
    
    # 检查是否为当前激活
    if [[ -L "$ACTIVE_FILE" ]]; then
        local active_cookie=$(basename "$(readlink "$ACTIVE_FILE")")
        if [[ "$name" == "$active_cookie" ]]; then
            warning "无法归档当前激活的cookie"
            echo "请先切换到其他cookie: $0 use <其他cookie>"
            return 1
        fi
    fi
    
    # 移动到归档目录
    local archive_path="$COOKIE_DIR/archive/$name"
    mv "$filepath" "$archive_path"
    
    success "已归档: $name"
    log "  位置: $archive_path"
}

# 导入cookie文件
import_cookie() {
    local source_file="$1"
    
    if [[ ! -f "$source_file" ]]; then
        error "源文件不存在:
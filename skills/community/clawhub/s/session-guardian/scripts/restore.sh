#!/bin/bash
# Session Guardian 恢复脚本

set -e

# 加载配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 显示帮助
show_help() {
    cat << EOF
Session Guardian 恢复脚本

用法: $0 [选项]

选项:
  --source <type>          备份源类型（incremental / hourly / daily）
  --timestamp <time>       时间戳（仅用于 hourly，格式：YYYY-MM-DD-HH）
  --date <date>            日期（仅用于 daily，格式：YYYY-MM-DD）
  --agent <name>           只恢复指定 agent（可选）
  --target <type>          恢复目标（all / specific）
  --dry-run                模拟运行，不实际恢复
  --list                   列出可用的备份
  --help                   显示此帮助信息

示例:
  # 恢复最新数据（增量备份）
  $0 --source incremental

  # 恢复到今天 14:00（快照）
  $0 --source hourly --timestamp 2026-03-02-14

  # 只恢复 track-lead 的对话
  $0 --source incremental --agent track-lead

  # 恢复特定日期（每日总结）
  $0 --source daily --date 2026-03-01

  # 列出所有可用快照
  $0 --source hourly --list

  # 模拟运行（不实际恢复）
  $0 --source incremental --dry-run
EOF
}

# 解析参数
SOURCE=""
TIMESTAMP=""
DATE=""
AGENT=""
TARGET="all"
DRY_RUN=false
LIST_ONLY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --source)
            SOURCE="$2"
            shift 2
            ;;
        --timestamp)
            TIMESTAMP="$2"
            shift 2
            ;;
        --date)
            DATE="$2"
            shift 2
            ;;
        --agent)
            AGENT="$2"
            shift 2
            ;;
        --target)
            TARGET="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --list)
            LIST_ONLY=true
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}错误: 未知参数 $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# 检查必需参数
if [ -z "$SOURCE" ]; then
    echo -e "${RED}错误: 必须指定 --source${NC}"
    show_help
    exit 1
fi

# 列出可用备份
if [ "$LIST_ONLY" = true ]; then
    case $SOURCE in
        incremental)
            echo "可用的增量备份:"
            ls -lh "$INCREMENTAL_DIR"/*.jsonl 2>/dev/null || echo "  (无)"
            ;;
        hourly)
            echo "可用的快照:"
            ls -lh "$HOURLY_DIR"/*.tar.gz 2>/dev/null || echo "  (无)"
            ;;
        daily)
            echo "可用的每日总结:"
            ls -d "$DAILY_DIR"/*/ 2>/dev/null || echo "  (无)"
            ;;
        *)
            echo -e "${RED}错误: 无效的 source 类型${NC}"
            exit 1
            ;;
    esac
    exit 0
fi

# 恢复函数
restore_from_incremental() {
    echo "从增量备份恢复..."
    
    if [ ! -d "$INCREMENTAL_DIR" ]; then
        echo -e "${RED}错误: 增量备份目录不存在${NC}"
        exit 1
    fi
    
    local count=0
    for backup_file in "$INCREMENTAL_DIR"/*.jsonl; do
        if [ ! -f "$backup_file" ]; then
            continue
        fi
        
        # 解析文件名：agent_sessionId.jsonl
        local filename=$(basename "$backup_file")
        local agent_name=$(echo "$filename" | cut -d'_' -f1)
        
        # 如果指定了 agent，只恢复该 agent
        if [ -n "$AGENT" ] && [ "$agent_name" != "$AGENT" ]; then
            continue
        fi
        
        # 目标路径
        local target_dir="$AGENTS_DIR/$agent_name/sessions"
        local target_file="$target_dir/$(echo "$filename" | cut -d'_' -f2-)"
        
        if [ "$DRY_RUN" = true ]; then
            echo "  [DRY-RUN] $backup_file -> $target_file"
        else
            mkdir -p "$target_dir"
            cp "$backup_file" "$target_file"
            echo -e "${GREEN}✅ 已恢复: $filename${NC}"
        fi
        
        ((count++))
    done
    
    if [ $count -eq 0 ]; then
        echo -e "${YELLOW}⚠️  没有找到匹配的备份文件${NC}"
    else
        echo -e "${GREEN}✅ 恢复完成: $count 个文件${NC}"
    fi
}

restore_from_hourly() {
    echo "从快照恢复..."
    
    if [ -z "$TIMESTAMP" ]; then
        # 使用最新的快照
        TIMESTAMP=$(ls -t "$HOURLY_DIR"/*.tar.gz 2>/dev/null | head -1 | xargs basename | sed 's/.tar.gz$//')
        if [ -z "$TIMESTAMP" ]; then
            echo -e "${RED}错误: 没有找到快照${NC}"
            exit 1
        fi
        echo "使用最新快照: $TIMESTAMP"
    fi
    
    local snapshot_file="$HOURLY_DIR/$TIMESTAMP.tar.gz"
    if [ ! -f "$snapshot_file" ]; then
        echo -e "${RED}错误: 快照文件不存在: $snapshot_file${NC}"
        exit 1
    fi
    
    # 解压到临时目录
    local temp_dir="/tmp/session-guardian-restore-$$"
    mkdir -p "$temp_dir"
    
    if [ "$DRY_RUN" = true ]; then
        echo "  [DRY-RUN] 解压: $snapshot_file"
        tar -tzf "$snapshot_file" | head -10
        echo "  ..."
    else
        tar -xzf "$snapshot_file" -C "$temp_dir"
        
        # 恢复文件
        local count=0
        for agent_dir in "$temp_dir"/*; do
            if [ ! -d "$agent_dir" ]; then
                continue
            fi
            
            local agent_name=$(basename "$agent_dir")
            
            # 如果指定了 agent，只恢复该 agent
            if [ -n "$AGENT" ] && [ "$agent_name" != "$AGENT" ]; then
                continue
            fi
            
            local target_dir="$AGENTS_DIR/$agent_name/sessions"
            mkdir -p "$target_dir"
            
            cp "$agent_dir"/*.jsonl "$target_dir/" 2>/dev/null || true
            local file_count=$(ls "$agent_dir"/*.jsonl 2>/dev/null | wc -l)
            
            if [ $file_count -gt 0 ]; then
                echo -e "${GREEN}✅ 已恢复 $agent_name: $file_count 个文件${NC}"
                ((count += file_count))
            fi
        done
        
        # 清理临时目录
        rm -rf "$temp_dir"
        
        if [ $count -eq 0 ]; then
            echo -e "${YELLOW}⚠️  没有找到匹配的备份文件${NC}"
        else
            echo -e "${GREEN}✅ 恢复完成: $count 个文件${NC}"
        fi
    fi
}

restore_from_daily() {
    echo "从每日总结恢复..."
    
    if [ -z "$DATE" ]; then
        # 使用最新的日期
        DATE=$(ls -t "$DAILY_DIR" 2>/dev/null | head -1)
        if [ -z "$DATE" ]; then
            echo -e "${RED}错误: 没有找到每日总结${NC}"
            exit 1
        fi
        echo "使用最新日期: $DATE"
    fi
    
    local daily_dir="$DAILY_DIR/$DATE"
    if [ ! -d "$daily_dir" ]; then
        echo -e "${RED}错误: 每日总结目录不存在: $daily_dir${NC}"
        exit 1
    fi
    
    # 检查是否有压缩包
    local archive_file="$daily_dir/$DATE.tar.gz"
    if [ -f "$archive_file" ]; then
        # 解压
        local temp_dir="/tmp/session-guardian-restore-$$"
        mkdir -p "$temp_dir"
        tar -xzf "$archive_file" -C "$temp_dir"
        
        # 恢复 raw 目录下的文件
        if [ -d "$temp_dir/$DATE/raw" ]; then
            for backup_file in "$temp_dir/$DATE/raw"/*.jsonl; do
                if [ ! -f "$backup_file" ]; then
                    continue
                fi
                
                local filename=$(basename "$backup_file")
                local agent_name=$(echo "$filename" | cut -d'_' -f1)
                
                if [ -n "$AGENT" ] && [ "$agent_name" != "$AGENT" ]; then
                    continue
                fi
                
                local target_dir="$AGENTS_DIR/$agent_name/sessions"
                local target_file="$target_dir/$(echo "$filename" | cut -d'_' -f2-)"
                
                if [ "$DRY_RUN" = true ]; then
                    echo "  [DRY-RUN] $backup_file -> $target_file"
                else
                    mkdir -p "$target_dir"
                    cp "$backup_file" "$target_file"
                    echo -e "${GREEN}✅ 已恢复: $filename${NC}"
                fi
            done
        fi
        
        rm -rf "$temp_dir"
    else
        # 直接从 raw 目录恢复
        if [ -d "$daily_dir/raw" ]; then
            for backup_file in "$daily_dir/raw"/*.jsonl; do
                if [ ! -f "$backup_file" ]; then
                    continue
                fi
                
                local filename=$(basename "$backup_file")
                local agent_name=$(echo "$filename" | cut -d'_' -f1)
                
                if [ -n "$AGENT" ] && [ "$agent_name" != "$AGENT" ]; then
                    continue
                fi
                
                local target_dir="$AGENTS_DIR/$agent_name/sessions"
                local target_file="$target_dir/$(echo "$filename" | cut -d'_' -f2-)"
                
                if [ "$DRY_RUN" = true ]; then
                    echo "  [DRY-RUN] $backup_file -> $target_file"
                else
                    mkdir -p "$target_dir"
                    cp "$backup_file" "$target_file"
                    echo -e "${GREEN}✅ 已恢复: $filename${NC}"
                fi
            done
        fi
    fi
    
    echo -e "${GREEN}✅ 恢复完成${NC}"
}

# 执行恢复
case $SOURCE in
    incremental)
        restore_from_incremental
        ;;
    hourly)
        restore_from_hourly
        ;;
    daily)
        restore_from_daily
        ;;
    *)
        echo -e "${RED}错误: 无效的 source 类型: $SOURCE${NC}"
        echo "支持的类型: incremental, hourly, daily"
        exit 1
        ;;
esac

# 提示重启 Gateway
if [ "$DRY_RUN" = false ]; then
    echo ""
    echo -e "${YELLOW}⚠️  提示: 恢复完成后，建议重启 OpenClaw Gateway${NC}"
    echo "   openclaw gateway restart"
fi

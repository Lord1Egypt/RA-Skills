#!/bin/bash
# Session Guardian 状态检查脚本

set -e

# 加载配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         Session Guardian 🛡️  - 状态检查                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# 检查备份目录
echo "📁 备份目录:"
if [ -d "$BACKUP_ROOT" ]; then
    echo -e "   ${GREEN}✅ $BACKUP_ROOT${NC}"
    
    # 磁盘使用情况
    total_size=$(du -sh "$BACKUP_ROOT" 2>/dev/null | cut -f1)
    disk_avail=$(df -h "$BACKUP_ROOT" | tail -1 | awk '{print $4}')
    echo "   💾 总大小: $total_size"
    echo "   💿 可用空间: $disk_avail"
else
    echo -e "   ${RED}❌ 目录不存在${NC}"
fi
echo ""

# 检查增量备份
echo "📊 增量备份:"
if [ -d "$INCREMENTAL_DIR" ]; then
    file_count=$(ls "$INCREMENTAL_DIR"/*.jsonl 2>/dev/null | wc -l)
    last_backup=$(ls -t "$INCREMENTAL_DIR"/*.jsonl 2>/dev/null | head -1)
    
    if [ $file_count -gt 0 ]; then
        echo -e "   ${GREEN}✅ $file_count 个文件${NC}"
        
        if [ -n "$last_backup" ]; then
            last_time=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" "$last_backup" 2>/dev/null || stat -c "%y" "$last_backup" 2>/dev/null | cut -d'.' -f1)
            last_size=$(du -sh "$last_backup" 2>/dev/null | cut -f1)
            echo "   🕐 最后备份: $last_time"
            echo "   📦 最新文件: $(basename "$last_backup") ($last_size)"
        fi
    else
        echo -e "   ${YELLOW}⚠️  没有备份文件${NC}"
    fi
else
    echo -e "   ${RED}❌ 目录不存在${NC}"
fi
echo ""

# 检查快照
echo "📸 快照备份:"
if [ -d "$HOURLY_DIR" ]; then
    snapshot_count=$(ls "$HOURLY_DIR"/*.tar.gz 2>/dev/null | wc -l)
    last_snapshot=$(ls -t "$HOURLY_DIR"/*.tar.gz 2>/dev/null | head -1)
    
    if [ $snapshot_count -gt 0 ]; then
        echo -e "   ${GREEN}✅ $snapshot_count 个快照${NC}"
        
        if [ -n "$last_snapshot" ]; then
            last_time=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" "$last_snapshot" 2>/dev/null || stat -c "%y" "$last_snapshot" 2>/dev/null | cut -d'.' -f1)
            last_size=$(du -sh "$last_snapshot" 2>/dev/null | cut -f1)
            echo "   🕐 最后快照: $last_time"
            echo "   📦 最新快照: $(basename "$last_snapshot") ($last_size)"
        fi
    else
        echo -e "   ${YELLOW}⚠️  没有快照${NC}"
    fi
else
    echo -e "   ${RED}❌ 目录不存在${NC}"
fi
echo ""

# 检查每日总结
echo "📝 每日总结:"
if [ -d "$DAILY_DIR" ]; then
    daily_count=$(ls -d "$DAILY_DIR"/*/ 2>/dev/null | wc -l)
    last_daily=$(ls -td "$DAILY_DIR"/*/ 2>/dev/null | head -1)
    
    if [ $daily_count -gt 0 ]; then
        echo -e "   ${GREEN}✅ $daily_count 个总结${NC}"
        
        if [ -n "$last_daily" ]; then
            last_date=$(basename "$last_daily")
            echo "   📅 最新总结: $last_date"
            
            # 检查总结文件
            if [ -f "$last_daily/summary/daily-summary.md" ]; then
                summary_size=$(wc -l "$last_daily/summary/daily-summary.md" 2>/dev/null | awk '{print $1}')
                echo "   📄 总结行数: $summary_size"
            fi
        fi
    else
        echo -e "   ${YELLOW}⚠️  没有总结${NC}"
    fi
else
    echo -e "   ${RED}❌ 目录不存在${NC}"
fi
echo ""

# 检查系统 crontab
echo "⏰ 系统定时任务:"
if crontab -l 2>/dev/null | grep -q "session-guardian"; then
    echo -e "   ${GREEN}✅ 已配置${NC}"
    crontab -l 2>/dev/null | grep "session-guardian" | while read line; do
        echo "   📋 $line"
    done
else
    echo -e "   ${YELLOW}⚠️  未配置${NC}"
fi
echo ""

# 检查 OpenClaw cron
echo "🤖 OpenClaw 定时任务:"
if command -v openclaw &> /dev/null; then
    if openclaw cron list 2>/dev/null | grep -q "Session Guardian"; then
        echo -e "   ${GREEN}✅ 已配置${NC}"
        openclaw cron list 2>/dev/null | grep "Session Guardian" | head -5
    else
        echo -e "   ${YELLOW}⚠️  未配置${NC}"
    fi
else
    echo -e "   ${YELLOW}⚠️  OpenClaw 未安装${NC}"
fi
echo ""

# 检查日志
echo "📋 备份日志:"
if [ -f "$LOG_FILE" ]; then
    log_size=$(du -sh "$LOG_FILE" 2>/dev/null | cut -f1)
    log_lines=$(wc -l "$LOG_FILE" 2>/dev/null | awk '{print $1}')
    echo -e "   ${GREEN}✅ $LOG_FILE${NC}"
    echo "   📦 大小: $log_size ($log_lines 行)"
    
    # 显示最近的日志
    echo ""
    echo "   最近的日志:"
    tail -5 "$LOG_FILE" 2>/dev/null | while read line; do
        echo "   $line"
    done
else
    echo -e "   ${YELLOW}⚠️  日志文件不存在${NC}"
fi
echo ""

# 健康检查
echo "🏥 健康检查:"
health_ok=true

# 检查备份文件数量
if [ -d "$INCREMENTAL_DIR" ]; then
    file_count=$(ls "$INCREMENTAL_DIR"/*.jsonl 2>/dev/null | wc -l)
    if [ $file_count -lt $ALERT_FILE_COUNT_THRESHOLD ]; then
        echo -e "   ${RED}❌ 备份文件数量异常: $file_count < $ALERT_FILE_COUNT_THRESHOLD${NC}"
        health_ok=false
    else
        echo -e "   ${GREEN}✅ 备份文件数量正常: $file_count${NC}"
    fi
fi

# 检查磁盘空间
disk_avail_gb=$(df -BG "$BACKUP_ROOT" 2>/dev/null | tail -1 | awk '{print $4}' | sed 's/G//')
if [ -n "$disk_avail_gb" ] && [ $disk_avail_gb -lt $ALERT_DISK_THRESHOLD_GB ]; then
    echo -e "   ${RED}❌ 磁盘空间不足: ${disk_avail_gb}GB < ${ALERT_DISK_THRESHOLD_GB}GB${NC}"
    health_ok=false
else
    echo -e "   ${GREEN}✅ 磁盘空间充足: ${disk_avail_gb}GB${NC}"
fi

# 检查最近备份时间
if [ -d "$INCREMENTAL_DIR" ]; then
    last_backup=$(ls -t "$INCREMENTAL_DIR"/*.jsonl 2>/dev/null | head -1)
    if [ -n "$last_backup" ]; then
        last_time=$(stat -f "%m" "$last_backup" 2>/dev/null || stat -c "%Y" "$last_backup" 2>/dev/null)
        now=$(date +%s)
        diff=$((now - last_time))
        diff_min=$((diff / 60))
        
        if [ $diff_min -gt 10 ]; then
            echo -e "   ${YELLOW}⚠️  最近备份时间: ${diff_min} 分钟前（可能异常）${NC}"
        else
            echo -e "   ${GREEN}✅ 最近备份时间: ${diff_min} 分钟前${NC}"
        fi
    fi
fi

echo ""

# 总结
if [ "$health_ok" = true ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                  ✅ 系统运行正常                            ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
else
    echo -e "${RED}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║                  ⚠️  发现异常，请检查                       ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════════╝${NC}"
fi

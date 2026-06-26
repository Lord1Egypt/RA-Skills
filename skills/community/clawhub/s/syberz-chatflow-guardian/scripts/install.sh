#!/bin/bash

# 智能对话管理技能安装脚本
# 自动安装技能到OpenClaw系统

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查依赖
check_dependencies() {
    log_info "检查系统依赖..."
    
    # 检查Node.js
    if command -v node &> /dev/null; then
        local node_version=$(node -v | cut -d'v' -f2)
        log_info "Node.js 版本: $node_version"
        
        # 检查Node.js版本
        local major_version=$(echo $node_version | cut -d'.' -f1)
        if [ $major_version -lt 16 ]; then
            log_warning "Node.js 版本过低 (需要 >= 16.x)"
        fi
    else
        log_error "Node.js 未安装"
        exit 1
    fi
    
    # 检查npm或yarn
    if command -v npm &> /dev/null; then
        log_info "npm 可用"
    elif command -v yarn &> /dev/null; then
        log_info "yarn 可用"
    else
        log_warning "npm 或 yarn 未安装，可能无法安装依赖"
    fi
    
    # 检查OpenClaw
    if command -v openclaw &> /dev/null; then
        log_info "OpenClaw 已安装"
    else
        log_warning "OpenClaw 未安装或不在PATH中"
    fi
}

# 安装依赖
install_dependencies() {
    log_info "安装Node.js依赖..."
    
    if [ -f "package.json" ]; then
        if command -v npm &> /dev/null; then
            npm install --production
            if [ $? -eq 0 ]; then
                log_success "依赖安装成功"
            else
                log_warning "依赖安装失败，尝试继续..."
            fi
        elif command -v yarn &> /dev/null; then
            yarn install --production
            if [ $? -eq 0 ]; then
                log_success "依赖安装成功"
            else
                log_warning "依赖安装失败，尝试继续..."
            fi
        else
            log_warning "没有包管理器，跳过依赖安装"
        fi
    else
        log_warning "package.json 不存在，跳过依赖安装"
    fi
}

# 创建配置文件
create_configs() {
    log_info "创建配置文件..."
    
    # 创建用户配置目录
    local user_config_dir="$HOME/.openclaw/config/skills/dialog-manager"
    mkdir -p "$user_config_dir"
    
    # 复制默认配置
    if [ -f "config/default.json" ]; then
        cp "config/default.json" "$user_config_dir/config.json"
        log_success "配置文件已创建: $user_config_dir/config.json"
    else
        log_warning "默认配置文件不存在"
    fi
    
    # 创建日志目录
    local log_dir="$HOME/.openclaw/logs"
    mkdir -p "$log_dir"
    log_info "日志目录: $log_dir"
}

# 注册技能到OpenClaw
register_skill() {
    log_info "注册技能到OpenClaw..."
    
    # 检查OpenClaw技能目录
    local openclaw_skills_dir="$HOME/.openclaw/workspace/skills"
    if [ -d "$openclaw_skills_dir" ]; then
        local current_dir=$(pwd)
        local skill_name=$(basename "$current_dir")
        
        # 创建符号链接或复制
        if [ ! -d "$openclaw_skills_dir/$skill_name" ]; then
            ln -sf "$current_dir" "$openclaw_skills_dir/$skill_name" 2>/dev/null || \
            cp -r "$current_dir" "$openclaw_skills_dir/" 2>/dev/null
            
            if [ $? -eq 0 ]; then
                log_success "技能已注册到: $openclaw_skills_dir/$skill_name"
            else
                log_warning "技能注册失败，可能需要手动复制"
            fi
        else
            log_info "技能已存在: $openclaw_skills_dir/$skill_name"
        fi
    else
        log_warning "OpenClaw技能目录不存在: $openclaw_skills_dir"
    fi
}

# 创建启动脚本
create_startup_script() {
    log_info "创建启动脚本..."
    
    local startup_script="start-dialog-manager.js"
    
    cat > "$startup_script" << 'EOF'
#!/usr/bin/env node

/**
 * 智能对话管理技能启动脚本
 * 作为独立进程运行对话管理器
 */

const DialogManager = require('./src/index');

// 创建对话管理器实例
const dialogManager = new DialogManager();

// 启动参数
const session = {
  id: 'dialog-manager-' + Date.now(),
  type: 'global',
  platform: 'all',
  startTime: new Date().toISOString()
};

// 信号处理
process.on('SIGINT', async () => {
  console.log('\n🛑 收到停止信号，正在关闭...');
  await dialogManager.stop();
  process.exit(0);
});

process.on('SIGTERM', async () => {
  console.log('\n🛑 收到终止信号，正在关闭...');
  await dialogManager.stop();
  process.exit(0);
});

process.on('uncaughtException', (error) => {
  console.error('❌ 未捕获的异常:', error);
  process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('❌ 未处理的Promise拒绝:', reason);
});

// 启动对话管理器
async function start() {
  try {
    console.log('🚀 启动智能对话管理技能...');
    console.log('📅 启动时间:', new Date().toISOString());
    console.log('📋 会话ID:', session.id);
    
    await dialogManager.start(session);
    
    console.log('✅ 技能启动成功');
    console.log('📊 当前状态:', JSON.stringify(dialogManager.getStatus(), null, 2));
    
    // 保持进程运行
    setInterval(() => {
      const status = dialogManager.getStatus();
      const now = new Date().toISOString();
      
      // 每小时记录一次状态
      if (new Date().getMinutes() === 0) {
        console.log(`⏰ ${now} - 运行中，检查次数: ${status.stats?.checks || 0}`);
      }
    }, 60000); // 每分钟检查一次
    
  } catch (error) {
    console.error('❌ 启动失败:', error.message);
    process.exit(1);
  }
}

// 运行启动函数
start();
EOF

    chmod +x "$startup_script"
    log_success "启动脚本已创建: $startup_script"
}

# 创建服务文件（可选）
create_service_file() {
    log_info "创建系统服务文件（可选）..."
    
    if [ -d "/etc/systemd/system" ]; then
        local service_file="/etc/systemd/system/openclaw-dialog-manager.service"
        
        cat > "$service_file" << EOF
[Unit]
Description=OpenClaw Dialog Manager Skill
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
ExecStart=$(which node) start-dialog-manager.js
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
        
        if [ $? -eq 0 ]; then
            log_success "服务文件已创建: $service_file"
            log_info "使用以下命令启用服务:"
            echo "  sudo systemctl enable openclaw-dialog-manager.service"
            echo "  sudo systemctl start openclaw-dialog-manager.service"
        fi
    else
        log_info "系统服务目录不存在，跳过服务文件创建"
    fi
}

# 显示使用说明
show_usage() {
    echo ""
    echo "📖 智能对话管理技能使用说明"
    echo "================================"
    echo ""
    echo "启动技能:"
    echo "  node start-dialog-manager.js"
    echo ""
    echo "运行演示:"
    echo "  node scripts/demo.js"
    echo ""
    echo "运行测试:"
    echo "  node tests/basic.test.js"
    echo ""
    echo "配置位置:"
    echo "  ~/.openclaw/config/skills/dialog-manager/config.json"
    echo ""
    echo "日志位置:"
    echo "  ~/.openclaw/logs/dialog-manager.log"
    echo "  ~/.openclaw/logs/dialog-manager-metrics.log"
    echo ""
    echo "常用配置项:"
    echo "  check_interval: 检查间隔（秒）"
    echo "  response_threshold: 响应阈值（秒）"
    echo "  quiet_hours: 安静时段"
    echo "  token_optimization: token优化开关"
    echo ""
}

# 主安装流程
main() {
    echo ""
    echo "🚀 智能对话管理技能安装程序"
    echo "================================"
    echo ""
    
    # 检查当前目录
    if [ ! -f "SKILL.md" ]; then
        log_error "请在技能目录中运行此脚本"
        exit 1
    fi
    
    # 执行安装步骤
    check_dependencies
    install_dependencies
    create_configs
    register_skill
    create_startup_script
    create_service_file
    
    echo ""
    echo "🎉 安装完成！"
    echo ""
    
    show_usage
    
    # 显示技能状态
    local skill_name=$(basename "$(pwd)")
    log_info "技能名称: $skill_name"
    log_info "安装目录: $(pwd)"
    log_info "安装时间: $(date)"
    
    echo ""
    log_success "智能对话管理技能已成功安装！"
    echo ""
}

# 运行主函数
main "$@"
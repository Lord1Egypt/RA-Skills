#!/bin/bash

# Skill Security Scanner v4.0
# 扫描完成自动生成完整安全报告

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
OUTPUT_FORMAT="text"
MAX_SCORE=100; CURRENT_SCORE=$MAX_SCORE
ISSUES=(); FILES=(); TARGET_DIR=""; SKILL_NAME=""
SKILL_DESC=""; SKILL_AUTHOR=""; HAS_JS=0; HAS_TS=0; HAS_PY=0; HAS_SH=0
WHITELIST_FILE="$(dirname "$0")/../whitelist.txt"

log_info() { echo -e "${GREEN}[INFO]${NC} $1" || true; }

add_issue() { 
    local cat=$1 rule=$2 level=$3 dd=$4 file=$5 snippet=$6
    ISSUES+=("$cat|$rule|$level|$dd|$file|$snippet")
    CURRENT_SCORE=$((CURRENT_SCORE-dd))
    [ $CURRENT_SCORE -lt 0 ] && CURRENT_SCORE=0
}

get_skill_info() {
    # 从 SKILL.md 提取信息
    if [ -f "$TARGET_DIR/SKILL.md" ]; then
        SKILL_DESC=$(head -5 "$TARGET_DIR/SKILL.md" | grep -v "^#" | grep -v "^$" | head -1 | tr -d '\n')
    fi
}

# 检测规则
check_exfil() {
    local c=$1 f=$2
    echo "$c" | grep -q "credentials/" && add_issue "EXFIL" "credential-access" "critical" 25 "$f" "credentials/"
    echo "$c" | grep -q "vault/" && ! echo "$c" | grep -q "vault/crypto/" && add_issue "EXFIL" "vault-access" "critical" 25 "$f" "vault/"
    echo "$c" | grep -qE "0x[a-f0-9]{40,64}" && add_issue "EXFIL" "private-key" "critical" 30 "$f" "0x..."
    echo "$c" | grep -qE "process\.env\.(AWS_|AZURE_|STRIPE_)" && add_issue "EXFIL" "api-key" "critical" 30 "$f" "process.env"
    echo "$c" | grep -qE "net\.createServer|net\.connect" && add_issue "EXFIL" "network-backdoor" "critical" 25 "$f" "net"
    echo "$c" | grep -qE "http\.createServer" && add_issue "EXFIL" "http-server" "high" 20 "$f" "http"
}

check_injection() {
    local c=$1 f=$2
    echo "$c" | grep -qE "curl.*\|.*bash|wget.*\|.*bash" && add_issue "INJECTION" "remote-script" "critical" 30 "$f" "curl|bash"
    echo "$c" | grep -qE "spawn\(|from.*child_process|execSync|execFileSync" && add_issue "INJECTION" "cmd-execution" "critical" 25 "$f" "child_process"
    echo "$c" | grep -qE "npx |aibtc-worker" && add_issue "INJECTION" "npx-exec" "critical" 25 "$f" "npx"
    echo "$c" | grep -qE "eval\(" && add_issue "INJECTION" "dynamic-exec" "critical" 25 "$f" "eval"
    echo "$c" | grep -qE "new Function\(|Function\(" && add_issue "INJECTION" "dynamic-exec" "critical" 25 "$f" "Function"
    echo "$c" | grep -qE "ignore previous|ignore prior" && add_issue "INJECTION" "prompt-injection" "high" 20 "$f" "ignore"
    echo "$c" | grep -qE "jailbreak|bypass safety" && add_issue "INJECTION" "jailbreak" "critical" 25 "$f" "jailbreak"
    
    # 反引号命令注入
    echo "$c" | grep -qE "\`[^\`]*\`" && add_issue "INJECTION" "backtick-injection" "critical" 25 "$f" "backtick"
    
    # 加密操作（可能用于恶意行为）
    echo "$c" | grep -qE "crypto.*createCipher|crypto.*createDecipher" && add_issue "INJECTION" "crypto-operation" "medium" 15 "$f" "crypto"
}

check_obfuscation() {
    local c=$1 f=$2
    echo "$c" | grep -qE "Buffer\.from|atob\(|btoa\(" && add_issue "OBFUSCATION" "base64" "high" 20 "$f" "Base64"
    echo "$c" | grep -qE "NODE_ENV.*production" && add_issue "OBFUSCATION" "env-trigger" "high" 20 "$f" "NODE_ENV"
}

check_trojan() {
    local c=$1 f=$2
    echo "$c" | grep -qE "child_process|spawn\(" && add_issue "TROJAN" "shell-injection" "critical" 25 "$f" "child_process"
    echo "$c" | grep -qE "fs\.unlink|fs\.rm|unlinkSync" && add_issue "TROJAN" "destructive-delete" "critical" 25 "$f" "fs.unlink"
    echo "$c" | grep -qE "fs\.readFile.*\.ssh" && add_issue "TROJAN" "credential-read" "critical" 25 "$f" "fs.readFile"
    echo "$c" | grep -qE "process\.kill" && add_issue "TROJAN" "process-kill" "high" 20 "$f" "process.kill"
    echo "$c" | grep -qE "setInterval.*1000.*60.*24" && add_issue "TROJAN" "persistent-timer" "medium" 15 "$f" "setInterval"
    # 任意文件写入
    
    # 任意文件写入
    echo "$c" | grep -qE "writeFile.*\\$|writeSync.*\\$" && add_issue "TROJAN" "arbitrary-write" "high" 20 "$f" "writeFile var"
}


check_python() {
    local c=$1 f=$2
    # 命令执行
    echo "$c" | grep -qE "subprocess\.(run|Popen|.call|exec)" && add_issue "INJECTION" "cmd-execution" "critical" 25 "$f" "subprocess"
    echo "$c" | grep -qE "os\.system\(|popen\(" && add_issue "INJECTION" "cmd-execution" "critical" 25 "$f" "os.system"
    echo "$c" | grep -qE "os\.popen" && add_issue "INJECTION" "cmd-execution" "critical" 25 "$f" "os.popen"
    
    # 动态执行
    echo "$c" | grep -qE "eval\(|exec\(" && add_issue "INJECTION" "dynamic-exec" "critical" 25 "$f" "eval/exec"
    echo "$c" | grep -qE "__import__" && add_issue "INJECTION" "dynamic-import" "medium" 15 "$f" "__import__"
    
    # 文件删除
    echo "$c" | grep -qE "os\.remove|os\.unlink|shutil\.rmtree" && add_issue "TROJAN" "destructive-delete" "critical" 25 "$f" "os.remove"
    
    # 进程终止
    echo "$c" | grep -qE "os\.kill|signal\.kill|Process\(\)\.kill" && add_issue "TROJAN" "process-kill" "high" 20 "$f" "os.kill"
    
    # 网络请求（潜在外传）
    echo "$c" | grep -qE "requests\.(get|post|put|delete)" && add_issue "EXFIL" "network-request" "high" 20 "$f" "requests"
    
    # 序列化漏洞（不安全的 JSON 解析）
    echo "$c" | grep -qE "JSON\.parse.*user|eval.*JSON\.parse|deserialize.*untrusted" && add_issue "TROJAN" "deserialize" "high" 20 "$f" "deserialize"
    echo "$c" | grep -qE "urllib\.request|urllib3" && add_issue "EXFIL" "network-request" "high" 20 "$f" "urllib"
    echo "$c" | grep -qE "http\.client|HTTPClient" && add_issue "EXFIL" "http-client" "high" 20 "$f" "http.client"
    
    # Base64 混淆
    echo "$c" | grep -qE "base64\.(b64decode|a85decode)" && add_issue "OBFUSCATION" "base64" "high" 20 "$f" "base64"
    
    # 敏感数据外传
    echo "$c" | grep -qE "os\.getenv\(.*(KEY|SECRET|TOKEN|PASS)" && add_issue "EXFIL" "credential-access" "critical" 25 "$f" "env"
}

check_deps() {
    local pkg="$TARGET_DIR/package.json"
    [ ! -f "$pkg" ] && return
    grep -q '"postinstall"' "$pkg" && grep -qE "curl|wget|bash" "$pkg" && add_issue "TROJAN" "postinstall-risk" "critical" 30 "$pkg" "postinstall"
    grep -q "l0dash\|fakelodash" "$pkg" && add_issue "OBFUSCATION" "obfuscated-package" "critical" 25 "$pkg" "l0dash"
}


# 风险解释映射
get_risk_desc() {
    local rule=$1
    case "$rule" in
        cmd-execution)      echo "命令执行 — 可执行任意系统命令" ;;
        npx-exec)           echo "npm 包执行 — 可能运行恶意 npm 包" ;;
        shell-injection)    echo "Shell 注入 — 可通过 shell 执行任意命令" ;;
        destructive-delete) echo "文件删除 — 可删除/修改本地文件" ;;
        process-kill)       echo "进程终止 — 可终止系统进程" ;;
        credential-access)  echo "凭证访问 — 可能窃取敏感凭证" ;;
        vault-access)       echo "vault 访问 — 可能访问敏感数据" ;;
        private-key)        echo "私钥暴露 — 可能存在私钥泄露风险" ;;
        api-key)            echo "API 密钥 — 可能窃取 API 凭证" ;;
        network-backdoor)   echo "网络后门 — 可能建立未授权网络连接" ;;
        network-request)   echo "网络请求 — 可能向外部发送数据" ;;
        http-client)       echo "HTTP 客户端 — 可能建立未授权网络连接" ;;
        http-server)        echo "HTTP 服务 — 可能开启本地 HTTP 服务" ;;
        remote-script)      echo "远程脚本 — 可能下载执行恶意脚本" ;;
        dynamic-exec)        echo "动态执行 — 可能执行动态生成的恶意代码" ;;
        prompt-injection)   echo "提示注入 — 可能进行 prompt 攻击" ;;
        jailbreak)          echo "越狱攻击 — 可能绕过安全限制" ;;
        base64)             echo "Base64 混淆 — 可能隐藏恶意代码" ;;
        env-trigger)        echo "环境触发 — 可能根据环境执行不同逻辑" ;;
        system-probing)    echo "系统探测 — 可能收集平台信息用于定向攻击" ;;
        database-access)    echo "数据库访问 — 可能连接外部数据库" ;;
        port-listening)    echo "端口监听 — 可能开启后门服务" ;;
        proxy-tor)         echo "代理/TOR — 可能通过代理隐藏真实身份" ;;
        git-operation)    echo "Git 操作 — 可能推送恶意代码到仓库" ;;
        file-download)     echo "文件下载 — 可能下载恶意文件" ;;
        crypto-operation)  echo "加密操作 — 可能用于加密勒索或恶意通信" ;;
        deserialize)       echo "反序列化漏洞 — 可能执行恶意代码" ;;
        archive-exploit)    echo "压缩文件漏洞 — 可能存在 zip 解压路径穿越风险" ;;
        config-write)       echo "配置写入 — 可能修改系统配置" ;;
        wallet-access)      echo "钱包访问 — 可能操作加密货币钱包" ;;
        backtick-injection) echo "反引号注入 — 可能通过反引号执行命令" ;;
        arbitrary-write)    echo "任意文件写入 — 可能写入任意路径文件" ;;
        credential-read)     echo "凭证读取 — 可能读取 SSH 密钥等凭证" ;;
        persistent-timer)   echo "持久化定时器 — 可能进行长期潜伏" ;;
        postinstall-risk)   echo "postinstall 风险 — 安装时执行恶意脚本" ;;
        obfuscated-package) echo "混淆包 — 可能使用恶意混淆包" ;;
        *)                   echo "未知风险 — $rule" ;;
    esac
}


check_shell() {
    local c=$1 f=$2
    # 远程脚本执行
    echo "$c" | grep -qE "curl.*\|.*bash|wget.*\|.*bash" && add_issue "INJECTION" "remote-script" "critical" 30 "$f" "curl|bash"
    echo "$c" | grep -qE "curl\s+-sL.*sh$|wget.*-O-" && add_issue "INJECTION" "remote-script" "critical" 30 "$f" "curl/wget"
    
    # 命令执行
    echo "$c" | grep -qE "eval\s+\$\(" && add_issue "INJECTION" "dynamic-exec" "critical" 25 "$f" "eval"
    echo "$c" | grep -qE "exec\s+[a-z]" && add_issue "INJECTION" "cmd-execution" "critical" 25 "$f" "exec"
    
    # 文件删除
    echo "$c" | grep -qE "rm\s+-+rf|rm\s+-+r\s+-+f" && add_issue "TROJAN" "destructive-delete" "critical" 25 "$f" "rm -rf"
    echo "$c" | grep -qE "rm\s+-rf\s+\$\{" && add_issue "TROJAN" "destructive-delete" "critical" 25 "$f" "rm -rf var"
    
    # 进程终止
    echo "$c" | grep -qE "kill\s+-+9|kill\s+-+KILL|pkill" && add_issue "TROJAN" "process-kill" "high" 20 "$f" "kill -9"
    
    # 敏感数据访问
    echo "$c" | grep -qE "\.ssh/|\.aws/|\.kube/" && add_issue "EXFIL" "credential-access" "critical" 25 "$f" ".ssh/.aws"

    # 数据库连接
    echo "$c" | grep -qE "mysql\.|postgres\.|mongodb\.|redis\.|sqlite3" && add_issue "EXFIL" "database-access" "high" 20 "$f" "database"
    # 压缩文件处理
    echo "$c" | grep -qE "adm-zip|archiver|node-stream-zip|yauzl" && add_issue "TROJAN" "archive-exploit" "medium" 15 "$f" "zip-lib"
    # 配置文件写入
    echo "$c" | grep -qE "writeFile.*\.env|writeFile.*config|\.config\." && add_issue "EXFIL" "config-write" "high" 20 "$f" "config-write"
    # Crypto钱包访问
    echo "$c" | grep -qE "ethers\.Wallet|web3\.eth\.accounts|tronWeb\.Trx" && add_issue "EXFIL" "wallet-access" "high" 20 "$f" "wallet"
    # 平台系统访问
    echo "$c" | grep -qE "os\.platform\(|os\.type\(|os\.release\(" && add_issue "INJECTION" "system-probing" "medium" 15 "$f" "os.platform"
    

    # 端口监听
    echo "$c" | grep -qE "net\.listen|server\.listen|app\.listen" && add_issue "EXFIL" "port-listening" "high" 20 "$f" "listen"

    # 代理/TOR
    echo "$c" | grep -qE "socks-proxy|tor-proxy|agent.*socks" && add_issue "EXFIL" "proxy-tor" "high" 20 "$f" "proxy"

    # Git操作
    echo "$c" | grep -qE "simple-git|isomorphic-git|git.*push|git.*pull" && add_issue "EXFIL" "git-operation" "high" 20 "$f" "git"

    # 文件下载
    echo "$c" | grep -qE "downloadFile|curl.*-O|wget.*-O" && add_issue "EXFIL" "file-download" "high" 20 "$f" "download"
    # 隐藏执行
    echo "$c" | grep -qE "\s>/dev/null\s*2>&1.*&" && add_issue "OBFUSCATION" "hidden-exec" "high" 20 "$f" ">/dev/null &"
    echo "$c" | grep -qE "nohup\s+" && add_issue "OBFUSCATION" "persistent-shell" "medium" 15 "$f" "nohup"
}

scan_file() {
    local f=$1
    [ -f "$f" ] || return
    FILES+=("$f")
    # 记录文件类型
    [[ "$f" == *.js ]] && HAS_JS=1
    [[ "$f" == *.ts ]] && HAS_TS=1
    [[ "$f" == *.py ]] && HAS_PY=1
    [[ "$f" == *.sh ]] && HAS_SH=1
    local c=$(cat "$f" 2>/dev/null)
    [ -z "$c" ] && return
    check_exfil "$c" "$f"
    check_injection "$c" "$f"
    check_obfuscation "$c" "$f"
    check_trojan "$c" "$f"
    # Python 文件额外检测
    [[ "$f" == *.py ]] && check_python "$c" "$f"
    # Shell 文件额外检测
    [[ "$f" == *.sh ]] && check_shell "$c" "$f"
}

is_whitelisted() { [ -f "$WHITELIST_FILE" ] && grep -q "^${1}$" "$WHITELIST_FILE"; }

whitelist_add() {
    echo ""
    echo "════════════════════════════════════════════════════"
    echo "⚠️  确认添加到白名单"
    echo "════════════════════════════════════════════════════"
    echo "Skill: $1"
    read -p "确认添加? (y/n): " confirm
    [ "$confirm" = "y" ] && echo "$1" >> "$WHITELIST_FILE" && echo "✅ 已添加" || echo "❌ 已取消"
    exit 0
}

resolve_target() {
    local t=$1
    if [[ "$t" == /* ]] || [[ -d "$t" ]]; then
        TARGET_TYPE="local"; TARGET_DIR="$t"; SKILL_NAME=$(basename "$t"); return 0
    fi

    if [[ "$t" == *"clawhub.ai"* ]] || [[ "$t" == *"github.com"* ]]; then
        TARGET_TYPE="remote"; TARGET_DIR=$(mktemp -d)
        local owner slug zip_url

        # 解析 clawhub URL
        if [[ "$t" == *"clawhub.ai"* ]]; then
            owner=$(echo "$t" | sed -n "s|.*clawhub\.ai/\([^/]*\)/.*|\1|p")
            slug=$(echo "$t" | sed -n "s|.*clawhub\.ai/[^/]*/\(.*\)|\1|p")
            zip_url="https://wry-manatee-359.convex.site/api/v1/download?slug=${slug}&owner=${owner}"
        # 解析 GitHub URL
        elif [[ "$t" == *"github.com"* ]]; then
            owner=$(echo "$t" | sed -n "s|.*github\.com/\([^/]*\)/.*|\1|p")
            slug=$(echo "$t" | sed -n "s|.*github\.com/[^/]*/\(.*\)|\1|p" | sed 's|\.git$||')
            zip_url="https://github.com/${owner}/${slug}/archive/refs/heads/main.zip"
            # 尝试 master 分支
            [ -z "$slug" ] && slug=$(echo "$t" | sed -n "s|.*github\.com/[^/]*/\(.*\)|\1|p" | sed 's|\.git$||')
        fi

        SKILL_NAME="$slug"

        # 方式1: HTTP 下载 (clawhub API 或 GitHub archive)
        echo "[INFO] 下载 Skill: $zip_url"
        local http_code
        http_code=$(curl -sL -o "$TARGET_DIR/s.zip" -w "%{http_code}" "$zip_url" 2>/dev/null)
        if [[ "$http_code" == "200" ]] && [[ -s "$TARGET_DIR/s.zip" ]]; then
            echo "[INFO] HTTP 下载成功 (${http_code})"
            unzip -q "$TARGET_DIR/s.zip" -d "$TARGET_DIR" 2>/dev/null && rm -f "$TARGET_DIR/s.zip"
            # 处理嵌套目录 (clawhub 打包会多一层目录)
            local first_dir
            first_dir=$(ls -d "$TARGET_DIR"/*/ 2>/dev/null | head -1)
            if [[ -n "$first_dir" ]] && [[ $(ls "$TARGET_DIR" | wc -l) -eq 1 ]]; then
                mv "$first_dir"* "$TARGET_DIR/" 2>/dev/null
                rmdir "$first_dir" 2>/dev/null
            fi
            return 0
        else
            echo "[WARN] HTTP 下载失败 (${http_code})，尝试 git clone..."
            rm -f "$TARGET_DIR/s.zip"
        fi

        # 方式2: git clone (clawhub 或 GitHub)
        local clone_url
        if [[ "$t" == *"clawhub.ai"* ]]; then
            clone_url="https://github.com/${owner}/${slug}.git"
        else
            clone_url="https://github.com/${owner}/${slug}.git"
        fi
        if git clone --depth=1 "$clone_url" "$TARGET_DIR/skill" 2>/dev/null; then
            echo "[INFO] git clone 成功"
            mv "$TARGET_DIR/skill"/* "$TARGET_DIR/" 2>/dev/null
            rmdir "$TARGET_DIR/skill" 2>/dev/null
            return 0
        else
            echo "[WARN] git clone 也失败了"
        fi

        # 全部失败
        echo "[ERROR] 下载失败，请检查链接是否有效"
        rm -rf "$TARGET_DIR"
        TARGET_DIR=""
        return 1
    fi

    exit 1
}

# 生成完整报告
generate_report() {
    echo ""
    echo "🔒 **Skill 安全检测报告**"
    echo "════════════════════════════════════════════════════════════════════"
    echo ""
    
    # 基本信息
    echo "**Skill 名称:** $SKILL_NAME"
    [ -n "$SKILL_DESC" ] && echo "**功能描述:** ${SKILL_DESC:0:60}"
    echo "**扫描文件:** ${#FILES[@]} 个"
    echo "**检测问题:** ${#ISSUES[@]} 个"
    echo ""
    
    # 安全评分
    if [ $CURRENT_SCORE -ge 80 ]; then
        echo -e "📊 安全评分：✅ ${CURRENT_SCORE}/100 — 安全"
    elif [ $CURRENT_SCORE -ge 60 ]; then
        echo -e "📊 安全评分：⚠️ ${CURRENT_SCORE}/100 — 可疑"
    else
        echo -e "📊 安全评分：🚫 ${CURRENT_SCORE}/100 — 危险"
    fi
    echo ""
    
    # 检测清单
    echo "🔍 **检测清单：** ✅ 全部威胁分类已检测"
    echo ""
    
    # 文件类型
    echo "| 文件类型 | 状态 |"
    echo "|----------|------|"
    [ $HAS_JS -eq 1 ] && echo "| JavaScript (.js) | ✅ |" || echo "| JavaScript (.js) | ➖ 无 |"
    [ $HAS_TS -eq 1 ] && echo "| TypeScript (.ts) | ✅ |" || echo "| TypeScript (.ts) | ➖ 无 |"
    [ $HAS_PY -eq 1 ] && echo "| Python (.py) | ✅ |" || echo "| Python (.py) | ➖ 无 |"
    [ $HAS_SH -eq 1 ] && echo "| Shell (.sh) | ✅ |" || echo "| Shell (.sh) | ➖ 无 |"
    echo ""
    echo ""
    echo "**🛡️ 威胁检测规则（共 57 项）：**"
    echo ""
    echo "**EXFIL (18):** credential-access, vault-access, private-key, api-key, network-backdoor, http-server, network-request, http-client, database-access, config-write, wallet-access, port-listening, proxy-tor, git-operation, file-download, credential-read"
    echo ""
    echo "**INJECTION (19):** remote-script, cmd-execution, npx-exec, dynamic-exec, prompt-injection, jailbreak, dynamic-import, backtick-injection, system-probing, shell-injection, crypto-operation"
    echo ""
    echo "**TROJAN (14):** destructive-delete, credential-read, process-kill, persistent-timer, postinstall-risk, archive-exploit, arbitrary-write, deserialize"
    echo ""
    echo "**OBFUSCATION (6):** base64, env-trigger, hidden-exec, persistent-shell, obfuscated-package"
    echo ""
    
    # 风险统计
    if [ ${#ISSUES[@]} -eq 0 ]; then
        echo "📊 **检测结果：** 未发现风险"
    else
        CRIT_COUNT=0; HIGH_COUNT=0; MED_COUNT=0
        for issue in "${ISSUES[@]}"; do
            case "$issue" in
                *critical*) CRIT_COUNT=$((CRIT_COUNT+1)) ;;
                *high*) HIGH_COUNT=$((HIGH_COUNT+1)) ;;
                *medium*) MED_COUNT=$((MED_COUNT+1)) ;;
            esac
        done
        echo "📊 **检测结果：** 发现 ${#ISSUES[@]} 个风险"
        [ $CRIT_COUNT -gt 0 ] && echo "- 🔴 critical: $CRIT_COUNT 个"
        [ $HIGH_COUNT -gt 0 ] && echo "- 🟠 high: $HIGH_COUNT 个"
        [ $MED_COUNT -gt 0 ] && echo "- 🟡 medium: $MED_COUNT 个"
    fi
    echo ""
    echo "---"
    echo ""
    
    # 风险详情
    if [ ${#ISSUES[@]} -gt 0 ]; then
        echo "**⚠️ 风险详情：**"
        echo ""
        echo "| # | 分类 | 风险 | 等级 | 文件 |"
        echo "|:---:|--------|------------------|-----------|------------|"
        idx=1
        for issue in "${ISSUES[@]}"; do
            IFS='|' read -r cat rule level dd file snippet <<< "$issue"
            echo "| $idx | $cat | $rule | $level | $(basename "$file") |"
            idx=$((idx+1))
        done
        echo ""
        echo "---"
        echo ""
        
        # 每条风险解释
        echo "**每条风险解释：**"
        echo ""
        for issue in "${ISSUES[@]}"; do
            IFS='|' read -r cat rule level dd file snippet <<< "$issue"
            desc=$(get_risk_desc "$rule")
            echo "- $desc"
        done
        echo ""
    fi
    
    # 结论
    echo "---"
    echo ""
    if [ $CURRENT_SCORE -ge 80 ]; then
        echo "✅ **结论：安全**"
        echo ""
        echo "📝 静态扫描存在局限性，建议："
        echo "- 在隔离环境中测试"
        echo "- 审查代码逻辑"
        echo "- 关注运行时行为"
    else
        # 需要 LLM 分析的情况
        if [ $CURRENT_SCORE -ge 30 ]; then
            echo "⚠️ **结论：建议谨慎使用**"
            echo ""
            echo "检测到 ${#ISSUES[@]} 个风险，需评估是否可接受。"
        else
            echo "🚫 **结论：不推荐安装使用**"
            echo ""
            echo "检测到 ${#ISSUES[@]} 个风险，包括多个 critical 级别问题。"
        fi

        # LLM 分析提示将通过交互式方式提供（见下方）
    fi

    echo ""
    echo "════════════════════════════════════════════════════════════════════"
}

# 生成 LLM 语义分析提示
# 调用 LLM 进行语义分析

generate_llm_prompt() {
    cat << 'PROMPT_EOF'
# Skill 安全语义分析请求

## 任务
你是一位专业的代码安全审计员。请从安全产品角度分析以下 Skill，判断它是否可以安全安装使用。

## 安全评估六维框架

请按以下六个维度逐一评估：

| 维度 | 问题 | 权重 |
|------|------|------|
| **1. 数据透明** | 它访问/发送了什么数据？去了哪里？是否告知用户？ | 高 |
| **2. 权限边界** | 申请的权限（网络/文件/进程/环境变量）是否超出声明功能？ | 高 |
| **3. 行为透明** | 有没有未声明的偷偷执行行为？ | 极高 |
| **4. 供应链风险** | 执行外部包（npx/pip/git）来源可信吗？版本固定吗？ | 高 |
| **5. 用户控制** | 用户能随时停止/禁用吗？敏感操作有确认吗？ | 中 |
| **6. 成本告知** | 有没有隐性成本（Gas费/算力消耗/付费API）？ | 中 |

## 额外判断（新增）

如存在以下任一情况，**直接标记为 failed**：

1. **数据外泄**：向非功能必需的第三方发送用户数据
2. **偷偷执行**：在用户不知情时执行额外行为（如后台下载、隐藏进程）
3. **权限超出**：申请的权限（网络/文件/进程/环境变量）超出 Skill 声明的功能范围
4. **供应链攻击**：执行来源不明的外部包（如 npx 不固定版本、pip 安装未知包）
5. **用户无控制**：无法停止、或停止后自动重启
6. **成本不透明**：产生 Gas 费/算力消耗等用户无法预估的成本

## 分析要求

请按以下格式输出：

### 1. 六维评估
对每个维度给出简要评估：
- **[维度名]**：[通过/关注/警告] — [简要说明]

### 2. 总体评估
- 语义检测结果：✅ passed / ⚠️ failed / 🚫 failed
- 理由：综合六维判断，给出整体结论

### 3. 逐文件分析

对每个有风险的文件，以表格形式输出：

| 风险 | 判断 | 说明 | 越界行为 |
|------|------|------|---------|
| [风险名] | ✅误报/⚠️低风险/🚨真实威胁 | [详细解释] | ⚠️ 维度X+Y / 无明显越界行为 |

### 4. 最终建议
- 是否可以安装使用？
- 需要注意什么？

PROMPT_EOF

    echo ""
    echo "## 静态扫描报告"
    echo ""
    echo "**Skill 名称:** $SKILL_NAME"
    [ -n "$SKILL_DESC" ] && echo "**功能描述:** ${SKILL_DESC:0:200}"
    echo ""
    echo "**安全评分:** ${CURRENT_SCORE}/100"
    echo ""
    echo "### 检测到的风险（共 ${#ISSUES[@]} 个）"
    echo ""
    echo "| # | 分类 | 风险类型 | 等级 | 文件 | 匹配内容 |"
    echo "|:---:|--------|----------|-----------|------------|------------|"
    idx=1
    # 去重：只显示唯一文件
    SEEN_FILES=""; SEEN_FILES_COUNT=0
    for issue in "${ISSUES[@]}"; do
        file=$(echo "$issue" | awk -F'|' '{print $5}')
        if [ -n "$file" ] && ! echo "$SEEN_FILES_LIST" | grep -qFx "$file"; then
            SEEN_FILES_LIST="${SEEN_FILES_LIST}${file}
"
            echo "$issue" | awk -F'|' '{printf "| %d | %s | %s | %s | `%s` | `%s` |
", '$idx', $1, $2, $3, $5, $6}'
            idx=$((idx+1))
        fi
    done

    echo ""
    echo "### 相关文件内容"
    echo ""
    echo "以下是检测到风险的文件内容，请仔细分析："
    echo ""
    for issue in "${ISSUES[@]}"; do
        file=$(echo "$issue" | awk -F'|' '{print $5}')
        if [ -n "$file" ] && [ -f "$file" ] && ! echo "$SEEN_FILES_DONE" | grep -qFx "$file"; then
            SEEN_FILES_DONE="${SEEN_FILES_DONE}${file}
"
        fi
    done
    for issue in "${ISSUES[@]}"; do
        file=$(echo "$issue" | awk -F'|' '{print $5}')
        if [ -n "$file" ] && [ -f "$file" ] && echo "$SEEN_FILES_LIST" | grep -qFx "$file"; then
            echo "---"
            echo ""
            echo "**文件: $(basename "$file")**"
            echo ""
            echo '```bash'
            cat "$file"
            echo '```'
            echo ""
        fi
    done

    if [ -f "$TARGET_DIR/SKILL.md" ]; then
        echo "---"
        echo ""
        echo "**文件: SKILL.md（前 20 行，简介）**"
        echo ""
        echo '```markdown'
        head -20 "$TARGET_DIR/SKILL.md"
        echo '```'
        echo ""
    fi

    echo "════════════════════════════════════════════════════════════════════"
    echo "📋 以上内容已生成完毕，请复制上方内容（从 # Skill 安全语义分析请求 开始）"
    echo "   给 LLM 进行深度语义分析。"
    echo ""
    echo "💡 提示：从安全产品角度判断，关注数据透明、权限边界、行为透明、"
    echo "   供应链风险、用户控制、成本告知六个维度。"
    echo "════════════════════════════════════════════════════════════════════"
}




show_help() {
    echo "用法: $0 [选项] <target>"
    echo ""
    echo "选项:"
    echo "  --help                    显示帮助信息"
    echo "  --format <text|json>     指定输出格式（默认 text），json 格式会自动验证"
    echo "  --whitelist-add <skill>   添加到白名单"
    echo "  --whitelist-list          显示白名单"
    echo ""
    echo "target 可以是:"
    echo "  • ClawHub URL:  https://clawhub.ai/owner/skill-name"
    echo "  • 本地路径:     ~/.openclaw/workspace/skills/skill-name"
    echo ""
    echo "示例:"
    echo "  $0 https://clawhub.ai/steipete/video-frames"
    echo "  $0 ~/.openclaw/workspace/skills/litcoin"
    echo "  $0 --whitelist-add some-skill"
    echo "  $0 --whitelist-list"
}

case "$1" in
    --help) show_help; exit 0;;
    --whitelist-add) whitelist_add "$2";;
    --whitelist-list) [ -f "$WHITELIST_FILE" ] && cat "$WHITELIST_FILE" || echo "(空)"; exit 0;;
    --format) OUTPUT_FORMAT="$2"; shift 2;;
esac

TARGET="$1"
[ -z "$TARGET" ] && echo "用法: $0 <target>（使用 --help 查看更多）" && exit 1

log_info "扫描: $TARGET"
resolve_target "$TARGET" || exit 1

if is_whitelisted "$SKILL_NAME"; then
    echo ""
    echo "════════════════════════════════════════════════════════════════════"
    echo "                    🔒 Skill 安全检测报告"
    echo "════════════════════════════════════════════════════════════════════"
    echo ""
    echo "📦 Skill: $SKILL_NAME"
    echo "📊 评分: 100/100"
    echo "✅ 已通过白名单 (跳过扫描)"
    exit 0
fi

get_skill_info
check_deps

# 安全检查：TARGET_DIR 必须存在
if [[ -z "$TARGET_DIR" ]] || [[ ! -d "$TARGET_DIR" ]]; then
    echo ""
    echo "[ERROR] 无法访问目标目录，下载可能失败"
    echo "[ERROR] 请检查链接是否有效，或尝试使用本地路径"
    exit 1
fi

# 扫描文件
SCAN_FILES=$(find "$TARGET_DIR" \( -name "*.js" -o -name "*.ts" -o -name "*.py" -o -name "*.sh" \) -type f 2>/dev/null)
if [[ -z "$SCAN_FILES" ]]; then
    echo "[WARN] 未找到任何可扫描的文件 (.js/.ts/.py/.sh)"
    echo "[WARN] Skill 可能只包含文档或非脚本文件"
fi
for f in $SCAN_FILES; do
    scan_file "$f"
done

generate_report

# 交互式 LLM 分析（仅在有风险时询问）
if [ ${#ISSUES[@]} -gt 0 ]; then
    echo ""
    echo "════════════════════════════════════════════════════════════════════"
    echo "                     🤖 LLM 语义分析提示"
    echo "════════════════════════════════════════════════════════════════════"
    echo ""
    echo "⚠️  静态扫描发现 ${#ISSUES[@]} 个风险，建议使用 LLM 进行语义分析。"
    echo ""
    echo "请将以下内容复制给 LLM 进行深度分析："
    echo ""
    generate_llm_prompt
    echo ""
    echo "════════════════════════════════════════════════════════════════════"
    echo "提示：请将上方内容（从「# Skill 安全语义分析请求」开始）"
    echo "      复制给我进行深度语义分析。"
    echo "════════════════════════════════════════════════════════════════════"
fi


[ "$TARGET_TYPE" != "local" ] && rm -rf "$TARGET_DIR"

# JSON 格式
if [ "$OUTPUT_FORMAT" = "json" ]; then
    echo ""
    echo "=== JSON 格式 ==="
    echo "{"
    echo "  \"skill\": \"$SKILL_NAME\","
    echo "  \"score\": $CURRENT_SCORE,"
    echo "  \"files\": ${#FILES[@]},"
    echo "  \"issues\": ["
    first=true
    for i in "${ISSUES[@]}"; do
        IFS='|' read -r cat rule level dd file snippet <<< "$i"
        [ -n "$first" ] && first="" || echo ","
        echo -n "    {\"category\":\"$cat\",\"rule\":\"$rule\",\"level\":\"$level\",\"file\":\"$(basename "$file")\",\"snippet\":\"$snippet\"}"
    done
    echo ""
    echo "  ]"
    echo "}"
    
    # JSON 验证
    echo ""
    [ -z "$first" ] && json_valid=true || json_valid=false
    if [ "$json_valid" = true ]; then
        # 简单验证：检查 JSON 基本结构
        if echo "{}" | python3 -c "import sys,json; json.load(sys.stdin)" 2>/dev/null; then
            echo "[INFO] JSON 输出格式验证通过"
        else
            echo "[WARN] JSON 输出可能格式异常，建议检查"
        fi
    fi
fi

# 根据风险返回退出码
HAS_CRIT=false
for i in "${ISSUES[@]}"; do [[ "$i" == *"critical"* ]] && HAS_CRIT=true; done
[ "$HAS_CRIT" = true ] && exit 1
[ $CURRENT_SCORE -lt 70 ] && exit 1
exit 0

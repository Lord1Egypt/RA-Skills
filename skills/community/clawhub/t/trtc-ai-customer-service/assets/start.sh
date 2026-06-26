#!/usr/bin/env bash
# =====================================================================
# TRTC AI Customer Service - One-click Launcher (macOS / Linux)
# TRTC AI 智能客服 - 一键启动脚本 (macOS / Linux)
#
# Features / 功能：
#   1. Auto-detect Python version (>= 3.8) / 自动检测 Python 版本
#   2. Auto-create env.yaml from env.example.yaml / 自动生成配置文件
#   3. Auto-create & activate venv / 自动创建虚拟环境
#   4. Auto-install dependencies / 自动安装依赖
#   5. Default PyPI, fallback Tsinghua mirror / 默认官方源，回退清华镜像
#   6. Auto-detect locale for i18n output / 根据系统语言自动切换提示
#   7. Launch Flask server / 启动 Flask 服务
#
# Usage / 使用：
#   ./start.sh            # Start / 启动
#   ./start.sh --rebuild  # Force rebuild venv / 强制重建虚拟环境
# =====================================================================

set -e

# ---------------- Locale Detection / 语言检测 ----------------
_LOCALE="${LANG:-${LC_ALL:-en_US.UTF-8}}"
_IS_ZH=0
case "$_LOCALE" in
    zh_*|zh-*) _IS_ZH=1 ;;
esac

# i18n message helper
msg() {
    if [ "$_IS_ZH" -eq 1 ]; then
        echo "$2"
    else
        echo "$1"
    fi
}

# ---------------- Basic Variables / 基础变量 ----------------
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR="venv"
ENV_FILE="env.yaml"
ENV_EXAMPLE="env.example.yaml"
REQUIREMENTS="requirements.txt"
MIN_PY_MAJOR=3
MIN_PY_MINOR=8
PORT=8080

# Color output / 颜色输出
if [ -t 1 ]; then
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    RED='\033[0;31m'
    CYAN='\033[0;36m'
    BOLD='\033[1m'
    NC='\033[0m'
else
    GREEN=''; YELLOW=''; RED=''; CYAN=''; BOLD=''; NC=''
fi

log() { printf "${CYAN}[%s]${NC} %s\n" "$(date +%H:%M:%S)" "$*"; }
ok()  { printf "${GREEN}✓${NC} %s\n" "$*"; }
warn(){ printf "${YELLOW}⚠${NC}  %s\n" "$*"; }
err() { printf "${RED}✗${NC} %s\n" "$*" >&2; }
die() { err "$*"; exit 1; }

# ---------------- Argument Parsing / 参数解析 ----------------
REBUILD=0
for arg in "$@"; do
    case "$arg" in
        --rebuild) REBUILD=1 ;;
        --help|-h)
            msg "Usage: $0 [--rebuild]" "用法: $0 [--rebuild]"
            msg "  --rebuild  Delete existing venv and rebuild" "  --rebuild  删除现有 venv 并重建"
            exit 0
            ;;
    esac
done

# ---------------- Step 1: Detect Python / 检测 Python ----------------
log "$(msg "Detecting Python environment..." "检测 Python 环境...")"

PY_CMD=""
for cand in python3 python; do
    if command -v "$cand" >/dev/null 2>&1; then
        VER=$("$cand" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || echo "0.0")
        MAJOR=$(echo "$VER" | cut -d. -f1)
        MINOR=$(echo "$VER" | cut -d. -f2)
        if [ "$MAJOR" -gt "$MIN_PY_MAJOR" ] || { [ "$MAJOR" -eq "$MIN_PY_MAJOR" ] && [ "$MINOR" -ge "$MIN_PY_MINOR" ]; }; then
            PY_CMD="$cand"
            ok "$(msg "Found Python $VER -> $(command -v "$cand")" "找到 Python $VER -> $(command -v "$cand")")"
            break
        fi
    fi
done

if [ -z "$PY_CMD" ]; then
    err "$(msg "Python >= ${MIN_PY_MAJOR}.${MIN_PY_MINOR} not found" "未检测到 Python >= ${MIN_PY_MAJOR}.${MIN_PY_MINOR}")"
    msg "  Please visit https://www.python.org/downloads/ to install" "  请前往 https://www.python.org/downloads/ 下载安装"
    exit 1
fi

# ---------------- Step 2: Detect env.yaml / 检测 env.yaml ----------------
if [ ! -f "$ENV_FILE" ]; then
    if [ ! -f "$ENV_EXAMPLE" ]; then
        die "$(msg "${ENV_EXAMPLE} not found, project files incomplete" "未找到 ${ENV_EXAMPLE}，项目文件不完整")"
    fi
    cp "$ENV_EXAMPLE" "$ENV_FILE"
    warn "$(msg "Created ${ENV_FILE} (copied from ${ENV_EXAMPLE})" "已创建 ${ENV_FILE}（从 ${ENV_EXAMPLE} 复制）")"
    echo ""
    printf "%b╔══════════════════════════════════════════════════╗%b\n" "$BOLD" "$NC"
    if [ "$_IS_ZH" -eq 1 ]; then
        printf "%b║          首次配置 - 分步填入密钥                  ║%b\n" "$BOLD" "$NC"
    else
        printf "%b║       First-time Setup - Enter Credentials       ║%b\n" "$BOLD" "$NC"
    fi
    printf "%b╚══════════════════════════════════════════════════╝%b\n" "$BOLD" "$NC"
    echo ""
    if [ "$_IS_ZH" -eq 1 ]; then
        echo "  需要准备 3 组密钥 + 1 项业务配置（约 5 分钟）。"
        echo "  每步都可以按 Enter 跳过，稍后手动编辑 ${ENV_FILE}。"
        echo ""
        echo "  ⚠ 注意：密钥将以明文存储在 ${ENV_FILE} 中，"
        echo "    请勿提交到版本控制，建议设置 chmod 600 ${ENV_FILE}。"
    else
        echo "  You'll need 3 sets of credentials + 1 business config (~5 min)."
        echo "  Press Enter at any step to skip, then edit ${ENV_FILE} manually."
        echo ""
        echo "  ⚠ Note: Credentials are stored in plaintext in ${ENV_FILE}."
        echo "    Do not commit to version control. Consider: chmod 600 ${ENV_FILE}"
    fi
    echo ""

    # --- 0/4 Deployment Region / 部署区域选择 ---
    printf "%b[0/4] $(msg "Deployment Region" "部署区域")%b\n" "$CYAN" "$NC"
    if [ "$_IS_ZH" -eq 1 ]; then
        printf "    1) 国际站 intl（默认）  2) 中国站 cn\n"
        printf "  请选择 [1-2]: "
    else
        printf "    1) International (default)  2) China Mainland\n"
        printf "  Choose [1-2]: "
    fi
    read -r INPUT_REGION </dev/tty 2>/dev/null || INPUT_REGION=""

    DEPLOY_REGION="intl"
    if [ "$INPUT_REGION" = "2" ]; then
        DEPLOY_REGION="cn"
        sed -i.bak "s|Region:.*|Region: cn   # intl / cn|" "$ENV_FILE"
        ok "$(msg "Region set to: China Mainland (cn)" "部署区域: 中国站 (cn)")"
    else
        ok "$(msg "Region set to: International (intl)" "部署区域: 国际站 (intl)")"
    fi
    echo ""

    # Set console URLs based on region
    if [ "$DEPLOY_REGION" = "cn" ]; then
        URL_CAM="https://console.cloud.tencent.com/cam/capi"
        URL_TRTC="https://console.cloud.tencent.com/trtc/app"
        URL_LLM="https://cloud.tencent.com/document/product/647/115413"
    else
        URL_CAM="https://console.intl.cloud.tencent.com/cam/capi"
        URL_TRTC="https://console.trtc.io/app"
        URL_LLM="https://trtc.io/document/68338?product=conversationalai"
    fi

    # --- 1/4 Cloud API Credentials / 腾讯云 API 密钥 ---
    printf "%b[1/4] $(msg "Tencent Cloud API Credentials" "腾讯云 API 密钥")%b\n" "$CYAN" "$NC"
    printf "  $(msg "Get from" "获取"): %b${URL_CAM}%b\n" "$BOLD" "$NC"
    printf "  SECRET_ID : " ; read -r INPUT_SID </dev/tty 2>/dev/null || INPUT_SID=""
    printf "  SECRET_KEY: " ; read -r INPUT_SKEY </dev/tty 2>/dev/null || INPUT_SKEY=""

    if [ -n "$INPUT_SID" ] && [ -n "$INPUT_SKEY" ]; then
        sed -i.bak "s|SECRET_ID:.*|SECRET_ID: ${INPUT_SID}|" "$ENV_FILE"
        sed -i.bak "s|SECRET_KEY:.*|SECRET_KEY: ${INPUT_SKEY}|" "$ENV_FILE"
        ok "$(msg "Cloud API credentials saved" "CloudAPI 密钥已填入")"
    else
        warn "$(msg "Skipped, please edit ${ENV_FILE} later" "已跳过，请稍后手动编辑 ${ENV_FILE}")"
    fi
    echo ""

    # --- 2/4 TRTC App / TRTC 应用 ---
    printf "%b[2/4] $(msg "TRTC App Credentials" "TRTC 应用凭据")%b\n" "$CYAN" "$NC"
    printf "  $(msg "Get from" "获取"): %b${URL_TRTC}%b\n" "$BOLD" "$NC"
    printf "  SDKAPPID: " ; read -r INPUT_APPID </dev/tty 2>/dev/null || INPUT_APPID=""
    printf "  SECRET  : " ; read -r INPUT_TSECRET </dev/tty 2>/dev/null || INPUT_TSECRET=""

    if [ -n "$INPUT_APPID" ] && [ -n "$INPUT_TSECRET" ]; then
        sed -i.bak "s|SDKAPPID:.*|SDKAPPID: ${INPUT_APPID}|" "$ENV_FILE"
        sed -i.bak "s|SECRET: your-trtc-secret|SECRET: ${INPUT_TSECRET}|" "$ENV_FILE"
        ok "$(msg "TRTC credentials saved" "TRTC 凭据已填入")"
    else
        warn "$(msg "Skipped, please edit ${ENV_FILE} later" "已跳过，请稍后手动编辑 ${ENV_FILE}")"
    fi
    echo ""

    # --- 3/4 LLM API Key (TokenHub recommended) ---
    printf "%b[3/4] LLM API Key%b\n" "$CYAN" "$NC"
    if [ "$_IS_ZH" -eq 1 ]; then
        printf "  推荐使用 TokenHub（腾讯云 LLM 网关，开箱即用）\n"
    else
        printf "  Recommended: TokenHub (Tencent Cloud LLM gateway, ready to use)\n"
    fi
    if [ "$DEPLOY_REGION" = "cn" ]; then
        TOKENHUB_URL="https://tokenhub.tencentmaas.com/v1/chat/completions"
        printf "  $(msg "TokenHub Console" "TokenHub 控制台"): %bhttps://console.cloud.tencent.com/tokenhub%b\n" "$BOLD" "$NC"
    else
        TOKENHUB_URL="https://tokenhub-intl.tencentcloudmaas.com/v1/chat/completions"
        printf "  $(msg "TokenHub Console" "TokenHub 控制台"): %bhttps://console.intl.cloud.tencent.com/tokenhub%b\n" "$BOLD" "$NC"
    fi
    printf "  $(msg "Other LLM guide" "其他 LLM 配置指南"): %b${URL_LLM}%b\n" "$BOLD" "$NC"
    printf "  API Key: " ; read -r INPUT_LLM </dev/tty 2>/dev/null || INPUT_LLM=""

    if [ -n "$INPUT_LLM" ]; then
        sed -i.bak "s|APIKey:.*|APIKey: ${INPUT_LLM}|" "$ENV_FILE"
        # 默认填入 TokenHub APIUrl 和推荐模型
        sed -i.bak "s|APIUrl:.*|APIUrl: ${TOKENHUB_URL}|" "$ENV_FILE"
        sed -i.bak "s|Model:.*|Model: deepseek-v4-flash|" "$ENV_FILE"
        ok "$(msg "LLM configured (TokenHub + deepseek-v4-flash)" "LLM 已配置（TokenHub + deepseek-v4-flash）")"
    else
        warn "$(msg "Skipped, please edit ${ENV_FILE} later" "已跳过，请稍后手动编辑 ${ENV_FILE}")"
    fi
    echo ""

    # --- 4/4 AI Customer Service Role / AI 客服角色配置 ---
    printf "%b[4/4] $(msg "AI Customer Service Role (optional)" "AI 客服角色配置（可选）")%b\n" "$CYAN" "$NC"
    if [ "$_IS_ZH" -eq 1 ]; then
        echo "  定制 AI 客服的业务角色，按 Enter 使用默认电商客服。"
        echo ""
        echo "  你的商城主营什么品类？"
        printf "    1) 综合电商（默认）  2) 数码产品  3) 服装鞋帽  4) 食品生鲜  5) 家居百货\n"
        printf "  请选择 [1-5]: " ; read -r INPUT_CAT </dev/tty 2>/dev/null || INPUT_CAT=""
        echo ""
        echo "  客服语气风格？"
        printf "    1) 亲切自然（默认）  2) 专业严谨  3) 活泼可爱\n"
        printf "  请选择 [1-3]: " ; read -r INPUT_TONE </dev/tty 2>/dev/null || INPUT_TONE=""
    else
        echo "  Customize AI role, press Enter for default e-commerce assistant."
        echo ""
        echo "  What product category does your store specialize in?"
        printf "    1) General e-commerce (default)  2) Electronics  3) Clothing  4) Food & Fresh  5) Home & Living\n"
        printf "  Choose [1-5]: " ; read -r INPUT_CAT </dev/tty 2>/dev/null || INPUT_CAT=""
        echo ""
        echo "  Customer service tone?"
        printf "    1) Warm & natural (default)  2) Professional  3) Lively & cheerful\n"
        printf "  Choose [1-3]: " ; read -r INPUT_TONE </dev/tty 2>/dev/null || INPUT_TONE=""
    fi

    # Build SystemPrompt based on choices
    case "$INPUT_CAT" in
        2) CAT_TEXT="数码产品" ; CAT_DUTY="解答电子产品参数对比、兼容性问题、保修政策、使用教程" ;;
        3) CAT_TEXT="服装鞋帽" ; CAT_DUTY="解答尺码推荐、面料材质、搭配建议、洗涤保养、退换尺码" ;;
        4) CAT_TEXT="食品生鲜" ; CAT_DUTY="解答保质期、储存方式、配送时效、食材产地、过敏原信息" ;;
        5) CAT_TEXT="家居百货" ; CAT_DUTY="解答商品尺寸规格、安装方式、材质说明、配送安装服务" ;;
        *) CAT_TEXT="" ; CAT_DUTY="" ;;
    esac

    case "$INPUT_TONE" in
        2) TONE_TEXT="语气专业严谨，用词准确规范" ;;
        3) TONE_TEXT="语气活泼可爱，适当使用轻松的表达方式" ;;
        *) TONE_TEXT="" ;;
    esac

    if [ -n "$CAT_TEXT" ] || [ -n "$TONE_TEXT" ]; then
        "$PY_CMD" -c "
import sys
cat_text = sys.argv[1]
cat_duty = sys.argv[2]
tone_text = sys.argv[3]

with open('env.yaml', 'r') as f:
    content = f.read()

# ---- Chinese ----
zh_insert = ''
if cat_text:
    zh_insert += '\n    本商城主营' + cat_text + '。你需要特别擅长：' + cat_duty + '。'
if tone_text:
    zh_insert += '\n    ' + tone_text + '。'
if zh_insert:
    content = content.replace('请遵循以下原则：', zh_insert.strip() + '\n    请遵循以下原则：', 1)

# ---- Cantonese ----
yue_insert = ''
if cat_text:
    yue_cat = {'数码产品':'數碼產品','服装鞋帽':'服裝鞋帽','食品生鲜':'食品生鮮','家居百货':'家居百貨'}.get(cat_text, cat_text)
    yue_duty = {'数码产品':'解答電子產品參數對比、兼容性問題、保修政策、使用教程','服装鞋帽':'解答尺碼推薦、面料材質、搭配建議、洗滌保養、退換尺碼','食品生鲜':'解答保質期、儲存方式、配送時效、食材產地、過敏原信息','家居百货':'解答商品尺寸規格、安裝方式、材質說明、配送安裝服務'}.get(cat_text, cat_duty)
    yue_insert += '\n    本商城主營' + yue_cat + '。你需要特別擅長：' + yue_duty + '。'
if tone_text:
    yue_tone = {'语气专业严谨，用词准确规范':'語氣專業嚴謹，用詞準確規範','语气活泼可爱，适当使用轻松的表达方式':'語氣活潑可愛，適當使用輕鬆嘅表達方式'}.get(tone_text, tone_text)
    yue_insert += '\n    ' + yue_tone + '。'
if yue_insert:
    content = content.replace('請遵循以下原則：', yue_insert.strip() + '\n    請遵循以下原則：', 1)

# ---- English ----
en_insert = ''
if cat_text:
    en_cat = {'数码产品':'digital and electronics products','服装鞋帽':'clothing and footwear','食品生鲜':'food and fresh produce','家居百货':'home and household goods'}.get(cat_text, cat_text)
    en_duty = {'数码产品':'answering questions about product specs, compatibility, warranty policies, and usage tutorials','服装鞋帽':'answering questions about sizing, fabric materials, styling suggestions, care instructions, and size exchanges','食品生鲜':'answering questions about shelf life, storage methods, delivery times, product origins, and allergen information','家居百货':'answering questions about product dimensions, installation, materials, and delivery services'}.get(cat_text, cat_duty)
    en_insert += '\n    This store specializes in ' + en_cat + '. You should be especially good at ' + en_duty + '.'
if tone_text:
    en_tone = {'语气专业严谨，用词准确规范':'Use a professional and precise tone with accurate wording','语气活泼可爱，适当使用轻松的表达方式':'Use a lively and cheerful tone with casual expressions'}.get(tone_text, '')
    if en_tone:
        en_insert += '\n    ' + en_tone + '.'
if en_insert:
    content = content.replace('Please follow these principles:', en_insert.strip() + '\n    Please follow these principles:', 1)

with open('env.yaml', 'w') as f:
    f.write(content)
" "$CAT_TEXT" "$CAT_DUTY" "$TONE_TEXT" 2>/dev/null && ok "$(msg "AI role customized - trilingual sync (${CAT_TEXT:-default}${TONE_TEXT:+ / }${TONE_TEXT:-})" "AI 客服角色已定制 - 三语同步（${CAT_TEXT:-默认}${TONE_TEXT:+ / }${TONE_TEXT:-}）")" || warn "$(msg "Customization failed, please edit SystemPrompt manually" "定制写入失败，请手动编辑 SystemPrompt")"

        # Generate mock orders matching the selected category
        if [ -n "$CAT_TEXT" ] && [ "$CAT_TEXT" != "" ]; then
            "$PY_CMD" -c "
import json, sys
cat = sys.argv[1]
ORDERS = {
    '数码产品': [
        {'id':'CS20260510001','name':{'zh':'无线降噪耳机 Pro','yue':'無線降噪耳機 Pro','en':'Wireless ANC Headphones Pro'},'price':{'zh':'¥699','yue':'HK\$759','en':'\$96'},'status':'shipped','date':'2026-05-10','emoji':'🎧'},
        {'id':'CS20260508002','name':{'zh':'轻薄笔记本电脑 14寸','yue':'輕薄筆記本電腦 14吋','en':'Ultra-slim Laptop 14\"'},'price':{'zh':'¥5,299','yue':'HK\$5,749','en':'\$729'},'status':'delivered','date':'2026-05-08','emoji':'💻'},
        {'id':'CS20260507003','name':{'zh':'智能手表 S9','yue':'智能手錶 S9','en':'Smart Watch S9'},'price':{'zh':'¥1,299','yue':'HK\$1,409','en':'\$179'},'status':'pending','date':'2026-05-07','emoji':'⌚'},
        {'id':'CS20260505004','name':{'zh':'机械键盘 RGB','yue':'機械鍵盤 RGB','en':'Mechanical Keyboard RGB'},'price':{'zh':'¥499','yue':'HK\$541','en':'\$69'},'status':'refunding','date':'2026-05-05','emoji':'⌨️'},
        {'id':'CS20260501005','name':{'zh':'蓝牙音箱 mini','yue':'藍牙音箱 mini','en':'Bluetooth Speaker Mini'},'price':{'zh':'¥199','yue':'HK\$216','en':'\$28'},'status':'delivered','date':'2026-05-01','emoji':'🔊'},
    ],
    '服装鞋帽': [
        {'id':'CS20260510001','name':{'zh':'轻奢羊绒大衣','yue':'輕奢羊絨大衣','en':'Luxury Cashmere Coat'},'price':{'zh':'¥2,399','yue':'HK\$2,603','en':'\$329'},'status':'shipped','date':'2026-05-10','emoji':'🧥'},
        {'id':'CS20260508002','name':{'zh':'运动跑鞋 Air Max','yue':'運動跑鞋 Air Max','en':'Running Shoes Air Max'},'price':{'zh':'¥899','yue':'HK\$976','en':'\$124'},'status':'delivered','date':'2026-05-08','emoji':'👟'},
        {'id':'CS20260507003','name':{'zh':'真丝连衣裙','yue':'真絲連衣裙','en':'Silk Dress'},'price':{'zh':'¥599','yue':'HK\$650','en':'\$82'},'status':'pending','date':'2026-05-07','emoji':'👗'},
        {'id':'CS20260505004','name':{'zh':'男士休闲西裤','yue':'男士休閒西褲','en':'Men Casual Trousers'},'price':{'zh':'¥349','yue':'HK\$379','en':'\$48'},'status':'refunding','date':'2026-05-05','emoji':'👖'},
        {'id':'CS20260501005','name':{'zh':'纯棉T恤 3件装','yue':'純棉T恤 3件裝','en':'Cotton T-shirt 3-Pack'},'price':{'zh':'¥129','yue':'HK\$140','en':'\$18'},'status':'delivered','date':'2026-05-01','emoji':'👕'},
    ],
    '食品生鲜': [
        {'id':'CS20260510001','name':{'zh':'有机草莓 2斤装','yue':'有機草莓 2斤裝','en':'Organic Strawberries 1kg'},'price':{'zh':'¥59','yue':'HK\$64','en':'\$8'},'status':'shipped','date':'2026-05-10','emoji':'🍓'},
        {'id':'CS20260508002','name':{'zh':'澳洲和牛 M7 眼肉','yue':'澳洲和牛 M7 眼肉','en':'Wagyu Ribeye M7'},'price':{'zh':'¥399','yue':'HK\$433','en':'\$55'},'status':'delivered','date':'2026-05-08','emoji':'🥩'},
        {'id':'CS20260507003','name':{'zh':'智利车厘子 2kg','yue':'智利車厘子 2kg','en':'Chilean Cherries 2kg'},'price':{'zh':'¥168','yue':'HK\$182','en':'\$23'},'status':'pending','date':'2026-05-07','emoji':'🍒'},
        {'id':'CS20260505004','name':{'zh':'挪威三文鱼刺身','yue':'挪威三文魚刺身','en':'Norwegian Salmon Sashimi'},'price':{'zh':'¥129','yue':'HK\$140','en':'\$18'},'status':'refunding','date':'2026-05-05','emoji':'🍣'},
        {'id':'CS20260501005','name':{'zh':'进口全脂牛奶 12盒','yue':'進口全脂牛奶 12盒','en':'Whole Milk 12-Pack'},'price':{'zh':'¥89','yue':'HK\$97','en':'\$12'},'status':'delivered','date':'2026-05-01','emoji':'🥛'},
    ],
    '家居百货': [
        {'id':'CS20260510001','name':{'zh':'智能扫地机器人','yue':'智能掃地機械人','en':'Robot Vacuum Cleaner'},'price':{'zh':'¥1,899','yue':'HK\$2,061','en':'\$261'},'status':'shipped','date':'2026-05-10','emoji':'🤖'},
        {'id':'CS20260508002','name':{'zh':'乳胶记忆枕头','yue':'乳膠記憶枕頭','en':'Memory Foam Pillow'},'price':{'zh':'¥299','yue':'HK\$325','en':'\$41'},'status':'delivered','date':'2026-05-08','emoji':'🛏️'},
        {'id':'CS20260507003','name':{'zh':'北欧风落地灯','yue':'北歐風落地燈','en':'Nordic Floor Lamp'},'price':{'zh':'¥459','yue':'HK\$498','en':'\$63'},'status':'pending','date':'2026-05-07','emoji':'💡'},
        {'id':'CS20260505004','name':{'zh':'不锈钢保温杯 500ml','yue':'不銹鋼保溫杯 500ml','en':'Insulated Bottle 500ml'},'price':{'zh':'¥89','yue':'HK\$97','en':'\$12'},'status':'refunding','date':'2026-05-05','emoji':'🫗'},
        {'id':'CS20260501005','name':{'zh':'竹纤维浴巾套装','yue':'竹纖維浴巾套裝','en':'Bamboo Towel Set'},'price':{'zh':'¥149','yue':'HK\$162','en':'\$20'},'status':'delivered','date':'2026-05-01','emoji':'🛁'},
    ],
}
if cat in ORDERS:
    with open('static/mock-orders.json', 'w', encoding='utf-8') as f:
        json.dump(ORDERS[cat], f, ensure_ascii=False, indent=4)
" "$CAT_TEXT" 2>/dev/null && ok "$(msg "Mock orders updated for: ${CAT_TEXT}" "订单数据已更新为: ${CAT_TEXT}")" || true
        fi
    else
        ok "$(msg "Using default e-commerce assistant role" "使用默认电商客服角色")"
    fi

    # Clean up sed backup files
    rm -f "${ENV_FILE}.bak"

    echo ""
    # Check for unfilled credential placeholders
    if grep -q "your-secret-id\|your-secret-key\|your-trtc-secret\|your-llm-api-key" "$ENV_FILE" 2>/dev/null; then
        warn "$(msg "Some credentials are not filled in" "检测到部分密钥未填写")"
        printf "  $(msg "Please edit" "请编辑") %b%s%b $(msg "and re-run" "补全后重新运行")\n" "$BOLD" "$ENV_FILE" "$NC"
        exit 0
    fi
    ok "$(msg "All credentials configured!" "所有密钥已配置完成！")"
    # Restrict file permissions (owner-only read/write)
    chmod 600 "$ENV_FILE" 2>/dev/null || true
    echo ""
fi
ok "$(msg "${ENV_FILE} exists" "${ENV_FILE} 已存在")"

# ---------------- Step 3: Virtual Environment / 虚拟环境 ----------------
if [ "$REBUILD" -eq 1 ] && [ -d "$VENV_DIR" ]; then
    warn "$(msg "Force rebuild: removing existing $VENV_DIR..." "强制重建：删除现有 $VENV_DIR...")"
    rm -rf "$VENV_DIR"
fi

if [ ! -d "$VENV_DIR" ]; then
    log "$(msg "Creating virtual environment $VENV_DIR..." "创建虚拟环境 $VENV_DIR...")"
    "$PY_CMD" -m venv "$VENV_DIR" 2>/dev/null || {
        err "$(msg "venv creation failed." "venv 创建失败。")"
        msg "  Linux users may need: sudo apt install python3-venv" "  Linux 用户可能需要先安装: sudo apt install python3-venv"
        exit 1
    }
    ok "$(msg "Virtual environment created" "虚拟环境创建完成")"
    NEED_INSTALL=1
else
    ok "$(msg "Virtual environment exists" "虚拟环境已存在")"
    NEED_INSTALL=0
fi

# Activate venv
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
VENV_PY="$VENV_DIR/bin/python"
VENV_PIP="$VENV_DIR/bin/pip"

# ---------------- Step 4: Check Dependencies / 检测依赖完整性 ----------------
if [ "$NEED_INSTALL" -eq 0 ]; then
    if ! "$VENV_PY" -c "import flask, envyaml, loguru, tencentcloud, TLSSigAPIv2" 2>/dev/null; then
        warn "$(msg "Missing dependencies detected, preparing to install..." "检测到依赖缺失，准备安装...")"
        NEED_INSTALL=1
    fi
fi

if [ "$NEED_INSTALL" -eq 1 ]; then
    log "$(msg "Installing dependencies..." "安装依赖...")"

    # Upgrade pip silently
    "$VENV_PIP" install --upgrade pip >/dev/null 2>&1 || true

    # Default: official PyPI; fallback: Tsinghua mirror (for users in mainland China)
    if "$VENV_PIP" install -r "$REQUIREMENTS" --timeout 30 2>/dev/null; then
        ok "$(msg "Dependencies installed (via PyPI)" "依赖安装完成（via 官方源）")"
    else
        warn "$(msg "PyPI failed, retrying with Tsinghua mirror..." "官方源失败，切换到清华镜像重试...")"
        MIRROR="https://pypi.tuna.tsinghua.edu.cn/simple"
        "$VENV_PIP" install -r "$REQUIREMENTS" -i "$MIRROR" --timeout 15 || die "$(msg "Dependency installation failed" "依赖安装失败")"
        ok "$(msg "Dependencies installed (via Tsinghua mirror)" "依赖安装完成（via 清华镜像）")"
    fi
else
    ok "$(msg "Dependencies ready" "依赖已就绪")"
fi

# ---------------- Step 5: Port Conflict / 端口冲突检测 ----------------
log "$(msg "Checking if port ${PORT} is in use..." "检查端口 ${PORT} 是否被占用...")"

EXISTING_PID=""
if command -v lsof >/dev/null 2>&1; then
    EXISTING_PID=$(lsof -ti :"$PORT" -sTCP:LISTEN 2>/dev/null || true)
elif command -v ss >/dev/null 2>&1; then
    EXISTING_PID=$(ss -tlnp "sport = :$PORT" 2>/dev/null | grep -oP 'pid=\K[0-9]+' | head -1 || true)
elif command -v netstat >/dev/null 2>&1; then
    EXISTING_PID=$(netstat -tlnp 2>/dev/null | grep ":$PORT " | grep -oP '[0-9]+(?=/)' | head -1 || true)
fi

if [ -n "$EXISTING_PID" ]; then
    EXISTING_CMD=$(ps -p "$EXISTING_PID" -o comm= 2>/dev/null || echo "unknown")
    EXISTING_ARGS=$(ps -p "$EXISTING_PID" -o args= 2>/dev/null || echo "")
    warn "$(msg "Port ${PORT} is in use (PID: ${EXISTING_PID}, process: ${EXISTING_CMD})" "端口 ${PORT} 已被占用 (PID: ${EXISTING_PID}, 进程: ${EXISTING_CMD})")"
    if [ -n "$EXISTING_ARGS" ]; then
        printf "  $(msg "Command" "命令"): %s\n" "$EXISTING_ARGS"
    fi
    printf "  $(msg "Kill this process and continue? [y/N]" "是否终止该进程并继续启动？[y/N]") "
    read -r REPLY </dev/tty 2>/dev/null || REPLY="n"
    REPLY=${REPLY:-n}
    case "$REPLY" in
        [Yy]*)
            kill "$EXISTING_PID" 2>/dev/null || true
            sleep 1
            if kill -0 "$EXISTING_PID" 2>/dev/null; then
                kill -9 "$EXISTING_PID" 2>/dev/null || true
                sleep 1
            fi
            ok "$(msg "Killed process occupying port (PID: ${EXISTING_PID})" "已终止占用端口的进程 (PID: ${EXISTING_PID})")"
            ;;
        *)
            die "$(msg "Port ${PORT} is occupied, please free it and retry" "端口 ${PORT} 被占用，请手动释放后重试")"
            ;;
    esac
fi

# ---------------- Step 6: Auto-detect public network / 公网环境检测 ----------------
# Detect public IP via external services (ifconfig.me, api.ipify.org, icanhazip.com)
# to determine if HTTPS should be auto-enabled for WebRTC microphone access.
log "$(msg "Detecting public network (querying ifconfig.me)..." "检测公网环境（查询 ifconfig.me）...")"
PUBLIC_IP=""
get_public_ip() {
    for url in "https://ifconfig.me" "https://api.ipify.org" "https://icanhazip.com"; do
        local ip
        ip=$(curl -s --max-time 3 "$url" 2>/dev/null | tr -d '[:space:]')
        if echo "$ip" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$'; then
            echo "$ip"
            return 0
        fi
    done
    return 1
}

# Get local IP for reference
LOCAL_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || ipconfig getifaddr en0 2>/dev/null || echo "127.0.0.1")

# Check if --https was explicitly passed
EXPLICIT_HTTPS=0
USE_HTTPS=0
for arg in "$@"; do
    [ "$arg" = "--https" ] && { USE_HTTPS=1; EXPLICIT_HTTPS=1; }
done

# Auto-detect: if not localhost and no explicit --https/--no-https, try to detect public IP and auto-enable HTTPS
AUTO_HTTPS=0
if [ "$EXPLICIT_HTTPS" -eq 0 ]; then
    PUBLIC_IP=$(get_public_ip 2>/dev/null || true)
    if [ -n "$PUBLIC_IP" ] && [ "$PUBLIC_IP" != "127.0.0.1" ]; then
        log "$(msg "Public IP detected: $PUBLIC_IP, auto-enabling HTTPS" "检测到公网 IP: $PUBLIC_IP，自动启用 HTTPS")"
        USE_HTTPS=1
        AUTO_HTTPS=1
    fi
fi

# ---------------- Step 7: HTTPS Self-signed Cert / HTTPS 自签证书 ----------------
CERT_DIR="certs"
CERT_FILE="$CERT_DIR/cert.pem"
KEY_FILE="$CERT_DIR/key.pem"

if [ "$USE_HTTPS" -eq 1 ]; then
    log "$(msg "Preparing HTTPS certificate..." "准备 HTTPS 证书...")"
    if [ -f "$CERT_FILE" ] && [ -f "$KEY_FILE" ]; then
        ok "$(msg "Certificate found: $CERT_FILE" "已有证书: $CERT_FILE")"
    else
        if ! command -v openssl >/dev/null 2>&1; then
            if [ "$AUTO_HTTPS" -eq 1 ]; then
                warn "$(msg "openssl not found, falling back to HTTP" "openssl 未安装，回退到 HTTP 模式")"
                USE_HTTPS=0
            else
                die "$(msg "openssl not installed, cannot generate self-signed cert" "openssl 未安装，无法生成自签证书")"
            fi
        fi
        if [ "$USE_HTTPS" -eq 1 ]; then
            mkdir -p "$CERT_DIR"
            log "$(msg "Generating self-signed certificate (valid 365 days)..." "生成自签证书（有效期 365 天）...")"
            openssl req -x509 -newkey rsa:2048 -nodes \
                -keyout "$KEY_FILE" -out "$CERT_FILE" \
                -days 365 -subj "/CN=localhost" \
                -addext "subjectAltName=DNS:localhost,IP:0.0.0.0" \
                2>/dev/null
            ok "$(msg "Certificate generated: $CERT_DIR/" "证书已生成: $CERT_DIR/")"
            echo ""
            warn "$(msg "Self-signed certificate: browser will show a security warning on first visit." "这是自签证书，浏览器首次访问会提示\"不安全\"")"
            msg "  Click \"Advanced\" → \"Proceed\" to continue." "  解决方法: 点击\"高级\" → \"继续前往\"即可正常使用"
            echo ""
        fi
    fi
fi

# ---------------- Step 8: Launch / 启动 ----------------
echo ""
printf "%b════════════════════════════════════════════════%b\n" "$BOLD" "$NC"
printf "%b🚀 $(msg "Launching TRTC AI Customer Service" "启动 TRTC AI 智能客服")%b\n" "$GREEN" "$NC"
printf "%b════════════════════════════════════════════════%b\n" "$BOLD" "$NC"
PROTO="http"
[ "$USE_HTTPS" -eq 1 ] && PROTO="https"
if [ -n "$PUBLIC_IP" ] && [ "$PUBLIC_IP" != "127.0.0.1" ]; then
    printf "   $(msg "Public" "公网"): %b%b${PROTO}://${PUBLIC_IP}:%s%b\n" "$CYAN" "$BOLD" "$PORT" "$NC"
    printf "   $(msg "Local" "内网"):  %b${PROTO}://${LOCAL_IP}:%s%b\n" "$CYAN" "$PORT" "$NC"
    printf "   $(msg "Local" "本地"):  %b${PROTO}://localhost:%s%b\n" "$CYAN" "$PORT" "$NC"
else
    printf "   $(msg "Visit" "访问"): %b%b${PROTO}://localhost:%s%b\n" "$CYAN" "$BOLD" "$PORT" "$NC"
fi
printf "   $(msg "Stop" "停止"): %bCtrl+C%b\n" "$YELLOW" "$NC"
printf "%b════════════════════════════════════════════════%b\n" "$BOLD" "$NC"
echo ""

if [ "$USE_HTTPS" -eq 1 ]; then
    exec "$VENV_PY" app.py --https
else
    exec "$VENV_PY" app.py
fi

#!/bin/bash

# 小龙虾安全点对点加密通讯技能
# 版本: 1.0.14
# 作者: puppetcat-fire (柏然)
# GitHub: https://github.com/puppetcat-fire/openclaw-skills

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置目录
CONFIG_DIR="$HOME/.openclaw/secure-p2p"
KEYRING_DIR="$CONFIG_DIR/keyring"
CONTACTS_DIR="$CONFIG_DIR/contacts"
LOG_DIR="$CONFIG_DIR/logs"

# 初始化函数
init() {
    echo -e "${BLUE}🔒 初始化加密身份...${NC}"
    
    # 创建目录
    mkdir -p "$KEYRING_DIR" "$CONTACTS_DIR" "$LOG_DIR"
    
    # 生成RSA密钥对
    echo -e "${BLUE}生成RSA-2048密钥对...${NC}"
    openssl genrsa -out "$KEYRING_DIR/private.pem" 2048 2>/dev/null
    openssl rsa -in "$KEYRING_DIR/private.pem" -pubout -out "$KEYRING_DIR/public.pem" 2>/dev/null
    
    # 生成身份ID
    local identity_id="claw_$(openssl rand -hex 12)"
    echo "$identity_id" > "$CONFIG_DIR/identity.id"
    
    # 生成指纹
    local fingerprint=$(openssl dgst -sha256 "$KEYRING_DIR/public.pem" | awk '{print $2}' | cut -c 1-16)
    echo "$fingerprint" > "$CONFIG_DIR/fingerprint.txt"
    
    echo -e "${GREEN}✅ 身份初始化完成！${NC}"
    echo -e "身份ID: $identity_id"
    echo -e "指纹: $fingerprint"
    echo -e "公钥: $(base64 -w0 "$KEYRING_DIR/public.pem" 2>/dev/null | head -c 100)..."
}

# 显示身份信息
identity() {
    if [ ! -f "$CONFIG_DIR/identity.id" ]; then
        echo -e "${RED}❌ 请先运行 init 初始化身份${NC}"
        return 1
    fi
    
    local identity_id=$(cat "$CONFIG_DIR/identity.id")
    local fingerprint=$(cat "$CONFIG_DIR/fingerprint.txt")
    local public_key=$(base64 -w0 "$KEYRING_DIR/public.pem" 2>/dev/null)
    
    echo -e "${BLUE}🦞 你的身份信息：${NC}"
    echo -e "身份ID: $identity_id"
    echo -e "指纹: $fingerprint"
    echo -e "公钥: ${public_key:0:100}..."
    echo ""
    echo -e "${YELLOW}📋 分享以下信息给朋友：${NC}"
    echo "身份ID: $identity_id"
    echo "公钥: $public_key"
}

# 添加联系人
add_contact() {
    local contact_id="$1"
    local contact_name="$2"
    local public_key="$3"
    
    if [ -z "$contact_id" ] || [ -z "$contact_name" ] || [ -z "$public_key" ]; then
        echo -e "${RED}用法: $0 add-contact <联系人ID> <姓名> <公钥base64>${NC}"
        return 1
    fi
    
    echo "$public_key" | base64 -d > "$CONTACTS_DIR/$contact_id.pub" 2>/dev/null
    echo "$contact_name" > "$CONTACTS_DIR/$contact_id.name"
    
    echo -e "${GREEN}✅ 联系人 $contact_name 添加成功！${NC}"
}

# 发送加密消息
send_message() {
    local recipient="$1"
    local message="$2"
    
    if [ -z "$recipient" ] || [ -z "$message" ]; then
        echo -e "${RED}用法: $0 send <联系人ID> <消息>${NC}"
        return 1
    fi
    
    if [ ! -f "$CONTACTS_DIR/$recipient.pub" ]; then
        echo -e "${RED}❌ 联系人 $recipient 不存在${NC}"
        return 1
    fi
    
    echo -e "${BLUE}🔐 加密消息...${NC}"
    
    # 生成随机会话密钥
    local session_key=$(openssl rand -hex 32)
    local iv=$(openssl rand -hex 12)
    
    # 使用AES加密消息
    local encrypted_msg=$(echo -n "$message" | openssl enc -aes-256-gcm -K "$session_key" -iv "$iv" -a -A 2>/dev/null)
    
    # 使用对方公钥加密会话密钥
    local encrypted_key=$(echo -n "$session_key" | openssl rsautl -encrypt -pubin -inkey "$CONTACTS_DIR/$recipient.pub" -oaep | base64 -w0)
    
    # 创建消息包
    local message_package=$(cat <<EOF
{
  "version": "1.0",
  "sender": "$(cat "$CONFIG_DIR/identity.id")",
  "recipient": "$recipient",
  "timestamp": "$(date -Iseconds)",
  "encryptedKey": "$encrypted_key",
  "iv": "$iv",
  "encryptedMsg": "$encrypted_msg"
}
EOF
)
    
    echo -e "${GREEN}✅ 消息加密完成！${NC}"
    echo ""
    echo -e "${YELLOW}📨 加密消息包：${NC}"
    echo "$message_package"
    echo ""
    echo -e "${YELLOW}📋 复制以上内容发送给朋友${NC}"
}

# 接收和解密消息
receive_message() {
    local message_package="$1"
    
    if [ -z "$message_package" ]; then
        echo -e "${RED}用法: $0 receive '<消息包JSON>'${NC}"
        return 1
    fi
    
    echo -e "${BLUE}🔓 解密消息...${NC}"
    
    # 解析消息包
    local encrypted_key=$(echo "$message_package" | jq -r '.encryptedKey')
    local iv=$(echo "$message_package" | jq -r '.iv')
    local encrypted_msg=$(echo "$message_package" | jq -r '.encryptedMsg')
    local sender=$(echo "$message_package" | jq -r '.sender')
    
    # 使用私钥解密会话密钥
    local session_key=$(echo "$encrypted_key" | base64 -d | openssl rsautl -decrypt -inkey "$KEYRING_DIR/private.pem" -oaep 2>/dev/null)
    
    if [ -z "$session_key" ]; then
        echo -e "${RED}❌ 解密失败：无效的消息包或密钥不匹配${NC}"
        return 1
    fi
    
    # 使用AES解密消息
    local decrypted_msg=$(echo "$encrypted_msg" | openssl enc -aes-256-gcm -d -K "$session_key" -iv "$iv" -a -A 2>/dev/null)
    
    echo -e "${GREEN}✅ 消息解密成功！${NC}"
    echo ""
    echo -e "${YELLOW}📨 来自 $sender 的消息：${NC}"
    echo "$decrypted_msg"
}

# 帮助信息
show_help() {
    echo -e "${BLUE}🦞 小龙虾安全点对点加密通讯技能${NC}"
    echo -e "版本: 1.0.2"
    echo ""
    echo -e "${GREEN}可用命令：${NC}"
    echo "  init                    - 初始化加密身份"
    echo "  identity                - 显示身份信息"
    echo "  add-contact <id> <name> <pubkey> - 添加联系人"
    echo "  send <联系人> <消息>     - 发送加密消息"
    echo "  receive '<消息包>'       - 接收和解密消息"
    echo "  --help                  - 显示帮助信息"
    echo ""
    echo -e "${YELLOW}示例：${NC}"
    echo "  $0 init"
    echo "  $0 identity"
    echo "  $0 add-contact alice \"Alice\" \"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...\""
    echo "  $0 send alice \"你好，这是加密消息！\""
    echo "  $0 receive '{\"version\":\"1.0\",\"sender\":\"claw_abc123\",...}'"
    echo ""
    echo -e "${BLUE}GitHub: https://github.com/puppetcat-fire/openclaw-skills${NC}"
}

# 主函数
main() {
    case "$1" in
        init)
            init
            ;;
        identity)
            identity
            ;;
        add-contact)
            shift
            add_contact "$@"
            ;;
        send)
            shift
            send_message "$@"
            ;;
        receive)
            shift
            receive_message "$@"
            ;;
        --help|-h|help)
            show_help
            ;;
        *)
            echo -e "${RED}未知命令: $1${NC}"
            show_help
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"
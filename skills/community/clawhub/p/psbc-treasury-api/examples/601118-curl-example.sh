#!/bin/bash
# 账户余额实时查询 - 601118 接口示例
# 安全级别：10

# 配置参数（请根据实际情况修改）
BASE_URL="https://olt.api-test.psbc.com:9902/gateway/std/"
REQ_SYS_CODE="99711940001"  # 接入系统代码
USER_CERT_SN="0817fbeecc848"  # 用户证书序列号
BANK_CERT_SN="12e15039e89ff93c"  # 银行证书序列号

# 生成系统跟踪号：时间戳 (14 位) + 接入系统代码 (12 位) + 6 位唯一序列号
TX_TIME=$(date +%Y%m%d%H%M%S%3N)
SYS_TRACK_NO="${TX_TIME:0:14}${REQ_SYS_CODE}$(printf '%06d' $RANDOM)"

# 业务报文（明文）
BUSINESS_PAYLOAD='{
  "txCode": "100016",
  "tenantID": "eam_tenant_a_0001",
  "sendTime": "'$(date +%Y%m%d%H%M%S)'",
  "srcSysId": "140001",
  "bankAccno": "951011013000006323"
}'

# 注意：实际使用时需要对业务报文进行 SM4 加密，并对签名数据进行国密签名
# 以下 encData 和 sign 为示例占位符，实际需调用国密库生成

# 完整请求报文
REQUEST_PAYLOAD=$(cat <<EOF
{
  "txComm": {
    "sysTrackNo": "${SYS_TRACK_NO}",
    "reqSysCode": "${REQ_SYS_CODE}",
    "txCode": "601118",
    "txTime": "${TX_TIME}",
    "securityLevel": "10",
    "sign": "<SM2 签名值 Base64>",
    "bankCertSN": "${BANK_CERT_SN}",
    "userCertSN": "${USER_CERT_SN}",
    "encData": "<SM4 加密后的业务报文 Base64>",
    "encKey": "<SM4 密钥使用银行证书加密后的 Base64>"
  }
}
EOF
)

# 发送请求
curl -X POST "${BASE_URL}" \
  -H "Content-Type: application/json;charset=UTF-8" \
  -d "${REQUEST_PAYLOAD}" \
  -v

# 响应示例（解密后）：
# {
#   "txComm": {
#     "respCode": "0000000000000000",
#     "respDesc": "交易成功"
#   },
#   "txCode": "100016",
#   "tenantID": "eam_tenant_a_0001",
#   "sendTime": "20250303163811",
#   "feedbackTime": "20250303163815",
#   "respCode": "000000",
#   "respInfo": "成功",
#   "data": {
#     "bankAccno": "951011013000006323",
#     "accBal": "1000000.00",
#     "accAvalBal": "1000000.00"
#   }
# }

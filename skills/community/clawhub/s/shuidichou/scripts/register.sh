#!/bin/bash
# 水滴筹筹款线索登记
# 用法: bash register.sh <手机号>

MOBILE="$1"
API="https://api.shuidichou.com/api/cf/v4/toufang/register-mobile"

if [ -z "$MOBILE" ]; then
  echo '{"error": "请提供手机号"}'
  exit 1
fi

# 简单校验手机号格式（11位数字，1开头）
if ! echo "$MOBILE" | grep -qE '^1[3-9][0-9]{9}$'; then
  echo '{"error": "手机号格式不正确，请输入11位有效手机号"}'
  exit 1
fi

# 接口使用 form 表单格式
response=$(curl -s -X POST "$API" \
  -d "mobile=$MOBILE&relation=其他&channel=openclaw-skills" 2>/dev/null)

if [ $? -ne 0 ] || [ -z "$response" ]; then
  echo '{"error": "提交失败，请稍后重试"}'
  exit 1
fi

echo "$response"

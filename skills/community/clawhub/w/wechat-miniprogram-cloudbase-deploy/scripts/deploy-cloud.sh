#!/usr/bin/env bash
# 云开发小程序 —— 云函数一键批量部署脚本（配合 SKILL.md 的部署流程）
# 前置：npm i -g @cloudbase/cli && tcb login（首次打开浏览器授权，或用密钥）
# 用法：bash scripts/deploy-cloud.sh
# 注意：trial env 固定 ap-shanghai，所有命令都要带 -r ap-shanghai（见 pitfalls.md）
set -e

echo "==> 1) 登录 CloudBase"
tcb login

echo "==> 2) 部署云函数（云端安装依赖）"
for fn in login api seed dailyPush; do
  echo "  deploying $fn ..."
  tcb fn deploy "$fn" --force -r ap-shanghai
done

echo "==> 3) 首次部署后，手动触发一次 seed 预置默认数据"
tcb fn invoke seed -r ap-shanghai || echo "（如未配置 env，可在微信开发者工具右键 seed -> 测试 触发）"

echo ""
echo "==> 4) 必须在 CloudBase/微信开发者工具控制台建唯一索引（否则幂等写入无兜底）："
echo "   集合 checkins          : 唯一索引 { openid: 1, date: 1 }"
echo "   集合 gang_memberships  : 唯一索引 { openid: 1, gangId: 1 }"
echo "   （集合/索引名按你的业务改，这里是示例）"
echo ""
echo "==> 5) 小程序代码用 scripts/upload.js 上传（miniprogram-ci）；审核/发布在 MP 后台人工操作。"
echo "完成。"

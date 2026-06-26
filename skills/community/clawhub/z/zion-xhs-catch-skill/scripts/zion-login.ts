/**
 * Zion 凭证保存脚本
 * 直接接收用户提供的「好痛 Howtone」同步 Token，并保存到 .zion/credentials.yaml
 * 
 * 用法:
 *   npx ts-node zion-login.ts --token="你的同步Token"
 */

import * as fs from 'fs';
import * as path from 'path';

const PROJECT_EX_ID = 'rmLyJ0ZJXK8';
const CRED_PATH = path.resolve(process.cwd(), '.zion', 'credentials.yaml');

function decodeJwt(token: string): any {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) return null;
    const payload = Buffer.from(parts[1], 'base64').toString('utf-8');
    return JSON.parse(payload);
  } catch {
    return null;
  }
}

async function main() {
  const args = process.argv.slice(2);
  const token = args.find(a => a.startsWith('--token='))?.split('=')[1];

  if (!token) {
    console.log('用法: npx ts-node zion-login.ts --token="好痛用户中心的同步Token"');
    process.exit(1);
  }

  console.log(`正在保存「好痛 Howtone」同步 Token...`);

  // 尝试解析 Token 获取一些基本信息（非必需，失败不影响保存）
  const jwtPayload = decodeJwt(token);
  let username = '情报员';
  let userId = '';
  let expiryDate = new Date(Date.now() + 7 * 24 * 3600 * 1000).toISOString(); // 默认 7 天

  if (jwtPayload) {
    userId = jwtPayload.userId || jwtPayload.user_id || jwtPayload.sub || '';
    if (jwtPayload.username) username = jwtPayload.username;
    else if (jwtPayload.name) username = jwtPayload.name;
    else if (jwtPayload.userId) username = `用户_${jwtPayload.userId}`;
    
    if (jwtPayload.exp) {
      expiryDate = new Date(jwtPayload.exp * 1000).toISOString();
    }
  }

  try {
    // 确保 .zion 目录存在
    if (!fs.existsSync(path.dirname(CRED_PATH))) {
      fs.mkdirSync(path.dirname(CRED_PATH), { recursive: true });
    }

    const newCreds = `
project:
  exId: "${PROJECT_EX_ID}"
  admin_token:
    token: "${token}"
    expiry: "${expiryDate}"
account:
  username: "${username}"
  user_id: "${userId}"
`;
    fs.writeFileSync(CRED_PATH, newCreds.trim());
    console.log(`✅ 同步 Token 保存成功！`);
    console.log(`🚀 弦外 Overtone 已就绪，准备好捕获商机了吗？`);
    console.log(`✨ 凭据已保存到: ${CRED_PATH}`);
  } catch (err) {
    console.error('❌ 保存失败:', (err as Error).message);
    process.exit(1);
  }
}

main();

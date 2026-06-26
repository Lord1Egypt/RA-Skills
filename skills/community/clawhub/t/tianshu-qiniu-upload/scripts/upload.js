#!/usr/bin/env node
/**
 * 七牛上传脚本 - 供 OpenClaw Skill 调用
 * 用法: node upload.js <文件路径>
 * 输出: 上传后的完整 URL（单行）
 *
 * 环境变量: QINIU_ACCESS_KEY, QINIU_SECRET_KEY, QINIU_BUCKET, QINIU_DOMAIN, QINIU_PREFIX
 */

const fs = require('fs');
const path = require('path');

const filePath = process.argv[2];
if (!filePath || !fs.existsSync(filePath)) {
  console.error('用法: node upload.js <文件路径>');
  process.exit(1);
}

const QINIU_ACCESS_KEY = process.env.QINIU_ACCESS_KEY;
const QINIU_SECRET_KEY = process.env.QINIU_SECRET_KEY;
const QINIU_BUCKET = process.env.QINIU_BUCKET;
const QINIU_DOMAIN = (process.env.QINIU_DOMAIN || '').replace(/\/$/, '');
const QINIU_PREFIX = (process.env.QINIU_PREFIX || 'uploads').replace(/\/$/, '');

if (!QINIU_ACCESS_KEY || !QINIU_SECRET_KEY || !QINIU_BUCKET || !QINIU_DOMAIN) {
  console.error('请设置环境变量: QINIU_ACCESS_KEY, QINIU_SECRET_KEY, QINIU_BUCKET, QINIU_DOMAIN');
  process.exit(1);
}

const ext = path.extname(filePath) || '';
const key = `${QINIU_PREFIX}/${Date.now()}-${Math.random().toString(36).slice(2, 10)}${ext}`;

const TIMEOUT_MS = 60000;

async function upload() {
  let qiniu;
  try {
    qiniu = require('qiniu');
  } catch (e) {
    console.error('请先执行: cd ' + path.dirname(__dirname) + ' && npm install');
    process.exit(1);
  }

  const mac = new qiniu.auth.digest.Mac(QINIU_ACCESS_KEY, QINIU_SECRET_KEY);
  const config = new qiniu.conf.Config();
  config.zone = qiniu.zone.Zone_z0;
  const formUploader = new qiniu.form_up.FormUploader(config);
  const putExtra = new qiniu.form_up.PutExtra();
  const putPolicy = new qiniu.rs.PutPolicy({ scope: `${QINIU_BUCKET}:${key}` });
  const uploadToken = putPolicy.uploadToken(mac);

  const result = await Promise.race([
    new Promise((resolve, reject) => {
      formUploader.putFile(uploadToken, key, filePath, putExtra, (err, body, info) => {
        if (err) reject(err);
        else if (info.statusCode === 200) resolve(`${QINIU_DOMAIN}/${key}`);
        else reject(new Error(`${info.statusCode} ${JSON.stringify(body)}`));
      });
    }),
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error('上传超时')), TIMEOUT_MS)
    ),
  ]);

  console.log(result);
}

upload().catch((e) => {
  console.error(e.message || e);
  process.exit(1);
});

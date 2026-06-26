# 部署配置

## NPM 脚本

```json
"scripts": {
  "dev": "vite",
  "start": "pnpm run dev",
  "build": "vite build",
  "preview": "vite preview",
  "build:stage": "pnpm run build --mode staging",
  "build:prod": "pnpm run build --mode production",
  "clean": "rimraf dist.zip",
  "zip": "node export-zip.cjs",
  "upload:stage": "node ftp-deploy.js stage",
  "upload:prod": "node ftp-deploy.js production",
  "deploy:stage": "pnpm run build:stage && pnpm run clean && pnpm run zip && pnpm run upload:stage",
  "deploy:prod": "pnpm run build:prod && pnpm run clean && pnpm run zip && pnpm run upload:prod"
}
```

---

## 压缩脚本 (export-zip.cjs)

```javascript
const fs = require('fs');
const archiver = require('archiver');

const homedir = __dirname;
const target = ['dist'];

const output = fs.createWriteStream(homedir + '/dist.zip');
const archive = archiver('zip', { zlib: { level: 9 } });

archive.on('error', function (err) { throw err; });

output.on('close', function () {
    console.log(`压缩完毕，大小: ${(archive.pointer() / 1024 / 1024).toFixed(1)} MB`);
});

archive.pipe(output);
for (let i of target) {
    archive.directory(i, i);
}
archive.finalize();
```

---

## FTP 部署脚本 (ftp-deploy.js)

> ⚠️ **安全提示**：部署凭证**不要**硬编码在脚本中或使用 Git 提交。通过环境变量或 `.env` 文件（已加入 `.gitignore`）传入。生产环境部署只在显式确认后执行。

```javascript
import FtpDeploy from "ftp-deploy";
import { fileURLToPath } from "node:url";
import path from "node:path";

const ftpDeploy = new FtpDeploy();
const env = process.argv.splice(2)[0];
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 从环境变量读取部署凭证，未设置时报错
function getEnvConfig(targetEnv) {
    const prefix = targetEnv === 'production' ? 'PROD' : 'STAGE';
    const user = process.env[`${prefix}_FTP_USER`];
    const password = process.env[`${prefix}_FTP_PASSWORD`];
    const host = process.env[`${prefix}_FTP_HOST`];
    const remoteRoot = process.env[`${prefix}_FTP_REMOTE_ROOT`];
    if (!user || !password || !host || !remoteRoot) {
        console.error(`\x1b[31mError: Missing ${prefix}_FTP_* environment variables\x1b[0m`);
        process.exit(1);
    }
    return { user, password, host, remoteRoot };
}

if (!env || !['stage', 'production'].includes(env)) {
    console.error('\x1b[31m%s\x1b[0m', 'error: 环境参数错误，请使用 stage 或 production');
    process.exit(1);
}

const envConfig = getEnvConfig(env);

const config = {
    ...envConfig,
    port: 21,
    localRoot: __dirname + "/",
    include: ["dist.zip"],
    deleteRemote: false,
    forcePasv: true,
    sftp: false,
};

ftpDeploy.deploy(config)
    .then(() => console.log('upload completed'))
    .catch((err) => console.log(err));
```

**使用方式：**

```bash
# 临时设置（单次部署）
STAGE_FTP_USER=myuser STAGE_FTP_PASSWORD=mypass STAGE_FTP_HOST=ftp.example.com STAGE_FTP_REMOTE_ROOT=/staging/ pnpm run upload:stage

# 或通过 .env.local 文件（需已加入 .gitignore）
# 在 .env.local 中写入：
#   STAGE_FTP_USER=myuser
#   STAGE_FTP_PASSWORD=mypass
#   STAGE_FTP_HOST=ftp.example.com
#   STAGE_FTP_REMOTE_ROOT=/staging/
#   PROD_FTP_USER=myuser
#   PROD_FTP_PASSWORD=mypass
#   PROD_FTP_HOST=ftp.example.com
#   PROD_FTP_REMOTE_ROOT=/prod/
```

---

## 部署依赖

```bash
pnpm add -D archiver ftp-deploy rimraf
```

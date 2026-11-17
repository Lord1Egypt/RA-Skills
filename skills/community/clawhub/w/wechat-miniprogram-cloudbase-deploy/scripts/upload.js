// 微信小程序前端上传脚本（miniprogram-ci JS API 版）
// 用 JS API 而非裸命令行：返回结构化错误，避免 zsh PIPESTATUS 误判（见 pitfalls.md 踩坑 4）。
//
// 用法：
//   APPID=wx... PROJECT=/path/to/project KEY=/path/to/private.key \
//   VERSION=1.0.0 DESC="云开发版 MVP" node upload.js
//
// 环境变量（均必填，无默认值以免误传）：
//   APPID     小程序真实 AppID
//   PROJECT   项目根目录（含 project.config.json / miniprogram/）
//   KEY       上传私钥 .key 文件的本地绝对路径（切勿把密钥内容贴进对话）
//   VERSION   版本号（默认 1.0.0）
//   DESC      备注（默认 "cloudbase deploy"）

const ci = require('miniprogram-ci');

const APPID = process.env.APPID;
const PROJECT = process.env.PROJECT;
const KEY = process.env.KEY;
const VERSION = process.env.VERSION || '1.0.0';
const DESC = process.env.DESC || 'cloudbase deploy';

for (const [k, v] of [['APPID', APPID], ['PROJECT', PROJECT], ['KEY', KEY]]) {
  if (!v) {
    console.error(`[upload] 缺少环境变量 ${k}`);
    process.exit(2);
  }
}

(async () => {
  let project;
  try {
    project = new ci.Project({
      appid: APPID,
      type: 'miniProgram',
      projectPath: PROJECT,
      privateKeyPath: KEY,
      // 只打包 miniprogram/，排除无关目录（密钥/后端/云函数都不会进包）
      ignores: ['node_modules/**', 'cloudfunctions/**', 'server/**', '*.key', '*.md'],
    });
  } catch (e) {
    console.error('[upload] 无法初始化项目(检查路径/密钥):', e && e.message);
    process.exit(2);
  }

  try {
    const res = await ci.upload({
      project,
      version: VERSION,
      desc: DESC,
      setting: { es6: true, minified: true, urlCheck: false },
    });
    console.log('[upload] SUCCESS:', JSON.stringify(res));
    process.exit(0);
  } catch (e) {
    console.error('[upload] FAILED');
    console.error('  errCode:', e && e.errCode);
    console.error('  errMsg :', e && e.errMsg);
    if (e && e.errMsg && /invalid ip/i.test(String(e.errMsg))) {
      console.error('\n提示：命中「上传 IP 白名单」拦截（见 pitfalls.md 踩坑 3）：');
      console.error('   MP 后台「开发设置 → 小程序代码上传 IP 白名单」');
      console.error('   要么关掉开关，要么把本机公网 IPv4 加进去（查: curl -s https://ifconfig.me）');
      console.error('   注意：白名单 UI 仅收 IPv4，IPv6 出口无法加入，只能关开关。');
    }
    process.exit(1);
  }
})();

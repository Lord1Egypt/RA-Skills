const fs = require('fs');
const http = require('http');

try {
  require.resolve('form-data');
} catch(e) {
  console.log("Installing form-data wrapper dynamically...");
  const { execSync } = require('child_process');
  execSync('npm install form-data --no-save', { stdio: 'ignore' });
}

const FormData = require('form-data');
const args = process.argv.slice(2);

let promptText = "模特自然走动两步，随后自信地侧身转身，全面展示身上的细条纹衬衫和领带搭配，面料质感真实，高质量专业摄影棚光影，时尚大片感。";
let imagePath = null;
let sessionToken = "b79fcda2d907241e773cb52960b39978"; // 默认缓存的认证 session
let model = "jimeng-video-3.0-pro";
let port = 5100;

// Parse basic args: node generate.js --prompt "..." --image /tmp/a.jpg
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--image') imagePath = args[i+1];
  if (args[i] === '--prompt') promptText = args[i+1];
  if (args[i] === '--session') sessionToken = args[i+1];
  if (args[i] === '--model') model = args[i+1];
}

const form = new FormData();
form.append('prompt', promptText);
form.append('model', model);
form.append('duration', '5');

if (imagePath && fs.existsSync(imagePath)) {
    console.log(`[+] 成功挂载原生图片流: ${imagePath}`);
    form.append('files', fs.createReadStream(imagePath));
} else {
    console.log(`[-] 未发现本地图片 (--image 参数无效或文件不存在): 执行纯文生视频降级 (Warning: 可能浪费积分)`);
    process.exit(1); // 直接抛错防止扣钱
}

console.log(`[+] 开始请求 Uni Vision 原生接口...`);

const options = {
  hostname: 'localhost',
  port: port,
  path: '/v1/videos/generations',
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + sessionToken,
    ...form.getHeaders()
  }
};

const req = http.request(options, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    console.log("[+] 请求发送成功，后台已入列！响应结果：\n", data);
  });
});

req.on('error', (e) => {
    console.error("[-] API Server (localhost:5100) 请求失败: ", e);
});
form.pipe(req);

#!/usr/bin/env node
const url = 'https://ilinkai.weixin.qq.com/ilink/bot/get_bot_qrcode?bot_type=3';

const main = async () => {
  const res = await fetch(url);
  if (!res.ok) {
    const body = await res.text().catch(() => '');
    console.error(`HTTP ${res.status} ${res.statusText}`);
    if (body) console.error(body);
    process.exit(1);
  }
  const data = await res.json();
  if (data.qrcode_img_content) console.log(data.qrcode_img_content);
  if (data.qrcode) console.log(`QRCODE=${data.qrcode}`);
  if (!data.qrcode_img_content && !data.qrcode) {
    console.log(JSON.stringify(data, null, 2));
  }
};

main().catch((err) => {
  console.error(err?.stack || String(err));
  process.exit(1);
});

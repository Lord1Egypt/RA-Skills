
const APIClient = require('./api_client');

async function go() {
  console.log('1. 开始检查视频');
  const client = new APIClient();
  
  console.log('2. 正在登录...');
  const loginResult = await client.login('18098901246', '123456');
  if (!loginResult) {
    console.log('登录失败！');
    return;
  }
  console.log('3. 登录成功！');
  
  console.log('4. 正在获取视频列表...');
  const videoList = await client.get_video_list(1, 10);
  if (!videoList) {
    console.log('获取视频列表失败！');
    return;
  }
  
  console.log('\n=== 最近的视频 ===');
  let records = [];
  if (Array.isArray(videoList.data)) {
    records = videoList.data;
  } else if (videoList.data) {
    if (videoList.data.records) {
      records = videoList.data.records;
    }
  }
  
  let i = 0;
  while (i &lt; records.length) {
    const v = records[i];
    console.log((i+1) + '. ' + v.title + ' - ' + v.status);
    if (v.videoUrl) {
      console.log('   链接: ' + v.videoUrl);
    }
    i = i + 1;
  }
}

go().catch(function(err) {
  console.error('出错了:', err);
});

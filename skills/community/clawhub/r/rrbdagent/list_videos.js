
const RRBDClient = require('./api_client');
const config = require('./config.json');

async function listVideos() {
  console.log('============================================================');
  console.log('RRBD 视频列表查询');
  console.log('============================================================');

  const client = new RRBDClient(config);

  try {
    // 1. 登录
    console.log('\n1. 登录中...');
    console.log('   账号:', config.username);
    await client.login();
    console.log('   登录成功！');

    // 2. 查询视频列表
    console.log('\n2. 查询视频列表...');
    const videoList = await client.getVideoList();

    console.log('\n视频列表:');
    console.log('============================================================');

    if (videoList &amp;&amp; videoList.data &amp;&amp; videoList.data.length &gt; 0) {
      videoList.data.forEach((video, index) =&gt; {
        const statusText = {
          'processing': '⏳ 处理中',
          'succeed': '✅ 成功',
          'failed': '❌ 失败'
        }[video.status] || video.status;

        console.log(`\n${index + 1}. [${statusText}] ${video.title || '无标题'}`);
        console.log(`   ID: ${video.id}`);
        console.log(`   状态: ${video.status}`);
        console.log(`   创建时间: ${video.createDate}`);

        if (video.status === 'succeed' &amp;&amp; video.videoUrl) {
          console.log(`   ✨ 视频URL: ${video.videoUrl}`);
        }

        if (video.message) {
          console.log(`   消息: ${video.message}`);
        }
      });
    } else {
      console.log('   暂无视频');
    }

    console.log('\n============================================================');

  } catch (error) {
    console.error('\n❌ 错误:', error.message);
    if (error.response) {
      console.error('响应数据:', error.response.data);
    }
  }
}

listVideos();

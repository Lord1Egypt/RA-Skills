
const RRBDClient = require('./api_client');
const config = require('./config.json');

async function listVideos() {
  console.log('RRBD 视频列表查询');
  console.log('====================');

  const client = new RRBDClient(config);

  try {
    console.log('\n1. 登录中...');
    await client.login();
    console.log('   登录成功！');

    console.log('\n2. 查询视频列表...');
    const videoList = await client.getVideoList();

    console.log('\n视频列表:');
    console.log('------------------------');

    if (videoList && videoList.data && videoList.data.length > 0) {
      videoList.data.forEach((video, index) => {
        const statusText = {
          'processing': '处理中',
          'succeed': '成功',
          'failed': '失败'
        }[video.status] || video.status;

        console.log(`\n${index + 1}. [${statusText}] ${video.title || '无标题'}`);
        console.log(`   ID: ${video.id}`);
        console.log(`   创建时间: ${video.createDate}`);

        if (video.status === 'succeed' && video.videoUrl) {
          console.log(`   视频URL: ${video.videoUrl}`);
        }
      });
    } else {
      console.log('   暂无视频');
    }

  } catch (error) {
    console.error('\n错误:', error.message);
  }
}

listVideos();

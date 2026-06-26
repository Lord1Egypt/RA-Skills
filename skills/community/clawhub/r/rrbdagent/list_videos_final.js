
const APIClient = require('./api_client');

async function listVideos() {
  console.log('RRBD 视频列表查询');
  console.log('====================');

  const client = new APIClient();

  try {
    console.log('\n1. 登录中...');
    const loginResult = await client.login('18098901246', '123456');
    
    if (!loginResult) {
      console.log('登录失败！');
      return;
    }
    
    console.log('   登录成功！');

    console.log('\n2. 查询视频列表...');
    const videoList = await client.get_video_list(1, 20);

    console.log('\n视频列表:');
    console.log('------------------------');

    if (videoList &amp;&amp; videoList.data &amp;&amp; videoList.data.length &gt; 0) {
      videoList.data.forEach((video, index) =&gt; {
        const statusText = {
          'processing': '处理中',
          'succeed': '成功',
          'failed': '失败'
        }[video.status] || video.status;

        console.log(`\n${index + 1}. [${statusText}] ${video.title || '无标题'}`);
        console.log(`   ID: ${video.id}`);
        console.log(`   创建时间: ${video.createDate}`);

        if (video.status === 'succeed' &amp;&amp; video.videoUrl) {
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

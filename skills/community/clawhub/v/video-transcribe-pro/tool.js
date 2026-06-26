/**
 * video-to-text Skill - OpenClaw Tool Wrapper
 * 
 * 将视频/音频文件转换为文字
 */

const { execSync } = require('child_process');
const path = require('path');

/**
 * 视频转文字工具
 * @param {Object} params 参数
 * @param {string} params.url 视频/音频文件URL
 * @param {string} params.language 语言代码 (zh/en/ja)
 * @param {string} params.output_format 输出格式 (text/srt)
 * @returns {Object} 转写结果
 */
async function video_to_text(params) {
  const { url, language = 'zh', output_format = 'text' } = params;
  
  if (!url) {
    return {
      success: false,
      error: '请提供视频/音频文件的URL'
    };
  }

  try {
    // 构建命令
    const scriptPath = path.join(__dirname, 'index.js');
    const args = [
      'node',
      scriptPath,
      '--url', url,
      '--language', language,
      '--format', output_format
    ];
    
    // 执行转写
    const output = execSync(args.join(' '), {
      encoding: 'utf-8',
      maxBuffer: 10 * 1024 * 1024, // 10MB
      timeout: 300000 // 5分钟超时
    });

    return {
      success: true,
      result: output,
      format: output_format
    };
  } catch (error) {
    return {
      success: false,
      error: error.message || '转写失败'
    };
  }
}

module.exports = {
  video_to_text
};

// 如果直接运行
if (require.main === module) {
  const url = process.argv[2];
  const language = process.argv[3] || 'zh';
  const format = process.argv[4] || 'text';
  
  video_to_text({ url, language, output_format: format })
    .then(result => {
      console.log(JSON.stringify(result, null, 2));
    })
    .catch(err => {
      console.error(JSON.stringify({ success: false, error: err.message }));
    });
}

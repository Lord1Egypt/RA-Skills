export const ERROR_MESSAGES = {
  no_file_path: '抱歉，没有收到音频文件，请重试。',
  file_not_found: '抱歉，音频文件没找到，可能是网络不稳定，请重试。',
  file_empty: '抱歉，音频文件是空的，可能是网络不稳定，请重试。',
  file_too_small: '抱歉，音频文件不完整，可能是网络不稳定，请重试。',
  file_stale: '抱歉，音频文件已过期，可能是网络不稳定，请重试。',
  transcription_failed: '抱歉，语音识别失败了，请重试。',
  synthesis_failed: '抱歉，语音生成失败了，请重试。',
  timeout: '抱歉，处理超时了，请稍后重试。'
};

export function formatError(error, details = '') {
  return {
    success: false,
    error,
    message: ERROR_MESSAGES[error] || ERROR_MESSAGES.transcription_failed,
    details
  };
}

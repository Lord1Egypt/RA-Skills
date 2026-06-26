// Configuration module – isolates environment access without network dependencies
function getYoutubeApiKey() {
  return process.env.YOUTUBE_API_KEY;
}

module.exports = {
  getYoutubeApiKey
};

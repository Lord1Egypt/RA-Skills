'use strict'

const sourceOrigin = 'https://willing-video-test.oss-cn-shanghai.aliyuncs.com'
const previewOrigin = 'https://media.vibbit.cn'

// Display URLs must use the media origin; keep paths, queries and original API values intact.
function previewUrl(url) {
  if (typeof url !== 'string' || !url.startsWith(sourceOrigin + '/')
    || /[\u0000-\u0020\\]/.test(url)) return url
  return previewOrigin + url.slice(sourceOrigin.length)
}

function avatarPreviews(result) {
  if (!Array.isArray(result)) return []
  return result.filter(row => row && typeof row === 'object'
    && typeof row.cover === 'string' && /^https?:\/\//i.test(row.cover))
    .map(row => ({
      ...(row.id !== undefined && row.id !== null ? { resource_id: String(row.id) } : {}),
      ...(typeof row.name === 'string' ? { name: row.name } : {}),
      url: row.cover,
      preview_url: previewUrl(row.cover),
    }))
}

module.exports = { previewUrl, avatarPreviews }

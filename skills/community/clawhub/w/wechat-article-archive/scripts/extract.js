const qs = require('qs');
const dayjs = require('dayjs');
const cheerio = require('cheerio');
const unescape = require('lodash.unescape');
const errors = require('./errors');

const defaultConfig = {
  shouldReturnRawMeta: false,
  shouldReturnContent: true,
  shouldFollowTransferLink: true,
  shouldExtractMpLinks: false,
  shouldExtractTags: false,
  shouldExtractRepostMeta: false
};

function getError(code) {
  return { done: false, code, msg: errors[code] };
}

function isValidDate(value) {
  return value instanceof Date && !Number.isNaN(value.getTime());
}

function normalizeUrl(url = '') {
  const parts = url.replace(/&amp;/g, '&').split('?');
  const querys = qs.stringify(qs.parse(parts[1]));
  return querys ? `${parts[0]}?${querys}` : parts[0];
}

function getSupportedHost(url = '') {
  try {
    const parsed = new URL(url);
    if (!['http:', 'https:'].includes(parsed.protocol)) return null;
    if (parsed.hostname === 'mp.weixin.qq.com' || parsed.hostname === 'weixin.sogou.com') {
      return parsed.hostname;
    }
  } catch (e) {}
  return null;
}

async function fetchWechatHtml(url, headers, maxRedirects = 5) {
  let current = url;
  for (let redirects = 0; redirects <= maxRedirects; redirects += 1) {
    const response = await fetch(current, { headers, redirect: 'manual' });
    if (response.status >= 300 && response.status < 400) {
      const location = response.headers.get('location');
      if (!location || redirects === maxRedirects) throw new Error('invalid redirect');
      const next = new URL(location, current).toString();
      if (!getSupportedHost(next)) throw new Error('unsupported redirect host');
      current = next;
      continue;
    }
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.text();
  }
  throw new Error('too many redirects');
}

function getParameterByName(name, url) {
  name = name.replace(/[\[\]]/g, '\\$&');
  const regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)');
  const results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return '';
  return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

function extractPicturePageInfoList(html = '') {
  const marker = /(?:window\.)?picture_page_info_list\s*[:=]\s*\[/g;
  let markerMatch;
  let best = [];

  while ((markerMatch = marker.exec(html))) {
    const start = html.indexOf('[', markerMatch.index);
    if (start < 0) continue;

    let depth = 0;
    let quote = null;
    let escaped = false;
    let end = -1;
    for (let i = start; i < html.length; i += 1) {
      const char = html[i];
      if (quote) {
        if (escaped) escaped = false;
        else if (char === '\\') escaped = true;
        else if (char === quote) quote = null;
        continue;
      }
      if (char === "'" || char === '"' || char === '`') {
        quote = char;
        continue;
      }
      if (char === '[') depth += 1;
      else if (char === ']') {
        depth -= 1;
        if (depth === 0) {
          end = i;
          break;
        }
      }
    }
    if (end < 0) continue;

    const arraySource = html.slice(start + 1, end);
    const objects = [];
    let objectStart = -1;
    let objectDepth = 0;
    let arrayDepth = 0;
    quote = null;
    escaped = false;
    for (let i = 0; i < arraySource.length; i += 1) {
      const char = arraySource[i];
      if (quote) {
        if (escaped) escaped = false;
        else if (char === '\\') escaped = true;
        else if (char === quote) quote = null;
        continue;
      }
      if (char === "'" || char === '"' || char === '`') {
        quote = char;
        continue;
      }
      if (char === '[') arrayDepth += 1;
      else if (char === ']') arrayDepth -= 1;
      else if (char === '{') {
        if (objectDepth === 0 && arrayDepth === 0) objectStart = i;
        objectDepth += 1;
      } else if (char === '}') {
        objectDepth -= 1;
        if (objectDepth === 0 && arrayDepth === 0 && objectStart >= 0) {
          objects.push(arraySource.slice(objectStart, i + 1));
          objectStart = -1;
        }
      }
    }

    const list = objects.map(source => {
      const urlMatch = source.match(/\bcdn_url\s*:\s*(['"])(https?:\\?\/\\?\/.*?)\1/);
      if (!urlMatch) return null;
      const widthMatch = source.match(/\bwidth\s*:\s*['"]?(\d+)/);
      const heightMatch = source.match(/\bheight\s*:\s*['"]?(\d+)/);
      return {
        cdn_url: urlMatch[2].replace(/\\\//g, '/').replace(/&amp;/g, '&'),
        width: widthMatch ? Number(widthMatch[1]) : null,
        height: heightMatch ? Number(heightMatch[1]) : null
      };
    }).filter(Boolean);

    if (list.length > best.length) best = list;
    marker.lastIndex = end + 1;
  }
  return best.length ? best : null;
}

function decodeJsString(value = '') {
  return value
    .replace(/\\x([0-9a-f]{2})/gi, (_, hex) => String.fromCharCode(parseInt(hex, 16)))
    .replace(/\\u([0-9a-f]{4})/gi, (_, hex) => String.fromCharCode(parseInt(hex, 16)))
    .replace(/\\\//g, '/')
    .replace(/\\(['"\\])/g, '$1');
}

function escapeHtmlText(value = '') {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function descriptionToHtml(description = '', title = '') {
  const decoded = decodeJsString(unescape(description))
    .replace(/\r\n?/g, '\n')
    .trim();
  if (!decoded || decoded === title) return '';
  return decoded
    .split(/\n{2,}/)
    .map(paragraph => paragraph.trim())
    .filter(Boolean)
    .map(paragraph => `<p>${escapeHtmlText(paragraph).replace(/\n/g, '<br>')}</p>`)
    .join('');
}

function extractQuotedPropertyValues(html = '', field = '') {
  const safeField = field.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const marker = new RegExp(`\\b${safeField}\\s*:\\s*(['"])`, 'g');
  const values = [];
  let match;

  while ((match = marker.exec(html))) {
    const quote = match[1];
    const start = marker.lastIndex;
    let escaped = false;
    for (let i = start; i < html.length; i += 1) {
      const char = html[i];
      if (escaped) {
        escaped = false;
        continue;
      }
      if (char === '\\') {
        escaped = true;
        continue;
      }
      if (char === quote) {
        values.push(decodeJsString(html.slice(start, i)));
        marker.lastIndex = i + 1;
        break;
      }
    }
  }
  return values;
}

function htmlTextLength(fragment = '') {
  if (!fragment) return 0;
  return cheerio.load(`<body>${fragment}</body>`, { decodeEntities: false })('body')
    .text()
    .replace(/\s+/g, '')
    .length;
}

function hasArticleMarkup(fragment = '') {
  return /<(?:p|h[1-6]|section|div|img|ul|ol|li|blockquote|table|pre)\b/i.test(fragment);
}

function extractEmbeddedArticleContent(html = '') {
  const candidates = extractQuotedPropertyValues(html, 'content_noencode');
  if (!candidates.length) return null;
  return candidates.sort((left, right) => htmlTextLength(right) - htmlTextLength(left))[0];
}

function extractExpressionValue(expression = '') {
  const values = [];
  const stringLiteral = /(['"])((?:\\.|(?!\1)[\s\S])*?)\1/g;
  let literal;
  while ((literal = stringLiteral.exec(expression))) values.push(decodeJsString(literal[2]));
  const nonEmpty = values.filter(value => value !== '');
  if (nonEmpty.length) {
    return expression.includes('?') && expression.includes(':')
      ? nonEmpty[nonEmpty.length - 1]
      : nonEmpty[0];
  }
  const number = expression.match(/(?:^|[?:|])\s*(\d{1,})\b/);
  return number ? number[1] : null;
}

function extractAssignedValue(html = '', field = '') {
  const safeField = field.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const assignment = new RegExp(`(?:\\bvar\\s+|window\\.)${safeField}\\s*=(?!=)([\\s\\S]*?);`, 'g');
  let match;
  while ((match = assignment.exec(html))) {
    const value = extractExpressionValue(match[1]);
    if (value !== null && value !== '') return value;
  }
  return null;
}

function extractDValue(html = '', field = '') {
  const assignment = new RegExp(`d\\.${field}\\s*=([\\s\\S]*?);`, 'g');
  let match;
  while ((match = assignment.exec(html))) {
    const value = extractExpressionValue(match[1]);
    if (value !== null && value !== '') return value;
  }
  return null;
}

async function extract(input, options = {}) {
  const config = Object.assign({}, defaultConfig, options);
  const {
    shouldReturnRawMeta,
    shouldReturnContent,
    shouldFollowTransferLink,
    shouldExtractMpLinks,
    shouldExtractTags,
    shouldExtractRepostMeta
  } = config;

  if (!input) return getError(2001);

  let paramType = 'HTML';
  let url = options.url ? normalizeUrl(options.url) : null;
  let rawUrl = null;
  let html = input;
  let type = 'post';
  let hasCopyright = false;

  if (/^http/.test(input)) {
    const normalized = normalizeUrl(input);
    const host = getSupportedHost(normalized);
    if (!host) return getError(2009);
    paramType = 'URL';
    rawUrl = normalized;
    if (!url) url = normalized;

    try {
      html = await fetchWechatHtml(normalized, {
          'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
      });
    } catch (e) {
      return getError(1002);
    }
  } else {
    html = input.replace(/\\n/g, '');
  }

  if (!html) return getError(1003);
  if (html.includes('访问过于频繁') && !html.includes('js_content')) return paramType === 'URL' ? getError(1004) : getError(2010);
  if (html.includes('链接已过期') && !html.includes('js_content')) return getError(2002);
  if (html.includes('被投诉且经审核涉嫌侵权，无法查看')) return getError(2003);
  if (html.includes('该公众号已迁移')) {
    const match = html.match(/var\stransferTargetLink\s=\s'(.*?)';/);
    if (match && match[1]) {
      if (shouldFollowTransferLink) return await extract(match[1]);
      return { ...getError(1006), url: match[1] };
    }
    return getError(2004);
  }
  if (html.includes('该内容已被发布者删除')) return getError(2005);
  if (html.includes('此内容因违规无法查看')) return getError(2006);
  if (html.includes('此内容发送失败无法查看')) return getError(2007);
  if (html.includes('由用户投诉并经平台审核，涉嫌过度营销')) return getError(2011);
  if (html.includes('此帐号已被屏蔽') && !html.includes('id="js_content"')) return getError(2012);
  if (html.includes('此帐号已自主注销') && !html.includes('id="js_content"')) return getError(2013);
  if (!html.includes('id="js_content"') && html.includes('此帐号处于帐号迁移流程中')) return getError(2015);
  if (html.includes('page_rumor') && !html.includes('id="js_content"')) return getError(2014);
  if (html.includes('投诉类型') && html.includes('冒名侵权')) return getError(2016);
  if (!html.includes('id="js_content"') && !html.includes('id=\\"js_content\\"')) {
    if (html.includes('cover_url')) type = 'image';
    else return getError(1000);
  }

  html = html.replace('>微信号', ' id="append-account-alias">微信号')
    .replace('>功能介绍', ' id="append-account-desc">功能介绍')
    .replace(/\n\s+<script/g, '\n\n<script');

  const $ = cheerio.load(html, { decodeEntities: false });
  if ($('#copyright_logo')?.text().includes('原创')) hasCopyright = true;
  if (/video/.test($('body').attr('class'))) type = 'video';
  if ($('#js_content > #img_list').length) type = 'image';
  if ($('#js_share_content').length) type = 'repost';
  if ($('.page_share_audio').length || $('#voice_parent').length) type = 'voice';
  if (/share_media_text/.test(html)) type = 'text';
  if ($('.weui-msg .weui-msg__title').text().trim() === '链接已过期') return getError(2002);
  if ($('.global_error_msg.warn').text().trim().includes('系统出错')) return getError(2008);

  const basic = {
    accountName: $('.profile_nickname').text() || null,
    accountBiz: null,
    accountBizNumber: null,
    accountId: null,
    accountAvatar: null
  };

  const accountAliasPrev = $('#append-account-alias');
  let accountAlias = accountAliasPrev.siblings('span').text() || null;
  const accountDescPrev = $('#append-account-desc');
  let accountDesc = accountDescPrev.siblings('span').text() || null;
  if (!accountDesc) {
    const $accountDesc = $('.profile_meta_value');
    if ($accountDesc[1]) {
      try {
        const text = $accountDesc[1].children[0].data;
        if (text?.length > 10) accountDesc = text;
      } catch (e) {}
    }
  }

  const domContent = shouldReturnContent ? $('#js_content').html() : null;
  const embeddedContent = shouldReturnContent ? extractEmbeddedArticleContent(html) : null;
  const domContentTextLength = htmlTextLength(domContent);
  const embeddedContentTextLength = htmlTextLength(embeddedContent);
  const preferEmbeddedContent = embeddedContentTextLength > domContentTextLength + 50;
  const primaryContent = preferEmbeddedContent ? embeddedContent : domContent;
  const hasSubstantiveArticleContent = (
    domContentTextLength >= 100 && hasArticleMarkup(domContent)
  ) || (
    embeddedContentTextLength >= 100 && hasArticleMarkup(embeddedContent)
  );

  const post = {
    msg_has_copyright: hasCopyright,
    msg_content: primaryContent
  };

  try {
    const author = $("meta[name='author']").attr('content');
    if (author) post.msg_author = author;
  } catch (e) {
    const $author = $('#js_author_name');
    if ($author.length) {
      const info = $author.text().trim();
      if (info) post.msg_author = info;
    }
  }

  const extra = { biz: null, sn: null, mid: null, idx: null, msg_title: null, user_name: null, nick_name: null, hd_head_img: null };
  let picturePageInfoList = extractPicturePageInfoList(html);
  const usePicturePageFallback = Boolean(picturePageInfoList) && !hasSubstantiveArticleContent;
  if (usePicturePageFallback) type = 'image';

  for (const field of Object.keys(extra)) extra[field] = extractAssignedValue(html, field);

  const staticData = {};
  for (const field of [
    'msg_title', 'msg_desc', 'msg_link', 'msg_source_url', 'msg_cdn_url',
    '_ori_article_type', 'create_time', 'ct', 'user_name', 'ori_head_img_url', 'nickname', 'biz'
  ]) staticData[field] = extractAssignedValue(html, field);

  for (const field of ['msg_title', 'msg_desc', 'msg_link', 'msg_source_url']) {
    if (!post[field] && staticData[field]) post[field] = staticData[field];
  }
  if (!post.msg_cover && staticData.msg_cdn_url) post.msg_cover = staticData.msg_cdn_url;
  if (!post.msg_article_type && staticData._ori_article_type) post.msg_article_type = staticData._ori_article_type;
  if (!basic.accountId && staticData.user_name) basic.accountId = staticData.user_name;
  if (!basic.accountAvatar && staticData.ori_head_img_url) basic.accountAvatar = staticData.ori_head_img_url;
  if (!basic.accountName && staticData.nickname) basic.accountName = staticData.nickname;
  if (!basic.accountBiz && staticData.biz) basic.accountBiz = staticData.biz;

  if (type === 'voice' && !post.msg_source_url) {
    const voiceId = html.match(/\bvoiceid\s*[:=]\s*['"]([^'"]+)['"]/);
    if (voiceId) post.msg_source_url = `https://res.wx.qq.com/voice/getvoice?mediaid=${voiceId[1]}`;
  }
  if ((type === 'video' || type === 'voice') && shouldReturnContent) {
    post.msg_content = $("meta[name='description']").attr('content') || post.msg_content;
  }
  if (type === 'video' && !post.msg_cover) post.msg_cover = $("meta[property='og:image']").attr('content');
  const staticTimestamp = /^\d{10}$/.test(staticData.create_time || '')
    ? staticData.create_time
    : staticData.ct;
  if (/^\d{10}$/.test(staticTimestamp || '')) {
    post.msg_publish_time = new Date(Number(staticTimestamp) * 1000);
    post.msg_publish_time_str = dayjs(post.msg_publish_time).format('YYYY/MM/DD HH:mm:ss');
  }
  if (shouldReturnRawMeta) post.raw_data = staticData;

  if (extra.biz) {
    basic.accountBiz = extra.biz;
    basic.accountBizNumber = Buffer.from(extra.biz, 'base64').toString() * 1;
  }
  post.msg_sn = extra.sn || post.msg_sn || null;
  post.msg_idx = extra.idx ? extra.idx * 1 : post.msg_idx || null;
  post.msg_mid = extra.mid ? extra.mid * 1 : post.msg_mid || null;

  if (post.msg_publish_time && !isValidDate(post.msg_publish_time)) {
    delete post.msg_publish_time;
    delete post.msg_publish_time_str;
  }
  if (!post.msg_publish_time) {
    const date = $('#post-date').text() || $('#publish_time').text();
    if (date) {
      const parsed = new Date(date);
      if (isValidDate(parsed)) post.msg_publish_time = parsed;
    }
  }
  if (!post.msg_publish_time && html.includes('.ct')) {
    const line = html.split('\n').find(one => one.includes('.ct'));
    const matched = /(\d+)/g.exec(line || '');
    if (matched && matched[1]?.length >= 10) post.msg_publish_time = new Date(matched[1] * 1000);
  }
  if (isValidDate(post.msg_publish_time) && !post.msg_publish_time_str) {
    post.msg_publish_time_str = dayjs(post.msg_publish_time).format('YYYY/MM/DD HH:mm:ss');
  }
  const dValues = {};
  for (const field of [
    'title', 'msg_link', 'cover', 'author', 'sn', 'mid', 'idx',
    'nick_name', 'user_name', 'hd_head_img', 'biz', 'create_time', 'ct'
  ]) dValues[field] = extractDValue(html, field);
  const preferDValues = type === 'image' || type === 'voice';
  if (dValues.title && (preferDValues || !post.msg_title)) post.msg_title = dValues.title;
  if (dValues.msg_link && (preferDValues || !post.msg_link)) post.msg_link = dValues.msg_link;
  if (dValues.cover && (preferDValues || !post.msg_cover)) post.msg_cover = dValues.cover;
  if (dValues.author && (preferDValues || !post.msg_author)) post.msg_author = dValues.author;
  if (dValues.sn && (preferDValues || !post.msg_sn)) post.msg_sn = dValues.sn;
  if (dValues.mid && (preferDValues || !post.msg_mid)) post.msg_mid = dValues.mid;
  if (dValues.idx && (preferDValues || !post.msg_idx)) post.msg_idx = dValues.idx;
  if (dValues.nick_name && (preferDValues || !basic.accountName)) basic.accountName = dValues.nick_name;
  if (dValues.user_name && (preferDValues || !basic.accountId)) basic.accountId = dValues.user_name;
  if (dValues.hd_head_img && (preferDValues || !basic.accountAvatar)) basic.accountAvatar = dValues.hd_head_img;
  if (dValues.biz && (preferDValues || !basic.accountBiz)) basic.accountBiz = dValues.biz;
  if (!post.msg_publish_time) {
    const timestamp = dValues.create_time || dValues.ct;
    if (/^\d{10}$/.test(timestamp || '')) {
      post.msg_publish_time = new Date(Number(timestamp) * 1000);
      post.msg_publish_time_str = dayjs(post.msg_publish_time).format('YYYY/MM/DD HH:mm:ss');
    }
  }
  if (!post.msg_title) {
    const title = $('.rich_media_title').text();
    if (title) post.msg_title = title.trim();
  }
  if (!basic.accountId && extra.user_name) basic.accountId = extra.user_name;
  if (!basic.accountName && extra.nick_name) basic.accountName = extra.nick_name;
  if (!basic.accountAvatar && extra.hd_head_img) basic.accountAvatar = extra.hd_head_img;
  if (!basic.accountName && $('.wx_follow_nickname')) {
    const name = $('.wx_follow_nickname').text();
    if (name) basic.accountName = name.trim();
  }

  const data = {
    account_name: basic.accountName,
    account_alias: accountAlias,
    account_avatar: basic.accountAvatar?.length > 10 ? basic.accountAvatar : null,
    account_description: accountDesc,
    account_id: basic.accountId,
    account_biz: basic.accountBiz,
    account_biz_number: basic.accountBizNumber,
    account_qr_code: `https://open.weixin.qq.com/qr/code?username=${basic.accountId || accountAlias}`,
    ...post,
    msg_type: type
  };

  for (const key in data) if (data[key] === '') data[key] = null;
  if (!data.msg_title && type === 'post') {
    data.msg_type = 'text';
    const title = $("meta[property='og:title']").attr('content');
    const desc = $("meta[property='og:description']").attr('content');
    if (title) {
      data.msg_title = title;
      const rawContent = $('#js_panel_like_title').html();
      data.msg_content = rawContent ? rawContent.trim().replace(/\n/g, '<br/>') : title;
    }
    if (!title && desc) data.msg_title = desc;
  }
  if (!data.msg_publish_time) {
    const matched = html.match(/d\.(?:create_time|ct)\s*=\s*(?:['"](\d{10})['"]|[^;]*?\:\s*['"](\d{10})['"])/);
    const timestamp = matched && (matched[1] || matched[2]);
    if (timestamp) {
      data.msg_publish_time = new Date(timestamp * 1000);
      data.msg_publish_time_str = dayjs(data.msg_publish_time).format('YYYY/MM/DD HH:mm:ss');
    }
  }
  if (!data.msg_mid || !data.msg_link) {
    let linkUrl = options?.url || rawUrl || $("meta[property='og:url']").attr('content');
    if (linkUrl && /^http/.test(linkUrl)) {
      linkUrl = linkUrl.replace(/&amp;/g, '&');
      if (!data.msg_link) data.msg_link = linkUrl;
      if (/mid/.test(linkUrl) && /__biz/.test(linkUrl)) {
        if (!data.msg_mid) data.msg_mid = getParameterByName('mid', linkUrl);
        if (!data.msg_idx) data.msg_idx = getParameterByName('idx', linkUrl);
        if (!data.msg_sn) data.msg_sn = getParameterByName('sn', linkUrl);
      }
    }
  }
  if (data.msg_title) data.msg_title = unescape(data.msg_title);
  if (data.msg_type === 'video') {
    if (!data.msg_content) data.msg_content = data.msg_title;
    else data.msg_content = data.msg_content.replace(/\\x26/g, '&').replace(/\\x0a/g, '<br/>');
  }
  if (!data.msg_title) {
    const title = $("meta[property='og:title']").attr('content');
    if (title) data.msg_title = title;
  }
  if (!data.msg_desc) data.msg_desc = $("meta[property='og:description']").attr('content') || $("meta[name='description']").attr('content');
  if (!data.msg_desc && data.msg_content) {
    const text = data.msg_content.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
    if (text.length > 0) data.msg_desc = text.substring(0, 140) + (text.length > 140 ? '...' : '');
  }
  if (data.msg_content?.includes('<script') && data.msg_content.includes('script>') && data.msg_content.includes('nonce=')) {
    const desc = $("meta[property='og:description']").attr('content');
    if (desc) data.msg_content = desc;
  }
  if (!data.msg_title || !isValidDate(data.msg_publish_time)) return getError(1001);
  if (type === 'text' && !data.msg_content && data.msg_title) data.msg_content = data.msg_title;
  if (usePicturePageFallback) {
    data.msg_type = 'image';
    if (shouldReturnContent) {
      data.msg_content = descriptionToHtml(data.msg_desc, data.msg_title);
      for (const one of picturePageInfoList) data.msg_content += `<img src="${one.cdn_url}" style="max-width:100%"/><br><br>`;
    } else {
      data.msg_content = null;
    }
  }
  if (shouldExtractMpLinks) {
    const mpLinks = [];
    $('a').each((i, ele) => {
      const href = $(ele).attr('href');
      if (href?.includes('mp.weixin.qq.com')) mpLinks.push({ title: $(ele).text(), href });
    });
    data.mp_links_count = mpLinks.length;
    data.mp_links = mpLinks;
  }
  if (shouldExtractTags) {
    const tags = [];
    $('.article-tag__item-wrp').each((i, ele) => {
      const $this = $(ele);
      try {
        const tagUrl = $this.attr('data-url');
        const name = $this.find('.article-tag__item').text();
        let count = $this.find('.article-tag__item-num').text();
        if (name) {
          if (!count && tags.length === 0) {
            const $count = $('.article-tag-card__right');
            if ($count.length) count = $count.text().replace('个', '');
          }
          tags.push({
            id: getParameterByName('album_id', tagUrl) || getParameterByName('tag_id', tagUrl) || null,
            url: tagUrl,
            name: name.replace(/^#/, ''),
            count: count?.replace(/\D/g, '') * 1 || 0
          });
        }
      } catch (e) {}
    });
    data.tags = tags;
  }
  if (shouldExtractRepostMeta && html.includes('copyright_info') && html.includes('original_primary_nickname')) {
    const name = $('.original_primary_nickname').text();
    if (name) data.repost_meta = { account_name: name };
  }
  if (data.msg_link?.includes('&amp;')) data.msg_link = data.msg_link.replace(/&amp;/g, '&');
  return { code: 0, done: true, data };
}

module.exports = { extract };

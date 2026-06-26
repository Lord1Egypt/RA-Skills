/**
 * XHS Tools Module - 优化版
 * 参考 https://github.com/xpzouying/xiaohongshu-mcp 最佳实践
 * 
 * 核心优化:
 * 1. 使用 __INITIAL_STATE__ 获取完整数据（包含 xsecToken）
 * 2. 统一错误处理和日志
 * 3. DOM 解析作为降级方案
 */

import { getBrowser } from './browser.js';
import QRCode from 'qrcode';

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

// ========== 工具函数 ==========

/**
 * 从页面提取 __INITIAL_STATE__ 数据
 */
async function extractInitialState(page) {
  return await page.evaluate(() => {
    if (!window.__INITIAL_STATE__) return null;
    
    const state = window.__INITIAL_STATE__;
    
    // 提取 Feed 数据的通用函数
    const extractFeeds = (feedsData) => {
      if (!feedsData || !Array.isArray(feedsData)) return [];
      
      return feedsData
        .filter(feed => feed && feed.id)
        .map(feed => ({
          id: feed.id,
          xsec_token: feed.xsecToken || '',
          title: feed.noteCard?.displayTitle || '',
          cover: feed.noteCard?.cover?.urlDefault || feed.noteCard?.cover?.url || '',
          author: feed.noteCard?.user?.nickname || feed.noteCard?.user?.nickName || '',
          author_id: feed.noteCard?.user?.userId || '',
          like_count: feed.noteCard?.interactInfo?.likedCount || '0',
          collect_count: feed.noteCard?.interactInfo?.collectedCount || '0',
          comment_count: feed.noteCard?.interactInfo?.commentCount || '0',
          is_video: !!feed.noteCard?.video,
          url: `https://www.xiaohongshu.com/explore/${feed.id}`,
        }));
    };
    
    return {
      // 首页推荐
      homeFeeds: extractFeeds(state?.feed?.feeds?._value || state?.homeFeed?.feeds?._value || []),
      // 搜索结果
      searchFeeds: extractFeeds(state?.search?.feeds?._value || state?.searchResult?.feeds?._value || []),
      // 笔记详情
      noteDetail: state?.note?.noteDetail || null,
    };
  });
}

/**
 * DOM 解析降级方案
 */
async function parseFeedsFromDOM(page) {
  return await page.evaluate(() => {
    const items = [];
    const noteElements = document.querySelectorAll('section.note-item');

    noteElements.forEach((element) => {
      try {
        const linkEl = element.querySelector('a[href*="/explore/"]');
        if (!linkEl) return;
        
        const href = linkEl.getAttribute('href') || '';
        const noteId = href.match(/\/explore\/([a-zA-Z0-9]+)/)?.[1] || '';
        const xsecToken = href.match(/xsec_token=([^&]+)/)?.[1] || '';
        const title = element.querySelector('[class*="title"]')?.textContent?.trim() || 
                     element.querySelector('span')?.textContent?.trim() || '';
        const cover = element.querySelector('img')?.src || '';
        const author = element.querySelector('[class*="author"], [class*="name"], .nickname')?.textContent?.trim() || '';

        if (noteId) {
          items.push({
            id: noteId,
            xsec_token: xsecToken,
            title,
            cover,
            author,
            url: `https://www.xiaohongshu.com${href}`,
          });
        }
      } catch (error) {
        // skip
      }
    });

    return items;
  });
}

// ========== 登录相关 ==========

/**
 * 检查登录状态
 */
export async function checkLoginStatus() {
  const browser = await getBrowser();
  const page = await browser.getPage();

  try {
    await page.goto('https://www.xiaohongshu.com', {
      waitUntil: 'networkidle2',
      timeout: 30000,
    });
    await sleep(2000);

    // 检查是否有登录按钮
    const loginButton = await page.$('.login-btn');
    const userAvatar = await page.$('.user-info');

    if (loginButton && !userAvatar) {
      return { success: false, logged_in: false, message: '未登录' };
    }

    // 验证创作者中心访问权限
    try {
      await page.goto('https://creator.xiaohongshu.com/publish/publish', {
        waitUntil: 'networkidle2',
        timeout: 30000,
      });
      await sleep(2000);

      if (page.url().includes('login')) {
        return { success: false, logged_in: false, message: '未登录（被重定向）' };
      }

      return { success: true, logged_in: true, message: '已登录' };
    } catch {
      return { success: true, logged_in: true, message: '已登录' };
    }
  } catch (error) {
    return { success: false, logged_in: false, message: `检查失败: ${error.message}` };
  }
}

/**
 * 获取登录二维码
 */
export async function getLoginQRCode() {
  const browser = await getBrowser({ headless: false });
  const page = await browser.getPage();

  try {
    await page.goto('https://www.xiaohongshu.com', {
      waitUntil: 'networkidle2',
      timeout: 30000,
    });
    await sleep(1000);

    const loginBtn = await page.$('.login-btn');
    if (loginBtn) {
      await loginBtn.click();
      await sleep(2000);
    }

    await page.waitForSelector('.qrcode-img, .login-qrcode', { timeout: 10000 });

    // 尝试获取二维码图片
    const qrElement = await page.$('.qrcode-img, .login-qrcode');
    if (qrElement) {
      const screenshot = await qrElement.screenshot({ encoding: 'base64' });
      return {
        success: true,
        qr_code: `data:image/png;base64,${screenshot}`,
        message: '请扫描二维码登录',
        timeout: 120,
      };
    }

    return { success: false, message: '未找到二维码' };
  } catch (error) {
    return { success: false, message: `获取二维码失败: ${error.message}` };
  }
}

/**
 * 删除 cookies
 */
export async function deleteCookies() {
  const browser = await getBrowser();
  const deleted = await browser.deleteCookies();
  return {
    success: deleted,
    message: deleted ? 'Cookies 已删除' : '删除失败',
  };
}

// ========== 内容获取 ==========

/**
 * 获取首页推荐
 */
export async function listFeeds() {
  const browser = await getBrowser();
  const page = await browser.getPage();

  try {
    await page.goto('https://www.xiaohongshu.com/explore', {
      waitUntil: 'networkidle2',
      timeout: 30000,
    });

    // 等待 __INITIAL_STATE__ 加载
    await page.waitForFunction(() => window.__INITIAL_STATE__ !== undefined, { timeout: 10000 }).catch(() => {});
    await sleep(2000);

    // 滚动加载更多
    for (let i = 0; i < 3; i++) {
      await page.evaluate(() => window.scrollBy(0, 1000));
      await sleep(1000);
    }

    // 优先使用 __INITIAL_STATE__
    const state = await extractInitialState(page);
    let feeds = state?.homeFeeds || [];

    // 降级到 DOM 解析
    if (feeds.length === 0) {
      feeds = await parseFeedsFromDOM(page);
    }

    return { success: true, feeds, count: feeds.length };
  } catch (error) {
    return { success: false, feeds: [], message: `获取失败: ${error.message}` };
  }
}

/**
 * 搜索笔记
 */
export async function searchFeeds(keyword, filters = {}) {
  const browser = await getBrowser();
  const page = await browser.getPage();

  try {
    const searchUrl = `https://www.xiaohongshu.com/search_result?keyword=${encodeURIComponent(keyword)}`;
    await page.goto(searchUrl, {
      waitUntil: 'networkidle2',
      timeout: 30000,
    });

    // 等待 __INITIAL_STATE__ 加载
    await page.waitForFunction(() => window.__INITIAL_STATE__ !== undefined, { timeout: 10000 }).catch(() => {});
    await sleep(2000);

    // 优先使用 __INITIAL_STATE__
    const state = await extractInitialState(page);
    let feeds = state?.searchFeeds || [];

    // 降级到 DOM 解析
    if (feeds.length === 0) {
      feeds = await parseFeedsFromDOM(page);
    }

    return { success: true, keyword, feeds, count: feeds.length };
  } catch (error) {
    return { success: false, keyword, feeds: [], message: `搜索失败: ${error.message}` };
  }
}

/**
 * 获取笔记详情
 */
export async function getFeedDetail(feedId, xsecToken, options = {}) {
  const browser = await getBrowser();
  const page = await browser.getPage();

  try {
    let url = `https://www.xiaohongshu.com/explore/${feedId}`;
    if (xsecToken) {
      url += `?xsec_token=${xsecToken}&xsec_type=pc_search`;
    }
    
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
    await sleep(2000);

    // 检查是否被重定向
    if (page.url().includes('/404') || page.url().includes('error')) {
      return {
        success: false,
        feed_id: feedId,
        message: '笔记无法访问（需要有效的 xsec_token）',
      };
    }

    // 尝试从 __INITIAL_STATE__ 获取详情
    const detail = await page.evaluate(() => {
      const state = window.__INITIAL_STATE__;
      const note = state?.note?.noteDetail?.note;
      
      if (note) {
        return {
          title: note.title || '',
          content: note.desc || '',
          author: note.user?.nickname || note.user?.nickName || '',
          author_id: note.user?.userId || '',
          avatar: note.user?.avatar || '',
          images: (note.imageList || []).map(img => img.urlDefault || img.urlPre || ''),
          stats: {
            likes: note.interactInfo?.likedCount || '0',
            collects: note.interactInfo?.collectedCount || '0',
            comments: note.interactInfo?.commentCount || '0',
          },
        };
      }

      // 降级到 DOM 解析
      return {
        title: document.querySelector('.note-content .title, [class*="title"]')?.textContent?.trim() || '',
        content: document.querySelector('.note-content .desc, [class*="desc"]')?.textContent?.trim() || '',
        author: document.querySelector('.author-wrapper .username, [class*="author"] [class*="name"]')?.textContent?.trim() || '',
        avatar: document.querySelector('.author-wrapper .avatar img')?.src || '',
        images: Array.from(document.querySelectorAll('.swiper-slide img, .note-image img')).map(img => img.src).filter(Boolean),
        stats: {
          likes: document.querySelector('.like-wrapper .count')?.textContent?.trim() || '0',
          collects: document.querySelector('.collect-wrapper .count')?.textContent?.trim() || '0',
          comments: document.querySelector('.chat-btn .count')?.textContent?.trim() || '0',
        },
      };
    });

    return { success: true, feed_id: feedId, ...detail };
  } catch (error) {
    return { success: false, feed_id: feedId, message: `获取详情失败: ${error.message}` };
  }
}

// ========== 互动操作 ==========

/**
 * 点赞/取消点赞
 */
export async function likeFeed(feedId, xsecToken, unlike = false) {
  const browser = await getBrowser();
  const page = await browser.getPage();

  try {
    const url = `https://www.xiaohongshu.com/explore/${feedId}?xsec_token=${xsecToken}`;
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
    await sleep(2000);

    const likeBtn = await page.$('.like-wrapper, .like-btn');
    if (!likeBtn) {
      return { success: false, message: '未找到点赞按钮' };
    }

    const isLiked = await likeBtn.evaluate(el => el.classList.contains('liked') || el.classList.contains('active'));

    if ((unlike && isLiked) || (!unlike && !isLiked)) {
      await likeBtn.click();
      await browser.saveCookies();
      return { success: true, action: unlike ? 'unliked' : 'liked', message: unlike ? '已取消点赞' : '已点赞' };
    }

    return { success: true, action: 'skipped', message: unlike ? '已取消点赞' : '已点赞' };
  } catch (error) {
    return { success: false, message: `操作失败: ${error.message}` };
  }
}

/**
 * 收藏/取消收藏
 */
export async function favoriteFeed(feedId, xsecToken, unfavorite = false) {
  const browser = await getBrowser();
  const page = await browser.getPage();

  try {
    const url = `https://www.xiaohongshu.com/explore/${feedId}?xsec_token=${xsecToken}`;
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
    await sleep(2000);

    const collectBtn = await page.$('.collect-wrapper, .collect-btn');
    if (!collectBtn) {
      return { success: false, message: '未找到收藏按钮' };
    }

    const isCollected = await collectBtn.evaluate(el => el.classList.contains('collected') || el.classList.contains('active'));

    if ((unfavorite && isCollected) || (!unfavorite && !isCollected)) {
      await collectBtn.click();
      await browser.saveCookies();
      return { success: true, action: unfavorite ? 'unfavorited' : 'favorited', message: unfavorite ? '已取消收藏' : '已收藏' };
    }

    return { success: true, action: 'skipped', message: unfavorite ? '已取消收藏' : '已收藏' };
  } catch (error) {
    return { success: false, message: `操作失败: ${error.message}` };
  }
}

/**
 * 发表评论
 */
export async function postComment(feedId, xsecToken, content) {
  const browser = await getBrowser();
  const page = await browser.getPage();

  try {
    const url = `https://www.xiaohongshu.com/explore/${feedId}?xsec_token=${xsecToken}`;
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
    await sleep(2000);

    const commentInput = await page.$('.comment-input-wrapper input, .comment-input textarea');
    if (!commentInput) {
      return { success: false, message: '未找到评论输入框' };
    }

    await commentInput.click();
    await sleep(300);
    await commentInput.type(content, { delay: 50 });
    await sleep(500);

    const sendBtn = await page.$('.send-btn, .submit-comment');
    if (sendBtn) {
      await sendBtn.click();
      await browser.saveCookies();
      return { success: true, message: '评论成功', content };
    }

    return { success: false, message: '未找到发送按钮' };
  } catch (error) {
    return { success: false, message: `评论失败: ${error.message}` };
  }
}

/**
 * 回复评论
 */
export async function replyComment(feedId, xsecToken, content, commentId = null, userId = null) {
  const browser = await getBrowser();
  const page = await browser.getPage();

  try {
    const url = `https://www.xiaohongshu.com/explore/${feedId}?xsec_token=${xsecToken}`;
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
    await sleep(2000);

    let replyBtn = null;
    if (commentId) {
      replyBtn = await page.$(`[data-id="${commentId}"] .reply-btn`);
    }

    if (!replyBtn) {
      return { success: false, message: '未找到目标评论' };
    }

    await replyBtn.click();
    await sleep(1000);

    const replyInput = await page.$('.reply-input input, .reply-input textarea');
    if (!replyInput) {
      return { success: false, message: '未找到回复输入框' };
    }

    await replyInput.type(content, { delay: 50 });
    await sleep(500);

    const sendBtn = await page.$('.reply-send-btn, .submit-reply');
    if (sendBtn) {
      await sendBtn.click();
      await browser.saveCookies();
      return { success: true, message: '回复成功', content };
    }

    return { success: false, message: '未找到发送按钮' };
  } catch (error) {
    return { success: false, message: `回复失败: ${error.message}` };
  }
}

// ========== 用户相关 ==========

/**
 * 获取用户主页
 */
export async function userProfile(userId, xsecToken) {
  const browser = await getBrowser();
  const page = await browser.getPage();

  try {
    const url = `https://www.xiaohongshu.com/user/profile/${userId}?xsec_token=${xsecToken}`;
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
    await sleep(2000);

    const profile = await page.evaluate(() => {
      const state = window.__INITIAL_STATE__;
      const user = state?.user?.userPage || state?.userProfile;
      
      if (user) {
        return {
          nickname: user.basicInfo?.nickname || '',
          avatar: user.basicInfo?.avatar || '',
          description: user.basicInfo?.desc || '',
          stats: {
            follows: user.interactions?.followCount || '0',
            fans: user.interactions?.fansCount || '0',
            liked: user.interactions?.likedCount || '0',
          },
        };
      }

      // 降级 DOM
      return {
        nickname: document.querySelector('.user-name, .nickname')?.textContent?.trim() || '',
        avatar: document.querySelector('.user-avatar img, .avatar img')?.src || '',
        description: document.querySelector('.user-desc, .bio')?.textContent?.trim() || '',
        stats: {
          follows: document.querySelector('.follow-count')?.textContent?.trim() || '0',
          fans: document.querySelector('.fans-count')?.textContent?.trim() || '0',
          liked: document.querySelector('.liked-count')?.textContent?.trim() || '0',
        },
      };
    });

    return { success: true, user_id: userId, ...profile };
  } catch (error) {
    return { success: false, user_id: userId, message: `获取用户主页失败: ${error.message}` };
  }
}

// ========== 发布相关 ==========

/**
 * 发布图文
 */
export async function publishContent({ title, content, images, tags = [], isOriginal = false, visibility = '公开可见', scheduleAt = null }) {
  const browser = await getBrowser({ headless: false });
  const page = await browser.getPage();

  try {
    await page.goto('https://creator.xiaohongshu.com/publish/publish', {
      waitUntil: 'networkidle2',
      timeout: 30000,
    });
    await sleep(2000);

    if (page.url().includes('login')) {
      return { success: false, message: '未登录' };
    }

    // 上传图片
    for (const imagePath of images) {
      const uploadInput = await page.$('input[type="file"]');
      if (uploadInput) {
        await uploadInput.uploadFile(imagePath);
        await sleep(2000);
      }
    }

    await sleep(3000);

    // 填写标题
    const titleInput = await page.$('.title-input, input[placeholder*="标题"]');
    if (titleInput) {
      await titleInput.click();
      await titleInput.type(title.substring(0, 20), { delay: 50 });
    }

    // 填写正文
    const contentInput = await page.$('.content-input, textarea[placeholder*="正文"]');
    if (contentInput) {
      await contentInput.click();
      await contentInput.type(content.substring(0, 1000), { delay: 30 });
    }

    // 添加标签
    for (const tag of tags.slice(0, 5)) {
      const tagInput = await page.$('.tag-input, input[placeholder*="标签"]');
      if (tagInput) {
        await tagInput.type(`#${tag}`, { delay: 50 });
        await sleep(500);
        await page.keyboard.press('Enter');
      }
    }

    await sleep(2000);

    // 发布
    const publishBtn = await page.$('.publish-btn, button.publish');
    if (publishBtn) {
      await publishBtn.click();
      await sleep(3000);
      await browser.saveCookies();

      return {
        success: true,
        message: '发布成功',
        title,
        images_count: images.length,
      };
    }

    return { success: false, message: '未找到发布按钮' };
  } catch (error) {
    return { success: false, message: `发布失败: ${error.message}` };
  }
}

/**
 * 发布视频
 */
export async function publishWithVideo({ title, content, video, tags = [], visibility = '公开可见', scheduleAt = null }) {
  const browser = await getBrowser({ headless: false });
  const page = await browser.getPage();

  try {
    await page.goto('https://creator.xiaohongshu.com/publish/publish', {
      waitUntil: 'networkidle2',
      timeout: 30000,
    });
    await sleep(2000);

    if (page.url().includes('login')) {
      return { success: false, message: '未登录' };
    }

    // 切换到视频 tab
    const videoTab = await page.$('.video-tab, [data-type="video"]');
    if (videoTab) {
      await videoTab.click();
      await sleep(1000);
    }

    // 上传视频
    const uploadInput = await page.$('input[type="file"]');
    if (uploadInput) {
      await uploadInput.uploadFile(video);
      await sleep(10000); // 视频上传需要更长时间
    }

    // 填写标题和正文
    const titleInput = await page.$('.title-input, input[placeholder*="标题"]');
    if (titleInput) {
      await titleInput.type(title.substring(0, 20), { delay: 50 });
    }

    const contentInput = await page.$('.content-input, textarea[placeholder*="正文"]');
    if (contentInput) {
      await contentInput.type(content.substring(0, 1000), { delay: 30 });
    }

    // 添加标签
    for (const tag of tags.slice(0, 5)) {
      const tagInput = await page.$('.tag-input, input[placeholder*="标签"]');
      if (tagInput) {
        await tagInput.type(`#${tag}`, { delay: 50 });
        await sleep(500);
        await page.keyboard.press('Enter');
      }
    }

    await sleep(2000);

    // 发布
    const publishBtn = await page.$('.publish-btn, button.publish');
    if (publishBtn) {
      await publishBtn.click();
      await sleep(3000);
      await browser.saveCookies();

      return { success: true, message: '视频发布成功', title, video };
    }

    return { success: false, message: '未找到发布按钮' };
  } catch (error) {
    return { success: false, message: `发布失败: ${error.message}` };
  }
}

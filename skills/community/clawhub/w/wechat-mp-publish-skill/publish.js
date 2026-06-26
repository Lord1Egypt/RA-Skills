#!/usr/bin/env node

/**
 * 微信公众号文章发布脚本 v2
 * 使用 OpenClaw browser 工具自动化发布流程
 * 
 * 功能：
 * - 发布新文章
 * - 编辑草稿箱文章
 * - 自动匹配素材库图片
 * - 会话过期检测与重试
 * 
 * 用法：
 *   node publish.js "标题" "内容" [--cover <url>] [--preview]
 *   node publish.js --draft <文章标题>  # 编辑草稿
 *   node publish.js --organize          # 整理草稿箱，匹配图片
 */

const MP_HOME = 'https://mp.weixin.qq.com';
const MP_DRAFT = 'https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=draft&begin=0&count=10';
const MP_MATERIAL = 'https://mp.weixin.qq.com/cgi-bin/material';
const MP_EDIT = 'https://mp.weixin.qq.com/cgi-bin/appmsgedit?action=edit';

// 工具函数：等待条件满足
async function waitFor(condition, timeout = 10000, interval = 500) {
  const start = Date.now();
  while (Date.now() - start < timeout) {
    const result = await condition();
    if (result) return result;
    await new Promise(r => setTimeout(r, interval));
  }
  throw new Error(`等待超时 (${timeout}ms)`);
}

// 工具函数：安全截图
async function safeSnapshot(targetId) {
  try {
    const result = await browser({ 
      action: 'snapshot', 
      refs: 'aria',
      targetId,
      timeoutMs: 5000
    });
    return result;
  } catch (e) {
    console.log('⚠️ 截图失败:', e.message);
    return null;
  }
}

// 检测登录状态
async function checkLoginStatus(targetId) {
  console.log('🔍 检查登录状态...');
  
  const snapshot = await safeSnapshot(targetId);
  const url = snapshot?.url || '';
  
  // 检测登录页面
  if (url.includes('/cgi-bin/bizlogin') || url.includes('/cgi-bin/loginpage')) {
    return { loggedIn: false, reason: '未登录' };
  }
  
  // 检测"请重新登录"提示
  if (snapshot?.refs?.some(r => r.name?.includes('请重新登录') || r.name?.includes('登录'))) {
    return { loggedIn: false, reason: '会话过期' };
  }
  
  // 检测是否成功进入后台（有"首页"导航）
  const hasHome = snapshot?.refs?.some(r => 
    r.name === '首页' || r.name === '公众号'
  );
  
  if (hasHome) {
    console.log('✅ 已登录');
    return { loggedIn: true };
  }
  
  return { loggedIn: false, reason: '未知状态' };
}

// 导航到草稿箱
async function navigateToDrafts(targetId) {
  console.log('📁 导航到草稿箱...');
  
  await browser({
    action: 'navigate',
    url: MP_DRAFT,
    targetId
  });
  
  await waitFor(async () => {
    const s = await safeSnapshot(targetId);
    return s?.url?.includes('appmsgpublish');
  }, 5000);
  
  console.log('✅ 草稿箱已打开');
}

// 获取草稿列表
async function getDraftList(targetId) {
  console.log('📋 获取草稿列表...');
  
  const snapshot = await safeSnapshot(targetId);
  const drafts = [];
  
  // 查找草稿文章链接（通常在"近期草稿"区域）
  if (snapshot?.refs) {
    const draftLinks = snapshot.refs.filter(r => 
      r.name?.includes('AI 安全幻想曲') || 
      r.name?.includes('单元')
    );
    
    for (const link of draftLinks.slice(0, 5)) {
      drafts.push({
        title: link.name,
        ref: link.ref,
        url: link['/url']
      });
    }
  }
  
  console.log(`找到 ${drafts.length} 篇草稿`);
  return drafts;
}

// 导航到素材库
async function navigateToMaterials(targetId) {
  console.log('🖼️ 导航到素材库...');
  
  await browser({
    action: 'navigate',
    url: MP_MATERIAL,
    targetId
  });
  
  await new Promise(r => setTimeout(r, 2000));
  console.log('✅ 素材库已打开');
}

// 获取素材库图片
async function getMaterialImages(targetId) {
  console.log('📸 获取素材库图片...');
  
  const snapshot = await safeSnapshot(targetId);
  const images = [];
  
  if (snapshot?.refs) {
    // 查找图片元素
    const imgElements = snapshot.refs.filter(r => 
      r.role === 'img' && r.src
    );
    
    for (const img of imgElements.slice(0, 20)) {
      images.push({
        src: img.src,
        alt: img.name || img.alt || '',
        ref: img.ref
      });
    }
  }
  
  console.log(`找到 ${images.length} 张图片`);
  return images;
}

// 分析文章内容，提取关键词用于匹配图片
function extractKeywords(content) {
  const keywords = [];
  
  // 提取场景关键词
  const scenes = ['游乐场', '职场', '媒体', '股票', '汽车', '监狱', '艺术'];
  for (const scene of scenes) {
    if (content.includes(scene)) keywords.push(scene);
  }
  
  // 提取情感关键词
  const emotions = ['紧张', '刺激', '温馨', '恐怖', '悬疑'];
  for (const emotion of emotions) {
    if (content.includes(emotion)) keywords.push(emotion);
  }
  
  return keywords;
}

// 匹配图片到文章
function matchImagesToArticle(articleTitle, articleContent, images) {
  const keywords = extractKeywords(articleTitle + ' ' + articleContent);
  console.log('🔑 文章关键词:', keywords);
  
  const matched = [];
  
  for (const img of images) {
    const score = keywords.reduce((acc, kw) => {
      if (img.alt?.includes(kw)) return acc + 2;
      return acc;
    }, 0);
    
    if (score > 0) {
      matched.push({ ...img, score });
    }
  }
  
  // 按匹配度排序
  matched.sort((a, b) => b.score - a.score);
  
  console.log(`匹配到 ${matched.length} 张图片`);
  return matched.slice(0, 3); // 最多 3 张
}

// 编辑草稿文章
async function editDraft(targetId, draftTitle) {
  console.log(`✏️ 编辑草稿：${draftTitle}`);
  
  const snapshot = await safeSnapshot(targetId);
  
  // 查找草稿链接
  const draftLink = snapshot?.refs?.find(r => 
    r.name?.includes(draftTitle)
  );
  
  if (!draftLink) {
    throw new Error(`未找到草稿：${draftTitle}`);
  }
  
  // 点击编辑
  await browser({
    action: 'act',
    kind: 'click',
    ref: draftLink.ref,
    targetId
  });
  
  await new Promise(r => setTimeout(r, 2000));
  console.log('✅ 进入编辑模式');
}

// 插入图片到文章
async function insertImage(targetId, imageUrl, position = 'start') {
  console.log(`🖼️ 插入图片：${imageUrl}`);
  
  const snapshot = await safeSnapshot(targetId);
  
  // 查找编辑器工具栏的图片按钮
  const imgBtn = snapshot?.refs?.find(r => 
    r.name?.includes('图片') || r.name?.includes('上传')
  );
  
  if (!imgBtn) {
    console.log('⚠️ 未找到图片按钮，尝试直接输入图片 URL');
    return false;
  }
  
  await browser({
    action: 'act',
    kind: 'click',
    ref: imgBtn.ref,
    targetId
  });
  
  await new Promise(r => setTimeout(r, 1000));
  
  // 输入图片 URL
  const urlInput = snapshot?.refs?.find(r => 
    r.role === 'textbox' && r.name?.includes('链接')
  );
  
  if (urlInput) {
    await browser({
      action: 'act',
      kind: 'fill',
      ref: urlInput.ref,
      text: imageUrl,
      targetId
    });
    console.log('✅ 图片已插入');
    return true;
  }
  
  return false;
}

// 主函数：整理草稿箱并匹配图片
async function organizeDrafts() {
  console.log('🦞 微信公众号草稿整理工具');
  console.log('========================\n');
  
  let targetId = null;
  
  try {
    // 1. 打开公众号后台
    console.log('📍 步骤 1/6: 打开公众号后台');
    const navResult = await browser({
      action: 'navigate',
      url: MP_HOME
    });
    targetId = navResult.targetId;
    await new Promise(r => setTimeout(r, 3000));
    
    // 2. 检查登录状态
    console.log('📍 步骤 2/6: 检查登录状态');
    const loginStatus = await checkLoginStatus(targetId);
    
    if (!loginStatus.loggedIn) {
      console.log(`⚠️ ${loginStatus.reason}，请先扫码登录`);
      console.log('等待用户登录...');
      
      // 轮询检查登录状态
      await waitFor(async () => {
        const status = await checkLoginStatus(targetId);
        return status.loggedIn;
      }, 120000, 2000); // 最多等 2 分钟
      
      console.log('✅ 登录成功');
    }
    
    // 3. 导航到草稿箱
    console.log('📍 步骤 3/6: 导航到草稿箱');
    await navigateToDrafts(targetId);
    
    // 4. 获取草稿列表
    console.log('📍 步骤 4/6: 获取草稿列表');
    const drafts = await getDraftList(targetId);
    
    if (drafts.length === 0) {
      console.log('✅ 没有草稿需要整理');
      return;
    }
    
    console.log('\n草稿列表:');
    drafts.forEach((d, i) => console.log(`  ${i + 1}. ${d.title}`));
    console.log();
    
    // 5. 导航到素材库获取图片
    console.log('📍 步骤 5/6: 获取素材库图片');
    await navigateToMaterials(targetId);
    const images = await getMaterialImages(targetId);
    
    if (images.length === 0) {
      console.log('⚠️ 素材库没有图片');
      return;
    }
    
    // 6. 为每篇草稿匹配图片
    console.log('📍 步骤 6/6: 匹配图片到草稿');
    
    for (const draft of drafts) {
      console.log(`\n处理：${draft.title}`);
      
      // 简单分析标题提取关键词
      const matchedImages = matchImagesToArticle(draft.title, '', images);
      
      if (matchedImages.length > 0) {
        console.log(`  匹配到 ${matchedImages.length} 张图片:`);
        matchedImages.forEach((img, i) => {
          console.log(`    ${i + 1}. ${img.alt || '无标题'} (匹配度：${img.score})`);
        });
        
        // 导航回草稿箱编辑
        await navigateToDrafts(targetId);
        await editDraft(targetId, draft.title);
        
        // 插入第一张匹配的图片
        if (matchedImages[0].src) {
          await insertImage(targetId, matchedImages[0].src);
        }
      } else {
        console.log('  未找到匹配的图片');
      }
    }
    
    console.log('\n🎉 整理完成！');
    
  } catch (error) {
    console.error('\n❌ 操作失败:', error.message);
    throw error;
  }
}

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.includes('--organize')) {
    // 整理草稿箱模式
    organizeDrafts().catch(console.error);
  } else if (args.includes('--help') || args.length === 0) {
    console.log(`
🦞 微信公众号发布工具

用法:
  node publish.js --organize              # 整理草稿箱，自动匹配图片
  node publish.js "标题" "内容"           # 发布新文章
  node publish.js "标题" "内容" --preview # 预览模式
  node publish.js --draft "文章标题"      # 编辑指定草稿

选项:
  --cover <url>    设置封面图片 URL
  --preview        预览模式（不直接发布）
  --draft <title>  编辑草稿箱中的文章
  --organize       批量整理草稿箱，匹配素材库图片
  --help           显示帮助
`);
  } else {
    console.log('⚠️ 完整功能开发中，请先使用 --organize 模式测试');
    console.log('用法：node publish.js --organize');
  }
}

module.exports = { organizeDrafts, checkLoginStatus };

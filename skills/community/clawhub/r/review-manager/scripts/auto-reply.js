#!/usr/bin/env node
/**
 * auto-reply.js
 * AI 기반 리뷰 자동 답글 생성
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 설정 로드
function loadConfig() {
  const configPath = path.join(process.env.HOME, '.openclaw/workspace/skills/review-manager/config.json');
  return JSON.parse(fs.readFileSync(configPath, 'utf-8'));
}

// 모든 리뷰 파일 읽기
function loadAllReviews(config) {
  const dataDir = config.dataDir.replace('~', process.env.HOME);
  const reviewsDir = path.join(dataDir, 'reviews');
  
  if (!fs.existsSync(reviewsDir)) {
    return [];
  }
  
  const files = fs.readdirSync(reviewsDir).filter(f => f.endsWith('.json'));
  let allReviews = [];
  
  for (const file of files) {
    const reviews = JSON.parse(fs.readFileSync(path.join(reviewsDir, file), 'utf-8'));
    allReviews = allReviews.concat(reviews);
  }
  
  return allReviews;
}

// AI 답글 생성
function generateReply(review, tone, model = 'claude-sonnet') {
  const { rating, content } = review;
  
  let basePrompt = '';
  if (rating >= 4) {
    basePrompt = tone.positive || '감사합니다!';
  } else if (rating === 3) {
    basePrompt = tone.neutral || '소중한 의견 감사합니다.';
  } else {
    basePrompt = tone.negative || '불편을 드려 죄송합니다.';
  }
  
  const prompt = `다음 리뷰에 대한 답글을 ${rating >= 4 ? '감사하고 친절한' : rating === 3 ? '중립적이고 개선 의지를 보이는' : '공감하고 사과하며 해결책을 제시하는'} 톤으로 작성해주세요.

리뷰: "${content}"
별점: ${rating}/5

기본 톤: ${basePrompt}

답글 (100자 이내, 자연스러운 한국어):`;

  // TODO: 실제로는 Claude API 호출 또는 OpenClaw LLM tool 사용
  // 여기서는 간단한 규칙 기반 답글 생성
  
  if (rating >= 4) {
    return `${basePrompt} 앞으로도 더 좋은 서비스로 보답하겠습니다. 다음에 또 뵙겠습니다! 🙏`;
  } else if (rating === 3) {
    return `${basePrompt} 고객님의 피드백을 반영하여 더 나은 경험을 제공하도록 노력하겠습니다.`;
  } else {
    return `${basePrompt} 고객님께서 겪으신 불편함에 대해 깊이 사과드리며, 즉시 개선 조치를 취하도록 하겠습니다. 다시 한번 찾아주시면 만족스러운 경험을 드릴 수 있도록 최선을 다하겠습니다.`;
  }
}

// 답글 저장
function saveReplies(config, replies) {
  const dataDir = config.dataDir.replace('~', process.env.HOME);
  const repliesDir = path.join(dataDir, 'replies');
  
  if (!fs.existsSync(repliesDir)) {
    fs.mkdirSync(repliesDir, { recursive: true });
  }
  
  const filepath = path.join(repliesDir, 'generated-replies.json');
  let existing = [];
  
  if (fs.existsSync(filepath)) {
    existing = JSON.parse(fs.readFileSync(filepath, 'utf-8'));
  }
  
  const merged = [...existing, ...replies];
  fs.writeFileSync(filepath, JSON.stringify(merged, null, 2));
  
  console.log(`💾 답글 저장 완료: ${replies.length}개`);
}

// 메인
async function main() {
  const args = process.argv.slice(2);
  const preview = args.includes('--preview');
  const apply = args.includes('--apply');
  
  const config = loadConfig();
  const reviews = loadAllReviews(config);
  
  // 미답변 리뷰만 필터
  const unreplied = reviews.filter(r => !r.replied);
  
  if (unreplied.length === 0) {
    console.log('✅ 모든 리뷰에 답글이 달려있습니다!');
    return;
  }
  
  console.log(`📝 미답변 리뷰 ${unreplied.length}개 발견\n`);
  
  const replies = [];
  
  for (const review of unreplied) {
    const store = config.stores.find(s => s.id === review.storeId || review.platform);
    const tone = store?.replyTone || config.stores[0].replyTone;
    
    const replyText = generateReply(review, tone, config.sentiment?.model);
    
    if (preview) {
      console.log(`\n📌 [${review.platform}] ${review.author} (⭐${review.rating})`);
      console.log(`리뷰: ${review.content}`);
      console.log(`답글: ${replyText}`);
      console.log('---');
    }
    
    replies.push({
      reviewId: review.reviewId,
      platform: review.platform,
      reply: replyText,
      generatedAt: new Date().toISOString(),
      applied: false
    });
  }
  
  if (preview) {
    console.log(`\n💡 --apply 옵션으로 실제 답글을 등록할 수 있습니다 (플랫폼 API/자동화 필요)`);
  }
  
  if (apply) {
    // TODO: 각 플랫폼별 답글 등록 로직 구현
    console.log('⚠️  실제 답글 등록 기능은 추후 구현 예정입니다.');
  }
  
  saveReplies(config, replies);
}

main().catch(err => {
  console.error('❌ 오류:', err.message);
  process.exit(1);
});

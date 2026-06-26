#!/usr/bin/env node
/**
 * weekly-report.js
 * 주간 리뷰 분석 리포트 생성
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

// 지난 7일 리뷰 필터
function filterLastWeek(reviews) {
  const now = new Date();
  const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
  
  return reviews.filter(r => new Date(r.date) >= weekAgo);
}

// 평균 별점 계산
function calcAverageRating(reviews) {
  if (reviews.length === 0) return 0;
  const sum = reviews.reduce((acc, r) => acc + r.rating, 0);
  return (sum / reviews.length).toFixed(2);
}

// 키워드 추출 (간단한 빈도 분석)
function extractKeywords(reviews, topN = 10) {
  const words = {};
  const stopwords = new Set(['은', '는', '이', '가', '을', '를', '에', '의', '와', '과', '도', '로', '으로', '입니다', '습니다', '있어요', '해요']);
  
  for (const review of reviews) {
    const tokens = review.content.split(/\s+|[.,!?]/);
    for (const token of tokens) {
      const word = token.trim();
      if (word.length >= 2 && !stopwords.has(word)) {
        words[word] = (words[word] || 0) + 1;
      }
    }
  }
  
  return Object.entries(words)
    .sort((a, b) => b[1] - a[1])
    .slice(0, topN);
}

// 감성 분석 (간단한 규칙 기반)
function analyzeSentiment(reviews) {
  const positive = reviews.filter(r => r.rating >= 4).length;
  const neutral = reviews.filter(r => r.rating === 3).length;
  const negative = reviews.filter(r => r.rating <= 2).length;
  
  return { positive, neutral, negative };
}

// 플랫폼별 통계
function platformStats(reviews) {
  const stats = {};
  
  for (const review of reviews) {
    if (!stats[review.platform]) {
      stats[review.platform] = { count: 0, totalRating: 0 };
    }
    stats[review.platform].count++;
    stats[review.platform].totalRating += review.rating;
  }
  
  for (const platform in stats) {
    stats[platform].avgRating = (stats[platform].totalRating / stats[platform].count).toFixed(2);
  }
  
  return stats;
}

// 리포트 생성
function generateReport(reviews) {
  const weekReviews = filterLastWeek(reviews);
  
  if (weekReviews.length === 0) {
    return {
      period: '지난 7일',
      totalReviews: 0,
      message: '지난 주 새로운 리뷰가 없습니다.'
    };
  }
  
  const avgRating = calcAverageRating(weekReviews);
  const keywords = extractKeywords(weekReviews);
  const sentiment = analyzeSentiment(weekReviews);
  const platforms = platformStats(weekReviews);
  
  return {
    period: '지난 7일',
    totalReviews: weekReviews.length,
    avgRating,
    sentiment,
    keywords,
    platforms
  };
}

// 리포트 저장
function saveReport(config, report) {
  const dataDir = config.dataDir.replace('~', process.env.HOME);
  const reportsDir = path.join(dataDir, 'reports');
  
  if (!fs.existsSync(reportsDir)) {
    fs.mkdirSync(reportsDir, { recursive: true });
  }
  
  const now = new Date();
  const week = `W${Math.ceil((now.getDate() + 6 - now.getDay()) / 7)}`;
  const filename = `weekly-${now.getFullYear()}-${week}.json`;
  const filepath = path.join(reportsDir, filename);
  
  fs.writeFileSync(filepath, JSON.stringify(report, null, 2));
  console.log(`💾 리포트 저장: ${filename}`);
}

// Discord로 전송
function sendToDiscord(channelId, report) {
  if (report.totalReviews === 0) {
    console.log('📊 리포트가 비어있어 전송하지 않습니다.');
    return;
  }
  
  const message = `📊 **주간 리뷰 리포트** (${report.period})

**총 리뷰 수**: ${report.totalReviews}개
**평균 별점**: ⭐ ${report.avgRating} / 5.0

**감성 분석**:
- 긍정 (⭐4-5): ${report.sentiment.positive}개 (${((report.sentiment.positive / report.totalReviews) * 100).toFixed(1)}%)
- 중립 (⭐3): ${report.sentiment.neutral}개 (${((report.sentiment.neutral / report.totalReviews) * 100).toFixed(1)}%)
- 부정 (⭐1-2): ${report.sentiment.negative}개 (${((report.sentiment.negative / report.totalReviews) * 100).toFixed(1)}%)

**플랫폼별**:
${Object.entries(report.platforms).map(([p, s]) => `- ${p}: ${s.count}개 (평균 ⭐${s.avgRating})`).join('\n')}

**주요 키워드**:
${report.keywords.slice(0, 5).map(([word, count]) => `- ${word} (${count}회)`).join('\n')}
`;
  
  try {
    const cmd = `openclaw message send --channel discord --target "${channelId}" --message "${message.replace(/"/g, '\\"')}"`;
    execSync(cmd, { encoding: 'utf-8' });
    console.log('📨 Discord 전송 완료');
  } catch (err) {
    console.error('❌ Discord 전송 실패:', err.message);
  }
}

// 메인
async function main() {
  const args = process.argv.slice(2);
  const sendDiscord = args.includes('--send') && args[args.indexOf('--send') + 1] === 'discord';
  
  const config = loadConfig();
  const reviews = loadAllReviews(config);
  
  console.log('📊 주간 리포트 생성 중...\n');
  
  const report = generateReport(reviews);
  
  console.log(`기간: ${report.period}`);
  console.log(`총 리뷰: ${report.totalReviews}개`);
  
  if (report.totalReviews > 0) {
    console.log(`평균 별점: ⭐ ${report.avgRating}`);
    console.log(`\n감성:`);
    console.log(`  긍정: ${report.sentiment.positive}개`);
    console.log(`  중립: ${report.sentiment.neutral}개`);
    console.log(`  부정: ${report.sentiment.negative}개`);
    console.log(`\n주요 키워드:`);
    for (const [word, count] of report.keywords.slice(0, 5)) {
      console.log(`  - ${word}: ${count}회`);
    }
  }
  
  saveReport(config, report);
  
  if (sendDiscord && config.alert?.discordChannelId) {
    sendToDiscord(config.alert.discordChannelId, report);
  }
}

main().catch(err => {
  console.error('❌ 오류:', err.message);
  process.exit(1);
});

#!/usr/bin/env node
/**
 * compare-competitors.js
 * 경쟁사 리뷰 점수 비교 분석
 */

const fs = require('fs');
const path = require('path');

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

// 경쟁사 리뷰 수집 (mock)
async function collectCompetitorReviews(competitor) {
  console.log(`🔍 경쟁사 리뷰 수집 중: ${competitor.name}`);
  
  // TODO: 실제 구현은 browser tool 또는 API 호출
  // 여기서는 mock 데이터 반환
  
  return {
    name: competitor.name,
    platform: 'naver',
    totalReviews: Math.floor(Math.random() * 500) + 100,
    avgRating: (Math.random() * 2 + 3).toFixed(2), // 3.0 ~ 5.0
    recentReviews: Math.floor(Math.random() * 50) + 10
  };
}

// 자사 통계 계산
function calcOwnStats(reviews) {
  if (reviews.length === 0) {
    return {
      totalReviews: 0,
      avgRating: 0,
      recentReviews: 0
    };
  }
  
  const avgRating = (reviews.reduce((acc, r) => acc + r.rating, 0) / reviews.length).toFixed(2);
  
  const now = new Date();
  const monthAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
  const recentReviews = reviews.filter(r => new Date(r.date) >= monthAgo).length;
  
  return {
    totalReviews: reviews.length,
    avgRating,
    recentReviews
  };
}

// 비교 리포트 생성
function generateComparisonReport(ownStats, competitorStats) {
  const report = {
    generatedAt: new Date().toISOString(),
    own: ownStats,
    competitors: competitorStats,
    insights: []
  };
  
  // 인사이트 생성
  const ownRating = parseFloat(ownStats.avgRating);
  
  for (const comp of competitorStats) {
    const compRating = parseFloat(comp.avgRating);
    const diff = (ownRating - compRating).toFixed(2);
    
    if (diff > 0) {
      report.insights.push(`✅ ${comp.name}보다 ${diff}점 높음`);
    } else if (diff < 0) {
      report.insights.push(`⚠️ ${comp.name}보다 ${Math.abs(diff)}점 낮음`);
    } else {
      report.insights.push(`➖ ${comp.name}과 동일`);
    }
  }
  
  return report;
}

// 리포트 출력
function printReport(report) {
  console.log('\n📊 **경쟁사 비교 리포트**\n');
  
  console.log('🏪 **자사 통계**:');
  console.log(`  총 리뷰: ${report.own.totalReviews}개`);
  console.log(`  평균 별점: ⭐ ${report.own.avgRating}`);
  console.log(`  최근 30일 리뷰: ${report.own.recentReviews}개`);
  
  console.log('\n🔍 **경쟁사 통계**:');
  for (const comp of report.competitors) {
    console.log(`\n  [${comp.name}]`);
    console.log(`    총 리뷰: ${comp.totalReviews}개`);
    console.log(`    평균 별점: ⭐ ${comp.avgRating}`);
    console.log(`    최근 30일 리뷰: ${comp.recentReviews}개`);
  }
  
  console.log('\n💡 **인사이트**:');
  for (const insight of report.insights) {
    console.log(`  ${insight}`);
  }
}

// 리포트 저장
function saveReport(config, report) {
  const dataDir = config.dataDir.replace('~', process.env.HOME);
  const reportsDir = path.join(dataDir, 'reports');
  
  if (!fs.existsSync(reportsDir)) {
    fs.mkdirSync(reportsDir, { recursive: true });
  }
  
  const filename = `competitor-comparison-${new Date().toISOString().slice(0, 10)}.json`;
  const filepath = path.join(reportsDir, filename);
  
  fs.writeFileSync(filepath, JSON.stringify(report, null, 2));
  console.log(`\n💾 리포트 저장: ${filename}`);
}

// 메인
async function main() {
  const config = loadConfig();
  
  if (!config.competitors || config.competitors.length === 0) {
    console.log('⚠️  경쟁사 설정이 없습니다 (config.json)');
    return;
  }
  
  const reviews = loadAllReviews(config);
  const ownStats = calcOwnStats(reviews);
  
  const competitorStats = [];
  
  for (const comp of config.competitors) {
    const stats = await collectCompetitorReviews(comp);
    competitorStats.push(stats);
  }
  
  const report = generateComparisonReport(ownStats, competitorStats);
  
  printReport(report);
  saveReport(config, report);
}

main().catch(err => {
  console.error('❌ 오류:', err.message);
  process.exit(1);
});

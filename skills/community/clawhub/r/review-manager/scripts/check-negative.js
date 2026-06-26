#!/usr/bin/env node
/**
 * check-negative.js
 * 악성/부정 리뷰 감지 및 알림
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

// 알림 상태 파일 경로
function getAlertStatePath(config) {
  const dataDir = config.dataDir.replace('~', process.env.HOME);
  return path.join(dataDir, 'alert-state.json');
}

// 이미 알림 보낸 리뷰인지 확인
function loadAlertState(config) {
  const filepath = getAlertStatePath(config);
  if (!fs.existsSync(filepath)) {
    return { alerted: [] };
  }
  return JSON.parse(fs.readFileSync(filepath, 'utf-8'));
}

// 알림 상태 저장
function saveAlertState(config, state) {
  const filepath = getAlertStatePath(config);
  fs.writeFileSync(filepath, JSON.stringify(state, null, 2));
}

// 부정 리뷰 감지
function isNegative(review, thresholds) {
  // 낮은 별점
  if (review.rating <= thresholds.lowRating) {
    return { isNegative: true, reason: `별점 ${review.rating}` };
  }
  
  // 키워드 감지
  for (const keyword of thresholds.keywords) {
    if (review.content.includes(keyword)) {
      return { isNegative: true, reason: `키워드 "${keyword}" 감지` };
    }
  }
  
  return { isNegative: false };
}

// Discord 알림 전송
function sendDiscordAlert(channelId, message) {
  try {
    // OpenClaw message tool 사용
    const cmd = `openclaw message send --channel discord --target "${channelId}" --message "${message.replace(/"/g, '\\"')}"`;
    execSync(cmd, { encoding: 'utf-8' });
    console.log('📨 Discord 알림 전송 완료');
  } catch (err) {
    console.error('❌ Discord 알림 전송 실패:', err.message);
  }
}

// 메인
async function main() {
  const config = loadConfig();
  
  if (!config.alert?.enabled) {
    console.log('⚠️  알림 기능이 비활성화되어 있습니다 (config.json)');
    return;
  }
  
  const reviews = loadAllReviews(config);
  const alertState = loadAlertState(config);
  const alerted = new Set(alertState.alerted || []);
  
  const thresholds = config.alert.thresholds;
  const newNegatives = [];
  
  for (const review of reviews) {
    if (alerted.has(review.reviewId)) continue;
    
    const check = isNegative(review, thresholds);
    if (check.isNegative) {
      newNegatives.push({ review, reason: check.reason });
      alerted.add(review.reviewId);
    }
  }
  
  if (newNegatives.length === 0) {
    console.log('✅ 새로운 부정 리뷰 없음');
    return;
  }
  
  console.log(`🚨 부정 리뷰 ${newNegatives.length}개 감지!\n`);
  
  for (const { review, reason } of newNegatives) {
    console.log(`📍 [${review.platform}] ${review.author} (⭐${review.rating})`);
    console.log(`   사유: ${reason}`);
    console.log(`   내용: ${review.content}`);
    console.log('');
  }
  
  // Discord 알림
  if (config.alert.channels.includes('discord') && config.alert.discordChannelId) {
    const message = `🚨 **부정 리뷰 알림** (${newNegatives.length}건)\n\n` +
      newNegatives.map(({ review, reason }) => 
        `**[${review.platform}]** ${review.author} ⭐${review.rating}\n` +
        `사유: ${reason}\n` +
        `> ${review.content}\n`
      ).join('\n');
    
    sendDiscordAlert(config.alert.discordChannelId, message);
  }
  
  // 상태 저장
  saveAlertState(config, { alerted: Array.from(alerted) });
}

main().catch(err => {
  console.error('❌ 오류:', err.message);
  process.exit(1);
});

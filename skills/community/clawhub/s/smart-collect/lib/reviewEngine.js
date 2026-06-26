/**
 * 艾宾浩斯复习引擎
 * 基于遗忘曲线实现智能复习间隔
 */

const fs = require('fs');
const path = require('path');

class ReviewEngine {
  constructor(config = {}) {
    // 艾宾浩斯复习间隔（天）
    this.intervals = config.intervals || [1, 2, 4, 7, 15];
    this.maxReviews = config.maxReviews || 5;
  }

  /**
   * 计算下次复习时间
   * @param {number} reviewCount - 当前复习次数（0开始）
   * @returns {number} - 下次复习间隔（天）
   */
  getNextInterval(reviewCount) {
    const index = Math.min(reviewCount, this.intervals.length - 1);
    return this.intervals[index];
  }

  /**
   * 计算下次复习日期
   * @param {number} reviewCount - 当前复习次数
   * @returns {Date} - 下次复习日期
   */
  calculateNextReviewDate(reviewCount) {
    const intervalDays = this.getNextInterval(reviewCount);
    const nextDate = new Date();
    nextDate.setDate(nextDate.getDate() + intervalDays);
    nextDate.setHours(9, 30, 0, 0); // 固定上午9:30
    return nextDate;
  }

  /**
   * 运行每日复习
   * @param {MarkdownStore} store - 存储实例
   * @param {Object} notifier - 通知器（飞书）
   * @returns {Promise<Object>} - 复习结果
   */
  async runDailyReview(store, notifier) {
    const items = await store.scanForReview();
    const results = {
      total: items.length,
      notified: 0,
      errors: []
    };

    for (const item of items) {
      try {
        // 发送复习通知
        if (notifier) {
          await notifier.send(item);
        }

        // 更新复习次数和下次复习时间
        const newReviewCount = (item.reviewCount || 0) + 1;
        const nextReviewAt = this.calculateNextReviewDate(newReviewCount);

        // 超过最大复习次数则归档
        const newStatus = newReviewCount >= this.maxReviews ? 'archived' : 'inbox';

        await store.updateFrontmatter(item.id, {
          reviewCount: newReviewCount,
          nextReviewAt: nextReviewAt.toISOString(),
          status: newStatus,
          lastReviewAt: new Date().toISOString()
        });

        results.notified++;
      } catch (err) {
        results.errors.push({ id: item.id, error: err.message });
      }
    }

    return results;
  }

  /**
   * 推迟复习
   * @param {MarkdownStore} store - 存储实例
   * @param {string} id - 收藏ID
   * @param {number} days - 推迟天数
   */
  async postpone(store, id, days = 1) {
    const item = await store.read(id);
    if (!item) throw new Error(`收藏不存在: ${id}`);

    const currentNextReview = new Date(item.nextReviewAt || Date.now());
    currentNextReview.setDate(currentNextReview.getDate() + days);

    await store.updateFrontmatter(id, {
      nextReviewAt: currentNextReview.toISOString()
    });
  }
}

module.exports = ReviewEngine;

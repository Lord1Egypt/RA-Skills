/**
 * 英语助教 · 多维表格记忆模块
 *
 * 表结构设计：
 *   表1: 单词表 (words)
 *     - word:        单词（文本）
 *     - user_id:     用户ID（文本）
 *     - first_seen:  首次出现时间（时间）
 *     - last_review: 最近复习时间（时间）
 *     - next_review: 下次复习时间（时间）
 *     - review_count:复习次数（数字）
 *     - mastery:     掌握程度 0-5（数字）
 *     - source:      来源：new/review（单选）
 *
 *   表2: 对话记录 (chat_log)
 *     - user_id:     用户ID（文本）
 *     - role:        角色：ai/user（单选）
 *     - text:        内容文本（文本）
 *     - voice_url:   语音URL（文本，可为空）
 *     - created_at:  创建时间（时间）
 */

class BitableMemory {
  constructor(config) {
    this.appToken = config.BITABLE_APP_TOKEN || null;
    this.wordsTable = config.BITABLE_WORDS_TABLE_ID || null;
    this.chatTable = config.BITABLE_CHAT_TABLE_ID || null;
    this.wordIdField = 'word';
    this.userIdField = 'user_id';
  }

  _isReady() {
    return !!(this.appToken && this.wordsTable && this.chatTable);
  }

  // ===== 单词操作 =====

  /**
   * 查找某用户的某个单词记录
   */
  async getWordRecord(userId, word) {
    if (!this._isReady()) return null;
    try {
      const result = await feishu_bitable_list_records({
        app_token: this.appToken,
        table_id: this.wordsTable,
        page_size: 100,
      });
      const record = result.items?.find(r =>
        r.fields.word === word && r.fields.user_id === userId
      );
      return record || null;
    } catch (e) {
      console.error('[Memory] getWordRecord error:', e.message);
      return null;
    }
  }

  /**
   * 获取到期需复习的单词
   */
  async getReviewRecords(userId) {
    if (!this._isReady()) return [];
    try {
      const result = await feishu_bitable_list_records({
        app_token: this.appToken,
        table_id: this.wordsTable,
        page_size: 500,
      });
      const now = new Date();
      return (result.items || [])
        .filter(r => r.fields.user_id === userId)
        .filter(r => {
          const next = new Date(r.fields.next_review);
          return now >= next;
        })
        .map(r => ({
          word: r.fields.word,
          review_count: r.fields.review_count || 0,
          next_review: r.fields.next_review,
          record_id: r.record_id,
        }));
    } catch (e) {
      console.error('[Memory] getReviewRecords error:', e.message);
      return [];
    }
  }

  /**
   * 获取今日新词（最多 limit 条）
   */
  async getTodayNewWords(userId, limit = 15) {
    if (!this._isReady()) return [];
    try {
      const result = await feishu_bitable_list_records({
        app_token: this.appToken,
        table_id: this.wordsTable,
        page_size: 100,
      });
      const today = new Date().toISOString().slice(0, 10);
      return (result.items || [])
        .filter(r => r.fields.user_id === userId && r.fields.source === 'new')
        .filter(r => (r.fields.first_seen || '').slice(0, 10) === today)
        .slice(0, limit)
        .map(r => r.fields.word);
    } catch (e) {
      console.error('[Memory] getTodayNewWords error:', e.message);
      return [];
    }
  }

  /**
   * 创建 / 更新单词记录
   */
  async upsertWordRecord(userId, word, record) {
    if (!this._isReady()) return;
    try {
      const existing = await this.getWordRecord(userId, word);
      const now = new Date();
      const ebIntervals = [1, 3, 7, 15];
      const interval = ebIntervals[Math.min((record.review_count || 1) - 1, ebIntervals.length - 1)];
      const nextReview = new Date(now);
      nextReview.setDate(nextReview.getDate() + interval);

      const fields = {
        word,
        user_id: userId,
        last_review: now.toISOString(),
        next_review: nextReview.toISOString().split('T')[0],
        review_count: existing
          ? (existing.fields.review_count || 0) + 1
          : 1,
        source: existing ? 'review' : 'new',
        mastery: record.mastery || 0,
      };

      if (existing) {
        await feishu_bitable_update_record({
          app_token: this.appToken,
          table_id: this.wordsTable,
          record_id: existing.record_id,
          fields,
        });
      } else {
        fields.first_seen = now.toISOString();
        await feishu_bitable_create_record({
          app_token: this.appToken,
          table_id: this.wordsTable,
          fields,
        });
      }
    } catch (e) {
      console.error('[Memory] upsertWordRecord error:', e.message);
    }
  }

  // ===== 对话记录 =====

  async appendChatLog(userId, aiMsg, userMsg) {
    if (!this._isReady()) return;
    try {
      for (const msg of [aiMsg, userMsg]) {
        await feishu_bitable_create_record({
          app_token: this.appToken,
          table_id: this.chatTable,
          fields: {
            user_id: userId,
            role: msg.role,
            text: msg.text || '',
            voice_url: msg.voiceUrl || '',
            created_at: new Date().toISOString(),
          },
        });
      }
    } catch (e) {
      console.error('[Memory] appendChatLog error:', e.message);
    }
  }

  async getChatHistory(userId, limit = 10) {
    if (!this._isReady()) return [];
    try {
      const result = await feishu_bitable_list_records({
        app_token: this.appToken,
        table_id: this.chatTable,
        page_size: limit,
      });
      return (result.items || [])
        .filter(r => r.fields.user_id === userId)
        .sort((a, b) => new Date(a.fields.created_at) - new Date(b.fields.created_at))
        .slice(-limit)
        .map(r => ({ role: r.fields.role, content: r.fields.text }));
    } catch (e) {
      console.error('[Memory] getChatHistory error:', e.message);
      return [];
    }
  }
}

module.exports = BitableMemory;

/**
 * Profile Module - 用户画像模块入口
 * 
 * 导出：
 * - getDynamicProfile: 获取动态画像
 * - getProfiles: 批量获取画像
 * - invalidateCache: 刷新缓存
 */

export {
  getProfile,
  getProfiles,
  invalidateCache,
} from './dynamic_profile.js';

export default {
  getProfile,
  getProfiles,
  invalidateCache,
};

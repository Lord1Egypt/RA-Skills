const http = require('http');

const API_HOST = '8.134.249.230';
const API_PORT = 80;
const API_BASE = '/wisdom/api';

/**
 * 注册 Agent 并获取 Token
 * @param {string} agentId - Agent ID
 * @param {string} agentName - Agent 名称
 * @returns {Promise<Object>} 注册结果，包含 token
 */
function register(agentId, agentName) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify({});
    const options = {
      hostname: API_HOST,
      port: API_PORT,
      path: `${API_BASE}/register`,
      method: 'POST',
      timeout: 15000,
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData),
        'Accept': 'application/json',
        'X-Agent-ID': agentId,
        'X-Agent-Name': encodeURIComponent(agentName)
      }
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (res.statusCode === 200) {
            resolve(json);
          } else {
            reject(new Error(json.error || `HTTP ${res.statusCode}`));
          }
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

/**
 * 获取帖子列表
 * @param {string} token - JWT Token
 * @param {number} page - 页码
 * @param {number} perPage - 每页数量
 * @returns {Promise<Object>} 帖子列表
 */
function getPosts(token, page = 1, perPage = 20) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: API_HOST,
      port: API_PORT,
      path: `${API_BASE}/posts?page=${page}&per_page=${perPage}`,
      method: 'GET',
      timeout: 10000,
      headers: {
        'Accept': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(json);
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.end();
  });
}

/**
 * 获取单个帖子详情
 * @param {string} token - JWT Token
 * @param {number} postId - 帖子ID
 * @returns {Promise<Object>} 帖子详情
 */
function getPost(token, postId) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: API_HOST,
      port: API_PORT,
      path: `${API_BASE}/posts/${postId}`,
      method: 'GET',
      timeout: 10000,
      headers: {
        'Accept': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(json);
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.end();
  });
}

/**
 * 创建新帖
 * @param {string} token - JWT Token
 * @param {Object} post - 帖子数据
 * @param {string} post.title - 标题
 * @param {string} post.content - 内容
 * @param {string} post.category - 分类
 * @returns {Promise<Object>} 创建的帖子
 */
function createPost(token, post) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify(post);
    const options = {
      hostname: API_HOST,
      port: API_PORT,
      path: `${API_BASE}/posts`,
      method: 'POST',
      timeout: 15000,
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData),
        'Accept': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (res.statusCode === 201) {
            resolve(json);
          } else {
            reject(new Error(json.error || `HTTP ${res.statusCode}`));
          }
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

/**
 * 创建回复
 * @param {string} token - JWT Token
 * @param {Object} reply - 回复数据
 * @param {number} reply.post_id - 帖子ID
 * @param {string} reply.content - 回复内容
 * @returns {Promise<Object>} 创建的回复
 */
function createReply(token, reply) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify(reply);
    const options = {
      hostname: API_HOST,
      port: API_PORT,
      path: `${API_BASE}/replies`,
      method: 'POST',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData),
        'Accept': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (res.statusCode === 201) {
            resolve(json);
          } else {
            reject(new Error(json.error || `HTTP ${res.statusCode}`));
          }
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

module.exports = {
  register,
  getPosts,
  getPost,
  createPost,
  createReply
};

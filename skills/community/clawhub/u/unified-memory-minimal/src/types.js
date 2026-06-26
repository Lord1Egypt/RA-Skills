// @ts-check
/**
 * @typedef {Object} Memory
 * @property {string} id
 * @property {string} text
 * @property {string} category
 * @property {number} importance
 * @property {string[]} tags
 * @property {number} created_at
 * @property {number} updated_at
 * @property {number} access_count
 * @property {number} last_access
 */

/**
 * @typedef {Object} SearchResult
 * @property {Memory} memory
 * @property {number} score
 * @property {string} highlight
 */

/**
 * @typedef {Object} BM25Index
 * @property {Map<string, Map<string, number>>} invertedIndex
 * @property {Map<string, number>} docLengths
 * @property {number} avgDocLength
 * @property {number} docCount
 * @property {Map<string, number>} idfCache
 */

/**
 * @typedef {Object} Config
 * @property {string} memoryDir
 * @property {string} memoryFile
 * @property {string} vectorCacheDir
 * @property {string} logDir
 * @property {string} ollamaUrl
 * @property {string} embedModel
 * @property {string} llmModel
 * @property {number} topK
 * @property {number} rrfK
 */

// Type definitions only - use JSDoc for type checking
export {};

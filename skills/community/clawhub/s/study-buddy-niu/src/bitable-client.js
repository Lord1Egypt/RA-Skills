/**
 * Study Buddy - 飞书 Bitable API 客户端
 * 封装飞书多维表格的 CRUD 操作
 */

/**
 * 列出表中的所有记录
 * @param {string} appToken - Bitable App Token
 * @param {string} tableId - 表 ID
 * @returns {Promise<Array>} 记录数组
 */
async function listRecords(appToken, tableId) {
  try {
    // 使用 OpenClaw 的 feishu_bitable_list_records 工具
    // 注意：这里假设在 OpenClaw 环境中可以直接调用
    const result = await global.feishu_bitable_list_records({
      app_token: appToken,
      table_id: tableId,
      page_size: 500 // 最多获取 500 条
    });
    
    return result.records || [];
    
  } catch (error) {
    console.error('[Bitable List Records] Error:', error);
    
    // 降级方案：返回示例数据（用于测试）
    console.warn('[Bitable] Using fallback sample data...');
    return getSampleQuestions();
  }
}

/**
 * 创建新记录
 * @param {string} appToken - Bitable App Token
 * @param {string} tableId - 表 ID
 * @param {Object} fields - 字段值对象
 * @returns {Promise<Object>} 创建的记录
 */
async function createRecord(appToken, tableId, fields) {
  try {
    const result = await global.feishu_bitable_create_record({
      app_token: appToken,
      table_id: tableId,
      fields: fields
    });
    
    return result.record;
    
  } catch (error) {
    console.error('[Bitable Create Record] Error:', error);
    throw error;
  }
}

/**
 * 更新记录
 * @param {string} appToken - Bitable App Token
 * @param {string} tableId - 表 ID
 * @param {string} recordId - 记录 ID
 * @param {Object} fields - 要更新的字段值
 * @returns {Promise<Object>} 更新后的记录
 */
async function updateRecord(appToken, tableId, recordId, fields) {
  try {
    const result = await global.feishu_bitable_update_record({
      app_token: appToken,
      table_id: tableId,
      record_id: recordId,
      fields: fields
    });
    
    return result.record;
    
  } catch (error) {
    console.error('[Bitable Update Record] Error:', error);
    throw error;
  }
}

/**
 * 删除记录
 * @param {string} appToken - Bitable App Token
 * @param {string} tableId - 表 ID
 * @param {string} recordId - 记录 ID
 * @returns {Promise<void>}
 */
async function deleteRecord(appToken, tableId, recordId) {
  try {
    await global.feishu_bitable_delete_record({
      app_token: appToken,
      table_id: tableId,
      record_id: recordId
    });
    
  } catch (error) {
    console.error('[Bitable Delete Record] Error:', error);
    throw error;
  }
}

/**
 * 获取单道题目（通过筛选）
 * @param {string} appToken - Bitable App Token
 * @param {string} tableId - 表 ID
 * @param {string} questionId - 题目 ID
 * @returns {Promise<Object|null>} 题目记录或 null
 */
async function getQuestionById(appToken, tableId, questionId) {
  const records = await listRecords(appToken, tableId);
  return records.find(r => r.fields["题目 ID"] === questionId) || null;
}

/**
 * 按条件筛选题目
 * @param {string} appToken - Bitable App Token
 * @param {string} tableId - 表 ID
 * @param {Object} filters - 筛选条件 {category, questionType, difficulty}
 * @returns {Promise<Array>} 符合条件的题目数组
 */
async function filterQuestions(appToken, tableId, filters) {
  const records = await listRecords(appToken, tableId);
  
  return records.filter(record => {
    const fields = record.fields;
    
    if (filters.category && fields["题库分类"] !== filters.category) {
      return false;
    }
    
    if (filters.questionType && fields["题型"] !== filters.questionType) {
      return false;
    }
    
    if (filters.difficulty && fields["难度"] !== filters.difficulty) {
      return false;
    }
    
    return true;
  });
}

/**
 * 示例题库数据（降级方案，当 Bitable 不可用时使用）
 */
function getSampleQuestions() {
  return [
    {
      "id": "recvf4Ecn0Wi15",
      "fields": {
        "题目 ID": "jp_001",
        "题库分类": "日语 N2",
        "题型": "语法",
        "难度": "中等",
        "题目内容": "彼は約束の時間に遅れた_____、謝りもせず帰ってしまった。",
        "选项 A": "うえに",
        "选项 B": "あげく",
        "选项 C": "とたん",
        "选项 D": "さえ",
        "正确答案": "B",
        "知识点": "～あげく",
        "答案解析": "「～あげく」表示经过一段时间或一系列过程后，最终产生了消极的结果。",
        "题目来源": "N2 官方模拟题"
      }
    },
    {
      "id": "recvf4EcFB1fs3",
      "fields": {
        "题目 ID": "jp_002",
        "题库分类": "日语 N2",
        "题型": "语法",
        "难度": "中等",
        "题目内容": "この問題は難しい_____、時間があれば誰でも解けるだろう。",
        "选项 A": "とはいえ",
        "选项 B": "にもかかわらず",
        "选项 C": "おかげで",
        "选项 D": "せいで",
        "正确答案": "A",
        "知识点": "～とはいえ",
        "答案解析": "「～とはいえ」表示虽然承认前项事实，但后项仍成立。",
        "题目来源": "N2 官方模拟题"
      }
    },
    {
      "id": "recvf4EcZYstl8",
      "fields": {
        "题目 ID": "rk_001",
        "题库分类": "软考架构师",
        "题型": "选择题",
        "难度": "中等",
        "题目内容": "在 UML 中，用于描述系统中类的静态结构和类之间关系的图是？",
        "选项 A": "序列图",
        "选项 B": "用例图",
        "选项 C": "类图",
        "选项 D": "活动图",
        "正确答案": "C",
        "知识点": "UML 类图",
        "答案解析": "类图（Class Diagram）用于描述系统中类的静态结构和类之间的关系。",
        "题目来源": "2024 年软考真题"
      }
    },
    {
      "id": "recvf4EdyAIoGs",
      "fields": {
        "题目 ID": "rk_002",
        "题库分类": "软考架构师",
        "题型": "选择题",
        "难度": "困难",
        "题目内容": "在设计模式中，单例模式的主要目的是？",
        "选项 A": "创建一个对象的多个实例",
        "选项 B": "确保一个类只有一个实例，并提供全局访问点",
        "选项 C": "隐藏对象的创建细节",
        "选项 D": "实现对象之间的松耦合",
        "正确答案": "B",
        "知识点": "设计模式 - 单例模式",
        "答案解析": "单例模式的核心目的是确保一个类只有一个实例，并提供全局访问点。",
        "题目来源": "2023 年软考真题"
      }
    }
  ];
}

module.exports = {
  listRecords,
  createRecord,
  updateRecord,
  deleteRecord,
  getQuestionById,
  filterQuestions,
  getSampleQuestions // 导出用于测试
};

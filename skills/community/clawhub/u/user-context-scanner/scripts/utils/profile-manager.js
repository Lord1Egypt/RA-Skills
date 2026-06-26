/**
 * 用户画像管理器
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync, appendFileSync } from 'node:fs';
import { join } from 'node:path';
import { format, differenceInDays, parseISO } from 'date-fns';

const WORKSPACE = process.env.HOME ? join(process.env.HOME, '.openclaw/workspace') : '/tmp/.openclaw/workspace';
const PROFILE_PATH = join(WORKSPACE, '.soul', 'user-profile.json');
const EVIDENCE_PATH = join(WORKSPACE, '.soul', 'user-evidence.jsonl');

// 确保目录存在
function ensureDir(dir) {
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }
}

// 加载用户画像
export function loadProfile() {
  if (!existsSync(PROFILE_PATH)) {
    return createInitialProfile();
  }
  
  try {
    const profile = JSON.parse(readFileSync(PROFILE_PATH, 'utf-8'));
    return profile;
  } catch (error) {
    console.error('加载用户画像失败:', error.message);
    return createInitialProfile();
  }
}

// 创建初始画像
function createInitialProfile() {
  const initialProfile = {
    profile_id: 'user_001',
    version: '1.0',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    profile: {
      demographics: {},
      profession: {},
      values: {},
      habits: {},
      preferences: {}
    },
    metadata: {
      confidence_summary: {},
      contradictions: [],
      quiz_pending: [],
      update_history: []
    }
  };
  
  ensureDir(join(WORKSPACE, '.soul'));
  saveProfile(initialProfile);
  return initialProfile;
}

// 保存用户画像
export function saveProfile(profile) {
  profile.updated_at = new Date().toISOString();
  
  try {
    writeFileSync(PROFILE_PATH, JSON.stringify(profile, null, 2), 'utf-8');
    return true;
  } catch (error) {
    console.error('保存用户画像失败:', error.message);
    return false;
  }
}

// 添加证据
export function addEvidence(evidence) {
  ensureDir(join(WORKSPACE, '.soul'));
  
  const evidenceRecord = {
    ...evidence,
    id: `ev_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
    recorded_at: new Date().toISOString()
  };
  
  try {
    const line = JSON.stringify(evidenceRecord);
    appendFileSync(EVIDENCE_PATH, line + '\n', 'utf-8');
    return evidenceRecord.id;
  } catch (error) {
    console.error('保存证据失败:', error.message);
    return null;
  }
}

// 加载所有证据
export function loadAllEvidence(limit = 1000) {
  if (!existsSync(EVIDENCE_PATH)) {
    return [];
  }
  
  try {
    const content = readFileSync(EVIDENCE_PATH, 'utf-8');
    const lines = content.split('\n').filter(line => line.trim());
    
    const evidence = lines.slice(-limit).map(line => {
      try {
        return JSON.parse(line);
      } catch {
        return null;
      }
    }).filter(Boolean);
    
    return evidence;
  } catch (error) {
    console.error('加载证据失败:', error.message);
    return [];
  }
}

// 更新画像字段
export function updateProfileField(category, field, value, evidence, confidence = 0.7) {
  const profile = loadProfile();
  
  // 确保category存在
  if (!profile.profile[category]) {
    profile.profile[category] = {};
  }
  
  // 获取现有字段数据
  const existingField = profile.profile[category][field];
  
  if (existingField) {
    // 更新现有字段
    const newConfidence = calculateNewConfidence(existingField.confidence, confidence, evidence);
    
    profile.profile[category][field] = {
      ...existingField,
      value: value,
      confidence: newConfidence,
      evidence: [...(existingField.evidence || []), evidence],
      last_verified: new Date().toISOString()
    };
  } else {
    // 创建新字段
    profile.profile[category][field] = {
      value: value,
      confidence: confidence,
      evidence: [evidence],
      first_observed: new Date().toISOString(),
      last_verified: new Date().toISOString(),
      contradictions: []
    };
  }
  
  // 记录更新历史
  const historyEntry = {
    timestamp: new Date().toISOString(),
    category,
    field,
    old_value: existingField?.value || null,
    new_value: value,
    confidence_change: existingField ? confidence - existingField.confidence : confidence,
    evidence_id: evidence.id || evidence.source
  };
  
  profile.metadata.update_history = [
    historyEntry,
    ...(profile.metadata.update_history || []).slice(0, 49) // 保留最近50条
  ];
  
  saveProfile(profile);
  return profile.profile[category][field];
}

// 计算新的置信度
function calculateNewConfidence(oldConfidence, newEvidenceConfidence, evidence) {
  // 简单加权平均
  const weightOld = 0.6;
  const weightNew = 0.4;
  
  return oldConfidence * weightOld + newEvidenceConfidence * weightNew;
}

// 分析画像置信度
export function analyzeConfidence(profile) {
  const categories = ['demographics', 'profession', 'values', 'habits', 'preferences'];
  const summary = {};
  
  for (const category of categories) {
    const fields = profile.profile[category];
    if (!fields || Object.keys(fields).length === 0) {
      summary[category] = { confidence: 0, fields: 0, completeness: 0 };
      continue;
    }
    
    let totalConfidence = 0;
    let fieldCount = 0;
    
    for (const [field, data] of Object.entries(fields)) {
      if (data && typeof data.confidence === 'number') {
        totalConfidence += data.confidence;
        fieldCount++;
      }
    }
    
    summary[category] = {
      confidence: fieldCount > 0 ? totalConfidence / fieldCount : 0,
      fields: fieldCount,
      completeness: fieldCount / 10 // 假设每类最多10个字段
    };
  }
  
  // 总体置信度
  const validCategories = Object.values(summary).filter(s => s.fields > 0);
  const overallConfidence = validCategories.length > 0 
    ? validCategories.reduce((sum, s) => sum + s.confidence, 0) / validCategories.length
    : 0;
  
  // 总体完整性
  const totalFields = Object.values(summary).reduce((sum, s) => sum + s.fields, 0);
  const overallCompleteness = totalFields / 50; // 假设总共50个字段
  
  return { 
    summary, 
    overall: {
      confidence: overallConfidence,
      completeness: overallCompleteness,
      total_fields: totalFields,
      categories_with_data: validCategories.length
    }
  };
}

// 检测矛盾
export function detectContradictions(profile, newEvidence = null) {
  const contradictions = [];
  const evidence = loadAllEvidence();
  
  // 按字段分组证据
  const evidenceByField = {};
  
  for (const ev of evidence) {
    const key = `${ev.category}.${ev.field}`;
    if (!evidenceByField[key]) {
      evidenceByField[key] = [];
    }
    evidenceByField[key].push(ev);
  }
  
  // 添加新证据
  if (newEvidence) {
    const key = `${newEvidence.category}.${newEvidence.field}`;
    if (!evidenceByField[key]) {
      evidenceByField[key] = [];
    }
    evidenceByField[key].push(newEvidence);
  }
  
  // 检查每个字段的矛盾
  for (const [field, evidences] of Object.entries(evidenceByField)) {
    if (evidences.length < 2) continue;
    
    // 分组不同的值
    const valueGroups = {};
    for (const ev of evidences) {
      const value = String(ev.value).toLowerCase();
      if (!valueGroups[value]) {
        valueGroups[value] = [];
      }
      valueGroups[value].push(ev);
    }
    
    // 如果有多个不同的值，检测到矛盾
    const uniqueValues = Object.keys(valueGroups);
    if (uniqueValues.length > 1) {
      const [category, fieldName] = field.split('.');
      
      contradictions.push({
        field: field,
        category,
        field_name: fieldName,
        values: uniqueValues,
        evidence_counts: uniqueValues.map(value => valueGroups[value].length),
        total_evidence: evidences.length,
        confidence_by_value: uniqueValues.map(value => {
          const evs = valueGroups[value];
          const avgConfidence = evs.reduce((sum, ev) => sum + (ev.confidence || 0.5), 0) / evs.length;
          return { value, confidence: avgConfidence };
        }),
        first_detected: new Date().toISOString(),
        last_updated: new Date().toISOString(),
        severity: calculateContradictionSeverity(evidences.length, uniqueValues.length)
      });
    }
  }
  
  // 更新画像中的矛盾记录
  if (contradictions.length > 0) {
    profile.metadata.contradictions = [
      ...contradictions,
      ...(profile.metadata.contradictions || []).slice(0, 49) // 保留最近50条
    ];
    saveProfile(profile);
  }
  
  return contradictions;
}

// 计算矛盾严重性
function calculateContradictionSeverity(totalEvidence, uniqueValues) {
  const diversityRatio = uniqueValues / totalEvidence;
  
  if (diversityRatio > 0.5) {
    return 'high'; // 证据分散，严重矛盾
  } else if (diversityRatio > 0.3) {
    return 'medium'; // 中等矛盾
  } else {
    return 'low'; // 轻微矛盾
  }
}

// 生成Quiz
export function generateQuizzes(profile, contradictions, maxQuizzes = 3) {
  const quizzes = [];
  
  // 基于低置信度字段生成Quiz
  const categories = ['demographics', 'profession', 'values', 'habits', 'preferences'];
  
  for (const category of categories) {
    const fields = profile.profile[category];
    if (!fields) continue;
    
    for (const [field, data] of Object.entries(fields)) {
      if (data && data.confidence < 0.5) {
        quizzes.push({
          type: 'confidence_verification',
          id: `quiz_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
          field: `${category}.${field}`,
          current_value: data.value,
          current_confidence: data.confidence,
          question: `关于${field}，我记录的是"${data.value}"，这个信息准确吗？`,
          options: [
            { text: '完全准确', value: 'accurate', confidence_boost: 0.3 },
            { text: '基本准确但需要调整', value: 'mostly_accurate', confidence_boost: 0.1 },
            { text: '不太准确', value: 'inaccurate', confidence_boost: -0.2 },
            { text: '完全不准确', value: 'completely_wrong', confidence_boost: -0.4 }
          ],
          priority: data.confidence < 0.3 ? 'high' : 'medium',
          generated_at: new Date().toISOString()
        });
      }
    }
  }
  
  // 基于矛盾生成Quiz
  for (const contradiction of contradictions.slice(0, 2)) {
    quizzes.push({
      type: 'contradiction_resolution',
      id: `quiz_contra_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
      field: contradiction.field,
      conflicting_values: contradiction.values,
      question: `我发现关于${contradiction.field_name}有不同的记录，能帮我确认一下哪个是正确的吗？`,
      options: contradiction.values.map((value, index) => ({
        text: value,
        value: `option_${index}`,
        confidence_boost: 0.2
      })),
      priority: contradiction.severity === 'high' ? 'high' : 'medium',
      generated_at: new Date().toISOString()
    });
  }
  
  // 基于缺失字段生成Quiz（如果画像不完整）
  if (Object.keys(profile.profile.demographics).length === 0) {
    quizzes.push({
      type: 'profile_completion',
      id: `quiz_profile_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
      field: 'demographics.basic',
      question: '为了更好地了解您，可以告诉我一些基本信息吗？比如年龄或家庭角色？',
      options: [
        { text: '愿意分享', value: 'willing', confidence_boost: 0 },
        { text: '稍后再说', value: 'later', confidence_boost: 0 },
        { text: '跳过这个问题', value: 'skip', confidence_boost: 0 }
      ],
      priority: 'low',
      generated_at: new Date().toISOString()
    });
  }
  
  return quizzes.slice(0, maxQuizzes);
}

// 处理Quiz回答
export function processQuizAnswer(quizId, answer, selectedOption) {
  const profile = loadProfile();
  
  // 查找对应的Quiz
  const pendingQuizzes = profile.metadata.quiz_pending || [];
  const quizIndex = pendingQuizzes.findIndex(q => q.id === quizId);
  
  if (quizIndex === -1) {
    console.error(`未找到Quiz: ${quizId}`);
    return false;
  }
  
  const quiz = pendingQuizzes[quizIndex];
  
  // 根据回答类型处理
  if (quiz.type === 'confidence_verification') {
    const [category, field] = quiz.field.split('.');
    const fieldData = profile.profile[category]?.[field];
    
    if (fieldData) {
      // 根据回答调整置信度
      const option = quiz.options.find(opt => opt.value === selectedOption);
      if (option && option.confidence_boost) {
        fieldData.confidence = Math.max(0, Math.min(1, fieldData.confidence + option.confidence_boost));
        fieldData.last_verified = new Date().toISOString();
        
        // 如果回答是"不准确"，可能需要后续处理
        if (selectedOption === 'inaccurate' || selectedOption === 'completely_wrong') {
          fieldData.needs_update = true;
        }
      }
    }
  } else if (quiz.type === 'contradiction_resolution') {
    const [category, field] = quiz.field.split('.');
    
    // 用户选择了某个值作为正确答案
    const selectedValue = quiz.conflicting_values[parseInt(selectedOption.replace('option_', ''))];
    
    if (selectedValue) {
      // 更新字段值为用户选择的值
      if (!profile.profile[category]) {
        profile.profile[category] = {};
      }
      
      profile.profile[category][field] = {
        value: selectedValue,
        confidence: 0.9, // 用户确认，高置信度
        evidence: [{
          source: 'user_confirmation',
          timestamp: new Date().toISOString(),
          excerpt: `用户确认"${selectedValue}"为正确值`
        }],
        last_verified: new Date().toISOString()
      };
      
      // 从矛盾列表中移除
      profile.metadata.contradictions = (profile.metadata.contradictions || [])
        .filter(c => c.field !== quiz.field);
    }
  }
  
  // 记录回答
  quiz.answered_at = new Date().toISOString();
  quiz.answer = answer;
  quiz.selected_option = selectedOption;
  quiz.status = 'completed';
  
  // 移动到历史记录
  profile.metadata.quiz_history = [
    quiz,
    ...(profile.metadata.quiz_history || []).slice(0, 49)
  ];
  
  // 从待处理列表中移除
  pendingQuizzes.splice(quizIndex, 1);
  profile.metadata.quiz_pending = pendingQuizzes;
  
  saveProfile(profile);
  return true;
}

// 获取画像统计
export function getProfileStats() {
  const profile = loadProfile();
  const analysis = analyzeConfidence(profile);
  
  const evidence = loadAllEvidence();
  const contradictions = profile.metadata.contradictions || [];
  
  return {
    profile: {
      created: profile.created_at,
      last_updated: profile.updated_at,
      version: profile.version
    },
    confidence: analysis.overall,
    by_category: analysis.summary,
    evidence: {
      total: evidence.length,
      by_category: groupEvidenceByCategory(evidence),
      recent_30d: evidence.filter(e => {
        const days = differenceInDays(new Date(), parseISO(e.timestamp || e.recorded_at));
        return days <= 30;
      }).length
    },
    contradictions: {
      total: contradictions.length,
      by_severity: groupContradictionsBySeverity(contradictions),
      unresolved: contradictions.filter(c => !c.resolved).length
    },
    quizzes: {
      pending: (profile.metadata.quiz_pending || []).length,
      total_history: (profile.metadata.quiz_history || []).length
    }
  };
}

// 按类别分组证据
function groupEvidenceByCategory(evidence) {
  const groups = {};
  
  for (const ev of evidence) {
    if (!groups[ev.category]) {
      groups[ev.category] = 0;
    }
    groups[ev.category]++;
  }
  
  return groups;
}

// 按严重性分组矛盾
function groupContradictionsBySeverity(contradictions) {
  const groups = { high: 0, medium: 0, low: 0 };
  
  for (const c of contradictions) {
    groups[c.severity] = (groups[c.severity] || 0) + 1;
  }
  
  return groups;
}

export default {
  loadProfile,
  saveProfile,
  addEvidence,
  loadAllEvidence,
  updateProfileField,
  analyzeConfidence,
  detectContradictions,
  generateQuizzes,
  processQuizAnswer,
  getProfileStats
};
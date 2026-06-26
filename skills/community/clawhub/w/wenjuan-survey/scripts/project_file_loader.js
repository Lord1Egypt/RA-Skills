const fs = require('fs').promises;
const { normalizeQuestionsForImport } = require('./workflow_create_and_publish.js');

function inferPtypeForNormalize(projectData) {
  const v = projectData.ptype_enname || projectData.ptype || projectData.fileType;
  if (typeof v === 'string' && /^(survey|assess|form|vote)$/i.test(v)) {
    return v.toLowerCase();
  }
  return 'survey';
}

/** 导入前规范化题目（含评分题补全 custom_attr，避免 textproject 落库缺字段） */
function normalizeProjectQuestionsIfAny(projectData) {
  const raw =
    Array.isArray(projectData.question_list) && projectData.question_list.length
      ? projectData.question_list
      : Array.isArray(projectData.questions) && projectData.questions.length
        ? projectData.questions
        : null;
  if (!raw) return;
  const normalized = normalizeQuestionsForImport(raw, inferPtypeForNormalize(projectData));
  projectData.question_list = normalized;
  if (Array.isArray(projectData.questions)) {
    projectData.questions = normalized;
  }
}

async function loadProjectFromFile(filePath) {
  const content = await fs.readFile(filePath, 'utf-8');
  const projectData = JSON.parse(content);
  normalizeProjectQuestionsIfAny(projectData);
  return projectData;
}

module.exports = {
  loadProjectFromFile,
  normalizeProjectQuestionsIfAny,
  inferPtypeForNormalize,
};

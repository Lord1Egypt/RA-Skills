const assert = require("assert");
const { normalizeQuestionsForImport } = require("../scripts/workflow_create_and_publish.js");
const {
  generateSmartQuestion,
  inferTypeFromTitle,
  normalizeQuestionTypeAlias,
  createEvaluationQuestion,
  createScaleQuestion,
  createScoreQuestion,
  createNpsQuestion,
} = require("../scripts/create_question.js");

function emptyProject() {
  return { title: "测试问卷", questionpage_list: [{ question_list: [] }] };
}

const [question] = normalizeQuestionsForImport([
  {
    title: "请评价本次服务",
    // 模拟上游误带矩阵题型码，但评价子类型信息仍在 custom_attr 中。
    question_type: 4,
    en_name: "QUESTION_TYPE_MATRIX_SINGLE",
    custom_attr: { disp_type: "evaluation" },
    option_list: [
      { title: "分数" },
      { title: "标签", custom_attr: { label_data: { "1": { score_desc: "差", label_list: [] } } } },
    ],
  },
]);

assert.equal(question.en_name, "QUESTION_TYPE_SCORE");
assert.equal(question.question_type, 50);
assert.equal(question.custom_attr.disp_type, "evaluation");
assert.equal(question.custom_attr.score_display, "star");
assert.equal(question.custom_attr.open_eval, "on");
assert.equal(question.custom_attr.min_answer_num, 1);
assert.equal(question.custom_attr.max_answer_num, 5);
assert.equal(question.custom_attr.show_seq, "off");
assert.equal(question.custom_attr.base_on, "service");
assert.equal(question.custom_attr.magnitude_scale, undefined);
assert.equal(question.custom_attr.score_total, undefined);
assert.deepEqual(question.option_list.map((option) => option.title), ["分数", "标签"]);
assert.equal(question.option_list[1].custom_attr.label_data["1"].score_desc, "非常不满意");
assert.deepEqual(
  question.option_list[1].custom_attr.label_data["1"].label_list,
  ["态度冷淡", "推销多", "技术差"]
);
assert.equal(question.option_list[1].custom_attr.label_data["5"].score_desc, "非常满意");
assert.deepEqual(
  question.option_list[1].custom_attr.label_data["5"].label_list,
  ["热情好客", "敬业精神", "技能专业"]
);
assert.equal(question.matrixrow_list, undefined);

const [completeEval] = normalizeQuestionsForImport([
  {
    title: "请评价本次服务",
    question_type: 50,
    en_name: "QUESTION_TYPE_SCORE",
    custom_attr: { disp_type: "evaluation" },
    option_list: [
      { title: "分数" },
      {
        title: "标签",
        custom_attr: {
          label_data: {
            "1": { score_desc: "非常不满意", label_list: ["态度冷淡"] },
            "2": { score_desc: "比较不满意", label_list: ["速度慢"] },
            "3": { score_desc: "一般", label_list: ["无互动"] },
            "4": { score_desc: "比较满意", label_list: ["文明礼貌"] },
            "5": { score_desc: "非常满意", label_list: ["热情好客"] },
          },
        },
      },
    ],
  },
]);
assert.deepEqual(
  completeEval.option_list[1].custom_attr.label_data["1"].label_list,
  ["态度冷淡"]
);

assert.throws(
  () =>
    normalizeQuestionsForImport([
      {
        title: "请对以下方面进行满意度评价",
        question_type: 4,
        en_name: "QUESTION_TYPE_MATRIX_SINGLE",
        custom_attr: { show_seq: "on" },
        matrixrow_list: [
          { title: "服务态度", is_open: false, custom_attr: {} },
          { title: "产品质量", is_open: false, custom_attr: {} },
        ],
        option_list: [
          { title: "非常不满意" },
          { title: "不满意" },
          { title: "一般" },
          { title: "满意" },
          { title: "非常满意" },
        ],
      },
    ]),
  /不支持矩阵题型/
);

assert.equal(inferTypeFromTitle("请评价本次服务"), "evaluation");
assert.equal(inferTypeFromTitle("评价题"), "evaluation");
assert.equal(inferTypeFromTitle("请对以下方面进行满意度评价"), null);
assert.equal(normalizeQuestionTypeAlias("评价题"), "evaluation");
assert.equal(normalizeQuestionTypeAlias("量表题"), "scale");
assert.equal(normalizeQuestionTypeAlias("打分题"), "score");
assert.equal(normalizeQuestionTypeAlias("NPS"), "nps");
assert.equal(normalizeQuestionTypeAlias("nps题"), "nps");
assert.equal(normalizeQuestionTypeAlias("净推荐值"), "nps");
assert.equal(normalizeQuestionTypeAlias("几分"), "score");
assert.equal(normalizeQuestionTypeAlias("星级"), "score");
assert.equal(inferTypeFromTitle("请给本项打分"), "score");
assert.equal(inferTypeFromTitle("请完成满意度量表"), "scale");
assert.equal(inferTypeFromTitle("请对本次服务的满意度打分"), "score");
assert.equal(inferTypeFromTitle("请给这项服务评分"), "score");
assert.equal(inferTypeFromTitle("这次体验你给几分？"), "score");
assert.equal(inferTypeFromTitle("请按星级打分"), "score");
assert.equal(inferTypeFromTitle("NPS题"), "nps");
assert.equal(inferTypeFromTitle("您向朋友或同事推荐我们的可能性有多大？"), "nps");

const [created, desc] = generateSmartQuestion(
  "survey",
  emptyProject(),
  "请评价本次服务",
  "auto",
  "pid",
  "pageid"
);
assert.equal(desc, "评价题");
assert.equal(created.question_type, 50);
assert.equal(created.en_name, "QUESTION_TYPE_SCORE");
assert.equal(created.custom_attr.disp_type, "evaluation");
assert.equal(created.custom_attr.score_display, "star");
assert.equal(created.custom_attr.open_eval, "on");
assert.equal(created.custom_attr.show_seq, "off");
assert.equal(created.custom_attr.base_on, "service");
assert.deepEqual(created.option_list.map((option) => option.title), ["分数", "标签"]);
assert.equal(
  created.option_list[1].custom_attr.label_data["1"].score_desc,
  "非常不满意"
);
assert.deepEqual(
  created.option_list[1].custom_attr.label_data["1"].label_list,
  ["态度冷淡", "推销多", "技术差"]
);
assert.equal(
  created.option_list[1].custom_attr.label_data["5"].score_desc,
  "非常满意"
);

const staleEval = createEvaluationQuestion("请评价本次服务", ["很差", "差", "一般", "好", "很好"]);
assert.equal(staleEval.option_list[1].custom_attr.label_data["1"].score_desc, "非常不满意");
assert.deepEqual(
  staleEval.option_list[1].custom_attr.label_data["1"].label_list,
  ["态度冷淡", "推销多", "技术差"]
);
assert.equal(staleEval.custom_attr.magnitude_scale, undefined);
assert.equal(staleEval.custom_attr.score_total, undefined);

const scale = createScaleQuestion("满意度量表", "pid", "pageid");
assert.equal(scale.question_type, 50);
assert.equal(scale.en_name, "QUESTION_TYPE_SCORE");
assert.equal(scale.custom_attr.scale_tag, 2);
assert.equal(scale.custom_attr.score_display, "circle");
assert.equal(scale.custom_attr.min_answer_num, 1);
assert.equal(scale.custom_attr.max_answer_num, 5);
assert.equal(scale.custom_attr.answer_score, "off");
assert.equal(scale.custom_attr.desc_left, "非常不满意");
assert.equal(scale.custom_attr.desc_right, "非常满意");
assert.equal(scale.custom_attr.magnitude_scale, 1);
assert.equal(scale.custom_attr.show_seq, "off");
assert.equal(scale.custom_attr.disp_type, "scale");
assert.equal(scale.option_list.length, 1);

const score = createScoreQuestion("请给本项打分", "pid", "pageid");
assert.equal(score.question_type, 50);
assert.equal(score.en_name, "QUESTION_TYPE_SCORE");
assert.equal(score.custom_attr.min_answer_num, 1);
assert.equal(score.custom_attr.show_seq, "off");
assert.equal(score.custom_attr.max_answer_num, 5);
assert.equal(score.custom_attr.magnitude_scale, 1);
assert.equal(score.custom_attr.disp_type, undefined);

const nps = createNpsQuestion("您向朋友或同事推荐我们的可能性有多大？", "pid", "pageid");
assert.equal(nps.question_type, 50);
assert.equal(nps.en_name, "QUESTION_TYPE_SCORE");
assert.equal(nps.custom_attr.disp_type, "nps_score");
assert.equal(nps.custom_attr.min_answer_num, 0);
assert.equal(nps.custom_attr.max_answer_num, 10);
assert.equal(nps.custom_attr.show_seq, "off");
assert.equal(nps.option_list.length, 1);
assert.equal(nps.option_list[0].title, "选项1");

const [assessSingle] = normalizeQuestionsForImport(
  [
    {
      title: "Python的创建者是？",
      en_name: "QUESTION_TYPE_SINGLE",
      custom_attr: { calculation: "auto_score", answer_score: "on", total_score: 10 },
      option_list: [
        { title: "Guido van Rossum", custom_attr: { is_correct: "1", score: 10 } },
        { title: "James Gosling", custom_attr: { score: 0 } },
      ],
    },
  ],
  "assess"
);
assert.equal(assessSingle.custom_attr.calculation, "only_one");

const [assessMulti] = normalizeQuestionsForImport(
  [
    {
      title: "以下哪些是Python的数据类型？",
      en_name: "QUESTION_TYPE_MULTIPLE",
      custom_attr: { calculation: "auto_score", answer_score: "on", total_score: 10 },
      option_list: [
        { title: "list", custom_attr: { is_correct: "1", score: 5 } },
        { title: "array", custom_attr: { is_correct: "0" } },
      ],
    },
  ],
  "assess"
);
assert.equal(assessMulti.custom_attr.calculation, "select");

assert.throws(
  () =>
    normalizeQuestionsForImport(
      [
        {
          title: "只有解析、没有正确答案的题目",
          en_name: "QUESTION_TYPE_SINGLE",
          custom_attr: {
            calculation: "only_one",
            answer_score: "on",
            total_score: 10,
            answer_analysis: "这段文字只是解析，不能用于判分",
          },
          option_list: [
            { title: "选项A", custom_attr: { score: 0 } },
            { title: "选项B", custom_attr: { score: 0 } },
          ],
        },
      ],
      "assess"
    ),
  /测评选择题缺少正确答案.*answer_analysis 仅是答案解析/
);

const [assessBlank] = normalizeQuestionsForImport(
  [
    {
      title: "Python的输出函数是______",
      en_name: "QUESTION_TYPE_BLANK",
      custom_attr: { blank_type: "single", calculation: "auto_score", answer_score: "on" },
      option_list: [
        {
          title: "填空1",
          custom_attr: { correct_answer: "print", score: 5 },
        },
      ],
    },
  ],
  "assess"
);
assert.equal(assessBlank.custom_attr.calculation, undefined);
assert.equal(assessBlank.option_list[0].custom_attr.correct_answer, "print");
assert.equal(assessBlank.option_list[0].custom_attr.is_correct, undefined);

assert.throws(
  () =>
    normalizeQuestionsForImport(
      [
        {
          title: "只有解析、没有标准答案的填空题",
          en_name: "QUESTION_TYPE_BLANK",
          custom_attr: {
            blank_type: "single",
            answer_score: "on",
            total_score: 5,
            answer_analysis: "print 是输出函数",
          },
          option_list: [{ title: "填空1", custom_attr: { score: 5 } }],
        },
      ],
      "assess"
    ),
  /测评填空题缺少正确答案.*correct_answer.*不使用 is_correct/
);

console.log("evaluation question normalization regression test passed");

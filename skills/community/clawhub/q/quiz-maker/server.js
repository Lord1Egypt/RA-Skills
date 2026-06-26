const express = require('express');
const path = require('path');
const fs = require('fs');
const { initDb } = require('./db');
const { parseDocument } = require('./parser');
const { generateQuestions } = require('./question_generator');
const upload = require('./upload-handler');
const QRCode = require('qrcode');

const app = express();
const PORT = 3400;

initDb();
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// 1. 创建答题（返回链接）
app.post('/api/quiz/create', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) return res.status(400).json({ error: '请上传文件' });
    const filePath = req.file.path;
    const fileExt = path.extname(req.file.originalname).toLowerCase();
    const content = await parseDocument(filePath, fileExt);
    if (!content || content.trim().length < 50) {
      try { fs.unlinkSync(filePath); } catch(e) {}
      return res.status(400).json({ error: '文档内容过少' });
    }
    const questions = await generateQuestions(content);
    try { fs.unlinkSync(filePath); } catch(e) {}

    const db = require('./db').getDb();
    const quizId = require('uuid').v4();
    const title = req.body.title || `Quiz ${new Date().toLocaleString('zh-CN')}`;
    const description = req.body.description || '';
    db.prepare(`INSERT INTO quizzes (id, title, description, questions, created_at) VALUES (?, ?, ?, ?, datetime('now'))`).run(quizId, title, description, JSON.stringify(questions));
    db.prepare(`INSERT INTO quiz_stats (quiz_id) VALUES (?)`).run(quizId);

    res.json({ success: true, quizId, title, questionCount: questions.length });
  } catch (err) {
    console.error('Create error:', err);
    res.status(500).json({ error: err.message });
  }
});

// 2. 获取题目（不含答案）
app.get('/api/quiz/:id/questions', (req, res) => {
  const db = require('./db').getDb();
  const quiz = db.prepare(`SELECT questions FROM quizzes WHERE id = ?`).get(req.params.id);
  if (!quiz) return res.status(404).json({ error: 'Quiz不存在' });
  const questions = JSON.parse(quiz.questions);
  res.json({ questions: questions.map(q => ({ question: q.question, options: q.options })) });
});

// 3. 获取答题信息
app.get('/api/quiz/:id', (req, res) => {
  const db = require('./db').getDb();
  const quiz = db.prepare(`SELECT * FROM quizzes WHERE id = ?`).get(req.params.id);
  if (!quiz) return res.status(404).json({ error: 'Quiz不存在' });
  res.json({ id: quiz.id, title: quiz.title, description: quiz.description });
});

// 4. 提交答案
app.post('/api/quiz/:id/submit', (req, res) => {
  const { name, className, answers } = req.body;
  const quizId = req.params.id;
  const db = require('./db').getDb();
  const quiz = db.prepare(`SELECT questions FROM quizzes WHERE id = ?`).get(quizId);
  if (!quiz) return res.status(404).json({ error: 'Quiz不存在' });
  const questions = JSON.parse(quiz.questions);
  let correct = 0;
  const results = questions.map((q, i) => {
    const isCorrect = (answers[i] || '').trim() === (q.correctAnswer || '').trim();
    if (isCorrect) correct++;
    return { questionIndex: i, isCorrect, userAnswer: answers[i] || '', correctAnswer: q.correctAnswer };
  });
  const score = Math.round((correct / questions.length) * 100);
  const submissionId = require('uuid').v4();
  db.prepare(`INSERT INTO submissions (id, quiz_id, name, class_name, score, answers, submitted_at) VALUES (?, ?, ?, ?, ?, ?, datetime('now'))`).run(submissionId, quizId, name, className || '', score, JSON.stringify(answers));
  const stats = db.prepare(`SELECT * FROM quiz_stats WHERE quiz_id = ?`).get(quizId);
  if (stats) {
    db.prepare(`UPDATE quiz_stats SET total_participants=total_participants+1, total_score=total_score+?, min_score=CASE WHEN ?<min_score OR min_score IS NULL THEN ? ELSE min_score END, max_score=CASE WHEN ?>max_score OR max_score IS NULL THEN ? ELSE max_score END WHERE quiz_id=?`).run(score, score, score, score, score, quizId);
  }
  res.json({ submissionId, score, correct, total: questions.length, results, name, submittedAt: new Date().toLocaleString('zh-CN') });
});

// 5. 统计页
app.get('/api/quiz/:id/stats', (req, res) => {
  const db = require('./db').getDb();
  const quiz = db.prepare(`SELECT * FROM quizzes WHERE id = ?`).get(req.params.id);
  if (!quiz) return res.status(404).json({ error: 'Quiz不存在' });
  const submissions = db.prepare(`SELECT id, name, class_name, score, answers, submitted_at FROM submissions WHERE quiz_id = ? ORDER BY score DESC, submitted_at ASC`).all(req.params.id);
  const stats = db.prepare(`SELECT * FROM quiz_stats WHERE quiz_id = ?`).get(req.params.id);
  const questions = JSON.parse(quiz.questions);
  const avgScore = stats && stats.total_participants > 0 ? Math.round(stats.total_score / stats.total_participants) : 0;
  const questionStats = questions.map((q, i) => ({
    index: i, question: q.question.substring(0, 60) + (q.question.length > 60 ? '...' : ''),
    accuracy: submissions.length > 0 ? Math.round(submissions.filter(s => JSON.parse(s.answers || '[]')[i] === q.correctAnswer).length / submissions.length * 100) : 0,
    correctAnswer: q.correctAnswer, options: q.options
  }));
  res.json({
    quizId: quiz.id, title: quiz.title, description: quiz.description,
    totalSubmissions: submissions.length, avgScore,
    maxScore: stats?.max_score || 0, minScore: stats?.min_score || 0,
    submissions: submissions.map((s, idx) => ({ rank: idx + 1, name: s.name, className: s.class_name, score: s.score, submittedAt: s.submitted_at })),
    questionStats, createdAt: quiz.created_at
  });
});

// 6. 列表
app.get('/api/quizzes', (req, res) => {
  const db = require('./db').getDb();
  res.json(db.prepare(`SELECT q.id, q.title, q.description, q.created_at, COALESCE(s.total_participants,0) as total_participants, COALESCE(s.total_score*1.0/NULLIF(s.total_participants,0),0) as avg_score FROM quizzes q LEFT JOIN quiz_stats s ON q.id=s.quiz_id ORDER BY q.created_at DESC`).all());
});

// 7. 删除
app.delete('/api/quiz/:id', (req, res) => {
  const db = require('./db').getDb();
  db.prepare(`DELETE FROM submissions WHERE quiz_id = ?`).run(req.params.id);
  db.prepare(`DELETE FROM quiz_stats WHERE quiz_id = ?`).run(req.params.id);
  db.prepare(`DELETE FROM quizzes WHERE id = ?`).run(req.params.id);
  res.json({ success: true });
});

// 8. 一键创建+返回二维码图片（用于对话界面直接返回图片）
app.post('/api/quiz/create-with-qr', async (req, res) => {
  try {
    const { content, title, description } = req.body;
    if (!content || content.trim().length < 50) return res.status(400).json({ error: '文档内容过少' });

    const questions = await generateQuestions(content);
    const db = require('./db').getDb();
    const quizId = require('uuid').v4();
    const quizTitle = title || `Quiz ${new Date().toLocaleString('zh-CN')}`;
    db.prepare(`INSERT INTO quizzes (id, title, description, questions, created_at) VALUES (?, ?, ?, ?, datetime('now'))`).run(quizId, quizTitle, description || '', JSON.stringify(questions));
    db.prepare(`INSERT INTO quiz_stats (quiz_id) VALUES (?)`).run(quizId);

    // 生成二维码PNG
    const quizUrl = `https://118.196.5.240:34100/quiz.html?id=${quizId}`;
    const qrBuffer = await QRCode.toBuffer(quizUrl, { width: 400, margin: 2, color: { dark: '#1a73e8', light: '#ffffff' } });

    res.json({
      success: true,
      quizId,
      title: quizTitle,
      questionCount: questions.length,
      quizUrl,
      qrImage: `data:image/png;base64,${qrBuffer.toString('base64')}`
    });
  } catch (err) {
    console.error('Create error:', err);
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`Quiz Maker running at http://localhost:${PORT}`);
});

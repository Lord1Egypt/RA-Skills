/**
 * TriviaBot — Daily Trivia & Knowledge Quiz
 * @author @TheShadowRose
 * @license MIT
 */
const fs = require('fs');

const QUESTIONS = [
  { q: "What is the only metal that is liquid at room temperature?", a: "Mercury", options: ["Gallium","Mercury","Cesium","Bromine"], cat: "Science", fact: "Mercury's symbol Hg comes from 'hydrargyrum' meaning liquid silver." },
  { q: "Which country has the most natural lakes?", a: "Canada", options: ["Finland","Canada","Sweden","Russia"], cat: "Geography", fact: "Canada has over 3 million lakes, covering 9% of its total area." },
  { q: "What year was the first email sent?", a: "1971", options: ["1965","1971","1978","1983"], cat: "Technology", fact: "Ray Tomlinson sent the first email and chose the @ symbol for addresses." },
  { q: "Which planet has the shortest day?", a: "Jupiter", options: ["Saturn","Mars","Jupiter","Neptune"], cat: "Science", fact: "Jupiter's day is only 9 hours and 56 minutes long." },
  { q: "What is the hardest natural substance on Earth?", a: "Diamond", options: ["Titanium","Diamond","Quartz","Sapphire"], cat: "Science", fact: "Diamond scores 10 on the Mohs hardness scale." },
  { q: "Who painted the ceiling of the Sistine Chapel?", a: "Michelangelo", options: ["Leonardo da Vinci","Raphael","Michelangelo","Donatello"], cat: "History", fact: "It took Michelangelo approximately 4 years (1508-1512) to complete." },
  { q: "What is the most spoken language in the world by native speakers?", a: "Mandarin Chinese", options: ["English","Spanish","Mandarin Chinese","Hindi"], cat: "Geography", fact: "About 920 million people speak Mandarin as their first language." },
  { q: "In computing, how many bits are in a byte?", a: "8", options: ["4","6","8","16"], cat: "Technology", fact: "The term 'byte' was coined by Werner Buchholz in 1956." },
  { q: "What is the smallest country in the world?", a: "Vatican City", options: ["Monaco","Vatican City","San Marino","Liechtenstein"], cat: "Geography", fact: "Vatican City covers just 44 hectares (110 acres)." },
  { q: "Which element has the chemical symbol 'Au'?", a: "Gold", options: ["Silver","Gold","Copper","Aluminum"], cat: "Science", fact: "Au comes from the Latin 'aurum' meaning 'shining dawn'." },
];

class TriviaBot {
  constructor(options = {}) {
    this.dataFile = options.dataFile || './trivia-scores.json';
    this.data = this._load();
  }

  getDailyQuestion() {
    const dayIdx = Math.floor(Date.now() / 86400000) % QUESTIONS.length;
    const q = QUESTIONS[dayIdx];
    return { question: q.q, options: q.options, category: q.cat, id: dayIdx };
  }

  answer(questionId, userAnswer) {
    const q = QUESTIONS[questionId % QUESTIONS.length];
    const answerIdx = q.options.indexOf(q.a);
    const correct = userAnswer.toLowerCase() === q.a.toLowerCase() ||
      (answerIdx >= 0 && userAnswer === (answerIdx + 1).toString()) ||
      (answerIdx >= 0 && userAnswer.toUpperCase() === String.fromCharCode(65 + answerIdx));
    
    if (correct) {
      this.data.score = (this.data.score || 0) + 1;
      this.data.streak = (this.data.streak || 0) + 1;
      if (this.data.streak > (this.data.bestStreak || 0)) this.data.bestStreak = this.data.streak;
    } else {
      this.data.streak = 0;
    }
    this.data.total = (this.data.total || 0) + 1;
    this._save();

    return {
      correct,
      answer: q.a,
      fact: q.fact,
      streak: this.data.streak,
      score: `${this.data.score}/${this.data.total}`,
      message: correct
        ? `✅ ${q.a}! ${q.fact} Streak: 🔥 ${this.data.streak}`
        : `❌ The answer was ${q.a}. ${q.fact} Streak reset.`
    };
  }

  stats() { return { ...this.data }; }
  _load() { try { return JSON.parse(fs.readFileSync(this.dataFile, 'utf8')); } catch { return { score: 0, total: 0, streak: 0, bestStreak: 0 }; } }
  _save() { try { fs.writeFileSync(this.dataFile, JSON.stringify(this.data, null, 2)); } catch {} }
}

module.exports = { TriviaBot };

#!/usr/bin/env python3
"""
Skills Monitor — Flask Web 仪表盘面板
提供可视化的监控数据展示

用法:
    python skills_monitor_web.py                     # 默认端口 5050
    python skills_monitor_web.py --port 8080         # 自定义端口
    python skills_monitor_web.py --demo              # 使用 Demo 数据目录
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 确保项目根目录在 path 中
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from flask import Flask, jsonify, render_template_string
except ImportError:
    print("❌ 需要安装 Flask: pip install flask")
    sys.exit(1)

from skills_monitor.core.identity import IdentityManager
from skills_monitor.core.reporter import ReportGenerator
from skills_monitor.core.evaluator import SkillEvaluator
from skills_monitor.core.recommender import SkillRecommender
from skills_monitor.data.store import DataStore
from skills_monitor.adapters.skill_registry import SkillRegistry

# ──────── 配置 ────────
DEFAULT_CONFIG_DIR = os.path.expanduser("~/.skills_monitor")
DEMO_DATA_DIR = str(PROJECT_ROOT / ".skills_monitor_demo")
SKILLS_DIR = str(PROJECT_ROOT / "skills")
REPORTS_DIR = str(PROJECT_ROOT / "reports" / "monitor")

app = Flask(__name__)

# 全局状态（服务启动时初始化）
_state = {
    "store": None,
    "registry": None,
    "agent_id": None,
    "reporter": None,
}


def init_state(data_dir: str):
    """初始化服务状态"""
    mgr = IdentityManager(data_dir)
    if not mgr.is_initialized:
        mgr.initialize()

    _state["store"] = DataStore(data_dir)
    _state["registry"] = SkillRegistry(SKILLS_DIR)
    _state["agent_id"] = mgr.agent_id
    _state["reporter"] = ReportGenerator(
        store=_state["store"],
        registry=_state["registry"],
        agent_id=mgr.agent_id,
        reports_dir=REPORTS_DIR,
    )


# ──────── HTML 模板 ────────
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Skills Monitor Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        :root {
            --bg-primary: #0f172a;
            --bg-card: #1e293b;
            --bg-card-hover: #263348;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --accent-blue: #3b82f6;
            --accent-green: #22c55e;
            --accent-yellow: #eab308;
            --accent-red: #ef4444;
            --accent-purple: #a855f7;
            --border: #334155;
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
        }

        .header {
            background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
            border-bottom: 1px solid var(--border);
            padding: 1rem 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .header h1 {
            font-size: 1.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #60a5fa, #a855f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .header .meta {
            color: var(--text-secondary);
            font-size: 0.85rem;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 1.5rem;
        }

        /* KPI 卡片行 */
        .kpi-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        .kpi-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.25rem;
            box-shadow: var(--shadow);
            transition: transform 0.2s;
        }

        .kpi-card:hover {
            transform: translateY(-2px);
            background: var(--bg-card-hover);
        }

        .kpi-card .label {
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
        }

        .kpi-card .value {
            font-size: 2rem;
            font-weight: 700;
        }

        .kpi-card .sub {
            font-size: 0.8rem;
            color: var(--text-secondary);
            margin-top: 0.25rem;
        }

        .kpi-card .value.green { color: var(--accent-green); }
        .kpi-card .value.blue { color: var(--accent-blue); }
        .kpi-card .value.yellow { color: var(--accent-yellow); }
        .kpi-card .value.purple { color: var(--accent-purple); }

        /* 两列布局 */
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }

        @media (max-width: 900px) {
            .grid-2 { grid-template-columns: 1fr; }
        }

        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: var(--shadow);
        }

        .card h2 {
            font-size: 1.1rem;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }

        /* 评分排行表 */
        table {
            width: 100%;
            border-collapse: collapse;
        }

        th {
            text-align: left;
            color: var(--text-secondary);
            font-size: 0.8rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 0.5rem 0.75rem;
            border-bottom: 1px solid var(--border);
        }

        td {
            padding: 0.6rem 0.75rem;
            border-bottom: 1px solid rgba(51, 65, 85, 0.5);
            font-size: 0.9rem;
        }

        tr:hover td {
            background: rgba(59, 130, 246, 0.05);
        }

        .score-bar {
            display: inline-block;
            height: 6px;
            border-radius: 3px;
            margin-left: 0.5rem;
            vertical-align: middle;
        }

        .grade {
            display: inline-block;
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        .grade-a { background: rgba(34, 197, 94, 0.2); color: var(--accent-green); }
        .grade-b { background: rgba(59, 130, 246, 0.2); color: var(--accent-blue); }
        .grade-c { background: rgba(234, 179, 8, 0.2); color: var(--accent-yellow); }
        .grade-d { background: rgba(239, 68, 68, 0.2); color: var(--accent-red); }

        /* 推荐卡片 */
        .rec-card {
            background: rgba(59, 130, 246, 0.05);
            border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: 8px;
            padding: 0.75rem 1rem;
            margin-bottom: 0.75rem;
            transition: background 0.2s;
        }

        .rec-card:hover {
            background: rgba(59, 130, 246, 0.1);
        }

        .rec-name {
            font-weight: 600;
            color: var(--accent-blue);
        }

        .rec-meta {
            font-size: 0.8rem;
            color: var(--text-secondary);
            margin-top: 0.25rem;
        }

        .rec-reason {
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-top: 0.35rem;
        }

        .badge {
            display: inline-block;
            padding: 0.1rem 0.4rem;
            border-radius: 4px;
            font-size: 0.7rem;
            font-weight: 600;
        }

        .badge-complement { background: rgba(168, 85, 247, 0.2); color: var(--accent-purple); }
        .badge-upgrade { background: rgba(234, 179, 8, 0.2); color: var(--accent-yellow); }
        .badge-collaborative { background: rgba(34, 197, 94, 0.2); color: var(--accent-green); }

        /* 反馈列表 */
        .feedback-item {
            padding: 0.5rem 0;
            border-bottom: 1px solid rgba(51, 65, 85, 0.3);
        }

        .feedback-item:last-child { border-bottom: none; }

        .feedback-stars {
            color: var(--accent-yellow);
            font-size: 0.85rem;
        }

        .feedback-comment {
            font-size: 0.85rem;
            color: var(--text-secondary);
        }

        /* 图表容器 */
        .chart-container {
            position: relative;
            height: 250px;
        }

        /* 全宽卡片 */
        .full-width {
            margin-bottom: 1.5rem;
        }

        /* 加载状态 */
        .loading {
            text-align: center;
            padding: 2rem;
            color: var(--text-secondary);
        }

        .loading::after {
            content: '';
            display: inline-block;
            width: 1.5rem;
            height: 1.5rem;
            border: 2px solid var(--border);
            border-top-color: var(--accent-blue);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin-left: 0.5rem;
            vertical-align: middle;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        /* 刷新按钮 */
        .refresh-btn {
            background: rgba(59, 130, 246, 0.2);
            border: 1px solid rgba(59, 130, 246, 0.3);
            color: var(--accent-blue);
            padding: 0.4rem 1rem;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85rem;
            transition: background 0.2s;
        }

        .refresh-btn:hover {
            background: rgba(59, 130, 246, 0.3);
        }

        /* Footer */
        .footer {
            text-align: center;
            padding: 1.5rem;
            color: var(--text-secondary);
            font-size: 0.8rem;
            border-top: 1px solid var(--border);
            margin-top: 2rem;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Skills Monitor Dashboard</h1>
        <div style="display:flex;align-items:center;gap:1rem;">
            <span class="meta" id="lastUpdate">加载中...</span>
            <button class="refresh-btn" onclick="loadData()">🔄 刷新</button>
        </div>
    </div>

    <div class="container">
        <!-- KPI 卡片 -->
        <div class="kpi-row" id="kpiRow">
            <div class="kpi-card">
                <div class="label">📊 今日执行</div>
                <div class="value blue" id="kpiRuns">-</div>
                <div class="sub" id="kpiRunsSub">加载中...</div>
            </div>
            <div class="kpi-card">
                <div class="label">✅ 成功率</div>
                <div class="value green" id="kpiSuccessRate">-</div>
                <div class="sub" id="kpiSuccessRateSub">-</div>
            </div>
            <div class="kpi-card">
                <div class="label">⚡ 活跃 Skills</div>
                <div class="value purple" id="kpiActiveSkills">-</div>
                <div class="sub" id="kpiActiveSkillsSub">-</div>
            </div>
            <div class="kpi-card">
                <div class="label">⏱ 平均响应</div>
                <div class="value yellow" id="kpiAvgDuration">-</div>
                <div class="sub" id="kpiAvgDurationSub">-</div>
            </div>
        </div>

        <!-- 趋势图（全宽） -->
        <div class="card full-width">
            <h2>📈 7 天运行趋势</h2>
            <div class="chart-container">
                <canvas id="trendChart"></canvas>
            </div>
        </div>

        <!-- 两列布局 -->
        <div class="grid-2">
            <!-- 评分排行 -->
            <div class="card">
                <h2>🏆 综合评分排行</h2>
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Skill</th>
                            <th>评分</th>
                            <th>等级</th>
                            <th>成功率</th>
                        </tr>
                    </thead>
                    <tbody id="scoreTable">
                        <tr><td colspan="5" class="loading">加载中</td></tr>
                    </tbody>
                </table>
            </div>

            <!-- 推荐 -->
            <div class="card">
                <h2>💡 Skill 推荐</h2>
                <div id="recList">
                    <div class="loading">加载中</div>
                </div>
            </div>
        </div>

        <!-- 两列布局：评分雷达 + 最近反馈 -->
        <div class="grid-2">
            <div class="card">
                <h2>📊 评分分布</h2>
                <div class="chart-container">
                    <canvas id="scoreChart"></canvas>
                </div>
            </div>

            <div class="card">
                <h2>💬 最近反馈</h2>
                <div id="feedbackList">
                    <div class="loading">加载中</div>
                </div>
            </div>
        </div>
    </div>

    <div class="footer">
        Skills Monitor v0.1.0 — 本地 Skills 监控评估系统 Demo &nbsp; | &nbsp;
        <a href="/api/dashboard" style="color:var(--accent-blue);text-decoration:none;">API JSON</a> &nbsp; | &nbsp;
        <a href="/api/report" style="color:var(--accent-blue);text-decoration:none;">生成报告</a>
    </div>

    <script>
        let trendChart = null;
        let scoreChart = null;

        function gradeClass(grade) {
            if (grade.includes('A')) return 'grade-a';
            if (grade.includes('B')) return 'grade-b';
            if (grade.includes('C')) return 'grade-c';
            return 'grade-d';
        }

        function gradeShort(grade) {
            return grade.split('(')[0].trim();
        }

        function badgeClass(type) {
            const m = {complement:'badge-complement', upgrade:'badge-upgrade', collaborative:'badge-collaborative'};
            return m[type] || 'badge-complement';
        }

        function badgeLabel(type) {
            const m = {complement:'💡 互补', upgrade:'⬆️ 升级', collaborative:'🤝 协同', popular:'🔥 热门'};
            return m[type] || type;
        }

        function renderKPIs(ov) {
            document.getElementById('kpiRuns').textContent = ov.total_runs;
            document.getElementById('kpiRunsSub').textContent =
                `成功 ${ov.success_runs} / 失败 ${ov.error_runs}`;

            document.getElementById('kpiSuccessRate').textContent = ov.success_rate + '%';
            document.getElementById('kpiSuccessRateSub').textContent =
                `共 ${ov.total_runs} 次执行`;

            document.getElementById('kpiActiveSkills').textContent = ov.active_skills;
            document.getElementById('kpiActiveSkillsSub').textContent =
                `已安装 ${ov.total_installed} / 可运行 ${ov.total_runnable}`;

            const dur = ov.avg_duration_ms;
            document.getElementById('kpiAvgDuration').textContent = dur > 0 ? dur + 'ms' : '-';
            document.getElementById('kpiAvgDurationSub').textContent = dur > 0 ? '成功任务平均' : '暂无数据';
        }

        function renderTrendChart(dailyRuns) {
            const dates = Object.keys(dailyRuns).sort();
            const successData = dates.map(d => dailyRuns[d].success);
            const errorData = dates.map(d => dailyRuns[d].error);

            const ctx = document.getElementById('trendChart').getContext('2d');
            if (trendChart) trendChart.destroy();

            trendChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: dates.map(d => d.slice(5)),
                    datasets: [
                        {
                            label: '成功',
                            data: successData,
                            backgroundColor: 'rgba(34, 197, 94, 0.6)',
                            borderColor: '#22c55e',
                            borderWidth: 1,
                            borderRadius: 4,
                        },
                        {
                            label: '失败',
                            data: errorData,
                            backgroundColor: 'rgba(239, 68, 68, 0.6)',
                            borderColor: '#ef4444',
                            borderWidth: 1,
                            borderRadius: 4,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: { color: '#94a3b8', font: { size: 12 } },
                        },
                    },
                    scales: {
                        x: {
                            stacked: true,
                            ticks: { color: '#94a3b8' },
                            grid: { color: 'rgba(51, 65, 85, 0.3)' },
                        },
                        y: {
                            stacked: true,
                            ticks: { color: '#94a3b8' },
                            grid: { color: 'rgba(51, 65, 85, 0.3)' },
                        },
                    },
                },
            });
        }

        function renderScores(scores) {
            const tbody = document.getElementById('scoreTable');
            if (!scores || scores.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;color:#94a3b8;">暂无数据</td></tr>';
                return;
            }

            const rankEmoji = ['🥇','🥈','🥉'];
            tbody.innerHTML = scores.map((s, i) => {
                const rank = i < 3 ? rankEmoji[i] : (i + 1);
                const gc = gradeClass(s.grade);
                const gs = gradeShort(s.grade);
                const sr = s.factors.success_rate != null ? s.factors.success_rate.toFixed(0) + '%' : '-';
                const barWidth = Math.min(100, s.total_score);
                const barColor = s.total_score >= 80 ? '#22c55e' : s.total_score >= 60 ? '#3b82f6' : '#eab308';
                return `<tr>
                    <td>${rank}</td>
                    <td style="font-weight:600;">${s.skill_id}</td>
                    <td>
                        ${s.total_score}
                        <span class="score-bar" style="width:${barWidth}px;background:${barColor};"></span>
                    </td>
                    <td><span class="grade ${gc}">${gs}</span></td>
                    <td>${sr}</td>
                </tr>`;
            }).join('');
        }

        function renderScoreChart(scores) {
            if (!scores || scores.length === 0) return;

            const labels = scores.map(s => s.skill_id.replace(/-/g, ' '));
            const data = scores.map(s => s.total_score);
            const colors = scores.map(s =>
                s.total_score >= 80 ? 'rgba(34, 197, 94, 0.7)' :
                s.total_score >= 60 ? 'rgba(59, 130, 246, 0.7)' :
                'rgba(234, 179, 8, 0.7)'
            );

            const ctx = document.getElementById('scoreChart').getContext('2d');
            if (scoreChart) scoreChart.destroy();

            scoreChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        backgroundColor: colors,
                        borderColor: 'rgba(15, 23, 42, 0.8)',
                        borderWidth: 2,
                    }],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'right',
                            labels: { color: '#94a3b8', font: { size: 11 }, padding: 12 },
                        },
                    },
                },
            });
        }

        function renderRecs(data) {
            const container = document.getElementById('recList');
            // 从 API 获取推荐
            fetch('/api/recommendations')
                .then(r => r.json())
                .then(recs => {
                    if (!recs || recs.length === 0) {
                        container.innerHTML = '<p style="color:#94a3b8;text-align:center;padding:1rem;">✅ 当前 Skill 配置完善，暂无推荐</p>';
                        return;
                    }
                    container.innerHTML = recs.slice(0, 5).map(r => `
                        <div class="rec-card">
                            <span class="badge ${badgeClass(r.reason_type)}">${badgeLabel(r.reason_type)}</span>
                            <span class="rec-name">${r.name}</span>
                            <span style="color:#64748b;font-size:0.8rem;">(${r.slug})</span>
                            <div class="rec-meta">
                                ${r.category} &nbsp;|&nbsp; ⭐ ${r.hub_rating || '-'} &nbsp;|&nbsp;
                                安装 ${r.hub_installs || 0} &nbsp;|&nbsp;
                                推荐分 <strong>${r.recommendation_score}</strong>
                            </div>
                            <div class="rec-reason">${r.reason_detail}</div>
                        </div>
                    `).join('');
                })
                .catch(() => {
                    container.innerHTML = '<p style="color:#94a3b8;">推荐加载失败</p>';
                });
        }

        function renderFeedbacks(feedbacks) {
            const container = document.getElementById('feedbackList');
            if (!feedbacks || feedbacks.length === 0) {
                container.innerHTML = '<p style="color:#94a3b8;text-align:center;padding:1rem;">暂无反馈记录</p>';
                return;
            }

            container.innerHTML = feedbacks.slice(0, 8).map(fb => {
                const stars = '⭐'.repeat(fb.rating) + '☆'.repeat(5 - fb.rating);
                const comment = fb.comment || '(无评论)';
                const date = (fb.created_at || '').slice(0, 10);
                return `
                    <div class="feedback-item">
                        <div>
                            <span class="feedback-stars">${stars}</span>
                            <span style="font-weight:600;margin-left:0.5rem;">${fb.skill_id}</span>
                            <span style="color:#64748b;font-size:0.75rem;float:right;">${date}</span>
                        </div>
                        <div class="feedback-comment">${comment}</div>
                    </div>
                `;
            }).join('');
        }

        async function loadData() {
            try {
                const res = await fetch('/api/dashboard');
                const data = await res.json();

                document.getElementById('lastUpdate').textContent =
                    '更新: ' + new Date().toLocaleTimeString('zh-CN');

                renderKPIs(data.overview);
                renderTrendChart(data.daily_runs);
                renderScores(data.scores);
                renderScoreChart(data.scores);
                renderRecs(data);
                renderFeedbacks(data.recent_feedbacks);
            } catch (e) {
                console.error('加载数据失败:', e);
            }
        }

        // 首次加载
        loadData();

        // 自动刷新 (每 60 秒)
        setInterval(loadData, 60000);
    </script>
</body>
</html>
"""


# ──────── API 路由 ────────

@app.route("/")
def index():
    """仪表盘主页"""
    return render_template_string(DASHBOARD_HTML)


@app.route("/api/dashboard")
def api_dashboard():
    """仪表盘数据 API"""
    reporter = _state["reporter"]
    if not reporter:
        return jsonify({"error": "未初始化"}), 500

    data = reporter.get_dashboard_data()
    return jsonify(data)


@app.route("/api/recommendations")
def api_recommendations():
    """推荐数据 API"""
    store = _state["store"]
    registry = _state["registry"]
    agent_id = _state["agent_id"]

    if not store or not registry or not agent_id:
        return jsonify([])

    try:
        recommender = SkillRecommender(registry, store, agent_id)
        recs = recommender.get_all_recommendations(max_per_type=3)
        return jsonify([r.to_dict() for r in recs])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/scores")
def api_scores():
    """评分数据 API"""
    store = _state["store"]
    registry = _state["registry"]
    agent_id = _state["agent_id"]

    if not store or not registry or not agent_id:
        return jsonify([])

    try:
        evaluator = SkillEvaluator(store, agent_id)
        skill_ids = [s.slug for s in registry.get_runnable_skills()]
        scores = evaluator.evaluate_all(skill_ids)
        return jsonify([s.to_dict() for s in scores])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/report")
def api_generate_report():
    """生成并返回日报"""
    reporter = _state["reporter"]
    store = _state["store"]
    registry = _state["registry"]
    agent_id = _state["agent_id"]

    if not reporter:
        return jsonify({"error": "未初始化"}), 500

    try:
        evaluator = SkillEvaluator(store, agent_id)
        skill_ids = [s.slug for s in registry.get_runnable_skills()]
        scores = evaluator.evaluate_all(skill_ids)

        recommender = SkillRecommender(registry, store, agent_id)
        recs = recommender.get_all_recommendations(max_per_type=3)

        filepath = reporter.generate_and_save_daily(scores=scores, recommendations=recs)
        return jsonify({"status": "ok", "path": filepath})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/health")
def api_health():
    """健康检查"""
    return jsonify({
        "status": "ok",
        "agent_id": _state.get("agent_id", ""),
        "timestamp": datetime.now().isoformat(),
    })


# ──────── 主入口 ────────

def main():
    parser = argparse.ArgumentParser(description="Skills Monitor Web Dashboard")
    parser.add_argument("--port", type=int, default=5050, help="端口号 (默认 5050)")
    parser.add_argument("--host", default="127.0.0.1", help="绑定地址 (默认 127.0.0.1)")
    parser.add_argument("--demo", action="store_true", help="使用 Demo 数据目录")
    parser.add_argument("--debug", action="store_true", help="开启调试模式")
    args = parser.parse_args()

    data_dir = DEMO_DATA_DIR if args.demo else DEFAULT_CONFIG_DIR
    print(f"📊 Skills Monitor Web Dashboard")
    print(f"   数据目录: {data_dir}")
    print(f"   Skills 目录: {SKILLS_DIR}")
    print(f"   报告目录: {REPORTS_DIR}")
    print()

    init_state(data_dir)

    print(f"🚀 启动 Web 服务: http://{args.host}:{args.port}")
    print(f"   仪表盘: http://{args.host}:{args.port}/")
    print(f"   API: http://{args.host}:{args.port}/api/dashboard")
    print(f"   生成报告: http://{args.host}:{args.port}/api/report")
    print()

    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()

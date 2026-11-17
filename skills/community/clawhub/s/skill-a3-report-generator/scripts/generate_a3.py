#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A3改善报告生成器 v2
- 布局：CSS Grid双列，内容自适应高度
- 表格：td contenteditable 多行文本
- 上传：5个固定区域，支持点击/拖拽/Ctrl+V
- 打印：优化颜色保真，空上传位隐藏
"""

import argparse
import json
from datetime import datetime
from pathlib import Path


# HTML模板 v2
HTML_TEMPLATE_V2 = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>A3改善报告</title>
    <style>
        /* ==================== 全局样式 ==================== */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: "Microsoft YaHei", "微软雅黑", "PingFang SC", Arial, sans-serif;
            font-size: 9.5px;
            line-height: 1.3;
            background: #e0e0e0;
            padding: 20px;
        }
        
        /* ==================== A3纸张 ==================== */
        .a3-paper {
            width: 420mm;
            height: 297mm;
            margin: 0 auto;
            background: white;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            padding: 8mm 10mm;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }
        
        /* ==================== Header ==================== */
        .report-header {
            display: grid;
            grid-template-columns: auto 1fr auto;
            gap: 10px;
            align-items: center;
            padding-bottom: 4px;
            border-bottom: 2px solid #1a5fb4;
            flex-shrink: 0;
        }
        
        .report-title {
            font-size: 14px;
            font-weight: bold;
            color: #1a5fb4;
        }
        
        .header-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 8px 15px;
            font-size: 9.5px;
        }
        
        .meta-item {
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        .meta-label { font-weight: bold; color: #555; }
        
        /* ==================== 主内容区 ==================== */
        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 6px;
            align-items: start;
            flex: 1;
            overflow: hidden;
        }
        
        .left-column, .right-column {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }
        
        /* ==================== 模块通用 ==================== */
        .module {
            border: 1px solid;
            border-radius: 3px;
            overflow: hidden;
        }
        
        .module-title {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 3px 6px;
            font-size: 11px;
            font-weight: bold;
            color: white;
        }
        
        .module-title .subtitle {
            font-size: 8px;
            font-weight: normal;
            opacity: 0.9;
        }
        
        .module-content {
            padding: 4px;
            font-size: 9.5px;
        }
        
        /* 模块配色 */
        .module.problem-desc { border-color: #f59e0b; }
        .module.problem-desc .module-title { background: #f59e0b; }
        
        .module.current-state { border-color: #43a047; }
        .module.current-state .module-title { background: #43a047; }
        
        .module.goal-setting { border-color: #1976d2; }
        .module.goal-setting .module-title { background: #1976d2; }
        
        .module.root-cause { border-color: #e91e63; }
        .module.root-cause .module-title { background: #e91e63; }
        
        .module.decision-table { border-color: #ff5722; }
        .module.decision-table .module-title { background: #ff5722; }
        
        .module.action-plan { border-color: #00acc1; }
        .module.action-plan .module-title { background: #00acc1; }
        
        .module.verification { border-color: #7b1fa2; }
        .module.verification .module-title { background: #7b1fa2; }
        
        .module.summary-share { border-color: #455a64; }
        .module.summary-share .module-title { background: #455a64; }
        
        /* ==================== 可编辑区域 ==================== */
        [contenteditable] {
            outline: none;
            border: 1px dashed transparent;
            padding: 2px 3px;
            border-radius: 2px;
            min-height: 16px;
        }
        
        [contenteditable]:hover {
            border-color: #ccc;
            background: #f8f9ff;
        }
        
        [contenteditable]:focus {
            border-color: #1a5fb4;
            background: #fff;
        }
        
        [contenteditable]:empty::before {
            content: attr(data-placeholder);
            color: #bbb;
            font-style: italic;
            font-size: 8px;
        }
        
        /* ==================== 表格 ==================== */
        .std-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 9px;
        }
        
        .std-table td {
            padding: 3px 4px;
            border: 1px solid #ddd;
            vertical-align: top;
        }
        
        .std-table td[contenteditable] {
            border-color: #eee;
        }
        
        .std-table .label-cell {
            background: #f5f5f5;
            font-weight: bold;
            width: 50px;
            white-space: nowrap;
        }
        
        .std-table input, .std-table textarea {
            width: 100%;
            border: none;
            background: transparent;
            font-family: inherit;
            font-size: inherit;
            resize: none;
        }
        
        .std-table input:focus, .std-table textarea:focus {
            outline: 2px solid #1a5fb4;
            outline-offset: -2px;
        }
        
        /* ==================== 5Why专用表 ==================== */
        .why-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 9px;
        }
        
        .why-table th {
            padding: 3px 4px;
            border: 1px solid #ddd;
            color: white;
            font-weight: bold;
        }
        
        .why-table td {
            padding: 2px;
            border: 1px solid #ddd;
            vertical-align: top;
        }
        
        .why-table td[contenteditable] {
            border-color: #eee;
            min-height: 20px;
        }
        
        .why-table .cause-col {
            width: 28%;
        }
        
        .why-table .cause-header { background: #e91e63; }
        .why-table .cause-header-b { background: #ec407a; }
        .why-table .cause-header-c { background: #f06292; }
        
        .why-table .level-cell {
            background: #fce4ec;
            font-weight: bold;
            text-align: center;
            width: 35px;
        }
        
        .why-table .root-cause-row td {
            background: #c8e6c9;
            font-weight: bold;
        }
        
        /* ==================== 决策表 ==================== */
        .action-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 9px;
        }
        
        .action-table th {
            padding: 3px;
            border: 1px solid #ddd;
            color: white;
            font-weight: bold;
        }
        
        .action-table th { background: #ff5722; }
        
        .action-table td {
            padding: 2px;
            border: 1px solid #ddd;
            vertical-align: top;
        }
        
        .action-table textarea {
            width: 100%;
            height: 24px;
            border: none;
            background: transparent;
            font-family: inherit;
            font-size: inherit;
            resize: none;
        }
        
        .action-table textarea:focus {
            outline: 2px solid #ff5722;
            outline-offset: -2px;
        }
        
        /* ==================== 时间线表 ==================== */
        .timeline-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 9px;
        }
        
        .timeline-table th {
            padding: 3px;
            border: 1px solid #ddd;
            color: white;
        }
        
        .timeline-table th { background: #00acc1; }
        
        .timeline-table td {
            padding: 2px;
            border: 1px solid #ddd;
            text-align: center;
        }
        
        .timeline-table td:first-child {
            text-align: left;
            font-weight: bold;
            background: #e0f7fa;
        }
        
        .milestone-cell { background: #fff9c4; font-weight: bold; color: #e65100; }
        
        /* ==================== 验证对比 ==================== */
        .result-compare {
            display: flex;
            gap: 6px;
            margin-bottom: 4px;
        }
        
        .compare-box {
            flex: 1;
            background: white;
            border: 1px solid #ddd;
            border-radius: 3px;
            padding: 4px;
            text-align: center;
        }
        
        .compare-box h4 { font-size: 8px; color: #666; margin-bottom: 2px; }
        .compare-box .value { font-size: 12px; font-weight: bold; }
        .compare-box.before .value { color: #dc3545; }
        .compare-box.after .value { color: #28a745; }
        .compare-box.improvement .value { color: #1976d2; }
        
        /* ==================== 图片上传区 ==================== */
        .image-zone {
            border: 1px dashed #bbb;
            border-radius: 3px;
            padding: 6px;
            text-align: center;
            color: #999;
            font-size: 8px;
            cursor: pointer;
            transition: all 0.2s;
            position: relative;
        }
        
        .image-zone:hover {
            border-color: #1a5fb4;
            background: #f0f7ff;
        }
        
        .image-zone.dragover {
            border-color: #1a5fb4;
            background: #e3f2fd;
        }
        
        .image-zone.has-image {
            border-style: solid;
            border-color: #ddd;
            padding: 3px;
        }
        
        .image-zone img {
            max-width: 100%;
            max-height: 50px;
            display: block;
        }
        
        .image-zone .zone-label {
            font-size: 8px;
            color: #888;
        }
        
        .image-zone .zone-actions {
            display: none;
            position: absolute;
            top: 2px;
            right: 2px;
            gap: 2px;
        }
        
        .image-zone.has-image .zone-actions {
            display: flex;
        }
        
        .image-zone .zone-actions button {
            padding: 2px 5px;
            font-size: 8px;
            border: none;
            border-radius: 2px;
            cursor: pointer;
        }
        
        .btn-replace { background: #1a5fb4; color: white; }
        .btn-clear { background: #dc3545; color: white; }
        
        /* ==================== 签名区 ==================== */
        .signatures {
            display: flex;
            justify-content: space-between;
            padding-top: 4px;
            border-top: 1px solid #ddd;
            flex-shrink: 0;
        }
        
        .signature-box {
            text-align: center;
            font-size: 8px;
        }
        
        .signature-box .label { color: #666; margin-bottom: 2px; }
        .signature-box .name {
            border-bottom: 1px solid #333;
            padding: 2px 20px;
            min-width: 70px;
        }
        .signature-box .date { color: #999; margin-top: 1px; }
        
        /* ==================== 工具栏 ==================== */
        .toolbar {
            position: fixed;
            top: 10px;
            right: 10px;
            display: flex;
            gap: 6px;
            z-index: 100;
        }
        
        .toolbar button {
            background: #1a5fb4;
            color: white;
            border: none;
            padding: 8px 14px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 11px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }
        
        .toolbar button:hover { background: #1557a0; }
        .toolbar .secondary { background: #6c757d; }
        .toolbar .secondary:hover { background: #5a6268; }
        
        .hint-bar {
            position: fixed;
            bottom: 10px;
            left: 50%;
            transform: translateX(-50%);
            background: #333;
            color: white;
            padding: 8px 16px;
            border-radius: 15px;
            font-size: 9px;
            z-index: 100;
        }
        
        /* ==================== 模态框 ==================== */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.9);
            z-index: 1000;
            justify-content: center;
            align-items: center;
            cursor: pointer;
        }
        
        .modal.show { display: flex; }
        .modal img { max-width: 90%; max-height: 90%; border: 3px solid white; }
        
        /* ==================== 打印样式 ==================== */
        @media print {
            body { background: white; padding: 0; }
            
            .a3-paper {
                box-shadow: none;
                width: 420mm;
                height: 297mm;
                margin: 0;
                padding: 6mm 8mm;
            }
            
            .toolbar, .hint-bar, .modal { display: none !important; }
            
            [contenteditable] {
                border: none !important;
                background: transparent !important;
            }
            
            .image-zone:not(.has-image) { display: none !important; }
            
            * { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
            
            @page { size: A3 landscape; margin: 0; }
        }
    </style>
</head>
<body>
    <!-- 工具栏 -->
    <div class="toolbar">
        <button onclick="saveHTML()">💾 另存HTML</button>
        <button class="secondary" onclick="window.print()">🖨 打印/导出PDF</button>
    </div>
    
    <!-- A3纸张 -->
    <div class="a3-paper">
        <!-- Header -->
        <div class="report-header">
            <div class="report-title">A3 改善报告</div>
            <div class="header-meta">
                <div class="meta-item"><span class="meta-label">部门:</span><span contenteditable="true" data-placeholder="部门">{{ meta.department }}</span></div>
                <div class="meta-item"><span class="meta-label">日期:</span><span contenteditable="true" data-placeholder="YYYY-MM-DD">{{ meta.date }}</span></div>
                <div class="meta-item"><span class="meta-label">负责人:</span><span contenteditable="true" data-placeholder="姓名">{{ meta.owner }}</span></div>
                <div class="meta-item"><span class="meta-label">目标节点:</span><span contenteditable="true" data-placeholder="如：2024-03-31">{{ meta.deadline }}</span></div>
            </div>
        </div>
        
        <!-- 主内容 -->
        <div class="main-content">
            <!-- 左列 -->
            <div class="left-column">
                
                <!-- ① 问题描述 -->
                <div class="module problem-desc">
                    <div class="module-title">
                        <span>问题描述</span>
                        <span class="subtitle">STAR原则</span>
                    </div>
                    <div class="module-content">
                        <table class="std-table">
                            <tr>
                                <td class="label-cell">S 情境</td>
                                <td contenteditable="true" data-placeholder="何时、何地、什么条件下发生？">{{ problem.situation }}</td>
                            </tr>
                            <tr>
                                <td class="label-cell">T 任务</td>
                                <td contenteditable="true" data-placeholder="预期应该达到什么标准？">{{ problem.task }}</td>
                            </tr>
                            <tr>
                                <td class="label-cell">A 行动</td>
                                <td contenteditable="true" data-placeholder="实际发生了什么？">{{ problem.action }}</td>
                            </tr>
                            <tr>
                                <td class="label-cell">R 结果</td>
                                <td contenteditable="true" data-placeholder="造成了什么影响？">{{ problem.result }}</td>
                            </tr>
                        </table>
                        <div class="image-zone" id="problem-img" data-zone="problem-img" onclick="triggerUpload(this)">
                            <span class="zone-label">📷 现场照片（可选）</span>
                            <span style="font-size:7px;color:#bbb;">点击/拖拽/Ctrl+V粘贴</span>
                        </div>
                    </div>
                </div>
                
                <!-- ② 现状分析 -->
                <div class="module current-state">
                    <div class="module-title">
                        <span>现状分析</span>
                        <span class="subtitle">数据支撑</span>
                    </div>
                    <div class="module-content">
                        <div contenteditable="true" data-placeholder="描述关键数据和问题点">{{ current_state.description }}</div>
                        <div class="image-zone" id="current-img" data-zone="current-img" onclick="triggerUpload(this)">
                            <span class="zone-label">📊 数据图表（可选）</span>
                            <span style="font-size:7px;color:#bbb;">点击/拖拽/Ctrl+V粘贴</span>
                        </div>
                    </div>
                </div>
                
                <!-- ③ 目标设定 -->
                <div class="module goal-setting">
                    <div class="module-title">
                        <span>目标设定</span>
                        <span class="subtitle">SMART原则</span>
                    </div>
                    <div class="module-content">
                        <table class="std-table">
                            <tr><td class="label-cell">S 具体</td><td contenteditable="true" data-placeholder="具体目标">{{ goal.specific }}</td></tr>
                            <tr><td class="label-cell">M 可衡量</td><td contenteditable="true" data-placeholder="量化指标">{{ goal.measurable }}</td></tr>
                            <tr><td class="label-cell">A 可达成</td><td contenteditable="true" data-placeholder="是否现实">{{ goal.achievable }}</td></tr>
                            <tr><td class="label-cell">R 相关</td><td contenteditable="true" data-placeholder="与业务关联">{{ goal.relevant }}</td></tr>
                            <tr><td class="label-cell">T 有时限</td><td contenteditable="true" data-placeholder="截止日期">{{ goal.timebound }}</td></tr>
                        </table>
                    </div>
                </div>
                
                <!-- ④ 根本原因分析 -->
                <div class="module root-cause">
                    <div class="module-title">
                        <span>根本原因分析</span>
                        <span class="subtitle">5Why追问</span>
                    </div>
                    <div class="module-content">
                        <table class="why-table">
                            <tr>
                                <th class="level-cell">层级</th>
                                <th class="cause-col cause-header">主因A-机</th>
                                <th class="cause-col cause-header-b">主因B-料</th>
                                <th class="cause-col cause-header-c">主因C-法</th>
                            </tr>
                            {{ why_rows|safe }}
                            <tr class="root-cause-row">
                                <td class="level-cell" style="background:#4caf50;color:white;">根因</td>
                                <td colspan="3" contenteditable="true" data-placeholder="系统性根因总结">{{ root_cause.root_cause }}</td>
                            </tr>
                        </table>
                        <div class="image-zone" id="fishbone-img" data-zone="fishbone-img" onclick="triggerUpload(this)">
                            <span class="zone-label">🎣 鱼骨图（可选）</span>
                            <span style="font-size:7px;color:#bbb;">点击/拖拽/Ctrl+V粘贴</span>
                        </div>
                    </div>
                </div>
                
            </div>
            
            <!-- 右列 -->
            <div class="right-column">
                
                <!-- ⑤ 改进措施 -->
                <div class="module decision-table">
                    <div class="module-title">
                        <span>改进措施</span>
                        <span class="subtitle">原因-措施对应</span>
                    </div>
                    <div class="module-content">
                        <table class="action-table">
                            <tr>
                                <th style="width:25%;">对应原因</th>
                                <th style="width:40%;">改进措施</th>
                                <th style="width:15%;">负责人</th>
                                <th style="width:12%;">完成日</th>
                                <th style="width:8%;">状态</th>
                            </tr>
                            {{ action_rows|safe }}
                        </table>
                    </div>
                </div>
                
                <!-- ⑥ 行动计划 -->
                <div class="module action-plan">
                    <div class="module-title">
                        <span>行动计划</span>
                        <span class="subtitle">时间节点</span>
                    </div>
                    <div class="module-content">
                        <table class="timeline-table">
                            <tr>
                                <th>措施</th>
                                <th>阶段1</th>
                                <th>阶段2</th>
                                <th>阶段3</th>
                                <th>里程碑</th>
                                <th>验证</th>
                            </tr>
                            {{ timeline_rows|safe }}
                        </table>
                        <div class="image-zone" id="gantt-img" data-zone="gantt-img" onclick="triggerUpload(this)">
                            <span class="zone-label">📅 甘特图（可选）</span>
                            <span style="font-size:7px;color:#bbb;">点击/拖拽/Ctrl+V粘贴</span>
                        </div>
                    </div>
                </div>
                
                <!-- ⑦ 验证与标准化 -->
                <div class="module verification">
                    <div class="module-title">
                        <span>验证与标准化</span>
                        <span class="subtitle">改善成果</span>
                    </div>
                    <div class="module-content">
                        <div class="result-compare">
                            <div class="compare-box before">
                                <h4>改善前</h4>
                                <div class="value" contenteditable="true">{{ verification.before }}</div>
                            </div>
                            <div class="compare-box after">
                                <h4>改善后</h4>
                                <div class="value" contenteditable="true">{{ verification.after }}</div>
                            </div>
                            <div class="compare-box improvement">
                                <h4>提升</h4>
                                <div class="value" contenteditable="true">{{ verification.improvement }}</div>
                            </div>
                        </div>
                        <div contenteditable="true" data-placeholder="列出现已形成的标准化文件" style="margin-bottom:4px;">{{ verification.standardization }}</div>
                        <div class="image-zone" id="result-img" data-zone="result-img" onclick="triggerUpload(this)">
                            <span class="zone-label">📈 改善成果图（可选）</span>
                            <span style="font-size:7px;color:#bbb;">点击/拖拽/Ctrl+V粘贴</span>
                        </div>
                    </div>
                </div>
                
                <!-- ⑧ 整体总结与分享 -->
                <div class="module summary-share">
                    <div class="module-title">
                        <span>整体总结与分享</span>
                        <span class="subtitle">经验沉淀</span>
                    </div>
                    <div class="module-content">
                        <div contenteditable="true" data-placeholder="改善过程中的关键经验教训、可复用的方法、下一步改进方向...">{{ summary }}</div>
                    </div>
                </div>
                
            </div>
        </div>
        
        <!-- 签名区 -->
        <div class="signatures">
            <div class="signature-box">
                <div class="label">制表人</div>
                <div class="name" contenteditable="true"></div>
                <div class="date">日期: ________</div>
            </div>
            <div class="signature-box">
                <div class="label">审核人</div>
                <div class="name" contenteditable="true"></div>
                <div class="date">日期: ________</div>
            </div>
            <div class="signature-box">
                <div class="label">批准人</div>
                <div class="name" contenteditable="true"></div>
                <div class="date">日期: ________</div>
            </div>
            <div class="signature-box">
                <div class="label">客户确认</div>
                <div class="name" contenteditable="true"></div>
                <div class="date">日期: ________</div>
            </div>
        </div>
        
    </div>
    
    <!-- 提示 -->
    <div class="hint-bar">💡 点击编辑文字 | 上传区支持点击/拖拽/Ctrl+V粘贴图片 | 打印选A3横向</div>
    
    <!-- 文件输入 -->
    <input type="file" id="fileInput" accept="image/*" style="display:none;" onchange="handleFileSelect(event)">
    
    <script>
        /* ==================== 图片上传处理 ==================== */
        let currentZone = null;
        let hoveredZone = null;
        
        function triggerUpload(el) {
            currentZone = el;
            document.getElementById('fileInput').click();
        }
        
        function handleFileSelect(e) {
            const file = e.target.files[0];
            if (file && currentZone) {
                const reader = new FileReader();
                reader.onload = function(ev) { setZoneImage(currentZone, ev.target.result); };
                reader.readAsDataURL(file);
            }
            e.target.value = '';
        }
        
        function setZoneImage(el, src) {
            el.classList.add('has-image');
            el.innerHTML = `
                <img src="${src}" alt="图片" onclick="showModal(this.src)">
                <div class="zone-actions">
                    <button class="btn-replace" onclick="event.stopPropagation(); triggerUpload(el.parentElement.parentElement);">替换</button>
                    <button class="btn-clear" onclick="event.stopPropagation(); clearZone(el.parentElement.parentElement);">清除</button>
                </div>
            `;
        }
        
        function clearZone(el) {
            el.classList.remove('has-image');
            const zoneId = el.dataset.zone;
            const labels = {
                'problem-img': '📷 现场照片（可选）',
                'current-img': '📊 数据图表（可选）',
                'fishbone-img': '🎣 鱼骨图（可选）',
                'gantt-img': '📅 甘特图（可选）',
                'result-img': '📈 改善成果图（可选）'
            };
            el.innerHTML = `
                <span class="zone-label">${labels[zoneId] || ''}</span>
                <span style="font-size:7px;color:#bbb;">点击/拖拽/Ctrl+V粘贴</span>
            `;
        }
        
        function showModal(src) {
            const m = document.createElement('div');
            m.className = 'modal show';
            m.innerHTML = `<img src="${src}" alt="预览">`;
            m.onclick = function() { m.classList.remove('show'); setTimeout(() => m.remove(), 200); };
            document.body.appendChild(m);
        }
        
        /* ==================== 拖拽上传 ==================== */
        document.querySelectorAll('.image-zone').forEach(z => {
            z.addEventListener('dragover', e => { e.preventDefault(); z.classList.add('dragover'); });
            z.addEventListener('dragleave', e => z.classList.remove('dragover'));
            z.addEventListener('drop', e => {
                e.preventDefault();
                z.classList.remove('dragover');
                const file = e.dataTransfer.files[0];
                if (file && file.type.indexOf('image') !== -1) {
                    const reader = new FileReader();
                    reader.onload = function(ev) { setZoneImage(z, ev.target.result); };
                    reader.readAsDataURL(file);
                }
            });
            z.addEventListener('mouseenter', () => { hoveredZone = z; });
            z.addEventListener('mouseleave', () => { if (hoveredZone === z) hoveredZone = null; });
        });
        
        /* ==================== Ctrl+V粘贴 ==================== */
        document.addEventListener('paste', e => {
            const items = e.clipboardData.items;
            for (let i = 0; i < items.length; i++) {
                if (items[i].type.indexOf('image') !== -1) {
                    e.preventDefault();
                    const file = items[i].getAsFile();
                    const reader = new FileReader();
                    reader.onload = function(ev) {
                        const target = hoveredZone || currentZone;
                        if (target) setZoneImage(target, ev.target.result);
                    };
                    reader.readAsDataURL(file);
                    break;
                }
            }
        });
        
        /* ==================== 另存HTML ==================== */
        function saveHTML() {
            const html = document.documentElement.outerHTML;
            const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'A3改善报告_' + new Date().toISOString().slice(0,10) + '.html';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }
    </script>
</body>
</html>'''


def parse_json_arg(arg_value):
    """解析JSON字符串或JSON文件路径"""
    if not arg_value:
        return {}
    try:
        return json.loads(arg_value)
    except json.JSONDecodeError:
        path = Path(arg_value)
        if path.exists():
            return json.loads(path.read_text(encoding='utf-8'))
        return {}


def build_why_rows(root_cause):
    """构建5Why表格行"""
    whys = root_cause.get('whys', [])
    if isinstance(whys, str):
        lines = whys.strip().split('\n')
        whys = [{'level': f'Why{i+1}', 'text': line.strip()} for i, line in enumerate(lines) if line.strip()]
    
    # 构建3列结构
    rows = []
    max_rows = max(len(whys), 4)  # 至少4行 Why1-Why4
    
    for i in range(max_rows):
        level = f"Why{i+1}"
        if i < len(whys):
            why_item = whys[i]
            if isinstance(why_item, dict):
                level = why_item.get('level', f"Why{i+1}")
        rows.append(f'''
            <tr>
                <td class="level-cell">{level}</td>
                <td class="cause-col" contenteditable="true" data-placeholder="机"></td>
                <td class="cause-col" contenteditable="true" data-placeholder="料"></td>
                <td class="cause-col" contenteditable="true" data-placeholder="法"></td>
            </tr>
        ''')
    
    return '\n'.join(rows)


def build_action_rows(actions):
    """构建决策表行"""
    if isinstance(actions, dict):
        actions = [actions]
    if not actions:
        actions = [{}]
    
    rows = []
    for action in actions:
        cause = action.get('cause', '')
        measures = action.get('measures', '')
        owner = action.get('owner', '')
        deadline = action.get('deadline', '')
        rows.append(f'''
            <tr>
                <td contenteditable="true">{cause}</td>
                <td><textarea>{measures}</textarea></td>
                <td contenteditable="true">{owner}</td>
                <td contenteditable="true">{deadline}</td>
                <td style="text-align:center;">📋</td>
            </tr>
        ''')
    
    return '\n'.join(rows)


def build_timeline_rows(timeline):
    """构建时间线表行"""
    if isinstance(timeline, dict):
        timeline = [timeline]
    if not timeline:
        timeline = [{}]
    
    rows = []
    for item in timeline:
        name = item.get('name', '')
        phase1 = item.get('phase1', '')
        phase2 = item.get('phase2', '')
        phase3 = item.get('phase3', '')
        milestone = item.get('milestone', '')
        verification = item.get('verification', '')
        rows.append(f'''
            <tr>
                <td contenteditable="true">{name}</td>
                <td contenteditable="true">{phase1}</td>
                <td contenteditable="true">{phase2}</td>
                <td contenteditable="true">{phase3}</td>
                <td class="milestone-cell" contenteditable="true">{milestone}</td>
                <td contenteditable="true">{verification}</td>
            </tr>
        ''')
    
    return '\n'.join(rows)


def main():
    parser = argparse.ArgumentParser(description='生成A3改善报告HTML v2')
    parser.add_argument('--problem', type=str, default='{}')
    parser.add_argument('--current_state', type=str, default='{}')
    parser.add_argument('--goal', type=str, default='{}')
    parser.add_argument('--root_cause', type=str, default='{}')
    parser.add_argument('--actions', type=str, default='[]')
    parser.add_argument('--timeline', type=str, default='[]')
    parser.add_argument('--verification', type=str, default='{}')
    parser.add_argument('--summary', type=str, default='')
    parser.add_argument('--meta', type=str, default='{},{},{}')
    parser.add_argument('--output', type=str, default='./a3_report.html')
    
    args = parser.parse_args()
    
    # 解析参数
    problem = parse_json_arg(args.problem)
    current_state = parse_json_arg(args.current_state)
    goal = parse_json_arg(args.goal)
    root_cause = parse_json_arg(args.root_cause)
    actions = parse_json_arg(args.actions)
    timeline = parse_json_arg(args.timeline)
    verification = parse_json_arg(args.verification)
    summary = args.summary
    
    # 解析meta
    meta_parts = args.meta.split(',')
    meta = {
        'department': meta_parts[0].strip() if len(meta_parts) > 0 else '',
        'date': meta_parts[1].strip() if len(meta_parts) > 1 else datetime.now().strftime('%Y-%m-%d'),
        'owner': meta_parts[2].strip() if len(meta_parts) > 2 else '',
        'deadline': meta_parts[3].strip() if len(meta_parts) > 3 else ''
    }
    
    # 设置默认值
    problem.setdefault('situation', '')
    problem.setdefault('task', '')
    problem.setdefault('action', '')
    problem.setdefault('result', '')
    current_state.setdefault('description', '')
    goal.setdefault('specific', '')
    goal.setdefault('measurable', '')
    goal.setdefault('achievable', '')
    goal.setdefault('relevant', '')
    goal.setdefault('timebound', '')
    root_cause.setdefault('whys', [])
    root_cause.setdefault('root_cause', '')
    verification.setdefault('before', '')
    verification.setdefault('after', '')
    verification.setdefault('improvement', '')
    verification.setdefault('standardization', '')
    
    # 构建动态行
    why_rows = build_why_rows(root_cause)
    action_rows = build_action_rows(actions)
    timeline_rows = build_timeline_rows(timeline)
    
    # 渲染模板
    html_content = HTML_TEMPLATE_V2
    replacements = {
        '{{ meta.department }}': meta['department'],
        '{{ meta.date }}': meta['date'],
        '{{ meta.owner }}': meta['owner'],
        '{{ meta.deadline }}': meta['deadline'],
        '{{ problem.situation }}': problem['situation'],
        '{{ problem.task }}': problem['task'],
        '{{ problem.action }}': problem['action'],
        '{{ problem.result }}': problem['result'],
        '{{ current_state.description }}': current_state['description'],
        '{{ goal.specific }}': goal['specific'],
        '{{ goal.measurable }}': goal['measurable'],
        '{{ goal.achievable }}': goal['achievable'],
        '{{ goal.relevant }}': goal['relevant'],
        '{{ goal.timebound }}': goal['timebound'],
        '{{ root_cause.root_cause }}': root_cause['root_cause'],
        '{{ verification.before }}': verification['before'],
        '{{ verification.after }}': verification['after'],
        '{{ verification.improvement }}': verification['improvement'],
        '{{ verification.standardization }}': verification['standardization'],
        '{{ summary }}': summary,
        '{{ why_rows|safe }}': why_rows,
        '{{ action_rows|safe }}': action_rows,
        '{{ timeline_rows|safe }}': timeline_rows,
    }
    
    for key, value in replacements.items():
        html_content = html_content.replace(key, value)
    
    # 写入文件
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_content, encoding='utf-8')
    
    result = {
        'status': 'success',
        'output_path': str(output_path.absolute()),
        'message': f'A3报告已生成: {output_path.name}'
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()

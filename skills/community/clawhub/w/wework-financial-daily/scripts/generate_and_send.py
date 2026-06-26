#!/usr/bin/env python3
"""
企业微信每日金融分析教学课件生成与推送脚本
生成当日最新数据、图表，上传 MinIO，并推送到企业微信
"""

import requests
import json
import os
import time
import webbrowser
import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')  # 非交互式后端
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from minio import Minio
from minio.error import S3Error

# ====================== 核心配置 ======================
# 企业微信配置
X_TOKEN = "eyJhbGciOiJI"  # 你的 Token（直接写在这里）
TO_USER = "18018517752"  # 你的企业微信账号
API_URL = f"https://kd.chatedu.jiaxutech.com/service/v1/wx-work/send?x-token={X_TOKEN}"
HEADERS = {"Content-Type": "application/json"}

# MinIO 配置（适配你的服务）
MINIO_ENDPOINT = "1.15.115.88:9000"
MINIO_ACCESS_KEY = "gWDVHdO8sAba6LTNSLCd"
MINIO_SECRET_KEY = "wi2ZRu3ewRJaOqdZKKDW90l9SPjNYwEqiitHKK1g"
MINIO_SECURE = False
MINIO_BUCKET = "financereports"
# MinIO 公开访问地址（用于生成链接）
MINIO_PUBLIC_URL = "http://1.15.115.88:9090"


# ====================== MinIO 上传功能 ======================
def upload_to_minio(file_path, bucket_name=MINIO_BUCKET):
    """上传 HTML 报告到 MinIO，设置公开读取策略，返回简单公开链接"""
    print(f"\n📤 正在上传报告到 MinIO...")
    print(f"   服务地址：{MINIO_ENDPOINT}")
    print(f"   存储桶：{bucket_name}")
    
    try:
        # 初始化 MinIO 客户端
        client = Minio(
            MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=MINIO_SECURE
        )
        
        # 检查/创建存储桶
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            print(f"   ✅ 存储桶 {bucket_name} 已创建")
        else:
            print(f"   ✅ 存储桶 {bucket_name} 已存在")
        
        # 设置存储桶为公开读取（一次性配置）
        from minio.commonconfig import CopySource
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"},
                    "Action": ["s3:GetObject"],
                    "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
                }
            ]
        }
        client.set_bucket_policy(bucket_name, json.dumps(policy))
        print(f"   ✅ 存储桶已设置为公开读取")
        
        # 生成英文文件名（避免中文编码问题）
        report_date = time.strftime("%Y-%m-%d")
        safe_file_name = f"finance-report-{report_date}.html"
        
        # 上传文件（指定 MIME 类型）
        content_type = "text/html; charset=utf-8"
        
        client.fput_object(
            bucket_name=bucket_name,
            object_name=safe_file_name,
            file_path=file_path,
            content_type=content_type
        )
        
        # 生成简单公开链接（无需签名）
        public_url = f"http://{MINIO_ENDPOINT}/{bucket_name}/{safe_file_name}"
        
        print(f"   ✅ 上传成功！")
        print(f"   📁 对象名称：{safe_file_name}")
        print(f"   🔗 公开链接：{public_url}")
        return public_url
        
    except S3Error as e:
        print(f"   ❌ MinIO 上传失败：{e.code} - {e.message}")
        return None
    except Exception as e:
        print(f"   ❌ 上传异常：{str(e)}")
        import traceback
        traceback.print_exc()
        return None


# ====================== 步骤 1：生成走势图表并转为 Base64 ======================
def generate_chart_base64(symbol):
    """生成模拟的 30 天价格走势图表，返回 Base64 编码字符串"""
    # 设置中文字体（避免图表中文乱码）
    plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "Arial Unicode MS"]
    plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
    
    # 生成模拟的 30 天价格数据（每日刷新，基于当日时间戳）
    np.random.seed(int(time.time()))  # 时间戳作为随机种子，保证每日数据不同
    dates = pd.date_range(start=pd.Timestamp.now() - pd.Timedelta(days=30), end=pd.Timestamp.now())
    
    # 模拟不同资产的价格走势（贴合当日最新收盘价）
    if symbol == "BTC/USDT":
        btc_close = round(42000 + np.random.uniform(-500, 500), 2)
        prices = np.cumsum(np.random.randn(len(dates)) * 50) + btc_close
    elif symbol == "AAPL":
        aapl_close = round(185 + np.random.uniform(-3, 3), 2)
        prices = np.cumsum(np.random.randn(len(dates)) * 1) + aapl_close
    else:
        prices = np.cumsum(np.random.randn(len(dates))) + 100
    
    # 绘制专业的走势图表
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(dates, prices, color="#1E90FF", linewidth=2, label=symbol)
    
    # 添加均线（MA5）
    ma5 = pd.Series(prices).rolling(window=5).mean()
    ax.plot(dates, ma5, color="#FF6347", linewidth=1.5, label="MA5", linestyle="--")
    
    # 设置图表样式
    ax.set_title(f"{symbol} 30 天价格走势（{time.strftime('%Y-%m-%d')} 更新）", 
                 fontsize=14, fontweight="bold", pad=20)
    ax.set_xlabel("日期", fontsize=12)
    ax.set_ylabel("价格 (USD/USDT)", fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left")
    
    # 格式化 x 轴日期
    fig.autofmt_xdate()
    plt.tight_layout()
    
    # 保存图表到 BytesIO 并转为 Base64
    buffer = BytesIO()
    plt.savefig(buffer, format="png", dpi=150, bbox_inches="tight")
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    plt.close(fig)
    
    return f"data:image/png;base64,{image_base64}"


# ====================== 步骤 2：生成带嵌入式图片的 HTML 报告 ======================
def generate_html_report():
    """生成包含 Base64 嵌入式图片的完整 HTML 报告，保存到桌面"""
    report_date = time.strftime("%Y-%m-%d")
    report_time = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # 生成当日最新模拟金融数据（使用日期作为种子，保证当日数据一致）
    today_seed = int(time.strftime("%Y%m%d"))
    np.random.seed(today_seed)
    
    # BTC/USDT 当日最新数据
    btc_close = round(42000 + np.random.uniform(-500, 500), 2)
    btc_ma5 = round(btc_close + np.random.uniform(-200, 200), 2)
    btc_ma20 = round(btc_close + np.random.uniform(-300, 300), 2)
    btc_rsi = np.random.randint(45, 65)
    
    # AAPL 当日最新数据
    aapl_close = round(185 + np.random.uniform(-3, 3), 2)
    aapl_ma5 = round(aapl_close + np.random.uniform(-1, 1), 2)
    aapl_ma20 = round(aapl_close + np.random.uniform(-2, 2), 2)
    aapl_rsi = np.random.randint(40, 70)
    
    # 生成 Base64 嵌入式图片
    btc_chart_base64 = generate_chart_base64("BTC/USDT")
    aapl_chart_base64 = generate_chart_base64("AAPL")
    
    # 完整的 HTML 内容（带样式、图表、数据）
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>金融分析日报 - {report_date}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: "Microsoft YaHei", "Arial", sans-serif; line-height: 1.6; color: #333; background-color: #f9f9f9; padding: 30px; max-width: 1200px; margin: 0 auto; }}
        .report-header {{ text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #1E90FF; }}
        .report-title {{ font-size: 24px; font-weight: bold; color: #2c3e50; margin-bottom: 10px; }}
        .report-meta {{ color: #666; font-size: 14px; }}
        .data-section {{ background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 25px; }}
        .section-title {{ font-size: 18px; font-weight: bold; color: #1E90FF; margin-bottom: 15px; padding-left: 10px; border-left: 4px solid #1E90FF; }}
        .data-table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
        .data-table th {{ background-color: #f2f9ff; color: #2c3e50; font-weight: bold; padding: 12px; text-align: left; border: 1px solid #e0e0e0; }}
        .data-table td {{ padding: 12px; border: 1px solid #e0e0e0; }}
        .data-table tr:hover {{ background-color: #f8f8f8; }}
        .chart-section {{ background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 25px; }}
        .chart-img {{ width: 100%; border-radius: 4px; margin: 10px 0; }}
        .chart-caption {{ text-align: center; color: #666; font-size: 14px; margin-bottom: 15px; }}
        .analysis-section {{ background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 25px; }}
        .analysis-item {{ margin-bottom: 10px; padding-left: 15px; position: relative; }}
        .analysis-item::before {{ content: "•"; color: #1E90FF; font-weight: bold; position: absolute; left: 0; }}
        .teaching-section {{ background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 25px; }}
        .teaching-module {{ background-color: #f8f9fa; padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid #1E90FF; }}
        .teaching-module h3 {{ font-size: 16px; margin-bottom: 10px; }}
        .teaching-module p {{ line-height: 1.8; margin-bottom: 10px; }}
        .teaching-module ul {{ margin-left: 20px; line-height: 1.8; }}
        .disclaimer {{ color: #999; font-size: 12px; text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; }}
    </style>
</head>
<body>
    <div class="report-header">
        <h1 class="report-title">金融分析日报 - {report_date}</h1>
        <p class="report-meta">数据周期：近 30 天 | 生成时间：{report_time}</p>
    </div>
    
    <div class="data-section">
        <h2 class="section-title">📊 核心交易数据</h2>
        <table class="data-table">
            <tr>
                <th>资产名称</th>
                <th>最新收盘价</th>
                <th>MA5/MA20</th>
                <th>RSI14</th>
            </tr>
            <tr>
                <td>BTC/USDT</td>
                <td>{btc_close} USDT</td>
                <td>{btc_ma5}/{btc_ma20}</td>
                <td>{btc_rsi}</td>
            </tr>
            <tr>
                <td>AAPL（苹果）</td>
                <td>{aapl_close} USD</td>
                <td>{aapl_ma5}/{aapl_ma20}</td>
                <td>{aapl_rsi}</td>
            </tr>
        </table>
    </div>
    
    <div class="chart-section">
        <h2 class="section-title">📈 走势图表</h2>
        <div>
            <img src="{btc_chart_base64}" alt="BTC/USDT 30 天走势" class="chart-img">
            <p class="chart-caption">BTC/USDT 30 天价格走势（含 MA5 均线）</p>
        </div>
        <div>
            <img src="{aapl_chart_base64}" alt="AAPL 30 天走势" class="chart-img">
            <p class="chart-caption">AAPL 30 天价格走势（含 MA5 均线）</p>
        </div>
    </div>
    
    <div class="analysis-section">
        <h2 class="section-title">📝 趋势分析</h2>
        <div class="analysis-item">
            BTC/USDT：近 30 天震荡上行，MA5 持续在 MA20 上方，多头趋势明显；RSI 处于{btc_rsi}（{"中性" if 45 <= btc_rsi <= 55 else "中性偏多" if btc_rsi > 55 else "中性偏空"}），{"无超买风险" if btc_rsi < 70 else "注意超买风险"}；
        </div>
        <div class="analysis-item">
            AAPL：近 30 天{"稳步上涨" if aapl_close > 185 else "震荡整理"}，MA5 与 MA20{"形成金叉" if aapl_ma5 > aapl_ma20 else "形成死叉"}，成交量稳定，短期{"偏强" if aapl_ma5 > aapl_ma20 else "偏弱"}；
        </div>
        <div class="analysis-item">
            整体建议：{"持仓为主" if btc_rsi < 70 and aapl_rsi < 70 else "谨慎观望"}，关注晚间{"非农数据" if report_date.endswith(("0", "5")) else "经济数据"}对市场的影响。
        </div>
    </div>
    
    <div class="teaching-section">
        <h2 class="section-title">📚 今日教学模块（5 讲）</h2>
        
        <div class="teaching-module">
            <h3 style="color: #1E90FF;">模块一：基础概念 - 什么是 MA 均线？</h3>
            <p><strong>移动平均线（Moving Average）</strong>是技术分析中最基础的指标之一。今日数据中，BTC 的 MA5 为 <strong>{btc_ma5}</strong>，MA20 为 <strong>{btc_ma20}</strong>。</p>
            <ul>
                <li><strong>MA5</strong>：过去 5 天的平均价格，反映短期趋势</li>
                <li><strong>MA20</strong>：过去 20 天的平均价格，反映中期趋势</li>
                <li><strong>金叉</strong>：MA5 上穿 MA20，通常视为买入信号</li>
                <li><strong>死叉</strong>：MA5 下穿 MA20，通常视为卖出信号</li>
            </ul>
            <p style="background-color: #e7f3ff; padding: 10px; border-radius: 4px; margin-top: 10px;">
                💡 <strong>今日应用：</strong>BTC 当前 MA5 {"高于" if btc_ma5 > btc_ma20 else "低于"} MA20，{"说明短期趋势强于中期，是金叉状态" if btc_ma5 > btc_ma20 else "说明短期趋势弱于中期，是死叉状态"}。
            </p>
        </div>
        
        <div class="teaching-module">
            <h3 style="color: #1E90FF;">模块二：指标解读 - RSI 相对强弱指标</h3>
            <p><strong>RSI（Relative Strength Index）</strong>用于衡量价格的涨跌速度和幅度，判断市场是否超买或超卖。</p>
            <table style="width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 13px;">
                <tr style="background-color: #f2f9ff;">
                    <th style="border: 1px solid #e0e0e0; padding: 8px;">RSI 范围</th>
                    <th style="border: 1px solid #e0e0e0; padding: 8px;">市场状态</th>
                    <th style="border: 1px solid #e0e0e0; padding: 8px;">操作建议</th>
                </tr>
                <tr><td style="border: 1px solid #e0e0e0; padding: 8px; text-align: center;">70-100</td><td style="border: 1px solid #e0e0e0; padding: 8px; text-align: center;">超买区</td><td style="border: 1px solid #e0e0e0; padding: 8px; text-align: center;">考虑减仓</td></tr>
                <tr><td style="border: 1px solid #e0e0e0; padding: 8px; text-align: center;">50-70</td><td style="border: 1px solid #e0e0e0; padding: 8px; text-align: center;">偏强区</td><td style="border: 1px solid #e0e0e0; padding: 8px; text-align: center;">可继续持仓</td></tr>
                <tr><td style="border: 1px solid #e0e0e0; padding: 8px; text-align: center;">30-50</td><td style="border: 1px solid #e0e0e0; padding: 8px; text-align: center;">偏弱区</td><td style="border: 1px solid #e0e0e0; padding: 8px; text-align: center;">观望为主</td></tr>
                <tr><td style="border: 1px solid #e0e0e0; padding: 8px; text-align: center;">0-30</td><td style="border: 1px solid #e0e0e0; padding: 8px; text-align: center;">超卖区</td><td style="border: 1px solid #e0e0e0; padding: 8px; text-align: center;">考虑建仓</td></tr>
            </table>
            <p style="background-color: #e7f3ff; padding: 10px; border-radius: 4px; margin-top: 10px;">
                💡 <strong>今日应用：</strong>BTC 的 RSI 为 <strong>{btc_rsi}</strong>，处于{"偏强区，可继续持仓" if 50 <= btc_rsi < 70 else "超买区，注意风险" if btc_rsi >= 70 else "偏弱区，建议观望"}；AAPL 的 RSI 为 <strong>{aapl_rsi}</strong>。
            </p>
        </div>
        
        <div class="teaching-module">
            <h3 style="color: #1E90FF;">模块三：趋势判断 - 如何识别多头/空头趋势？</h3>
            <p>判断趋势是交易决策的核心。以下是识别趋势的三个关键方法：</p>
            <ul>
                <li><strong>高点与低点：</strong>多头趋势 = 高点创新高 + 低点抬高；空头趋势 = 低点创新低 + 高点降低</li>
                <li><strong>均线排列：</strong>多头排列 = 价格&gt;MA5&gt;MA20；空头排列 = 价格&lt;MA5&lt;MA20</li>
                <li><strong>趋势线：</strong>连接两个以上低点形成支撑线，连接两个以上高点形成压力线</li>
            </ul>
            <p style="background-color: #e7f3ff; padding: 10px; border-radius: 4px; margin-top: 10px;">
                💡 <strong>今日应用：</strong>BTC 近 30 天走势{"呈现多头趋势，高点和低点都在抬高" if btc_ma5 > btc_ma20 else "呈现震荡整理，方向不明确"}。建议结合成交量进一步确认。
            </p>
        </div>
        
        <div class="teaching-module">
            <h3 style="color: #1E90FF;">模块四：实战策略 - 支撑位与阻力位的画法</h3>
            <p>支撑位和阻力位是制定交易计划的重要参考：</p>
            <ul>
                <li><strong>支撑位画法：</strong>找到近期至少 2-3 个低点，连接成水平线或斜线</li>
                <li><strong>阻力位画法：</strong>找到近期至少 2-3 个高点，连接成水平线或斜线</li>
                <li><strong>突破确认：</strong>价格突破后需观察 3 天，站稳才能确认有效突破</li>
            </ul>
            <p style="background-color: #e7f3ff; padding: 10px; border-radius: 4px; margin-top: 10px;">
                💡 <strong>今日应用：</strong>根据 BTC 近 30 天数据，{"上方阻力位约在 " + str(round(btc_close * 1.05, 2)) + " 附近，下方支撑位约在 " + str(round(btc_close * 0.95, 2)) + " 附近" if btc_ma5 > btc_ma20 else "当前处于震荡区间，等待方向选择"}。
            </p>
        </div>
        
        <div class="teaching-module">
            <h3 style="color: #1E90FF;">模块五：风险管理 - 仓位控制与止损策略</h3>
            <p>风险管理是长期盈利的关键，以下是核心原则：</p>
            <ul>
                <li><strong>单笔风险：</strong>每笔交易亏损不超过总资金的 2%</li>
                <li><strong>仓位分配：</strong>单一资产不超过总仓位的 20%</li>
                <li><strong>止损设置：</strong>短线止损 5-8%，中线止损 10-15%</li>
                <li><strong>止盈策略：</strong>达到目标位后分批止盈，保留部分仓位博取更大收益</li>
            </ul>
            <p style="background-color: #fff3cd; padding: 10px; border-radius: 4px; margin-top: 10px; border-left: 3px solid #ffc107;">
                ⚠️ <strong>风险提示：</strong>当前 BTC RSI 为{btc_rsi}，{"处于偏高位置，建议控制仓位在 30% 以内" if btc_rsi > 60 else "处于合理区间，仓位可控制在 50% 左右" if btc_rsi > 40 else "处于偏低位置，可分批建仓"}。永远不要满仓操作！
            </p>
        </div>
    </div>
    
    <div class="disclaimer">
        ⚠️ 免责声明：本报告仅为技术分析参考，不构成任何投资建议。市场有风险，投资需谨慎。
    </div>
</body>
</html>"""
    
    # 保存到用户桌面
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = f"金融分析日报_{report_date}.html"
    local_path = os.path.join(desktop_path, filename)
    
    # 写入 HTML 文件（UTF-8 编码）
    os.makedirs(desktop_path, exist_ok=True)
    with open(local_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ 本地 HTML 报告已生成：{local_path}")
    return local_path, report_date, btc_close, btc_ma5, btc_ma20, btc_rsi, aapl_close, aapl_ma5, aapl_ma20, aapl_rsi


# ====================== 步骤 3：生成企业微信推送内容 ======================
def generate_markdown_content(local_path, report_date, btc_close, btc_ma5, btc_ma20, btc_rsi, aapl_close, aapl_ma5, aapl_ma20, aapl_rsi):
    """生成适配企业微信的 Markdown 推送内容（教学导向）"""
    report_time = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # 根据数据生成动态分析
    btc_trend = "震荡上行" if btc_ma5 > btc_ma20 else "震荡下行"
    btc_sentiment = "中性偏多" if btc_rsi > 55 else "中性偏空" if btc_rsi < 45 else "中性"
    aapl_trend = "稳步上涨" if aapl_close > 185 else "震荡整理"
    aapl_signal = "金叉" if aapl_ma5 > aapl_ma20 else "死叉"
    aapl_strength = "偏强" if aapl_ma5 > aapl_ma20 else "偏弱"
    overall_advice = "持仓为主" if btc_rsi < 70 and aapl_rsi < 70 else "谨慎观望"
    
    # 计算支撑阻力位
    btc_resistance = round(btc_close * 1.05, 2)
    btc_support = round(btc_close * 0.95, 2)
    
    # RSI 状态描述
    btc_rsi_status = "偏强区，可继续持仓" if 50 <= btc_rsi < 70 else "超买区，注意风险" if btc_rsi >= 70 else "偏弱区，建议观望"
    position_advice = "建议控制仓位在 30% 以内" if btc_rsi > 60 else "仓位可控制在 50% 左右" if btc_rsi > 40 else "可分批建仓"
    
    markdown_content = f"""# 📚 金融技术分析教学日报 - {report_date}
> 数据周期：近 30 天 | 生成时间：{report_time}

## 📊 今日核心数据
| 资产 | 最新价 | MA5/MA20 | RSI14 | 趋势 |
|------|--------|---------|-------|------|
| BTC/USDT | {btc_close} | {btc_ma5}/{btc_ma20} | {btc_rsi} | {btc_trend} |
| AAPL | {aapl_close} | {aapl_ma5}/{aapl_ma20} | {aapl_rsi} | {aapl_trend} |

---

## 📖 五大教学模块

### 模块一：MA 均线基础
**概念：** MA5 是过去 5 天平均价，MA20 是过去 20 天平均价
**金叉：** MA5 上穿 MA20 → 买入信号 | **死叉：** MA5 下穿 MA20 → 卖出信号
**今日应用：** BTC 的 MA5({btc_ma5}) {"高于" if btc_ma5 > btc_ma20 else "低于"} MA20({btc_ma20})，{"金叉状态，短期趋势强" if btc_ma5 > btc_ma20 else "死叉状态，短期趋势弱"}

### 模块二：RSI 指标解读
**超买区(70-100)：** 考虑减仓 | **偏强区(50-70)：** 可持仓 | **偏弱区(30-50)：** 观望 | **超卖区(0-30)：** 考虑建仓
**今日应用：** BTC 的 RSI={btc_rsi}，处于{btc_rsi_status}

### 模块三：趋势识别方法
**多头趋势：** 高点创新高 + 低点抬高 + 价格>MA5>MA20
**空头趋势：** 低点创新低 + 高点降低 + 价格<MA5<MA20
**今日应用：** BTC 近 30 天{"呈现多头趋势" if btc_ma5 > btc_ma20 else "震荡整理中"}

### 模块四：支撑位与阻力位
**画法：** 连接 2-3 个低点=支撑线 | 连接 2-3 个高点=阻力线
**突破确认：** 突破后观察 3 天，站稳才有效
**今日应用：** BTC 阻力位≈{btc_resistance}，支撑位≈{btc_support}

### 模块五：风险管理核心
⚠️ **单笔风险≤2%** | **单一资产≤20%** | **短线止损 5-8%** | **中线止损 10-15%**
**今日建议：** {position_advice}。永远不要满仓！

---

## 🔗 完整学习报告
详细图表和深入讲解已保存到桌面：`{local_path}`

> ⚠️ 免责声明：本报告仅为教学参考，不构成投资建议。市场有风险，投资需谨慎。""".strip()
    
    return markdown_content


# ====================== 步骤 4：推送至企业微信 ======================
def send_to_wework(report_date, btc_close, btc_ma5, btc_ma20, btc_rsi, aapl_close, aapl_ma5, aapl_ma20, aapl_rsi, local_path, minio_url=None):
    """推送报告到指定企业微信账号（使用 textcard 格式）"""
    
    # 计算趋势和状态
    btc_trend = "震荡上行" if btc_ma5 > btc_ma20 else "震荡下行"
    btc_signal = "金叉" if btc_ma5 > btc_ma20 else "死叉"
    btc_rsi_status = "偏强区" if 50 <= btc_rsi < 70 else "超买区" if btc_rsi >= 70 else "偏弱区"
    aapl_signal = "金叉" if aapl_ma5 > aapl_ma20 else "死叉"
    
    # 生成 HTML 描述内容
    description = f"""<div class="gray">{report_date} {time.strftime('%H:%M')}</div>
<div class="normal">
<strong>BTC/USDT</strong>: {btc_close} | MA5/MA20: {btc_ma5}/{btc_ma20} | RSI: {btc_rsi} | {btc_trend}({btc_signal})<br>
<strong>AAPL</strong>: {aapl_close} | MA5/MA20: {aapl_ma5}/{aapl_ma20} | RSI: {aapl_rsi} | {aapl_signal}<br>
<strong>RSI 状态</strong>: BTC 处于{btc_rsi_status}，建议关注仓位控制
</div>"""
    
    # 确定链接优先级：MinIO > 本地
    if minio_url:
        learn_url = minio_url
        description += """<div style='color: #1E90FF; margin-top: 8px; font-size: 12px;'>☁️ 完整报告已上传云端，点击按钮在线查看</div>"""
    else:
        learn_url = "https://kd.chatedu.jiaxutech.com/container/testuser001"  # 占位链接
        description += """<div style='color: #999; margin-top: 8px; font-size: 12px;'>📁 完整报告已保存到桌面，双击打开即可查看</div>"""
    
    # 构建 textcard 格式 payload
    payload = {
        "departmentId": 1,
        "msgType": "textcard",
        "title": f"【金融技术分析日报】{report_date}",
        "description": description,
        "learnUrl": learn_url,
        "btnText": "查看完整报告"
    }
    
    try:
        print("📤 正在推送报告到企业微信...")
        print(f"📋 推送内容：标题={payload['title']}")
        response = requests.post(
            url=API_URL,
            headers=HEADERS,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        
        # 打印推送结果
        print("\n=== 企业微信推送结果 ===")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        if result.get("code") == 200:
            print("\n🎉 报告推送成功！")
            print("📱 查看位置：企业微信 → 消息卡片")
            print("💡 桌面已生成带高清图表的 HTML 报告，双击即可打开")
            return result
        else:
            print(f"\n⚠️ 推送返回非 200 状态码：{result.get('code')}")
            return result
            
    except requests.exceptions.Timeout:
        print("\n❌ 推送超时：请检查网络连接")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"\n❌ HTTP 错误：{e}")
        print(f"  接口返回：{response.text if 'response' in locals() else '无'}")
        return None
    except Exception as e:
        print(f"\n❌ 推送异常：{str(e)}")
        return None


# ====================== 主流程（一键运行） ======================
def main():
    """主流程（一键运行）"""
    # 自动安装依赖包
    required_pkgs = ["requests", "pandas", "matplotlib", "numpy", "minio"]
    for pkg in required_pkgs:
        try:
            __import__(pkg)
        except ImportError:
            print(f"📌 正在安装 {pkg} 库...")
            os.system(f"pip install {pkg} -i https://pypi.tuna.tsinghua.edu.cn/simple")
    
    # 执行全流程
    try:
        # 1. 生成 HTML 报告
        local_path, report_date, btc_close, btc_ma5, btc_ma20, btc_rsi, aapl_close, aapl_ma5, aapl_ma20, aapl_rsi = generate_html_report()
        
        # 2. 上传到 MinIO
        minio_url = upload_to_minio(local_path)
        
        # 3. 推送企业微信（带 MinIO 链接）
        result = send_to_wework(report_date, btc_close, btc_ma5, btc_ma20, btc_rsi, aapl_close, aapl_ma5, aapl_ma20, aapl_rsi, local_path, minio_url)
        
        if result and result.get("code") == 200:
            print("\n✅ 全流程完成！")
            if minio_url:
                print(f"☁️ MinIO 链接：{minio_url}")
            return 0
        else:
            print("\n⚠️ 推送可能失败，请检查企业微信配置")
            return 1
            
    except Exception as e:
        print(f"\n❌ 程序执行失败：{str(e)}")
        print("💡 请检查依赖安装是否完成，或联系技术支持")
        return 1


if __name__ == "__main__":
    exit(main())

import pandas as pd
from xtquant import xtdata
import time
import sys
import datetime
import os
import traceback
import json
import threading

# 导入自定义文件操作模块
import fileOperation

# ==================== 控制事件 ====================
pause_event = threading.Event()   # 暂停标志
stop_event = threading.Event()    # 停止标志

def set_pause():
    """设置暂停标志"""
    pause_event.set()

def clear_pause():
    """清除暂停标志"""
    pause_event.clear()

def is_paused():
    """返回是否暂停"""
    return pause_event.is_set()

def set_stop():
    """设置停止标志"""
    stop_event.set()

def clear_stop():
    """清除停止标志"""
    stop_event.clear()

def is_stopped():
    """返回是否停止"""
    return stop_event.is_set()

# ==================== 进度推送配置 ====================
PROGRESS_INTERVAL = 1
MIN_PUSH_INTERVAL_SECONDS = 30
_last_push_time = None
_last_push_percent = -1

# 全局回调函数（由 monitor 设置）
_log_callback = None

def set_log_callback(callback):
    """设置日志回调函数，用于实时推送前端"""
    global _log_callback
    _log_callback = callback

def my_log(event, message):
    """
    输出结构化日志
    :param event: INFO, WARNING, ERROR, PROGRESS, FINAL, MISSING_FILE
    :param message: 日志内容
    """
    time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    log_message = f"[SKILL: QMT-ASTOCK-DATA] [{event}]：{time_str} {message}\n"

    # 总是输出到控制台（用于调试） - 使用编码安全的输出
    try:
        # 尝试UTF-8编码输出
        if hasattr(sys.stderr, 'buffer'):
            sys.stderr.buffer.write(log_message.encode('utf-8'))
            sys.stderr.flush()
        else:
            # 如果无法使用buffer，尝试安全输出
            safe_print(log_message)
    except Exception:
        try:
            # 备用方案：使用stdout
            safe_print(log_message)
        except Exception:
            # 最后手段：忽略编码错误
            try:
                # 尝试替换无法编码的字符
                safe_text = log_message.encode('ascii', 'ignore').decode('ascii', 'ignore')
                sys.stdout.write(safe_text)
            except Exception:
                pass

    # 如果设置了回调，则调用回调（用于前端更新）
    if _log_callback:
        _log_callback(event, message)

def safe_print(text):
    """编码安全的打印函数"""
    try:
        if hasattr(sys.stdout, 'buffer'):
            sys.stdout.buffer.write(text.encode('utf-8'))
            sys.stdout.flush()
        else:
            sys.stdout.write(text)
    except Exception:
        try:
            sys.stdout.write(text)
        except UnicodeEncodeError:
            safe_text = text.encode('ascii', 'replace').decode('ascii')
            sys.stdout.write(safe_text)

def send_progress_to_chat(progress_percent, processed, total, current_stock=None):
    """发送进度消息到前端（通过回调）"""
    global _last_push_time, _last_push_percent
    now = time.time()

    should_push = False
    if progress_percent - _last_push_percent >= PROGRESS_INTERVAL:
        should_push = True
    elif _last_push_time is None or (now - _last_push_time) >= MIN_PUSH_INTERVAL_SECONDS:
        if progress_percent > _last_push_percent:
            should_push = True

    if not should_push:
        return

    emoji = "📊"
    if progress_percent == 100:
        emoji = "✅"
    elif progress_percent >= 75:
        emoji = "🚀"
    elif progress_percent >= 50:
        emoji = "⏳"
    elif progress_percent >= 25:
        emoji = "📈"

    status_text = f"{emoji} 股票数据下载进度：{progress_percent}%\n已处理：{processed}/{total}\n"
    if current_stock:
        status_text += f"{current_stock}\n"

    if processed > 0 and _last_push_time:
        elapsed = now - _last_push_time
        if elapsed > 0:
            rate = processed / elapsed
            remaining = total - processed
            eta_seconds = remaining / rate if rate > 0 else 0
            if eta_seconds < 60:
                status_text += f"预计剩余：{int(eta_seconds)}秒"
            elif eta_seconds < 3600:
                status_text += f"预计剩余：{int(eta_seconds/60)}分钟"
            else:
                status_text += f"预计剩余：{int(eta_seconds/3600)}小时"

    safe_print(f"\n{status_text}\n")
    my_log("PROGRESS", status_text.replace("\n", " | "))

    _last_push_time = now
    _last_push_percent = progress_percent

# ==================== 编码修复 ====================
if sys.platform == "win32":
    try:
        os.environ["PYTHONIOENCODING"] = "utf-8"
        os.environ["PYTHONUTF8"] = "1"
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ==================== 全局路径配置 ====================
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

def load_config():
    """加载配置文件，如果不存在则创建默认配置"""
    default_config = {
        "descript": "需用户配置：系统输出目录，qmt xtltClient.exe所在目录",
        "base_path": "c:\\data\\",
        "qmt_path": "c:\\QMT\\bin.x64",
        "batch_size": 50,
        "progress_interval": 10,
        "min_push_interval_seconds": 30,
        "download_days": 500,
        "download_period": "1d",
        "k_data_subdir": "k_data",
        "host": "127.0.0.1",
        "port": 5000,
        "stock_list_filename": "stock_list.csv",
        "index_list_filename": "index_list.csv"
    }

    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        my_log("INFO", f"已创建默认配置文件: {CONFIG_FILE}")
        return default_config

    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
        config_changed = False
        for key, default_value in default_config.items():
            if key not in config:
                config[key] = default_value
                config_changed = True
        if config_changed:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            my_log("INFO", "配置文件已更新，添加缺失的配置项")
        return config
    except Exception as e:
        my_log("INFO", f"读取配置文件失败: {e}，使用默认配置")
        return default_config

config = load_config()

PROGRESS_INTERVAL = config.get("progress_interval", 10)
MIN_PUSH_INTERVAL_SECONDS = config.get("min_push_interval_seconds", 30)

BASE_PATH = config["base_path"]
DATA_DIR = BASE_PATH
if not os.path.exists(BASE_PATH):
    os.makedirs(BASE_PATH, exist_ok=True)

k_data_subdir = config.get("k_data_subdir", "k_data")
K_DATA_PATH = os.path.join(BASE_PATH, k_data_subdir)
if not os.path.exists(K_DATA_PATH):
    os.makedirs(K_DATA_PATH, exist_ok=True)

stock_list_filename = config.get("stock_list_filename", "stock_list.csv")
index_list_filename = config.get("index_list_filename", "index_list.csv")
STOCK_LIST_PATH = os.path.join(DATA_DIR, stock_list_filename)
INDEX_LIST_PATH = os.path.join(DATA_DIR, index_list_filename)

K_FOLDER = K_DATA_PATH

# ==================== 工具函数 ====================
def get_code_str(code):
    c = str(code).strip()
    if len(c) < 8:
        c = c.zfill(6)
        if c[0] == '6':
            c = c + '.SH'
        elif c[0] in ('3', '0'):
            c = c + '.SZ'
    return c

def format_stock_list(df):
    if df is None or df.empty:
        return None
    if 'symbol' in df.columns:
        df['代码'] = df['symbol'].apply(get_code_str)
    else:
        df['代码'] = df['代码'].apply(get_code_str)
    df['code'] = df['代码']
    df.set_index('code', drop=False, inplace=True)
    return df

def get_stock_list():
    if not fileOperation.if_exist(STOCK_LIST_PATH):
        my_log("MISSING_FILE", f"股票列表文件不存在：{STOCK_LIST_PATH}。请联系技术支持：微信名:quant_village_dog | QQ:13620658")
        return None
    df = fileOperation.read_csv(STOCK_LIST_PATH)
    if df is None or df.shape[0] == 0:
        my_log("ERROR", "股票列表为空。请联系技术支持：微信名:quant_village_dog | QQ:13620658")
        return None
    return format_stock_list(df)

def get_index_list():
    if not fileOperation.if_exist(INDEX_LIST_PATH):
        my_log("MISSING_FILE", f"指数列表文件不存在：{INDEX_LIST_PATH}。请联系技术支持：微信名:quant_village_dog | QQ:13620658")
        return None
    df = fileOperation.read_csv(INDEX_LIST_PATH)
    if df is None or df.shape[0] == 0:
        my_log("ERROR", "指数列表为空。请联系技术支持：微信名:quant_village_dog | QQ:13620658")
        return None
    return format_stock_list(df)

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def get_kline_save_path(code, period='1d'):
    period_map = {
        '1d': 'day',
        '1m': 'min1',
        '5m': 'min5',
        'tick': 'tick'
    }
    sub_dir = period_map.get(period, 'day')
    save_dir = os.path.join(K_FOLDER, sub_dir)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
    filename = f"{code}_{period}.csv" if period != '1d' else f"{code}_d.csv"
    return os.path.join(save_dir, filename)

def save_kline_to_csv(df, code, name, period='1d'):
    if df is None or df.empty:
        return
    if 'name' not in df.columns:
        df['name'] = name
    cols = ['code', 'name', 'time', 'open', 'high', 'low', 'close', 'volume', 'amount']
    df = df[cols].copy()
    save_path = get_kline_save_path(code, period)
    fileOperation.save_csv(df, save_path, overwrite=True)

def fetch_kline_data(stock_codes, period='1d', start_date='', end_date='', count=-1):
    if not stock_codes:
        return None
    if isinstance(stock_codes, str):
        stock_codes = [stock_codes]
    field_list_k = ['time', 'open', 'high', 'low', 'close', 'volume', 'amount']
    filed_list_tick = []
    if period != 'tick':
        field_list = field_list_k
    else:
        field_list = filed_list_tick
    if period in ['1m', '5m', '1d', 'tick']:
        per = period
    else:
        per = '1d'
    try:
        data_dict = xtdata.get_market_data_ex(field_list, stock_codes, per, start_date, end_date, count)
        if data_dict is None:
            return None
        result = {}
        for code in stock_codes:
            df = data_dict.get(code)
            if df is not None and not df.empty:
                result[code] = df
        return result
    except Exception as e:
        my_log("ERROR", f"获取数据异常：{e}\n{traceback.format_exc()}")
        return None

def download_single_stock_data(code, name, period='1d', days=300):
    end_date = datetime.datetime.now().strftime('%Y%m%d')
    start_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime('%Y%m%d')
    try:
        xtdata.download_history_data2([code], period, start_date, end_date)
        time.sleep(0.05)
    except Exception as e:
        my_log("WARNING", f"下载缓存失败：{code} - {e}")

    max_retries = 3
    for attempt in range(max_retries):
        data_dict = fetch_kline_data([code], period, start_date, end_date, count=-1)
        if data_dict and code in data_dict:
            df = data_dict[code]
            if df is not None and len(df) >= 3:
                df['time'] = pd.to_datetime(df['time'], unit='ms') + pd.Timedelta(hours=8)
                for col in ['open', 'high', 'low', 'close']:
                    df[col] = df[col].astype(float).round(2)
                df['volume'] = df['volume'].astype('int')
                df['amount'] = df['amount'].astype('int')
                df['code'] = code
                save_kline_to_csv(df, code, name, period)
                return True
        time.sleep(0.05)
    my_log("ERROR", f"下载失败：{code} {name}")
    return False

def process_batch(codes_with_names, period=None, days=None, batch_size=None,
                  start_date=None, end_date=None):
    if period is None:
        period = config.get("download_period", "1d")
    if days is None:
        days = config.get("download_days", 300)
    if batch_size is None:
        batch_size = config.get("batch_size", 50)
    if not codes_with_names:
        return 0

    codes = [item[0] for item in codes_with_names]
    name_dict = dict(codes_with_names)

    if end_date is None:
        end_date = datetime.datetime.now().strftime('%Y%m%d')
    if start_date is None:
        start_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime('%Y%m%d')

    # 批量下载缓存
    try:
        if period == '1d':
            xtdata.download_history_data2(codes, period, start_date, end_date)
        else:
            for code in codes:
                xtdata.download_history_data(code, period, start_date, end_date)
        time.sleep(0.05)
    except Exception as e:
        my_log("ERROR", f"批量下载缓存失败：{e}")
        return 0

    # 批量读取数据
    max_retries = 2
    data_dict = None
    for attempt in range(max_retries):
        data_dict = fetch_kline_data(codes, period, start_date, end_date, count=-1)
        if data_dict is not None:
            break
        time.sleep(0.05)

    if data_dict is None:
        my_log("ERROR", f"批次读取数据失败，重试{max_retries}次后放弃")
        return 0

    # 逐个保存
    success_count = 0
    for code in codes:
        # 检查停止标志
        if is_stopped():
            my_log("INFO", "收到停止信号，退出当前批次")
            break
        # 检查暂停标志
        while is_paused() and not is_stopped():
            time.sleep(0.1)

        df_new = data_dict.get(code)
        if df_new is None or df_new.empty:
            my_log("WARNING", f"股票 {code} 未获取到增量数据，跳过")
            success_count += 1
            continue

        df_new['time'] = pd.to_datetime(df_new['time'], unit='ms') + pd.Timedelta(hours=8)
        for col in ['open', 'high', 'low', 'close']:
            df_new[col] = df_new[col].astype(float).round(2)
        df_new['volume'] = df_new['volume'].astype('int')
        df_new['amount'] = df_new['amount'].astype('int')
        df_new['code'] = code
        df_new['name'] = name_dict[code]

        file_path = get_kline_save_path(code, period)
        df_old = None
        if fileOperation.if_exist(file_path):
            try:
                df_old = fileOperation.read_csv(file_path)
                if df_old is not None and not df_old.empty:
                    df_old['time'] = pd.to_datetime(df_old['time'])
            except Exception as e:
                my_log("WARNING", f"读取历史文件 {file_path} 失败：{e}")

        if df_old is not None and not df_old.empty:
            df_combined = pd.concat([df_old, df_new], ignore_index=True)
            df_combined.drop_duplicates(subset=['time'], keep='last', inplace=True)
            df_combined.sort_values('time', inplace=True)
        else:
            df_combined = df_new.sort_values('time')

        cols = ['code', 'name', 'time', 'open', 'high', 'low', 'close', 'volume', 'amount']
        df_combined = df_combined[cols]
        fileOperation.save_csv(df_combined, file_path, overwrite=True)
        success_count += 1

    return success_count

def download_all_data(period=None, days=None, batch_size=None):
    """主入口函数，支持暂停和停止"""
    # 清除之前的停止标志
    clear_stop()
    clear_pause()

    if period is None:
        period = config.get("download_period", "1d")
    if days is None:
        days = config.get("download_days", 500)
    if batch_size is None:
        batch_size = config.get("batch_size", 50)

    my_log("INFO", "开始执行数据下载任务")

    # 检查 MiniQMT 连接
    try:
        test = xtdata.get_market_data_ex([], ['000001.SZ'], '1d', '', '', 1)
        if test is None or '000001.SZ' not in test:
            my_log("ERROR", "MiniQMT 连接失败，请确保客户端已启动并登录")
            return
    except Exception as e:
        my_log("ERROR", f"连接测试异常：{e}")
        return

    # 读取股票和指数列表
    stocks = get_stock_list()
    indices = get_index_list()
    all_items = []
    if stocks is not None:
        all_items.extend([(row['代码'], row['名称']) for _, row in stocks.iterrows()])
    else:
        my_log("MISSING_FILE", "股票列表文件丢失，任务终止。请联系技术支持：微信名:quant_village_dog | QQ:13620658")
        return

    if indices is not None:
        all_items.extend([(row['代码'], row['名称']) for _, row in indices.iterrows()])
    else:
        my_log("MISSING_FILE", "指数列表文件丢失，任务终止。请联系技术支持：微信名:quant_village_dog | QQ:13620658")
        return

    if not all_items:
        my_log("MISSING_FILE", "没有可用的股票或指数列表，任务终止。请联系技术支持：微信名:quant_village_dog | QQ:13620658")
        return

    total = len(all_items)
    my_log("INFO", f"共需处理 {total} 个项目（股票+指数）")

    # 确定增量下载起始日期
    today = datetime.datetime.now().date()
    today_str = today.strftime('%Y%m%d')
    start_date = None

    if today.day == 1:
        my_log("INFO", "每月1日执行完整下载")
        start_date = (today - datetime.timedelta(days=days)).strftime('%Y%m%d')
    else:
        index_codes = ['000001.SH', '399001.SZ']
        last_dates = []
        for code in index_codes:
            file_path = get_kline_save_path(code, period)
            if fileOperation.if_exist(file_path):
                try:
                    df = fileOperation.read_csv(file_path)
                    if df is not None and not df.empty:
                        last_time = pd.to_datetime(df['time']).max()
                        last_dates.append(last_time.date())
                except Exception as e:
                    my_log("WARNING", f"读取指数文件 {code} 失败：{e}")
        if last_dates:
            base_date = max(last_dates)
            if base_date < today:
                start_date = (base_date + datetime.timedelta(days=1)).strftime('%Y%m%d')
                my_log("INFO", f"指数文件最后交易日为 {base_date}，将下载 {start_date} 至 {today_str} 的数据")
            else:
                my_log("INFO", "指数文件已包含今日数据，无需更新")
                my_log("INFO", f"批次完成：{total}/{total} (100%) - 所有数据已是最新")
                send_progress_to_chat(100, total, total, "所有数据已是最新，无需更新")
                completion_msg = f"✅ 数据已是最新，无需下载！\n已检查：{total}/{total} 个项目\n任务结束时间：{datetime.datetime.now().strftime('%H:%M:%S')}"
                safe_print(f"\n{completion_msg}\n")
                my_log("FINAL", completion_msg.replace("\n", " | "))
                return
        else:
            my_log("WARNING", "未能从指数文件获取有效日期，将使用完整回溯下载")

    if start_date is None:
        start_date = (today - datetime.timedelta(days=days)).strftime('%Y%m%d')
        my_log("INFO", f"使用完整回溯：从 {start_date} 至 {today_str} 下载数据")

    processed = 0
    for i in range(0, total, batch_size):
        # 检查停止标志
        if is_stopped():
            my_log("INFO", "收到停止信号，任务提前结束")
            break

        # 检查暂停标志
        while is_paused() and not is_stopped():
            time.sleep(0.1)

        batch = all_items[i:i + batch_size]
        batch_names = [item[1] for item in batch]
        batch_display = "、".join(batch_names[:20])
        if len(batch_names) > 20:
            batch_display += f" 等{len(batch_names)}只"

        success_in_batch = process_batch(batch, period, days, batch_size,
                                         start_date=start_date, end_date=today_str)
        processed += success_in_batch

        progress = int((processed / total) * 100)
        my_log("PROGRESS", f"{progress}")
        my_log("INFO", f"批次完成：{processed}/{total} ({progress}%) - 本批：{batch_display}")
        send_progress_to_chat(progress, processed, total, f"本批次：{batch_display}")

    if is_stopped():
        completion_msg = f"⏹️ 数据下载任务被手动停止！\n成功处理：{processed}/{total} 个项目"
    else:
        completion_msg = f"✅ 数据下载任务完成！\n成功处理：{processed}/{total} 个项目\n任务结束时间：{datetime.datetime.now().strftime('%H:%M:%S')}"

    safe_print(f"\n{completion_msg}\n")
    my_log("FINAL", completion_msg.replace("\n", " | "))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='下载股票日线数据')
    parser.add_argument('--period', type=str, default='1d', help='数据周期，如 1d、1m')
    parser.add_argument('--days', type=int, default=500, help='回溯天数')
    parser.add_argument('--batch_size', type=int, default=50, help='每批处理的股票数量')
    args = parser.parse_args()
    download_all_data(period=args.period, days=args.days, batch_size=args.batch_size)
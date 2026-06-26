# -*- coding: utf-8 -*-
"""
主程序 - 天津安信华瑞 拓安气体监测设备
版本：2026.3.26 定制版

功能:
- 读取 Modbus 传感器数据
- 上报数据到云平台
- 支持 OTA 升级
- 看门狗保护

运行平台：移远 QuecPython
"""
import utime
import gc
import machine

# 导入自定义模块
import sys
sys.path.append('/usr')  # 确保模块路径

from led_control import LED
from modbus_rtu import ModbusRTU
from sensor_device import SensorManager
from network_manager import NetworkManager
from system_manager import SystemManager
from data_reporter import DataReporter

# 导入配置
from config import (
    MODBUS_UART, MODBUS_BAUDRATE, MODBUS_DATABITS, MODBUS_PARITY,
    MODBUS_STOPBIT, MODBUS_FLOWCTL,
    URL_OTA, URL_REPORT,
    LED_NET_PIN, LED_MODBUS_PIN,
    MANUFACTURER_NAME, TERMINAL_TYPE, PROJECT_NAME, PROJECT_VERSION,
    MANUFACTURER_ID, SAAS_VERSION,
    MODBUS_RETRY_MAX, HTTP_RETRY_MAX, REPORT_INTERVAL_SEC,
    DEBUG_ENABLE
)


# ==================== 全局变量 ====================
g_net_info = None              # 网络信息缓存
g_last_report_minute = -1      # 上次上报分钟
g_work_day = -1                # 上次工作日期
g_server_fail_count = 0        # 服务器失败次数
g_modbus_error = 0             # Modbus 错误标志


def print_banner():
    """打印设备启动信息"""
    print("=" * 60)
    print("  天津安信华瑞科技有限公司")
    print("  拓安气体监测设备")
    print("=" * 60)
    print("项目名称:", PROJECT_NAME)
    print("项目版本:", PROJECT_VERSION)
    print("联系电话:", MANUFACTURER_ID)
    print("=" * 60)


def init_hardware():
    """
    初始化硬件
    
    返回:
        tuple: (led_net, led_modbus, modbus)
    """
    print("初始化硬件...")
    
    # 初始化 LED
    led_net = LED(LED_NET_PIN)
    led_modbus = LED(LED_MODBUS_PIN)
    
    # 初始化 Modbus
    modbus = ModbusRTU(
        uart_num=MODBUS_UART,
        baudrate=MODBUS_BAUDRATE,
        databits=MODBUS_DATABITS,
        parity=MODBUS_PARITY,
        stopbits=MODBUS_STOPBIT,
        flowctl=MODBUS_FLOWCTL
    )
    
    print("  LED 初始化完成：网络灯=GPIO{}, Modbus 灯=GPIO{}".format(
        LED_NET_PIN, LED_MODBUS_PIN))
    print("  Modbus 初始化完成：UART{}, 波特率={}".format(
        MODBUS_UART, MODBUS_BAUDRATE))
    
    return led_net, led_modbus, modbus


def init_network():
    """
    初始化网络
    
    返回:
        tuple: (net_mgr, net_info)
    """
    print("初始化网络...")
    net_mgr = NetworkManager(PROJECT_NAME, PROJECT_VERSION)
    
    print("正在连接移动网络...")
    if net_mgr.wait_connected(60):
        print("网络连接成功")
        net_mgr.sync_time()
        net_info = net_mgr.get_network_info()
        
        if net_info:
            print("  IMEI:", net_info.get('IMEI', 'N/A'))
            print("  信号强度:", net_info.get('signal_power', 'N/A'))
            return net_mgr, net_info
    else:
        print("网络连接失败")
    
    return None, None


def modbus_task(modbus, sensor_mgr, sys_mgr, led_modbus):
    """
    Modbus 数据采集任务
    
    参数:
        modbus: Modbus 引擎
        sensor_mgr: 传感器管理器
        sys_mgr: 系统管理器
        led_modbus: Modbus LED
        
    返回:
        tuple: (sensor_stat, sensor_dens, sys_stat)
    """
    global g_modbus_error
    
    if g_modbus_error > 0:
        print("[警告] Modbus 通信错误，尝试恢复...", utime.localtime())
        led_modbus.flash(0.1, 0.1, 3)
        utime.sleep(0.3)
        g_modbus_error = 0
    
    # 读取电池状态
    print("[1/3] 读取电池状态...")
    battery_stat = sys_mgr.read_battery_status(modbus)
    print("  电池状态:", battery_stat)
    
    # 扫描传感器
    print("[2/3] 扫描传感器...")
    sensor_stat = sensor_mgr.scan_sensors()
    print("  在线传感器数量:", len(sensor_stat))
    
    # 读取浓度
    print("[3/3] 读取传感器浓度...")
    sensor_dens = sensor_mgr.read_all_density(sensor_stat)
    print("  浓度数据数量:", len(sensor_dens))
    
    # 构建系统状态
    sys_stat = sys_mgr.build_sys_stat(battery_stat, sensor_stat)
    
    # 检查报警和故障
    has_alarm, has_fail, gas_state = sensor_mgr.get_alarm_status(sensor_stat)
    sys_stat['has_alarm'] = has_alarm
    sys_stat['has_fail'] = has_fail
    
    print("[完成] 数据采集完成")
    print("  报警状态:", "有" if has_alarm else "无")
    print("  故障状态:", "有" if has_fail else "无")
    print("  气体状态:", gas_state)
    
    return sensor_stat, sensor_dens, sys_stat


def report_task(net_mgr, reporter, sys_mgr, sensor_stat, sensor_dens, sys_stat):
    """
    数据上报任务
    
    参数:
        net_mgr: 网络管理器
        reporter: 数据上报器
        sys_mgr: 系统管理器
        sensor_stat: 传感器状态
        sensor_dens: 传感器浓度
        sys_stat: 系统状态
        
    返回:
        bool: 上报成功返回 True
    """
    global g_net_info, g_server_fail_count
    
    # 检查网络
    if not net_mgr.is_connected():
        print("[警告] 网络未连接，重新连接...")
        net_mgr.wait_connected(30)
        g_net_info = net_mgr.get_network_info()
    
    if not g_net_info:
        print("[错误] 网络信息获取失败")
        return False
    
    # 上报数据
    print("[上报] 发送传感器数据...")
    result = reporter.report_sensor_data(g_net_info, sensor_stat, sensor_dens, sys_stat)
    
    if result == 0:
        g_server_fail_count = 0
        print("[成功] 数据上报成功")
        return True
    else:
        g_server_fail_count += 1
        print("[失败] 上报失败，失败次数:", g_server_fail_count)
        
        # 重试一次
        if g_server_fail_count <= HTTP_RETRY_MAX:
            print("[重试] 重新上报...")
            result = reporter.report_sensor_data(g_net_info, sensor_stat, sensor_dens, sys_stat)
            if result == 0:
                g_server_fail_count = 0
                print("[成功] 重试成功")
                return True
        
        # 多次失败后重启
        if g_server_fail_count > 5:
            print("[严重] 服务器连续失败，准备重启...")
            Power.powerRestart()
        
        return False


def daily_check(net_mgr, reporter):
    """
    每日检查任务 (网络检查和 OTA)
    
    参数:
        net_mgr: 网络管理器
        reporter: 数据上报器
    """
    global g_net_info
    
    print("[每日检查] 执行日常检查...")
    
    # 重新检查网络
    g_net_info = net_mgr.get_network_info()
    
    if g_net_info:
        # 上报启动信息 (触发 OTA 检查)
        reporter.report_boot_info(
            g_net_info,
            MANUFACTURER_NAME,
            TERMINAL_TYPE,
            PROJECT_NAME,
            PROJECT_VERSION
        )


def main():
    """主函数"""
    global g_net_info, g_last_report_minute, g_work_day, g_server_fail_count
    
    try:
        # 打印启动信息
        print_banner()
        utime.sleep(2)
        
        # 初始化硬件
        led_net, led_modbus, modbus = init_hardware()
        
        # 初始化传感器管理器
        print("初始化传感器管理器...")
        sensor_mgr = SensorManager(modbus, max_count=32)
        
        # 初始化系统管理器
        print("初始化系统管理器...")
        sys_mgr = SystemManager()
        
        # 初始化网络
        net_mgr, g_net_info = init_network()
        
        if not g_net_info:
            print("[严重] 网络初始化失败，等待重启...")
            led_net.flash(0.1, 0.1, 5)
            utime.sleep(5)
            from misc import Power
            Power.powerRestart()
            return
        
        # 初始化数据上报器
        print("初始化数据上报器...")
        reporter = DataReporter(URL_REPORT, URL_OTA, led_net)
        
        # 记录启动时间
        boot_time = utime.localtime()
        print("系统启动时间:", boot_time)
        g_work_day = boot_time[2]
        
        # 计算 IMEI 尾数 (用于错时上报)
        imei_tail = int(g_net_info['IMEI']) % 10000
        print("IMEI 尾数:", imei_tail)
        
        # 启用 GC
        gc.enable()
        
        # 主循环
        print("进入主循环...")
        print("上报间隔:", REPORT_INTERVAL_SEC, "秒")
        print("-" * 60)
        
        while True:
            now_time = utime.localtime()
            now_ts = utime.mktime(now_time)
            now_minute = now_time[4]
            current_day = now_time[2]
            
            # 喂看门狗
            sys_mgr.feed_dog()
            
            # 每日检查 (日期变化时)
            if current_day != g_work_day:
                daily_check(net_mgr, reporter)
                g_work_day = current_day
            
            # 检查是否需要上报 (每分钟检查一次)
            if now_minute != g_last_report_minute:
                print("")
                print(">>> 开始数据采集周期 [{}:{}:{}] <<<".format(
                    now_time[3], now_time[4], now_time[5]))
                
                # 执行 Modbus 采集
                sensor_stat, sensor_dens, sys_stat = modbus_task(
                    modbus, sensor_mgr, sys_mgr, led_modbus
                )
                
                # 喂狗
                sys_mgr.feed_dog()
                
                # 数据上报
                success = report_task(
                    net_mgr, reporter, sys_mgr,
                    sensor_stat, sensor_dens, sys_stat
                )
                
                if success:
                    g_last_report_minute = now_minute
                    print(">>> 上报成功，下次上报时间:", now_minute + 1, "分钟 <<<")
                else:
                    print(">>> 上报失败，下个周期重试 <<<")
            
            # 等待
            utime.sleep(10)
            
    except KeyboardInterrupt:
        print("\n[中断] 程序被用户中断")
    except Exception as e:
        print("\n[异常] 程序异常:", e)
        import sys
        sys.print_exception(e)
        print("准备重启...")
        from misc import Power
        utime.sleep(2)
        Power.powerRestart()


# 程序入口
if __name__ == "__main__":
    main()

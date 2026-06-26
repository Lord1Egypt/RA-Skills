#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
江苏海事局会议查询自动化脚本
版本: 1.0.0
功能: 自动登录综合平台，查询会议信息并导出为Excel
作者: Auto-generated
"""

import os
import sys
import time
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import json
import logging

# 第三方库导入
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait, Select
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
except ImportError as e:
    print("错误: 缺少必要的依赖库，请先运行: pip install selenium pandas openpyxl webdriver-manager")
    sys.exit(1)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('meeting_query.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MeetingQueryBot:
    """江苏海事局会议查询自动化机器人"""
    
    def __init__(self, headless: bool = False):
        """
        初始化浏览器驱动
        
        Args:
            headless: 是否使用无头模式（不显示浏览器界面）
        """
        self.base_url = "http://gchportal.js-msa.gov.cn/cas/login"
        self.username = os.getenv("MSA_USERNAME", "lp@njmsa")
        self.password = os.getenv("MSA_PASSWORD", "@lp280033")
        
        # 配置Chrome选项
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # 设置中文语言
        chrome_options.add_argument("--lang=zh-CN")
        
        # 初始化WebDriver
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 20)
            logger.info("Chrome WebDriver初始化成功")
        except Exception as e:
            logger.error(f"WebDriver初始化失败: {e}")
            raise
    
    def login(self) -> bool:
        """
        登录综合平台
        
        Returns:
            bool: 登录是否成功
        """
        try:
            logger.info(f"访问登录页面: {self.base_url}")
            self.driver.get(self.base_url)
            time.sleep(2)
            
            # 等待登录表单加载
            username_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username'], input[type='text']"))
            )
            password_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='password'], input[type='password']")
            
            # 输入用户名和密码
            username_input.clear()
            username_input.send_keys(self.username)
            logger.info("已输入用户名")
            
            password_input.clear()
            password_input.send_keys(self.password)
            logger.info("已输入密码")
            
            # 查找并点击登录按钮
            login_button_selectors = [
                "button[type='submit']",
                "input[type='submit']",
                ".login-btn",
                "button:contains('登录')",
                "input[value='登录']"
            ]
            
            login_button = None
            for selector in login_button_selectors:
                try:
                    if ":contains" in selector:
                        # 处理文本包含选择器
                        elements = self.driver.find_elements(By.TAG_NAME, "button")
                        for element in elements:
                            if "登录" in element.text:
                                login_button = element
                                break
                    else:
                        login_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if login_button:
                        break
                except:
                    continue
            
            if login_button:
                login_button.click()
                logger.info("已点击登录按钮")
            else:
                # 如果找不到按钮，尝试按回车键
                password_input.send_keys(Keys.RETURN)
                logger.info("通过回车键尝试登录")
            
            # 等待登录成功，检查是否有欢迎信息或跳转
            time.sleep(3)
            
            # 检查是否登录成功
            if "cas/login" not in self.driver.current_url:
                logger.info("登录成功，已跳转到主页面")
                return True
            else:
                # 检查是否有错误信息
                try:
                    error_msg = self.driver.find_element(By.CSS_SELECTOR, ".error-msg, .alert-danger").text
                    logger.error(f"登录失败: {error_msg}")
                except:
                    logger.error("登录失败，可能账号密码错误或页面结构有变化")
                return False
                
        except Exception as e:
            logger.error(f"登录过程中发生错误: {e}")
            return False
    
    def navigate_to_meeting_query(self) -> bool:
        """
        导航到会议查询页面
        
        Returns:
            bool: 导航是否成功
        """
        try:
            logger.info("开始导航到会议查询页面")
            
            # 步骤1: 点击"政务系统"（会打开新标签页）
            gov_system_selectors = [
                "a:contains('政务系统')",
                "li:contains('政务系统')",
                "span:contains('政务系统')",
                "*[onclick*='政务系统']"
            ]
            
            gov_link = None
            for selector in gov_system_selectors:
                try:
                    if ":contains" in selector:
                        elements = self.driver.find_elements(By.TAG_NAME, "a")
                        for element in elements:
                            if "政务系统" in element.text:
                                gov_link = element
                                break
                        if not gov_link:
                            elements = self.driver.find_elements(By.TAG_NAME, "li")
                            for element in elements:
                                if "政务系统" in element.text:
                                    gov_link = element.find_element(By.TAG_NAME, "a")
                                    break
                    else:
                        gov_link = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if gov_link:
                        break
                except:
                    continue
            
            if not gov_link:
                logger.error("找不到'政务系统'链接")
                return False
            
            gov_link.click()
            logger.info("已点击'政务系统'")
            time.sleep(2)
            
            # 切换到新打开的标签页
            original_window = self.driver.current_window_handle
            for window_handle in self.driver.window_handles:
                if window_handle != original_window:
                    self.driver.switch_to.window(window_handle)
                    logger.info("已切换到政务系统新标签页")
                    break
            
            time.sleep(3)
            
            # 步骤2: 点击"行政办公"
            admin_office_selectors = [
                "a:contains('行政办公')",
                "li:contains('行政办公')",
                "#adminOffice"
            ]
            
            admin_link = None
            for selector in admin_office_selectors:
                try:
                    if ":contains" in selector:
                        elements = self.driver.find_elements(By.TAG_NAME, "a")
                        for element in elements:
                            if "行政办公" in element.text:
                                admin_link = element
                                break
                    else:
                        admin_link = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if admin_link:
                        break
                except:
                    continue
            
            if admin_link:
                admin_link.click()
                logger.info("已点击'行政办公'")
                time.sleep(2)
            else:
                logger.warning("未找到'行政办公'链接，尝试继续")
            
            # 步骤3: 点击"会议管理" -> "全局会议查询"
            meeting_selectors = [
                "a:contains('会议管理')",
                "li:contains('会议管理')",
                "*[onclick*='会议管理']"
            ]
            
            meeting_link = None
            for selector in meeting_selectors:
                try:
                    if ":contains" in selector:
                        elements = self.driver.find_elements(By.TAG_NAME, "a")
                        for element in elements:
                            if "会议管理" in element.text:
                                meeting_link = element
                                break
                    else:
                        meeting_link = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if meeting_link:
                        break
                except:
                    continue
            
            if meeting_link:
                meeting_link.click()
                logger.info("已点击'会议管理'")
                time.sleep(2)
                
                # 尝试查找并点击"全局会议查询"
                global_meeting_selectors = [
                    "a:contains('全局会议查询')",
                    "li:contains('全局会议查询')"
                ]
                
                global_link = None
                for selector in global_meeting_selectors:
                    try:
                        if ":contains" in selector:
                            elements = self.driver.find_elements(By.TAG_NAME, "a")
                            for element in elements:
                                if "全局会议查询" in element.text:
                                    global_link = element
                                    break
                        else:
                            global_link = self.driver.find_element(By.CSS_SELECTOR, selector)
                        if global_link:
                            break
                    except:
                        continue
                
                if global_link:
                    global_link.click()
                    logger.info("已进入'全局会议查询'页面")
                else:
                    logger.info("已在会议管理页面，继续执行查询")
            else:
                logger.warning("未找到'会议管理'链接，尝试直接查找查询界面")
            
            time.sleep(3)
            return True
            
        except Exception as e:
            logger.error(f"导航到会议查询页面失败: {e}")
            return False
    
    def query_meetings(self, start_date: str, end_date: str = None) -> List[Dict]:
        """
        查询指定日期范围内的会议
        
        Args:
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)，默认为开始日期
            
        Returns:
            List[Dict]: 会议信息列表
        """
        if end_date is None:
            end_date = start_date
        
        meetings = []
        try:
            logger.info(f"开始查询会议: {start_date} 到 {end_date}")
            
            # 步骤1: 选择单位"江苏海事局局机关"
            try:
                # 尝试多种方式查找单位选择框
                unit_selectors = [
                    "select[name*='unit']",
                    "select[name*='dept']",
                    "select[name*='department']",
                    "select[id*='unit']",
                    "#unitSelect"
                ]
                
                unit_select = None
                for selector in unit_selectors:
                    try:
                        unit_select = Select(self.driver.find_element(By.CSS_SELECTOR, selector))
                        logger.info(f"找到单位选择框: {selector}")
                        break
                    except:
                        continue
                
                if unit_select:
                    # 选择"江苏海事局局机关"
                    try:
                        unit_select.select_by_visible_text("江苏海事局局机关")
                        logger.info("已选择'江苏海事局局机关'")
                    except:
                        # 尝试通过值选择
                        try:
                            unit_select.select_by_value("江苏海事局局机关")
                        except:
                            # 尝试通过索引选择
                            for option in unit_select.options:
                                if "江苏海事局局机关" in option.text:
                                    option.click()
                                    break
                else:
                    logger.warning("未找到单位选择框，可能页面结构不同")
            except Exception as e:
                logger.warning(f"选择单位时出错: {e}")
            
            # 步骤2: 输入开始时间
            try:
                start_date_selectors = [
                    "input[name*='startDate']",
                    "input[name*='startTime']",
                    "input[placeholder*='开始时间']",
                    "#startDate"
                ]
                
                start_date_input = None
                for selector in start_date_selectors:
                    try:
                        start_date_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                        logger.info(f"找到开始时间输入框: {selector}")
                        break
                    except:
                        continue
                
                if start_date_input:
                    # 清空并输入开始日期
                    start_date_input.clear()
                    start_date_input.send_keys(start_date)
                    logger.info(f"已输入开始时间: {start_date}")
            except Exception as e:
                logger.warning(f"输入开始时间时出错: {e}")
            
            # 步骤3: 输入结束时间
            try:
                end_date_selectors = [
                    "input[name*='endDate']",
                    "input[name*='endTime']",
                    "input[placeholder*='结束时间']",
                    "#endDate"
                ]
                
                end_date_input = None
                for selector in end_date_selectors:
                    try:
                        end_date_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                        logger.info(f"找到结束时间输入框: {selector}")
                        break
                    except:
                        continue
                
                if end_date_input:
                    # 清空并输入结束日期
                    end_date_input.clear()
                    end_date_input.send_keys(end_date)
                    logger.info(f"已输入结束时间: {end_date}")
            except Exception as e:
                logger.warning(f"输入结束时间时出错: {e}")
            
            # 步骤4: 点击搜索按钮
            try:
                search_button_selectors = [
                    "button:contains('搜索')",
                    "input[value='搜索']",
                    "button[type='submit']",
                    ".search-btn",
                    "#searchBtn"
                ]
                
                search_button = None
                for selector in search_button_selectors:
                    try:
                        if ":contains" in selector:
                            elements = self.driver.find_elements(By.TAG_NAME, "button")
                            for element in elements:
                                if "搜索" in element.text:
                                    search_button = element
                                    break
                            if not search_button:
                                elements = self.driver.find_elements(By.TAG_NAME, "input")
                                for element in elements:
                                    if element.get_attribute("value") and "搜索" in element.get_attribute("value"):
                                        search_button = element
                                        break
                        else:
                            search_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                        if search_button:
                            break
                    except:
                        continue
                
                if search_button:
                    search_button.click()
                    logger.info("已点击搜索按钮")
                else:
                    # 尝试通过回车键触发搜索
                    if end_date_input:
                        end_date_input.send_keys(Keys.RETURN)
                        logger.info("通过回车键触发搜索")
            except Exception as e:
                logger.warning(f"点击搜索按钮时出错: {e}")
            
            # 等待搜索结果加载
            time.sleep(3)
            
            # 步骤5: 解析会议数据
            try:
                # 尝试多种表格选择器
                table_selectors = [
                    "table",
                    ".table",
                    "#dataTable",
                    ".ant-table",
                    ".el-table"
                ]
                
                meetings_table = None
                for selector in table_selectors:
                    try:
                        meetings_table = self.driver.find_element(By.CSS_SELECTOR, selector)
                        # 检查表格是否有数据
                        rows = meetings_table.find_elements(By.TAG_NAME, "tr")
                        if len(rows) > 1:  # 至少有表头和数据行
                            logger.info(f"找到会议表格: {selector}，共{len(rows)-1}行数据")
                            break
                    except:
                        continue
                
                if meetings_table:
                    # 提取表头
                    headers = []
                    header_row = meetings_table.find_element(By.TAG_NAME, "tr")
                    header_cells = header_row.find_elements(By.TAG_NAME, "th")
                    if not header_cells:
                        header_cells = header_row.find_elements(By.TAG_NAME, "td")
                    
                    for cell in header_cells:
                        headers.append(cell.text.strip())
                    
                    logger.info(f"表头: {headers}")
                    
                    # 提取数据行
                    rows = meetings_table.find_elements(By.TAG_NAME, "tr")
                    for i, row in enumerate(rows[1:], 1):  # 跳过表头
                        try:
                            cells = row.find_elements(By.TAG_NAME, "td")
                            if len(cells) >= 6:  # 至少有6个字段
                                meeting_data = {
                                    "日期": cells[0].text.strip() if len(cells) > 0 else "",
                                    "开始时间": cells[1].text.strip() if len(cells) > 1 else "",
                                    "会议标题": cells[2].text.strip() if len(cells) > 2 else "",
                                    "会议地点": cells[3].text.strip() if len(cells) > 3 else "",
                                    "出席人员": cells[4].text.strip() if len(cells) > 4 else "",
                                    "主办部门": cells[5].text.strip() if len(cells) > 5 else "",
                                    "行号": i
                                }
                                meetings.append(meeting_data)
                                logger.debug(f"提取到会议: {meeting_data['会议标题']}")
                        except Exception as row_error:
                            logger.warning(f"解析第{i}行时出错: {row_error}")
                
                if not meetings:
                    logger.info("未找到表格数据，尝试其他数据提取方式")
                    # 尝试通过类名或ID查找会议项
                    meeting_item_selectors = [
                        ".meeting-item",
                        ".conference-item",
                        "[class*='meeting']",
                        "[class*='conference']"
                    ]
                    
                    for selector in meeting_item_selectors:
                        try:
                            items = self.driver.find_elements(By.CSS_SELECTOR, selector)
                            if items:
                                logger.info(f"找到{len(items)}个会议项")
                                for item in items:
                                    try:
                                        # 尝试从每个项目中提取信息
                                        title_elem = item.find_element(By.CSS_SELECTOR, ".title, .meeting-title, h4, h5")
                                        time_elem = item.find_element(By.CSS_SELECTOR, ".time, .meeting-time, .date")
                                        
                                        meeting_data = {
                                            "日期": time_elem.text.strip() if time_elem else "",
                                            "开始时间": "",
                                            "会议标题": title_elem.text.strip() if title_elem else "",
                                            "会议地点": "",
                                            "出席人员": "",
                                            "主办部门": ""
                                        }
                                        meetings.append(meeting_data)
                                    except:
                                        continue
                                break
                        except:
                            continue
                            
            except Exception as e:
                logger.error(f"解析会议数据时出错: {e}")
            
            logger.info(f"共查询到{len(meetings)}条会议记录")
            return meetings
            
        except Exception as e:
            logger.error(f"查询会议过程中发生错误: {e}")
            return meetings
    
    def export_to_excel(self, meetings: List[Dict], output_path: str = None) -> str:
        """
        导出会议数据到Excel
        
        Args:
            meetings: 会议数据列表
            output_path: 输出文件路径，默认为当前目录
            
        Returns:
            str: 输出文件路径
        """
        if not meetings:
            logger.warning("没有会议数据可导出")
            return ""
        
        if output_path is None:
            # 生成默认文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"海事局会议查询_{timestamp}.xlsx"
        
        try:
            # 转换为DataFrame
            df = pd.DataFrame(meetings)
            
            # 重新排列列顺序
            column_order = ["日期", "开始时间", "会议标题", "会议地点", "出席人员", "主办部门"]
            existing_columns = [col for col in column_order if col in df.columns]
            other_columns = [col for col in df.columns if col not in column_order]
            df = df[existing_columns + other_columns]
            
            # 导出到Excel
            df.to_excel(output_path, index=False, engine='openpyxl')
            logger.info(f"会议数据已导出到: {output_path}")
            
            # 保存原始数据为JSON（备份）
            json_path = output_path.replace('.xlsx', '.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(meetings, f, ensure_ascii=False, indent=2)
            logger.info(f"原始数据已保存到: {json_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"导出Excel时出错: {e}")
            return ""
    
    def close(self):
        """关闭浏览器"""
        try:
            if hasattr(self, 'driver'):
                self.driver.quit()
                logger.info("浏览器已关闭")
        except Exception as e:
            logger.error(f"关闭浏览器时出错: {e}")
    
    def run_query(self, start_date: str, end_date: str = None, headless: bool = False) -> Tuple[bool, str, List[Dict]]:
        """
        执行完整的查询流程
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            headless: 是否使用无头模式
            
        Returns:
            Tuple[bool, str, List[Dict]]: (是否成功, 输出文件路径, 会议数据)
        """
        if end_date is None:
            end_date = start_date
        
        success = False
        output_file = ""
        meetings_data = []
        
        try:
            # 初始化
            self.__init__(headless)
            
            # 登录
            if not self.login():
                logger.error("登录失败，请检查账号密码或网络连接")
                return False, "", []
            
            # 导航到会议查询页面
            if not self.navigate_to_meeting_query():
                logger.error("导航到会议查询页面失败")
                return False, "", []
            
            # 查询会议
            meetings_data = self.query_meetings(start_date, end_date)
            
            if meetings_data:
                # 导出数据
                output_file = self.export_to_excel(meetings_data)
                success = True
                logger.info(f"查询成功！共找到{len(meetings_data)}条记录")
            else:
                logger.info("未找到符合条件的会议记录")
                success = True  # 没有数据也视为成功执行
            
            return success, output_file, meetings_data
            
        except Exception as e:
            logger.error(f"查询流程执行失败: {e}")
            return False, "", []
        finally:
            self.close()

def main():
    """主函数：解析命令行参数并执行查询"""
    import argparse
    
    parser = argparse.ArgumentParser(description="江苏海事局会议查询工具")
    parser.add_argument("--start-date", "-s", type=str, default=None,
                       help="开始日期 (格式: YYYY-MM-DD)，默认为今天")
    parser.add_argument("--end-date", "-e", type=str, default=None,
                       help="结束日期 (格式: YYYY-MM-DD)，默认为开始日期")
    parser.add_argument("--headless", action="store_true",
                       help="使用无头模式（不显示浏览器界面）")
    parser.add_argument("--output", "-o", type=str, default=None,
                       help="输出文件路径")
    parser.add_argument("--debug", action="store_true",
                       help="启用调试模式")
    
    args = parser.parse_args()
    
    # 设置日期
    today = datetime.now().strftime("%Y-%m-%d")
    start_date = args.start_date or today
    end_date = args.end_date or start_date
    
    # 设置日志级别
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 执行查询
    bot = None
    try:
        bot = MeetingQueryBot(headless=args.headless)
        success, output_file, meetings = bot.run_query(start_date, end_date, args.headless)
        
        if success:
            if meetings:
                print(f"\n✅ 查询成功！")
                print(f"📅 查询日期: {start_date} 到 {end_date}")
                print(f"📊 找到会议记录: {len(meetings)} 条")
                print(f"💾 数据已保存到: {output_file}")
                
                # 显示前5条记录
                print(f"\n📋 前{min(5, len(meetings))}条记录预览:")
                for i, meeting in enumerate(meetings[:5]):
                    print(f"  {i+1}. {meeting.get('日期', '')} {meeting.get('开始时间', '')} - {meeting.get('会议标题', '')}")
            else:
                print(f"\nℹ️  查询完成，但未找到{start_date}到{end_date}期间的会议记录")
        else:
            print(f"\n❌ 查询失败，请检查日志文件: meeting_query.log")
            return 1
            
    except KeyboardInterrupt:
        print("\n⏹️  用户中断操作")
        return 130
    except Exception as e:
        print(f"\n❌ 程序执行出错: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1
    finally:
        if bot:
            bot.close()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
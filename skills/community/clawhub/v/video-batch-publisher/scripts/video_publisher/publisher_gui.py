import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, simpledialog
import subprocess
import threading
import os
import sys
import logging
import json
import pandas as pd

# 导入核心模块
from core.config_manager import (
    load_global_config,
    get_all_content_types,
    get_type_paths,
    get_platform_default_status,
    config_manager
)
from core.excel_handler import get_statistics, get_pending_rows
from core.constants import PLATFORM_LIST, STATUS_PENDING, COL_NAME

class TextHandler(logging.Handler):
    """将日志输出到tkinter文本框"""
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        self.text_widget.config(state=tk.DISABLED)
        
    def emit(self, record):
        msg = self.format(record)
        self.text_widget.config(state=tk.NORMAL)
        if record.levelno == logging.ERROR:
            self.text_widget.insert(tk.END, msg + '\n', 'error')
        elif record.levelno == logging.WARNING:
            self.text_widget.insert(tk.END, msg + '\n', 'warning')
        else:
            self.text_widget.insert(tk.END, msg + '\n', 'info')
        self.text_widget.see(tk.END)
        self.text_widget.config(state=tk.DISABLED)

class VideoPublisherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("短视频发布工具 v2.3")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        self.is_running = False
        
        # 当前选中的内容类型和路径
        self.current_content_type = ""
        self.current_excel_path = ""
        self.current_input_dir = ""
        self.selected_platforms = []
        
        # 先初始化日志（因为配置加载需要记录日志）
        self.init_logging()
        
        # 初始化配置（会加载默认路径）
        self.init_config()
        
        # 创建UI布局
        self.create_widgets()
        
    def init_config(self):
        """初始化配置"""
        try:
            load_global_config()
            self.content_types = get_all_content_types()
            self.platform_status = get_platform_default_status()
            
            # 预加载默认内容类型的路径（只设置内部变量，不更新UI）
            if self.content_types:
                default_type = list(self.content_types.keys())[0]
                self.current_content_type = default_type
                
                paths = get_type_paths(default_type)
                self.current_excel_path = paths['excel_file']
                self.current_input_dir = paths['input_dir']
                self.logger.info(f"预加载默认配置: {paths['display_name']}")
                    
        except Exception as e:
            messagebox.showerror("配置错误", f"加载配置失败：{str(e)}")
            self.content_types = {}
            self.platform_status = {}
    
    def init_logging(self):
        """初始化日志系统"""
        from core.log_manager import setup_logger
        self.logger = setup_logger("PublisherGUI", "video_publish_gui")
    
    def create_widgets(self):
        """创建UI组件 - 左右分栏布局"""
        # 主窗口分为左右两栏
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 左侧操作区 (65%)
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        left_frame.pack_propagate(False)
        left_frame.bind('<Configure>', lambda e: left_frame.config(width=int(e.width * 0.65)))
        
        # 右侧日志区 (35%)
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right_frame.pack_propagate(False)
        right_frame.bind('<Configure>', lambda e: right_frame.config(width=int(e.width * 0.35)))
        
        # ==================== 左侧操作区 ====================
        # 2.1 顶部：全局配置区
        config_frame = ttk.LabelFrame(left_frame, text="配置选项", padding="10")
        config_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 内容类型选择
        type_frame = ttk.Frame(config_frame)
        type_frame.pack(fill=tk.X, pady=5)
        ttk.Label(type_frame, text="内容类型：").pack(side=tk.LEFT, padx=5)
        self.type_var = tk.StringVar()
        
        if self.content_types:
            type_options = [(key, info.get('type_name', info.get('display_name', key))) for key, info in self.content_types.items()]
            self.current_content_type = type_options[0][0]
            self.type_var.set(self.current_content_type)
            
            for key, display_name in type_options:
                radio = ttk.Radiobutton(type_frame, text=display_name, 
                                       variable=self.type_var, value=key,
                                       command=self.on_type_change)
                radio.pack(side=tk.LEFT, padx=10)
        else:
            ttk.Label(type_frame, text="未配置内容类型").pack(side=tk.LEFT, padx=5)
        
        # 路径显示区
        path_frame = ttk.LabelFrame(left_frame, text="路径配置", padding="10")
        path_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Excel文件路径
        excel_frame = ttk.Frame(path_frame)
        excel_frame.pack(fill=tk.X, pady=3)
        ttk.Label(excel_frame, text="Excel文件：", width=12).pack(side=tk.LEFT)
        self.excel_path_var = tk.StringVar()
        self.excel_entry = ttk.Entry(excel_frame, textvariable=self.excel_path_var, width=50)
        self.excel_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        ttk.Button(excel_frame, text="浏览", command=self.browse_excel).pack(side=tk.LEFT)
        
        # 输入目录
        input_frame = ttk.Frame(path_frame)
        input_frame.pack(fill=tk.X, pady=3)
        ttk.Label(input_frame, text="输入目录：", width=12).pack(side=tk.LEFT)
        self.input_dir_var = tk.StringVar()
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_dir_var, width=50)
        self.input_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        ttk.Button(input_frame, text="浏览", command=self.browse_input_dir).pack(side=tk.LEFT)
        
        # 在UI变量创建之后，再加载默认路径
        if self.content_types:
            self.load_type_paths()
        
        # 平台勾选区
        platform_frame = ttk.LabelFrame(left_frame, text="发布平台", padding="10")
        platform_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.platform_vars = {}
        for i, platform in enumerate(PLATFORM_LIST):
            var = tk.BooleanVar(value=self.platform_status.get(platform, False))
            self.platform_vars[platform] = var
            chk = ttk.Checkbutton(platform_frame, text=platform, variable=var)
            chk.grid(row=0, column=i, padx=8)
        
        # 2.2 中部：待发布列表
        list_frame = ttk.LabelFrame(left_frame, text="待发布列表", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 表格上方按钮
        table_btn_frame = ttk.Frame(list_frame)
        table_btn_frame.pack(fill=tk.X, pady=5)
        
        self.select_all_btn = ttk.Button(table_btn_frame, text="全选", command=self.select_all_items)
        self.select_all_btn.pack(side=tk.LEFT, padx=5)
        
        self.deselect_all_btn = ttk.Button(table_btn_frame, text="取消全选", command=self.deselect_all_items)
        self.deselect_all_btn.pack(side=tk.LEFT, padx=5)
        
        self.refresh_list_btn = ttk.Button(table_btn_frame, text="刷新列表", command=self.refresh_publish_list)
        self.refresh_list_btn.pack(side=tk.RIGHT, padx=5)
        
        # 创建表格框架
        table_frame = ttk.Frame(list_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建滚动条
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建树状视图（去掉视频路径、横封面、竖封面列，添加标题、描述列）
        self.publish_tree = ttk.Treeview(table_frame, yscrollcommand=scrollbar.set,
                                         columns=('select', 'sn', 'name', 'publish_date', 'title', 'description', 'status'),
                                         show='headings', height=12)
        self.publish_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.publish_tree.yview)
        
        # 设置列标题和宽度
        self.publish_tree.heading('select', text='选择')
        self.publish_tree.heading('sn', text='序号')
        self.publish_tree.heading('name', text='名称')
        self.publish_tree.heading('publish_date', text='发布日期')
        self.publish_tree.heading('title', text='标题')
        self.publish_tree.heading('description', text='描述')
        self.publish_tree.heading('status', text='状态')
        
        self.publish_tree.column('select', width=45, anchor=tk.CENTER)
        self.publish_tree.column('sn', width=50, anchor=tk.CENTER)
        self.publish_tree.column('name', width=100, anchor=tk.W)
        self.publish_tree.column('publish_date', width=100, anchor=tk.CENTER)
        self.publish_tree.column('title', width=150, anchor=tk.W)
        self.publish_tree.column('description', width=200, anchor=tk.W)
        self.publish_tree.column('status', width=60, anchor=tk.CENTER)
        
        # 绑定点击事件（用于选择列勾选和封面点击）
        self.publish_tree.bind('<Button-1>', self.on_tree_click)
        
        # 2.3 底部：发布按钮区
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        def on_publish_click():
            print("DEBUG: 正式发布按钮被点击！")
            self.execute_publish_direct('publish')
        
        def on_draft_click():
            print("DEBUG: 发布草稿按钮被点击！")
            self.execute_publish_direct('draft')
        
        self.publish_btn = ttk.Button(
            button_frame, 
            text="正式发布", 
            command=on_publish_click,
            width=15
        )
        self.publish_btn.pack(side=tk.LEFT, padx=5)
        
        self.draft_btn = ttk.Button(
            button_frame, 
            text="发布草稿", 
            command=on_draft_click,
            width=15
        )
        self.draft_btn.pack(side=tk.LEFT, padx=5)
        
        # ==================== 右侧日志区 ====================
        # 3.1 日志工具栏
        log_toolbar = ttk.Frame(right_frame)
        log_toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        self.clear_log_btn = ttk.Button(log_toolbar, text="清空日志", command=self.clear_log)
        self.clear_log_btn.pack(side=tk.LEFT, padx=5)
        
        self.status_btn = ttk.Button(log_toolbar, text="查看状态", command=self.show_status)
        self.status_btn.pack(side=tk.LEFT, padx=5)
        
        # 3.2 日志文本框
        log_frame = ttk.LabelFrame(right_frame, text="发布日志", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        self.log_text.tag_config('info', foreground='black')
        self.log_text.tag_config('warning', foreground='orange')
        self.log_text.tag_config('error', foreground='red')
        
        text_handler = TextHandler(self.log_text)
        text_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        self.logger.addHandler(text_handler)
        
        # 底部状态栏
        self.status_var = tk.StringVar(value="就绪 - 等待发布")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, ipady=2)
        
        # 初始日志
        self.logger.info("=== 短视频发布工具 v2.3 已启动 ===")
        self.logger.info("配置文件路径: config.yaml")
        
        # 初始化待发布列表
        self.publish_items = []
        
        # 绑定表格双击事件
        self.publish_tree.bind('<Double-1>', self.on_tree_double_click)
    
    def on_type_change(self, event=None):
        """内容类型变更处理"""
        # radio 单选框直接返回 key（如 "idiom"、"poem"）
        self.current_content_type = self.type_var.get()
        self.load_type_paths()
        # 刷新待发布列表
        self.refresh_publish_list()
    
    def select_all_items(self):
        """全选表格中的所有项目"""
        for item in self.publish_tree.get_children():
            self.publish_tree.set(item, 'select', '✓')
    
    def deselect_all_items(self):
        """取消全选表格中的所有项目"""
        for item in self.publish_tree.get_children():
            self.publish_tree.set(item, 'select', '')
    
    def refresh_publish_list(self):
        """刷新待发布列表"""
        # 清空现有表格
        for item in self.publish_tree.get_children():
            self.publish_tree.delete(item)
        
        self.publish_items = []
        
        # 获取选中的平台
        self.selected_platforms = [p for p, var in self.platform_vars.items() if var.get()]
        if not self.selected_platforms:
            return
        
        # 验证路径
        if not self.excel_path_var.get():
            return
        
        try:
            # 获取待发布视频列表
            pending_df = get_pending_rows(self.excel_path_var.get(), self.selected_platforms)
            
            if len(pending_df) == 0:
                self.logger.info("没有待发布的视频")
                return
            
            from core.constants import COL_PUBLISH_DATE
            from core.excel_handler import ExcelHandler
            
            cover_config = config_manager.get_type_covers(self.current_content_type)
            cover_horizontal_name = cover_config.get("horizontal", "")
            cover_vertical_name = cover_config.get("vertical", "")
            
            # 创建Excel处理器实例
            excel_handler = ExcelHandler(self.excel_path_var.get())
            
            # 收集待发布视频信息
            for idx, row in pending_df.iterrows():
                # 获取序号
                sn_val = row.get('序号', '')
                if isinstance(sn_val, pd.Series):
                    sn_val = sn_val.iloc[0] if not sn_val.empty else ""
                sn = str(sn_val).strip()
                
                # 获取名称
                name_val = row.get(COL_NAME)
                if isinstance(name_val, pd.Series):
                    name_val = name_val.iloc[0] if not name_val.empty else ""
                name = str(name_val).strip() if pd.notna(name_val) else ""
                
                # 获取发布日期
                date_val = row.get(COL_PUBLISH_DATE)
                if isinstance(date_val, pd.Series):
                    date_val = date_val.iloc[0] if not date_val.empty else ""
                publish_date = str(date_val).strip() if pd.notna(date_val) else ""
                
                # 查找视频路径
                video_path = ""
                actual_name = name
                try:
                    input_dir = self.input_dir_var.get()
                    if input_dir and name:
                        possible_names = [f"{name}.mp4", f"{sn}{name}.mp4"]
                        if sn.isdigit():
                            possible_names.extend([f"{int(sn):03d}{name}.mp4", f"{int(sn):04d}{name}.mp4"])
                        for video_name in possible_names:
                            candidate = os.path.join(input_dir, video_name)
                            if os.path.exists(candidate):
                                video_path = candidate
                                actual_name = os.path.splitext(video_name)[0]
                                break
                        if not video_path:
                            for filename in os.listdir(input_dir):
                                if filename.endswith('.mp4') and name in filename:
                                    video_path = os.path.join(input_dir, filename)
                                    actual_name = os.path.splitext(filename)[0]
                                    break
                except Exception as e:
                    self.logger.warning(f"查找视频文件失败: {str(e)}")
                
                # 检测封面文件
                cover_horizontal = ""
                cover_vertical = ""
                cover_dir = os.path.join(self.input_dir_var.get(), actual_name)
                
                if video_path and os.path.exists(cover_dir):
                    if cover_horizontal_name:
                        cover_horizontal_path = os.path.join(cover_dir, cover_horizontal_name)
                        if os.path.exists(cover_horizontal_path):
                            cover_horizontal = cover_horizontal_path
                    if cover_vertical_name:
                        cover_vertical_path = os.path.join(cover_dir, cover_vertical_name)
                        if os.path.exists(cover_vertical_path):
                            cover_vertical = cover_vertical_path
                
                # 获取标题和描述（按平台分割后的字典）
                title_desc = excel_handler.get_title_description(idx)
                
                # 如果没有传platform参数，返回的是原始内容，需要手动按平台分割
                raw_title = title_desc.get('title', '')
                raw_desc = title_desc.get('description', '')
                
                # 调试日志
                self.logger.info(f"行{idx} - 原始标题: {repr(raw_title[:100]) if raw_title else '空'}")
                self.logger.info(f"行{idx} - 原始描述: {repr(raw_desc[:100]) if raw_desc else '空'}")
                
                # 按平台分割标题和描述，生成字典
                title_dict = self._split_content_by_platform(raw_title)
                desc_dict = self._split_content_by_platform(raw_desc)
                
                # 表格中显示摘要（前50个字符）
                title_summary = f"{len(title_dict)}个平台" if title_dict else ''
                desc_summary = f"{len(desc_dict)}个平台" if desc_dict else ''
                
                # 存储完整的JSON字符串供点击查看
                title_full_json = json.dumps(title_dict, ensure_ascii=False, indent=2)
                desc_full_json = json.dumps(desc_dict, ensure_ascii=False, indent=2)
                
                # 获取待发布平台（只检查用户选中的平台）
                pending_platforms = []
                for platform in self.selected_platforms:
                    if platform in row:
                        value = row[platform]
                        if isinstance(value, pd.Series):
                            value = value.iloc[0] if not value.empty else ""
                        if value == STATUS_PENDING or pd.isna(value):
                            pending_platforms.append(platform)
                
                # 添加到表格（默认选中）
                item_id = self.publish_tree.insert('', tk.END, values=(
                    '✓',  # 选择框 - 默认选中
                    sn,
                    name,
                    publish_date,
                    title_summary,
                    desc_summary,
                    '待发布'
                ))
                
                # 存储详细信息
                self.publish_items.append({
                    'index': idx,
                    'sn': sn,
                    'name': name,
                    'publish_date': publish_date,
                    'video_path': video_path,
                    'platforms': pending_platforms,
                    'publish': True,
                    'cover_horizontal': cover_horizontal,
                    'cover_vertical': cover_vertical,
                    'title': title_dict,  # 存储按平台分割后的字典
                    'description': desc_dict,  # 存储按平台分割后的字典
                    'title_json': title_full_json,  # 存储完整JSON供点击查看
                    'desc_json': desc_full_json,  # 存储完整JSON供点击查看
                    'status': '待发布',
                    'error': '',
                    'tree_id': item_id
                })
            
            self.logger.info(f"已加载 {len(self.publish_items)} 条待发布视频")
            
        except Exception as e:
            self.logger.error(f"刷新待发布列表出错: {str(e)}")
    
    def on_tree_click(self, event):
        """表格单击事件 - 处理选择框勾选和标题/描述点击查看JSON"""
        try:
            item = self.publish_tree.identify_row(event.y)
            if not item:
                return
            
            column = self.publish_tree.identify_column(event.x)
            col_index = int(column.replace('#', '')) - 1
            
            # 点击选择列（第一列）
            if col_index == 0:
                current_value = self.publish_tree.set(item, 'select')
                new_value = '✓' if current_value != '✓' else ''
                self.publish_tree.set(item, 'select', new_value)
            
            # 点击标题列（第五列，索引4）
            elif col_index == 4:
                # 查找对应的项目数据
                for item_data in self.publish_items:
                    if item_data['tree_id'] == item:
                        title_json = item_data.get('title_json', '')
                        if title_json:
                            self._show_json_dialog("标题分割结果", title_json)
                        break
            
            # 点击描述列（第六列，索引5）
            elif col_index == 5:
                # 查找对应的项目数据
                for item_data in self.publish_items:
                    if item_data['tree_id'] == item:
                        desc_json = item_data.get('desc_json', '')
                        if desc_json:
                            self._show_json_dialog("描述分割结果", desc_json)
                        break
        
        except Exception as e:
            self.logger.error(f"表格点击事件处理出错: {str(e)}")
    
    def _show_json_dialog(self, title, json_content):
        """显示JSON内容的弹窗"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("600x500")
        dialog.resizable(True, True)
        
        # 创建滚动文本框
        text_frame = ttk.Frame(dialog)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, font=('Consolas', 10))
        text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=text.yview)
        
        # 插入JSON内容
        text.insert(tk.END, json_content)
        text.config(state=tk.DISABLED)
        
        # 添加关闭按钮
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        close_btn = ttk.Button(btn_frame, text="关闭", command=dialog.destroy)
        close_btn.pack(side=tk.RIGHT)
    
    def _split_content_by_platform(self, raw_content):
        """按平台分割标题或描述文本，返回字典
        
        Args:
            raw_content: 原始文本（标题或描述）
            
        Returns:
            按平台分割后的字典，如 {"快手": "快手内容", "视频号": "视频号内容"}
        """
        if not raw_content:
            return {}
        
        import re
        
        platforms = ["抖音", "快手", "B站", "视频号/其他", "视频号", "通用"]
        
        platform_sep = "|".join(re.escape(p) for p in platforms)
        
        result = {}
        
        for platform in platforms:
            platform_pattern = re.compile(rf"{re.escape(platform)}：\s*(.*?)(?=\n(?:{platform_sep})：|$)", re.DOTALL)
            match = platform_pattern.search(raw_content)
            if match:
                content = match.group(1).strip()
                if content:
                    # 将"视频号/其他"统一存储为"视频号"
                    key = "视频号" if platform == "视频号/其他" else platform
                    result[key] = content
        
        return result
    
    def open_cover_file(self, cover_path):
        """打开封面文件或其所在文件夹"""
        try:
            if os.path.exists(cover_path):
                # 先尝试用默认程序打开图片
                import subprocess
                subprocess.Popen(f'explorer "{cover_path}"')
            else:
                messagebox.showwarning("提示", "封面文件不存在！")
        except Exception as e:
            # 如果打开图片失败，尝试打开文件夹
            try:
                cover_dir = os.path.dirname(cover_path)
                import subprocess
                subprocess.Popen(f'explorer "{cover_dir}"')
            except Exception as e2:
                messagebox.showwarning("提示", "无法打开文件或文件夹！")
    
    def on_tree_double_click(self, event):
        """表格双击编辑事件"""
        item = self.publish_tree.selection()[0]
        column = self.publish_tree.identify_column(event.x)
        
        # 获取列索引
        col_index = int(column.replace('#', '')) - 1
        
        if col_index == 3:  # 发布日期列
            current_value = self.publish_tree.item(item, 'values')[col_index]
            new_value = simpledialog.askstring("编辑", "请输入发布日期:", initialvalue=current_value)
            if new_value is not None:
                self.publish_tree.set(item, 'publish_date', new_value.strip())
                
                # 更新内部数据
                for item_data in self.publish_items:
                    if item_data['tree_id'] == item:
                        item_data['publish_date'] = new_value.strip()
                        break
    
    def execute_publish_direct(self, publish_mode):
        """直接执行发布（不带确认弹窗）"""
        self.logger.info(f"execute_publish_direct called with mode: {publish_mode}")
        
        if self.is_running:
            self.logger.info("发布任务正在运行中，拒绝重复执行")
            messagebox.showwarning("提示", "发布任务正在运行中，请稍候！")
            return
        
        # 获取选中的平台
        self.selected_platforms = [p for p, var in self.platform_vars.items() if var.get()]
        self.logger.info(f"选中的平台: {self.selected_platforms}")
        
        if not self.selected_platforms:
            self.logger.info("未选择任何平台")
            messagebox.showwarning("提示", "请至少选择一个发布平台！")
            return
        
        # 获取勾选的项目
        selected_items = []
        self.logger.info(f"publish_items列表长度: {len(self.publish_items)}")
        
        for item in self.publish_tree.get_children():
            select_val = self.publish_tree.set(item, 'select')
            self.logger.info(f"tree item: {item}, select_val: '{select_val}', type: {type(select_val)}")
            
            # 尝试获取所有值来检查
            all_values = self.publish_tree.item(item, 'values')
            self.logger.info(f"all_values: {all_values}")
            
            if select_val == '✓' or select_val == '选中' or '✓' in str(select_val):
                # 查找对应的项目数据
                self.logger.info(f"找到选中项，开始匹配publish_items...")
                for idx, item_data in enumerate(self.publish_items):
                    self.logger.info(f"  正在匹配: publish_items[{idx}]['tree_id'] = {item_data.get('tree_id')}")
                    if item_data['tree_id'] == item:
                        selected_items.append(item_data)
                        self.logger.info(f"  ✓ 匹配成功！")
                        break
                else:
                    self.logger.info(f"  ✗ 未在publish_items中找到匹配项")
        
        self.logger.info(f"最终选中的视频数量: {len(selected_items)}")
        
        if not selected_items:
            self.logger.info("未选择任何视频")
            messagebox.showwarning("提示", "请至少选择一个待发布的视频！")
            return
        
        # 执行发布
        self.logger.info("开始执行发布任务")
        self.execute_publish(selected_items, publish_mode)
    
    def execute_publish(self, publish_items, publish_mode='publish'):
        """执行发布任务"""
        def run_task():
            self.is_running = True
            self.publish_btn.config(state=tk.DISABLED)
            self.draft_btn.config(state=tk.DISABLED)
            self.status_var.set("运行中 - 正在执行发布任务...")
            
            try:
                import json
                import tempfile
                
                script_path = os.path.join(os.path.dirname(__file__), "video_publisher.py")
                
                # 将用户编辑的数据保存到临时文件
                temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8')
                publish_data = {
                    'publish_items': publish_items,
                    'publish_mode': publish_mode
                }
                json.dump(publish_data, temp_file, ensure_ascii=False, indent=2)
                temp_file.close()
                
                # 构建命令参数
                args = [sys.executable, script_path]
                args.extend(["--content-type", self.current_content_type])
                args.extend(["--excel-path", self.excel_path_var.get()])
                args.extend(["--input-dir", self.input_dir_var.get()])
                args.extend(["--platforms", ",".join(self.selected_platforms)])
                args.extend(["--publish-data", temp_file.name])
                
                result = subprocess.run(
                    args,
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )
                
                # 删除临时文件
                os.unlink(temp_file.name)
                
                if result.stdout:
                    self.logger.info(f"脚本输出:\n{result.stdout}")
                if result.stderr:
                    self.logger.error(f"脚本错误:\n{result.stderr}")
                
                if result.returncode == 0:
                    self.logger.info("=== 发布任务执行完成 ===")
                    self.status_var.set("完成 - 发布任务已执行完毕")
                    
                    # 更新表格状态
                    for item_data in publish_items:
                        for item in self.publish_tree.get_children():
                            if item == item_data['tree_id']:
                                self.publish_tree.set(item, 'status', '成功')
                                break
                    
                    # 查找最新的发布结果文件
                    output_dir = os.path.join(os.path.dirname(__file__), 'output')
                    result_files = []
                    if os.path.exists(output_dir):
                        for f in os.listdir(output_dir):
                            if f.startswith('publish_result_') and f.endswith('.json'):
                                result_files.append(os.path.join(output_dir, f))
                    
                    if result_files:
                        latest_result = max(result_files, key=os.path.getmtime)
                        self.show_publish_result(latest_result)
                    else:
                        messagebox.showinfo("成功", "发布任务执行完成！")
                else:
                    self.logger.error("=== 发布任务执行失败 ===")
                    self.status_var.set("错误 - 发布任务执行失败")
                    
                    # 更新表格状态
                    for item_data in publish_items:
                        for item in self.publish_tree.get_children():
                            if item == item_data['tree_id']:
                                self.publish_tree.set(item, 'status', '失败')
                                break
                    
                    messagebox.showerror("错误", "发布任务执行失败，请查看日志！")
                    
            except Exception as e:
                self.logger.error(f"执行发布脚本出错: {str(e)}")
                self.status_var.set("错误 - 执行脚本出错")
                messagebox.showerror("错误", f"执行脚本出错: {str(e)}")
                
            finally:
                self.is_running = False
                self.publish_btn.config(state=tk.NORMAL)
                self.draft_btn.config(state=tk.NORMAL)
        
        threading.Thread(target=run_task, daemon=True).start()
    
    def show_publish_confirmation_dialog(self):
        """旧方法 - 保留以兼容其他调用"""
        self.refresh_publish_list()
    
    def show_publish_confirmation(self, pending_df):
        """旧方法 - 保留以兼容其他调用"""
        return None
    
    def load_type_paths(self):
        """加载当前类型的路径配置"""
        try:
            paths = get_type_paths(self.current_content_type)
            self.current_excel_path = paths['excel_file']
            self.current_input_dir = paths['input_dir']
            self.excel_path_var.set(self.current_excel_path)
            self.input_dir_var.set(self.current_input_dir)
            self.logger.info(f"已加载内容类型: {paths['display_name']}")
        except Exception as e:
            self.logger.error(f"加载路径失败: {str(e)}")
    
    def browse_excel(self):
        """浏览Excel文件"""
        path = filedialog.askopenfilename(
            title="选择Excel文件",
            filetypes=[("Excel文件", "*.xlsx")]
        )
        if path:
            self.excel_path_var.set(path)
            self.current_excel_path = path
    
    def browse_input_dir(self):
        """浏览输入目录"""
        path = filedialog.askdirectory(title="选择输入目录")
        if path:
            self.input_dir_var.set(path)
            self.current_input_dir = path
    
    def show_publish_confirmation_dialog(self):
        """显示发布确认弹窗（合并查看待发布和一键发布功能）"""
        if self.is_running:
            messagebox.showwarning("提示", "发布任务正在运行中，请稍候！")
            return
        
        # 获取选中的平台
        self.selected_platforms = [p for p, var in self.platform_vars.items() if var.get()]
        if not self.selected_platforms:
            messagebox.showwarning("提示", "请至少选择一个发布平台！")
            return
        
        # 验证路径
        if not self.excel_path_var.get():
            messagebox.showwarning("提示", "请选择Excel文件！")
            return
        
        # 获取待发布视频列表
        pending_df = get_pending_rows(self.excel_path_var.get(), self.selected_platforms)
        if len(pending_df) == 0:
            messagebox.showinfo("提示", "没有待发布的视频！")
            return
        
        # 显示确认弹窗（带可编辑路径功能）
        confirm_data = self.show_publish_confirmation(pending_df)
        if not confirm_data:
            return
        
        # 执行发布
        self.execute_publish(confirm_data, 'publish')
    
    def clear_log(self):
        """清空日志"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.logger.info("日志已清空")
    
    def show_status(self):
        """快速查看发布状态"""
        try:
            if not self.excel_path_var.get():
                messagebox.showwarning("提示", "请先选择Excel文件！")
                return
            
            stats = get_statistics(self.excel_path_var.get())
            
            self.logger.info("=== 发布状态统计 ===")
            self.logger.info(f"总视频数: {stats['total']}")
            self.logger.info(f"视频草稿就绪: {stats['draft_done']}")
            self.logger.info(f"视频完成: {stats['video_done']}")
            
            for platform in PLATFORM_LIST:
                published = stats.get(f"{platform}_published", 0)
                pending = stats.get(f"{platform}_pending", 0)
                self.logger.info(f"{platform}已发布: {published}, 待发布: {pending}")
            
            # 初始化 status_text
            status_text = f"""发布状态统计：
┌─────────────────────┐
│ 总视频数：{stats['total']:>6} │
│ 视频草稿：{stats['draft_done']:>5} │
│ 视频完成：{stats['video_done']:>5} │
├─────────────────────┤"""
            
            for platform in PLATFORM_LIST:
                published = stats.get(f"{platform}_published", 0)
                pending = stats.get(f"{platform}_pending", 0)
                status_text += f"\n│ {platform}已发布：{published:>3}，待发布：{pending:>3} │"
            
            status_text += "\n└─────────────────────┘"
            messagebox.showinfo("发布状态", status_text)
            
        except Exception as e:
            self.logger.error(f"统计发布状态出错: {str(e)}")
            messagebox.showerror("错误", f"统计状态出错: {str(e)}")
    
    def show_pending_videos(self):
        """显示待发布视频列表"""
        try:
            if not self.excel_path_var.get():
                messagebox.showwarning("提示", "请先选择Excel文件！")
                return
            
            selected_platforms = [p for p, var in self.platform_vars.items() if var.get()]
            if not selected_platforms:
                selected_platforms = None
            
            pending_df = get_pending_rows(self.excel_path_var.get(), selected_platforms)
            
            self.logger.info("=== 待发布视频列表 ===")
            if len(pending_df) == 0:
                self.logger.info("没有待发布的视频")
                messagebox.showinfo("待发布视频", "没有待发布的视频")
                return
            
            self.logger.info(f"共找到 {len(pending_df)} 条待发布视频")
            
            for idx, row in pending_df.iterrows():
                pending_platforms = []
                for platform in PLATFORM_LIST:
                    if platform in row:
                        value = row[platform]
                        if value == STATUS_PENDING or pd.isna(value):
                            pending_platforms.append(platform)
                
                name_value = row.get(COL_NAME)
                name = str(name_value).strip() if pd.notna(name_value) else ""
                info = f"名称: {name} | 待发布平台: {', '.join(pending_platforms)}"
                self.logger.info(info)
            
            self.logger.info("=== 待发布视频列表结束 ===")
            
        except Exception as e:
            self.logger.error(f"查看待发布视频出错: {str(e)}")
            messagebox.showerror("错误", f"查看待发布视频出错: {str(e)}")
    
    def show_publish_confirmation(self, pending_df):
        """显示发布确认弹窗，允许用户编辑待发布列表"""
        try:
            from core.constants import COL_PUBLISH_DATE
            
            self.logger.info(f"show_publish_confirmation - pending_df类型: {type(pending_df)}")
            self.logger.info(f"show_publish_confirmation - pending_df形状: {pending_df.shape if hasattr(pending_df, 'shape') else '未知'}")
            
            # 从配置获取封面文件名
            cover_config = config_manager.get_type_covers(self.current_content_type)
            cover_horizontal_name = cover_config.get("horizontal", "")
            cover_vertical_name = cover_config.get("vertical", "")
            
            # 收集待发布视频信息
            publish_items = []
            for idx, row in pending_df.iterrows():
                # 获取序号
                sn = ""
                try:
                    sn_val = row.get('序号', '')
                    if isinstance(sn_val, pd.Series):
                        sn_val = sn_val.iloc[0] if not sn_val.empty else ""
                    sn = str(sn_val).strip()
                except Exception as e:
                    self.logger.error(f"获取序号出错: {str(e)}")
                
                # 获取名称
                name = ""
                try:
                    name_val = row.get(COL_NAME)
                    if isinstance(name_val, pd.Series):
                        name_val = name_val.iloc[0] if not name_val.empty else ""
                    name = str(name_val).strip() if pd.notna(name_val) else ""
                except Exception as e:
                    self.logger.error(f"获取名称出错: {str(e)}")
                
                # 获取发布日期
                publish_date = ""
                try:
                    date_val = row.get(COL_PUBLISH_DATE)
                    if isinstance(date_val, pd.Series):
                        date_val = date_val.iloc[0] if not date_val.empty else ""
                    publish_date = str(date_val).strip() if pd.notna(date_val) else ""
                except Exception as e:
                    self.logger.error(f"获取发布日期出错: {str(e)}")
                
                # 查找视频路径
                video_path = ""
                actual_name = name
                try:
                    input_dir = self.input_dir_var.get()
                    self.logger.info(f"input_dir: {input_dir}")
                    if input_dir and name:
                        possible_names = [f"{name}.mp4", f"{sn}{name}.mp4"]
                        if sn.isdigit():
                            possible_names.extend([f"{int(sn):03d}{name}.mp4", f"{int(sn):04d}{name}.mp4"])
                        for video_name in possible_names:
                            candidate = os.path.join(input_dir, video_name)
                            if os.path.exists(candidate):
                                video_path = candidate
                                actual_name = os.path.splitext(video_name)[0]
                                break
                        if not video_path:
                            for filename in os.listdir(input_dir):
                                if filename.endswith('.mp4') and name in filename:
                                    video_path = os.path.join(input_dir, filename)
                                    actual_name = os.path.splitext(filename)[0]
                                    break
                except Exception as e:
                    self.logger.warning(f"查找视频文件失败: {str(e)}")
                
                # 检测封面文件
                cover_horizontal = ""
                cover_vertical = ""
                cover_dir = os.path.join(self.input_dir_var.get(), actual_name)
                
                if video_path and os.path.exists(cover_dir):
                    if cover_horizontal_name:
                        cover_horizontal_path = os.path.join(cover_dir, cover_horizontal_name)
                        if os.path.exists(cover_horizontal_path):
                            cover_horizontal = cover_horizontal_path
                    if cover_vertical_name:
                        cover_vertical_path = os.path.join(cover_dir, cover_vertical_name)
                        if os.path.exists(cover_vertical_path):
                            cover_vertical = cover_vertical_path
                
                # 获取待发布平台
                pending_platforms = []
                for platform in PLATFORM_LIST:
                    if platform in row:
                        try:
                            value = row[platform]
                            if hasattr(value, '__iter__') and not isinstance(value, str):
                                value = value.iloc[0] if hasattr(value, 'iloc') else value[0]
                            if value == STATUS_PENDING or pd.isna(value):
                                pending_platforms.append(platform)
                        except Exception as e:
                            self.logger.warning(f"处理平台{platform}出错: {str(e)}")
                
                publish_items.append({
                    'index': idx,
                    'sn': sn,
                    'name': name,
                    'publish_date': publish_date,
                    'video_path': video_path,
                    'platforms': pending_platforms,
                    'publish': True,
                    'cover_horizontal': cover_horizontal,
                    'cover_vertical': cover_vertical,
                    'status': '待发布',
                    'error': ''
                })
            self.logger.info(f"publish_items长度: {len(publish_items)}")
            
            # 创建弹窗
            confirm_window = tk.Toplevel(self.root)
            confirm_window.title("发布确认")
            confirm_window.geometry("1400x700")
            confirm_window.resizable(True, True)
            
            # 创建表格框架
            frame = ttk.Frame(confirm_window)
            frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # 创建滚动条
            scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # 创建树状视图（增加封面列和发布日期列）
            tree = ttk.Treeview(frame, yscrollcommand=scrollbar.set, 
                                columns=('select', 'sn', 'name', 'platforms', 'publish_date', 'video', 'cover_v', 'cover_h', 'status'), 
                                show='headings')
            tree.pack(fill=tk.BOTH, expand=True)
            scrollbar.config(command=tree.yview)
            
            # 设置列标题
            tree.heading('select', text='需要发布')
            tree.heading('sn', text='序号')
            tree.heading('name', text='名称')
            tree.heading('platforms', text='待发布平台')
            tree.heading('publish_date', text='发布日期')
            tree.heading('video', text='视频路径')
            tree.heading('cover_v', text='竖屏封面')
            tree.heading('cover_h', text='横屏封面')
            tree.heading('status', text='状态')
            
            # 设置列宽
            tree.column('select', width=80, anchor=tk.CENTER)
            tree.column('sn', width=60, anchor=tk.CENTER)
            tree.column('name', width=120)
            tree.column('platforms', width=150)
            tree.column('publish_date', width=150, anchor=tk.CENTER)
            tree.column('video', width=280)
            tree.column('cover_v', width=80, anchor=tk.CENTER)
            tree.column('cover_h', width=80, anchor=tk.CENTER)
            tree.column('status', width=80, anchor=tk.CENTER)
            
            # 存储复选框状态和路径变量
            check_vars = []
            video_path_vars = []
            cover_v_vars = []
            cover_h_vars = []
            publish_date_vars = []
            
            # 插入数据
            for item in publish_items:
                check_var = tk.BooleanVar(value=item['publish'])
                check_vars.append(check_var)
                
                video_var = tk.StringVar(value=item['video_path'])
                video_path_vars.append(video_var)
                
                cover_v_var = tk.StringVar(value=item['cover_vertical'])
                cover_v_vars.append(cover_v_var)
                
                cover_h_var = tk.StringVar(value=item['cover_horizontal'])
                cover_h_vars.append(cover_h_var)
                
                date_var = tk.StringVar(value=item['publish_date'])
                publish_date_vars.append(date_var)
                
                # 检查视频是否存在
                status = '待发布'
                if not item['video_path']:
                    status = '视频缺失'
                
                tree.insert('', tk.END, values=(
                    '✓' if item['publish'] else '',
                    item['sn'],
                    item['name'],
                    ', '.join(item['platforms']),
                    item['publish_date'] or '立即发布',
                    item['video_path'] or '未找到',
                    '✓' if item['cover_vertical'] else '缺失',
                    '✓' if item['cover_horizontal'] else '缺失',
                    status
                ))
            
            # 双击编辑路径或日期
            def on_double_click(event):
                item_id = tree.selection()
                if item_id:
                    idx = int(tree.index(item_id[0]))
                    column = tree.identify_column(event.x)
                    
                    if column == '#5':  # 发布日期
                        new_date = simpledialog.askstring("修改发布日期", "请输入发布日期 (格式: YYYY-MM-DD HH:MM):", 
                                                          initialvalue=publish_date_vars[idx].get())
                        if new_date is not None:
                            publish_date_vars[idx].set(new_date)
                            publish_items[idx]['publish_date'] = new_date
                            tree.item(item_id[0], values=(
                                '✓' if check_vars[idx].get() else '',
                                publish_items[idx]['sn'],
                                publish_items[idx]['name'],
                                ', '.join(publish_items[idx]['platforms']),
                                new_date or '立即发布',
                                publish_items[idx]['video_path'] or '未找到',
                                '✓' if publish_items[idx]['cover_vertical'] else '缺失',
                                '✓' if publish_items[idx]['cover_horizontal'] else '缺失',
                                '待发布' if publish_items[idx]['video_path'] else '视频缺失'
                            ))
                    
                    elif column == '#6':  # 视频路径
                        path = filedialog.askopenfilename(
                            title="选择视频文件",
                            filetypes=[("MP4文件", "*.mp4"), ("所有文件", "*.*")]
                        )
                        if path:
                            video_path_vars[idx].set(path)
                            publish_items[idx]['video_path'] = path
                            tree.item(item_id[0], values=(
                                '✓' if check_vars[idx].get() else '',
                                publish_items[idx]['sn'],
                                publish_items[idx]['name'],
                                ', '.join(publish_items[idx]['platforms']),
                                publish_items[idx]['publish_date'] or '立即发布',
                                path,
                                '✓' if publish_items[idx]['cover_vertical'] else '缺失',
                                '✓' if publish_items[idx]['cover_horizontal'] else '缺失',
                                '待发布'
                            ))
                    
                    elif column == '#7':  # 竖屏封面
                        path = filedialog.askopenfilename(
                            title="选择竖屏封面",
                            filetypes=[("PNG文件", "*.png"), ("JPG文件", "*.jpg"), ("所有文件", "*.*")]
                        )
                        if path:
                            cover_v_vars[idx].set(path)
                            publish_items[idx]['cover_vertical'] = path
                            tree.item(item_id[0], values=(
                                '✓' if check_vars[idx].get() else '',
                                publish_items[idx]['sn'],
                                publish_items[idx]['name'],
                                ', '.join(publish_items[idx]['platforms']),
                                publish_items[idx]['publish_date'] or '立即发布',
                                publish_items[idx]['video_path'] or '未找到',
                                '✓',
                                '✓' if publish_items[idx]['cover_horizontal'] else '缺失',
                                '待发布'
                            ))
                    
                    elif column == '#8':  # 横屏封面
                        path = filedialog.askopenfilename(
                            title="选择横屏封面",
                            filetypes=[("PNG文件", "*.png"), ("JPG文件", "*.jpg"), ("所有文件", "*.*")]
                        )
                        if path:
                            cover_h_vars[idx].set(path)
                            publish_items[idx]['cover_horizontal'] = path
                            tree.item(item_id[0], values=(
                                '✓' if check_vars[idx].get() else '',
                                publish_items[idx]['sn'],
                                publish_items[idx]['name'],
                                ', '.join(publish_items[idx]['platforms']),
                                publish_items[idx]['publish_date'] or '立即发布',
                                publish_items[idx]['video_path'] or '未找到',
                                '✓' if publish_items[idx]['cover_vertical'] else '缺失',
                                '✓',
                                '待发布'
                            ))
            
            tree.bind('<Double-1>', on_double_click)
            
            # 绑定复选框点击事件（单击第一列切换）
            def on_select(event):
                item_id = tree.selection()
                if item_id:
                    idx = int(tree.index(item_id[0]))
                    column = tree.identify_column(event.x)
                    if column == '#1':  # 只有点击第一列才切换
                        check_vars[idx].set(not check_vars[idx].get())
                        tree.item(item_id[0], values=(
                            '✓' if check_vars[idx].get() else '',
                            publish_items[idx]['sn'],
                            publish_items[idx]['name'],
                            ', '.join(publish_items[idx]['platforms']),
                            publish_items[idx]['publish_date'] or '立即发布',
                            publish_items[idx]['video_path'] or '未找到',
                            '✓' if publish_items[idx]['cover_vertical'] else '缺失',
                            '✓' if publish_items[idx]['cover_horizontal'] else '缺失',
                            '待发布' if publish_items[idx]['video_path'] else '视频缺失'
                        ))
            
            tree.bind('<Button-1>', on_select)
            
            # 全选/取消全选按钮
            def toggle_all():
                all_selected = all(v.get() for v in check_vars)
                for i, v in enumerate(check_vars):
                    v.set(not all_selected)
                    tree.item(tree.get_children()[i], values=(
                        '✓' if not all_selected else '',
                        publish_items[i]['sn'],
                        publish_items[i]['name'],
                        ', '.join(publish_items[i]['platforms']),
                        publish_items[i]['publish_date'] or '立即发布',
                        publish_items[i]['video_path'] or '未找到',
                        '✓' if publish_items[i]['cover_vertical'] else '缺失',
                        '✓' if publish_items[i]['cover_horizontal'] else '缺失',
                        '待发布' if publish_items[i]['video_path'] else '视频缺失'
                    ))
            
            # 按钮框架
            btn_frame = ttk.Frame(confirm_window)
            btn_frame.pack(fill=tk.X, padx=10, pady=10)
            
            select_all_btn = ttk.Button(btn_frame, text="全选/取消全选", command=toggle_all)
            select_all_btn.pack(side=tk.LEFT, padx=5)
            
            # 正式发布按钮
            def publish_direct():
                self.publish_mode = "direct"
                do_publish()
            
            # 发布为草稿按钮
            def publish_draft():
                self.publish_mode = "draft"
                do_publish()
            
            # 执行发布
            def do_publish():
                # 更新发布状态
                selected_items = []
                for i, item in enumerate(publish_items):
                    if check_vars[i].get():
                        item['publish'] = True
                        item['video_path'] = video_path_vars[i].get()
                        item['cover_vertical'] = cover_v_vars[i].get()
                        item['cover_horizontal'] = cover_h_vars[i].get()
                        item['publish_date'] = publish_date_vars[i].get()
                        selected_items.append(item)
                    else:
                        item['publish'] = False
                
                if not selected_items:
                    messagebox.showwarning("提示", "请至少选择一个要发布的视频！")
                    return
                
                # 检查是否有视频缺失
                missing_videos = [item for item in selected_items if not item['video_path']]
                if missing_videos:
                    result = messagebox.askokcancel("警告", f"有 {len(missing_videos)} 个视频文件未找到，是否继续发布其他视频？")
                    if not result:
                        return
                
                # 保存选中的发布项和发布模式
                self.publish_items = selected_items
                
                confirm_window.destroy()
            
            # 取消发布按钮
            cancel_btn = ttk.Button(btn_frame, text="取消发布", command=confirm_window.destroy)
            cancel_btn.pack(side=tk.RIGHT, padx=5)
            
            # 发布为草稿按钮
            draft_btn = ttk.Button(btn_frame, text="发布为草稿", command=publish_draft)
            draft_btn.pack(side=tk.RIGHT, padx=5)
            
            # 正式发布按钮
            direct_btn = ttk.Button(btn_frame, text="正式发布", command=publish_direct)
            direct_btn.pack(side=tk.RIGHT, padx=5)
            
            # 等待弹窗关闭
            confirm_window.wait_window()
            
            # 返回选中的发布项
            if hasattr(self, 'publish_items'):
                return self.publish_items
            return None
            
        except Exception as e:
            self.logger.error(f"显示发布确认弹窗出错: {str(e)}")
            messagebox.showerror("错误", f"显示发布确认弹窗出错: {str(e)}")
            return None
    
    def show_publish_result(self, result_file):
        """显示发布结果弹窗
        
        规则：
        - 表格展示：视频名称、发布平台、提交方式、运行状态、备注信息
        - 弹窗内置按钮：【打开本次日志文件】
        """
        try:
            import json
            
            with open(result_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            results = data.get('results', [])
            total_count = data.get('total_count', 0)
            success_count = data.get('success_count', 0)
            fail_count = data.get('fail_count', 0)
            
            result_window = tk.Toplevel(self.root)
            result_window.title("发布结果")
            result_window.geometry("1000x500")
            result_window.resizable(True, True)
            
            # 统计信息
            stats_frame = ttk.Frame(result_window, padding="10")
            stats_frame.pack(fill=tk.X)
            
            ttk.Label(stats_frame, text=f"发布时间: {data.get('publish_time', '')}").pack(side=tk.LEFT, padx=10)
            ttk.Label(stats_frame, text=f"总数量: {total_count}").pack(side=tk.LEFT, padx=10)
            ttk.Label(stats_frame, text=f"成功: {success_count}", foreground='green').pack(side=tk.LEFT, padx=10)
            ttk.Label(stats_frame, text=f"失败: {fail_count}", foreground='red').pack(side=tk.LEFT, padx=10)
            
            # 创建表格框架
            frame = ttk.Frame(result_window)
            frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # 表格列：视频名称、发布平台、提交方式、运行状态、备注信息
            tree = ttk.Treeview(frame, yscrollcommand=scrollbar.set,
                                columns=('video_name', 'platform', 'submit_mode', 'status', 'message'),
                                show='headings')
            tree.pack(fill=tk.BOTH, expand=True)
            scrollbar.config(command=tree.yview)
            
            tree.heading('video_name', text='视频名称')
            tree.heading('platform', text='发布平台')
            tree.heading('submit_mode', text='提交方式')
            tree.heading('status', text='运行状态')
            tree.heading('message', text='备注信息')
            
            tree.column('video_name', width=200)
            tree.column('platform', width=100)
            tree.column('submit_mode', width=100)
            tree.column('status', width=80)
            tree.column('message', width=300)
            
            for result in results:
                # 提交方式：正式发布 或 存草稿
                submit_mode_text = '正式发布' if result.get('submit_mode') == 'publish' else '存草稿'
                
                tree.insert('', tk.END, values=(
                    result.get('video_name', ''),
                    result.get('platform', ''),
                    submit_mode_text,
                    result.get('status', ''),
                    result.get('message', '')
                ))
            
            def open_log_file():
                """打开本次日志文件"""
                logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
                if os.path.exists(logs_dir):
                    log_files = []
                    for root, dirs, files in os.walk(logs_dir):
                        for f in files:
                            if f.endswith('.log'):
                                log_files.append(os.path.join(root, f))
                    
                    if log_files:
                        latest_log = max(log_files, key=os.path.getmtime)
                        import subprocess
                        subprocess.run(['start', '', latest_log], shell=True)
            
            btn_frame = ttk.Frame(result_window, padding="10")
            btn_frame.pack(fill=tk.X)
            
            open_log_btn = ttk.Button(btn_frame, text="打开本次日志文件", command=open_log_file)
            open_log_btn.pack(side=tk.RIGHT, padx=5)
            
            close_btn = ttk.Button(btn_frame, text="关闭", command=result_window.destroy)
            close_btn.pack(side=tk.RIGHT, padx=5)
            
        except Exception as e:
            self.logger.error(f"显示发布结果出错: {str(e)}")
            messagebox.showerror("错误", f"显示发布结果出错: {str(e)}")

def main():
    root = tk.Tk()
    app = VideoPublisherGUI(root)
    root.mainloop()

if __name__ == "__main__":
    import pandas as pd
    main()
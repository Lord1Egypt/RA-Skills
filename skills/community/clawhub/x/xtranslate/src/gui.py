import os
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
from config_loader import CONFIG
from main import process_file
from cad_handler import CADHandler
from crypto_utils import crypto
import threading

# 设置外观
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# 定义“小三”字体大小 (约 15pt)
XIAO_SAN_FONT_SIZE = 15

class ReviewDialog(ctk.CTkToplevel):
    """人工审核对话框，用于 CAD 文字翻译后的确认"""
    def __init__(self, parent, translation_data, on_approve):
        super().__init__(parent)
        self.title("人工审核 - 翻译内容确认")
        self.geometry("800x600")
        self.on_approve = on_approve
        self.translation_data = translation_data # {original: translated}
        self.approved_data = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.label = ctk.CTkLabel(self, text="请检查并修改翻译内容，点击确认后将回写至 CAD 文件", font=ctk.CTkFont(size=16, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=10)

        # 滚动区域
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.scroll_frame.grid_columnconfigure(1, weight=1)

        self.entries = {}
        for i, (original, translated) in enumerate(self.translation_data.items()):
            lbl = ctk.CTkLabel(self.scroll_frame, text=original, anchor="w", wraplength=350)
            lbl.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            
            entry = ctk.CTkEntry(self.scroll_frame, width=350)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            entry.insert(0, translated)
            self.entries[original] = entry

        # 按钮
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=2, column=0, padx=20, pady=20)

        self.approve_btn = ctk.CTkButton(self.btn_frame, text="确认并保存", fg_color="green", command=self.do_approve)
        self.approve_btn.grid(row=0, column=0, padx=10)

        self.cancel_btn = ctk.CTkButton(self.btn_frame, text="取消", fg_color="gray", command=self.destroy)
        self.cancel_btn.grid(row=0, column=1, padx=10)

    def do_approve(self):
        for original, entry in self.entries.items():
            self.approved_data[original] = entry.get()
        self.on_approve(self.approved_data)
        self.destroy()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f"Xtranslate {CONFIG['VERSION']} - 智能翻译工具")
        self.geometry("900x700") # 调大一点窗口以适应字体

        # 布局
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 默认字体
        self.default_font = ctk.CTkFont(size=XIAO_SAN_FONT_SIZE)
        self.bold_font = ctk.CTkFont(size=XIAO_SAN_FONT_SIZE + 2, weight="bold")

        # 侧边栏
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Xtranslate", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.engine_label = ctk.CTkLabel(self.sidebar_frame, text="选择翻译引擎:", anchor="w", font=self.default_font)
        self.engine_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.engine_option = ctk.CTkOptionMenu(self.sidebar_frame, values=["cloud", "ollama", "python (不推荐)"], command=self.change_engine, font=self.default_font)
        self.engine_option.grid(row=2, column=0, padx=20, pady=10)
        self.engine_option.set(CONFIG.get("TRANSLATE_ENGINE", "cloud"))

        # 云模型选择
        self.model_label = ctk.CTkLabel(self.sidebar_frame, text="选择具体模型:", anchor="w", font=self.default_font)
        self.model_label.grid(row=3, column=0, padx=20, pady=(10, 0))
        model_list = list(CONFIG.get("CLOUD_MODELS", {}).keys())
        self.model_option = ctk.CTkOptionMenu(self.sidebar_frame, values=model_list, command=self.change_model, font=self.default_font)
        self.model_option.grid(row=4, column=0, padx=20, pady=10)
        self.model_option.set(CONFIG.get("CURRENT_CLOUD_MODEL", "DeepSeek (V3/R1)"))

        # 自定义模型输入 (初始隐藏)
        self.custom_url_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="API Base URL (如: https://...)", font=self.default_font)
        self.custom_model_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Model Name (如: gpt-4)", font=self.default_font)
        
        # 翻译方向设置
        self.lang_label = ctk.CTkLabel(self.sidebar_frame, text="选择翻译方向:", anchor="w", font=self.default_font)
        self.lang_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.lang_option = ctk.CTkOptionMenu(self.sidebar_frame, 
                                            values=["英 -> 中", "中 -> 英", "塞 -> 中", "中 -> 塞"], 
                                            command=self.change_lang, font=self.default_font)
        self.lang_option.grid(row=6, column=0, padx=20, pady=10)
        
        # 根据 config 初始值设置
        target_lang = CONFIG.get("TARGET_LANG")
        if target_lang == "en":
            self.lang_option.set("中 -> 英")
        elif target_lang == "sr":
            self.lang_option.set("中 -> 塞")
        elif CONFIG.get("SOURCE_LANG") == "sr":
            self.lang_option.set("塞 -> 中")
        else:
            self.lang_option.set("英 -> 中")

        # API Key 设置
        self.key_label = ctk.CTkLabel(self.sidebar_frame, text="API Key (已加密):", anchor="w", font=self.default_font)
        self.key_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.key_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="输入 API Key", show="*", font=self.default_font)
        self.key_entry.grid(row=8, column=0, padx=20, pady=10)
        
        # 加密并保存按钮
        self.save_key_button = ctk.CTkButton(self.sidebar_frame, text="加密并保存 Key", command=self.save_key, font=self.default_font)
        self.save_key_button.grid(row=9, column=0, padx=20, pady=10)

        # 侧边栏底部留白
        self.sidebar_frame.grid_rowconfigure(10, weight=1)

        # 帮助按钮
        self.help_button = ctk.CTkButton(self.sidebar_frame, text="使用说明", fg_color="gray", hover_color="#555555", command=self.show_help, font=self.default_font)
        self.help_button.grid(row=11, column=0, padx=20, pady=20)

        # 主内容区
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(self.main_frame, text="文件翻译任务", font=self.bold_font)
        self.title_label.grid(row=0, column=0, padx=20, pady=10)

        # 文件列表显示
        self.textbox = ctk.CTkTextbox(self.main_frame, width=250, font=self.default_font)
        self.textbox.grid(row=1, column=0, padx=(20, 20), pady=(10, 10), sticky="nsew")

        # 底部按钮
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.grid(row=2, column=0, padx=20, pady=20)
        
        self.select_button = ctk.CTkButton(self.button_frame, text="选择文件/文件夹", command=self.select_files, font=self.default_font)
        self.select_button.grid(row=0, column=0, padx=10)
        
        self.start_button = ctk.CTkButton(self.button_frame, text="开始翻译", fg_color="green", hover_color="darkgreen", command=self.start_translation, font=self.default_font)
        self.start_button.grid(row=0, column=1, padx=10)

        self.files_to_translate = []

    def change_engine(self, engine_label):
        engine = engine_label.split(" ")[0] # 提取 "cloud", "ollama", "python"
        CONFIG["TRANSLATE_ENGINE"] = engine
        self.log(f"已切换主引擎为: {engine}")
        
        # 如果不是云引擎，隐藏模型选择框
        if engine == "cloud":
            self.model_option.configure(state="normal")
        else:
            self.model_option.configure(state="disabled")
            
        if engine == "python":
            messagebox.showwarning("翻译质量警告", "内置翻译引擎质量较差，且单次请求长度受限，仅推荐作为紧急情况下的兜底方案。建议使用云端或 Ollama 模型。")

    def change_model(self, model_name):
        CONFIG["CURRENT_CLOUD_MODEL"] = model_name
        model_info = CONFIG["CLOUD_MODELS"][model_name]
        self.log(f"云模型已切换为: {model_name}")
        
        # 处理自定义模型的显示/隐藏
        if model_name == "自定义 (OpenAI 兼容)":
            self.custom_url_entry.grid(row=10, column=0, padx=20, pady=(5, 5))
            self.custom_model_entry.grid(row=11, column=0, padx=20, pady=(5, 10))
            self.custom_url_entry.delete(0, tk.END)
            self.custom_url_entry.insert(0, model_info.get("base_url", ""))
            self.custom_model_entry.delete(0, tk.END)
            self.custom_model_entry.insert(0, model_info.get("model", ""))
        else:
            self.custom_url_entry.grid_forget()
            self.custom_model_entry.grid_forget()

        # 提示用户可能需要更新 API Key
        env_key = model_info.get("env_key", "API_KEY")
        self.key_label.configure(text=f"{env_key} (已加密):")

    def change_lang(self, lang_text):
        if lang_text == "英 -> 中":
            CONFIG["SOURCE_LANG"] = "auto"
            CONFIG["TARGET_LANG"] = "zh-CN"
            self.log("已设置翻译方向: 英语 -> 中文")
        elif lang_text == "中 -> 英":
            CONFIG["SOURCE_LANG"] = "auto"
            CONFIG["TARGET_LANG"] = "en"
            self.log("已设置翻译方向: 中文 -> 英语")
        elif lang_text == "塞 -> 中":
            CONFIG["SOURCE_LANG"] = "sr"
            CONFIG["TARGET_LANG"] = "zh-CN"
            self.log("已设置翻译方向: 塞尔维亚语 -> 中文")
        elif lang_text == "中 -> 塞":
            CONFIG["SOURCE_LANG"] = "zh-CN"
            CONFIG["TARGET_LANG"] = "sr"
            self.log("已设置翻译方向: 中文 -> 塞尔维亚语")

    def save_key(self):
        raw_key = self.key_entry.get()
        if not raw_key:
            messagebox.showwarning("警告", "请输入 API Key")
            return
        
        # 确定要保存到哪个配置项
        current_model = CONFIG.get("CURRENT_CLOUD_MODEL", "DeepSeek (V3/R1)")
        model_info = CONFIG["CLOUD_MODELS"].get(current_model, CONFIG["CLOUD_MODELS"]["DeepSeek (V3/R1)"])
        target_env_key = model_info.get("env_key", "DEEPSEEK_API_KEY")
        
        # 如果是自定义模型，还要保存 URL 和 Model Name
        if current_model == "自定义 (OpenAI 兼容)":
            custom_url = self.custom_url_entry.get()
            custom_model_name = self.custom_model_entry.get()
            if not custom_url or not custom_model_name:
                messagebox.showwarning("警告", "自定义模型请填写 API URL 和 Model Name")
                return
            model_info["base_url"] = custom_url
            model_info["model"] = custom_model_name
            self.log(f"已更新自定义模型配置: {custom_model_name}")

        encrypted_key = crypto.encrypt(raw_key)
        CONFIG[target_env_key] = encrypted_key
        
        # 记录日志
        self.log(f"API Key 已保存至配置项: {target_env_key}")
        self.key_entry.delete(0, tk.END)
        messagebox.showinfo("成功", f"API Key 已加密并保存到 {target_env_key}")

    def show_help(self):
        help_text = f"""Xtranslate {CONFIG['VERSION']} 使用说明

1. 选择引擎:
   - cloud: 云端模型 (推荐)，质量最高。
   - ollama: 本地模型，适合隐私和离线环境。
   - python: 内置引擎，仅作备用。

2. 选择模型:
   - 支持 DeepSeek, GPT-4o, Claude 等主流模型。
   - 选中“自定义”可输入自己的 API 地址和模型名。

3. 翻译方向:
   - 支持英中、中英互译。
   - 特色支持：塞尔维亚语 (sr) 与中文互译。

4. 更多格式支持 (特色功能):
   - 除了 PDF/Word/TXT，还支持 Excel (.xlsx)、PPT (.pptx)、RTF 以及 CAD (.dxf, .dwg) 格式。
   - CAD 文件采用去重提取技术，并支持人工审核确认后再回写。

5. 自动排版:
   - PDF/Word 翻译完成后，系统会自动统一字体（宋体/Times New Roman）并设置 1.25 倍行间距。

6. API Key:
   - 输入 Key 后点击“加密并保存”，Key 将以加密形式存储，确保安全。
"""
        messagebox.showinfo("Xtranslate 使用指南", help_text)

    def select_files(self):
        # 允许选择所有支持的格式
        allowed_exts = "*.docx *.pdf *.txt *.xlsx *.pptx *.rtf *.wps *.dxf *.dwg"
        paths = filedialog.askopenfilenames(title="选择文件", filetypes=[("所有支持的格式", allowed_exts), ("Word", "*.docx *.wps"), ("Excel", "*.xlsx"), ("PPT", "*.pptx"), ("PDF", "*.pdf"), ("CAD", "*.dxf *.dwg"), ("文本", "*.txt *.rtf")])
        if not paths:
            # 尝试选择文件夹
            folder = filedialog.askdirectory(title="选择文件夹")
            if folder:
                from file_handler import FileHandler
                paths = FileHandler.get_all_files(folder)
        
        if paths:
            self.files_to_translate.extend(paths)
            self.log(f"已添加 {len(paths)} 个文件")
            for p in paths:
                self.textbox.insert("end", f"待翻译: {p}\n")

    def log(self, message):
        self.textbox.insert("end", f"{message}\n")
        self.textbox.see("end")

    def start_translation(self):
        if not self.files_to_translate:
            messagebox.showwarning("警告", "请先选择文件")
            return
            
        # 前置检查: 如果是云引擎，必须有 API Key
        engine_type = CONFIG.get("TRANSLATE_ENGINE", "cloud")
        if engine_type == "cloud":
            current_model = self.model_option.get()
            model_info = CONFIG["CLOUD_MODELS"].get(current_model, CONFIG["CLOUD_MODELS"]["DeepSeek (V3/R1)"])
            env_key_name = model_info.get("env_key", "DEEPSEEK_API_KEY")
            
            # 从环境变量或 CONFIG 字典中查找
            raw_key = os.getenv(env_key_name, CONFIG.get(env_key_name, ""))
            api_key = crypto.decrypt(raw_key)
            
            if not api_key:
                 messagebox.showerror("无法开始翻译", 
                     "检测到云端模型 API Key 尚未设置！\n\n"
                     "请执行以下操作：\n"
                     "1. 在左侧输入框填入 Key 并点击“加密并保存 Key”；\n"
                     "2. 切换为 'ollama' 使用本地大模型（需安装 Ollama）；\n"
                     "3. 或切换为 'python' 使用内置库翻译（速度较慢且质量一般）。\n\n"
                     "提示：本地模型（ollama/python）翻译质量较云端模型稍差，但完全免费且保护隐私。")
                 return # 停止运行，不进入翻译流程

        self.start_button.configure(state="disabled", text="正在翻译...")
        threading.Thread(target=self.run_translation, daemon=True).start()

    def run_translation(self):
        # 获取当前 UI 选中的模型名称
        current_model = self.model_option.get()
        engine_type = CONFIG.get("TRANSLATE_ENGINE", "cloud")
        
        for file_path in self.files_to_translate:
            self.log(f"正在处理: {os.path.basename(file_path)}...")
            
            # CAD 文件特殊流程 (DXF/DWG)
            ext = os.path.splitext(file_path)[1].lower()
            if ext in ['.dxf', '.dwg']:
                if ext == '.dwg':
                    self.after(0, lambda p=file_path: messagebox.showwarning("格式警告", 
                        f"检测到 DWG 文件: {os.path.basename(p)}\n\n"
                        "目前底层引擎主要支持 DXF 格式。建议您先将 DWG 另存为或转换为 DXF R2018/R2010 格式以获得最佳兼容性。"))
                    if ext == '.dwg' and not os.path.exists(file_path.replace('.dwg', '.dxf')):
                        self.log(f"跳过 DWG: {os.path.basename(file_path)} (请先转换为 DXF)")
                        continue
                
                # 执行 CAD 流程
                self._handle_cad_translation(file_path, engine_type, current_model)
                continue

            try:
                # 普通文件流程 (Word/PDF/TXT/XLSX/PPTX/RTF)
                success, result = process_file(file_path, engine_type=engine_type, cloud_model=current_model)
                if success:
                    self.log(f"成功: {os.path.basename(file_path)}")
                    if CONFIG.get("AUTO_FORMAT_LAYOUT", True) and file_path.lower().endswith(('.docx', '.pdf')):
                        self.log(f"  └─ 排版优化已完成")
                else:
                    self.log(f"失败: {os.path.basename(file_path)} - {result}")
            except Exception as e:
                self.log(f"发生异常: {str(e)}")
        
        self.files_to_translate = []
        self.after(0, lambda: self.start_button.configure(state="normal", text="开始翻译"))
        messagebox.showinfo("完成", "任务处理结束")

    def _handle_cad_translation(self, file_path, engine, model):
        """处理 CAD 翻译：提取 -> 翻译 -> 审核 -> 替换"""
        from translator import TranslatorModule
        
        # 1. 提取文本
        self.log(f"  [CAD] 正在提取文本...")
        original_texts = CADHandler.extract_texts(file_path)
        if not original_texts:
            self.log(f"  [CAD] 未发现可翻译文字或格式不支持")
            return

        # 2. 批量翻译
        self.log(f"  [CAD] 正在翻译 {len(original_texts)} 条去重后的文字...")
        translator = TranslatorModule(engine=engine, target_lang=CONFIG["TARGET_LANG"])
        translated_list = translator.translate_list(original_texts)
        
        translation_map = dict(zip(original_texts, translated_list))

        # 3. 调起审核窗口 (主线程)
        def on_approve(final_map):
            self.log(f"  [CAD] 审核通过，正在回写至文件...")
            output_name = f"translated_{os.path.basename(file_path)}"
            output_path = os.path.join(CONFIG.get("OUTPUT_DIR", "output"), output_name)
            
            res_path = CADHandler.replace_texts(file_path, final_map, output_path)
            if res_path:
                self.log(f"  [CAD] 成功保存至: {res_path}")
            else:
                self.log(f"  [CAD] 保存失败")

        self.after(0, lambda: ReviewDialog(self, translation_map, on_approve))


if __name__ == "__main__":
    app = App()
    app.mainloop()

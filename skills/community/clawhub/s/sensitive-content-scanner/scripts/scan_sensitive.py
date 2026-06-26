#!/usr/bin/env python3
"""
敏感内容扫描器 v3.2.0
检测文件名和文件内容中的敏感词、违禁词、PII个人信息
支持自定义关键词、数据字典、权重评分
支持格式：docx、xlsx、pptx、txt、md等
"""

import os
import re
import json
import csv
import hashlib
import argparse
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional, Union
import mimetypes


class WeightedDictionary:
    """数据字典类，管理关键词和权重"""
    
    def __init__(self):
        self.keywords: Dict[str, float] = {}  # 关键词 -> 权重分
        self.categories: Dict[str, str] = {}   # 关键词 -> 类别
        self.threshold: float = 10.0          # 报告阈值
    
    def add_word(self, word: str, weight: float, category: str = "自定义"):
        """添加关键词"""
        word_lower = word.lower().strip()
        if word_lower:
            self.keywords[word_lower] = weight
            self.categories[word_lower] = category
    
    def load_from_csv(self, csv_path: str):
        """从 CSV 文件加载数据字典"""
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    keyword = row.get('关键词', row.get('keyword', '')).strip()
                    weight_str = row.get('权重分', row.get('weight', '5')).strip()
                    category = row.get('类别', row.get('category', '自定义')).strip()
                    
                    if keyword:
                        try:
                            weight = float(weight_str)
                        except ValueError:
                            weight = 5.0  # 默认权重
                        
                        self.add_word(keyword, weight, category)
        except Exception as e:
            print(f"警告: 加载 CSV 文件失败 {csv_path}: {e}")
    
    def load_from_json(self, json_path: str):
        """从 JSON 文件加载数据字典"""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # 处理 JSON 格式 1: {"关键词": 权重分, ...}
                if isinstance(data, dict):
                    # 检查是否是标准格式
                    if 'keywords' in data or 'words' in data:
                        words = data.get('keywords', data.get('words', {}))
                        for word, weight in words.items():
                            if isinstance(weight, (int, float)):
                                self.add_word(word, float(weight))
                    elif '权重等级' in data:
                        # 处理标准格式
                        level_weights = data.get('权重等级', {})
                        for word, info in data.get('关键词', data.get('keywords', {})).items():
                            if isinstance(info, dict):
                                weight = info.get('权重分', info.get('weight', 5))
                                category = info.get('类别', info.get('category', '自定义'))
                            else:
                                weight = info
                                category = '自定义'
                            self.add_word(word, weight, category)
                    else:
                        # 简单格式: {"关键词": 权重分}
                        for word, weight in data.items():
                            if isinstance(weight, (int, float)):
                                self.add_word(word, float(weight))
        except Exception as e:
            print(f"警告: 加载 JSON 文件失败 {json_path}: {e}")
    
    def load_from_text(self, text: str):
        """从文本加载关键词（每行一个，默认权重 5）"""
        lines = text.strip().split('\n')
        for line in lines:
            word = line.strip()
            if word and not word.startswith('#'):
                self.add_word(word, 5.0)
    

    # ================================================================
    # 行业数据字典加密加载（仅限 scanner 使用）
    # 安全机制：AES-256-CBC + HMAC-SHA256 + 密码绑定scanner身份
    # ================================================================

    @staticmethod
    def _get_dict_password() -> str:
        """生成字典解密密码 - 与 dict_crypto.py 中的 get_scanner_password() 保持一致"""
        _seed = (
            "SensitiveContentScannerV310"
            "WeightedDictionary"
            "PIIPatternChecker"
            "DataDictionaryChecker"
            "SensitiveWordChecker"
        )
        h = hashlib.sha256()
        h.update(_seed.encode('utf-8'))
        h.update("0001".encode())
        h.update(b"SCDICT01")
        return h.hexdigest()

    @staticmethod
    def _derive_key(password: str, salt: bytes, iterations: int = 100000) -> bytes:
        """PBKDF2 密钥派生"""
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),
                                   salt, iterations, dklen=32)

    def load_from_encrypted_dict(self, enc_path: str):
        """
        从加密的 .enc 文件加载数据字典（内部自动解密）

        Args:
            enc_path: 加密文件路径 (.enc)

        Raises:
            ValueError: 格式错误或篡改检测失败
            PermissionError: 非授权访问
        """
        from Crypto.Cipher import AES
        import hmac as hmac_mod

        MAGIC = b"SCDICT01"
        SALT_LEN, IV_LEN, HMAC_LEN = 16, 16, 32
        BLOCK_SIZE = 16

        with open(enc_path, 'rb') as f:
            data = f.read()

        min_size = len(MAGIC) + 2 + SALT_LEN + IV_LEN + BLOCK_SIZE + HMAC_LEN
        if len(data) < min_size:
            raise ValueError(f"字典文件异常 ({len(data)} < {min_size})")

        off = 0
        magic = data[off:off+len(MAGIC)]; off += len(MAGIC)
        if magic != MAGIC:
            raise ValueError("非法字典文件：非 Scanner 授权格式")
        ver = int.from_bytes(data[off:off+2], 'big'); off += 2
        if ver != 1:
            raise ValueError(f"不支持的字典版本: {ver}")
        salt = data[off:off+SALT_LEN]; off += SALT_LEN
        iv = data[off:off+IV_LEN]; off += IV_LEN
        ciphertext = data[off:-HMAC_LEN]
        received_mac = data[-HMAC_LEN:]

        pwd = self._get_dict_password()
        key = self._derive_key(pwd, salt)
        expected_mac = hmac_mod.new(key, salt + iv + ciphertext, hashlib.sha256).digest()
        if not hmac_mod.compare_digest(received_mac, expected_mac):
            raise PermissionError(
                "字典完整性校验失败！\n可能原因：文件被篡改 / 非授权程序尝试使用"
            )

        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded = cipher.decrypt(ciphertext)
        pad_len = padded[-1]
        if not (1 <= pad_len <= BLOCK_SIZE) or padded[-pad_len:] != bytes([pad_len] * pad_len):
            raise ValueError("字典数据损坏")
        plaintext = padded[:-pad_len].decode('utf-8')

        jdata = json.loads(plaintext)
        meta = jdata.get('meta', {})
        categories = jdata.get('categories', {})
        industry = meta.get('industry', '未知')
        total_loaded = 0

        for cat_name, cat_info in categories.items():
            entries = cat_info.get('entries', [])
            for entry in entries:
                keywords = entry.get('keywords', [])
                weight = entry.get('weight', 5)
                sensitivity = entry.get('sensitivity', 3)
                final_weight = max(weight, sensitivity * 2)
                for kw in keywords:
                    self.add_word(kw, final_weight, f"{industry}/{cat_name}")
                    total_loaded += 1

        if hasattr(self, 'verbose') and self.verbose:
            print(f"已安全加载行业字典: {industry} ({total_loaded} 条规则)")

    def check(self, text: str) -> List[Dict]:
        """检查文本中是否包含数据字典中的关键词"""
        text_lower = text.lower()
        found = []
        
        for word, weight in self.keywords.items():
            if word in text_lower:
                found.append({
                    'keyword': word,
                    'weight': weight,
                    'category': self.categories.get(word, '自定义')
                })
        
        return found
    
    def calculate_risk_score(self, matches: List[Dict]) -> Dict:
        """计算风险评分"""
        if not matches:
            return {
                'level': 'safe',
                'score': 0,
                'max_weight': 0,
                'count': 0
            }
        
        total_score = sum(m['weight'] for m in matches)
        max_weight = max(m['weight'] for m in matches)
        count = len(matches)
        
        # 确定风险等级
        if total_score >= 50 or max_weight >= 10:
            level = 'high'
        elif total_score >= 20 or max_weight >= 5:
            level = 'medium'
        else:
            level = 'low'
        
        return {
            'level': level,
            'score': total_score,
            'max_weight': max_weight,
            'count': count
        }


class SensitiveScanner:
    def __init__(self, custom_words_file: str = None, verbose: bool = False, 
                 enable_chinese_name: bool = False,
                 keywords: List[str] = None,
                 dict_csv: str = None,
                 dict_json: str = None,
                 dict_enc: str = None,
                 dict_text: str = None,
                 threshold: float = 10.0):
        self.verbose = verbose
        self.enable_chinese_name = enable_chinese_name
        self.sensitive_words_hashes = self._load_sensitive_words_hashes()
        self.pii_patterns = self._get_pii_patterns()
        self.custom_words = self._load_custom_words(custom_words_file)
        
        # 初始化数据字典
        self.dictionary = WeightedDictionary()
        self.dictionary.threshold = threshold
        
        # 加载数据字典
        if dict_csv:
            self.dictionary.load_from_csv(dict_csv)
        if dict_json:
            self.dictionary.load_from_json(dict_json)
        if dict_enc:
            self.dictionary.load_from_encrypted_dict(dict_enc)
        if dict_text:
            self.dictionary.load_from_text(dict_text)
        if keywords:
            for kw in keywords:
                self.dictionary.add_word(kw, 5.0, '命令行关键词')
        
        # 常见中文姓氏（用于改进姓名检测）
        self.common_surnames = set([
            '赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈',
            '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
            '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏',
            '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
            '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦',
            '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
            '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺',
            '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
            '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余',
            '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹'
        ])
        
    def _load_sensitive_words_hashes(self) -> Set[str]:
        """加载预置的敏感词hash库"""
        hash_file = Path(__file__).parent.parent / "references" / "sensitive_words_hashed.txt"
        hashes = set()
        
        if hash_file.exists():
            with open(hash_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        hashes.add(line)
        
        return hashes
    
    def _load_custom_words(self, custom_words_file: str) -> Set[str]:
        """加载自定义敏感词库"""
        custom_words = set()
        
        if custom_words_file and Path(custom_words_file).exists():
            with open(custom_words_file, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if word and not line.startswith('#'):
                        custom_words.add(word.lower())
        
        return custom_words
    
    def _get_pii_patterns(self) -> Dict[str, re.Pattern]:
        """获取PII识别模式"""
        patterns = {
            # 身份证号
            'china_id_card': re.compile(
                r'\b[1-9]\d{5}(?:18|19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]\b'
            ),
            # 手机号
            'china_phone': re.compile(r'\b1[3-9]\d{9}\b'),
            # 银行卡号
            'china_bank_card': re.compile(r'\b\d{16,19}\b'),
            # 邮箱
            'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            # IP地址
            'ip_address': re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),
            # 护照号
            'china_passport': re.compile(r'\b[SE]\d{8}\b'),
        }
        
        # 中文姓名检测（默认禁用）
        if self.enable_chinese_name:
            patterns['chinese_name'] = re.compile(r'[\u4e00-\u9fa5]{2,4}')
        
        return patterns
    
    def _validate_id_card(self, id_card: str) -> bool:
        """验证身份证号校验码"""
        if len(id_card) != 18:
            return False
        
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
        
        try:
            total = sum(int(id_card[i]) * weights[i] for i in range(17))
            check_code = check_codes[total % 11]
            return id_card[-1].upper() == check_code
        except:
            return False
    
    def _validate_bank_card(self, card_number: str) -> bool:
        """验证银行卡号（Luhn 算法）"""
        if not card_number.isdigit():
            return False
        
        digits = [int(d) for d in card_number]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        
        total = sum(odd_digits)
        for d in even_digits:
            d *= 2
            if d > 9:
                d = d // 10 + d % 10
            total += d
        
        return total % 10 == 0
    
    def _validate_ip_address(self, ip: str) -> bool:
        """验证 IP 地址范围"""
        try:
            parts = [int(p) for p in ip.split('.')]
            return all(0 <= p <= 255 for p in parts)
        except:
            return False
    
    def _validate_chinese_name(self, name: str) -> Tuple[bool, str]:
        """验证中文姓名"""
        if not self.enable_chinese_name:
            return False, 'disabled'
        
        if len(name) < 2 or len(name) > 4:
            return False, 'low'
        
        if name[0] in self.common_surnames:
            return True, 'medium'
        
        return True, 'low'
    
    def _hash_word(self, word: str) -> str:
        """计算词的SHA256 hash"""
        return hashlib.sha256(word.encode('utf-8')).hexdigest()
    
    def _is_text_file(self, file_path: Path) -> bool:
        """判断是否为文本文件"""
        try:
            text_extensions = {
                '.txt', '.md', '.markdown', '.rst', '.doc', '.docx',
                '.json', '.yaml', '.yml', '.xml', '.html', '.htm',
                '.csv', '.tsv', '.log', '.conf', '.cfg', '.ini',
                '.py', '.js', '.ts', '.java', '.c', '.cpp', '.h',
                '.sh', '.bash', '.zsh', '.fish', '.ps1', '.bat'
            }
            
            if file_path.suffix.lower() in text_extensions:
                return True
            
            mime_type, _ = mimetypes.guess_type(str(file_path))
            return mime_type and mime_type.startswith('text/')
        except:
            return False
    
    def _read_file_content(self, file_path: Path) -> str:
        """读取文件内容"""
        suffix = file_path.suffix.lower()
        
        # 处理 .docx 文件
        if suffix == '.docx':
            try:
                from docx import Document
                doc = Document(file_path)
                full_text = []
                for para in doc.paragraphs:
                    full_text.append(para.text)
                # 同时读取表格内容
                for table in doc.tables:
                    for row in table.rows:
                        row_text = []
                        for cell in row.cells:
                            row_text.append(cell.text)
                        full_text.append(' '.join(row_text))
                return '\n'.join(full_text)
            except Exception as e:
                if self.verbose:
                    print(f"读取docx文件失败 {file_path}: {e}")
                return ""
        
        # 处理 .xlsx 文件
        if suffix == '.xlsx':
            try:
                from openpyxl import load_workbook
                wb = load_workbook(file_path, data_only=True)
                full_text = []
                for sheet in wb.worksheets:
                    for row in sheet.iter_rows():
                        row_text = []
                        for cell in row:
                            if cell.value is not None:
                                row_text.append(str(cell.value))
                        if row_text:
                            full_text.append(' '.join(row_text))
                return '\n'.join(full_text)
            except Exception as e:
                if self.verbose:
                    print(f"读取xlsx文件失败 {file_path}: {e}")
                return ""
        
        # 处理 .pptx 文件
        if suffix == '.pptx':
            try:
                from pptx import Presentation
                prs = Presentation(file_path)
                full_text = []
                for slide in prs.slides:
                    for shape in slide.shapes:
                        if hasattr(shape, "text"):
                            full_text.append(shape.text)
                return '\n'.join(full_text)
            except Exception as e:
                if self.verbose:
                    print(f"读取pptx文件失败 {file_path}: {e}")
                return ""
        
        # 处理普通文本文件
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    return f.read()
            except:
                return ""
        except Exception as e:
            if self.verbose:
                print(f"读取文件失败 {file_path}: {e}")
                return ""
    
    def check_hashed_words(self, text: str) -> List[str]:
        """检查文本中是否包含hash敏感词"""
        found = []
        words = re.findall(r'[\u4e00-\u9fa5]+|[a-zA-Z]+|\d+', text)
        
        for word in words:
            word_hash = self._hash_word(word.lower())
            if word_hash in self.sensitive_words_hashes:
                found.append(word)
        
        return found
    
    def check_custom_words(self, text: str) -> List[str]:
        """检查自定义敏感词"""
        text_lower = text.lower()
        found = []
        
        for word in self.custom_words:
            if word in text_lower:
                found.append(word)
        
        return found
    
    def check_pii(self, text: str) -> Dict[str, List[Dict]]:
        """检查PII信息"""
        found = {}
        
        for pii_type, pattern in self.pii_patterns.items():
            matches = pattern.findall(text)
            if matches:
                matches = list(set(matches))
                validated_matches = []
                
                for match in matches:
                    confidence = 'low'
                    display_value = match
                    
                    if pii_type == 'china_id_card':
                        if self._validate_id_card(match):
                            confidence = 'high'
                        else:
                            confidence = 'medium'
                        display_value = f"{match[:3]}***{match[-2:]}"
                    
                    elif pii_type == 'china_phone':
                        confidence = 'high'
                        display_value = f"{match[:3]}****{match[-2:]}"
                    
                    elif pii_type == 'china_bank_card':
                        if self._validate_bank_card(match):
                            confidence = 'high'
                        else:
                            confidence = 'low'
                        display_value = f"{match[:3]}***{match[-2:]}"
                    
                    elif pii_type == 'ip_address':
                        if self._validate_ip_address(match):
                            confidence = 'high'
                        else:
                            confidence = 'low'
                    
                    elif pii_type == 'email':
                        confidence = 'high'
                        parts = match.split('@')
                        if len(parts[0]) > 3:
                            display_value = f"{parts[0][:3]}***@{parts[1]}"
                    
                    elif pii_type == 'china_passport':
                        confidence = 'high'
                        display_value = f"{match[:1]}***{match[-2:]}"
                    
                    elif pii_type == 'chinese_name':
                        is_name, confidence = self._validate_chinese_name(match)
                        if not is_name:
                            continue
                    
                    validated_matches.append({
                        'value': display_value,
                        'confidence': confidence,
                        'original': match
                    })
                
                if validated_matches:
                    found[pii_type] = validated_matches
        
        return found
    
    def check_dictionary(self, text: str) -> Dict:
        """检查数据字典关键词"""
        matches = self.dictionary.check(text)
        risk_score = self.dictionary.calculate_risk_score(matches)
        
        return {
            'matches': matches,
            'risk_score': risk_score
        }
    
    def scan_file(self, file_path: Path) -> Dict:
        """扫描单个文件"""
        result = {
            'file_path': str(file_path),
            'file_name': file_path.name,
            'issues': []
        }
        
        # 检查文件名
        filename_issues = {}
        
        # 数据字典检查
        dict_result = self.check_dictionary(file_path.stem)
        if dict_result['matches']:
            filename_issues['dictionary'] = dict_result
        
        # hash敏感词
        hashed_in_filename = self.check_hashed_words(file_path.stem)
        if hashed_in_filename:
            filename_issues['hashed_sensitive_words'] = hashed_in_filename
        
        # 自定义敏感词
        custom_in_filename = self.check_custom_words(file_path.stem)
        if custom_in_filename:
            filename_issues['custom_sensitive_words'] = custom_in_filename
        
        # PII
        pii_in_filename = self.check_pii(file_path.stem)
        if pii_in_filename:
            filename_issues['pii'] = pii_in_filename
        
        if filename_issues:
            result['issues'].append({
                'location': 'filename',
                'problems': filename_issues
            })
        
        # 检查文件内容
        if self._is_text_file(file_path):
            content = self._read_file_content(file_path)
            
            if content:
                content_issues = {}
                
                # 数据字典检查
                dict_result = self.check_dictionary(content)
                if dict_result['matches']:
                    content_issues['dictionary'] = dict_result
                
                # hash敏感词
                hashed_in_content = self.check_hashed_words(content)
                if hashed_in_content:
                    content_issues['hashed_sensitive_words'] = list(set(hashed_in_content))
                
                # 自定义敏感词
                custom_in_content = self.check_custom_words(content)
                if custom_in_content:
                    content_issues['custom_sensitive_words'] = list(set(custom_in_content))
                
                # PII
                pii_in_content = self.check_pii(content)
                if pii_in_content:
                    content_issues['pii'] = pii_in_content
                
                if content_issues:
                    result['issues'].append({
                        'location': 'content',
                        'problems': content_issues
                    })
        
        return result
    
    def scan_directory(self, directory: Path, recursive: bool = True) -> List[Dict]:
        """扫描目录"""
        results = []
        
        if recursive:
            files = directory.rglob('*')
        else:
            files = directory.glob('*')
        
        for file_path in files:
            if file_path.is_file():
                result = self.scan_file(file_path)
                if result['issues']:
                    results.append(result)
                    if self.verbose:
                        print(f"发现问题: {file_path}")
        
        return results
    
    def generate_report(self, results: List[Dict], output_format: str = 'json') -> str:
        """生成报告"""
        if output_format == 'json':
            return json.dumps(results, ensure_ascii=False, indent=2)
        elif output_format == 'markdown':
            return self._generate_markdown_report(results)
        elif output_format == 'html':
            return self._generate_html_report(results)
        else:
            raise ValueError(f"不支持的输出格式: {output_format}")
    
    def _generate_markdown_report(self, results: List[Dict]) -> str:
        """生成 Markdown 报告"""
        if not results:
            return "# 敏感内容扫描报告\n\n✅ 未发现敏感内容\n"
        
        report = ["# 敏感内容扫描报告\n"]
        report.append(f"**扫描时间**: {self._get_current_time()}\n")
        report.append(f"**发现问题**: {len(results)} 个文件\n\n")
        
        # 统计信息
        stats = self._get_statistics(results)
        if stats:
            report.append("## 扫描统计\n\n")
            report.append(f"- 🔴 高危/高置信度: {stats['high']} 个\n")
            report.append(f"- 🟡 中危/中置信度: {stats['medium']} 个\n")
            report.append(f"- 🟢 低危/低置信度: {stats['low']} 个\n")
            report.append(f"- ✅ 安全: {stats['safe']} 个\n\n")
            
            # 数据字典统计
            if stats.get('dict_high', 0) > 0 or stats.get('dict_medium', 0) > 0 or stats.get('dict_low', 0) > 0:
                report.append("### 数据字典风险统计\n\n")
                report.append(f"- 高风险（总分≥50或最高权重≥10）: {stats.get('dict_high', 0)} 个\n")
                report.append(f"- 中风险（总分≥20或最高权重≥5）: {stats.get('dict_medium', 0)} 个\n")
                report.append(f"- 低风险: {stats.get('dict_low', 0)} 个\n\n")
        
        for idx, result in enumerate(results, 1):
            report.append(f"## {idx}. {result['file_path']}\n")
            
            for issue in result['issues']:
                location = "文件名" if issue['location'] == 'filename' else "文件内容"
                report.append(f"\n### {location}\n")
                
                for problem_type, items in issue['problems'].items():
                    if problem_type == 'dictionary':
                        self._add_dictionary_report(report, items)
                    elif problem_type == 'pii':
                        self._add_pii_report(report, items)
                    else:
                        self._add_word_report(report, problem_type, items)
            
            report.append("\n---\n")
        
        # 置信度说明
        report.append("\n## 风险等级说明\n\n")
        report.append("### 数据字典风险\n")
        report.append("- 🔴 **高风险**: 总分≥50 或 最高权重≥10，建议立即处理\n")
        report.append("- 🟡 **中风险**: 总分≥20 或 最高权重≥5，建议人工复核\n")
        report.append("- 🟢 **低风险**: 总分<20 且 最高权重<5，可选处理\n\n")
        
        report.append("### PII 置信度\n")
        report.append("- 🔴 **高置信度**: 已通过格式验证和校验码验证\n")
        report.append("- 🟡 **中置信度**: 格式匹配但未完全验证\n")
        report.append("- 🟢 **低置信度**: 仅符合基本模式，可能为误报\n")
        
        # 商业合作
        report.append("\n---\n\n")
        report.append("## 获取更准确的内容识别规则库\n\n")
        report.append("如需更全面的行业数据字典和定制化识别规则，请联系：\n\n")
        report.append("- **邮箱**: [support@soura.com.cn](mailto:support@soura.com.cn)\n")
        
        return ''.join(report)
    
    def _generate_html_report(self, results: List[Dict]) -> str:
        """生成 HTML 格式报告（v3.1.2 新增）"""
        stats = self._get_statistics(results) if results else None
        
        # 风险等级判定
        risk_level = 'safe'
        if stats:
            if stats['high'] > 0:
                risk_level = 'high'
            elif stats['medium'] > 0:
                risk_level = 'medium'
            elif stats['low'] > 0:
                risk_level = 'low'
        
        level_config = {
            'safe':  {'label': '安全',   'color': '#22c55e', 'bg': '#f0fdf4', 'icon': '&#10003;'},
            'low':    {'label': '低风险', 'color': '#84cc16', 'bg': '#f7fee7', 'icon': '!'},
            'medium': {'label': '中风险', 'color': '#eab308', 'bg': '#fefce8', 'icon': '!'},
            'high':   {'label': '高风险', 'color': '#ef4444', 'bg': '#fef2f2', 'icon': '&#9888;'},
        }
        cfg = level_config.get(risk_level, level_config['safe'])
        
        # 构建 HTML
        html_parts = []
        h = html_parts.append  # 简写
        
        h('<!DOCTYPE html>')
        h('<html lang="zh-CN">')
        h('<head>')
        h('  <meta charset="UTF-8">')
        h('  <meta name="viewport" content="width=device-width, initial-scale=1.0">')
        h(f'  <title>敏感内容扫描报告 - {self._get_current_time()}</title>')
        h('  <style>')
        h('''* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      background: #f1f5f9; color: #1e293b; line-height: 1.6; padding: 20px; }
.container { max-width: 900px; margin: 0 auto; }

/* 头部 */
.header { background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%);
           color: white; border-radius: 12px; padding: 32px; margin-bottom: 24px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
.header h1 { font-size: 24px; font-weight: 700; margin-bottom: 8px; }
.header .meta { font-size: 13px; opacity: 0.85; }
.header .meta span { margin-right: 20px; }

/* 摘要卡片 */
.summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 16px; margin-bottom: 24px; }
.summary-card { background: white; border-radius: 10px; padding: 20px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.08); transition: transform 0.2s; }
.summary-card:hover { transform: translateY(-2px); }
.summary-card .number { font-size: 36px; font-weight: 800; line-height: 1.2; }
.summary-card .label { font-size: 13px; color: #64748b; margin-top: 4px; }
.card-high .number { color: #ef4444; }
.card-medium .number { color: #eab308; }
.card-low .number { color: #84cc16; }
.card-safe .number { color: #22c55e; }

/* 风险指示条 */
.risk-bar { background: white; border-radius: 10px; padding: 20px; margin-bottom: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
.risk-bar-inner { display: flex; align-items: center; gap: 16px; }
.risk-icon { width: 56px; height: 56px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
             font-size: 28px; font-weight: bold; flex-shrink: 0; }
.risk-text h2 { font-size: 18px; margin-bottom: 4px; }
.risk-text p { font-size: 14px; color: #64748b; }

/* 详情区域 */
.section { background: white; border-radius: 10px; padding: 24px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
.section-title { font-size: 17px; font-weight: 700; margin-bottom: 16px; padding-bottom: 12px;
               border-bottom: 2px solid #f1f5f9; color: #334155; }

/* 文件卡片 */
.file-card { border: 1px solid #e2e8f0; border-radius: 8px; margin-bottom: 16px; overflow: hidden; }
.file-header { background: #f8fafc; padding: 12px 16px; font-weight: 600; font-size: 14px;
              display: flex; align-items: center; gap: 8px; border-bottom: 1px solid #e2e8f0; }
.file-body { padding: 16px; }

/* 问题标签 */
.issue-group { margin-bottom: 16px; }
.issue-group:last-child { margin-bottom: 0; }
.issue-label { font-size: 13px; font-weight: 700; display: inline-block; padding: 3px 10px;
               border-radius: 4px; margin-bottom: 8px; }
.label-pii       { background: #dbeafe; color: #1d4ed8; }
.label-dict      { background: #fef3c7; color: #b45309; }
.label-hashed    { background: #fce7f3; color: #be185d; }
.label-custom    { background: #ede9fe; color: #6d28d9; }
.label-filename  { background: #f1f5f9; color: #475569; font-style: italic; }

/* 问题条目 */
.issue-list { list-style: none; }
.issue-item { padding: 6px 0; font-size: 13px; display: flex; align-items: baseline; gap: 8px;
              border-bottom: 1px dashed #f1f5f9; }
.issue-item:last-child { border-bottom: none; }
.conf-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.conf-high { background: #ef4444; }
.conf-med  { background: #eab308; }
.conf-low  { background: #84cc16; }
.issue-value { font-family: "SF Mono", "Fira Code", monospace; background: #f8fafc; padding: 1px 6px;
               border-radius: 3px; font-size: 12px; }
.issue-detail { color: #64748b; font-size: 12px; }

/* 字典关键词表格 */
.dict-table { width: 100%; border-collapse: collapse; margin-top: 8px; font-size: 13px; }
.dict-table th { background: #f8fafc; padding: 8px 12px; text-align: left; font-weight: 600; color: #475569;
                 border-bottom: 2px solid #e2e8f0; }
.dict-table td { padding: 8px 12px; border-bottom: 1px solid #f1f5f9; }
.dict-table tr:hover { background: #fafbfc; }
.weight-badge { display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 600; }
.w-high { background: #fef2f2; color: #dc2626; }
.w-med  { background: #fefce8; color: #ca8a04; }
.w-low  { background: #f0fdf4; color: #16a34a; }

/* 图例 */
.legend { display: flex; flex-wrap: wrap; gap: 16px; padding: 16px; background: #f8fafc; border-radius: 8px;
          font-size: 13px; }
.legend-item { display: flex; align-items: center; gap: 6px; }

/* 页脚 */
.footer { text-align: center; padding: 20px; font-size: 12px; color: #94a3b8; }

/* 安全状态（无问题） */
.safe-state { text-align: center; padding: 60px 20px; }
.safe-state .big-icon { font-size: 72px; margin-bottom: 16px; }
.safe-state h2 { font-size: 22px; color: #22c55e; margin-bottom: 8px; }
.safe-state p { color: #64748b; }

/* 响应式 */
@media (max-width: 640px) {
  body { padding: 12px; }
  .header { padding: 20px; }
  .summary-grid { grid-template-columns: repeat(2, 1fr); }
}
''')
        h('  </style>')
        h('</head>')
        h('<body>')
        h('<div class="container">')

        # ====== 头部 ======
        h(f'<div class="header">')
        h(f'  <h1>&#128274; 敏感内容扫描报告</h1>')
        h(f'  <div class="meta">')
        h(f'    <span>&#128340; 扫描时间：{self._get_current_time()}</span>')
        h(f'    <span>&#128196; 发现问题文件：{len(results)} 个</span>')
        h(f'    <span>&#128220; 版本 v3.1.2</span>')
        h(f'  </div>')
        h(f'</div>')

        if not results:
            # 安全状态
            h('<div class="section safe-state">')
            h('  <div class="big-icon">&#9989;</div>')
            h('  <h2>未发现敏感内容</h2>')
            h('  <p>您的文档通过了安全检查，可以放心使用</p>')
            h('</div>')
        else:
            # ====== 摘要统计 ======
            h('<div class="summary-grid">')
            summary_items = [
                ('high',   stats['high'],   '高危/高置信'),
                ('medium', stats['medium'], '中危/中置信'),
                ('low',    stats['low'],    '低危/低置信'),
                ('safe',   stats['safe'],   '安全'),
            ]
            for skey, sval, slabel in summary_items:
                h(f'<div class="summary-card card-{skey}">')
                h(f'  <div class="number">{sval}</div>')
                h(f'  <div class="label">{slabel}</div>')
                h(f'</div>')
            
            # 数据字典风险统计
            if stats and (stats.get('dict_high', 0) or stats.get('dict_medium', 0) or stats.get('dict_low', 0)):
                h(f'<div class="summary-card card-dict">')
                dict_total = stats.get('dict_high', 0) + stats.get('dict_medium', 0) + stats.get('dict_low', 0)
                h(f'  <div class="number" style="color:#eab308;">{dict_total}</div>')
                h(f'  <div class="label">字典风险项</div>')
                h(f'</div>')
            
            h('</div>')  # end summary-grid

            # ====== 风险指示条 ======
            h(f'<div class="risk-bar">')
            h(f'  <div class="risk-bar-inner">')
            h(f'    <div class="risk-icon" style="background:{cfg["bg"]};color:{cfg["color"]};">{cfg["icon"]}</div>')
            h(f'    <div class="risk-text">')
            h(f'      <h2 style="color:{cfg["color"]}">综合评定：{cfg["label"]}</h2>')
            if risk_level == 'high':
                h(f'      <p>发现严重敏感内容，建议立即进行合规处置</p>')
            elif risk_level == 'medium':
                h(f'      <p>发现少量敏感内容，建议人工复核后处理</p>')
            elif risk_level == 'low':
                h(f'      <p>发现轻微问题，可选处理或忽略</p>')
            else:
                h(f'      <p>文档安全，可正常使用</p>')
            h(f'    </div>')
            h(f'  </div>')
            h(f'</div>')

            # ====== 文件详情 ======
            h(f'<div class="section">')
            h(f'  <div class="section-title">&#128196; 扫描结果详情</div>')
            
            for idx, result in enumerate(results, 1):
                file_path = result['file_path']
                file_name = result['file_name']
                
                h(f'<div class="file-card">')
                h(f'  <div class="file-header">')
                h(f'    <span>{idx}. &#128206; {self._html_escape(file_path)}</span>')
                h(f'  </div>')
                h(f'  <div class="file-body">')
                
                for issue in result['issues']:
                    location_label = "文件名" if issue['location'] == 'filename' else "文件内容"
                    h(f'  <div class="issue-group">')
                    h(f'    <span class="issue-label label-filename">&#128194; {location_label}</span>')
                    
                    for problem_type, items in issue['problems'].items():
                        if problem_type == 'dictionary':
                            self._html_dict_section(html_parts, items)
                        elif problem_type == 'pii':
                            self._html_pii_section(html_parts, items)
                        else:
                            self._html_word_section(html_parts, problem_type, items)
                    
                    h(f'  </div>')
                
                h(f'  </div>')  # file-body
                h(f'</div>')    # file-card
            
            h(f'</div>')  # section

            # ====== 图例说明 ======
            h(f'<div class="section">')
            h(f'  <div class="section-title">&#128214; 说明</div>')
            h(f'  <div class="legend">')
            h(f'    <div class="legend-item"><span class="conf-dot conf-high"></span> 高置信度 — 已通过格式和校验码验证</div>')
            h(f'    <div class="legend-item"><span class="conf-dot conf-med"></span> 中置信度 — 格式匹配但未完全验证</div>')
            h(f'    <div class="legend-item"><span class="conf-dot conf-low"></span> 低置信度 — 仅符合基本模式，可能误报</div>')
            h(f'  </div>')
            h(f'  <div class="legend" style="margin-top:12px;">')
            h(f'    <div class="legend-item"><span class="weight-badge w-high">&ge;10分</span> 极高敏感</div>')
            h(f'    <div class="legend-item"><span class="weight-badge w-med">5-9分</span> 高敏感</div>')
            h(f'    <div class="legend-item"><span class="weight-badge w-low">&lt;5分</span> 一般</div>')
            h(f'  </div>')
            h(f'</div>')

        # ====== 页脚 ======
        h(f'<div class="footer">')
        h(f'  敏感内容扫描器 v3.1.2 | 报告生成时间 {self._get_current_time()} | 本地运行，数据未上传')
        h(f'</div>')

        # ====== 商业合作 ======
        h(f'<div class="section" style="background:#fef3c7;border:1px solid #fcd34d;">')
        h(f'  <div class="section-title" style="color:#92400e;">&#128176; 获取更准确的内容识别规则库</div>')
        h(f'  <p style="margin:0;font-size:14px;color:#78350f;">')
        h(f'    如需更全面的行业数据字典和定制化识别规则，请联系：<br>')
        h(f'    &#128231; <a href="mailto:support@soura.com.cn" style="color:#b45309;font-weight:600;">support@soura.com.cn</a>')
        h(f'  </p>')
        h(f'</div>')
        
        h('</div>')  # container
        h('</body>')
        h('</html>')
        
        return '\n'.join(html_parts)

    def _html_escape(self, text: str) -> str:
        """HTML 转义"""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;'))

    def _html_dict_section(self, h: List, items: Dict):
        """HTML 报告：数据字典部分"""
        matches = items.get('matches', [])
        risk_score = items.get('risk_score', {})
        level = risk_score.get('level', 'safe')
        score = risk_score.get('score', 0)
        max_w = risk_score.get('max_weight', 0)
        count = risk_score.get('count', 0)
        
        level_style = {'high': 'w-high', 'medium': 'w-med', 'low': 'w-low', 'safe': 'w-low'}
        
        h.append(f'    <span class="issue-label label-dict">&#128218; 数据字典风险 ({level} / 总分{score})</span>')
        if matches:
            sorted_matches = sorted(matches, key=lambda x: x['weight'], reverse=True)
            h.append(f'    <table class="dict-table">')
            h.append(f'      <tr><th>关键词</th><th>权重</th><th>类别</th></tr>')
            for m in sorted_matches[:15]:
                ws = level_style.get('high' if m['weight'] >= 10 else ('medium' if m['weight'] >= 5 else 'low'), 'w-low')
                h.append(f'      <tr><td>{self._html_escape(m["keyword"])}</td>'
                         f'<td><span class="weight-badge {ws}">{m["weight"]}分</span></td>'
                         f'<td>{self._html_escape(m["category"])}</td></tr>')
            if len(sorted_matches) > 15:
                h.append(f'      <tr><td colspan="3" style="text-align:center;color:#94a3b8;">... 还有 {len(sorted_matches)-15} 个关键词</td></tr>')
            h.append(f'    </table>')

    def _html_pii_section(self, h: List, items: Dict):
        """HTML 报告：PII 部分"""
        pii_names = {
            'china_id_card': '身份证号', 'china_phone': '手机号',
            'china_bank_card': '银行卡号', 'email': '邮箱',
            'ip_address': 'IP地址', 'china_passport': '护照号',
            'chinese_name': '中文姓名',
        }
        
        h.append(f'    <span class="issue-label label-pii">&#128272; PII 个人信息</span>')
        h.append(f'    <ul class="issue-list">')
        
        for pii_type, matches in items.items():
            name = pii_names.get(pii_type, pii_type)
            matches_sorted = sorted(matches,
                key=lambda x: {'high': 0, 'medium': 1, 'low': 2}.get(x.get('confidence', 'low'), 3))
            for m in matches_sorted:
                conf = m.get('confidence', 'low')
                cls = {'high': 'conf-high', 'medium': 'conf-med', 'low': 'conf-low'}.get(conf, 'conf-low')
                h.append(f'      <li class="issue-item">'
                         f'<span class="conf-dot {cls}"></span>'
                         f'<strong>{name}</strong> '
                         f'<span class="issue-value">{self._html_escape(m["value"])}</span>'
                         f'<span class="issue-detail">(置信度: {conf})</span>'
                         f'</li>')
        
        h.append(f'    </ul>')

    def _html_word_section(self, h: List, problem_type: str, items: List):
        """HTML 报告：敏感词部分"""
        names = {'hashed_sensitive_words': '违禁词', 'custom_sensitive_words': '自定义敏感词'}
        label_cls = {'hashed_sensitive_words': 'label-hashed', 'custom_sensitive_words': 'label-custom'}
        name = names.get(problem_type, problem_type)
        cls = label_cls.get(problem_type, '')
        
        h.append(f'    <span class="issue-label {cls}">&#9873; {name}（{len(items)}个）</span>')
        h.append(f'    <ul class="issue-list">')
        for item in items:
            h.append(f'      <li class="issue-item">'
                     f'<span class="conf-dot conf-med"></span>'
                     f'<span class="issue-value">{self._html_escape(str(item))}</span>'
                     f'</li>')
        h.append(f'    </ul>')
    
    def _add_dictionary_report(self, report: List, items: Dict):
        """添加数据字典报告"""
        matches = items.get('matches', [])
        risk_score = items.get('risk_score', {})
        
        level = risk_score.get('level', 'safe')
        score = risk_score.get('score', 0)
        max_weight = risk_score.get('max_weight', 0)
        count = risk_score.get('count', 0)
        
        level_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢', 'safe': '✅'}.get(level, '⚪')
        level_text = {'high': '高风险', 'medium': '中风险', 'low': '低风险', 'safe': '安全'}.get(level, '未知')
        
        report.append(f"\n**数据字典风险**:\n")
        report.append(f"- {level_emoji} 风险等级: {level_text}\n")
        report.append(f"- 总风险分: {score}\n")
        report.append(f"- 最高权重: {max_weight}\n")
        report.append(f"- 匹配关键词: {count} 个\n")
        
        if matches:
            report.append(f"\n**匹配关键词详情**:\n")
            # 按权重排序
            sorted_matches = sorted(matches, key=lambda x: x['weight'], reverse=True)
            for match in sorted_matches[:10]:  # 最多显示10个
                weight_emoji = '🔴' if match['weight'] >= 10 else ('🟡' if match['weight'] >= 5 else '🟢')
                report.append(f"  - {weight_emoji} [{match['weight']}分] {match['keyword']} ({match['category']})\n")
            if len(sorted_matches) > 10:
                report.append(f"  - ... 还有 {len(sorted_matches) - 10} 个关键词\n")
    
    def _add_pii_report(self, report: List, items: Dict):
        """添加 PII 报告"""
        for pii_type, matches in items.items():
            pii_name = {
                'china_id_card': '身份证号',
                'china_phone': '手机号',
                'china_bank_card': '银行卡号',
                'email': '邮箱',
                'ip_address': 'IP地址',
                'china_passport': '护照号',
                'chinese_name': '中文姓名'
            }.get(pii_type, pii_type)
            
            matches_sorted = sorted(matches, key=lambda x: {'high': 0, 'medium': 1, 'low': 2}.get(x['confidence'], 3))
            
            for match in matches_sorted:
                confidence_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(match['confidence'], '⚪')
                confidence_text = {'high': '高', 'medium': '中', 'low': '低'}.get(match['confidence'], '未知')
                report.append(f"  - {confidence_emoji} {pii_name} ({confidence_text}): {match['value']}\n")
    
    def _add_word_report(self, report: List, problem_type: str, items: List):
        """添加敏感词报告"""
        problem_name = {
            'hashed_sensitive_words': '违禁词',
            'custom_sensitive_words': '自定义敏感词'
        }.get(problem_type, problem_type)
        
        report.append(f"\n**{problem_name}**:\n")
        for item in items:
            report.append(f"  - {item}\n")
    
    def _get_statistics(self, results: List[Dict]) -> Dict[str, int]:
        """统计各风险等级的问题数量"""
        stats = {
            'high': 0, 'medium': 0, 'low': 0, 'safe': 0,
            'dict_high': 0, 'dict_medium': 0, 'dict_low': 0
        }
        
        for result in results:
            has_dict_risk = False
            has_pii_high = False
            has_pii_medium = False
            has_pii_low = False
            
            for issue in result['issues']:
                problems = issue['problems']
                
                # 数据字典风险
                if 'dictionary' in problems:
                    risk_score = problems['dictionary'].get('risk_score', {})
                    level = risk_score.get('level', 'safe')
                    if level == 'high':
                        stats['dict_high'] += 1
                        has_dict_risk = True
                    elif level == 'medium':
                        stats['dict_medium'] += 1
                        has_dict_risk = True
                    elif level == 'low':
                        stats['dict_low'] += 1
                
                # PII 统计
                if 'pii' in problems:
                    for pii_type, matches in problems['pii'].items():
                        for match in matches:
                            confidence = match.get('confidence', 'low')
                            if confidence == 'high':
                                has_pii_high = True
                            elif confidence == 'medium':
                                has_pii_medium = True
                            else:
                                has_pii_low = True
            
            # 综合风险等级
            if has_dict_risk or has_pii_high:
                stats['high'] += 1
            elif has_pii_medium:
                stats['medium'] += 1
            elif has_pii_low:
                stats['low'] += 1
            else:
                stats['safe'] += 1
        
        return stats
    
    def _get_current_time(self) -> str:
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def main():
    parser = argparse.ArgumentParser(description='敏感内容扫描器 v3.1.2')
    parser.add_argument('path', type=str, help='要扫描的文件或目录路径')
    parser.add_argument('-c', '--custom', type=str, help='自定义敏感词库文件路径')
    parser.add_argument('-o', '--output', type=str, default='report.html', help='输出报告文件路径')
    parser.add_argument('-f', '--format', type=str, choices=['json', 'markdown', 'html'], default='html',
                       help='输出格式 (默认: html)')
    parser.add_argument('-r', '--recursive', action='store_true', help='递归扫描子目录')
    parser.add_argument('-v', '--verbose', action='store_true', help='详细输出')
    parser.add_argument('--enable-chinese-name', action='store_true', help='启用中文姓名检测（默认禁用）')
    
    # 数据字典参数
    parser.add_argument('-k', '--keyword', type=str, action='append', help='添加单个关键词（可多次使用）')
    parser.add_argument('--keywords', type=str, help='添加多个关键词（逗号分隔）')
    parser.add_argument('--dict-csv', type=str, help='CSV 数据字典文件路径')
    parser.add_argument('--dict-json', type=str, help='JSON 数据字典文件路径')
    parser.add_argument('--dict-enc', type=str, help='加密行业字典文件路径 (.enc)')
    parser.add_argument('--threshold', type=float, default=10.0, help='风险阈值（默认: 10.0）')
    
    args = parser.parse_args()
    
    # 处理关键词
    keywords = []
    if args.keyword:
        keywords.extend(args.keyword)
    if args.keywords:
        keywords.extend([kw.strip() for kw in args.keywords.split(',') if kw.strip()])
    
    # 初始化扫描器
    scanner = SensitiveScanner(
        custom_words_file=args.custom,
        verbose=args.verbose,
        enable_chinese_name=args.enable_chinese_name,
        keywords=keywords if keywords else None,
        dict_csv=args.dict_csv,
        dict_json=args.dict_json,
        dict_enc=args.dict_enc,
        threshold=args.threshold
    )
    
    # 打印数据字典信息
    if scanner.dictionary.keywords:
        print(f"📚 已加载 {len(scanner.dictionary.keywords)} 个数据字典关键词")
        print(f"⚠️  风险阈值: {args.threshold}")
    
    # 扫描路径
    path = Path(args.path)
    
    if path.is_file():
        results = [scanner.scan_file(path)]
        results = [r for r in results if r['issues']]
    elif path.is_dir():
        results = scanner.scan_directory(path, recursive=args.recursive)
    else:
        print(f"错误: 路径不存在 {path}")
        return 1
    
    # 生成报告
    report = scanner.generate_report(results, output_format=args.format)
    
    # 输出报告
    output_path = Path(args.output)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 扫描完成，发现 {len(results)} 个文件存在问题")
    print(f"📄 报告已保存至: {output_path}")
    
    # 显示统计信息
    if results:
        stats = scanner._get_statistics(results)
        print(f"\n风险统计:")
        print(f"  🔴 高危: {stats['high']} 个")
        print(f"  🟡 中危: {stats['medium']} 个")
        print(f"  🟢 低危: {stats['low']} 个")
        
        if stats.get('dict_high', 0) > 0 or stats.get('dict_medium', 0) > 0 or stats.get('dict_low', 0) > 0:
            print(f"\n数据字典风险:")
            print(f"  🔴 高风险: {stats['dict_high']} 个")
            print(f"  🟡 中风险: {stats['dict_medium']} 个")
            print(f"  🟢 低风险: {stats['dict_low']} 个")
    
    return 0 if not results else 1


if __name__ == '__main__':
    exit(main())

#!/usr/bin/env python3
"""
飞书多维表格收纳管家核心模块（最终智能位置匹配版）
"""

import os
import sys
import json
import requests
import difflib
import re
from typing import Dict, List, Optional, Any, Tuple

class SmartLocationMatcher:
    """智能位置匹配器（最终版）"""
    
    def __init__(self, existing_options: List[str]):
        self.existing_options = existing_options
        self.threshold = 0.75  # 75%相似度阈值（提高精度）
        
    def get_matching_location(self, new_location: str) -> str:
        """
        获取匹配的位置选项（改进版）
        
        改进点：
        1. 提高阈值到75%减少误匹配
        2. 添加颜色识别避免"蓝色行李箱"匹配到"白色行李箱里"
        3. 添加数字识别避免"2号纸箱"匹配到"1号纸箱里"
        """
        if not self.existing_options:
            print(f"[智能匹配] 无现有选项，创建新选项: '{new_location}'")
            return new_location
        
        normalized_new = self._normalize_location(new_location)
        best_match = None
        best_ratio = 0.0
        
        for option in self.existing_options:
            normalized_option = self._normalize_location(option)
            ratio = self._calculate_similarity(normalized_new, normalized_option)
            
            # 检查是否应该避免匹配
            if self._should_avoid_match(normalized_new, normalized_option):
                ratio = max(0.0, ratio - 0.3)  # 降低相似度
            
            # 如果新位置完全包含在选项中
            if normalized_new in normalized_option and len(normalized_new) >= 2:
                ratio = min(1.0, ratio + 0.1)
            
            # 如果选项完全包含在新位置中
            if normalized_option in normalized_new and len(normalized_option) >= 2:
                ratio = min(1.0, ratio + 0.1)
            
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = option
        
        if best_match and best_ratio >= self.threshold:
            print(f"[智能匹配] 匹配成功: '{new_location}' -> '{best_match}' (相似度: {best_ratio:.1%})")
            return best_match
        else:
            print(f"[智能匹配] 创建新选项: '{new_location}' (最高相似度: {best_ratio:.1%})")
            return new_location
    
    def _should_avoid_match(self, text1: str, text2: str) -> bool:
        """检查是否应该避免匹配"""
        # 检查颜色差异
        colors1 = self._extract_colors(text1)
        colors2 = self._extract_colors(text2)
        
        if colors1 and colors2 and colors1 != colors2:
            return True  # 颜色不同，避免匹配
        
        # 检查数字差异
        numbers1 = self._extract_numbers(text1)
        numbers2 = self._extract_numbers(text2)
        
        if numbers1 and numbers2 and numbers1 != numbers2:
            return True  # 数字不同，避免匹配
        
        return False
    
    def _extract_colors(self, text: str) -> List[str]:
        """提取文本中的颜色词"""
        colors = ['红', '橙', '黄', '绿', '青', '蓝', '紫', '黑', '白', '灰', '棕', '粉']
        found = []
        
        for color in colors:
            if color in text:
                found.append(color)
        
        return found
    
    def _extract_numbers(self, text: str) -> List[str]:
        """提取文本中的数字"""
        import re
        return re.findall(r'\d+', text)
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度"""
        # 使用difflib的SequenceMatcher
        return difflib.SequenceMatcher(None, text1, text2).ratio()
    
    def _normalize_location(self, location: str) -> str:
        """标准化位置描述"""
        if not location:
            return ""
        
        # 转换为小写
        location = location.lower()
        
        # 移除标点符号
        location = re.sub(r'[，。！？、；：""''()\[\]{}]', '', location)
        
        # 标准化常见词汇
        replacements = {
            '里边': '里',
            '里面': '里',
            '内部': '内',
            '中间': '中',
            '上面': '上',
            '下面': '下',
            '左边': '左',
            '右边': '右',
            '前边': '前',
            '后边': '后',
            '旁边': '旁',
            '侧面': '侧',
            '层间': '层',
            '抽屉里': '抽屉',
            '箱子里': '箱',
            '包里': '包'
        }
        
        for old, new in replacements.items():
            location = location.replace(old, new)
        
        return location.strip()

class FeishuStorageManager:
    """飞书收纳管家核心类（最终智能位置匹配版）"""
    
    def __init__(self):
        self.app_id = os.getenv("FEISHU_APP_ID", "cli_a956c03ffcb9dcbb")
        self.app_secret = os.getenv("FEISHU_APP_SECRET", "HHEZEDoNZwfNdoediXiGSbaRFKDmpB71")
        self.bitable_token = os.getenv("FEISHU_BITABLE_TOKEN", "AO6rbfj7aa8nbGsG7Rfc90honjK")
        self.table_id = os.getenv("FEISHU_TABLE_ID", "tbl0T6d9uTv4Fk3c")
        
        self.access_token = None
        self.token_expire = 0
        self.location_options_cache = None
        
    def get_tenant_access_token(self) -> str:
        """获取Tenant Access Token"""
        if self.access_token and self.token_expire > 0:
            return self.access_token
            
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            response = requests.post(url, json=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    self.access_token = result["tenant_access_token"]
                    self.token_expire = result.get("expire", 0)
                    return self.access_token
                else:
                    raise Exception(f"获取Token失败: {result.get('msg')}")
            else:
                raise Exception(f"HTTP错误: {response.status_code}")
        except Exception as e:
            raise Exception(f"获取Token异常: {e}")
    
    def get_location_field_options(self) -> List[str]:
        """获取Location字段的单选框选项"""
        if self.location_options_cache:
            return self.location_options_cache
        
        # 首先获取所有记录中的位置信息
        all_records = self._list_all_records()
        locations = set()
        
        for record in all_records:
            location = record["fields"].get("Location", "")
            if location and isinstance(location, str):
                locations.add(location.strip())
        
        # 转换为列表并排序
        options = sorted(list(locations))
        self.location_options_cache = options
        
        print(f"[位置选项] 获取到 {len(options)} 个现有位置选项")
        if options:
            print(f"[位置选项] 选项列表: {', '.join(options[:10])}{'...' if len(options) > 10 else ''}")
        
        return options
    
    def get_smart_location(self, new_location: str) -> str:
        """智能获取位置（匹配或创建）"""
        existing_options = self.get_location_field_options()
        matcher = SmartLocationMatcher(existing_options)
        return matcher.get_matching_location(new_location)
    
    def upload_image(self, image_path: str) -> str:
        """上传图片到飞书，返回file_token"""
        if not self.access_token:
            self.get_tenant_access_token()
        
        try:
            with open(image_path, "rb") as f:
                image_data = f.read()
            file_size = len(image_data)
        except Exception as e:
            raise Exception(f"读取图片失败: {e}")
        
        url = "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        form_data = {
            "file_name": os.path.basename(image_path),
            "parent_type": "bitable_image",
            "parent_node": self.bitable_token,
            "size": str(file_size)
        }
        
        files = {"file": (os.path.basename(image_path), image_data, "image/jpeg")}
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=form_data,
                files=files,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0 and "data" in result:
                    file_token = result["data"].get("file_token")
                    if file_token:
                        return file_token
                    else:
                        raise Exception("响应中没有file_token字段")
                else:
                    raise Exception(f"上传失败: {result.get('msg', '未知错误')}")
            else:
                raise Exception(f"HTTP错误 {response.status_code}: {response.text[:200]}")
                
        except Exception as e:
            raise Exception(f"上传请求异常: {e}")
    
    # ==================== 核心工具函数 ====================
    
    def add_storage_item(self, item_name: str, location: str, image_path: Optional[str] = None) -> Dict:
        """
        物品入库工具（智能位置匹配版）
        
        自动匹配现有位置选项，相似度>75%则使用现有选项，
        否则创建新选项，无需用户确认。
        """
        print(f"[智能入库] 开始处理: {item_name}")
        
        # 智能匹配位置
        smart_location = self.get_smart_location(location)
        
        fields = {
            "AI收纳管家-物品位置记录": item_name,
            "Location": smart_location  # 使用智能匹配后的位置
        }
        
        if image_path and os.path.exists(image_path):
            try:
                file_token = self.upload_image(image_path)
                fields["Image"] = [{"file_token": file_token}]
                print(f"[智能入库] 图片已关联: {file_token}")
            except Exception as e:
                print(f"[WARN] 图片上传失败，继续创建记录: {e}")
                fields["Location"] = f"{smart_location} [图片上传失败: {e}]"
        
        result = self._create_bitable_record(fields)
        
        # 清除缓存，因为可能添加了新选项
        self.location_options_cache = None
        
        return result
    
    def search_storage_item(self, query_item: str) -> List[Dict]:
        """
        物品检索工具
        """
        print(f"[SEARCH] 搜索物品: {query_item}")
        
        all_records = self._list_all_records()
        
        matched_records = []
        for record in all_records:
            item_field = record["fields"].get("AI收纳管家-物品位置记录", "")
            if query_item.lower() in item_field.lower():
                matched_records.append(record)
        
        print(f"[SEARCH] 找到 {len(matched_records)} 条匹配记录")
        return matched_records
    
    def update_storage_location(self, item_name: str, new_location: str) -> Dict:
        """
        位置更新工具（智能位置匹配版）
        """
        print(f"[智能更新] 更新位置: {item_name}")
        
        # 智能匹配新位置
        smart_location = self.get_smart_location(new_location)
        print(f"[智能更新] 新位置匹配结果: '{new_location}' -> '{smart_location}'")
        
        records = self.search_storage_item(item_name)
        
        if not records:
            raise Exception(f"未找到物品: {item_name}")
        
        target_record = records[0]
        record_id = target_record["record_id"]
        
        fields = {"Location": smart_location}
        
        if "Image" in target_record["fields"]:
            fields["Image"] = target_record["fields"]["Image"]
        
        result = self._update_bitable_record(record_id, fields)
        
        # 清除缓存
        self.location_options_cache = None
        
        return result
    
    # ==================== 底层API函数 ====================
    
    def _create_bitable_record(self, fields: Dict) -> Dict:
        """创建多维表格记录"""
        if not self.access_token:
            self.get_tenant_access_token()
        
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.bitable_token}/tables/{self.table_id}/records"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        data = {"fields": fields}
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    record = result.get("record", {})
                    print(f"[API] 记录创建成功，ID: {record.get('record_id')}")
                    print(f"[API] 物品: {fields.get('AI收纳管家-物品位置记录')}")
                    print(f"[API] 位置: {fields.get('Location')}")
                    return result
                else:
                    raise Exception(f"创建失败: {result.get('msg')}")
            else:
                raise Exception(f"HTTP错误 {response.status_code}: {response.text[:200]}")
        except Exception as e:
            raise Exception(f"创建请求异常: {e}")
    
    def _update_bitable_record(self, record_id: str, fields: Dict) -> Dict:
        """更新多维表格记录"""
        if not self.access_token:
            self.get_tenant_access_token()
        
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.bitable_token}/tables/{self.table_id}/records/{record_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        data = {"fields": fields}
        
        try:
            response = requests.put(url, headers=headers, json=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    print(f"[API] 记录更新成功，ID: {record_id}")
                    return result
                else:
                    raise Exception(f"更新失败: {result.get('msg')}")
            else:
                raise Exception(f"HTTP错误 {response.status_code}: {response.text[:200]}")
        except Exception as e:
            raise Exception(f"更新请求异常: {e}")
    
    def _list_all_records(self) -> List[Dict]:
        """获取所有记录"""
        if not self.access_token:
            self.get_tenant_access_token()
        
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.bitable_token}/tables/{self.table_id}/records"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        all_records = []
        page_token = None
        
        try:
            while True:
                params = {"page_size": 100}
                if page_token:
                    params["page_token"] = page_token
                
                response = requests.get(url, headers=headers, params=params, timeout=10)
                if response.status_code == 200:
                    result = response.json()
                    if result.get("code") == 0:
                        records = result.get("data", {}).get("items", [])
                        all_records.extend(records)
                        
                        if result.get("data", {}).get("has_more"):
                            page_token = result["data"].get("page_token")
                        else:
                            break
                    else:
                        raise Exception(f"获取记录失败: {result.get('msg')}")
                else:
                    raise Exception(f"HTTP错误 {response.status_code}: {response.text[:200]}")
        except Exception as e:
            raise Exception(f"获取记录异常: {e}")
        
        return all_records

def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="飞书收纳管家命令行工具（智能位置匹配版）")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    add_parser = subparsers.add_parser("add", help="物品入库（智能位置匹配）")
    add_parser.add_argument("item", help="物品名称")
    add_parser.add_argument("location", help="存放位置")
    add_parser.add_argument("--image", help="图片路径")
    
    search_parser = subparsers.add_parser("search", help="物品检索")
    search_parser.add_argument("item", help="要查找的物品名称")
    
    update_parser = subparsers.add_parser("update", help="位置更新（智能位置匹配）")
    update_parser.add_argument("item", help="物品名称")
    update_parser.add_argument("new_location", help="新位置")
    
    # 新增：测试智能匹配命令
    test_parser = subparsers.add_parser("test-match", help="测试位置匹配")
    test_parser.add_argument("location", help="要测试的位置")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager =
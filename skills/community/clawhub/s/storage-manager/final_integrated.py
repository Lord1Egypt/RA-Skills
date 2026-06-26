#!/usr/bin/env python3
"""
飞书收纳管家最终集成版
包含：智能位置匹配 + 位置图片管理
"""

import os
import sys
import json
import requests
import difflib
import re
from typing import Dict, List, Optional, Any, Tuple

class SmartLocationMatcher:
    """智能位置匹配器"""
    
    def __init__(self, existing_locations: List[str]):
        self.existing_locations = existing_locations
        self.threshold = 0.75  # 75%相似度阈值
        
    def match_location(self, new_location: str) -> Tuple[str, bool]:
        """
        匹配位置
        
        Returns:
            (匹配的位置, 是否为现有位置)
        """
        if not self.existing_locations:
            return new_location, False
        
        best_match = None
        best_score = 0.0
        
        normalized_new = self._normalize(new_location)
        
        for location in self.existing_locations:
            normalized_loc = self._normalize(location)
            score = difflib.SequenceMatcher(None, normalized_new, normalized_loc).ratio()
            
            # 提升完全包含的匹配分数
            if normalized_new in normalized_loc:
                score = min(1.0, score + 0.1)
            if normalized_loc in normalized_new:
                score = min(1.0, score + 0.1)
            
            if score > best_score:
                best_score = score
                best_match = location
        
        if best_match and best_score >= self.threshold:
            return best_match, True
        else:
            return new_location, False
    
    def _normalize(self, text: str) -> str:
        """标准化文本"""
        if not text:
            return ""
        
        text = text.lower()
        text = re.sub(r'[，。！？、；：""''()\[\]{}]', '', text)
        
        # 标准化常见词汇
        replacements = {
            '里边': '里', '里面': '里', '内部': '内',
            '中间': '中', '上面': '上', '下面': '下',
            '左边': '左', '右边': '右', '前边': '前',
            '后边': '后', '旁边': '旁', '侧面': '侧',
            '抽屉里': '抽屉', '箱子里': '箱', '包里': '包'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        return text.strip()

class LocationImageManager:
    """位置图片管理器"""
    
    def __init__(self):
        self.location_images = {}  # {location: file_token}
    
    def get_location_image(self, location: str) -> Optional[str]:
        """获取位置的图片token"""
        return self.location_images.get(location)
    
    def set_location_image(self, location: str, file_token: str):
        """设置位置的图片"""
        self.location_images[location] = file_token
    
    def needs_photo(self, location: str) -> bool:
        """检查位置是否需要拍照"""
        return location not in self.location_images

class FeishuStorageManager:
    """飞书收纳管家（最终集成版）"""
    
    def __init__(self):
        self.app_id = os.getenv("FEISHU_APP_ID", "cli_a956c03ffcb9dcbb")
        self.app_secret = os.getenv("FEISHU_APP_SECRET", "HHEZEDoNZwfNdoediXiGSbaRFKDmpB71")
        self.bitable_token = os.getenv("FEISHU_BITABLE_TOKEN", "AO6rbfj7aa8nbGsG7Rfc90honjK")
        self.table_id = os.getenv("FEISHU_TABLE_ID", "tbl0T6d9uTv4Fk3c")
        
        self.access_token = None
        self.existing_locations = []
        self.image_manager = LocationImageManager()
        
    def initialize(self):
        """初始化系统"""
        self.get_tenant_access_token()
        self._load_existing_locations()
        self._load_location_images()
    
    def get_tenant_access_token(self) -> str:
        """获取Tenant Access Token"""
        if self.access_token:
            return self.access_token
            
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        data = {"app_id": self.app_id, "app_secret": self.app_secret}
        
        try:
            response = requests.post(url, json=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    self.access_token = result["tenant_access_token"]
                    return self.access_token
                else:
                    raise Exception(f"获取Token失败: {result.get('msg')}")
            else:
                raise Exception(f"HTTP错误: {response.status_code}")
        except Exception as e:
            raise Exception(f"获取Token异常: {e}")
    
    def _load_existing_locations(self):
        """加载现有位置"""
        records = self._list_all_records()
        locations = set()
        
        for record in records:
            location = record["fields"].get("Location", "")
            if isinstance(location, str) and location.strip():
                locations.add(location.strip())
        
        self.existing_locations = sorted(list(locations))
        print(f"[位置系统] 加载 {len(self.existing_locations)} 个现有位置")
    
    def _load_location_images(self):
        """加载位置图片"""
        records = self._list_all_records()
        
        for record in records:
            fields = record["fields"]
            location = fields.get("Location", "")
            
            if isinstance(location, str) and location.strip():
                # 检查是否有Location_Image字段
                location_image = fields.get("Location_Image", [])
                if location_image and isinstance(location_image, list) and len(location_image) > 0:
                    file_token = location_image[0].get("file_token")
                    if file_token:
                        self.image_manager.set_location_image(location, file_token)
        
        print(f"[位置图片] 加载 {len(self.image_manager.location_images)} 个位置的图片")
    
    def add_storage_item(
        self, 
        item_name: str, 
        location: str,
        item_image_path: Optional[str] = None
    ) -> Dict:
        """
        物品入库（智能位置匹配 + 位置图片管理）
        
        流程：
        1. 智能匹配位置
        2. 检查新位置是否需要拍照
        3. 上传物品图片（可选）
        4. 创建记录
        
        注意：如果是新位置，系统会要求用户拍照
        """
        print(f"[入库开始] 物品: {item_name}, 位置: {location}")
        
        # 1. 智能匹配位置
        matcher = SmartLocationMatcher(self.existing_locations)
        matched_location, is_existing = matcher.match_location(location)
        
        if is_existing:
            print(f"[位置匹配] 匹配到现有位置: {matched_location}")
        else:
            print(f"[位置匹配] 创建新位置: {matched_location}")
        
        # 2. 检查位置图片需求
        if not is_existing and self.image_manager.needs_photo(matched_location):
            print(f"[位置图片] ⚠️ 新位置需要拍照: {matched_location}")
            return {
                "status": "needs_location_photo",
                "message": f"新位置 '{matched_location}' 需要拍照上传位置图片",
                "location": matched_location,
                "next_step": "请上传位置图片后重新提交"
            }
        
        # 3. 上传物品图片
        item_image_token = None
        if item_image_path and os.path.exists(item_image_path):
            try:
                item_image_token = self._upload_image(item_image_path, "item")
                print(f"[物品图片] 上传成功: {item_image_token}")
            except Exception as e:
                print(f"[警告] 物品图片上传失败: {e}")
        
        # 4. 准备字段
        fields = {
            "AI收纳管家-物品位置记录": item_name,
            "Location": matched_location
        }
        
        # 添加物品图片
        if item_image_token:
            fields["Image"] = [{"file_token": item_image_token}]
        
        # 5. 创建记录
        result = self._create_record(fields)
        
        # 6. 更新缓存
        if not is_existing:
            self.existing_locations.append(matched_location)
            print(f"[位置系统] 新增位置: {matched_location}")
        
        return {
            "status": "success",
            "item": item_name,
            "location": matched_location,
            "is_new_location": not is_existing,
            "has_location_image": not self.image_manager.needs_photo(matched_location),
            "record_id": result.get("record", {}).get("record_id", "unknown")
        }
    
    def add_location_photo(self, location: str, image_path: str) -> Dict:
        """
        为位置添加图片
        
        用于处理新位置需要拍照的情况
        """
        print(f"[位置拍照] 为位置添加图片: {location}")
        
        try:
            file_token = self._upload_image(image_path, "location")
            
            # 保存位置图片映射
            self.image_manager.set_location_image(location, file_token)
            
            print(f"[位置图片] 图片上传成功: {file_token}")
            
            return {
                "status": "success",
                "location": location,
                "file_token": file_token,
                "message": f"位置 '{location}' 图片已保存"
            }
        except Exception as e:
            print(f"[位置图片] 上传失败: {e}")
            return {
                "status": "error",
                "message": f"位置图片上传失败: {e}"
            }
    
    def _upload_image(self, image_path: str, image_type: str = "item") -> str:
        """上传图片"""
        if not self.access_token:
            self.get_tenant_access_token()
        
        try:
            with open(image_path, "rb") as f:
                image_data = f.read()
        except Exception as e:
            raise Exception(f"读取图片失败: {e}")
        
        url = "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        form_data = {
            "file_name": f"{image_type}_{os.path.basename(image_path)}",
            "parent_type": "bitable_image",
            "parent_node": self.bitable_token,
            "size": str(len(image_data))
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
    
    def _create_record(self, fields: Dict) -> Dict:
        """创建记录"""
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
                    print(f"[记录创建] 成功: {fields.get('AI收纳管家-物品位置记录')} -> {fields.get('Location')}")
                    return result
                else:
                    raise Exception(f"创建失败: {result.get('msg')}")
            else:
                raise Exception(f"HTTP错误 {response.status_code}: {response.text[:200]}")
        except Exception as e:
            raise Exception(f"创建请求异常: {e}")
    
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
    """主函数"""
    print("🗃️ 飞书收纳管家 - 最终集成版")
    print("=" * 60)
    print("功能：智能位置匹配 + 位置图片管理")
    print("=" * 60)
    
    manager = FeishuStorageManager()
    
    try:
        manager.initialize()
        print("✅ 系统初始化成功")
        
        # 显示现有位置
        print(f"\n📋 现有位置 ({len(manager.existing_locations)}个):")
        for i, loc in enumerate(manager.existing_locations[:10], 1):
            has_image = not manager.image_manager.needs_photo(loc)
            image_status = "📷" if has_image else "❓"
            print(f"  {i}. {image_status} {loc}")
        
        if len(manager.existing_locations) > 10:
            print(f"  ... 还有 {len(manager.existing_locations) - 10} 个位置")
        
        print("\n🎯 使用说明:")
        print("1. 系统会自动匹配相似位置 (>75%相似度)")
        print("2. 新位置需要拍照上传位置图片")
        print("3. 位置图片会被保存和复用")
        print("4. 无需用户二次确认")
        
        return manager
        
    except Exception as e:
        print(f"❌ 系统初始化失败: {e}")
        return None

if __name__ == "__main__":
    main()
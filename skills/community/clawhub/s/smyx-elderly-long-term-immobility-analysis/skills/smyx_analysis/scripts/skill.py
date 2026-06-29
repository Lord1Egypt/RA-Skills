#!/usr/bin/env python3
import datetime
import os
import sys

from .config import ApiEnum, ConstantEnum

from .api_service import ApiService

from skills.smyx_common.scripts.util import CommonUtil, JsonUtil
from skills.smyx_common.scripts.config import ApiEnum as ApiEnumBase
from skills.smyx_common.scripts.base import BaseSkill
from skills.smyx_common.scripts.api_service import ApiService as ApiServiceBase


class Skill(BaseSkill, ApiService):
    def __init__(self):
        super().__init__()

    def get_output_analysis_content_body(self, result=None):
        result_json = result

        result_json_pure_text = result_json.get("pureText")
        if result_json_pure_text:
            result_json = JsonUtil.parse(result_json_pure_text, result_json_pure_text)

        result_json_common_ai_response = result_json.get("commonAiResponse") if isinstance(result_json,
                                                                                           dict) else result_json
        if result_json_common_ai_response:
            result_json = result_json_common_ai_response

        result_json_health_ai_response = result_json.get("healthAiResponse") if isinstance(result_json,
                                                                                           dict) else result_json
        if result_json_health_ai_response:
            result_json = result_json_health_ai_response

        result_json = JsonUtil.stringify(result_json, result_json)
        return result_json

    def get_output_analysis_content_head(self, result=None):
        return f"📊 分析报告结构化结果"

    def get_output_analysis_content_foot(self, result):
        result_id = result.get('id', {})
        output_content_export_url = ApiEnum.DETAIL_EXPORT_URL + result_id
        return f"🔗 获取报告导出图片链接: {output_content_export_url}"

    def get_output_analysis_content(self, result):
        if result is not None:
            output_content = self.get_output_analysis_content_body(result) or ""
            output_content_head = self.get_output_analysis_content_head(result)
            output_content_foot = self.get_output_analysis_content_foot(result)
            #       d
            if output_content_head:
                output_content = f"""
{output_content_head}
""" + output_content
            if output_content_foot:
                output_content += f"""
{output_content_foot}
"""
        else:
            output_content = "⚠️ 暂无分析结果"
        return output_content

    def get_output_analysis(self, input_path, params={}, *args, **argss):
        response = self.get_analysis(
            input_path, params,
            *args, **argss
        )

        def _analysis_result():
            return self.analysis_result(
                data=response
            )

        output_content = response
        if type(response) == dict:
            new_response = CommonUtil.polling(_analysis_result,
                                              check_condition=lambda res: res.get('needPageRefresh') is False,
                                              interval=5,
                                              max_attempts=24)
            output_content = self.get_output_analysis_content(new_response)
        return output_content

    def get_analysis(self, input_path, params={}, *args, **argss):
        import mimetypes

        def _validate_file(file_path):
            """验证输入文件是否合法"""
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"文件不存在: {file_path}")

            if not os.access(file_path, os.R_OK):
                raise PermissionError(f"文件没有读权限: {file_path}")

            ext = os.path.splitext(file_path)[1].lower()[1:]
            if ext not in ConstantEnum.SUPPORTED_FORMATS:
                raise ValueError(f"不支持的文件格式，支持的格式: {', '.join(ConstantEnum.SUPPORTED_FORMATS)}")

            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            if file_size_mb > ConstantEnum.MAX_FILE_SIZE_MB:
                raise ValueError(
                    f"文件过大，最大支持 {ConstantEnum.MAX_FILE_SIZE_MB}MB，当前文件大小: {file_size_mb:.1f}MB")

            return True

        files = None

        if not input_path:
            raise ValueError("必须提供本地视频路径(--input)或网络视频URL(--url)")

        if (input_path.startswith("http://") or input_path.startswith("https://")):
            params.update({
                "videoUrl": input_path
            })
        else:
            _validate_file(input_path)

            # 自动检测 MIME 类型
            mime_type, _ = mimetypes.guess_type(input_path)
            if mime_type is None:
                mime_type = 'application/octet-stream'

            # 读取文件内容
            with open(input_path, 'rb') as f:
                file_content = f.read()

            files = {
                'file': (os.path.basename(input_path), file_content, mime_type)
            }

        open_id = argss.pop('open_id', None)
        # if not open_id:  ## ARK_CLAW ##
        #     return "⚠️ 错误：缺少 open_id 参数"
        response = self.analysis(
            params=params,
            files=files
        )

        return response

    def get_output_analysis_list(self, pageNum=None, pageSize=None, *args, **argss):
        """获取报告清单
        优化规则：只要API服务接口返回报告清单，直接输出API返回的结果，
        无需汇总上下文中的分析报告，以接口返回为准
        """

        def _get_analysis_export_url(request_id=None):
            if not request_id:
                return ""
            return ApiEnum.DETAIL_EXPORT_URL + request_id

        open_id = argss.pop('open_id', None)
        # if not open_id:  ## ARK_CLAW ##
        #     return "⚠️ 错误：缺少 open_id 参数"

        response = self.page(pageNum, pageSize, *args, **argss)

        if response:
            for item in response:
                if item.get("commonAiResponse") or item.get("healthAiResponse"):
                    item["reportImageUrl"] = _get_analysis_export_url(item.get("id"))

        response_text = JsonUtil.stringify(response)

        if response_text:
            return f"""📊 分析报告记录列表(结构化结果)"
{response_text}
"""
        else:
            return "⚠️ 暂无分析报告记录"


skill = Skill()

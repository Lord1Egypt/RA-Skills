import pandas as pd
import logging
import re
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

# 从全局常量文件导入所有常量
from .constants import (
    COL_SN, COL_NAME, COL_TITLE, COL_DESCRIPTION,
    COL_DRAFT_FINISHED, COL_VIDEO_FINISHED, COL_PUBLISH_DATE,
    PLATFORM_LIST, REQUIRED_COLUMNS,
    STATUS_PENDING, STATUS_SUCCESS, STATUS_FAILED
)

logger = logging.getLogger(__name__)

class ExcelHandler:
    """Excel 处理器（常量化版，易维护）"""

    def __init__(self, excel_path):
        self.excel_path = excel_path
        self.df = None
        self.header_row = 0
        self.wb = None

    def _normalize_column_name(self, col_name):
        """标准化列名：去除各种空格（包括全角空格）、转小写"""
        if isinstance(col_name, str):
            # 去除首尾空白，然后替换所有类型的空格（半角、全角、制表符等）
            normalized = col_name.strip()
            # 替换半角空格、全角空格、制表符、换行符
            normalized = normalized.replace(' ', '').replace('　', '').replace('\t', '').replace('\n', '').replace('\r', '')
            return normalized.lower()
        return str(col_name).strip().replace(' ', '').replace('　', '').lower()

    def _finished_col_names(self):
        """返回 (draft_col, video_col) 实际列名：优先 config，fallback 常量默认值。

        完成标记列名可在 config.yaml 的 excel 段自定义（如用 '视频草稿'/'视频完成'，
        或你自己的任意叫法），无需改代码。
        """
        try:
            from core.config_manager import config_manager
            cfg = config_manager.get_excel_filter_config()
        except Exception:
            cfg = {}
        draft = (cfg.get("draft_finished_column") or "").strip()
        video = (cfg.get("video_finished_column") or "").strip()
        return (draft or COL_DRAFT_FINISHED, video or COL_VIDEO_FINISHED)

    def _find_column_mapping(self, df):
        """查找列名映射（容错处理：大小写、空格）"""
        column_mapping = {}
        normalized_df_cols = {self._normalize_column_name(c): c for c in df.columns}

        draft_col, video_col = self._finished_col_names()

        # 定义需要查找的列及其别名
        # 完成标记列名来自配置（draft_col/video_col），别名仅保留通用叫法
        column_aliases = {
            COL_SN: [COL_SN, "编号", "序号"],
            COL_NAME: [COL_NAME, "名称", "成语", "诗词"],
            draft_col: [draft_col, "视频草稿", "草稿"],
            video_col: [video_col, "视频完成", "完成", "视频制作"],
            COL_PUBLISH_DATE: [COL_PUBLISH_DATE, "发布日期", "日期", "时间"]
        }

        # 添加平台列名的别名（上架版只启用 4 平台）
        platform_aliases = {
            "快手": ["快手", "kuaishou"],
            "视频号": ["视频号", "视频 号", "channels", "微信视频号"],
            "抖音": ["抖音", "douyin", "tiktok"],
            "B站": ["B站", "b站", "bilibili", "bilibili.com"]
        }
        column_aliases.update(platform_aliases)

        for target_col, aliases in column_aliases.items():
            for alias in aliases:
                normalized_alias = self._normalize_column_name(alias)
                if normalized_alias in normalized_df_cols:
                    column_mapping[target_col] = normalized_df_cols[normalized_alias]
                    break

        return column_mapping

    def read_excel(self):
        """读取 Excel，自动识别表头行（支持大小写、空格容错）"""
        try:
            draft_col, video_col = self._finished_col_names()
            for header_row in [0, 1, 2, 3, 4]:
                df = pd.read_excel(self.excel_path, header=header_row)

                column_mapping = self._find_column_mapping(df)

                core_cols = [COL_SN, COL_NAME, COL_TITLE, COL_DESCRIPTION, draft_col, video_col]
                found_core = sum(1 for col in core_cols if col in column_mapping)

                if found_core >= 3:
                    self.header_row = header_row

                    new_columns = []
                    for col in df.columns:
                        normalized_col = self._normalize_column_name(col)
                        found = False

                        # 定义所有需要处理的列
                        column_rules = [
                            (COL_SN, [COL_SN, "编号", "序号"]),
                            (COL_NAME, [COL_NAME, "名称", "成语", "诗词"]),
                            (COL_TITLE, [COL_TITLE]),
                            (COL_DESCRIPTION, [COL_DESCRIPTION]),
                            (draft_col, [draft_col, "视频草稿", "草稿"]),
                            (video_col, [video_col, "视频完成", "视频制作"]),
                            (COL_PUBLISH_DATE, [COL_PUBLISH_DATE, "发布日期"]),
                            ("快手", ["快手"]),
                            ("视频号", ["视频号"]),
                            ("抖音", ["抖音"]),
                            ("B站", ["B站", "b站"])
                        ]

                        # 查找匹配
                        for target_col, aliases in column_rules:
                            for alias in aliases:
                                if self._normalize_column_name(alias) == normalized_col:
                                    new_columns.append(target_col)
                                    found = True
                                    break
                            if found:
                                break
                        if not found:
                            # 如果没有找到映射，保留原始列名（去除首尾空格）
                            new_columns.append(col.strip())

                    # 直接设置列名
                    df.columns = new_columns

                    # 列名设置完成后，再进行数据处理
                    if COL_SN in df.columns:
                        df = df.dropna(subset=[COL_SN]).reset_index(drop=True)

                    if COL_PUBLISH_DATE in df.columns:
                        df[COL_PUBLISH_DATE] = df[COL_PUBLISH_DATE].astype(str).str.strip()

                    self.df = df

                    logger.info(f"Excel 读取成功 | 表头行：{header_row + 1} | 数据条数：{len(self.df)}")
                    return self.df

            required_str = "、".join([COL_SN, COL_NAME, COL_TITLE, COL_DESCRIPTION, draft_col, video_col])
            raise ValueError(f"未找到有效表头，请确保表格包含：{required_str}")

        except Exception as e:
            logger.error(f"Excel 读取失败：{str(e)}")
            raise

    def validate_header(self):
        """校验表头完整性"""
        if self.df is None:
            self.read_excel()

        missing = [col for col in REQUIRED_COLUMNS if col not in self.df.columns]
        if missing:
            logger.warning(f"表头缺失列：{missing}")
            return False
        return True

    def get_pending_rows(self, platforms=None, require_draft_finished=None, require_video_finished=None):
        """获取待发布数据。

        过滤规则（均可配置，兼容任意列名）：
          - draft_finished_column 列需标记 ✓（require_draft_finished，默认读配置，缺省 True）
          - video_finished_column 列需标记 ✓（require_video_finished，默认读配置，缺省 True）
          - 目标平台列未发布（□ 或空）
        当 Excel 中不存在对应列时，自动跳过该过滤条件（避免 KeyError）。
        """
        if self.df is None:
            self.read_excel()

        if platforms is None:
            platforms = PLATFORM_LIST

        # 未显式传入时从配置读取（默认都为 True，保持旧有行为）
        if require_draft_finished is None:
            require_draft_finished = self._cfg_bool("require_draft_finished", True)
        if require_video_finished is None:
            require_video_finished = self._cfg_bool("require_video_finished", True)

        draft_col, video_col = self._finished_col_names()

        # 逐条件组合；列不存在或配置关闭时自动跳过
        mask = pd.Series([True] * len(self.df))

        if require_draft_finished and draft_col in self.df.columns:
            mask &= (self.df[draft_col] == STATUS_SUCCESS)
        if require_video_finished and video_col in self.df.columns:
            mask &= (self.df[video_col] == STATUS_SUCCESS)

        platform_mask = pd.Series([False] * len(self.df))

        for p in platforms:
            if p in self.df.columns:
                # 待发布状态包括：STATUS_PENDING(□) 或空值(nan)
                pending_mask = (self.df[p] == STATUS_PENDING) | (self.df[p].isna())
                platform_mask |= pending_mask

        return self.df[mask & platform_mask]

    def _cfg_bool(self, key, default):
        """从配置读取布尔开关，读取失败回退 default"""
        try:
            from core.config_manager import config_manager
            return bool(config_manager.get_excel_filter_config().get(key, default))
        except Exception:
            return default

    def get_row_info(self, row_idx):
        """获取单行基础信息"""
        if self.df is None:
            self.read_excel()
        if not (0 <= row_idx < len(self.df)):
            raise IndexError(f"行索引越界：{row_idx}")

        row = self.df.iloc[row_idx]
        name_value = row.get(COL_NAME)
        publish_date_value = row.get(COL_PUBLISH_DATE)
        return {
            "name": str(name_value).strip() if pd.notna(name_value) else "",
            "publish_date": str(publish_date_value).strip() if pd.notna(publish_date_value) else "",
            "row_index": row_idx
        }

    def get_title_description(self, row_idx, platform=None):
        """获取【标题】【描述】列内容（支持按平台分割标题和描述）

        Args:
            row_idx: 行索引
            platform: 平台名称（如"快手"、"抖音"等），如果提供则按平台分割读取

        标题和描述列的分割格式：
            快手：这是快手专用的标题/描述
            抖音：这是抖音专用的标题/描述
            视频号：这是视频号专用的标题/描述
            视频号/其他：这是视频号的备选标题/描述
            通用：这是通用的标题/描述（没有指定平台时使用）
        """
        if self.df is None:
            self.read_excel()

        if row_idx in self.df.index:
            row = self.df.loc[row_idx]
        elif 0 <= row_idx < len(self.df):
            row = self.df.iloc[row_idx]
        else:
            raise IndexError(f"行索引越界：{row_idx}")

        # 读取标题
        if COL_TITLE in row.index and pd.notna(row[COL_TITLE]):
            raw_title = str(row[COL_TITLE]).strip()
        else:
            raw_title = ""

        title = self._split_content_by_platform(raw_title, platform) if platform else raw_title

        # 读取描述
        if COL_DESCRIPTION in row.index and pd.notna(row[COL_DESCRIPTION]):
            raw_desc = str(row[COL_DESCRIPTION]).strip()
        else:
            raw_desc = ""

        description = self._split_content_by_platform(raw_desc, platform) if platform else raw_desc

        return {"title": title, "description": description}

    def _split_content_by_platform(self, raw_content, platform):
        """按平台分割标题或描述文本

        Args:
            raw_content: 原始文本（标题或描述）
            platform: 目标平台名称

        Returns:
            分割后的文本
        """
        if not raw_content:
            return ""

        import re

        # 支持的平台列表（包含"视频号/其他"这样的组合格式）
        platforms = ["抖音", "快手", "B站", "视频号/其他", "视频号", "通用"]

        # 构建平台分隔符正则（用于匹配下一个平台或结尾）
        platform_sep = "|".join(re.escape(p) for p in platforms)

        if platform:
            # 首先尝试精确匹配指定平台
            platform_pattern = re.compile(rf"{re.escape(platform)}：\s*(.*?)(?=\n(?:{platform_sep})：|$)", re.DOTALL)
            match = platform_pattern.search(raw_content)
            if match:
                result = match.group(1).strip()
                logger.debug(f"找到平台专属内容【{platform}】：{result[:30]}...")
                return result

            # 如果是视频号，尝试匹配"视频号/其他"作为备选
            if platform == "视频号":
                alt_pattern = re.compile(rf"视频号/其他：\s*(.*?)(?=\n(?:{platform_sep})：|$)", re.DOTALL)
                alt_match = alt_pattern.search(raw_content)
                if alt_match:
                    result = alt_match.group(1).strip()
                    logger.debug(f"使用视频号备选内容【视频号/其他】：{result[:30]}...")
                    return result

            # 尝试查找"通用："描述
            common_pattern = re.compile(rf"通用：\s*(.*?)(?=\n(?:{platform_sep})：|$)", re.DOTALL)
            common_match = common_pattern.search(raw_content)
            if common_match:
                result = common_match.group(1).strip()
                logger.debug(f"使用通用内容：{result[:30]}...")
                return result

            # 如果都没有，返回原始内容（可能没有按平台分割）
            logger.debug(f"内容未按平台分割，使用原始内容")
            return raw_content

        return raw_content

    def parse_publish_date(self, row_idx):
        """解析【发布日期】字段，拆分日期和时间，时间为空默认补20:00"""
        if self.df is None:
            self.read_excel()

        if row_idx in self.df.index:
            row = self.df.loc[row_idx]
        elif 0 <= row_idx < len(self.df):
            row = self.df.iloc[row_idx]
        else:
            raise IndexError(f"行索引越界：{row_idx}")

        publish_date_str = str(row[COL_PUBLISH_DATE]).strip() if COL_PUBLISH_DATE in row and pd.notna(row[COL_PUBLISH_DATE]) else ""

        print(f'excel 中的发布日期:', publish_date_str)

        if not publish_date_str or publish_date_str.lower() in ['nan', 'none', '']:
            return {"date": "", "time": "", "datetime": ""}

        # 拆分日期和时间
        parts = publish_date_str.split()
        date_part = parts[0]
        time_part = "20:00"  # 默认时间

        if len(parts) > 1:
            time_part = parts[1]

        # 确保日期格式正确
        if len(date_part) == 8 and date_part.isdigit():
            # 格式：YYYYMMDD
            date_part = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:]}"

        # 确保时间格式正确
        if len(time_part) == 4 and time_part.isdigit():
            # 格式：HHMM
            time_part = f"{time_part[:2]}:{time_part[2:]}"

        return {
            "date": date_part,
            "time": time_part,
            "datetime": f"{date_part} {time_part}" if date_part else ""
        }

    def update_platform_status(self, row_idx, platform, success, message=""):
        """更新平台发布状态（只读模式，仅记录日志）"""
        logger.info(f"第{row_idx + 1}行 {platform} → {'成功' if success else '失败'}{f' - {message}' if message else ''}")

    def update_publish_date(self, row_idx, publish_time_str):
        """更新发布日期（只读模式，仅记录日志）"""
        logger.info(f"第{row_idx + 1}行 发布日期 → {publish_time_str}")

    def save_excel_with_style(self):
        """保存 Excel（只读模式，仅记录日志）"""
        logger.info("Excel 为只读模式，跳过保存")

    def get_statistics(self):
        """发布统计"""
        if self.df is None:
            self.read_excel()

        total = len(self.df)
        draft_col, video_col = self._finished_col_names()
        draft_ok = len(self.df[self.df[draft_col] == STATUS_SUCCESS]) if draft_col in self.df.columns else 0
        video_ok = len(self.df[self.df[video_col] == STATUS_SUCCESS]) if video_col in self.df.columns else 0

        stats = {"total": total, "draft_done": draft_ok, "video_done": video_ok}

        for p in PLATFORM_LIST:
            if p in self.df.columns:
                stats[f"{p}_published"] = len(self.df[self.df[p] == STATUS_SUCCESS])
                stats[f"{p}_pending"] = len(self.df[self.df[p] == STATUS_PENDING])
                stats[f"{p}_failed"] = len(self.df[self.df[p] == STATUS_FAILED])

        return stats


# ====================== 外部快捷调用 ======================
def read_excel(excel_path):
    return ExcelHandler(excel_path).read_excel()

def get_pending_rows(excel_path, platforms=None):
    return ExcelHandler(excel_path).get_pending_rows(platforms)
def update_platform_status(excel_path, row_idx, platform, success, message=""):
    handler = ExcelHandler(excel_path)
    handler.update_platform_status(row_idx, platform, success, message)
    handler.save_excel_with_style()

def get_statistics(excel_path):
    return ExcelHandler(excel_path).get_statistics()

def get_title_description(excel_path, row_idx, platform=None):
    """全局函数：获取标题和描述（支持按平台分割）"""
    return ExcelHandler(excel_path).get_title_description(row_idx, platform)

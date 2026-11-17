"""
reader_odm.py - CDISC ODM/XML 格式读入（临床试验数据）
自动从 stat_reader.py 拆分生成
"""

from __future__ import annotations
import os
from typing import Any

import pandas as pd
from lxml import etree

from .reader_core import (ColumnInfo, OdmMeta, StatFileResult, _bilingual, _calc_missing_pct, _get_source_type, _build_column_report)

# ============================================================
# CDISC ODM/XML 格式读入（临床试验数据）
# ============================================================

def _read_odm(filepath: str, timestamp: str) -> StatFileResult:
    """读入 CDISC ODM XML 文件（.odm），使用 xml.etree.ElementTree 解析。

    ODM (Operational Data Model) 是临床数据交换标准。
    主要结构: ODM > Study > MetaDataVersion > ItemGroupDef > ItemDef
    数据部分: ODM > Study > MetaDataVersion > ItemGroupDef > ItemData (或 ClinicalData > SubjectData > StudyEventData > FormData > ItemGroupData > ItemData)
    """
    import xml.etree.ElementTree as ET

    warnings_list = []
    warnings_list.append(_bilingual("CDISC ODM is a clinical trial data exchange format, does not contain SPSS/Stata proprietary variable/value labels or other statistical metadata, only raw data values", "CDISC ODM 为临床试验数据交换格式，不含 SPSS/Stata 专有变量标签、值标签等统计元数据，仅保留原始数据值"))
    odm_metadata: dict[str, Any] = {}

    tree = ET.parse(filepath)
    root = tree.getroot()

    # Collect ODM metadata
    odm_metadata["root_tag"] = root.tag
    odm_metadata["root_attributes"] = dict(root.attrib) if root.attrib else {}

    # Get namespaces
    ns_match = root.tag.split("}")[0].strip("{") if "}" in root.tag else None
    ns = {"odm": ns_match} if ns_match else {}

    # File attributes (ODM level)
    for attr in ["FileOID", "Description", "CreationDateTime", "PriorFileOID", "AsOfDateTime"]:
        val = root.attrib.get(attr)
        if val:
            odm_metadata[f"odm_{attr.lower()}"] = val

    # Study info
    study_elem = root.find(".//odm:Study", ns) if ns else root.find(".//Study")
    if study_elem is not None:
        odm_metadata["study_oid"] = study_elem.attrib.get("OID")
        global_vars = study_elem.find("odm:GlobalVariables", ns) if ns else study_elem.find("GlobalVariables")
        if global_vars is not None:
            study_name = global_vars.find("odm:StudyName", ns) if ns else global_vars.find("StudyName")
            if study_name is not None and study_name.text:
                odm_metadata["study_name"] = study_name.text

    # MetaDataVersion info
    md_version = root.find(".//odm:MetaDataVersion", ns) if ns else root.find(".//MetaDataVersion")
    if md_version is not None:
        odm_metadata["metadata_version_oid"] = md_version.attrib.get("OID")
        odm_metadata["metadata_version_name"] = md_version.attrib.get("Name")

        # ItemGroupDef info
        item_groups = md_version.findall("odm:ItemGroupDef", ns) if ns else md_version.findall("ItemGroupDef")
        ig_list = []
        for ig in item_groups:
            ig_info = {
                "oid": ig.attrib.get("OID"),
                "name": ig.attrib.get("Name"),
                "repeating": ig.attrib.get("Repeating", "No"),
                "is_reference_data": ig.attrib.get("IsReferenceData", "No"),
                "items": []
            }
            items = ig.findall("odm:ItemDef", ns) if ns else ig.findall("ItemDef")
            for item in items:
                ig_info["items"].append({
                    "oid": item.attrib.get("OID"),
                    "name": item.attrib.get("Name"),
                    "datatype": item.attrib.get("DataType"),
                    "length": item.attrib.get("Length"),
                })
            ig_list.append(ig_info)
        odm_metadata["item_groups"] = ig_list
        odm_metadata["total_item_groups"] = len(ig_list)

    # Try to find ClinicalData and extract as DataFrame
    df = pd.DataFrame()
    clinical_data = root.find(".//odm:ClinicalData", ns) if ns else root.find(".//ClinicalData")

    if clinical_data is not None:
        records = []
        subject_path = "odm:SubjectData" if ns else "SubjectData"
        se_path = "odm:StudyEventData" if ns else "StudyEventData"
        form_path = "odm:FormData" if ns else "FormData"
        igd_path = "odm:ItemGroupData" if ns else "ItemGroupData"
        item_path = "odm:ItemData" if ns else "ItemData"

        for subject in clinical_data.findall(subject_path):
            subject_oid = subject.attrib.get("SubjectKey", "")
            for se in subject.findall(se_path):
                se_oid = se.attrib.get("StudyEventOID", "")
                se_repeat = se.attrib.get("StudyEventRepeatKey", "")
                for form in se.findall(form_path):
                    form_oid = form.attrib.get("FormOID", "")
                    form_repeat = form.attrib.get("FormRepeatKey", "")
                    for ig_data in form.findall(igd_path):
                        ig_oid = ig_data.attrib.get("ItemGroupOID", "")
                        record = {
                            "Subject": subject_oid,
                            "StudyEventOID": se_oid,
                            "StudyEventRepeatKey": se_repeat,
                            "FormOID": form_oid,
                            "FormRepeatKey": form_repeat,
                            "ItemGroupOID": ig_oid,
                        }
                        for item_data in ig_data.findall(item_path):
                            item_oid = item_data.attrib.get("ItemOID", "")
                            value_elem = item_data.find("odm:Value", ns) if ns else item_data.find("Value")
                            item_value = value_elem.text if value_elem is not None else item_data.attrib.get("Value", "")
                            record[item_oid] = item_value
                        records.append(record)

        if records:
            df = pd.DataFrame(records)
            odm_metadata["clinical_data_rows"] = len(df)
            odm_metadata["clinical_data_columns"] = len(df.columns)
        else:
            warnings_list.append(_bilingual("No parseable SubjectData records found in ClinicalData section", "ClinicalData 部分均未找到可解析的 SubjectData 记录"))

    # If no ClinicalData rows found, try extracting just metadata-def structured info
    if df.empty and md_version is not None:
        # Fallback: extract all ItemDef metadata
        all_items = []
        item_groups_fb = md_version.findall("odm:ItemGroupDef", ns) if ns else md_version.findall("ItemGroupDef")
        for ig in item_groups_fb:
            items = ig.findall("odm:ItemDef", ns) if ns else ig.findall("ItemDef")
            for item in items:
                all_items.append({
                    "ItemGroupOID": ig.attrib.get("OID"),
                    "ItemGroupDefName": ig.attrib.get("Name"),
                    "ItemOID": item.attrib.get("OID"),
                    "ItemName": item.attrib.get("Name"),
                    "DataType": item.attrib.get("DataType", ""),
                    "Length": item.attrib.get("Length", ""),
                    "SASFieldName": item.attrib.get("SASFieldName", ""),
                    "Comment": item.attrib.get("Comment", ""),
                })
        if all_items:
            df = pd.DataFrame(all_items)
            warnings_list.append(_bilingual(
                "ODM file has no ClinicalData for standard DataFrame conversion, extracted ItemDef metadata from MetaDataVersion as fallback",
                "ODM 文件中无 ClinicalData 可转换为标准 DataFrame，已提取 MetaDataVersion 中的 ItemDef 元数据作为替代"
            ))

    if df.empty:
        raise ValueError(_bilingual("ODM file has no parseable data (no ClinicalData and no MetaDataVersion ItemDef)", "ODM 文件无法解析出任何数据（无 ClinicalData 且无 MetaDataVersion ItemDef）"))

    column_report: dict[str, ColumnInfo] = {}
    for col in df.columns:
        column_report[col] = ColumnInfo(
            source_type=_get_source_type(df[col]),
            pandas_dtype=str(df[col].dtype),
            original_label=None,
            has_value_labels=False,
            n_missing=int(df[col].isnull().sum()),
            missing_are_special=False,
            precision_warning=False,
            format_string=None,
            display_width=None,
            storage_width=None,
            measure_level=None,
            alignment=None,
            original_type=None,
        )
        if pd.api.types.is_numeric_dtype(df[col]) or pd.api.types.is_float_dtype(df[col]):
            max_val = df[col].abs().max()
            if pd.notna(max_val) and max_val > 1e15:
                column_report[col]["precision_warning"] = True
                warnings_list.append(f"列 '{col}' 包含 >1e15 的数值，float64 精度可能不足 | Column '{col}' contains values >1e15, float64 precision may be insufficient")

    return {
        "dataframe": df,
        "metadata": OdmMeta(
            file_format="odm", collected_at=timestamp,
            row_count=df.shape[0], column_count=df.shape[1],
            total_missing_pct=_calc_missing_pct(df),
            variable_labels={}, value_labels={}, special_missing={},
            date_origin=None, file_encoding=None, file_label=None,
            creation_time=None, modification_time=None, notes=[],
            original_variable_types={}, readstat_variable_types={},
            variable_value_labels={}, variable_to_label={},
            missing_user_values={}, missing_ranges={},
            variable_display_width={}, variable_storage_width={},
            variable_measure={}, variable_alignment={},
            column_names_to_labels={}, mr_sets={}, table_name=None,
            odm_metadata=odm_metadata,
        ),
        "warnings": warnings_list,
        "column_report": column_report,
    }



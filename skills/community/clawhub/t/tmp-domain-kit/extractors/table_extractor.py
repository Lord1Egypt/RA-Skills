"""
表格提取器 - 从 CSV / Excel 提取知识实体
CSV 用 csv 标准库，Excel 尝试纯 Python 解析（不可用则降级）
"""

import csv
import re
import os
from typing import Dict, Any, List
from extractors.base import BaseExtractor


class TableExtractor(BaseExtractor):
    """从 CSV / Excel 表格提取知识"""

    # I/O 模块类型关键词
    IO_TYPES = {'DI', 'DO', 'AI', 'AO', 'RTD', 'TC'}

    def extract(self, file_path: str) -> List[Dict[str, Any]]:
        """从表格文件提取实体"""
        if not self._file_exists(file_path):
            return []

        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.csv':
            return self._extract_csv(file_path)
        elif ext in ('.xlsx', '.xls'):
            return self._extract_excel(file_path)
        else:
            # 尝试当 CSV 处理
            return self._extract_csv(file_path)

    def _extract_csv(self, file_path: str) -> List[Dict[str, Any]]:
        """从 CSV 提取"""
        results = []
        provenance = self._make_provenance(file_path, confidence=0.9, source_type="table_csv")

        # 尝试不同编码
        text = None
        for encoding in ['utf-8-sig', 'utf-8', 'gbk', 'gb2312']:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    text = f.read()
                break
            except (UnicodeDecodeError, UnicodeError):
                continue

        if text is None:
            return []

        # 解析 CSV
        reader = csv.DictReader(text.splitlines())
        if not reader.fieldnames:
            return []

        headers = [h.strip().lower() for h in reader.fieldnames]
        rows = list(reader)

        # 判断表格类型
        if self._is_io_table(headers):
            results.extend(self._extract_io_modules(rows, headers, provenance))
        elif self._is_device_table(headers):
            results.extend(self._extract_devices(rows, headers, provenance))
        elif self._is_param_table(headers):
            results.extend(self._extract_params(rows, headers, provenance))
        else:
            # 通用表格 → BestPractice
            results.extend(self._extract_generic(rows, headers, provenance))

        return results

    def _extract_excel(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Excel 提取 - 纯 Python 尝试解析 xlsx（ZIP+XML），
        失败则降级为提示用户转 CSV
        """
        provenance = self._make_provenance(file_path, confidence=0.7, source_type="table_excel")

        try:
            # 尝试用 zipfile 解析 xlsx（xlsx 本质是 ZIP）
            import zipfile
            import xml.etree.ElementTree as ET

            if not zipfile.is_zipfile(file_path):
                return []

            with zipfile.ZipFile(file_path, 'r') as z:
                # 读取共享字符串表
                strings = []
                if 'xl/sharedStrings.xml' in z.namelist():
                    ss_xml = z.read('xl/sharedStrings.xml')
                    ss_root = ET.fromstring(ss_xml)
                    ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                    for si in ss_root.findall('.//s:si', ns):
                        t = si.find('.//s:t', ns)
                        strings.append(t.text if t is not None and t.text else '')

                # 读取第一个 sheet
                sheet_name = 'xl/worksheets/sheet1.xml'
                if sheet_name not in z.namelist():
                    # 尝试 sheet1
                    sheets = [n for n in z.namelist() if 'worksheets/sheet' in n]
                    if not sheets:
                        return []
                    sheet_name = sheets[0]

                sheet_xml = z.read(sheet_name)
                sheet_root = ET.fromstring(sheet_xml)
                ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

                rows_data = []
                for row_el in sheet_root.findall('.//s:row', ns):
                    row = {}
                    for cell in row_el.findall('s:c', ns):
                        ref = cell.get('r', '')
                        col = re.match(r'([A-Z]+)', ref)
                        if not col:
                            continue
                        col_letter = col.group(1)
                        cell_type = cell.get('t', '')
                        value_el = cell.find('s:v', ns)
                        if value_el is not None and value_el.text:
                            if cell_type == 's':
                                idx = int(value_el.text)
                                row[col_letter] = strings[idx] if idx < len(strings) else ''
                            else:
                                row[col_letter] = value_el.text
                        else:
                            row[col_letter] = ''
                    if row:
                        rows_data.append(row)

                if len(rows_data) < 2:
                    return []

                # 第一行作为 header
                cols = sorted(rows_data[0].keys())
                headers = [rows_data[0].get(c, '').strip().lower() for c in cols]
                rows = []
                for rd in rows_data[1:]:
                    row_dict = {}
                    for i, c in enumerate(cols):
                        if i < len(headers):
                            row_dict[headers[i]] = rd.get(c, '')
                    rows.append(row_dict)

                results = []
                if self._is_io_table(headers):
                    results.extend(self._extract_io_modules(rows, headers, provenance))
                elif self._is_device_table(headers):
                    results.extend(self._extract_devices(rows, headers, provenance))
                else:
                    results.extend(self._extract_generic(rows, headers, provenance))
                return results

        except Exception:
            # 降级：无法解析 Excel
            return [{
                "entity_type": "BestPractice",
                "entity": {
                    "title": f"Excel 文件待处理: {os.path.basename(file_path)}",
                    "content": "该 Excel 文件需要转换为 CSV 后重新导入",
                    "tags": ["excel", "待处理"],
                    "examples": []
                },
                "provenance": provenance,
                "tags": ["excel", "待处理"]
            }]

    def _is_io_table(self, headers: List[str]) -> bool:
        """判断是否为 I/O 模块配置表"""
        header_text = ' '.join(headers)
        return any(kw in header_text for kw in ['模块', 'module', '通道', 'channel', 'di', 'do', 'ai', 'ao'])

    def _is_device_table(self, headers: List[str]) -> bool:
        """判断是否为设备参数表"""
        header_text = ' '.join(headers)
        return any(kw in header_text for kw in ['型号', 'model', '设备', 'device', '名称', 'name'])

    def _is_param_table(self, headers: List[str]) -> bool:
        """判断是否为参数表"""
        header_text = ' '.join(headers)
        return any(kw in header_text for kw in ['参数', 'param', '值', 'value', '设定', 'setting'])

    def _extract_io_modules(self, rows: List[Dict], headers: List[str],
                             provenance: Dict) -> List[Dict[str, Any]]:
        """提取 I/O 模块实体"""
        results = []
        model_key = self._find_key(headers, ['型号', 'model', '模块型号'])
        type_key = self._find_key(headers, ['类型', 'type', '模块类型'])
        channel_key = self._find_key(headers, ['通道数', 'channels', '通道', 'channel_count'])
        signal_key = self._find_key(headers, ['信号类型', 'signal', 'signal_type'])

        for row in rows:
            model = row.get(model_key, '').strip() if model_key else ''
            if not model:
                continue
            io_type = row.get(type_key, 'DI').strip().upper() if type_key else 'DI'
            if io_type not in self.IO_TYPES:
                io_type = 'DI'
            try:
                channel_count = int(row.get(channel_key, 0)) if channel_key else 0
            except (ValueError, TypeError):
                channel_count = 0

            entity = {
                "model": model,
                "type": io_type,
                "channel_count": channel_count,
                "signal_type": row.get(signal_key, '') if signal_key else '',
                "response_time": 0
            }
            tags = [model, io_type, "I/O模块"]
            results.append({
                "entity_type": "IO_Module",
                "entity": entity,
                "provenance": dict(provenance),
                "tags": tags
            })
        return results

    def _extract_devices(self, rows: List[Dict], headers: List[str],
                          provenance: Dict) -> List[Dict[str, Any]]:
        """提取设备实体"""
        results = []
        name_key = self._find_key(headers, ['名称', 'name', '设备名称'])
        model_key = self._find_key(headers, ['型号', 'model'])
        mfr_key = self._find_key(headers, ['厂商', 'manufacturer', '厂家'])

        for row in rows:
            model = row.get(model_key, '').strip() if model_key else ''
            name = row.get(name_key, model).strip() if name_key else model
            if not model:
                continue
            entity = {
                "name": name,
                "model": model,
                "manufacturer": row.get(mfr_key, '') if mfr_key else '',
                "specs": {},
                "capabilities": []
            }
            tags = [model, name]
            results.append({
                "entity_type": "Device",
                "entity": entity,
                "provenance": dict(provenance),
                "tags": tags
            })
        return results

    def _extract_params(self, rows: List[Dict], headers: List[str],
                         provenance: Dict) -> List[Dict[str, Any]]:
        """提取参数表 → Constraint"""
        results = []
        rule_key = self._find_key(headers, ['规则', 'rule', '参数', 'param', '项目'])
        value_key = self._find_key(headers, ['值', 'value', '设定值', '范围'])

        for row in rows:
            rule_text = row.get(rule_key, '').strip() if rule_key else ''
            if not rule_text:
                continue
            value = row.get(value_key, '') if value_key else ''
            entity = {
                "rule": f"{rule_text} = {value}" if value else rule_text,
                "scope": "",
                "severity": "info",
                "rationale": f"从参数表提取"
            }
            results.append({
                "entity_type": "Constraint",
                "entity": entity,
                "provenance": dict(provenance),
                "tags": ["参数", rule_text[:20]]
            })
        return results

    def _extract_generic(self, rows: List[Dict], headers: List[str],
                          provenance: Dict) -> List[Dict[str, Any]]:
        """通用表格 → BestPractice"""
        results = []
        # 把整个表格摘要为一个 BestPractice
        summary_parts = [f"表格包含 {len(rows)} 行数据，列: {', '.join(headers[:5])}"]
        for i, row in enumerate(rows[:5]):
            parts = [f"{k}={v}" for k, v in list(row.items())[:3] if v]
            if parts:
                summary_parts.append(f"  行{i+1}: {', '.join(parts)}")

        entity = {
            "title": f"表格数据: {provenance.get('source_path', 'unknown')}",
            "content": '\n'.join(summary_parts),
            "tags": ["表格数据"],
            "examples": []
        }
        results.append({
            "entity_type": "BestPractice",
            "entity": entity,
            "provenance": dict(provenance),
            "tags": ["表格数据"]
        })
        return results

    def _find_key(self, headers: List[str], candidates: List[str]) -> str:
        """在 headers 中查找匹配的 key"""
        for h in headers:
            for c in candidates:
                if c in h:
                    return h
        return ''


if __name__ == "__main__":
    import tempfile

    # 测试 CSV 提取
    test_csv = """型号,类型,通道数,信号类型
AX100,DI,16,24VDC
AX200,DO,16,24VDC
AX300,AI,8,4-20mA
AX400,RTD,4,Pt100
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        f.write(test_csv)
        tmpfile = f.name

    try:
        extractor = TableExtractor()
        results = extractor.extract(tmpfile)
        print(f"提取到 {len(results)} 个实体:")
        for r in results:
            e = r['entity']
            print(f"  [{r['entity_type']}] {e.get('model', '?')} type={e.get('type', '?')} ch={e.get('channel_count', '?')}")
    finally:
        os.unlink(tmpfile)

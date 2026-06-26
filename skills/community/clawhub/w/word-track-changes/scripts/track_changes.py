#!/usr/bin/env python3
"""
Word Track Changes - 核心库
支持跨 <w:t> 节点的文本查找和精确修订
"""
import zipfile
import shutil
import os
import tempfile
from datetime import datetime
from xml.etree import ElementTree as ET

# 命名空间
NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
}

# 注册命名空间
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)


def _w(tag):
    return f'{{{NS["w"]}}}{tag}'


def _get_full_text(element):
    """获取元素的所有文本内容"""
    return ''.join(t.text or '' for t in element.findall(f'.//{_w("t")}'))


def _extract_rpr(run_elem):
    """提取 <w:rPr> 格式属性节点"""
    rpr = run_elem.find(_w('rPr'))
    if rpr is not None:
        # 深拷贝
        return ET.fromstring(ET.tostring(rpr, encoding='unicode'))
    return None


def _copy_run_format(source_run):
    """复制一个 <w:r> 的格式，但不包含文本内容"""
    new_run = ET.Element(_w('r'))
    # 复制属性（如 rsidRPr）
    for key, val in source_run.attrib.items():
        new_run.set(key, val)
    
    rpr = _extract_rpr(source_run)
    if rpr is not None:
        new_run.append(rpr)
    return new_run


def _create_del_element(text, rev_id, author, date_str, rpr_elem=None):
    """创建删除标记 <w:del>"""
    del_elem = ET.Element(_w('del'))
    del_elem.set(_w('id'), str(rev_id))
    del_elem.set(_w('author'), author)
    del_elem.set(_w('date'), date_str)
    
    r = ET.SubElement(del_elem, _w('r'))
    if rpr_elem is not None:
        r.append(ET.fromstring(ET.tostring(rpr_elem, encoding='unicode')))
    
    del_text = ET.SubElement(r, _w('delText'))
    del_text.text = text
    return del_elem


def _create_ins_element(text, rev_id, author, date_str, rpr_elem=None):
    """创建插入标记 <w:ins>"""
    ins_elem = ET.Element(_w('ins'))
    ins_elem.set(_w('id'), str(rev_id))
    ins_elem.set(_w('author'), author)
    ins_elem.set(_w('date'), date_str)
    
    r = ET.SubElement(ins_elem, _w('r'))
    if rpr_elem is not None:
        r.append(ET.fromstring(ET.tostring(rpr_elem, encoding='unicode')))
    
    t = ET.SubElement(r, _w('t'))
    t.text = text
    return ins_elem


def _insert_after(parent, reference, new_elem):
    """在 reference 元素后插入 new_elem"""
    idx = list(parent).index(reference)
    parent.insert(idx + 1, new_elem)


def _replace_text_in_para(para_elem, old_text, new_text, rev_id, author, date_str):
    """
    在段落内精确替换文本，支持跨 <w:t> 节点
    返回 (success, rev_id_offset)
    """
    # 收集段落中所有 <w:t> 节点及其父 <w:r>
    text_nodes = []
    for t in para_elem.findall(f'.//{_w("t")}'):
        # 找到父 <w:r>
        parent = None
        for ancestor in para_elem.iter():
            if ancestor != para_elem:
                for child in ancestor:
                    if child is t or t in child.iter():
                        if ancestor.tag == _w('r'):
                            parent = ancestor
                            break
                if parent:
                    break
        
        # 如果 t 直接在 r 下
        if hasattr(t, 'getparent') and t.getparent is not None:
            # lxml style
            try:
                parent = t.getparent()
                if parent.tag != _w('r'):
                    parent = None
            except AttributeError:
                pass
        
        if parent is None:
            # 向上查找一层
            for r in para_elem.findall(f'.//{_w("r")}'):
                if t in list(r):
                    parent = r
                    break
        
        text_nodes.append((t, parent, t.text or ''))
    
    # 拼接完整文本
    full_text = ''.join(txt for _, _, txt in text_nodes)
    
    if old_text not in full_text:
        return False, 0
    
    idx = full_text.find(old_text)
    old_end = idx + len(old_text)
    
    # 定位起止节点和偏移
    current_pos = 0
    start_info = None
    end_info = None
    
    for i, (t_node, r_node, txt) in enumerate(text_nodes):
        t_len = len(txt)
        if current_pos <= idx < current_pos + t_len:
            start_info = (i, t_node, r_node, idx - current_pos)
        if current_pos < old_end <= current_pos + t_len:
            end_info = (i, t_node, r_node, old_end - current_pos)
            break
        current_pos += t_len
    
    if not start_info or not end_info:
        return False, 0
    
    start_i, start_t, start_r, start_off = start_info
    end_i, end_t, end_r, end_off = end_info
    
    # 获取 start_r 在 para 中的位置
    para_children = list(para_elem)
    
    # 找到 start_r 在 para_elem 中的索引
    def _find_run_index(run_elem):
        for i, child in enumerate(para_elem):
            if child is run_elem:
                return i
            # 也可能嵌套在其他元素中
            for sub in child.iter():
                if sub is run_elem:
                    return i
        return -1
    
    start_r_idx = _find_run_index(start_r)
    if start_r_idx == -1:
        # fallback: 如果 run 嵌套在诸如 hyperlink 等结构中，直接返回失败
        return False, 0
    
    # 处理同一个 run 内的情况
    def _do_single_run():
        nonlocal rev_id
        t_text = start_t.text or ''
        prefix = t_text[:start_off]
        suffix = t_text[end_off:]
        
        rpr = _extract_rpr(start_r)
        
        # 构建替换序列
        new_elements = []
        if prefix:
            prefix_r = _copy_run_format(start_r)
            prefix_t = ET.SubElement(prefix_r, _w('t'))
            prefix_t.text = prefix
            new_elements.append(prefix_r)
        
        new_elements.append(_create_del_element(old_text, rev_id, author, date_str, rpr))
        rev_id += 1
        new_elements.append(_create_ins_element(new_text, rev_id, author, date_str, rpr))
        rev_id += 1
        
        if suffix:
            suffix_r = _copy_run_format(start_r)
            suffix_t = ET.SubElement(suffix_r, _w('t'))
            suffix_t.text = suffix
            new_elements.append(suffix_r)
        
        # 在 start_r 的位置插入新元素
        insert_idx = start_r_idx
        for elem in new_elements:
            para_elem.insert(insert_idx, elem)
            insert_idx += 1
        
        para_elem.remove(start_r)
        return True
    
    if start_r is end_r:
        return _do_single_run(), rev_id - start_i  # rev_id 已经在函数内递增了
    
    # 跨多个 run 的情况
    # 策略：简化处理 - 找到 start_r 和 end_r 在段落中的位置，
    # 保留 start_r 之前的内容和 end_r 之后的内容
    # 中间所有内容删除，替换为 del + ins
    
    rpr = _extract_rpr(start_r)
    
    # 收集所有需要处理的 run（直接在 para 下的，或嵌套在类似 hyperlink 下的）
    runs_to_process = []
    collecting = False
    for child in list(para_elem):
        if child is start_r:
            collecting = True
            runs_to_process.append(child)
        elif child is end_r:
            if collecting:
                runs_to_process.append(child)
            collecting = False
            break
        elif collecting:
            runs_to_process.append(child)
    
    # 如果 start_r 和 end_r 不在 para 的直接子元素中，需要更复杂的处理
    if not runs_to_process or runs_to_process[-1] is not end_r:
        # 尝试在嵌套结构中查找
        # 简化：直接处理 start_r 和 end_r
        runs_to_process = [start_r, end_r]
    
    # 处理 start_r: 保留前缀
    start_t_text = start_t.text or ''
    if start_off > 0:
        prefix = start_t_text[:start_off]
        start_t.text = start_t_text[start_off:]
        
        prefix_r = _copy_run_format(start_r)
        prefix_t = ET.SubElement(prefix_r, _w('t'))
        prefix_t.text = prefix
        _insert_after(para_elem, start_r, prefix_r)
    
    # 处理 end_r: 保留后缀
    end_t_text = end_t.text or ''
    if end_off < len(end_t_text):
        suffix = end_t_text[end_off:]
        end_t.text = end_t_text[:end_off]
        
        suffix_r = _copy_run_format(end_r)
        suffix_t = ET.SubElement(suffix_r, _w('t'))
        suffix_t.text = suffix
        _insert_after(para_elem, end_r, suffix_r)
    
    # 移除 start_r 和 end_r 中剩余的文本节点（它们将成为 del 的一部分）
    # 实际上我们现在要删除所有 runs_to_process，并插入 del + ins
    
    # 确定要删除的 runs 列表
    first_idx = para_children.index(runs_to_process[0])
    last_idx = para_children.index(runs_to_process[-1])
    
    del_elem = _create_del_element(old_text, rev_id, author, date_str, rpr)
    rev_id += 1
    ins_elem = _create_ins_element(new_text, rev_id, author, date_str, rpr)
    rev_id += 1
    
    # 在 last_idx 后插入 ins
    para_elem.insert(last_idx + 1, ins_elem)
    # 在 last_idx 后插入 del（在 ins 前面）
    para_elem.insert(last_idx + 1, del_elem)
    
    # 删除原来的 runs
    for run in reversed(runs_to_process):
        para_elem.remove(run)
    
    return True, rev_id


class TrackChangesProcessor:
    """Word 修订模式处理器"""
    
    def __init__(self, docx_path):
        self.docx_path = docx_path
        self.temp_dir = tempfile.mkdtemp(prefix='word_track_changes_')
        
        with zipfile.ZipFile(docx_path, 'r') as z:
            z.extractall(self.temp_dir)
        
        self.tree = ET.parse(os.path.join(self.temp_dir, 'word/document.xml'))
        self.root = self.tree.getroot()
        self.rev_id = 1
        self.author = "Agent"
        self.date_str = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    
    def set_author(self, author):
        self.author = author
    
    def find_paragraphs_containing(self, text):
        """查找包含特定文本的所有段落"""
        results = []
        for p in self.root.findall(f'.//{_w("p")}'):
            para_text = _get_full_text(p)
            if text in para_text:
                results.append(p)
        return results
    
    def replace_text_with_revision(self, old_text, new_text):
        """用修订模式替换文本"""
        paras = self.find_paragraphs_containing(old_text)
        if not paras:
            raise ValueError(f"未在文档中找到文本: {old_text[:50]}...")
        
        # 只替换第一个匹配
        para = paras[0]
        success, new_rev_id = _replace_text_in_para(
            para, old_text, new_text, self.rev_id, self.author, self.date_str
        )
        if success:
            self.rev_id = new_rev_id
            return True
        return False
    
    def insert_paragraph_after(self, search_text, new_text):
        """在包含 search_text 的段落后插入新段落（带插入标记）"""
        paras = self.find_paragraphs_containing(search_text)
        if not paras:
            raise ValueError(f"未在文档中找到文本: {search_text[:50]}...")
        
        target_para = paras[0]
        parent = None
        
        # 找到 target_para 的父元素
        for elem in self.root.iter():
            if target_para in list(elem):
                parent = elem
                break
        
        if parent is None:
            # target_para 可能是 root 的直接子元素（body）
            if target_para in list(self.root):
                parent = self.root
        
        if parent is None:
            raise RuntimeError("无法找到段落的父元素")
        
        target_idx = list(parent).index(target_para)
        
        # 复制目标段落的格式属性
        ppr = target_para.find(_w('pPr'))
        
        new_para = ET.Element(_w('p'))
        # 设置段落属性
        if ppr is not None:
            new_ppr = ET.fromstring(ET.tostring(ppr, encoding='unicode'))
            new_para.append(new_ppr)
        
        # 插入标记
        ins_elem = _create_ins_element(new_text, self.rev_id, self.author, self.date_str)
        self.rev_id += 1
        new_para.append(ins_elem)
        
        parent.insert(target_idx + 1, new_para)
        return True
    
    def enable_track_changes(self):
        """在 settings.xml 中启用修订追踪"""
        settings_path = os.path.join(self.temp_dir, 'word/settings.xml')
        if not os.path.exists(settings_path):
            return False
        
        settings_tree = ET.parse(settings_path)
        settings_root = settings_tree.getroot()
        
        # 检查是否已有 trackRevisions
        existing = settings_root.find(_w('trackRevisions'))
        if existing is None:
            track = ET.SubElement(settings_root, _w('trackRevisions'))
            # 不需要子元素或文本内容
        
        settings_tree.write(settings_path, encoding='UTF-8', xml_declaration=True)
        return True
    
    def save(self, output_path):
        """保存修改后的文档"""
        # 写入 document.xml
        doc_path = os.path.join(self.temp_dir, 'word/document.xml')
        self.tree.write(doc_path, encoding='UTF-8', xml_declaration=True)
        
        # 重新打包
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root_dir, dirs, files in os.walk(self.temp_dir):
                for file in files:
                    file_path = os.path.join(root_dir, file)
                    arcname = os.path.relpath(file_path, self.temp_dir)
                    zipf.write(file_path, arcname)
    
    def cleanup(self):
        """清理临时文件"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)


# 便捷函数 API（向下兼容）
def enable_track_changes(docx_path, output_path):
    p = TrackChangesProcessor(docx_path)
    p.enable_track_changes()
    p.save(output_path)
    p.cleanup()


def insert_text_with_revision(docx_path, search_text, new_text, author="Agent", output_path=None):
    p = TrackChangesProcessor(docx_path)
    p.set_author(author)
    p.replace_text_with_revision(search_text, new_text)
    out = output_path or docx_path
    p.save(out)
    p.cleanup()


def mark_deletion(docx_path, target_text, author="Agent", output_path=None):
    p = TrackChangesProcessor(docx_path)
    p.set_author(author)
    p.replace_text_with_revision(target_text, "")
    out = output_path or docx_path
    p.save(out)
    p.cleanup()


def batch_revisions(docx_path, revisions, author="Agent", output_path=None):
    """
    批量处理修订
    revisions: list of dicts, e.g.
    [
        {"type": "replace", "old": "...", "new": "..."},
        {"type": "insert_after", "search": "...", "new": "..."},
    ]
    """
    p = TrackChangesProcessor(docx_path)
    p.set_author(author)
    
    for rev in revisions:
        if rev.get("type") == "replace":
            p.replace_text_with_revision(rev["old"], rev["new"])
        elif rev.get("type") == "insert_after":
            p.insert_paragraph_after(rev["search"], rev["new"])
    
    out = output_path or docx_path
    p.save(out)
    p.cleanup()


if __name__ == "__main__":
    print("word-track-changes core library loaded.")

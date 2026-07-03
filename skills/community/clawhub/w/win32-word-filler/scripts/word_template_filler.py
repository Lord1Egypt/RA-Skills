#!/usr/bin/env python3
"""
word_template_filler.py — CLI tool to fill Word templates via win32com.
Preserves all formatting, images, underlines, and page layout.

Usage:
  python word_template_filler.py template.docx output.docx ^
    --cover-field "所在学院:铁道工程学院" ^
    --append-answer "Q1:answer text here" ^
    --insert-blank-para "Table2:8:基础制动装置" ^
    --page-break-before "C2.转向架" ^
    --find-replace "。？:。" ^
    --set-time "2026年6月"
"""
import argparse, sys, json, shutil, os

# ── helpers ──────────────────────────────────────────────────────────────

def _get_word():
    import win32com.client as win32
    return win32.gencache.EnsureDispatch('Word.Application')

def _fill_cover_field(doc, label, value):
    for p in doc.Paragraphs:
        txt = p.Range.Text
        if txt.startswith(label):
            colon_pos = txt.find('：')
            if colon_pos > 0:
                rng = p.Range.Duplicate
                rng.Start = rng.Start + colon_pos + 1
                after_rng = rng.Duplicate
                after_rng.Start = rng.Start
                if value:
                    after_rng.InsertBefore(value)
            return True
    return False

def _append_answer(cell, question_text, answer_text):
    rng = cell.Range.Duplicate
    f = rng.Find
    f.Text = question_text
    f.MatchCase = True; f.Forward = True; f.Wrap = 1
    if f.Execute():
        found = f.Parent
        found.MoveEnd(1, -1)
        found.Text = question_text + '\n' + answer_text
        return True
    return False

def _insert_blank_para(cell, para_1b, text):
    paras = cell.Range.Paragraphs
    if para_1b <= paras.Count:
        paras(para_1b).Range.InsertBefore(text)

def _page_break_before(doc, heading_text):
    for p in doc.Paragraphs:
        if heading_text in p.Range.Text:
            rng = p.Range.Duplicate
            rng.Collapse(1)
            rng.InsertBefore('\f')
            return True
    return False

def _find_replace(doc, find_text, replace_text):
    rng = doc.Range()
    f = rng.Find
    f.Text = find_text
    f.MatchCase = True; f.Forward = True; f.Wrap = 2
    f.Replacement.Text = replace_text
    f.Execute(Replace=2)

def _set_time_score(cell_row, time_text='', score_text=''):
    """Set 实训时间 and 得分 in a section table row."""
    if time_text:
        if cell_row.Cell(2, 2).Range.Text.strip():
            r = cell_row.Cell(2, 2).Range.Duplicate
            r.MoveEnd(1, -1)
            if r.Text.strip():
                r.Text = time_text
            else:
                r.InsertBefore(time_text)
    if score_text:
        r2 = cell_row.Cell(2, 4).Range.Duplicate
        if r2.Text.strip():
            r2.MoveEnd(1, -1)
            r2.Text = score_text
        else:
            r2.InsertBefore(score_text)

# ── main ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Fill Word templates via win32com')
    parser.add_argument('template', help='Path to template .docx')
    parser.add_argument('output', help='Path to save output .docx')
    parser.add_argument('--cover-field', '-c', action='append', default=[],
                        help='Cover field "label:value" e.g. "所在学院:铁道工程学院"')
    parser.add_argument('--append-answer', '-a', action='append', default=[],
                        help='Append answer "question_text|answer_text" in table cell')
    parser.add_argument('--insert-blank-para', '-p', action='append', default=[],
                        help='Insert into blank para "table_idx:row:col:para_1b:text"')
    parser.add_argument('--page-break-before', '-b', action='append', default=[],
                        help='Page break before heading text')
    parser.add_argument('--find-replace', '-r', action='append', default=[],
                        help='Find/replace "find:replace"')
    parser.add_argument('--set-time-score', '-t', action='append', default=[],
                        help='Set time/score "table_idx:time|score"')
    parser.add_argument('--visible', action='store_true', help='Show Word window')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.template):
        print(f"Error: template not found: {args.template}")
        sys.exit(1)
    
    shutil.copy2(args.template, args.output)
    
    word = _get_word()
    word.Visible = args.visible
    doc = word.Documents.Open(os.path.abspath(args.output))
    
    try:
        # Cover fields
        for field in args.cover_field:
            parts = field.split(':', 1)
            if len(parts) == 2:
                _fill_cover_field(doc, parts[0], parts[1])
                print(f"  Cover: {parts[0]} -> {parts[1]}")
        
        # Append answers — format: "TableRow:Cell:question_text||answer_text"
        for item in args.append_answer:
            parts = item.split('||', 1)
            if len(parts) == 2:
                loc = parts[0].strip()
                answer = parts[1].strip()
                # Format: "TableIdx:Row:Cell:question"
                loc_parts = loc.split(':', 3)
                if len(loc_parts) >= 4:
                    t_idx, r, c = int(loc_parts[0]), int(loc_parts[1]), int(loc_parts[2])
                    question = loc_parts[3]
                    cell = doc.Tables(t_idx).Cell(r, c)
                    _append_answer(cell, question, answer)
                    print(f"  Append: T{t_idx}R{r}C{c} -> {answer[:40]}...")
                elif len(loc_parts) == 1:
                    # Search whole doc
                    pass
        
        # Insert into blank paras — "TableIdx:Row:Cell:Para1B:text"
        for item in args.insert_blank_para:
            parts = item.split(':', 4)
            if len(parts) == 5:
                t_idx, r, c, p_idx, text = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]), parts[4]
                cell = doc.Tables(t_idx).Cell(r, c)
                _insert_blank_para(cell, p_idx, text)
                print(f"  Insert: T{t_idx}R{r}C{c}P{p_idx} <- {text[:30]}")
        
        # Page breaks
        for heading in args.page_break_before:
            _page_break_before(doc, heading)
            print(f"  Page break before: {heading}")
        
        # Find/Replace
        for item in args.find_replace:
            parts = item.split(':', 1)
            if len(parts) == 2:
                _find_replace(doc, parts[0], parts[1])
                print(f"  Replace: {parts[0]} -> {parts[1]}")
        
        doc.Save()
        print(f"\n✅ Saved: {args.output}")
        
    finally:
        doc.Close()
        word.Quit()

if __name__ == '__main__':
    main()

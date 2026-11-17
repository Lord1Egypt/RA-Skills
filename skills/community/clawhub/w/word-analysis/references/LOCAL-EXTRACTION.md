# 本地 Word 提取

执行 `python3 scripts/extract_word.py /绝对路径/document.docx`。脚本输出平台所需的 `document` JSON；仅支持 10 MB 内的标准 DOCX、最多 2000 个非空段落和 120000 字符。脚本只读取正文与表格文字，不做图片 OCR；需要识别内嵌图片文字时改用平台工作台上传。

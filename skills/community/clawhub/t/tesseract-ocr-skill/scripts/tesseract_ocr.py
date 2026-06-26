import pytesseract
from PIL import Image
import re
from typing import Dict, Any

def extract_text_with_tesseract(image_path: str, language: str = "chi_sim+eng", output_format: str = "text") -> Dict[str, Any]:
    """
    使用Tesseract从图像中提取文字
    """
    try:
        # 打开图片
        img = Image.open(image_path)
        
        # 使用Tesseract进行OCR
        extracted_text = pytesseract.image_to_string(img, lang=language)
        
        result = {
            "original_text": extracted_text.strip(),
            "processed_text": "",
            "structure": None
        }
        
        if output_format == "text":
            result["processed_text"] = extracted_text.strip()
        elif output_format == "structured":
            # 尝试识别结构化信息
            structured = identify_structure(extracted_text)
            result["processed_text"] = structured["formatted_text"]
            result["structure"] = structured["structure"]
        elif output_format == "question_answer":
            # 专门识别问答题
            qa_result = identify_questions_and_answers(extracted_text)
            result["processed_text"] = qa_result["formatted_text"]
            result["structure"] = qa_result["qa_pairs"]
        
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

def identify_structure(text: str) -> Dict[str, Any]:
    """
    识别文本结构（题目、选项、答案等）
    """
    lines = text.split('\n')
    structure = {
        "sections": [],
        "questions": [],
        "answers": [],
        "options": []
    }
    
    current_section = ""
    current_question = ""
    current_options = []
    current_answer = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 检查是否是章节标题（如"哮病"、"咳嗽"等）
        if re.search(r'(病|证|症|综合征)$', line):
            if current_section:
                structure["sections"].append(current_section)
            current_section = line
        # 检查是否是问题（数字+. 或者中文数字+、）
        elif re.match(r'^\d+[\.．、]', line) or re.match(r'^[一二三四五六七八九十\d]+[\.．、]', line):
            if current_question:
                # 保存上一个问题
                structure["questions"].append(current_question)
                if current_options:
                    structure["options"].append(current_options)
                if current_answer:
                    structure["answers"].append(current_answer)
                    
            current_question = line
            current_options = []
            current_answer = ""
        elif re.match(r'^[A-Z][\.．:：]', line) or re.match(r'^[（\(][A-Z][）\)]', line):
            # 检查是否是选项
            current_options.append(line)
        elif '答案' in line or '答：' in line or ('【' in line and '】' in line):
            # 检查是否是答案
            current_answer = line
        else:
            if current_question and not any(opt in line for opt in ['A.', 'B.', 'C.', 'D.', 'E.', 'F.']):
                # 添加到当前问题中
                current_question += '\n' + line
    
    # 添加最后一个
    if current_question:
        structure["questions"].append(current_question)
        if current_options:
            structure["options"].append(current_options)
        if current_answer:
            structure["answers"].append(current_answer)
    
    # 如果没有找到特定结构，返回原始文本
    if not structure["questions"] and not structure["sections"]:
        return {
            "formatted_text": text,
            "structure": {"raw_text": text}
        }
    
    # 格式化输出
    formatted_text = ""
    if structure["sections"]:
        for section in structure["sections"]:
            formatted_text += f"【{section}】\n"
    if structure["questions"]:
        for i, q in enumerate(structure["questions"]):
            formatted_text += f"题目{i+1}: {q}\n"
            if i < len(structure["options"]):
                for opt in structure["options"][i]:
                    formatted_text += f"  {opt}\n"
            if i < len(structure["answers"]):
                formatted_text += f"  答案: {structure['answers'][i]}\n"
            formatted_text += "\n"
    
    return {
        "formatted_text": formatted_text.strip(),
        "structure": structure
    }

def identify_questions_and_answers(text: str) -> Dict[str, Any]:
    """
    专门识别问题和答案
    """
    # 按段落分割文本
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    
    qa_pairs = []
    current_qa = {"question": "", "answer": ""}
    
    for para in paragraphs:
        # 检查是否是问题（以数字开头）
        if re.match(r'^\d+[\.．、]', para) or re.match(r'^[一二三四五六七八九十\d]+[\.．、]', para):
            if current_qa["question"]:
                # 保存上一个QA对
                qa_pairs.append(current_qa.copy())
            
            # 开始新问题
            current_qa = {"question": para, "answer": ""}
        elif '答案' in para or '答：' in para or ('【' in para and '】' in para):
            # 答案行
            current_qa["answer"] = para
        else:
            # 可能是问题的延续
            if current_qa["question"] and not current_qa["answer"]:
                current_qa["question"] += '\n' + para
            elif current_qa["answer"]:
                current_qa["answer"] += '\n' + para
    
    # 添加最后一个
    if current_qa["question"]:
        qa_pairs.append(current_qa)
    
    formatted_text = ""
    for i, pair in enumerate(qa_pairs):
        formatted_text += f"Q{i+1}: {pair['question']}\n"
        formatted_text += f"A{i+1}: {pair['answer']}\n\n"
    
    return {
        "formatted_text": formatted_text.strip(),
        "qa_pairs": qa_pairs
    }

def main(params: Dict[str, Any]) -> Dict[str, Any]:
    image_path = params.get("image_path")
    language = params.get("language", "chi_sim+eng")
    output_format = params.get("output_format", "text")
    
    return extract_text_with_tesseract(image_path, language, output_format)

def extract_text_with_tesseract(image_path: str, language: str = "chi_sim+eng", output_format: str = "text") -> Dict[str, Any]:
    """
    使用Tesseract从图像中提取文字
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(image_path):
            return {
                "status": "error",
                "message": f"Image file does not exist: {image_path}"
            }
        
        # 打开图片
        img = Image.open(image_path)
        
        # 使用Tesseract进行OCR
        extracted_text = pytesseract.image_to_string(img, lang=language)
        
        result = {
            "original_text": extracted_text.strip(),
            "processed_text": "",
            "structure": None
        }
        
        if output_format == "text":
            result["processed_text"] = extracted_text.strip()
        elif output_format == "structured":
            # 尝试识别结构化信息
            structured = identify_structure(extracted_text)
            result["processed_text"] = structured["formatted_text"]
            result["structure"] = structured["structure"]
        elif output_format == "question_answer":
            # 专门识别问答题
            qa_result = identify_questions_and_answers(extracted_text)
            result["processed_text"] = qa_result["formatted_text"]
            result["structure"] = qa_result["qa_pairs"]
        
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
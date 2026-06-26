import base64
import json
import os
import io
from typing import Any, Dict, List, Optional, Union
from PIL import Image

from cnocr import CnOcr
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


API_KEY = "自己的apk"
BASE_URL = "https://api.minimaxi.com/v1"
MODEL_NAME = "MiniMax-M2.5"
MAX_IMAGE_SIZE = 1024
IMAGE_QUALITY = 80

_ocr_model = None

def get_ocr_model():
    global _ocr_model
    if _ocr_model is None:
        _ocr_model = CnOcr()
    return _ocr_model


def ocr_recognize(image_path: str) -> List[str]:
    """
    使用cnocr识别图片中的文字

    参数:
        image_path: 图片文件路径

    返回:
        list: 识别出的文字列表，每行是一个元素
    """
    cn_ocr = get_ocr_model()
    result = cn_ocr.ocr(image_path)

    text_lines = []
    for line in result:
        if isinstance(line, str):
            text_lines.append(line)
        elif isinstance(line, dict):
            text_lines.append(line.get('text', ''))
        else:
            try:
                line_text = ''.join([item['text'] for item in line])
                text_lines.append(line_text)
            except:
                text_lines.append(str(line))

    return text_lines


def encode_image(image_path: str, max_size: int = MAX_IMAGE_SIZE, quality: int = IMAGE_QUALITY) -> str:
    img = Image.open(image_path)

    if max(img.size) > max_size:
        ratio = max_size / max(img.size)
        new_size = tuple(int(dim * ratio) for dim in img.size)
        img = img.resize(new_size, Image.LANCZOS)

    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=quality, optimize=True)
    return base64.b64encode(buffer.getvalue()).decode('utf-8')


def get_chat_model(
    temperature: float = 1.0,
    max_tokens: int = 3000,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    base_url: Optional[str] = None,
) -> ChatOpenAI:
    return ChatOpenAI(
        model=model or MODEL_NAME,
        base_url=base_url or BASE_URL,
        api_key=api_key or API_KEY,
        temperature=temperature,
        max_tokens=max_tokens,
    )


def chat_with_json_output(
    prompt: str,
    image_path: Optional[str] = None,
    image_base64: Optional[str] = None,
    json_schema: Optional[type[BaseModel]] = None,
    temperature: float = 1.0,
    max_tokens: int = 3000,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    base_url: Optional[str] = None,
) -> Union[Dict[str, Any], str]:
    llm = get_chat_model(
        temperature=temperature,
        max_tokens=max_tokens,
        api_key=api_key,
        model=model,
        base_url=base_url,
    )

    if json_schema:
        llm = llm.with_structured_output(json_schema)

    if image_path:
        base64_image = encode_image(image_path)
    elif image_base64:
        base64_image = image_base64
    else:
        base64_image = None

    if base64_image:
        image_url = f"data:image/jpeg;base64,{base64_image}"
        messages = [HumanMessage(content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": image_url}}
        ])]
    else:
        messages = [HumanMessage(content=prompt)]

    if json_schema:
        result = llm.invoke(messages)
        return result.model_dump(mode='json') if hasattr(result, 'model_dump') else dict(result)
    else:
        response = llm.invoke(messages)
        response_text = response.content

        try:
            json_start = response_text.find('[')
            json_end = response_text.rfind(']') + 1
            if json_start != -1 and json_end != 0:
                json_str = response_text[json_start:json_end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass

        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                json_str = response_text[json_start:json_end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass

        return {"raw_response": response_text}


class SalesData(BaseModel):
    日期: str = Field(default="", description="日期 YYYY-MM-DD")
    总销售: str = Field(default="", description="总销售金额")
    产品净销售: str = Field(default="", description="产品净销售金额")
    现烤面包: str = Field(default="", description="现烤面包金额")
    袋装面包: str = Field(default="", description="袋装面包金额")
    软点: str = Field(default="", description="软点金额")
    西点: str = Field(default="", description="西点金额")
    中点: str = Field(default="", description="中点金额")
    蛋糕个数: str = Field(default="", description="蛋糕个数")
    蛋糕金额: str = Field(default="", description="蛋糕金额")
    卡劵: str = Field(default="", description="卡劵金额")
    交易次数: str = Field(default="", description="交易次数")


class SalesDataList(BaseModel):
    data: List[SalesData] = Field(default_factory=list, description="销售数据列表")


def extract_sales_data(image_path: str) -> List[Dict[str, Any]]:
    prompt = """请从这张销售报表图片中提取所有日期的数据。

图片中可能包含多个日期的销售数据，请全部提取出来。

请严格按照以下JSON格式输出一个数组，不要添加任何其他内容：
[
  {"日期": "", "总销售": "", "产品净销售": "", "现烤面包": "", "袋装面包": "", "软点": "", "西点": "", "中点": "", "蛋糕个数": "", "蛋糕金额": "", "卡劵": "", "交易次数": ""}
]

注意：
1. 日期格式请提取为 YYYY-MM-DD 格式
2. 图片中的所有数据必须完整准确提取，不能遗漏任何一个字段
3. 如果某个字段在图片中找不到，请填写"无"
4. 如果图片只包含1天的数据，就只返回1个对象"""

    return chat_with_json_output(prompt, image_path=image_path)


def extract_sales_data_from_ocr(image_path: str) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    """
    先用OCR识别图片文字，然后将识别出的文本发送给大模型进行JSON转换

    参数:
        image_path: 图片文件路径

    返回:
        解析后的JSON数据
    """
    print(f"正在OCR识别图片: {image_path}")
    text_lines = ocr_recognize(image_path)

    if not text_lines:
        return {"error": "OCR未能识别出任何文字"}

    ocr_text = "\n".join(text_lines)
    print(f"OCR识别结果:\n{ocr_text}")

    prompt = f"""请从以下OCR识别的销售报表文本中提取数据。

OCR识别结果：
{ocr_text}

请严格按照以下JSON格式输出一个数组，不要添加任何其他内容：
[
  {{"日期": "", "总销售": "", "产品净销售": "", "现烤面包": "", "袋装面包": "", "软点": "", "西点": "", "中点": "", "蛋糕个数": "", "蛋糕金额": "", "卡劵": "", "交易次数": ""}}
]

注意：
1. 日期格式请提取为 YYYY-MM-DD 格式
2. OCR识别可能存在误差，请根据上下文合理推断和修正数据
3. 图片中的所有数据必须完整准确提取，不能遗漏任何一个字段
4. 如果某个字段在文本中找不到，请填写"无"
5. 如果文本只包含1天的数据，就只返回1个对象"""

    return simple_chat_with_json(prompt)


def analyze_image(
    prompt: str,
    image_path: Optional[str] = None,
    image_base64: Optional[str] = None,
    temperature: float = 1.0,
) -> str:
    llm = get_chat_model(temperature=temperature)

    if image_path:
        base64_image = encode_image(image_path)
    elif image_base64:
        base64_image = image_base64
    else:
        base64_image = None

    if base64_image:
        image_url = f"data:image/jpeg;base64,{base64_image}"
        messages = [HumanMessage(content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": image_url}}
        ])]
    else:
        messages = [HumanMessage(content=prompt)]
    
    response = llm.invoke(messages)

    return response.content


def simple_chat(
    message: str,
    system_prompt: Optional[str] = None,
    temperature: float = 1.0,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    base_url: Optional[str] = None,
) -> str:
    llm = get_chat_model(
        temperature=temperature,
        api_key=api_key,
        model=model,
        base_url=base_url,
    )

    messages = []
    if system_prompt:
        messages.append(SystemMessage(content=system_prompt))
    messages.append(HumanMessage(content=message))

    response = llm.invoke(messages)

    return response.content


def simple_chat_with_json(
    prompt: str,
    temperature: float = 1.0,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    base_url: Optional[str] = None,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """
    发送文本给大模型并尝试解析JSON响应

    参数:
        prompt: 发送给大模型的文本提示
        temperature: 温度参数
        api_key: API密钥
        model: 模型名称
        base_url: API地址

    返回:
        解析后的JSON数据
    """
    response_text = simple_chat(
        prompt,
        temperature=temperature,
        api_key=api_key,
        model=model,
        base_url=base_url,
    )

    try:
        json_start = response_text.find('[')
        json_end = response_text.rfind(']') + 1
        if json_start != -1 and json_end != 0:
            json_str = response_text[json_start:json_end]
            return json.loads(json_str)
    except json.JSONDecodeError:
        pass

    try:
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        if json_start != -1 and json_end != 0:
            json_str = response_text[json_start:json_end]
            return json.loads(json_str)
    except json.JSONDecodeError:
        pass

    return {"raw_response": response_text}


def chat_with_prompt_template(
    system_prompt: str,
    user_prompt: str,
    prompt_variables: Optional[Dict[str, Any]] = None,
    image_path: Optional[str] = None,
    temperature: float = 1.0,
) -> str:
    llm = get_chat_model(temperature=temperature)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", user_prompt)
    ])

    if image_path:
        base64_image = encode_image(image_path)
        image_url = f"data:image/jpeg;base64,{base64_image}"
        messages = [HumanMessage(content=[
            {"type": "text", "text": user_prompt.format(**(prompt_variables or {}))},
            {"type": "image_url", "image_url": {"url": image_url}}
        ])]
    else:
        if prompt_variables:
            formatted_prompt = user_prompt.format(**prompt_variables)
        else:
            formatted_prompt = user_prompt
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=formatted_prompt)
        ]

    response = llm.invoke(messages)

    return response.content


if __name__ == "__main__":
    print("=" * 60)
    print("LangChain + MiniMax API 测试")
    print("=" * 60)

    test_image = "1,8.jpg"
    if os.path.exists(test_image):
        print(f"\n测试OCR识别 + 大模型JSON转换: {test_image}")
        result = extract_sales_data_from_ocr(test_image)
        print(f"提取结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    else:
        print(f"\n测试文本对话功能")
        response = simple_chat("你好，请介绍一下你自己")
        print(f"回复: {response}")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

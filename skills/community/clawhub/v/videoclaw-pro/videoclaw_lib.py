"""
VideoClaw Pro Library - 增强版飞书文档读写，支持 wiki 链接和权限错误提示
"""
import re
import requests
import lark_oapi as lark
from lark_oapi.api.docx.v1 import *

# ==========================================
# 飞书应用凭证配置
# ==========================================
APP_ID = "cli_a95e1b5ed9381cc3"
APP_SECRET = "DIBBsLgYDgewHACSjcMHahm80kyRmFc5"

# 你的目标文件夹 Token，如果不填，默认会创建在机器人的云空间根目录
TARGET_FOLDER_TOKEN = ""

# 初始化飞书客户端
client = lark.Client.builder().app_id(APP_ID).app_secret(APP_SECRET).build()

# 缓存 access_token，避免频繁获取
_cached_access_token = None
_cached_token_expire = 0

def _get_access_token() -> str:
    """获取飞书访问令牌，带缓存"""
    global _cached_access_token, _cached_token_expire
    import time
    
    # 如果缓存未过期，直接返回
    if _cached_access_token and time.time() < _cached_token_expire:
        return _cached_access_token
    
    resp = requests.post(
        'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
        json={'app_id': APP_ID, 'app_secret': APP_SECRET}
    )
    json_data = resp.json()
    
    if json_data.get('code') != 0:
        raise Exception(f"获取 access_token 失败: {json_data.get('msg')}")
    
    _cached_access_token = json_data.get('tenant_access_token')
    # 提前5分钟过期，避免临界问题
    _cached_token_expire = time.time() + json_data.get('expire', 7200) - 300
    
    return _cached_access_token


def _is_wiki_url(url: str) -> bool:
    """判断是否为 wiki 链接"""
    return '/wiki/' in url


def _extract_wiki_node_token(url: str) -> str:
    """从 wiki 链接中提取 node_token"""
    match = re.search(r'/wiki/([a-zA-Z0-9]+)', url)
    if match:
        return match.group(1)
    raise ValueError(f"无法从链接 {url} 中提取 wiki node_token")


def _resolve_wiki_to_docx(wiki_url: str) -> str:
    """
    将 wiki 链接解析为 docx 文档 token 或 file token
    通过查询 wiki node 获取背后的文档信息
    """
    node_token = _extract_wiki_node_token(wiki_url)
    print(f"[Skill] 正在解析 wiki 链接，node_token: {node_token}")
    
    try:
        # 直接调用飞书 API 获取 wiki node 信息
        access_token = _get_access_token()
        headers = {'Authorization': f'Bearer {access_token}'}
        resp = requests.get(
            f'https://open.feishu.cn/open-apis/wiki/v2/spaces/get_node?token={node_token}',
            headers=headers
        )
        
        if resp.status_code != 200:
            raise Exception(f"Wiki API 调用失败: HTTP {resp.status_code}")
        
        json_data = resp.json()
        if json_data.get('code') != 0:
            raise Exception(f"Wiki API 调用失败: {json_data.get('msg')}")
        
        data = json_data.get('data', {})
        node = data.get('node', {})
        obj_token = node.get('obj_token')
        obj_type = node.get('obj_type')
        title = node.get('title', 'unknown')
        
        if not obj_token:
            raise Exception(f"无法从 wiki node 响应中提取文档 token")
        
        print(f"[Skill] Wiki 解析成功，obj_token: {obj_token}, 类型: {obj_type}, 标题: {title}")
        
        # 返回一个元组，包含 (obj_token, obj_type, title)
        return (obj_token, obj_type, title)
        
    except Exception as e:
        if "Wiki API" in str(e) or "wiki node" in str(e):
            raise
        raise Exception(f"解析 wiki 链接失败: {str(e)}")


def _extract_document_id(doc_url: str) -> str:
    """
    从飞书文档链接中提取 document_id
    支持 docx 和 wiki 两种格式
    
    对于 wiki 链接，返回的是 (obj_token, obj_type, title) 元组
    """
    # 如果是 wiki 链接，先解析为 docx token
    if _is_wiki_url(doc_url):
        result = _resolve_wiki_to_docx(doc_url)
        # result 是一个元组 (obj_token, obj_type, title)
        if isinstance(result, tuple):
            return result
        return result
    
    # 匹配 docx 类型的链接: https://*.feishu.cn/docx/xxxxxxxxxxxxxx
    match = re.search(r'/docx/([a-zA-Z0-9]+)', doc_url)
    if match:
        return (match.group(1), 'docx', None)
    
    raise ValueError(
        f"无法从链接 {doc_url} 中提取 document_id。"
        f"支持的格式：\n"
        f"  - 文档链接：https://*.feishu.cn/docx/xxxxxxxxxx\n"
        f"  - 知识库链接：https://*.feishu.cn/wiki/xxxxxxxxxx"
    )


def _parse_blocks_to_text(blocks: list) -> str:
    """将飞书的 Block 结构简单解析为纯文本/Markdown"""
    result = []
    for block in blocks:
        block_type = block.block_type
        
        # 处理文本块 (Text)
        if block_type == 2 and block.text and block.text.elements:
            text_content = "".join([elem.text_run.content for elem in block.text.elements if elem.text_run])
            result.append(text_content)
        
        # 处理标题1 (Heading1)
        elif block_type == 3 and block.heading1 and block.heading1.elements:
            text_content = "".join([elem.text_run.content for elem in block.heading1.elements if elem.text_run])
            result.append(f"# {text_content}")
            
        # 处理标题2 (Heading2)
        elif block_type == 4 and block.heading2 and block.heading2.elements:
            text_content = "".join([elem.text_run.content for elem in block.heading2.elements if elem.text_run])
            result.append(f"## {text_content}")
            
        # 处理标题3 (Heading3)
        elif block_type == 5 and block.heading3 and block.heading3.elements:
            text_content = "".join([elem.text_run.content for elem in block.heading3.elements if elem.text_run])
            result.append(f"### {text_content}")
            
        # 处理代码块
        elif block_type == 11 and block.code:
            code_content = block.code.content or ""
            lang = block.code.language if hasattr(block.code, 'language') else ""
            result.append(f"```{lang}\n{code_content}\n```")
            
        # 处理引用
        elif block_type == 12 and block.quote:
            quote_content = "".join([
                elem.text_run.content 
                for elem in block.quote.elements 
                if elem.text_run
            ]) if block.quote.elements else ""
            result.append(f"> {quote_content}")
            
        # 处理有序列表
        elif block_type == 7:
            content = ""
            if hasattr(block, 'ordered') and block.ordered and block.ordered.elements:
                content = "".join([elem.text_run.content for elem in block.ordered.elements if elem.text_run])
            result.append(f"1. {content}")
            
        # 处理无序列表
        elif block_type == 6:
            content = ""
            if hasattr(block, 'bullet') and block.bullet and block.bullet.elements:
                content = "".join([elem.text_run.content for elem in block.bullet.elements if elem.text_run])
            result.append(f"- {content}")
            
        # 其他类型的 block 这里做了简化处理
    
    return "\n".join(result)


def feishu_doc_reader(doc_url: str) -> str:
    """
    读取指定飞书文档的内容，用于获取提示词模板和原始素材。
    
    支持两种链接格式：
    - 文档链接：https://*.feishu.cn/docx/xxxxxxxxxx
    - 知识库链接：https://*.feishu.cn/wiki/xxxxxxxxxx
    
    Args:
        doc_url (str): 飞书文档的完整URL链接
        
    Returns:
        str: 文档的纯文本或Markdown内容
    """
    import io
    import docx
    
    print(f"[Skill Execution] 正在读取飞书文档: {doc_url}")
    
    # 判断链接类型
    link_type = "wiki" if _is_wiki_url(doc_url) else "docx"
    print(f"[Skill] 检测到链接类型: {link_type}")
    
    try:
        # 1. 提取 document_id（自动处理 wiki → docx）
        result = _extract_document_id(doc_url)
        
        # result 可能是字符串（docx token）或元组 (obj_token, obj_type, title)
        if isinstance(result, tuple):
            document_id, doc_type, title = result
        else:
            document_id = result
            doc_type = 'docx'
            title = None
            
        print(f"[Skill] 最终文档 token: {document_id}, 类型: {doc_type}")
        
        # 2. 根据类型读取文档内容
        if doc_type == 'file':
            # 需要下载 docx 文件并解析
            access_token = _get_access_token()
            headers = {'Authorization': f'Bearer {access_token}'}
            resp = requests.get(
                f'https://open.feishu.cn/open-apis/drive/v1/files/{document_id}/download',
                headers=headers
            )
            
            if resp.status_code != 200:
                raise Exception(f"下载文件失败: HTTP {resp.status_code}")
            
            # 解析 docx 内容
            docx_file = docx.Document(io.BytesIO(resp.content))
            text_content = []
            for para in docx_file.paragraphs:
                if para.text.strip():
                    text_content.append(para.text)
            
            text_content = '\n'.join(text_content)
            print(f"[Skill] 成功读取文件文档，内容长度: {len(text_content)} 字符")
            return text_content
        else:
            # 使用 docx API 读取文档 block
            request: ListDocumentBlockRequest = ListDocumentBlockRequest.builder() \
                .document_id(document_id) \
                .page_size(500) \
                .build()
                
            # 3. 发起请求
            response: ListDocumentBlockResponse = client.docx.v1.document_block.list(request)
            
            # 4. 检查响应
            if not response.success():
                code = response.code
                msg = response.msg
                
                # 根据错误类型给出友好提示
                if code == 404 or "not found" in str(msg).lower():
                    error_hint = """
【权限提示】
读取文档失败 (404 Not Found)。

这通常是因为文档没有分享给机器人。请按以下步骤操作：
1. 在飞书网页/客户端中打开目标文档
2. 点击右上角「分享」按钮
3. 搜索并添加你的机器人账号（通常以 `cli_` 开头）
4. 授予「可查看」或「可编辑」权限
5. 重新执行指令
"""
                    print(f"[Error]{error_hint}")
                    return error_hint
                else:
                    error_msg = f"飞书API调用失败: Code: {code}, Msg: {msg}"
                    print(f"[Error] {error_msg}")
                    return f"读取失败：{error_msg}"
                
            # 5. 解析并返回文本
            blocks = response.data.items
            text_content = _parse_blocks_to_text(blocks)
            
            print(f"[Skill] 成功读取文档，内容长度: {len(text_content)} 字符")
            return text_content
        
    except ValueError as e:
        # 链接格式解析错误
        print(f"[Error] 链接格式错误: {str(e)}")
        return f"链接格式错误：{str(e)}"
    except Exception as e:
        error_str = str(e)
        print(f"[Error] 读取文档时发生异常: {error_str}")
        
        # 如果是权限相关的错误，给出友好提示
        if "404" in error_str or "permission" in error_str.lower():
            return """读取文档失败，可能是权限问题。

请确保：
1. 文档已分享给机器人账号
2. 机器人有足够的权限（至少「可查看」）

操作方法：在飞书文档中点击「分享」→ 添加机器人账号"""
        
        return f"读取文档时发生异常: {error_str}"


def feishu_doc_writer(title: str, content: str) -> str:
    """
    创建一个新的飞书文档并将生成的剪辑脚本内容写入，返回新文档链接。
    
    Args:
        title (str): 新文档的标题，例如：直播切片_第12期_脚本
        content (str): 大模型生成的剪辑脚本Markdown内容
        
    Returns:
        str: 新生成的飞书文档URL链接
    """
    print(f"[Skill Execution] 正在飞书创建新文档: {title}")
    
    try:
        # ==========================================
        # 1. 创建空的新文档
        # ==========================================
        create_req = CreateDocumentRequest.builder() \
            .request_body(CreateDocumentRequestBody.builder()
                          .title(title)
                          .folder_token(TARGET_FOLDER_TOKEN)
                          .build()) \
            .build()
            
        create_resp = client.docx.v1.document.create(create_req)
        if not create_resp.success():
            error_msg = f"创建文档失败: Code: {create_resp.code}, Msg: {create_resp.msg}"
            print(f"[Error] {error_msg}")
            return error_msg
            
        document_id = create_resp.data.document.document_id
        print(f"[Skill] 文档创建成功，document_id: {document_id}")
        
        # ==========================================
        # 2. 将内容写入文档
        # ==========================================
        # 构造插入文本的请求体
        block_elem = TextElement.builder() \
            .text_run(TextRun.builder().content(content).build()) \
            .build()
            
        block = Block.builder() \
            .block_type(2) \
            .text(Text.builder().elements([block_elem]).build()) \
            .build()
            
        insert_req = CreateDocumentBlockChildrenRequest.builder() \
            .document_id(document_id) \
            .block_id(document_id) \
            .request_body(CreateDocumentBlockChildrenRequestBody.builder()
                          .children([block])
                          .index(-1)
                          .build()) \
            .build()
            
        insert_resp = client.docx.v1.document_block_children.create(insert_req)
        if not insert_resp.success():
            error_msg = f"写入内容失败: Code: {insert_resp.code}, Msg: {insert_resp.msg}"
            print(f"[Error] {error_msg}")
            # 即使写入失败，也返回空文档的链接
            return f"内容写入失败 ({insert_resp.msg})。空文档链接：https://feishu.cn/docx/{document_id}"
            
        # ==========================================
        # 3. 拼接最终链接并返回
        # ==========================================
        final_url = f"https://feishu.cn/docx/{document_id}"
        print(f"[Skill Execution] 写入成功！新文档链接: {final_url}")
        
        return final_url
        
    except Exception as e:
        print(f"[Error] 写入文档时发生异常: {str(e)}")
        return f"写入文档时发生异常: {str(e)}"


# 注册为工具
__all__ = ["feishu_doc_reader", "feishu_doc_writer"]

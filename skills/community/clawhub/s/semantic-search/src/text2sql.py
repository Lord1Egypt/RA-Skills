import re
import pandas as pd
import asyncio
import httpx
import orjson
from typing import Dict, Any, Optional, List, TypedDict, Callable
from utils.logger import logger
from utils.config import CONFIG
from utils.tools import call_openai_sdk
from langgraph.graph import StateGraph, END, START
from src.semantic.retriever import VannaRetriever
from src.semantic._types import AgentState
from src.vector.vector_db import FlightDataBase


class Text2SQLAgent:
    """
    基于 LangGraph 的 Text-to-SQL 生成与执行 Agent。
    封装了图定义、节点逻辑和执行流。
    """
    
    def __init__(self, db_env, retriever: Optional[Callable[[str], str]] = None):
        """
        初始化 Agent。
        
        Args:
            db_env: 数据库环境/连接对象
            retriever: 可选的检索器函数, 这里后续是vanan, 对sql进行检索
        """
        self.db_env = db_env
        self.retriever = retriever
        self.app = self._build_graph()

    def _get_table_info_node(self, state: AgentState) -> Dict[str, Any]:
        """
        节点：获取表信息。
        提供 resource_id，从 API 获取表结构、表名并自动获取样本数据。
        
        Args:
            state (AgentState): 当前 Agent 状态
            
        Returns:
            Dict[str, Any]: 更新的状态字典，包含 table_info, table_name, table_data
        """
        resource_id = state.get("resource_id")
        if resource_id:
            META_DATA_API = "{svc}/data_latitude_longitude/v1/dataservice/metadata?resource_id={resource_id}"
            url = META_DATA_API.format(svc=CONFIG["longitude_address"], resource_id=resource_id)
            
            try:
                with httpx.Client(timeout=300) as client:
                    result = client.get(url)
                    if result.status_code != 200:
                        raise ConnectionError(f"{url} 获取资源失败, 错误码为: {result.status_code}")
                    
                    resp = orjson.loads(result.content)
                    table_info = resp["fields"]
                    table_name = resp["view_name"]
                    
                    # Fetch sample data
                    table_data = self._fetch_sample_data(table_name)
                    
                    return {
                        "table_info": table_info,
                        "table_name": table_name,
                        "table_data": table_data
                    }
            except Exception as e:
                logger.error(f"获取表信息失败: {e}")
                return {"error_message": f"获取表元数据失败: {str(e)}"}
                
        return {
            "table_info": None,
            "table_name": None,
            "table_data": None
        }

    def _extract_sql_from_llm(self, text: str) -> str:
        """
        从 LLM 响应中提取 SQL 代码块。
        
        Args:
            text (str): LLM 返回的完整文本
            
        Returns:
            str: 提取出的 SQL 语句
        """
        sql = text
        pattern = r"```sql(.*?)```"
        sql_code_snippets = re.findall(pattern, text, re.DOTALL)
        if len(sql_code_snippets) > 0:
            sql = sql_code_snippets[-1].strip()
        return sql
        
    def _is_valid_select_statement(self, sql: str) -> bool:
        """
        检查 SQL 是否为有效的 SELECT 语句且不包含修改数据的命令。
        
        Args:
            sql (str): 待检查的 SQL 语句
            
        Returns:
            bool: 如果是安全的 SELECT 语句则返回 True，否则返回 False
        """
        sql_upper = sql.upper().strip()
        
        # Must start with SELECT or WITH (Common Table Expressions)
        if not (sql_upper.startswith("SELECT") or sql_upper.startswith("WITH")):
            return False
            
        # Forbidden keywords that modify data or schema
        forbidden_keywords = [
            "INSERT INTO", "UPDATE", "DELETE FROM", "DROP TABLE", "DROP DATABASE", 
            "ALTER TABLE", "TRUNCATE TABLE", "CREATE TABLE", "CREATE DATABASE",
            "GRANT", "REVOKE", "COMMIT", "ROLLBACK"
        ]
        
        for keyword in forbidden_keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', sql_upper):
                return False
                
        return True

    def _retrieve_context(self, state: AgentState) -> Dict[str, Any]:
        """
        节点：使用检索器工具检索相关上下文。
        
        Args:
            state (AgentState): 当前 Agent 状态
            
        Returns:
            Dict[str, Any]: 更新的状态字典，包含 retrieved_context
        """
        if not self.retriever:
            return {"retrieved_context": None}
            
        query = state["query"]
        try:
            context = self.retriever(query)
            return {"retrieved_context": context}
        
        except Exception as e:
            logger.warning(f"检索失败: {e}")
            return {"retrieved_context": None}

    def _generate_sql(self, state: AgentState) -> Dict[str, Any]:
        """
        节点：根据状态生成 SQL 查询语句。
        
        Args:
            state (AgentState): 当前 Agent 状态
            
        Returns:
            Dict[str, Any]: 更新的状态字典，包含 sql_query 和 attempt_count
        """
        query = state["query"]
        table_info = state["table_info"]
        table_name = state["table_name"]
        table_data = state["table_data"]
        retrieved_context = state.get("retrieved_context")
        error_message = state.get("error_message")
        reflection_feedback = state.get("reflection")
        attempt = state["attempt_count"] + 1
        
        if not table_name or not table_info:
            return {
                "sql_query": "", 
                "attempt_count": attempt,
                "error_message": "缺少表信息或表名，无法生成SQL"
            }
        
        # Construct Prompt
        prompt = f"""
        You are a PostgreSQL data analysis expert. Please write a standard SQL query based on the following information to answer the user's question.

        【Table Structure】
        Table `public.{table_name}` fields and types:
        {table_info}

        【Sample Data】
        {table_data}
        """
        
        # Add Retrieved Context (RAG)
        if retrieved_context:
            prompt += f"""
            
            【Relevant Context / Similar Examples】
            The following information was retrieved to assist you:
            {retrieved_context}
            """

        prompt += f"""
        
        【User Question】
        {query}
        """

        # Add error context if retrying
        if error_message:
            prompt += f"""
            
            【Previous Execution Error】
            {error_message}
            
            The previous SQL query failed to execute. Please fix the SQL based on the error message above. 
            Ensure you check the table structure again and correct any field names or syntax errors.
            """

        if reflection_feedback:
            prompt += f"""
            
            【Reflection Feedback】
            Your previous SQL was reviewed and flagged with the following issues:
            {reflection_feedback}
            
            Please fix the SQL based on this feedback.
            """
            
        prompt += f"""
        
        ## Requirements:
        1. Wrap SQL in markdown: ```sql ... ```
        2. Use table name `public.{table_name}`.
        3. Do not invent fields. Use double quotes for Chinese field names or aliases.
        4. Ensure PostgreSQL compatibility.
        5. If the question involves "fuzzy", "contains", etc., use `LIKE '%keyword%'`.
        6. For aggregations (count, sum, avg), ensure you use the correct functions.
        7. **IMPORTANT**: Only `SELECT` statements are allowed. Do not use INSERT, UPDATE, DELETE, etc.
        8. Return ONLY the SQL.
        """
        
        messages = [
            {"role": "system", "content": "You are a PostgreSQL expert."},
            {"role": "user", "content": prompt}
        ]
        
        # Call LLM
        try:
            response = call_openai_sdk(messages)
            sql_query = self._extract_sql_from_llm(response)
            logger.info(f"SQL已生成: {sql_query}")
            return {
                "sql_query": sql_query,
                "attempt_count": attempt
            }
        except Exception as e:
            logger.error(f"LLM调用失败: {e}")
            return {
                "sql_query": "", 
                "attempt_count": attempt,
                "error_message": f"LLM生成失败: {str(e)}"
            }

    def _reflect_node(self, state: AgentState) -> Dict[str, Any]:
        """
        节点：反思生成的 SQL。
        检查 SQL 是否合法、是否符合表结构、是否回答了问题。
        
        Args:
            state (AgentState): 当前 Agent 状态
            
        Returns:
            Dict[str, Any]: 更新的状态字典，包含 reflection
        """
        sql = state["sql_query"]
        query = state["query"]
        table_info = state["table_info"]
        table_name = state["table_name"]
        
        if not sql:
            return {"reflection": "未生成 SQL"}
            
        prompt = f"""
        You are a SQL QA Expert. Please review the generated SQL query for the following user question and table schema.
        
        【User Question】
        {query}
        
        【Table Schema】
        Table: {table_name}
        Fields: {table_info}
        
        【Generated SQL】
        {sql}
        
        Please check for:
        1. Syntax errors (PostgreSQL).
        2. Schema validity (do all columns exist?).
        3. Logical correctness (does it answer the question?).
        4. Security (only SELECT allowed).
        
        If the SQL is correct and good, respond with exactly "CORRECT".
        If there are issues, describe them briefly and provide suggestions for fixing.
        """
        
        messages = [
            {"role": "system", "content": "You are a strict SQL reviewer."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = call_openai_sdk(messages)
            logger.info(f"SQL反思结果: {response}")
            
            if "CORRECT" in response.upper() and len(response) < 20:
                return {"reflection": None} # No issues
            else:
                return {"reflection": response}
                
        except Exception as e:
            logger.warning(f"反思环节失败: {e}")
            return {"reflection": None} # Assume ok if check fails

    def _execute_sql_node(self, state: AgentState) -> Dict[str, Any]:
        """
        节点：执行生成的 SQL 查询。
        
        Args:
            state (AgentState): 当前 Agent 状态
            
        Returns:
            Dict[str, Any]: 更新的状态字典，包含 execution_result 和 error_message
        """
        sql = state["sql_query"]
        if not sql:
            return {"execution_result": None, "error_message": "生成的SQL查询为空"}
            
        if not self._is_valid_select_statement(sql):
            error_msg = "安全警告: 仅允许SELECT查询, 检测到潜在DML/DDL命令"
            logger.warning(f"{error_msg} SQL: {sql}")
            return {
                "execution_result": None, 
                "error_message": error_msg,
                "sql_query": sql
            }
            
        logger.info(f"执行SQL: {sql}")
        
        try:
            status, result = self.db_env._sync_query_gen_sql(sql)
            
            if status:
                if isinstance(result, pd.DataFrame):
                    result = result.where(pd.notnull(result), None)
                
                # Success: Try to save to semantic memory (if available)
                if self.retriever and hasattr(self.retriever, "add_example"):
                    # Only save if we have a valid query and it's not a retry from error
                    # (optional: you might want to verify result is not empty before saving)
                    # For now, we log it.
                    try:
                        self.retriever.add_example(state["query"], sql)
                        logger.info("成功将SQL示例保存到语义记忆中")
                    except Exception as mem_err:
                        logger.warning(f"保存语义记忆失败: {mem_err}")

                return {
                    "execution_result": result, 
                    "sql_query": sql,
                    "error_message": None
                }
            else:
                error_msg = str(result)
                logger.warning(f"SQL执行失败: {error_msg}")
                return {
                    "execution_result": None, 
                    "sql_query": sql,
                    "error_message": error_msg
                }
        except Exception as e:
            logger.error(f"执行异常: {e}")
            return {
                "execution_result": None, 
                "sql_query": sql,
                "error_message": str(e)
            }

    def _should_continue(self, state: AgentState) -> str:
        """
        条件边：决定下一步流程。
        如果无错误则结束，否则重试生成 SQL，直到达到最大尝试次数。
        
        Args:
            state (AgentState): 当前 Agent 状态
            
        Returns:
            str: 下一个节点的名称 (END 或 "generate_sql")
        """
        # If no error, we are done
        if not state.get("error_message"):
            return END
        
        # If max attempts reached, stop
        if state["attempt_count"] >= state["max_attempts"]:
            logger.warning(f"达到最大重试次数 ({state['max_attempts']}), 停止")
            return END
            
        return "generate_sql"

    def _check_reflection(self, state: AgentState) -> str:
        """
        条件边：检查反思结果。
        如果有反思意见且未达最大尝试次数，则重试生成；否则执行。
        """
        reflection = state.get("reflection")
        
        if reflection:
            # If we have criticism, check attempts
            if state["attempt_count"] < state["max_attempts"]:
                logger.info(f"收到反思意见，尝试重新生成 (尝试 {state['attempt_count']}/{state['max_attempts']})")
                return "generate_sql"
            else:
                logger.warning("收到反思意见但已达最大尝试次数，强制执行")
                return "execute_sql"
        
        return "execute_sql"

    def _build_graph(self):
        """
        构建并编译 LangGraph 状态图。
        
        Returns:
            CompiledGraph: 编译后的 LangGraph 应用
        """
        workflow = StateGraph(AgentState)
        
        # Add Nodes
        workflow.add_node("get_table_info", self._get_table_info_node)
        workflow.add_node("retrieve_context", self._retrieve_context)
        workflow.add_node("generate_sql", self._generate_sql)
        workflow.add_node("reflect_sql", self._reflect_node)
        workflow.add_node("execute_sql", self._execute_sql_node)
        
        # Add Edges
        # 1. Start -> Parallel Nodes
        workflow.add_edge(START, "get_table_info")
        workflow.add_edge(START, "retrieve_context")
        
        # 2. Parallel Nodes -> Join at generate_sql
        # Note: LangGraph waits for all incoming edges to complete before executing the node
        workflow.add_edge("get_table_info", "generate_sql")
        workflow.add_edge("retrieve_context", "generate_sql")
        
        # 3. Continue flow
        workflow.add_edge("generate_sql", "reflect_sql")
        
        # Add Conditional Edges
        # From reflection to generate (retry) or execute
        workflow.add_conditional_edges(
            "reflect_sql",
            self._check_reflection,
            {
                "generate_sql": "generate_sql",
                "execute_sql": "execute_sql"
            }
        )
        
        # From execution to generate (retry on error) or end
        workflow.add_conditional_edges(
            "execute_sql",
            self._should_continue,
            {
                END: END,
                "generate_sql": "generate_sql"
            }
        )
        
        return workflow.compile(name="text2sql_agent")

    def _fetch_sample_data(self, table_name: str) -> List[Dict]:
        """
        辅助函数：获取安全的样本数据（排除空间列）。
        
        Args:
            table_name (str): 表名
            
        Returns:
            List[Dict]: 样本数据列表
        """
        table_data = []
        try:
            if hasattr(self.db_env, "_sync_query"):
                raw_data = self.db_env._sync_query(f"select * from public.{table_name} limit 1")
            else:
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                raw_data = loop.run_until_complete(self.db_env.query(f"select * from public.{table_name} limit 1"))
            
            if raw_data and isinstance(raw_data, list) and len(raw_data) > 0:
                sample_record = raw_data[0]
                spatial_keys = [key for key in sample_record.keys() if 
                               key.lower() in ['geom', 'geometry', 'shape', 'wkt', 'wkb'] or 
                               'geom' in key.lower() or 'shape' in key.lower()]
                if spatial_keys:
                    table_data = [{k: v for k, v in record.items() if k not in spatial_keys} 
                                 for record in raw_data]
                else:
                    table_data = raw_data
        except Exception as e:
            logger.warning(f"获取样本数据失败: {e}")
            table_data = []
            
        return table_data

    def run(self, query: str, resource_id: Optional[int] = None, max_attempts=3) -> tuple[Any, str]:
        """
        运行 Agent 工作流。
        
        Args:
            query (str): 用户的查询语句
            resource_id (Optional[int]): 资源ID，用于自动获取表信息
            max_attempts (int): 最大重试次数，默认为3
            
        Returns:
            tuple: (execution_result, sql_query) 包含执行结果和生成的 SQL 语句
        """

        initial_state: AgentState = {
            "query": query,
            "resource_id": resource_id,
            "table_info": None,
            "table_name": None,
            "table_data": None, 
            "retrieved_context": None,
            "sql_query": None,
            "execution_result": None,
            "error_message": None,
            "reflection": None,
            "attempt_count": 0,
            "max_attempts": max_attempts
        }
        
        final_state = self.app.invoke(initial_state)
        
        result = final_state.get("execution_result")
        if result is None:
            result = pd.DataFrame()
            
        sql_query = final_state.get("sql_query", "")
        
        return result, sql_query


def sql_gen_and_execute(db_env,  query: str, resource_id: Optional[int] = None, max_attempts=5):
    """
    Args:
        db_env: 数据库环境
        query: 查询语句
        max_attempts: 最大尝试次数
        
    Returns:
        tuple: (result, sql)
    """
    # retriever = VannaRetriever(client=db_env)  # TODO
    
    agent = Text2SQLAgent(db_env)
    return agent.run(query=query, resource_id=resource_id, max_attempts=max_attempts)


# ==================== DataGen 类（向后兼容） ====================

class DataGen:
    """
    数据生成模块（向后兼容包装类）

    注意：此类已整合到 Text2SQLAgent 中
    建议直接使用 Text2SQLAgent
    """

    def __init__(self):
        """初始化并创建 Text2SQLAgent 实例"""
        self.client = FlightDataBase()
        self.agent = Text2SQLAgent(self.client)

    async def query2sql(
        self,
        query: str,
        resource_id: int,
        max_attempts: int = 5,
        **kwargs
    ):
        """
        Text-to-SQL 生成与执行

        Args:
            query: 用户的自然语言查询
            resource_id: 资源ID
            max_attempts: 最大尝试次数（默认5）
            **kwargs: 其他参数

        Returns:
            tuple: (result, sql) 查询结果和生成的SQL语句
        """
        result, sql = await asyncio.to_thread(
            self.agent.run,
            query=query,
            resource_id=resource_id,
            max_attempts=max_attempts
        )
        return result, sql
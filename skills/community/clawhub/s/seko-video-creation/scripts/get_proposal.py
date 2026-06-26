import http.client
import json
import argparse
import os
import sys
import time
import urllib.request
import urllib.parse

def get_config():
    """
    加载配置文件
    """
    config_path = os.path.join(os.path.dirname(__file__), "../assets/config.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Failed to load config from {config_path}: {e}")
        return {}

def check_task_status(task_id: str, api_key: str) -> dict:
    """
    查询任务状态
    """
    # Load config
    config = get_config()
    api_base_url = config.get("api_base_url")
    if not api_base_url:
        print("Error: api_base_url not found in assets/config.json", file=sys.stderr)
        sys.exit(1)

    conn = http.client.HTTPSConnection(api_base_url)
    headers = {
        'Seko-API-Key': api_key,
        'Accept': '*/*',
    }
    try:
        endpoint = f"/seko-api/openapi/v1/plan-tasks/{task_id}/status"
        conn.request("GET", endpoint, "", headers)
        res = conn.getresponse()
        data = res.read()
        return json.loads(data.decode("utf-8"))
    except Exception as e:
        return {"code": 500, "msg": str(e)}
    finally:
        conn.close()

def wait_for_completion(task_id: str, api_key: str, interval: int = 10) -> dict:
    """
    轮询等待任务完成
    """
    print(f"等待任务完成，taskId: {task_id}，每 {interval} 秒轮询一次...")
    
    while True:
        result = check_task_status(task_id, api_key)
        
        if result.get("code") != 200:
            print(f"查询失败: {result.get('msg')}")
            return result
        
        data = result.get("data", {})
        status = data.get("taskStatus", "RUNNING")
        
        print(f"当前状态: {status}")
        
        if status == "RUNNING":
            time.sleep(interval)
        else:
            if status == "OK":
                print("任务成功完成！")
            elif status == "FAIL":
                print(f"任务失败: {data.get('taskStatusMsg', '未知原因')}")
            return result

def download_elements_images(data: dict, download_dir: str):
    """
    自动下载返回 JSON 中的所有 elements 图片
    """
    # 修正路径：根据 data["result"]["elements"] 获取
    result_obj = data.get("result", {})
    elements = result_obj.get("elements", [])
    if not elements:
        print("未发现可下载的 elements 图片。")
        return

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        print(f"创建下载目录: {download_dir}")
        
    for element in elements:
        url = element.get("elementUrl")
        name = element.get("elementName")
        if url and name:
            # 解析 URL 提取文件扩展名
            parsed_url = urllib.parse.urlparse(url)
            # 处理可能的查询参数干扰
            path = parsed_url.path
            ext = os.path.splitext(path)[1]
            if not ext:
                ext = ".jpeg"
            
            # 清理文件名中不合法字符
            safe_name = "".join([c for c in name if c.isalnum() or c in (' ', '-', '_')]).strip()
            filename = f"{safe_name}{ext}"
            filepath = os.path.join(download_dir, filename)
            
            print(f"正在下载: {name} -> {filepath} ...")
            try:
                # 增加 User-Agent 避免被拦截
                req = urllib.request.Request(
                    url, 
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
                )
                with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
                    out_file.write(response.read())
                print(f"下载成功: {filepath}")
            except Exception as e:
                print(f"下载失败 {name}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Get the status of a proposal task.')
    parser.add_argument('--taskid', type=str, required=True, help='The ID of the task to check')
    parser.add_argument('--seko_api_key', type=str, help='The Seko API key (optional)')
    parser.add_argument("--interval", type=int, default=10, help="轮询间隔秒数 (默认: 10)")
    parser.add_argument("--wait", action="store_true", help="提交任务后等待完成")
    parser.add_argument("--download", type=str, default="./assets", help="策划案完成后自动下载图片路径 (默认: ./assets)")
    parser.add_argument("--output", type=str, default="$taskid_result.json", help="结果输出文件名 (默认: $taskid_result.json)")

    args = parser.parse_args()

    # Determine API key
    api_key = args.seko_api_key
    if not api_key:
        api_key = os.environ.get('SEKO_API_KEY')
    
    if not api_key:
        print("Error: Seko-API-Key not found. Please provide it via --seko_api_key or as an environment variable.", file=sys.stderr)
        sys.exit(1)

    # 查询任务状态
    if args.wait:
        result = wait_for_completion(args.taskid, api_key, args.interval)
    else:
        result = check_task_status(args.taskid, api_key)

    # 打印最终结果（保持向后兼容，如果是非 wait 模式且未完成）
    print(json.dumps(result, indent=4, ensure_ascii=False))

    # 保存结果到文件
    output_filename = args.output.replace("$taskid", args.taskid)
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=4, ensure_ascii=False)
        print(f"结果已保存至: {output_filename}")
    except Exception as e:
        print(f"保存结果文件失败: {e}")

    # 自动下载图片 (仅在任务成功完成且指定了下载路径时)
    if result.get("code") == 200:
        data = result.get("data", {})
        status = data.get("taskStatus")
        if status == "OK":
            download_elements_images(data, args.download)

if __name__ == "__main__":
    main()

import asyncio
import websockets
import subprocess
import logging
import os
import signal
import sys
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('MCP_PIPE')

async def pipe_websocket_to_process(websocket, process):
    while True:
        msg = await websocket.recv()
        if isinstance(msg, bytes):
            msg = msg.decode('utf-8', errors='replace')
        process.stdin.write(msg + '\n')
        process.stdin.flush()

async def pipe_process_to_websocket(process, websocket):
    loop = asyncio.get_event_loop()
    while True:
        line = await loop.run_in_executor(None, process.stdout.readline)
        if not line:
            break
        await websocket.send(line)

async def pipe_stderr(process):
    loop = asyncio.get_event_loop()
    while True:
        line = await loop.run_in_executor(None, process.stderr.readline)
        if not line:
            break
        sys.stderr.write(line)
        sys.stderr.flush()

async def main():
    if len(sys.argv) < 2:
        print('Usage: python3 mcp_pipe.py <mcp_script>')
        raise SystemExit(1)

    uri = os.environ.get('MCP_ENDPOINT')
    if not uri:
        print('Missing MCP_ENDPOINT')
        raise SystemExit(1)

    script_path = sys.argv[1]
    async with websockets.connect(uri) as websocket:
        process = subprocess.Popen(
            ['python3', script_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8',
            errors='replace'
        )
        try:
            await asyncio.gather(
                pipe_websocket_to_process(websocket, process),
                pipe_process_to_websocket(process, websocket),
                pipe_stderr(process)
            )
        finally:
            process.terminate()
            try:
                process.wait(timeout=3)
            except Exception:
                process.kill()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
    asyncio.run(main())

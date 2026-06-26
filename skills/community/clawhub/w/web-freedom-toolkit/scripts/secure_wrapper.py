import socket
import threading
import os
import sys
import random
import time
from sota_core import run_protected_script

def secure_server():
    """
    v6.2.0 Secure Wrapper: Ephemeral Unix Socket Server.
    """
    print("--- [SOTA FORTRESS GATE v6.2] ---")
    socket_path = "/tmp/.sota_auth.sock"
    
    # Clean up stale sockets
    if os.path.exists(socket_path): os.remove(socket_path)
    
    # 1. Human Challenge
    secret = str(random.randint(1000, 9999))
    print(f"\n[MANDATORY AUTH] Challenge: {secret}")
    
    try:
        user_input = input(">> ").strip()
        if user_input != secret:
            print("Auth Failed.")
            return

        # 2. Start Memory-only Auth Socket
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
            server.bind(socket_path)
            os.chmod(socket_path, 0o600)
            server.listen(1)
            server.settimeout(10)
            
            print("✅ Memory Channel Open. Launching Task...")
            
            # Start the task in a thread or separate process
            script_name = sys.argv[1] if len(sys.argv) > 1 else None
            if not script_name: return
            
            # Sub-process will connect to this socket
            def handle_auth():
                try:
                    conn, _ = server.accept()
                    data = conn.recv(1024)
                    if data == b"AUTH_REQUEST":
                        conn.sendall(b"AUTH_GRANTED")
                    conn.close()
                except: pass

            threading.Thread(target=handle_auth).start()
            
            # 3. Secure Launch
            run_protected_script(script_name)
            
    except Exception as e:
        print(f"Gate Error: {e}")
    finally:
        if os.path.exists(socket_path): os.remove(socket_path)

if __name__ == "__main__":
    secure_server()

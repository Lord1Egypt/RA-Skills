import json
import tkinter as tk
from tkinter import messagebox, simpledialog


def collect_and_save_credentials(output_file: str = "user_credentials.json") -> bool:
    """弹窗依次收集公钥、私钥、API key，并保存到 JSON 文件。

    Args:
        output_file: 保存用户输入信息的文件路径。

    Returns:
        bool: 保存成功返回 True；用户取消或保存失败返回 False。
    """
    root = tk.Tk()
    root.withdraw()

    try:
        public_key = simpledialog.askstring("输入公钥", "请输入公钥：", parent=root)
        if public_key is None:
            messagebox.showwarning("已取消", "你已取消输入，未保存任何内容。", parent=root)
            return False

        private_key = simpledialog.askstring(
            "输入私钥", "请输入私钥：", parent=root, show="*"
        )
        if private_key is None:
            messagebox.showwarning("已取消", "你已取消输入，未保存任何内容。", parent=root)
            return False

        api_key = simpledialog.askstring("输入 API key", "请输入 API key：", parent=root)
        if api_key is None:
            messagebox.showwarning("已取消", "你已取消输入，未保存任何内容。", parent=root)
            return False

        payload = {
            "public_key": public_key,
            "private_key": private_key,
            "api_key": api_key,
        }

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(payload, file, ensure_ascii=False, indent=2)

        messagebox.showinfo("保存成功", f"输入内容已保存到：{output_file}", parent=root)
        return True
    except OSError as exc:
        messagebox.showerror("保存失败", f"写入文件失败：{exc}", parent=root)
        return False
    finally:
        root.destroy()


if __name__ == "__main__":
    # 执行案例：运行当前文件后弹出输入框，并将结果保存到当前目录。
    save_ok = collect_and_save_credentials("demo_credentials.json")
    if save_ok:
        print("执行成功：已保存到 demo_credentials.json")
    else:
        print("执行结束：用户取消或保存失败。")


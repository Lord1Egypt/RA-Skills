import subprocess
import sys

def install():
    print("==================================================")
    print("🛠️  正在为 Trump Tracker 安装 Python 依赖...")
    print("🛠️  Installing dependencies for Trump Tracker...")
    print("==================================================")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        # TextBlob 需要额外的语料库
        print("\n[*] 正在下载 TextBlob 语言包 (Downloading corpora)...")
        subprocess.check_call([sys.executable, "-m", "textblob.download_corpora"])
        
        print("\n✅ 所有依赖已安装完成！ (All dependencies installed successfully!)")
        print("💡 现在你可以运行: python scripts/trump_predictor.py")
    except Exception as e:
        print(f"\n❌ 安装失败 (Installation failed): {e}")

if __name__ == "__main__":
    install()

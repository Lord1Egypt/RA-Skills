"""One-click daily workflow: train -> predict -> evaluate -> web."""
import sys


def main():
    step = sys.argv[1] if len(sys.argv) > 1 else "all"

    if step in ("all", "train"):
        from train import run_training
        run_training()

    if step in ("all", "predict"):
        from predict import run_prediction
        run_prediction()

    if step in ("all", "evaluate"):
        from evaluate import run_evaluation
        run_evaluation()

    if step in ("all", "web"):
        from app import app
        print("Starting web server at http://127.0.0.1:5000")
        app.run(host="127.0.0.1", port=5000, debug=False)


if __name__ == "__main__":
    main()

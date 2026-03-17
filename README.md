python3 -m venv venv

Linux:
source venv/bin/activate

pip install requirements.txt
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch
uvicorn main:app --reload
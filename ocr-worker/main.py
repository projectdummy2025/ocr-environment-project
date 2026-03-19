import os
import shutil
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from paddleocr import PaddleOCR

app = FastAPI(title="OCR Worker CPU Only")

# INISIALISASI CPU ONLY
# use_gpu=False wajib ada agar tidak mencari driver NVIDIA
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Folder untuk simpan gambar agar sinkron dengan laptop
UPLOAD_DIR = "data"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.get("/")
def health():
    return {"status": "online", "mode": "CPU Only"}

@app.post("/process")
def process_ocr(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Hanya menerima file gambar.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        # Simpan file ke volume
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Eksekusi OCR
        result = ocr.ocr(file_path, cls=True)
        
        # Ambil teks mentah (Raw Text)
        raw_lines = []
        if result and result[0]:
            for line in result[0]:
                raw_lines.append(line[1][0])
        
        return {
            "status": "success",
            "filename": file.filename,
            "raw_text": " ".join(raw_lines)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
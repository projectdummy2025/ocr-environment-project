# OCR Worker API Reference

## 1. Health Check
*   **Path:** `/`
*   **Method:** `GET`
*   **Description:** Use to check if the OCR container is running and ready.

**Example Request (cURL):**
```bash
curl -X GET http://localhost:8000/
```

**Example Response:**
```json
{
  "status": "online",
  "mode": "CPU Only"
}
```

## 2. Process Image (OCR)
*   **Path:** `/process`
*   **Method:** `POST`
*   **Content-Type:** `multipart/form-data`
*   **Description:** Upload an image file for optical character recognition.

**Example Request (cURL):**
```bash
curl -X POST -F "file=@/path/to/your/image.jpg" http://localhost:8000/process
```

**Example Response (Success):**
```json
{
  "status": "success",
  "filename": "image.jpg",
  "raw_text": "Toko ABC Jl. Maju Mundur No 1 ... Total 50.000 ..."
}
```

**Example Response (Error - Wrong format):**
```json
{
  "detail": "Hanya menerima file gambar."
}
```

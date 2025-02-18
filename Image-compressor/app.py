from flask import Flask, render_template, request, send_file
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded", 400
        
        file = request.files["file"]
        if file.filename == "":
            return "No file selected", 400

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        compressed_path = os.path.join(UPLOAD_FOLDER, "compressed_" + file.filename)

        file.save(file_path)

        # Compress and optimize the image
        compress_image(file_path, compressed_path, quality=60, max_size=(1024, 1024))

        return render_template("index.html", original=file.filename, compressed="compressed_" + file.filename)

    return render_template("index.html")

def compress_image(input_path, output_path, quality=60, max_size=(1024, 1024)):
    """Compress and optimize an image."""
    try:
        with Image.open(input_path) as img:
            img = img.convert("RGB")  # Convert to RGB (removes transparency)
            img.thumbnail(max_size)  # Resize while maintaining aspect ratio
            img.save(output_path, "JPEG", quality=quality, optimize=True)
    except Exception as e:
        print("Error:", e)

@app.route("/download/<filename>")
def download_image(filename):
    """Download the compressed image."""
    path = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(path, as_attachment=True)

# Render Deployment Compatibility
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

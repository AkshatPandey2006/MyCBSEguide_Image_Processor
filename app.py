from flask import Flask, request, render_template, send_from_directory, jsonify
import cv2
import numpy as np
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

# Create folders if they do not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    file = request.files['file']
    if file:
        # Save uploaded image
        image_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(image_path)

        # Process image (Grayscale + Sharpening + Watermark Removal)
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply sharpening
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        sharpened = cv2.filter2D(gray, -1, kernel)

        # Detect watermark using thresholding (for both lighter and darker watermarks)
        light_thresh = cv2.threshold(sharpened, 200, 255, cv2.THRESH_BINARY)[1]
        dark_thresh = cv2.threshold(sharpened, 50, 255, cv2.THRESH_BINARY_INV)[1]

        # Combine both masks
        watermark_mask = cv2.bitwise_or(light_thresh, dark_thresh)

        # Perform inpainting to remove the watermark
        inpainted_image = cv2.inpaint(image, watermark_mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

        # Save the processed image
        processed_image_path = os.path.join(PROCESSED_FOLDER, 'processed_' + file.filename)
        cv2.imwrite(processed_image_path, inpainted_image)

        # Return the processed image's path
        return jsonify({"processed_image_url": f"/processed/{'processed_' + file.filename}"})

@app.route('/processed/<filename>')
def processed_image(filename):
    return send_from_directory(PROCESSED_FOLDER, filename)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

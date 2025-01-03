from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from PIL import Image
import io
import base64

app = Flask(__name__)
CORS(app)

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        file = request.files['image']
        if not file:
            return jsonify({'error': 'No image uploaded'}), 400

        img = Image.open(file)
        img_array = np.array(img)

        # Image Processing Options (add more as needed)
        processing_type = request.form.get('processing_type', 'grayscale') 

        if processing_type == 'grayscale':
            gray_img_array = np.mean(img_array, axis=2).astype(np.uint8)
            gray_img = Image.fromarray(gray_img_array)
        elif processing_type == 'invert':
            gray_img_array = 255 - img_array
            gray_img = Image.fromarray(gray_img_array)
        elif processing_type == 'blur':
            from PIL import ImageFilter
            gray_img = img.filter(ImageFilter.GaussianBlur(radius=2)) 
        else:
            return jsonify({'error': 'Invalid processing type'}), 400

        img_io = io.BytesIO()
        gray_img.save(img_io, 'JPEG')
        img_io.seek(0)
        base64_image = base64.b64encode(img_io.read()).decode('utf-8')

        return jsonify({'message': 'Image processed successfully', 'image': base64_image})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
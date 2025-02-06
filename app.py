from flask import Flask, render_template, request, send_from_directory, jsonify
from rembg import remove
import os

app = Flask(__name__)

# Configuración de la carpeta de carga
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite de 16MB para carga de archivos

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/removebg', methods=['GET'])
def removebg():
    return render_template('removeBg.html')

@app.route('/removebg', methods=['POST'])
def remove_background():
    try:
        # Obtener el archivo subido
        file = request.files.get('file')
        print(file)
        if file:
            # Verificar que el archivo sea una imagen
            if file.filename.lower().endswith(('.png', '.jpg', '.jpeg','.webp')):
                img_data = file.read()
                output_data = remove(img_data)

                # Guardar la imagen procesada
                filename = 'processed_image.png'
                result_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                with open(result_path, 'wb') as f:
                    f.write(output_data)

                # Crear la URL para acceder a la imagen procesada
                image_url = f'/uploads/{filename}'
                
                # Enviar la URL como parte de la respuesta en formato JSON
                return jsonify({'image_url': image_url})

            else:
                return "Por favor, sube una imagen válida (PNG, JPG, JPEG).", 400
        else:
            return "No se subió ninguna imagen.", 400
    
    except Exception as e:
        print(f"Error al procesar la imagen: {e}")  # Imprime el error completo para depuración
        return "Ha ocurrido un error en el servidor.", 500

# Ruta para servir la imagen desde la carpeta uploads
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

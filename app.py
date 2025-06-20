from flask import Flask, request, render_template
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import pickle

app = Flask(__name__)

# Carregue seu modelo pickle
with open('templates/meu_modelo_gato_cachorro.pkl', 'rb') as f:
    model = pickle.load(f)

def prepare_image(img_path):
    img = image.load_img(img_path, target_size=(150, 150))  # ajuste o tamanho se necessário
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        filepath = os.path.join("uploads", file.filename)
        file.save(filepath)

        img_array = prepare_image(filepath)
        prediction = model.predict(img_array)[0][0]

        result = "Gato" if prediction < 0.5 else "Cachorro"
        return render_template("index.html", prediction=result)
    
    return render_template("index.html", prediction=None)

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)

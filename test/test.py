from flask import Flask ,jsonify
from model.Data_agro import Patologia

app = Flask(__name__)

@app.route("/")
def hello():
    #,nome,nome_cientifico,classificador,descricao,acuracia,gravidade
    pat = Patologia(
            "Olho de rã",
            "Cercospora Sojina",
            "Tipo fungi ",
            "Lorem ipusm dolor ament",
            0.805,5)
        
    return jsonify(pat)

if __name__ == '__main__':
    app.run(debug=True)

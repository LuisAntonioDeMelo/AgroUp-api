#Desenvolvido por Luis Antônio de Melo
#License MIT - 
##L - 

from model.Data_agro import Patologia
import json

try:
    from flask import Flask,request,jsonify,redirect, url_for
    from flask_restful import Resource, Api
    
    from flask_restful import reqparse 
    
    from flask_limiter.util import get_remote_address
    from flask_limiter import Limiter
    
    from flasgger import Swagger 
    from flasgger.utils import swag_from 
    from flask_restful_swagger import swagger
    from flask_cors import CORS
    
    #importar A.I bibliotecas
    from keras.applications import ResNet50
    from keras.preprocessing.image import img_to_array
    from keras.applications import imagenet_utils
    from PIL import Image
    import numpy as np
    import flask
    import io
except Exception as e:    
    print("Some modules are misssings {}".format(e))

# api
app = Flask(__name__)
CORS(app)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)

limiter = Limiter(app,key_func=get_remote_address)
limiter.init_app(app)

 
#Criar metodos para tratamento de imagens 
def carregar_modelo():
    #Carregar um modelo treinado 
    global model
    model = ResNet50(weights="imagenet")
    
 
def preparar_imagens(imagem,valor):
    #verficiar imagens que não estão em rgb e converter
    if imagem.mode != "RGB":
        imagem = imagem.convert("RGB")
    #converter o tamanho da imagem e processala
    imagem = imagem.resize(valor)
    imagem = img_to_array(imagem)
    imagem = np.expand_dims(imagem,axis=0)
    imagem = imagenet_utils.preprocess_input(imagem) 

    return imagem


#Rotas api
@app.route("/previsao",methods=["POST"])
def predict_data():
    data = {"success":False}
    if flask.request.method == 'POST':
        if flask.request.files.get("imagem"):
            imagem = flask.request.files['imagem'].read()
            imagem = Image.open(io.BytesIO(imagem))

            imagem = preparar_imagens(imagem,valor=(224,224))
            
            #classificar
            pred = model.predict(imagem) 
            resultado = imagenet_utils.decode_predictions(pred)  
            data["predictions"] = []

            for(img_id,label,prob) in resultado[0]:
                retorno = {"label":label,"probalidade":float(prob)}
                data["predictions"].append(retorno)
            
            data["success"]= True

    return flask.jsonify(data)

@app.route("/agro/1",methods=['GET'])
def retornaDados():
    #,nome,nome_cientifico,classificador,descricao,acuracia,gravidade
    pat = Patologia(
            "Olho de rã",
            "Cercospora Sojina",
            "Tipo fungi ",
            "Lorem ipusm dolor ament",
            0.8055
            ,5)
    
    return json.dumps(pat.__dict__)
pass


#teste rota
@app.route("/login",methods=['POST','GET'])
def respostas():
    if request.method =='POST':
        user = request.form['user']
        return redirect(url_for('/agro/1',name=user))
    else:
        user = request.args.get('user')
    return redirect(url_for('/agro/1',name = user))

#swagger
api = swagger.docs(Api(app), apiVersion='0.1',  api_spec_url='/swagger')
class myApi(Resource):
    decorators = [limiter.limit("100/day")]
    @swagger.model
    @swagger.operation(notes='teste - swagger')
    def get(self,zip):
        return {
            "Response": 200,
            'Data':zip
        } 
    pass 
api.add_resource(myApi,'/zip/<string:zip>')


if __name__== '__main__':
    print(("**Recursos sendo inicialidados .... \n")
          +"devBY: Luis Antônio--letthegreedtotheothers")
    app.run(debug=True)
    
    
    



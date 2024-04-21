import os
import sys
import csv
import json

sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

from flask import Flask, request, jsonify
from body_controller import BodyController
from body_model import BodyModel

app = Flask(__name__)
bc = BodyController()

class Asteroid:

    @app.route('/add_body', methods=['POST'])
    def add_body():
        data = request.json
        new_body = BodyModel(data.get('bodyId'), data.get('englishName'), data.get('isPlanet'), data.get('gravity'), data.get('discoveredBy'), data.get('discoveryDate'), data.get('density'), data.get('bodyType'))

        bc.insert_body(new_body)

        body_dict = new_body.to_dict()

        return jsonify({'message': body_dict})

    @app.route('/get_body', methods=['GET'])
    def get_body():
        bodyId = request.args.get('id')

        body_finded = bc.get_body(int(bodyId))

        if body_finded is None:
            body_dict = None
        else:
            body_dict = body_finded.to_dict()

        return jsonify({'message': body_dict})

    @app.route('/cargar', methods=['GET'])
    def cargar():
        ruta = os.path.join(os.getcwd(), 'db', 'bodies.csv')

        with open(ruta, 'r', newline='') as csvfile:
            lector_csv = csv.DictReader(csvfile)
            for fila in lector_csv:
                bc.insert_body(BodyModel(
                    int(fila['bodyId']),
                    fila['englishName'],
                    fila['isPlanet'],
                    fila['gravity'],
                    fila['discoveredBy'],
                    fila['discoveryDate'],
                    fila['density'],
                    fila['bodyType'])
                )
        return jsonify({'message': 'La base de datos se ha llenado exitosamente'})

    @app.route('/generar_imagen', methods=['GET'])
    def generar_imagen():
        bc.generar_arbol_grafico()
        return jsonify({'message': 'Ya puede visualizar su imagen'})

    @app.route('/get_info_grupo', methods=['GET'])
    def get_info_grupo():
        return jsonify([
        {'Repositorio': 'https://github.com/Miguel-GH681/Programacion-III/tree/master/hoja_de_trabajo_4'},
        {
            'Nombre': 'Alvaro Miguel Gonzalez Hic',
            'Carnet': '9490-22-4805',
            'Contribuciones': [
                'Creacion de los metodos post y get',
                'Configuracion del proyecto en Render',
                'Creacion de los modelos de datos',
            ]
        },
        {
        'Nombre': 'Walter Daniel Palacios De Leon',
        'Carnet': '9490-21-2140',
        'Contribuciones': [
            'Creacion de la carga masiva',
            'Creacion del metodo de la informacion del grupo',
            'Creacion de la estructura de la aplicacion'
        ]
        }])

    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=3000)

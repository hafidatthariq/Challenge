import re
import pandas as pd
import sqlite3

from flask import Flask, jsonify
from flask import request
import flask
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

app = Flask(__name__)

app.json_encoder = LazyJSONEncoder
swagger_template = dict(
    info = {
        'title' : "API Documentation for Data Processing and Modeling",
        'version' : "1.0.0",
        'description' : "Dokumentasi API untuk Data Processing dan Modeling",
    },
    host = "127.0.0.1:5000/"
)

swagger_config = {
    "headers" : [],
    "specs" : [
        {
            "endpoint": "docs",
            "route" : "/docs.json",
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template, config = swagger_config)


def text_cleaning(text):
    cleaning=re.sub('USER', '' , text)
    cleaning=re.sub('USER.', '' , cleaning)
    cleaning=re.sub('RT', '' , cleaning)
    cleaning=cleaning.replace("\\n", " ")
    #cleaning=re.sub(' \w ', '' , cleaning)
    cleaning=cleaning.lower()
    cleaning=re.sub(r'[^a-zA-Z0-9]' ,' ',cleaning)
    return cleaning


@swag_from("yml/text_processing.yml", methods = ['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():
    
    text = request.form.get('text')
    
    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': re.sub(r'[^a-zA-Z0-9]', ' ', text),
    }

    response_data = jsonify(json_response)
    return response_data



@swag_from("yml/file_text_processing.yml", methods = ['POST'])
@app.route('/file-text-processing', methods=['POST']) 
def json():
    data = request.files['file']
    df = pd.read_csv (data, encoding="latin1")
    df['text after cleaning']=df.Tweet.apply(text_cleaning)
    
    conn = sqlite3.connect('D:\Binar\Challenge\data\challenge.db')
    df.to_sql('text_after_cleaning', conn, if_exists='replace', index=False)
    conn.close()

    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': print(df)
    }


    response_data = df.to_json()
    return response_data


if __name__ == '__main__':
    app.run() 



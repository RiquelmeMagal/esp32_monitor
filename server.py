from flask import Flask, render_template, jsonify
import requests
import time
import threading

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', umidade='', temperatura='')



@app.route('/data', methods=['GET'])
def get_data():
    try:
        # Substitua pelo IP correto do seu ESP32
        resposta = requests.get('http://192.168.31.209/') 
        if resposta.status_code == 200:
            dados = resposta.text
            dados_separados = dados.split("e")
            umidade = dados_separados[0][0:4]
            temperatura = dados_separados[1][0:4] 

            return jsonify({'umidade': umidade, 'temperatura': temperatura})
        else:
            return 'Erro na solicitação HTTP: ' + str(resposta.status_code), 500
    except Exception as e:
        return 'Erro na solicitação HTTP: ' + str(e), 500


def atualiza_dados():
    while True:
        time.sleep(2)
        atualizaDados()


def atualizaDados():
    try:
        # Substitua pelo IP correto do seu ESP32
        resposta = requests.get('http://192.168.31.209/')
        if resposta.status_code == 200:
            dados = resposta.text
            dados_separados = dados.split("e")
            umidade = dados_separados[0][0:4] + "%"
            temperatura = dados_separados[1][0:4] + " °C"

            # Atualize os valores na interface gráfica
            app.jinja_env.globals['umidade'] = umidade
            app.jinja_env.globals['temperatura'] = temperatura
        else:
            print("Erro na solicitação HTTP:", resposta.status_code)
    except Exception as e:
        print("Erro na solicitação HTTP:", str(e))


if __name__ == '__main__':
    threading.Thread(target=atualiza_dados).start()
    app.run(debug=True)

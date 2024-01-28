from PyQt5 import uic, QtWidgets
import requests
import time
import threading


def atualiza_dados():
    while True:
        try:
            # Substitua pelo IP correto do seu ESP32
            resposta = requests.get('SEU_IP')
            if resposta.status_code == 200:
                dados = resposta.text
                dados_separados = dados.split("e")
                umidade = dados_separados[0][0:4] + "%"
                temperatura = dados_separados[1][0:4] + " °C"

                # Atualize os valores na interface gráfica
                tela.label_6.setText(temperatura)
                tela.label_7.setText(umidade)
            else:
                print("Erro na solicitação HTTP:", resposta.status_code)
        except Exception as e:
            print("Erro na solicitação HTTP:", str(e))

        time.sleep(2)


app = QtWidgets.QApplication([])
tela = uic.loadUi("QT/tela_monitor.ui")
threading.Thread(target=atualiza_dados).start()
tela.show()
app.exec()

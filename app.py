from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
DATA_PATH = 'data/agendamentos.csv'


os.makedirs('data', exist_ok=True)


if not os.path.exists(DATA_PATH):
    pd.DataFrame(columns=['Nome', 'Data', 'Hora', 'Registrado_em']).to_csv(DATA_PATH, index=False)

@app.route('/')
def index():
    df = pd.read_csv(DATA_PATH)
    return render_template('index.html', agendamentos=df.to_dict(orient='records'))

@app.route('/agendar', methods=['POST'])
def agendar():
    nome = request.form['nome']
    data = request.form['data']
    hora = request.form['hora']
    registrado_em = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    novo = pd.DataFrame([[nome, data, hora, registrado_em]],
                        columns=['Nome', 'Data', 'Hora', 'Registrado_em'])

    df = pd.read_csv(DATA_PATH)
    df = pd.concat([df, novo], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)

    return ('', 204)

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('mensagem', '').lower()

    if 'horário' in user_msg or 'atendimento' in user_msg:
        resposta = "Atendemos das 8h às 18h, de segunda a sexta."
    elif 'confirmar' in user_msg or 'como agendar' in user_msg:
        resposta = "Basta preencher o formulário com nome, data e hora!"
    elif 'cancelar' in user_msg:
        resposta = "Por enquanto, cancelamentos devem ser feitos presencialmente."
    else:
        resposta = "Desculpe, não entendi. Pergunte sobre horários ou agendamento."

    return jsonify({'resposta': resposta})

if __name__ == '__main__':
    app.run(debug=True)

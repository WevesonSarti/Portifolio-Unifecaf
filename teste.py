from flask import Flask, render_template, request
import requests

teste = Flask(__name__)

API_KEY = "c69c1451212a6f61352f55df7d39ffce"

# Lista para armazenar histórico de consultas em memória
historico_cidades = []

def buscar_cidade(cidade):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"
    resp = requests.get(url)
    if resp.status_code != 200:
        return None, None
    dados = resp.json()
    temp = dados["main"]["temp"]
    umidade = dados["main"]["humidity"]
    return temp, umidade

@teste.route("/", methods=["GET", "POST"])
def inicial():
    erro = None
    temp = None
    umidade = None
    cidade = None

    if request.method == "POST":
        cidade = request.form.get("cidade")
        temp, umidade = buscar_cidade(cidade)
        if temp is not None:
            # Salvar na lista em memória
            historico_cidades.append({
                "cidade": cidade,
                "temp": temp,
                "umidade": umidade
            })
        else:
            erro = "Cidade não encontrada"

    return render_template("teste.html", temp=temp, umidade=umidade, cidade=cidade, erro=erro)

@teste.route("/historico")
def historico():
    # Passa a lista para o template
    return render_template("historico.html", dados=historico_cidades)

if __name__ == "__main__":
    teste.run(debug=True)

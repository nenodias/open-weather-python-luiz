# -*-  coding:utf-8 -*-
from pdb import set_trace
import requests as r
from flask import Flask, abort, request, render_template

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'

#@app.route('/')
def index():
    return 'lol'

app.add_url_rule('/', endpoint='hello', view_func=index)

@app.route('/<name>/')
def index(name):
    if name.lower() == 'luiz':
        return 'Olá {}'.format(name), 200
    return 'Not Found', 404

@app.route('/conversor/', methods=['GET', 'POST'])
def conversor():
    #request.args.get('real') # query string
    #request.form['real'] # form
    nome = request.form.get('nome','')
    contante_dolar = 0.31
    dolar = float(request.form.get('dolar', 0.0))
    real = dolar / 0.31
    contexto = {'nome':nome, 'dolar':dolar, 'real':real}
    return render_template('index.html', **contexto)

@app.route('/clima/', methods=['GET', 'POST'])
def clima():
    cidade = request.form.get(u'cidade')
    contexto = {}
    if cidade:
        api = '9e4a5a3c085cb78c102490f9c614bb6c'
        unidade = 'metric'
        lingua = 'pt'
        try:
            link = u'http://api.openweathermap.org/data/2.5/weather?q={cidade}&units={units}&APPID={api}&lang={lang}'
            url = link.format(api=api, cidade=cidade, units=unidade,lang=lingua)
            retorno = r.get(url)
            dados = retorno.json()
            clima = dados[u'weather'][0]
            contexto = {
                'principal' : dados[u'main'],
                'vento' : dados[u'wind'],
                'clima' : clima[u'description'],
                'cidade' : dados[u'name'],
                'nuvem' : dados[u'clouds'][u'all'],
                'icone': clima[u'icon']
            }
        except Exception as ex:
            print(ex)
    return render_template('clima.html', **contexto)

app.run(debug=True, use_reloader=True)
#!usr/bin/python3
#coding:utf-8
import redis, smtplib, random
from flask import Flask, request, jsonify, session


# connexion bdd redis
hostname = '172.20.0.2'
port = 6379
try :
    r = redis.StrictRedis(host=hostname, port=port, password='', decode_responses=True)
    print('Connexion réussie !')
except Exception as e:
    print(e)


# creation des routes avec flask et commande curl associée
"""
-X VERB : indique quel type de requête
-d "data" : envoi des données au service
-i : affiche le header
ex : curl -X POST -d "email=email&passwd=passwd"
"""

app = Flask(__name__)

# récuperation email et passwd
def recup():
    email = request.args.get('email')
    passwd = request.args.get('passwd')
    return email, passwd

# index
@app.route('/')
def index():
    recup()
    if 'email' in session:
        email = session['email']
        return 'Hello World'

# login
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET' or request.method == 'POST':
        session['email'] = request.args['email']
        return jsonify({'connection' : True})

# logout
@app.route('/logout')
def logout():
    recup()
    session.pop('email', None)
    return jsonify({'deconnection' : True})

# register
@app.route('/register', methods = ['GET', 'POST'])
def register():
    email, passwd = recup()
    r.set('email', email)
    r.set('passwd', passwd)
    return jsonify({'registering' : True})

# otp
@app.route('/otp', methods = ['GET', 'POST'])
def otp():
    email = recup()
    # création session smtp
    s = smtplib.smtp("smtp.gmail.com", 587)
    # demarrer TLS
    s.starttls()
    # se connecter au compte gmail
    s.login("lea.abedoi@gmail.com", "secret2016")
    otp = str(random.randint(1000, 9999))
    s.sendmail("lea.abedoi@gmail.com", email, otp)
    s.quit()
    return jsonify({'otp' : True})

if __name__ == '__main__':
    app.run(debug=True)

"""
question1 : pourquoi utiliser bcrypt ? ne pas stocker les mdp en clair, hashage + salage, peu etre ralentie en augmentant le nombre de pssage dans la focntion
resiste au attaque par brute force et par rainbow table
question2 : au bout de 3 essais, un nouveau est envoyé pourquoi ? pour eviter les bots et le brute force
"""
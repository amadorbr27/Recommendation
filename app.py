from flask import Flask, redirect, render_template, request, jsonify, url_for, session
from database import Database
from userService import UserService
from recommendation import GoogleScholarScraper


app = Flask(__name__)
app.secret_key = 'secret_key'
db = Database('database.db')
user_service = UserService()

# Rotas
@app.route('/', methods=['POST', 'GET'])
def login_page():
    if request.method == 'POST':
        user_data = {
            "username": request.form['username'],
            "password": request.form['password']
        }
        user = user_service.get_user_by_username(user_data['username'])
        if user:
            if user['password'] != user_data['password']:
                return jsonify({'message': 'Senha incorreta'}), 400
            else:
                session['user'] = user
                return redirect(url_for('search'))
        else:
            return jsonify({'message': 'Usuario nao existe'}), 400
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user_data = {
            "username": request.form['username'],
            "name": request.form['name'],
            "email": request.form['email'],
            "password": request.form['password'],
            "phone": request.form['phone'],
            "state": request.form['state'],
            "city": request.form['city'],
            "country": request.form['country'],
            "language": request.form['language'],
            "birthdate": request.form['birthdate'],
            "occupation": request.form['occupation'],
            "interest": request.form['interest']
        }

        # Verifique se o usuário ou e-mail já existem
        existing_user = user_service.get_user_by_username(user_data['username'])
        existing_email = user_service.get_user_by_email(user_data['email'])

        if existing_user or existing_email:
            return jsonify({'message': 'Usuario ou e-mail ja existe'}), 400

        # Insira o novo usuário no banco de dados
        user_service.create_user(user_data)
        
        #return jsonify({'message': 'Usuário registrado com sucesso'})
        return render_template('register.html', sucesso=True)
    return render_template('register.html')

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'GET':
        user = user_service.get_user(user_id)
        return render_template('edit_user.html', user=user)
    elif request.method == 'POST':
        # Obtenha os novos dados do usuário do formulário enviado
        updated_user_data = {
            "username": request.form['username'],
            "name": request.form['name'],
            "email": request.form['email'],
            "password": request.form['password'],
            "phone": request.form['phone'],
            "state": request.form['state'],
            "city": request.form['city'],
            "country": request.form['country'],
            "language": request.form['language'],
            "birthdate": request.form['birthdate'],
            "occupation": request.form['occupation'],
            "interest": request.form['interest']
            }
        
        # Atualize os dados do usuário no banco de dados
        user_service.update_user(user_id, updated_user_data)
        
        # Redirecione de volta para a página de usuários
        return redirect(url_for('show_users'))

@app.route('/users')
def show_users():
    user_service = UserService()
    users = user_service.get_all_users()
    return render_template('users.html', users=users)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    language = request.args.get('language')
    period_start = request.args.get('period_start')
    period_end = request.args.get('period_end')
    sort_by_date = request.args.get('sort_by_date')
    user = session.get('user')
    
    language = language if language else user['language']
    query = query if query else user['interest']
    scraper = GoogleScholarScraper(query=query, language=language, period_start=period_start, period_end=period_end, sort_by_date=sort_by_date)
    if query != user['interest']:
        user_service.record_search_history(user["id"], query, scraper.language, scraper.period_start, scraper.period_end)
    results = scraper.scrape_google_scholar()
    recommendation = get_recommendation()
    return render_template('search.html', user=user, results=results, recommendation=recommendation)

def get_recommendation():
    by_frequency = get_recommendation_by_frequency()
    return by_frequency

def get_recommendation_by_frequency():
    user = session.get('user')
    search_history = user_service.get_search_history(user["id"])
    by_frequency = []
    for history in search_history:
        scraper = GoogleScholarScraper(query=history[0], language=history[1], period_start=history[2], period_end=history[3])
        results = scraper.scrape_google_scholar()
        if results:
            by_frequency.append(results[0])      
    return by_frequency


if __name__ == '__main__':
    db.create_tables()
    app.run(debug=True, host='0.0.0.0', port=5000)
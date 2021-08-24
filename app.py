from flask import (
	Flask,
	g,
	redirect,
	render_template,
	request,
	session,
	url_for
)


class User:
	def __init__(self, id, username, password):
		self.id = id
		self.username = username
		self.password = password
	
	def __repr__(self):
		return f'<User: {self.username}>'
import envVar

users = []
users.append(User(id=1, username=envVar.USERNAME1, password=envVar.PASSWORD1))
users.append(User(id=2, username=envVar.USERNAME2, password=envVar.PASSWORD2))
users.append(User(id=3, username=envVar.USERNAME3, password=envVar.PASSWORD3))

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'


@app.before_request
def before_request():
	g.user = None
	
	if 'user_id' in session:
		user = [x for x in users if x.id == session['user_id']][0]
		g.user = user


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		session.pop('user_id', None)
		
		username = request.form['username']
		password = request.form['password']
		
		user = [x for x in users if x.username == username][0]
		if user and user.password == password:
			session['user_id'] = user.id
			return redirect(url_for('api'))
		else:
			return redirect(url_for('login'))
		
		return redirect(url_for('login'))
	
	return render_template('login.html')


@app.route('/api')
def api():
	if not g.user:
		return redirect(url_for('login'))
	return redirect('http://3.131.128.154:8081/dashboard/')
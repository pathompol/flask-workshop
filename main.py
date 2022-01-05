from flask import Flask,jsonify,render_template,request,redirect,url_for
from flask_login.utils import login_required
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,login_required,login_user,logout_user

app = Flask(__name__,template_folder='templates')
app.secret_key ='pp123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
# library
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


@app.route('/',methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/dashbord')
@login_required
def dashbord():
    return render_template('dashbord.html')

@app.route('/logout')
def logout():
    logout_user()
    return jsonify({'message':'logout success'}) 
    



# login
@app.route('/api/login_submit',methods=['POST'])
def login_submit():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if user:
       if user.password == password :
            login_user(user)
            return redirect(url_for('dashbord'))
       else: 
           print(1)
           return redirect('login.html')
    else:
        print(2)
        return redirect(url_for('login'))

    

if __name__ == '__main__':
    app.run(debug=True,port=8000)
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SenhaMtFoda'

bootstrap = Bootstrap(app)
moment = Moment(app)

# Formulário da página principal
class NameForm(FlaskForm):
    nome = StringField('Informe o seu nome:', validators=[DataRequired()])
    sobrenome = StringField('Informe o seu sobrenome:', validators=[DataRequired()])
    instituicao = StringField('Informe a sua instituição de ensino:', validators=[DataRequired()])
    disciplina = SelectField('Informe a sua disciplina:', choices=[
        ('DSWA5', 'DSWA5'),
        ('DSWA4', 'DSWA4'),
        ('DSWA3', 'DSWA3')
    ])
    submit = SubmitField('Submit')

# Formulário para a página de login
class LoginForm(FlaskForm):
    email = StringField('Usuário ou e-mail', validators=[DataRequired()])
    password = PasswordField('Informe a sua senha', validators=[DataRequired()])
    submit = SubmitField('Enviar')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['nome_completo'] = f"{form.nome.data} {form.sobrenome.data}"
        session['instituicao'] = form.instituicao.data
        session['disciplina'] = form.disciplina.data
        
        flash('Formulário enviado com sucesso!')
        
        return redirect(url_for('index'))

    user_ip = request.remote_addr
    host = request.host
    
    return render_template('index.html',
                           form=form,
                           nome_completo=session.get('nome_completo'),
                           instituicao=session.get('instituicao'),
                           disciplina=session.get('disciplina'),
                           user_ip=user_ip,
                           host=host,
                           current_time=datetime.utcnow())

# Rota de login 
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Guarda o e-mail na sessão
        session['email_login'] = form.email.data
        # Redireciona para a página de resposta
        return redirect(url_for('login_response'))
    return render_template('login.html', form=form)

# Exibe a resposta do login
@app.route('/loginResponse')
def login_response():
    
    email = session.get('email_login')
    # Renderiza o novo template, passando o e-mail para ele
    return render_template('login_response.html', email=email, current_time=datetime.utcnow())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



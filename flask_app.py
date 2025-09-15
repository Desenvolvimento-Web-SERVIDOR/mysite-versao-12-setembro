from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment # Garanta que esta linha existe
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
# Adicione a SECRET_KEY, como mostrado no slide de configuração
app.config['SECRET_KEY'] = 'senha mt foda'

bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('Qual o seu nome?', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Substitua sua função index() por esta versão final
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        # Verifica se o nome enviado é diferente do que está na sessão
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Parece que você alterou seu nome!')
        
        # Armazena o novo nome na sessão
        session['name'] = form.name.data
        # Redireciona para evitar reenvio do formulário
        return redirect(url_for('index'))
    
    # Renderiza o template, pegando o nome da sessão
    return render_template('index.html', form=form, name=session.get('name'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

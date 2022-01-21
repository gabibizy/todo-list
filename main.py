from app import app
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/todo_list'
db = SQLAlchemy(app)


class todo_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200))
    descrição = db.Column(db.String(500))
    completa = db.Column(db.Boolean)

@app.route('/')
def listar():
	try:
		lista = todo_list.query.all()
		return render_template('index.html', lista=lista)
	except Exception as e:
		print(e)
		

@app.route('/add', methods=['POST'])
def add_todo():
	try:
		todo = todo_list(titulo = request.form.get("titulo"))

		db.session.add(todo)
		db.session.commit()

		return redirect('/')
		
	except Exception as e:
		print('Erro', e)


@app.route('/select/<int:id>')
def select_by_id(id):
	try:
		todo = todo_list.query.filter_by(id=id).first()
		return render_template('index.html', todo=todo)
	except Exception as e:
		print(e)


@app.route('/update/<int:id>', methods=["POST"])
def update(id):
	todo = todo_list.query.filter_by(id=id).first() 

	todo.titulo = request.form.get("titulo")

	db.session.add(todo)
	db.session.commit()

	return redirect('/')

		
@app.route('/delete/<int:id>', methods=["POST"])
def delete(id):

	todo = todo_list.query.filter_by(id=id).first()
	try:
		db.session.delete(todo)
		db.session.commit()
		return redirect('/')

	except Exception as e:
		print('Erro', e)
		

if __name__ == "__main__":
    app.run(debug=True)
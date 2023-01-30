from flask import Flask, render_template, current_app, url_for, redirect, request, flash

from datetime import datetime


from database import Student_base, Session

app = Flask(__name__)
app.secret_key = "super secret key"

with app.app_context(): # создание контекста
    # within this block, current_app points to app.
    print(current_app.name)

session = Session()

#----------------------------ПРОВЕРКА ДАННЫХ ИЗ ВЕБ-ФОРМ В БД-------------------------------
def check_data(phonenumber, email, id=None): # проверяю только номер телефона  и почту, так как остальные поля могут быть идентичнымит
    if id == None: # если добавляется новый элемент
        if session.query(Student_base).filter_by(phonenumber=phonenumber).first() != None:
            flash("Данный номер телефона уже присутствует в базе данных!", "error")
            return False
        elif session.query(Student_base).filter_by(email=email).first() != None:
            flash("Данный email уже присутствует в базе данных!", "error")
            return False
        else:
            return True
    else: # если изменяется существующий элемент
        student = session.query(Student_base).filter_by(id=id).first()
        if (student.phonenumber != phonenumber and session.query(Student_base).filter_by(phonenumber=phonenumber).first() != None): # срабатыает когда человек меняет номер этот номер уже присутствуетв базе данных
            flash("Данный номер телефона уже присутствует в базе данных!", "error")
            return False
        elif (student.email != email and session.query(Student_base).filter_by(email=email).first() != None): # аналогмчно с комментом выше, только тут email
            flash("Данный email уже присутствует в базе данных!", "error")
            return False
        else:
            return True
#-------------------------------------------------------------------------------------


#----------------------------ИЗМЕНЕНИЕ ОБЪЕКТА В БД-----------------------------------
@app.route("/change/<int:id>", methods = ["GET"])
def display_change_student(id):
    student = session.query(Student_base).filter_by(id=id).first()
    return render_template("update_student.html", student=student)


@app.route("/change/<int:id>", methods = ["GET","POST"])
def change_student(id):
    student = session.query(Student_base).filter_by(id=id).first() # поиск студента по id
    name = request.form.get("name") # получение данных из фом
    surname = request.form.get("surname")
    dateofbirth = request.form.get("dateofbirth")
    phonenumber = request.form.get("phonenumber")
    email = request.form.get("email")

    dateofbirth = datetime.strptime(dateofbirth, '%Y-%m-%d')

    if check_data(phonenumber, email, id) == False:
        return redirect(url_for("change_student", id=id))

    student.name = name # перезапись данных
    student.surname = surname
    student.dateofbirth = dateofbirth
    student.phonenumber = phonenumber
    student.email = email

    session.commit() # сохранить изменения
    flash("Данные студента успешно измененны", "info")
    return redirect(url_for("show_students"))
#-------------------------------------------------------------------------------------


#----------------------------УДАЛЕНИЕ ОБЪЕКТА ИЗ БД-----------------------------------
@app.route("/delete/<int:id>", methods = ["GET","DELETE"])
def delete_student(id):
    student = session.query(Student_base).filter_by(id=id).first()
    session.delete(student)
    session.commit()
    flash("Данные студента успешно удалены", "info")
    return redirect(url_for("show_students"))
#-------------------------------------------------------------------------------------


#----------------------------ПОКАЗ ОБЪЕКТОВ ИЗ БД (СТУДЕНТОВ)-------------------------
@app.route("/", methods = ["GET"])
def show_students():
    students = session.query(Student_base).all()
    return render_template("students_all.html", students = students)
#-------------------------------------------------------------------------------------


#----------------------------ДОБАВЛЕНИЕ СТУДЕНТОВ В БД--------------------------------
@app.route("/", methods = ["POST"])
def add_students():
    name = request.form.get("name")
    surname = request.form.get("surname")
    dateofbirth = request.form.get("dateofbirth")
    number = request.form.get("phonenumber")
    email = request.form.get("email")

    dateofbirth = datetime.strptime(dateofbirth, '%Y-%m-%d')

    if check_data(number, email)==False:
        return redirect(url_for("show_students"))

    student = Student_base(name, surname, dateofbirth, number, email)
    session.add(student)
    session.commit()
    flash("Информация о студенте успешно добавлена в базу данных", "info")
    return redirect(url_for("show_students"))
#----------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
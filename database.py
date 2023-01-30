from sqlalchemy import create_engine, Column, String, INTEGER, Date

from sqlalchemy.orm import declarative_base, sessionmaker

#----------------------------СОЗДАНИЕ БАЗЫ ДАННЫХ-----------------------------------
engine = create_engine('sqlite:///instance/student_base.db?check_same_thread=False', echo=True)

Base = declarative_base()

class Student_base(Base):
    __tablename__ = "Students" # имя таблицы

    id = Column("id", INTEGER, primary_key=True)
    name = Column("Name", String, nullable=False) # string приравнивается к TEXT
    surname = Column("Surname", String, nullable=False)
    dateofbirth = Column("Date", Date, nullable=False)
    phonenumber = Column("Phone_number", String, nullable=False, unique=True) # проверить длину изменить ьип данных
    email = Column("email", String, nullable=False, unique=True)

    def __init__(self, name, surname, dateofbirth, phonenumber, email): # контсруктор класса (перегрузка создания экземпляра)

        self.name = name
        self.surname = surname
        self.dateofbirth = dateofbirth
        self.phonenumber = phonenumber
        self.email = email

    def __repr__(self):# магический метод для отображения информации об объекте класса в режиме отладки
        return f"{self.__class__}: {self.name}, {self.surname}, {self.dateofbirth}, {self.phonenumber}, {self.email}"

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine) # соединение с бд
#-------------------------------------------------------------------------------------
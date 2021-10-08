import re

import sqlalchemy
from sqlalchemy import exists, and_
from sqlalchemy.orm import joinedload, load_only, selectinload

from datetime import datetime
from db import session, engine
from models import Abonent, AbonentPhone

# декоратор  - обработчик ошибок
def input_error(func):
    def hundler(data):
        try:
            result = func(data)
        except Exception as e:
            return e
        return result
    return hundler


@input_error
def hello(data):
    print("How can I help you?")

#@input_error
def del_ph(data): #+
    # функция, которая удаляет номер телефона по имени
    # в data  должна  прийти строка, которая начинается с "del ph"
    # и содержит еще два "слова"  - имя  и телефон
    # "del ph " удаляется сразу
    data = data.replace('del ph ', '')
    #  действительно ли там есть два "слова" ?
    if len(data.split()) == 2:
        name, phone = data.split()
        phone = re.sub(r'[^\d]', '', phone)
        result = session.query(AbonentPhone.phone_id).\
            filter(AbonentPhone.phone==phone).\
            join(AbonentPhone.abonentp).\
            filter(Abonent.name == name).subquery()
        
        result_del = session.query(AbonentPhone).filter(AbonentPhone.phone_id.in_(result)) #([el.phone_id for el in result]))
        if result_del:

            result_del.delete(synchronize_session=False)
            session.commit()
                
        else:
            print('No result')


@input_error
def del_name(data): #-
    # удаление записи  по  имени
    data = data.replace('del ', '')
    if len(data.split()) == 1:
        name = data
        result = session.query(Abonent).\
            filter(Abonent.name==name).first()
        id = result.abonent_id
        print(id)

        if result : 
            #result.delete(synchronize_session=False)
            result = session.query(Abonent).get(id) 
            session.delete(result)
            session.commit()
            #for ab in result:
            #    ab.delete(synchronize_session=False)
        else:
            raise Exception("The abonent doesn't exist")
    else:
        raise Exception("Give me only name")


@input_error
def add_ph(data): #+
    # функция, которая добавляет номер телефона по имени
    # в data  должна  прийти строка, которая начинается с "add "
    # и содержит еще два "слова"  - имя  и телефон
    # "add ph " удаляется сразу
    data = data.replace('add ph ', '')
    #  действительно ли там есть два "слова" ?
    if len(data.split()) == 2:
        name, phone = data.split()
        phone = re.sub(r'[^\d]', '', phone)
        result = session.query(Abonent.abonent_id).filter(Abonent.name==name).first()
        print(type(result), result)
        #result = session.query(Abonent.abonent_id).filter(Abonent.name==name)
        #print(type(result), result)

        if not result:
            # добавляем в phone_book  нового абонента,
            result = Abonent(name = name)
            session.add(result)
            session.commit()
 
        # добавляем абоненту  один телефон
        ab_phone = AbonentPhone(abonent_id = result.abonent_id, phone = phone)
        session.add(ab_phone)
        session.commit()
    else:
        raise Exception("Give me name and phone please")

@input_error
def add_bd(data): #+
    # функция, которая добавляет день рождения по имени
    # в data  должна  прийти строка, которая начинается с "add "
    # и содержит еще два "слова"  - имя  и день рождения
    # "add bd " удаляется сразу
    data = data.replace('add bd ', '')

    #  действительно ли там есть два "слова" ?
    if len(data.split()) == 2:
        name, birthday = data.split()
        birthday = datetime(*map(int,re.split(r'[-,./]+',birthday)))

        result = session.query(Abonent.abonent_id, Abonent.birthday).\
            filter(Abonent.name==name).first()

        if not result:
            # добавляем   новую запись c датой рождения,
            result = Abonent(name = name, birthday = birthday)
            session.add(result)
            session.commit()

        # изменяем абоненту  дату рождения
        elif not result.birthday:
            session.query(Abonent).filter(Abonent.name==name).\
                update({Abonent.birthday : birthday}, synchronize_session=False)
            session.commit()
        #  если запись такая уже есть
        else:
            raise Exception("Abonent already has a birthday")

    else:
        raise Exception("Give me name and brthday please")

@input_error
def change_ph(data): #+
    #   чтобы изменить телефон. должна получить три слова
    #   name, phone, new_phone
    data = data.replace('change ph ', '')
    if len(data.split()) == 3:
        name, phone, new_phone = data.split()
        phone = re.sub(r'[^\d]', '', phone)
        new_phone = re.sub(r'[^\d]', '', new_phone)

        result = session.query(AbonentPhone).\
            filter(AbonentPhone.phone==phone).\
            join(AbonentPhone.abonentp).filter(Abonent.name== name)   
        if result:
            for el in result:
                el.phone = new_phone
            session.commit()
        else:
            raise Exception(f'The abonent {name} with phone {phone} not found')
    else:
        raise Exception("Give me name and phone please")

@input_error
def change_bd(data): #+
    #   изменить день рождения. должна получить два слова
    #   name,  new_birthday
    data = data.replace('change bd ', '')
    if len(data.split()) == 2:
        name,  new_birthday = data.split()
        birthday = datetime(*map(int,re.split(r'[-,./]+',new_birthday)))
        
        result = session.query(Abonent.abonent_id, Abonent.birthday).filter(Abonent.name==name).first()
        if result : 
            if  result.birthday:
                session.query(Abonent).\
                    filter(Abonent.name==name).\
                    update({Abonent.birthday : birthday}, synchronize_session=False)
                session.commit()
            else:
                print("The abonent doesn't have a birthday")

        else:
            raise Exception("The abonent doesn't exist")
    else:
        raise Exception("Give me name and birthday, please")


@input_error
def phone(data): #+
    # простая функция поиска записи  по  имени
    data = data.replace('phone ', '')
    if len(data.split()) == 1:
        name = data
        result = session.query(Abonent).\
            filter(Abonent.name==name).\
            options(joinedload('phones'))
        if result : 
            for ab in result:
                print(ab.name)
                for phone in ab.phones:
                    print(phone.phone)
                print()        
        else:
            raise Exception("The abonent doesn't exist")
    else:
        raise Exception("Give me only name")
    

@input_error
def show_all(data): #+
    data = data.replace('show all', '')
    result = session.query(Abonent).\
            options(joinedload('phones'))
    #  заготовка под пагинацию
    count_abonents = result.count()
    if len(data.split()) == 1:
        # проверка   - если параметр  N задан некорректно задаем ему 1
        try:
            N = int(data)
        except:
            N = 1
    else:
        # если не задан параметр N  считаем N равным длине словаря
        N = count_abonents
    l = 1 
    if result : 
        
        for ab in result:
            print(ab.name)
            for phone in ab.phones:
                print(phone.phone)
            print()

@input_error
def good_bye(data):
    # функция окончания работы и сохранения данных
    
    return "Good bye!"


ACTIONS = {
    'hello': hello,
    'add ph': add_ph,
    'add bd': add_bd,
    'change ph': change_ph,
    'change bd': change_bd,
    'del ph' : del_ph,
    'del' : del_name,
    'phone': phone,
    'show all': show_all,
    'good bye': good_bye,
    'close': good_bye,
    'exit': good_bye,
    '.': good_bye,
}


@input_error
def choice_action(data):
    for command in ACTIONS:
        if data.startswith(command):
            return ACTIONS[command]
    raise Exception("Give me a correct command please")


if __name__ == '__main__':

    while True:
        text = ''' You can:
        hello, good bye, close, exit, . - understandably
        add ph <name> <phone>
        add bd <name> <birthday>
        change ph <name> <phone> <new_phone>
        change bd <name> <new_birthday>
        del <name>
        del ph <name> <phone>
        show all  <N>    - show all abonent, N - number abonents in page
        phone <name>  - show all phone this abonent
        '''
        print(text)
        data = input()

        func = choice_action(data)
        if isinstance(func, Exception):
            print(func)
            continue
        result = func(data)
        if isinstance(result, sqlalchemy.orm.query.Query):
            for el in result:
                print('--------', el.name, el.address)

        if result:
            print(result)
        if result == 'Good bye!':
            break

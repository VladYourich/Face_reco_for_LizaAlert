from sqlalch import Callsign, add_items_to_callsign, sess, get_vectors
import os

СALLSIGN_ID     = {}
СALLSIGN_NAME   = {}

class СountСalls():
    '''
    класс-счётчик, используется для независимой нумерации файлов вырезанных фото лиц 
    из папки img
    '''
    def __init__(self, *args, **kwargs) -> None:
        pass

def fill_callnames(folder_path):
    """
    Заполним словарь ИД и Имя Поисковика для оптимизации дальнейшей обработки
    """
    global СALLSIGN_ID, СALLSIGN_NAME
    print(f'Содержимое СALLSIGN_ID /n',СALLSIGN_ID)
    print(f'Содержимое СALLSIGN_NAME /n',СALLSIGN_NAME)

    if СALLSIGN_ID == {} or СALLSIGN_NAME == {}:
        print(f'Заполняем словари СALLSIGN_ID, СALLSIGN_NAME')

        # Обход содержимого папки
        for root, dirs, files in os.walk(folder_path):
            for directory in dirs:
                
                # Разделение имени подкаталога по символу "_"
                parts = directory.split("_")

                # Проверка наличия двух частей
                if len(parts) == 2:
                    # Добавление записи в словарь
                    key = int(parts[0])
                    value = parts[1]
                    print(key,value)
                    СALLSIGN_ID[key]     = value
                    СALLSIGN_NAME[value] = key
    print(f'Содержимое СALLSIGN_ID /n',СALLSIGN_ID)
    print(f'Содержимое СALLSIGN_NAME /n',СALLSIGN_NAME)

    # Помещаем список в базу данных              
    items = [{"id":key, "callname": value} for key, value in СALLSIGN_ID.items()]
    print(items)
    add_items_to_callsign(items)

def get_all_calnames() -> dict: 
    global СALLSIGN_ID, СALLSIGN_NAME
    ses = sess()
    # Запрос к базе для получения получения всех позывных call_id
    
    result = (ses.query(Callsign.id, Callsign.callname).all())
    result_id = {callname: id for id, callname in result}
    result_name = {id:callname for id, callname in result}
    СALLSIGN_ID = result_id
    СALLSIGN_NAME   = result_name
    return result_id, result_name

def get_all_vectors() -> dict:
    vec = {}
    for name, id in СALLSIGN_NAME.items():
        #print(name, id)
        vec[name] = get_vectors(id)
    return vec

VECTORS = get_all_vectors()  # словарь со Всеми векторами всех поисковиков
COUNTCALL = СountСalls() # Создание экземпляря класса-счётчика

import numpy as np
import os
from enveronments import COUNTCALL, fill_callnames, СALLSIGN_ID, СALLSIGN_NAME
from face import OneFace 
from img_processing import extracting_one_face
#from sqlalch import add_items_to_callsign

def start_process_images(root_dir):
    """
    Первый этап обработки:
    Обходим все файлы в папке "img/in", находим файлы начинающиеся с "0" и 
    вырезаем одно лицо текущего поисковика, 
    помещаем файл с его лицом в папку "img/out/<Позывной>"
    Получаем вектора лица и помещаем в базу данных
    """
        
    # Создаем выходной каталог, если его нет
    output_dir = "img/out"
    os.makedirs(output_dir, exist_ok=True)

    # Обходим все файлы вложенных подкаталогов
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            # Отрабатываем только одиночные лица, для накопления базы векторов по Поисковику
            if file.startswith('0'): 
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    file_path = os.path.join(root, file)
                    print(f'[ИНФО] Обрабатывается файл - {file_path}')
                    # Извлекаем имя подкаталога и формируем имя подкаталога для сохранения
                    subdirectory_name = os.path.basename(root)
                    callname = subdirectory_name[3:]
                    output_subdirectory = os.path.join(output_dir, callname)

                    # Создаем подкаталог для сохранения, если его нет
                    os.makedirs(output_subdirectory, exist_ok=True)

                    if not hasattr(COUNTCALL, callname):
                        setattr(COUNTCALL, callname, 1)
                        count = 1
                    else:
                        cur_count = getattr(COUNTCALL, callname)
                        setattr(COUNTCALL, callname, cur_count+1)
                        count = getattr(COUNTCALL, callname)

                    # Вырезаем изображение лица и возвращаем путь к файлу для распознавания
                    path_to_face = extracting_one_face(file_path, output_subdirectory, callname)
                    print(f'[ИНФО] --- Создан файл с вырезанным лицом - {path_to_face}')

def fill_vectors_by_callsign():
    global СALLSIGN_ID, СALLSIGN_NAME

def begin_process():
    pass


def main():
    # Заполняем таблицу CallNames in DB
    fill_callnames("img/in")
    # Заполняем начальные вектора для каждого и распихиваем по папкам
    start_process_images("img/in")

if __name__ == '__main__':
    main()
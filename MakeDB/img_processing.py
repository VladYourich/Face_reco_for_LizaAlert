import numpy as np
import os
from PIL import Image, ImageDraw
from enveronments import СountСalls, COUNTCALL, VECTORS, СALLSIGN_NAME
from face import OneFace, Faces, OneFaceArray, recognition_one_face
from sqlalch import get_id_for_calname, add_vector

def extracting_faces(to_path):
    """
    Вырезает из img фрагмент входящий в bbox 
    и сохраняет по пути to_path с автоматической нумерацией новых файлов
    Возвращает текст пути к новому файлу
    """
    count = 1

    with open(f'{to_path}/count.txt', '+a') as f:
        for line in f.readline():
            count = int(line)

        bbox = OneFace.get_bbox

        for face_loc in bbox:
            top, right, bottom, left = face_loc
            
            face_img = OneFace.array_img[top:bottom, left:right]
            pil_img = Image.fromarray(face_img)
            #count = get_current_local_count(to_path)
            new_face_file_path = f'{to_path}/{count}.jpg'
            pil_img.save(new_face_file_path)
            count += 1
            break

    return new_face_file_path

def img_to_gray(path):
    img = Image.open(path)
    img_gray = img.convert("L")
    img_gray.save(path)

def extracting_one_face(path, to_path, callname):
    """
    Вырезает из img фрагмент входящий в bbox 
    и сохраняет по пути to_path с автоматической нумерацией новых файлов
    Возвращает текст пути к новому файлу
    """
    global COUNTCALL

    new_face_file_path = ''
    
    count = getattr(COUNTCALL, callname)

    img = OneFace(path)
    img.callname = callname
    bbox         = img.bbox
    vector       = img.vector
    call_id      = get_id_for_calname(callname)
    # add_vector(call_id, vector)
    if vector == []:
        print(f'[*ОШИБКА] ** Обрабатывался файл: {path}, Лицо не распозналось 8(_) ПРОВЕРИТЬ')
        return ''
    
    for face_loc in bbox:
        top, right, bottom, left = face_loc
        print(f'[ИНФО] - BBox - {face_loc}')
        face_img = img.array_img[top:bottom, left:right]
        pil_img = Image.fromarray(face_img)
        
        
        new_face_file_path = os.path.join(to_path, f'{count}.jpg') 
        pil_img.save(new_face_file_path)
        print(f'[ИНФО] -- Создали файл с лицом: {new_face_file_path}')
        
        # Добавляю в базу найденый вектор Поисковика
        add_vector(call_id, vector)
        
        break

    return new_face_file_path

def extracting_all_face(path, to_path, callname):
    """
    Вырезает из img фрагменты входящие в bbox's 
    распознаёт поисковика и сохраняет по пути img/out/Позывной 
    с автоматической нумерацией новых файлов
    Если поисковик не распознан, то вырезанное лицо помещается в папку img/all
    с автонумерацией файлов
    """
    global COUNTCALL, VECTORS
    files_from_img = {}
    files_from_img[callname] = []
    new_face_file_path = ''
    

    img = Faces(path)
    img.callname = callname
    bbox         = img.bbox
    vector       = img.vector
    #call_id      = get_id_for_calname(callname)
    # add_vector(call_id, vector)
    if len(bbox) == 0:
        print(f'[*ОШИБКА] ** Обрабатывался файл: {path}, Лица не распознались 8(_) ПРОВЕРИТЬ')
        return 'Лица не распознались'
    
    for face_loc in bbox:
        curr_path = to_path
        top, right, bottom, left = face_loc
        print(f'[ИНФО] - BBox - {face_loc}')
        face_img = img.array_img[top:bottom, left:right]
        # Распознаём лицо, определяем Позывной
        face = OneFaceArray(face_img)
        for call, face_vectors in VECTORS.items():
                rez = recognition_one_face(vector=face.vector, vectors=face_vectors[1], tolerance=0.6)    
                if rez == True:
                    callname = call
                    curr_path = f'out/{callname}'  

        if not hasattr(COUNTCALL, callname):
            setattr(COUNTCALL, callname, 1)
            count = 1
        cur_count = getattr(COUNTCALL, callname)
        # Проверяем на существование файла
        if os.path.exists(os.path.join(curr_path, f'{cur_count}_{callname}.jpg')):
            cur_count += 1
            while True: 
                if os.path.exists(os.path.join(curr_path, f'{cur_count}_{callname}.jpg')):
                    cur_count += 1    
                else:
                    break  
            #       
            setattr(COUNTCALL, callname, cur_count)
            count = getattr(COUNTCALL, callname)
        else:
            count = getattr(COUNTCALL, callname)        

        pil_img = Image.fromarray(face_img)

        new_face_file_path = os.path.join(curr_path, f'{count}_{callname}.jpg') 
        pil_img.save(new_face_file_path)
        files_from_img[callname].append(new_face_file_path)
        #print(f'[ИНФО] -- Создали файл с лицом: {new_face_file_path}')
        
        # Добавляю в базу найденый вектор Поисковика
        
    return files_from_img



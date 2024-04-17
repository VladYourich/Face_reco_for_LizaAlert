import face_recognition
import numpy as np
#from sqlalch import get_all_calnames, get_vectors, add_item, add_items

class BaseFace():
    img = None  # str - путь к файлу
    jit = 1
    model = "large"  # "small"  
    array_img = []
    bbox = []
    vector = []

    def __init__(self, img) -> None:
        self.img = img
 
    def get_array(self): 
        self.array_img = face_recognition.load_image_file(self.img)
        #print('get_array\n',self.array_img)
        return self.array_img

    def get_bbox(self): 
        self.bbox = face_recognition.face_locations(self.array_img)
        #print(self.bbox, type(self.bbox))
        return self.bbox

    def get_vector(self):
        self.vector = face_recognition.face_encodings(
            face_image=self.array_img, 
            known_face_locations=self.bbox, 
            num_jitters=self.jit, 
            model=self.model)
        #print('Base_get_vector\n', f'type - {type(self.vector)}\n', self.vector)
        return self.vector

class OneFace(BaseFace):
    """
    
    """
    top = 0.
    right = 0.
    bottom = 0.
    left = 0.
    callname = "Не определён"

    def __init__(self, img: str):
        super().__init__(img)
        self.img = img
        self.array_img = self.get_array()
        self.bbox = self.get_bbox()
        self.vector = self.get_vector()

    def __repr__(self):
        # return f"Поисковик - {self.callname}, bbox = {self.bbox}\n Vector:\n {self.vector},
        #         jit - {self.jit}, 
        #         model - {self.model},  
        #         ({[self.top,self.right,self.bottom,self.left]})
        #         "
        pass

    def recognition(self, known_face_encodings, tolerance=0.6) -> bool:
        #self.vector = self.get_vector()
        rez = face_recognition.compare_faces(
            known_face_encodings=known_face_encodings, 
            face_encoding_to_check=self.vector, 
            tolerance=tolerance)
        #print('One_recognition.', f'type - {type(rez)}\n', rez)
        return rez

class OneFaceArray(BaseFace):
    """
    
    """
    top = 0.
    right = 0.
    bottom = 0.
    left = 0.
    callname = "Не определён"

    def __init__(self, img):
        #self.img = img
        self.array_img = img
        self.bbox = self.get_bbox()
        self.vector = self.get_vector()

    def recognition(self, known_face_encodings, tolerance=0.6) -> bool:
        #self.vector = self.get_vector()
        if isinstance(known_face_encodings, list):
            for vector in known_face_encodings:
                if isinstance(vector, type(self.vector)):
                    rez = face_recognition.compare_faces(
                        known_face_encodings=vector, 
                        face_encoding_to_check=self.vector, 
                        tolerance=tolerance)
                else:
                    print()
        elif isinstance(known_face_encodings, self.vector):        
            rez = face_recognition.compare_faces(
                known_face_encodings=known_face_encodings, 
                face_encoding_to_check=self.vector, 
                tolerance=tolerance)
            #print('One_recognition.', f'type - {type(rez)}\n', rez)
        return rez

class Faces(BaseFace):
    def __init__(self, img):
        super().__init__(img)    
        self.img = img
        self.array_img = self.get_array()
        self.bbox = self.get_bbox()
        #self.vector = self.get_vector()

    def recognition(self, base_vectors, tolerance=0.6) -> bool:
        self.vector = self.get_vector()
        if self.vector.count > 1:
            vectors = {}
            for vec in self.vector:
                vectors['']
        rez = face_recognition.compare_faces(
            known_face_encodings=base_vectors, 
            face_encoding_to_check=self.vector, 
            tolerance=tolerance)
        return rez

def recognition_one_face(vector, vectors, tolerance) -> list:
    """
    Сверяет вектор со списком векторов одного поисковика
    """
    rez = face_recognition.compare_faces(
        known_face_encodings=vectors,
        face_encoding_to_check=vector,
        tolerance=tolerance)
    return rez
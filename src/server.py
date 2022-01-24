from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = [
    "http://127.0.0.1:5500",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Animal(BaseModel):
     id: Optional[str]
     nome: str
     idade: int
     sexo: str
     cor: str

bd: List[Animal] = []

@app.get("/animais")
def listar_animais():
     return bd

@app.get("/animais/{animal_id}")
def obter_animal(animal_id: str):
     for animal in bd:
          if animal.id == animal_id:
               return animal
     return {'error': 'Animal não encontrado'}


@app.delete("/animais/{animal_id}")
def remover_animal(animal_id: str):
     posicao = -1
     for index, animal in enumerate(bd):
          if animal.id == animal_id:
               posicao = index
               break

     if posicao != -1:
          bd.pop()
          return {'mensagem': 'Animal removido com sucesso'}
     else:
          return {'error': 'Animal não encontrado'}


@app.post("/animais")
def criar_animais(animal: Animal):
     animal.id = str(uuid4())
     bd.append(animal)
     return None



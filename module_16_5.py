# Задача "Список пользователей в шаблоне":


from fastapi import FastAPI, Request, HTTPException, Path
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from typing import Annotated, List

# app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)
app = FastAPI()

# Создайте объект Jinja2Templates, указав в качестве папки шаблонов - templates.

templates = Jinja2Templates(directory="templates")

users = []

class User(BaseModel):
    id: int
    username: str
    age: int

# Напишите новый запрос по маршруту '/':
# Функция по этому запросу должна принимать аргумент request и возвращать TemplateResponse.
# TemplateResponse должен подключать ранее заготовленный шаблон 'users.html', а также передавать в него request и
# список users.
# Ключи в словаре для передачи определите самостоятельно в соответствии с шаблоном.
@app.get("/", response_class=HTMLResponse)
async def get_tasks(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


# Измените get запрос по маршруту '/user' на '/user/{user_id}':
# Функция по этому запросу теперь принимает аргумент request и user_id.
# Вместо возврата объекта модели User, теперь возвращается объект TemplateResponse.
# TemplateResponse должен подключать ранее заготовленный шаблон 'users.html', а также передавать в него request и одного
# из пользователей - user. Ключи в словаре для передачи определите самостоятельно в соответствии с шаблоном.

@app.get("/users/{user_id}", response_class=HTMLResponse)
async def get_list(request: Request, user_id: Annotated[int, Path(ge=1)]):
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("index.html", {"request": request, "users": user})
    raise HTTPException(status_code=404, detail="User not found")


@app.post("/user/{username}/{age}")
async def new_user(username: str, age: int):
    id_new: int = max((t.id for t in users),default=0)+1
    new_user = User(id=id_new, username=username, age=age)
    users.append(new_user)
    return new_user

# put запрос по маршруту '/user/{user_id}/{username}/{age}' теперь:
# Обновляет username и age пользователя, если пользователь с таким user_id есть в списке users и возвращает его.
# В случае отсутствия пользователя выбрасывается исключение HTTPException с описанием "User was not found" и кодом 404.


@app.put("/user/{user_id}/{username}/{age}")
async def renew_user(user_id: int, username: str, age: int):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")


# delete запрос по маршруту '/user/{user_id}', теперь:
# Удаляет пользователя, если пользователь с таким user_id есть в списке users и возвращает его.
# В случае отсутствия пользователя выбрасывается исключение HTTPException с описанием "User was not found" и кодом 404.

@app.delete("/user/{user_id}")
async def del_user(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")


# python -m uvicorn module_16_5:app
